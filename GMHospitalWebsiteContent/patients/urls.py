from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^registration$', views.patientRegistration, name='registration'),
    url(r'^postToDB$', views.logPatientDetailsToDB, name='postToDB'),
    url(r'^generateOp$', views.generateOP, name="createOP"),
    url(r'^patientOp$', views.opGenerationForm, name="opGenerationForm"),
]