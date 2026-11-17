"""나의 여행 추구미 테스트 - 메인 앱 (2단계: 주요 기능)."""
import base64
import html
import json
import mimetypes
import time
from pathlib import Path

import streamlit as st

from data import QUESTIONS, RESULTS, TYPE_CODES
from logic import build_share_text, compute_scores, decide_result, score_percentages
from style import TYPE_COLORS, get_css

TOTAL = len(QUESTIONS)
IMAGE_DIR = Path(__file__).parent / "assets" / "images"


# ---------- 이미지 ----------
@st.cache_data(show_spinner=False)
def _read_image_uri(path_str):
    """이미지 파일을 base64 data URI로 변환 (결과 캐싱)."""
    path = Path(path_str)
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def image_uri(filename):
    """파일이 있으면 data URI, 없으면 None. (없음 결과는 캐싱하지 않아 나중에 추가해도 반영됨)"""
    path = IMAGE_DIR / filename
    if not path.is_file():
        return None
    try:
        return _read_image_uri(str(path))
    except OSError:
        return None


def hero_html(filename, fallback_emoji, alt, chip=None):
    """히어로 이미지 HTML. 파일이 없으면 그라데이션 + 이모지로 대체."""
    alt = html.escape(alt, quote=True)
    uri = image_uri(filename)
    if uri:
        inner = f'<img src="{uri}" alt="{alt}">'
    else:
        inner = f'<div class="hero-fallback" role="img" aria-label="{alt}">{fallback_emoji}</div>'
    chip_html = f'<span class="hero-chip">{html.escape(chip)}</span>' if chip else ""
    return f'<div class="hero">{inner}<div class="hero-fade"></div>{chip_html}</div>'


def show_html(slot, markup):
    """한 줄 HTML을 슬롯에 출력 (마크다운 코드블록 오해석 방지를 위해 개행 제거)."""
    slot.markdown(markup.replace("\n", ""), unsafe_allow_html=True)


def share_button_html(text):
    """결과 공유 버튼 HTML. 기기 공유창(Web Share)을 우선 쓰고, 없으면 클립보드 복사로 대체한다.
    st.iframe 안에서 실행되며, 공유 문구 뒤에 현재 앱 주소를 붙인다."""
    payload = json.dumps(text, ensure_ascii=False).replace("</", "<\\/")
    return """<!doctype html><html lang="ko"><head><meta charset="utf-8">
<style>
  html, body { margin: 0; background: transparent; }
  button { width: 100%; min-height: 56px; border-radius: 16px; border: 2px solid #F6DDE3; background: #fff;
    color: #3D2B35; font: 700 1rem "Pretendard Variable", Pretendard, "Malgun Gothic", sans-serif;
    cursor: pointer; transition: transform .15s, border-color .15s, box-shadow .15s, background .15s; }
  button:hover { transform: translateY(-2px); border-color: #FFB6C1; background: #FFF8F9;
    box-shadow: 0 8px 20px rgba(255,182,193,.35); }
  button:active { transform: scale(.98); background: #FFEFF2; }
  button:focus-visible { outline: 3px solid rgba(255,182,193,.6); outline-offset: 2px; }
</style></head><body>
<button id="share" type="button">📤 결과 공유하기</button>
<script>
const text = __PAYLOAD__;
const btn = document.getElementById("share");
const label = btn.textContent;
function flash(msg) { btn.textContent = msg; setTimeout(() => { btn.textContent = label; }, 2500); }
// 공유창은 모바일에서만 사용 (데스크톱 공유창은 어색하므로 바로 복사)
const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent) ||
  (navigator.maxTouchPoints > 1 && /Mac/.test(navigator.platform));
function pageUrl() { try { return window.parent.location.href; } catch (e) { return document.referrer || ""; } }
async function copy(t) {
  try { await navigator.clipboard.writeText(t); return true; } catch (e) {}
  try {
    const ta = document.createElement("textarea");
    ta.value = t; ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select();
    const ok = document.execCommand("copy");
    document.body.removeChild(ta);
    return ok;
  } catch (e) { return false; }
}
btn.addEventListener("click", async () => {
  const url = pageUrl();
  const full = url ? text + "\\n\\n나도 해보기 👉 " + url : text;
  if (navigator.share && isMobile) {
    try { await navigator.share({ title: "나의 여행 추구미 테스트", text: full }); return; }
    catch (e) { if (e && e.name === "AbortError") return; }
  }
  flash((await copy(full)) ? "✅ 복사되었어요! 붙여넣어 공유하세요" : "⚠️ 복사 실패: 위 공유 텍스트를 직접 복사해 주세요");
});
</script></body></html>""".replace("__PAYLOAD__", payload)


# ---------- 상태 ----------
def init_state():
    """세션 상태 초기화 (없는 키만 채움). 새로고침하면 시작 화면으로 복귀."""
    st.session_state.setdefault("stage", "start")  # start / quiz / loading / result
    st.session_state.setdefault("history", [])  # [(문항 id, 선택 라벨), ...]


def reset_state():
    """테스트 다시하기: 모든 상태 초기화."""
    st.session_state.stage = "start"
    st.session_state.history = []


def start_quiz():
    reset_state()
    st.session_state.stage = "quiz"


def current_index():
    """현재 문항 번호(0부터). 선택 이력 길이와 항상 일치하므로 중복 누적이 불가능."""
    return len(st.session_state.history)


def choose(question_id, label):
    """선택 콜백: 현재 문항에 대한 선택만 한 번 기록한다 (연타·오래된 클릭 무시)."""
    if st.session_state.stage != "quiz":
        return
    idx = current_index()
    if idx >= TOTAL or QUESTIONS[idx]["id"] != question_id:
        return
    st.session_state.history.append((question_id, label))
    if current_index() >= TOTAL:
        st.session_state.stage = "loading"


def go_back():
    """이전 문항으로: 직전 선택을 이력에서 제거(=점수 차감)."""
    if st.session_state.stage == "quiz" and st.session_state.history:
        st.session_state.history.pop()


# ---------- 화면 ----------
# Streamlit은 재실행 중 이전 실행의 위젯을 stale 상태로 남겨 둔다. 화면을 고정 개수의 슬롯에
# 그리고 쓰지 않는 슬롯은 비워 두면, 단계가 바뀔 때 이전 단계의 위젯이 즉시 덮어써진다.
SLOT_COUNT = 5


def render_start(slots):
    show_html(
        slots[0],
        '<div class="fx-fade">'
        + hero_html("start.jpg", "✈️", "여행 분위기의 파스텔 하늘")
        + '<div class="h1">✈️ 나의 여행 추구미 테스트</div>'
        '<p class="sub">16개의 질문으로 알아보는 나의 여행 스타일</p>'
        '<p class="meta">16문항 · 약 2분 소요</p></div>',
    )
    with slots[1]:
        st.button("테스트 시작하기", key="start_btn", on_click=start_quiz, use_container_width=True)


def render_quiz(slots):
    idx = current_index()
    if idx >= TOTAL:  # 방어: 비정상 상태면 결과로
        st.session_state.stage = "loading"
        st.rerun()
    q = QUESTIONS[idx]
    pct = round((idx + 1) / TOTAL * 100)
    prev_pct = round(idx / TOTAL * 100)
    show_html(
        slots[0],
        '<div class="p-head">'
        f'<span class="p-count">{idx + 1} <small>/ {TOTAL}</small></span>'
        f'<span class="p-pct">{pct}%</span></div>'
        '<div class="p-track">'
        f'<div class="p-fill" style="--from:{prev_pct}%;--to:{pct}%"></div></div>'
        '<div class="fx">'
        + hero_html(q["image"], q["emoji"], q["title"], chip=f"Q{q['id']}")
        + f'<div class="q-title"><span class="q-no">Q{q["id"]}.</span>{html.escape(q["title"])}</div></div>',
    )
    for i, c in enumerate(q["choices"]):
        with slots[1 + i]:
            st.button(
                f"{c['label']}. {c['text']}",
                key=f"choice_{q['id']}_{c['label']}",
                on_click=choose,
                args=(q["id"], c["label"]),
                use_container_width=True,
            )
    if idx > 0:
        with slots[3]:
            st.button("← 이전 문항", key=f"back_{q['id']}", on_click=go_back)


def render_loading(slots):
    show_html(
        slots[0],
        '<div class="loading"><div class="spinner"><span>✈️</span></div>'
        "<p>나의 여행 추구미를 분석 중입니다...</p></div>",
    )
    time.sleep(1.5)
    st.session_state.stage = "result"
    render_result(slots)  # 재실행 없이 같은 슬롯을 결과로 바로 교체 (빈 화면 틈 방지)


def render_result(slots):
    history = st.session_state.history
    if len(history) < TOTAL:  # 방어: 미완료 상태에서 결과로 온 경우
        reset_state()
        st.rerun()
    code = decide_result(history)
    r = RESULTS[code]
    percentages = score_percentages(compute_scores(history))
    accent = TYPE_COLORS[code]

    places = "".join(
        f'<span class="place" style="background:{accent}55">📍 {html.escape(p)}</span>'
        for p in r["places"]
    )
    top = max(percentages.values())
    bars = ""
    for t in TYPE_CODES:
        info = RESULTS[t]
        cls = "bar-top" if percentages[t] == top else ""
        bars += (
            f'<div class="{cls}"><div class="bar-row"><span>{info["emoji"]} {info["name"]}</span>'
            f'<b>{percentages[t]}%</b></div>'
            f'<div class="bar-track"><div class="bar-fill" '
            f'style="--to:{percentages[t]}%;background:{TYPE_COLORS[t]}"></div></div></div>'
        )

    show_html(
        slots[0],
        f'<div class="result" style="--accent:{accent}">'
        + hero_html(r["image"], r["emoji"], f"{r['name']} 대표 이미지")
        + '<div class="r-label">당신의 여행 추구미는</div>'
        f'<div class="r-title"><span>{r["emoji"]} {r["name"]}</span></div>'
        f'<div class="r-tag">"{html.escape(r["tagline"])}"</div>'
        f'<div class="r-desc">{html.escape(r["description"])}</div>'
        '<div class="sec">📍 어울리는 추천 여행지</div>'
        f'<div class="places">{places}</div>'
        '<div class="sec">📊 유형별 점수 분포</div>'
        f"{bars}"
        '<div class="sec">📋 결과 공유용 텍스트</div></div>',
    )
    with slots[1]:
        st.code(build_share_text(r, percentages), language=None, wrap_lines=True)
    with slots[2]:
        st.button("테스트 다시하기", key="restart_btn", on_click=reset_state, use_container_width=True)
    with slots[3]:  # 맨 뒤: 공유하기 버튼
        st.iframe(share_button_html(build_share_text(r, percentages)), height=64)


def main():
    st.set_page_config(page_title="나의 여행 추구미 테스트", page_icon="✈️")
    css = get_css()
    if css:
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    init_state()
    slots = [st.empty() for _ in range(SLOT_COUNT)]
    {
        "start": render_start,
        "quiz": render_quiz,
        "loading": render_loading,
        "result": render_result,
    }.get(st.session_state.stage, render_start)(slots)


main()
