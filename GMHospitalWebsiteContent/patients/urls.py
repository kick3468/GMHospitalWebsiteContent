from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^registration$', views.patientRegistration, name='registration'),
    url(r'^postToDB$', views.logPatientDetailsToDB, name='postToDB'),
    url(r'^generateOp$', views.generateOP, name="createOP"),
    url(r'^patientOp$', views.opGenerationForm, name="opGenerationForm"),
    url(r'^login$', views.userLoginForm, name="userLogin"),
    url(r'^adminLogin$', views.adminLoginForm, name="adminLogin"),
    url(r'^newUser$', views.userRegistrationForm, name="userRegistration"),
    url(r'^createUser$', views.createUser, name="createUser"),
    url(r'^verifyUser$', views.userVerification, name="verifyUser"),
    url(r'^adminLogin$', views.adminLoginForm, name="adminLoginForm"),
    url(r'^forgetPassword$', views.forgetPassword, name="forgetPassword"),
    url(r'^resetPassword$', views.resetPassword, name="resetPassword"),
    url(r'^verifyAdmin$', views.adminVerification, name="verifyAdmin"),
    url(r'^listOfRequests$', views.listOfRequests, name="listOfRequests"),
    url(r'^logout$',views.logout,name="logout"),
    url(r'^adminPage$', views.adminManagement, name='adminManagement'),
    url(r'^alogout$', views.aLogout, name="adminLogout"),
    url(r'^getUnapprovedUsers$', views.pendingApprovals, name="getUnapprovedUsers"),
]