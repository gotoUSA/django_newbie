from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from ..models import Question


def index(request):
    page = request.GET.get("page", "1")
    kw = request.GET.get("kw", "")
    question_list = Question.objects.order_by("-create_date")
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw)
            | Q(content__icontains=kw)
            | Q(answer__content__icontains=kw)
            | Q(author__username__icontains=kw)
            | Q(answer__author__username__icontains=kw)
        ).distinct()
    paginator = Paginator(question_list, 10)
    max_index = len(paginator.page_range)
    page_obj = paginator.get_page(page)
    current_page = int(page)
    group_start = ((current_page - 1) // 5) * 5 + 1
    group_end = min(group_start + 4, paginator.num_pages)

    context = {
        "question_list": page_obj,
        "page": page,
        "kw": kw,
        "max_index": max_index,
        "group_start": group_start,
        "group_end": group_end,
    }
    return render(request, "pybo/question_list.html", context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {"question": question}
    return render(request, "pybo/question_detail.html", context)
