from django.contrib.auth.models import User
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.response import Response
from frontend.models import  Assessment
from .models import Job, JobApplication, DevRequest
from accounts.models import Profile
from rest_framework.permissions import IsAuthenticated
from .serializers import DevRequestSerializer, JobRequestSerializer, JobApplicationsRequestSerializer, \
    JobApplicationsUpdaterSerializer, \
    DevRequestUpdaterSerializer, MyapplicantsRequestSerializer, \
    JobApplicationsRequestSerializerspecific, DevRequestSerializersimple

from rest_framework import generics
from frontend.serializers import AssesmentSerializer
from marketplace.tasks import send_email
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
import datetime

class DevRequestpick(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = DevRequest.objects.all()
    serializer_class = DevRequestUpdaterSerializer


class DevRequests(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DevRequestSerializer
    lookup_field = 'owner'

    def get_queryset(self):
        user_id = self.kwargs['owner']
        user = Profile.objects.get(id=user_id)
        return DevRequest.objects.filter(owner=user)


class DevRequestssimple(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DevRequestSerializersimple
    lookup_field = 'owner'

    def get_queryset(self):
        user_id = self.kwargs['owner']
        user = Profile.objects.get(id=user_id)
        return DevRequest.objects.filter(owner=user)


class MyApplicants(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MyapplicantsRequestSerializer

    def get_queryset(self):
        user_id = self.kwargs['owner']
        user = Profile.objects.get(id=user_id)

        return JobApplication.objects.select_related('job').filter(recruiter=user)


class Myjobapplication(generics.ListAPIView):
    serializer_class = JobApplicationsRequestSerializer

    def get_queryset(self):
        job_id = self.kwargs['job']
        candidate_id = self.kwargs['candidate']
        job = Job.objects.get(id=job_id)
        user = Profile.objects.get(id=candidate_id)
        return JobApplication.objects.filter(job=job).filter(candidate=user)


class JobsList(generics.ListCreateAPIView):
    queryset = Job.objects.all().order_by('-created')
    serializer_class = JobRequestSerializer


class JobsListverified(generics.ListCreateAPIView):
    queryset = Job.objects.exclude(verified=False).exclude(published=False).all().order_by('-created')
    serializer_class = JobRequestSerializer


class Alljobsdeadlinefilter(generics.ListCreateAPIView):
    queryset = Job.objects.filter(deadline__gte=datetime.datetime.now()).exclude(verified=False).exclude(
        published=False).all().order_by('-created')
    serializer_class = JobRequestSerializer


class Jobdetails(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobRequestSerializer


class Myjobsrequests(generics.ListAPIView):
    serializer_class = JobRequestSerializer

    def get_queryset(self):
        user_id = self.kwargs['posted_by']
        user = User.objects.get(id=user_id)
        if user.is_staff:
            return Job.objects.all().order_by('-created')
        else:
            return Job.objects.filter(posted_by=user).order_by('-created')


class Myjobsrequestssliced(generics.ListAPIView):
    serializer_class = JobRequestSerializer

    def get_queryset(self):
        user_id = self.kwargs['posted_by']
        user = User.objects.get(id=user_id)
        return Job.objects.filter(posted_by=user).order_by('-created')[:2]


class Jobsapplicants(generics.ListAPIView):
    serializer_class = MyapplicantsRequestSerializer

    def get_queryset(self):
        job_id = self.kwargs['job']
        job = Job.objects.get(id=job_id)
        return JobApplication.objects.select_related('job').filter(job=job)


class Specificjob(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobRequestSerializer


class SpecificJobsapplicants(generics.ListAPIView):
    serializer_class = JobApplicationsRequestSerializerspecific

    def get_queryset(self):
        job_id = self.kwargs['job']
        job = Job.objects.get(id=job_id)
        return JobApplication.objects.select_related('candidate').filter(job=job)


class JobUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Job.objects.all()
    serializer_class = JobRequestSerializer


class JobUnpublish(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Job.objects.all()
    serializer_class = JobRequestSerializer


class JobCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = JobRequestSerializer

    def get_queryset(self):
        return Job.objects.all()


class newonsite(generics.RetrieveAPIView):
    serializer_class = AssesmentSerializer

    def get_queryset(self):
        assesment_id = self.kwargs['pk']
        assesment = Assessment.objects.get(id=assesment_id)

        # candidate email

        subject = 'Codeln onsite assessment'
        html_message = render_to_string('invitations/email/onsite.html',
                                        {'center': assesment})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = [assesment.candidate.user.email]
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        # recruiter notification  email

        subject = 'New Onsite assessment applicant'
        html_message = render_to_string('invitations/email/onsitenotify.html',
                                        {'center': assesment})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = 'philisiah@codeln.com'
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return Assessment.objects.all()


class newpick(generics.RetrieveAPIView):
    serializer_class = JobApplicationsRequestSerializer

    def get_queryset(self):
        application_id = self.kwargs['pk']
        application = JobApplication.objects.get(id=application_id)

        # candidate email

        subject = 'Invitation to recruitment drive'
        html_message = render_to_string('invitations/email/invite.html',
                                        {'application': application})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = [application.candidate.user.email]
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return Assessment.objects.all()


class acceptreject(generics.RetrieveAPIView):
    serializer_class = JobApplicationsRequestSerializer

    def get_queryset(self):
        application_id = self.kwargs['pk']
        application = JobApplication.objects.get(id=application_id)

        # candidate email

        subject = 'Recruitment invitation status'
        html_message = render_to_string('invitations/email/Acceptance.html',
                                        {'application': application})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = [application.job.posted_by.email]
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return Assessment.objects.all()


class newjobapplication(generics.RetrieveAPIView):
    serializer_class = JobApplicationsRequestSerializer
    job_id = 0

    def get_queryset(self):
        application_id = self.kwargs['pk']
        application = JobApplication.objects.get(id=application_id)
        # recruiter notification  email

        # subject = application.job.title + ' ' + 'new applicant'
        # html_message = render_to_string('invitations/email/jobapplications.html',
        #                                 {'job': application.job})
        # plain_message = strip_tags(html_message)
        # from_email = 'codeln@codeln.com'
        # to = application.job.posted_by.email
        # mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        # candidate email

        subject = 'Application received'
        html_message = render_to_string('invitations/email/applynotifiy.html',
                                        {'dev': application.candidate.user, 'job': application.job})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = [application.candidate.user.email]
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return Job.objects.all()


class newjob(generics.RetrieveAPIView):
    serializer_class = JobRequestSerializer

    def get_queryset(self):
        job_id = self.kwargs['pk']
        job = Job.objects.get(id=job_id)
        # recruiter notification  email

        subject = job.title + ' ' + 'under review'
        html_message = render_to_string('invitations/email/jobreview.html',
                                        {'job': job})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = job.posted_by.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        # codeln notification email

        subject = 'Review new job'
        html_message = render_to_string('invitations/email/newjob.html',
                                        {'job': job})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = 'codeln@codeln.com'
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return Job.objects.all()


class recruiterpublished(generics.RetrieveAPIView):

    serializer_class = JobRequestSerializer

    def get_queryset(self):
        job_id = self.kwargs['pk']
        job = Job.objects.get(id=job_id)
        # recruiter notification  email

        subject = job.title + ' ' + 'has been published'
        html_message = render_to_string('invitations/email/jobreviewsuccess.html',
                                        {'job': job})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = job.posted_by.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return Job.objects.all()


class rejectionemail(generics.RetrieveAPIView):
    serializer_class = JobApplicationsRequestSerializer

    def get_queryset(self):
        application_id = self.kwargs['pk']
        application = JobApplication.objects.get(id=application_id)
        # candidate rejection  email

        subject = application.job.title + ' ' + 'Your application under job has been rejected'
        html_message = render_to_string('invitations/email/rejectionemail.html',
                                        {'application': application})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = application.candidate.user.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return Job.objects.all()

class pickedcandidateemail(generics.RetrieveAPIView):
    serializer_class = JobApplicationsRequestSerializer

    def get_queryset(self):
        application_id = self.kwargs['pk']
        application = JobApplication.objects.get(id=application_id)

        subject = 'Shortlisted for job'
        html_message = render_to_string('invitations/email/accepted.html',
                                        {'dev': application.candidate.user, 'application': application})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = [application.candidate.user.email]
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        return Job.objects.all()

class projectemail(generics.RetrieveAPIView):
    serializer_class = JobApplicationsRequestSerializer

    def get_queryset(self):
        application_id = self.kwargs['pk']
        application = JobApplication.objects.get(id=application_id)
        # candidate project asign  email

        subject = 'Your have been assigned a project under job  under job' + ' ' + application.job.title
        html_message = render_to_string('invitations/email/projectemail.html',
                                        {'application': application})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = application.candidate.user.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        return Job.objects.all()


class timesetemail(generics.RetrieveAPIView):
    serializer_class = JobApplicationsRequestSerializer

    def get_queryset(self):
        application_id = self.kwargs['pk']
        application = JobApplication.objects.get(id=application_id)
        # candidate project asign  email

        subject = 'Candidate has set time for project under job' + ' ' + application.job.title
        html_message = render_to_string('invitations/email/jobprojecttime.html',
                                        {'application': application})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = 'philisiah@codeln.com'
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return Job.objects.all()


class Applicationprofile(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationsRequestSerializer


class PickReject(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationsUpdaterSerializer


class PickRecommended(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationsUpdaterSerializer


class CandidateManager(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = DevRequest.objects.all()
    serializer_class = DevRequestUpdaterSerializer


class CandidateManagerInfo(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = DevRequest.objects.all()
    serializer_class = DevRequestSerializer



class JobApply(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationsUpdaterSerializer


class CandidateJobs(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = JobApplicationsRequestSerializer

    def get_queryset(self):
        candidate_id = self.kwargs['candidate']
        user = Profile.objects.get(id=candidate_id)
        return JobApplication.objects.filter(candidate=user)


class TalentPoolapplications(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DevRequestSerializer

    def get_queryset(self):
        candidate_id = self.kwargs['candidate']
        user = Profile.objects.get(id=candidate_id)
        return DevRequest.objects.filter(developer=user)


@api_view()
@permission_classes((permissions.AllowAny,))
def publishedemails(request, pk):

    send_email(pk)
    return Response({"message": "Hello, world!"})


