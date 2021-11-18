from django.urls import path
from post_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('addpost', views.addpost, name='addpost'),
    path('viewpost/<int:id>', views.viewpost, name='viewpost'),
    path('myaccount',views.myaccount, name='myaccount'),
    path('changepassword',views.changepassword, name='changepassword'),
]
