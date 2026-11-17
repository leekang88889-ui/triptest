"""커스텀 CSS (3단계): 인스타 감성 파스텔 카드 UI."""

# 결과 유형별 포인트 컬러 (힐링=민트, 배낭=피치, 맛집=핑크, 인스타=라벤더)
TYPE_COLORS = {
    "H": "#B5EAD7",
    "B": "#FFD6A5",
    "F": "#FFB6C1",
    "I": "#CDB4DB",
}

_CSS = """
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.css");

:root {
  --pink: #FFB6C1; --peach: #FFD6A5; --mint: #B5EAD7; --lavender: #CDB4DB;
  --text: #4A4A4A; --muted: #6B6B76; --accent-text: #B8486A; --btn-text: #3D2B35;
}

/* ---------- 기본/배경/폰트 ---------- */
html, body, .stApp, .stApp button, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp code {
  font-family: "Pretendard Variable", Pretendard, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
}
.stApp {
  background: linear-gradient(160deg, #FFF1F0 0%, #FBEAF5 50%, #F3E8FF 100%);
  background-attachment: fixed;
  color: var(--text);
}
[data-testid="stAppViewContainer"], [data-testid="stMain"] { background: transparent; }

/* 기본 헤더/푸터/메뉴 숨김 */
#MainMenu, footer, header[data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; visibility: hidden; }

/* ---------- 카드 레이아웃 ---------- */
.stMain .block-container, [data-testid="stMainBlockContainer"] {
  max-width: 480px !important;
  margin: 1.5rem auto !important;
  padding: 1.1rem 1.2rem 1.8rem !important;
  background: #FFFFFF;
  border-radius: 28px;
  box-shadow: 0 12px 40px rgba(205, 180, 219, .35);
}
@media (max-width: 520px) {
  .stMain .block-container, [data-testid="stMainBlockContainer"] {
    width: calc(100% - 1.2rem) !important;
    margin: .6rem auto 1.2rem !important;
    padding: 1rem .95rem 1.5rem !important;
    border-radius: 22px;
  }
}

/* ---------- 애니메이션 ---------- */
@keyframes fadeUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes grow { from { width: var(--from, 0%); } to { width: var(--to, 100%); } }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes pulse { 0%, 100% { transform: scale(1); opacity: .85; } 50% { transform: scale(1.18); opacity: 1; } }
.fx { animation: fadeUp .5s ease both; }
.fx-fade { animation: fadeIn .55s ease both; }

/* ---------- 히어로 이미지 ---------- */
.hero { position: relative; border-radius: 20px; overflow: hidden; height: 200px; }
.hero img { width: 100%; height: 100%; object-fit: cover; display: block;
  filter: saturate(1.05) brightness(1.04) contrast(.96); }
.hero::before { content: ""; position: absolute; inset: 0; z-index: 1; pointer-events: none;
  background: rgba(255, 214, 224, .16); }                       /* 파스텔 톤 오버레이 */
.hero-fade { position: absolute; left: 0; right: 0; bottom: 0; height: 45%; z-index: 2; pointer-events: none;
  background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,.92)); }
.hero-fallback { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
  font-size: 72px; background: linear-gradient(135deg, #FFE3E6 0%, #F3E8FF 55%, #DDF5EB 100%); }
.hero-chip { position: absolute; top: 12px; left: 12px; z-index: 3; padding: 4px 12px; border-radius: 999px;
  background: rgba(255,255,255,.88); color: var(--text); font-size: .8rem; font-weight: 700;
  box-shadow: 0 2px 8px rgba(0,0,0,.08); }

/* ---------- 진행 바 ---------- */
.p-head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 6px; }
.p-count { font-weight: 800; font-size: 1.05rem; color: var(--text); }
.p-count small { font-weight: 600; color: var(--muted); }
.p-pct { font-size: .85rem; font-weight: 700; color: var(--accent-text); }
.p-track { height: 10px; border-radius: 999px; background: #F4EDF7; overflow: hidden; margin-bottom: 14px; }
.p-fill { height: 100%; border-radius: 999px; width: var(--to);
  background: linear-gradient(90deg, #FFB6C1, #FFD6A5 50%, #CDB4DB);
  animation: grow .6s ease both; }

/* ---------- 텍스트 ---------- */
.q-title { font-size: 1.35rem; font-weight: 800; line-height: 1.4; margin: 14px 2px 14px; color: var(--text); }
.q-no { color: var(--accent-text); margin-right: 4px; }
.h1 { font-size: 1.7rem; font-weight: 800; line-height: 1.3; margin: 18px 0 8px; text-align: center; color: var(--text); }
.sub { text-align: center; color: var(--muted); font-size: 1rem; margin: 0 0 6px; }
.meta { text-align: center; color: #6F6478; font-size: .85rem; margin: 0 0 18px; }

/* ---------- 버튼 (선택지/시작/다시하기/이전) ---------- */
.stApp .stButton > button {
  min-height: 56px; height: auto; border-radius: 16px; padding: .8rem 1rem;
  border: 2px solid #F6DDE3; background: #FFFFFF; color: var(--text);
  box-shadow: 0 2px 8px rgba(0,0,0,.03);
  transition: transform .15s ease, border-color .15s ease, box-shadow .15s ease, background .15s ease;
}
.stApp .stButton > button p { margin: 0; font-size: 1rem; line-height: 1.45; font-weight: 600;
  white-space: normal; word-break: keep-all; }
.stApp .stButton > button:hover { transform: translateY(-2px); border-color: var(--pink);
  background: #FFF8F9; color: var(--text); box-shadow: 0 8px 20px rgba(255,182,193,.35); }
.stApp .stButton > button:active { transform: scale(.98); border-color: var(--pink); background: #FFEFF2; color: var(--text); }
.stApp .stButton > button:focus:not(:active) { border-color: var(--pink); color: var(--text); box-shadow: 0 0 0 3px rgba(255,182,193,.35); }

div[class*="st-key-choice_"] { animation: fadeUp .5s ease both; }
div[class*="st-key-choice_"]:nth-of-type(2) { animation-delay: .06s; }

.stApp div[class*="st-key-start_btn"] button, .stApp div[class*="st-key-restart_btn"] button {
  min-height: 60px; border: none; color: var(--btn-text);
  background: linear-gradient(135deg, #FFA9BA 0%, #E3A8D8 55%, #CDB4DB 100%);
  box-shadow: 0 8px 22px rgba(229,138,160,.4);
}
.stApp div[class*="st-key-start_btn"] button p, .stApp div[class*="st-key-restart_btn"] button p { color: var(--btn-text); font-size: 1.1rem; font-weight: 800; }
.stApp div[class*="st-key-start_btn"] button:hover, .stApp div[class*="st-key-restart_btn"] button:hover,
.stApp div[class*="st-key-start_btn"] button:focus:not(:active), .stApp div[class*="st-key-restart_btn"] button:focus:not(:active) {
  border: none; color: var(--btn-text); filter: brightness(1.04);
  background: linear-gradient(135deg, #FFA9BA 0%, #E3A8D8 55%, #CDB4DB 100%);
  box-shadow: 0 12px 28px rgba(229,138,160,.5);
}
.stApp div[class*="st-key-start_btn"] button:active, .stApp div[class*="st-key-restart_btn"] button:active {
  border: none; color: var(--btn-text); background: linear-gradient(135deg, #FF98AD 0%, #D998CF 55%, #C2A5D3 100%);
}

.stApp div[class*="st-key-back_"] button { min-height: 40px; background: transparent; border: none; box-shadow: none; }
.stApp div[class*="st-key-back_"] button p { color: var(--muted); font-size: .9rem; font-weight: 600; }
.stApp div[class*="st-key-back_"] button:hover { background: #F7F1FA; box-shadow: none; transform: none; }

/* ---------- 로딩 ---------- */
.loading { text-align: center; padding: 70px 0 60px; animation: fadeIn .4s ease both; }
.spinner { width: 74px; height: 74px; margin: 0 auto 22px; border-radius: 50%;
  border: 6px solid #F4EDF7; border-top-color: #FFB6C1; border-right-color: #CDB4DB;
  animation: spin 1s linear infinite; display: flex; align-items: center; justify-content: center; }
.spinner span { font-size: 28px; animation: pulse 1.2s ease-in-out infinite; transform-origin: center; }
.loading p { font-size: 1.1rem; font-weight: 700; color: var(--text); margin: 0; }

/* ---------- 결과 ---------- */
.result { animation: fadeUp .7s ease both; }
.r-label { text-align: center; color: var(--muted); font-size: .95rem; margin: 16px 0 2px; }
.r-title { text-align: center; font-size: 2rem; font-weight: 800; margin: 0 0 6px; color: var(--text); }
.r-title span { background: linear-gradient(transparent 62%, var(--accent) 62%); padding: 0 6px; }
.r-tag { text-align: center; font-size: 1.05rem; font-weight: 700; color: var(--accent-text); margin: 0 0 14px; }
.r-desc { font-size: 1rem; line-height: 1.7; color: var(--text); background: #FFFAFB;
  border-radius: 16px; padding: 14px 16px; margin: 0 0 18px; word-break: keep-all; }
.sec { font-size: 1.05rem; font-weight: 800; margin: 18px 0 10px; color: var(--text); }
.places { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 6px; }
.place { padding: 8px 14px; border-radius: 999px; font-size: .92rem; font-weight: 700; color: var(--text); }
.bar-row { display: flex; justify-content: space-between; font-size: .92rem; font-weight: 600; margin: 10px 0 4px; }
.bar-row b { font-weight: 800; }
.bar-track { height: 12px; border-radius: 999px; background: #F4EDF7; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 999px; width: var(--to); animation: grow .9s ease both; }
.bar-top .bar-row { color: var(--accent-text); }

/* 공유 텍스트 코드블록 */
.stApp [data-testid="stCode"] { border-radius: 14px; }

@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
"""


def get_css() -> str:
    return _CSS
