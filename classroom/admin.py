from django.contrib import admin
from classroom.models import Quiz,StudentAnswer,Answer,TakenQuiz,Subject,Question,RandomQuiz

admin.site.register(Quiz)
admin.site.register(StudentAnswer)
admin.site.register(Answer)
admin.site.register(TakenQuiz)
admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(RandomQuiz)
