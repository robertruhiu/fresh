from marketplace.models import Job

from projects.models import Project,Framework
from rest_framework.permissions import IsAuthenticated
from .serializers import Projectserializer,FrameworkSerializer
from rest_framework import generics
import random
from django.contrib.auth.models import User
from marketplace.models import JobApplication,DevRequest
from accounts.models import Profile
from frontend.models import Assessment



class Projects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer
    def get_queryset(self):
        job_id = self.kwargs['id']
        job = Job.objects.get(id=job_id)
        projects = Project.objects.all()
        tags = job.tech_stack.split(",")
        randomlist =[]
        for oneproject  in projects :
            for onetag in tags:
                if oneproject.tags.find(onetag.lower()):
                    randomlist.append(oneproject.id)

        if len(randomlist) > 0:
            projectid = random.choice(randomlist)
        else:
            projectid = randomlist[0]


        return Project.objects.filter(pk=projectid)

class RecommendedProjects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer
    def get_queryset(self):
        user_id = self.kwargs['id']
        user = User.objects.get(pk=user_id)
        userprofile = Profile.objects.get(user=user)
        projects = Project.objects.all()
        tags = userprofile.skills.split(",")


        randomlists =[]
        for oneproject  in projects :
            for onetag in tags:

                if onetag.lower() in oneproject.tags.lower():
                    randomlists.append(oneproject.id)
        randomlist = list(set(randomlists))

        if len(randomlist) > 0:
            projectid = random.choice(randomlist)
        else:
            projectid = randomlist[0]

        return Project.objects.filter(pk=projectid)

class BasicProject(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer
    def get_queryset(self):


        user_id = self.kwargs['dev_id']
        user = Profile.objects.get(pk=user_id)
        # enable filter to ensure non repeat already done project in assessment
        doneprojects = Assessment.objects.filter(candidate=user)
        donelist =[]
        for onedoneproject in doneprojects:
            donelist.append(onedoneproject.project.id)

        projects = Project.objects.all()

        randomlists =[]
        for oneproject  in projects :
            if oneproject.level == 'Basic':
                randomlists.append(oneproject.id)


        randomlistinitial = list(set(randomlists))

        randomlist =list(set(randomlistinitial)-set(donelist))

        if len(randomlist) > 0:
            projectid = random.choice(randomlist)
        else:
            projectid = randomlist[0]

        return Project.objects.filter(pk=projectid)
class SelfverifyProject(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer
    def get_queryset(self):
        framework = self.kwargs['framework']

        user_id = self.kwargs['dev_id']
        user = Profile.objects.get(pk=user_id)
        # enable filter to ensure non repeat already done project in assessment
        doneprojects = Assessment.objects.filter(candidate=user)
        donelist =[]
        for onedoneproject in doneprojects:
            donelist.append(onedoneproject.project.id)

        projects = Project.objects.all()

        randomlists =[]
        for oneproject  in projects :
            if oneproject.tags:
                if framework.lower() in oneproject.tags.lower():
                    randomlists.append(oneproject.id)
        randomlistinitial = list(set(randomlists))

        randomlist =list(set(randomlistinitial)-set(donelist))

        if len(randomlist) > 0:
            projectid = random.choice(randomlist)
        else:
            projectid = randomlist[0]

        return Project.objects.filter(pk=projectid)

class Allprojects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = Projectserializer

class ProjectDetails(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = Projectserializer

class RecentProjects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer
    def get_queryset(self):
        user_id = self.kwargs['id']
        user = Profile.objects.get(pk=user_id)
        recentprojects = JobApplication.objects.select_related('recruiter').filter(recruiter=user)
        project_ids = []
        for oneproject in recentprojects:
            if oneproject.project:
                project_ids.append(oneproject.project.id)
                return Project.objects.filter(pk__in=project_ids)

class MyRecentProjects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer
    def get_queryset(self):
        user_id = self.kwargs['id']
        user = Profile.objects.get(pk=user_id)
        recentprojects = DevRequest.objects.filter(owner=user)[:2]
        project_ids = []
        for oneproject in recentprojects:
            project_ids.append(oneproject.project)
        return project_ids

class Frameworks(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FrameworkSerializer
    queryset = Framework.objects.all()

# developer api views
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from frontend.models import AssessmentReport
from  frontend.serializers import AssesmentReportSerializer

class DeveloperProjects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer
    def get_queryset(self):
        framework = self.kwargs['framework']

        developerprojects = Project.objects.filter(framework__name=framework)
        return developerprojects


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def developerprojectreport(request, candidate_id, project_id):
    candidate = Profile.objects.get(id=candidate_id)
    project = Project.objects.get(id=project_id)
    candidate.verified_skills = project.tags
    candidate.save()
    report = AssessmentReport.objects.filter(candidate=candidate.user).filter(project=project).get()
    serializer = AssesmentReportSerializer(report)
    return Response(serializer.data)







