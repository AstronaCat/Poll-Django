from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Board, Question, Choice
from django.contrib.auth.decorators import login_required
import json



def dashboard(request):
    boards = Board.objects.filter(activate=True, completed=False).order_by('-created_at').prefetch_related(
        Prefetch('question_set', queryset=Question.objects.order_by('id'), to_attr='questions')
    )
    return render(request, 'polls/dashboard.html', {'boards': boards})


@login_required
def my_page(request):
    # boards = Board.objects.filter(created_by=request.user).order_by('-created_at')
    boards = Board.objects.filter(created_by=request.user).order_by('-created_at').prefetch_related(
        Prefetch('question_set', queryset=Question.objects.order_by('id'), to_attr='questions')
    )
    return render(request, 'polls/my_page.html', {'boards': boards})


def done_page(request):
    boards = Board.objects.filter(completed=True).order_by('-created_at').prefetch_related(
        Prefetch('question_set', queryset=Question.objects.order_by('id'), to_attr='questions')
    )

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

def board_vote(request, id):
    try:
        # URL 경로에서 받은 id 값으로 해당 board 찾기
        board = Board.objects.get(id=id)
        questions = board.question_set.all()  # board와 연결된 모든 질문 가져오기
        # 각 질문에 대한 choice를 함께 가져옴
        ids = []
        for question in questions:
            question.choices = question.choice_set.all()  # choice들을 속성으로 추가
            ids.append(question.id)

        context = {
            'sub_title': '투표하기',
            'board': board,
            'questions': questions,  # question과 그에 연결된 choice들 포함
            'question_ids': ids
        }
        return render(request, 'polls/board_vote.html', context)
    except Board.DoesNotExist:
        return HttpResponse('Board not found', status=404)


def board_result(request, id):
    try:
        # URL 경로에서 받은 id 값으로 해당 board 찾기
        board = Board.objects.get(id=id)
        questions = board.question_set.all()  # board와 연결된 모든 질문 가져오기
        # 각 질문에 대한 choice를 함께 가져옴
        chart_data = []
        for question in questions:
            question.choices = question.choice_set.all()  # choice들을 속성으로 추가
            chart_data.append({
                "question_id": question.id,
                "choice_labels": [choice.text for choice in question.choices],
                "choice_count": [choice.votes for choice in question.choices]
            })

        chart_data_json = json.dumps(chart_data)  # JSON 문자열로 변환
        context = {
            'sub_title': '투표 결과 보기',
            'board': board,
            'questions': questions,  # question과 그에 연결된 choice들 포함
            'chart_data': chart_data_json
        }
        return render(request, 'polls/board_result.html', context)
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
def api_modify_board(request):
    if request.method == "POST":
        data = json.loads(request.body)
        board = Board.objects.get(id=data.get('board_id'))
        board.name = data.get('name')
        board.start_time = data.get('start_time') or None
        board.end_time  = data.get('end_time') or None
        board.activate = data.get('activate', False)
        board.completed = data.get('completed', False)

        board.save()
        return JsonResponse({'id': board.id, 'name': board.name}, status=201)  # 생성된 객체 반환


@login_required
@csrf_exempt
def api_vote_board(request):
    if request.method == "POST":
        data = json.loads(request.body)

        for item in data:
            q = item.get('question')
            a = item.get('answer')
            print(f"q={q}, a={a}")
            choice = Choice.objects.get(id=a)
            choice.increment_votes()

        return JsonResponse({'count': len(data)}, status=201)  # 생성된 객체 반환


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
