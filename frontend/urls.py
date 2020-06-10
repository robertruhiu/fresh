from django.urls import path

from frontend.views import index, UserList
from frontend.views import home,manageprojects,\
    editproject,deleteproject,addproject\
    ,portfolio,experience,\
    management,ProfileUpdate,Profileget,Experienceget,\
    Portfolioget,AllUsers,Userget,SelfAssesmentCreate,MySelfAssesments,\
    MySelfAssesmentsproject,MySelfAssesmentsprojectupdater,Portfoliocreate,Portfolioupdate,Experiencecreate,Experienceupdate,\
    UserListsliced,DevList,RecruiterList,Alldevs,Allrecruiters,Mytestcenters,Talentorder,Timesetemail,Newuser,\
    unsubscribe,Resourcecreate,Subjectresources,Resourceslikeupdate,Portfoliolikeupdate

from accounts.views import update_profile

app_name = 'frontend'



urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),




    path('credits', credits, name='credits'),

    path('update_profile/', update_profile, name='update-profile'),

    path('seedevs',DevList,name='seedevs'),
    path('seerecruiters',RecruiterList,name='seerecruiters'),
    path('manageprojects',manageprojects,name='manageprojects'),

    path('editproject/<int:project_id>',editproject,name='editproject'),
    path('deleteproject/<int:project_id>',deleteproject,name='deleteproject'),

    path('addproject',addproject,name='addproject'),

    path('management',management,name='management'),
    # new code

    path('qualified', UserList.as_view()),
    path('devlist', DevList, name='devlist'),
    path('recruiterlist', RecruiterList),
    path('userssliced/', UserListsliced.as_view()),
    path('allusers/', AllUsers.as_view()),
    path('updater/<int:pk>', ProfileUpdate.as_view()),
    path('getuser/<int:pk>', Userget.as_view()),
    path('getprofile/<int:pk>', Profileget.as_view()),
    path('getexperience/<int:candidate_id>', Experienceget.as_view()),
    path('getportofolio/<int:candidate_id>', Portfolioget.as_view()),
    path('updateportfolio/<int:pk>', Portfolioupdate.as_view()),
    path('newportfolio', Portfoliocreate.as_view()),
    path('updateexperience/<int:pk>', Experienceupdate.as_view()),
    path('newexperience', Experiencecreate.as_view()),
    path('newresource', Resourcecreate.as_view()),
    path('subjectresources/<int:subject>', Subjectresources.as_view()),
    path('resourceslikeupdate/<int:pk>', Resourceslikeupdate.as_view()),
    path('portfoliolikeupdate/<int:pk>', Portfoliolikeupdate.as_view()),


    path('createassess',SelfAssesmentCreate.as_view()),
    path('myprojects/<int:candidate_id>',MySelfAssesments.as_view()),
    path('mytestcenters/<int:candidate_id>',Mytestcenters.as_view()),
    path('myprojectdetails/<int:pk>',MySelfAssesmentsproject.as_view()),
    path('myprojectdetailsupdater/<int:pk>',MySelfAssesmentsprojectupdater.as_view()),
    path('newselfverify/<int:pk>',Timesetemail.as_view()),
    path('newuser/<int:pk>',Newuser.as_view()),
    path('alldevs',Alldevs.as_view()),
    path('allrecruiters',Allrecruiters.as_view()),
    path('talentorder', Talentorder, name='Talentorder'),
    path('unsubscribe/<str:token>',unsubscribe,name='unsubscribe'),
    # path('selfprojectmanger')
]

from  servermanagement.views import AssessmentJobCreate

urlpatterns += [
    path('schedulejob/', AssessmentJobCreate.as_view()),
]

# referral codes
from frontend.views import ReferralCreate, ReferralCodeCreate

urlpatterns += [
    path('getreferral/<int:pk>/', ReferralCodeCreate.as_view(), name='referral'),
    path('referral/', ReferralCreate.as_view(), name='referral'),
]

