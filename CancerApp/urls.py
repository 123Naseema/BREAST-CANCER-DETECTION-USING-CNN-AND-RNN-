from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path('UserLoginAction', views.UserLoginAction, name="UserLoginAction"),	   
	       path('UploadFile', views.UploadFile, name="UploadFile"),
	       path('UploadFileAction', views.UploadFileAction, name="UploadFileAction"),	
	       path('Aboutus', views.Aboutus, name="Aboutus"),	       
]
