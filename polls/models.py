from django.db import models
from django.contrib.auth.models import User

class Media(models.Model):
    MEDIA_TYPES = [('image', 'Image'), ('video', 'Video')]
    type = models.CharField(max_length=5, choices=MEDIA_TYPES)
    url = models.URLField()

    def is_image(self):
        return self.type == 'image'

    def is_video(self):
        return self.type == 'video'

class Board(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def add_question(self, text, media=None):
        return Question.objects.create(board=self, text=text, media=media)

    def get_stats(self):
        questions = self.question_set.all()
        total_votes = sum(choice.votes for question in questions for choice in question.choice_set.all())
        return {"questions": len(questions), "total_votes": total_votes}

class Question(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    text = models.TextField()
    media = models.OneToOneField(Media, on_delete=models.CASCADE, null=True, blank=True)

    def add_choice(self, text):
        return Choice.objects.create(question=self, text=text)

    def cast_vote(self, choice_id):
        choice = self.choice_set.get(id=choice_id)
        choice.increment_votes()

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def increment_votes(self):
        self.votes += 1
        self.save()
