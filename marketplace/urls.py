from django.urls import path

from marketplace.views import  Myjobsrequests, Jobsapplicants, \
    Specificjob, SpecificJobsapplicants, Myjobapplication, JobUpdate, JobCreate, PickReject, PickRecommended, \
    JobUnpublish, \
    DevRequestpick, DevRequests, CandidateManager, MyApplicants, Jobdetails, JobApply, CandidateJobs, \
    TalentPoolapplications, Applicationprofile, CandidateManagerInfo, \
    Myjobsrequestssliced, \
    JobsListverified, DevRequestssimple, newjobapplication, newjob, newonsite, newpick, acceptreject, publishedemails,\
    Alljobsdeadlinefilter,recruiterpublished,rejectionemail,projectemail,timesetemail,pickedcandidateemail

app_name = 'marketplace'

urlpatterns = [


    path('mydevs/<int:owner>', DevRequests.as_view()),
    path('mydevssimple/<int:owner>', DevRequestssimple.as_view()),
    path('myapplicants/<int:owner>', MyApplicants.as_view()),
    path('pickdev', DevRequestpick.as_view()),
    path('myjobs/<int:posted_by>', Myjobsrequests.as_view()),
    path('myjobssliced/<int:posted_by>', Myjobsrequestssliced.as_view()),
    path('jobapplicants/<int:job>', Jobsapplicants.as_view()),

    path('specificjob/<int:pk>', Specificjob.as_view()),
    path('specificjobapplicants/<int:job>', SpecificJobsapplicants.as_view()),
    path('updatejob/<int:pk>', JobUpdate.as_view()),
    path('unpublishjob/<int:pk>', JobUnpublish.as_view()),
    path('pickreject/<int:pk>', PickReject.as_view()),
    path('applicationprofile/<int:pk>', Applicationprofile.as_view()),
    path('candidateinfoupdater/<int:pk>', CandidateManager.as_view()),
    path('candidateinfo/<int:pk>', CandidateManagerInfo.as_view()),
    path('pickrecommended', PickRecommended.as_view()),
    path('createjob', JobCreate.as_view()),
    path('alljobs', JobsListverified.as_view()),
    path('alljobsdeadlinefilter', Alljobsdeadlinefilter.as_view()),

    path('myjobapplication/<int:candidate>/<int:job>', Myjobapplication.as_view()),
    path('jobdetails/<int:pk>', Jobdetails.as_view()),
    path('applyjob', JobApply.as_view()),
    path('candidatejobs/<int:candidate>', CandidateJobs.as_view()),
    path('pickedapplications/<int:candidate>', TalentPoolapplications.as_view()),


    path('newjobapplication/<int:pk>', newjobapplication.as_view()),
    path('newonsite/<int:pk>', newonsite.as_view()),
    path('newjobemail/<int:pk>', newjob.as_view()),
    path('newpick/<int:pk>', newpick.as_view()),
    path('acceptreject/<int:pk>', acceptreject.as_view()),
    path('publishedemails/<int:pk>', publishedemails, name='publishedemails'),
    path('recruiterpublished/<int:pk>', recruiterpublished.as_view(), name='recruiterpublished'),
    path('rejectionemail/<int:pk>', rejectionemail.as_view(), name='rejectionemail'),
    path('pickedcandidateemail/<int:pk>', pickedcandidateemail.as_view(), name='pickedcandidateemail'),
    path('projectemail/<int:pk>', projectemail.as_view()),
    path('timesetemail/<int:pk>', timesetemail.as_view()),





]
