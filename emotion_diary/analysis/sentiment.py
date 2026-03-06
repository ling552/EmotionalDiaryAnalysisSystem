import re
from dataclasses import dataclass
from typing import Dict, Iterable, Tuple


@dataclass(frozen=True)
class SentimentResult:
    emotion: str
    score: int


_POSITIVE: Dict[str, int] = {
    '开心': 2,
    '快乐': 2,
    '高兴': 2,
    '满足': 2,
    '兴奋': 2,
    '顺利': 1,
    '喜欢': 1,
    '感恩': 2,
    '放松': 1,
    '轻松': 1,
}

_NEGATIVE: Dict[str, int] = {
    '难过': 2,
    '伤心': 2,
    '失落': 2,
    '沮丧': 2,
    '烦': 1,
    '生气': 2,
    '愤怒': 2,
    '压力': 2,
    '焦虑': 2,
    '紧张': 1,
    '崩溃': 3,
    '疲惫': 1,
}

_NEUTRAL: Dict[str, int] = {
    '平静': 1,
    '一般': 1,
    '还好': 1,
    '普通': 1,
}


def _tokenize(text: str) -> Iterable[str]:
    if not text:
        return []
    text = re.sub(r"\s+", " ", text)
    tokens = []
    for word in list(_POSITIVE.keys()) + list(_NEGATIVE.keys()) + list(_NEUTRAL.keys()):
        if word in text:
            tokens.append(word)
    return tokens


def analyze_text(text: str) -> SentimentResult:
    tokens = list(_tokenize(text))

    pos = sum(_POSITIVE.get(t, 0) for t in tokens)
    neg = sum(_NEGATIVE.get(t, 0) for t in tokens)
    neu = sum(_NEUTRAL.get(t, 0) for t in tokens)

    score = pos - neg

    if neg >= 3 and neg > pos:
        emotion = '焦虑' if any(t in tokens for t in ['焦虑', '压力', '紧张']) else '难过'
    elif score >= 2:
        emotion = '开心'
    elif abs(score) <= 1 and neu > 0:
        emotion = '平静'
    elif score <= -2:
        emotion = '难过'
    else:
        emotion = '平静' if neu > 0 else '未知'

    return SentimentResult(emotion=emotion, score=score)


def emotion_suggestion(emotion: str, recent_negative_days: int = 0) -> str:
    if recent_negative_days >= 3:
        return '最近你的负面情绪偏多，建议适当休息，减少高强度任务，并尝试与朋友交流或进行轻度运动。'
    if emotion in {'焦虑'}:
        return '最近你的压力较大，建议适当休息。可以尝试运动、冥想或听音乐来放松心情。'
    if emotion in {'难过'}:
        return '你可能有些难过或疲惫，建议给自己一点时间，做一些能带来舒适感的小事，比如散步或整理房间。'
    if emotion in {'开心'}:
        return '你的状态很不错，继续保持规律作息和积极的生活节奏，把这份好心情延续下去。'
    return '你的情绪较为稳定，保持良好生活状态，规律作息，适当运动。'


def aggregate_emotions(items: Iterable[Tuple[str, int]]) -> Dict[str, int]:
    result: Dict[str, int] = {}
    for emotion, count in items:
        result[emotion] = result.get(emotion, 0) + int(count)
    return result
