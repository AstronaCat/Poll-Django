from django.contrib import admin

from polls.models import Board, Question, Choice


# Register your models here.


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('board', 'text', 'media')


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'votes')