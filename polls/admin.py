from django.contrib import admin

from polls.models import Board, Question, Choice


# Register your models here.


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', 'start_time', 'end_time', 'activate')
    readonly_fields = ('created_at',)  # created_at 필드를 읽기 전용으로 설정


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'board')


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'votes')