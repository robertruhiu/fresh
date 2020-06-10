
from django.db.models import Count

from django.shortcuts import get_object_or_404, redirect, render

from ..models import Quiz, TakenQuiz, User,StudentAnswer,Answer,Subject,RandomQuiz,Question
import random

from rest_framework import generics
from ..serializers import QuizSerializer,TakenQuizSerializer,RandomQuizSerializer,QuestionSerializer,StudentAnswerSerializer,SubjectSerializer
from accounts.models import Profile
from rest_framework.permissions import IsAuthenticated
class AllQuizzes(generics.ListAPIView):

    serializer_class = QuizSerializer
    def get_queryset(self):


        return Quiz.objects.all() \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)

class TakenQuizzes(generics.ListAPIView):
    serializer_class = TakenQuizSerializer
    def get_queryset(self):
        candidate_id = self.kwargs['candidate']
        user = Profile.objects.get(pk=candidate_id)
        return TakenQuiz.objects.filter(user=user)

class QuizQuestions(generics.ListAPIView):
    serializer_class = QuestionSerializer
    def get_queryset(self):
        quiz_id = self.kwargs['quiz']
        return Question.objects.filter(quiz_id=quiz_id)

class TakeQuiz(generics.ListAPIView):
    serializer_class = RandomQuizSerializer
    def get_queryset(self):

        candidate_id = self.kwargs['candidate']
        quiz_id = self.kwargs['quiz']

        quiz = get_object_or_404(Quiz, pk=quiz_id)
        student = Profile.objects.get(id=candidate_id)


        questionlist = []
        quizzes = RandomQuiz.objects.filter(student_id=student.id).filter(quiz_id=quiz_id)
        if len(quizzes) >0:
            return quizzes
        else:
            currentquiz = Question.objects.filter(quiz_id=quiz_id)
            for onequestion in currentquiz:
                questionlist.append(onequestion.id)

            questionrandomlist = random.sample(questionlist, 30)
            questions= ','.join(map(str, questionrandomlist))


            obj = RandomQuiz(quiz=quiz, student=student, questions=questions)
            obj.save()
            return RandomQuiz.objects.filter(student_id=student.id).filter(quiz_id=quiz_id)

class PostAnswer(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer

class Subjects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class UpdateRandomquiz(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = RandomQuiz.objects.all()
    serializer_class = RandomQuizSerializer

class CalculateScore(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TakenQuizSerializer

    def get_queryset(self):
        candidate_id = self.kwargs['candidate']
        quiz_id = self.kwargs['quiz']
        student = Profile.objects.get(id=candidate_id)
        quiz = Quiz.objects.get(id=quiz_id)

        correctanswercounter = StudentAnswer.objects.filter(quiz=quiz, student=student, answer__is_correct=True).count()
        score = (correctanswercounter / 30) * 100
        TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
        return TakenQuiz.objects.filter(student=student)

class Taken(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TakenQuizSerializer

    def get_queryset(self):
        candidate_id = self.kwargs['candidate']
        student = Profile.objects.get(id=candidate_id)
        return TakenQuiz.objects.filter(student=student)






