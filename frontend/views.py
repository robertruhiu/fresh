import json
import requests
from cryptography.fernet import Fernet
from decouple import config
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import mail

from django.db.models import Count, CharField
from django.db.models.functions import  Length
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.forms import Profile
from accounts.models import Referral, ReferralCode

from frontend.form import  EditProjectForm

from frontend.models import  Portfolio, Experience, Assessment, Resources
from marketplace.models import Job
from projects.models import Project
from .serializers import UserSerializer, ProfileSerializer, ExperienceSerializer, ProjectSerializer, \
     AssesmentSerializer, AssesmentSerializerUpdater, ProfileSerializerUpdater, ProjectSerializerupdater, \
    ExperienceSerializerupdater, AssesmentSerializermini, ResourceSerializer, \
    ResourceSerializercreater, ResourceSerializerupdater, ReferralCodeSerializer

CharField.register_lookup(Length, 'length')

filteredcandidates = []
# filteredcandidates = Profile.objects.select_related('user').exclude(about__isnull=True).exclude(skills__isnull=True).exclude(student=True).filter(user_type='developer')
candidate_list =[]
for onecandidate in filteredcandidates:
    candidate_list.append(onecandidate.pk)

taken = []
portfolio = []
experience = []
# taken = TakenQuiz.objects.select_related('student').filter(pk__in=candidate_list)
# portfolio = Portfolio.objects.select_related('candidate').filter(pk__in=candidate_list)
# experience = Experience.objects.select_related('candidate').filter(pk__in=candidate_list)
takenlist =[]
portfoliolist=[]
experiencelist=[]
for onetaken in taken:
    takenlist.append(onetaken.student.id)
for oneportfolio in portfolio:
    portfoliolist.append(oneportfolio.candidate.id)
for oneexperience in experience:
    experiencelist.append(oneexperience.candidate.id)
candidateslist = list(set(portfoliolist+experiencelist+takenlist))


def Talentorder(request):
    order_list =[]


    combolist = portfoliolist + experiencelist


    for one_in_combo in combolist:
        if one_in_combo in takenlist:
            takenlist.remove(one_in_combo)

        order_list = combolist + takenlist


    return HttpResponse(json.dumps(order_list), content_type="application/json")
class UserList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = ProfileSerializer

    def get_queryset(self):

        return Profile.objects.select_related('user').exclude(about__isnull=True).exclude(skills__isnull=True).filter(user_type='developer')

class Alldevs(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.select_related('user').filter(user_type='developer').order_by('-user__date_joined')

class Allrecruiters(generics.ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.select_related('user').filter(user_type='recruiter').order_by('-user__date_joined')
@login_required
def DevList(request):


    response = requests.get('https://codelnapi.herokuapp.com/alldevs')
    data = response.json()


    return render(request, 'frontend/recruiter/devlist.html', {'developers':data})

@login_required
def RecruiterList(request):


    response = requests.get('https://codelnapi.herokuapp.com/allrecruiters')
    data = response.json()

    return render(request, 'frontend/recruiter/recruiterslist.html', {'payers': data})




class UserListsliced(generics.ListAPIView):

    serializer_class = ProfileSerializer

    def get_queryset(self):
        customlist =config('TOPTIER', default='TOPTIER').split(",")

        return Profile.objects.exclude(about__isnull=True).exclude(skills__isnull=True).filter(about__length__gt=100).filter(user_type='developer').filter(pk__in=customlist)
class AllUsers(generics.ListAPIView):

    serializer_class = UserSerializer

    def get_queryset(self):

        return User.objects.all()


class Portfolioget(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        candidate_id = self.kwargs['candidate_id']
        user = Profile.objects.get(id=candidate_id)
        return Portfolio.objects.select_related('candidate').filter(candidate_id=user)

class Portfoliocreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Portfolio.objects.all()
    serializer_class = ProjectSerializerupdater

class Portfolioupdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Portfolio.objects.all()
    serializer_class = ProjectSerializerupdater

class Experienceget(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExperienceSerializer

    def get_queryset(self):

        candidate_id = self.kwargs['candidate_id']
        user = Profile.objects.get(id=candidate_id)
        return Experience.objects.select_related('candidate').filter(candidate=user)

class Experiencecreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializerupdater

class Experienceupdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializerupdater

class Profileget(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class Userget(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializerUpdater


# class ReferralCodeCreate(APIView):
#     # permission_classes = (Is,)
#     queryset = ReferralCode.objects.all()
#
#     def get(self, request):
#         user = Profile.objects.get(id=request.data.get('id'))
#         new_code = ReferralCode.objects.create(user=user)
#         return Response({'message': f'Your referral code is {new_code.code}'})

class ReferralCodeCreate(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = ReferralCode.objects.all()
    serializer_class = ReferralCodeSerializer

    def get(self, request, pk, **kwargs):
        user = Profile.objects.get(user_id=pk)
        new_code = ReferralCode.objects.create(user=user)
        return Response({'message': f'Your referral code is {new_code.code}'})


class ReferralCreate(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Referral.objects.all()

    def post(self, request):
        code = request.data.get('referral_code')
        referred = Profile.objects.get(request.data.get('referred_id'))
        referrer = ReferralCode.objects.get(code=code).user
        Referral.objects.create(referrer=referrer, referred=referred)
        return Response({'message': 'referral code accepted!'})



class SelfAssesmentCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Assessment.objects.all()
    serializer_class = AssesmentSerializerUpdater

class MySelfAssesments(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AssesmentSerializermini
    def get_queryset(self):
        candidate_id = self.kwargs['candidate_id']

        return Assessment.objects.select_related('project').exclude(project__isnull=True).filter(candidate_id=candidate_id)
class Mytestcenters(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AssesmentSerializermini
    def get_queryset(self):
        candidate_id = self.kwargs['candidate_id']

        return Assessment.objects.select_related('project').filter(candidate_id=candidate_id)

class MySelfAssesmentsproject(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Assessment.objects.all()
    serializer_class = AssesmentSerializer

class MySelfAssesmentsprojectupdater(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Assessment.objects.all()
    serializer_class = AssesmentSerializerUpdater

class Timesetemail(generics.RetrieveAPIView):
    serializer_class = AssesmentSerializer

    def get_queryset(self):
        assesment_id = self.kwargs['pk']
        assesment = Assessment.objects.get(id=assesment_id)

        # recruiter notification  email

        subject = 'New online assessment applicant'
        html_message = render_to_string('invitations/email/online.html',
                                        {'center': assesment})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = 'philisiah@codeln.com'
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return Assessment.objects.all()
class Newuser(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        User = Profile.objects.get(id=user_id)
        if User.user_type == 'developer':
            subject = 'Welcome to Codeln'
            html_message = render_to_string('invitations/email/newusers.html')
            plain_message = strip_tags(html_message)
            from_email = 'codeln@codeln.com'
            to = User.user.email
            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        else:
            subject = 'Welcome to Codeln'
            html_message = render_to_string('invitations/email/newuserrecruiter.html')
            plain_message = strip_tags(html_message)
            from_email = 'codeln@codeln.com'
            to = User.user.email
            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


        return Assessment.objects.all()

@api_view()
@permission_classes((permissions.AllowAny,))
def unsubscribe(request,token):
    key = config('KEY', default='KEY').encode()
    # message = "1".encode()
    # print(type(str(token[2:-1]).encode()))
    user_token = token[2:-1].encode()

    f = Fernet(key)

    decrypted = f.decrypt(user_token)
    currentprofile = Profile.objects.get(pk=int(decrypted))
    currentprofile.notifications = False
    currentprofile.save()


    return HttpResponse(currentprofile)

class Resourcecreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Resources.objects.all()
    serializer_class = ResourceSerializercreater

class Subjectresources(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResourceSerializer
    def get_queryset(self):
        subject_id = self.kwargs['subject']

        return Resources.objects.select_related('subject').exclude(verified=False).filter(subject__id=subject_id)

class Resourceslikeupdate(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ResourceSerializerupdater
    queryset = Resources.objects.all()

class Portfoliolikeupdate(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializerupdater
    queryset = Portfolio.objects.all()






def index(request):
    if request.user.is_authenticated:
        current_profile = request.user.profile

        if request.user.profile.stage == 'complete':
            if request.user.profile.user_type == 'developer':
                return render(request, 'frontend/developer/developer.html',)

            elif request.user.profile.user_type == 'recruiter':

                return render(request, 'frontend/recruiter/recruiter.html',)
    else:
        return home(request)


def home(request):


    return render(request, 'frontend/landing.html')


def page_404(request,exception=None):
    return render(request, 'frontend/error_pages/404.html')


def page_500(request):
    return render(request, 'frontend/error_pages/500.html')




@login_required
def manageprojects(request):
    projects = Project.objects.all()
    return render(request, 'frontend/recruiter/projects.html', {'projects': projects})

@login_required
def editproject(request, project_id):
    instance = get_object_or_404(Project, id=project_id)
    project = Project.objects.get(id=project_id)
    form = EditProjectForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('frontend:manageprojects')

    return render(request, 'frontend/recruiter/editproject.html',
                  {'project': project, 'form': form})

@login_required
def deleteproject(request, project_id):
    Project.objects.filter(id=project_id).delete()
    return redirect('frontend:manageprojects')
@login_required
def addproject(request):
    form = EditProjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('frontend:manageprojects')
    return render(request, 'frontend/recruiter/addproject.html',
                  { 'form': form})








@login_required
def management(request):
    jobs=Job.objects.all()

    return render(request, 'frontend/recruiter/management.html',{'jobs':jobs})


from .tasks import send_notification

def testcelery(request):
    send_notification()
    return HttpResponse('completed')




