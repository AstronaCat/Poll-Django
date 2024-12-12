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
        questions = board.question_set.all()  # board와 연결된 모든 질문 가져오기
        # 각 질문에 대한 choice를 함께 가져옴
        for question in questions:
            question.choices = question.choice_set.all()  # choice들을 속성으로 추가

        context = {
            'sub_title': '보드 수정',
            'board': board,
            'questions': questions,  # question과 그에 연결된 choice들 포함
        }
        return render(request, 'polls/board_modify.html', context)
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


@login_required
@csrf_exempt
def api_create_question(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        board = Board.objects.get(id=data.get("board_id"))
        question = Question.objects.create(
            board=board,
            text=data.get("text"),
            media_type=data.get("media_type"),
            media_url=data.get("media_url")
        )

        count = 0
        for i in range(1, 10):
            answer = data.get(f"answer{i}")
            if not answer:
                break
            Choice.objects.create(
                question=question,
                text=answer
            )
            count += 1

        return JsonResponse({'id': question.id, 'name': question.text, 'answwers': count}, status=201)  # 생성된 객체 반환
