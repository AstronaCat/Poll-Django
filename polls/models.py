from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def add_question(self, text, media=None):
        return Question.objects.create(board=self, text=text, media=media)

    def get_stats(self):
        questions = self.question_set.all()
        total_votes = sum(choice.votes for question in questions for choice in question.choice_set.all())
        return {"questions": len(questions), "total_votes": total_votes}

    def __str__(self):
        return self.name


class Question(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    text = models.TextField()

    MEDIA_TYPES = [('image', 'Image'), ('video', 'Video')]
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES, null=True, blank=True)
    media_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.text} of {self.board}"

    def has_image(self):
        return self.media_type == 'image'

    def has_video(self):
        return self.media_type == 'video'

    def add_choice(self, text):
        return Choice.objects.create(question=self, text=text)

    # cast_vote() function 수정 필요
    def cast_vote(self, choice_id):
        choice = self.choice_set.get(id=choice_id)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text
    
    def increment_votes(self):
        self.votes += 1
        self.save()
