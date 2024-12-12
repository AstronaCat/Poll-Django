from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Board, Question, Choice
from django.contrib.auth.decorators import login_required
import json



def dashboard(request):
    boards = Board.objects.all()
    for board in boards:
        board.has_image = any(q.has_image() for q in board.question_set.all())
        board.has_video = any(q.has_video() for q in board.question_set.all())
    return render(request, 'polls/dashboard.html', {'boards': boards})


@login_required
def my_page(request):
    boards = Board.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'polls/my_page.html', {'boards': boards})


def done_page(request):
    # #TODO 완료된 것으로 필터링
    boards = Board.objects.filter()
    return render(request, 'polls/done_page.html', {'boards': boards})

def board_modify(request, id):
    try:
        # URL 경로에서 받은 id 값으로 해당 board 찾기
        board = Board.objects.get(id=id)
        return render(request, 'polls/board_modify.html', {'board': board, 'sub_title': '보드 수정'})
    except Board.DoesNotExist:
        return HttpResponse('Board not found', status=404)


def vote(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == "POST":
        choice_id = request.POST['choice']
        question.cast_vote(choice_id)
        return redirect('dashboard')
    return render(request, 'polls/vote.html', {'question': question})


@login_required
@csrf_exempt
def api_create_board(request):
    if request.method == "POST":
        data = json.loads(request.body)
        new_board = Board.objects.create(
            name=data.get('name'),
            created_by=request.user,
            start_time=data.get('start_time') or None,
            end_time=data.get('end_time') or None,
            activate=data.get('activate', False),
        )
        return JsonResponse({'id': new_board.id, 'name': new_board.name}, status=201)  # 생성된 객체 반환
