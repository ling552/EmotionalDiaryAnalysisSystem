from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from diary.models import Diary

from .sentiment import emotion_suggestion


@login_required
def analysis_dashboard_view(request):
    diaries = list(Diary.objects.filter(user=request.user).order_by('-create_time')[:60])
    recent_30 = list(reversed(diaries[:30]))

    labels = [d.create_time.strftime('%m-%d') for d in recent_30]
    scores = [int(d.score) for d in recent_30]

    emotion_counts = {}
    for d in diaries:
        emotion_counts[d.emotion] = emotion_counts.get(d.emotion, 0) + 1

    negative_streak = 0
    for d in diaries[:7]:
        if d.emotion in {'难过', '焦虑'}:
            negative_streak += 1
        else:
            break

    latest_emotion = diaries[0].emotion if diaries else '未知'
    suggestion = emotion_suggestion(latest_emotion, recent_negative_days=negative_streak)

    chart_data = {
        'labels': labels,
        'scores': scores,
        'emotion_counts': emotion_counts,
    }

    return render(
        request,
        'analysis.html',
        {
            'chart_data': chart_data,
            'suggestion': suggestion,
        },
    )
