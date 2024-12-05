from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Question, Choice
from django.contrib.auth.decorators import login_required


@login_required
def create_board(request):
    if request.method == "POST":
        name = request.POST.get('name')
        Board.objects.create(name=name, created_by=request.user)
        return redirect('dashboard')
    return render(request, 'polls/create_board.html')



def dashboard(request):
    boards = Board.objects.all()
    for board in boards:
        board.has_image = any(q.has_image() for q in board.question_set.all())
        board.has_video = any(q.has_video() for q in board.question_set.all())
    return render(request, 'polls/dashboard.html', {'boards': boards})



def vote(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == "POST":
        choice_id = request.POST['choice']
        question.cast_vote(choice_id)
        return redirect('dashboard')
    return render(request, 'polls/vote.html', {'question': question})
