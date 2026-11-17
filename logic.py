"""점수 계산·판정 순수 함수 (Streamlit 비의존, pytest 대상).

선택 이력(history)을 단일 진실 공급원으로 삼는다.
history: [(question_id, choice_label), ...]  예) [(1, "A"), (2, "B")]
이전 문항 되돌리기는 history.pop()만 하면 점수/동점 판정이 자동으로 일관된다.
"""
from data import QUESTIONS, TYPE_CODES


def choice_type(question_id, label, questions=QUESTIONS):
    """문항 id와 선택지 라벨(A/B)에 매핑된 유형 코드를 반환."""
    for q in questions:
        if q["id"] == question_id:
            for c in q["choices"]:
                if c["label"] == label:
                    return c["type"]
    raise ValueError(f"알 수 없는 선택: Q{question_id} {label}")


def compute_scores(history, questions=QUESTIONS):
    """선택 이력으로부터 유형별 점수를 계산."""
    scores = {c: 0 for c in TYPE_CODES}
    for qid, label in history:
        scores[choice_type(qid, label, questions)] += 1
    return scores


def decide_result(history, questions=QUESTIONS):
    """최고 점수 유형 판정. 동점이면 동점 유형 중 가장 최근에 선택한 유형 우선."""
    scores = compute_scores(history, questions)
    top = max(scores.values())
    winners = [c for c, s in scores.items() if s == top]
    if len(winners) == 1:
        return winners[0]
    for qid, label in reversed(history):
        t = choice_type(qid, label, questions)
        if t in winners:
            return t
    return winners[0]  # 이력이 비어 있는 경우(전부 0점)


def score_percentages(scores):
    """점수를 합계 100%가 되도록 정수 %로 변환 (최대잔여법). 합계 0이면 전부 0."""
    total = sum(scores.values())
    if total == 0:
        return {c: 0 for c in scores}
    raw = {c: scores[c] * 100 / total for c in scores}
    pct = {c: int(v) for c, v in raw.items()}
    remain = 100 - sum(pct.values())
    for c in sorted(raw, key=lambda k: raw[k] - pct[k], reverse=True)[:remain]:
        pct[c] += 1
    return pct


def build_share_text(result, percentages):
    """결과 공유용 텍스트 생성. result는 data.RESULTS의 한 항목."""
    lines = [
        "✈️ 나의 여행 추구미 테스트 결과",
        f"{result['emoji']} {result['name']} - \"{result['tagline']}\"",
        "",
        "📍 추천 여행지: " + ", ".join(result["places"]),
        "",
        "점수 분포",
    ]
    for code in TYPE_CODES:
        lines.append(f"- {code}: {percentages[code]}%")
    return "\n".join(lines)
