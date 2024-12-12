from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    name = models.CharField(max_length=100, verbose_name='보드의 이름')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='보드 생성자')
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='투표 시작시각')  # 시작 시간
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='투표 종료시각')    # 종료 시간
    activate = models.BooleanField(default=False, verbose_name='보드 활성화')             # 활성화 여부
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성 시각')  # 자동으로 생성 시간 입력

    @property
    def question_count(self):
        return self.question_set.count()

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

    @property
    def video_id(self):
        if self.media_type == 'video' and self.media_url:
            return self.media_url[-11:]  # https://www.youtube.com/watch?v=llaMn3OZGn8  에서 뒤 11자리가 ID임.
        else:
            return None

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
