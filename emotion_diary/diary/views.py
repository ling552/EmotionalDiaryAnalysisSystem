from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.utils import timezone

from analysis.sentiment import analyze_text
from .models import Diary


@login_required
def diary_list_view(request):
    qs = Diary.objects.filter(user=request.user)

    date_str = (request.GET.get('date') or '').strip()
    if date_str:
        try:
            d = datetime.strptime(date_str, '%Y-%m-%d').date()
            start = timezone.make_aware(datetime.combine(d, datetime.min.time()))
            end = timezone.make_aware(datetime.combine(d, datetime.max.time()))
            qs = qs.filter(create_time__range=(start, end))
        except ValueError:
            messages.error(request, '日期格式不正确。')

    q = (request.GET.get('q') or '').strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))

    return render(
        request,
        'diary_list.html',
        {
            'diaries': qs[:200],
            'date': date_str,
            'q': q,
        },
    )


@login_required
def diary_add_view(request):
    if request.method == 'POST':
        title = (request.POST.get('title') or '').strip()
        content = (request.POST.get('content') or '').strip()

        if not title:
            messages.error(request, '请输入日记标题。')
            return render(request, 'diary_add.html', {'title': title, 'content': content})
        if not content:
            messages.error(request, '请输入日记内容。')
            return render(request, 'diary_add.html', {'title': title, 'content': content})

        r = analyze_text(content)
        Diary.objects.create(
            user=request.user,
            title=title,
            content=content,
            emotion=r.emotion,
            score=r.score,
        )
        messages.success(request, '保存成功。')
        return redirect('diary_list')

    return render(request, 'diary_add.html')


@login_required
def diary_edit_view(request, diary_id: int):
    try:
        diary = Diary.objects.get(id=diary_id, user=request.user)
    except Diary.DoesNotExist as e:
        raise Http404 from e

    if request.method == 'POST':
        title = (request.POST.get('title') or '').strip()
        content = (request.POST.get('content') or '').strip()
        if not title:
            messages.error(request, '请输入日记标题。')
        elif not content:
            messages.error(request, '请输入日记内容。')
        else:
            r = analyze_text(content)
            diary.title = title
            diary.content = content
            diary.emotion = r.emotion
            diary.score = r.score
            diary.save(update_fields=['title', 'content', 'emotion', 'score', 'update_time'])
            messages.success(request, '修改成功。')
            return redirect('diary_list')

    return render(request, 'diary_edit.html', {'diary': diary})


@login_required
def diary_delete_view(request, diary_id: int):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    deleted, _ = Diary.objects.filter(id=diary_id, user=request.user).delete()
    if deleted:
        messages.success(request, '删除成功。')
    else:
        messages.error(request, '日记不存在或无权限。')
    return redirect('diary_list')
