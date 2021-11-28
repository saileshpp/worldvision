from django.urls import path
from post_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search',views.search, name='search'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('addpost', views.addpost, name='addpost'),
    path('viewpost/<int:id>', views.viewpost, name='viewpost'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('myaccount',views.myaccount, name='myaccount'),
    path('changepassword',views.changepassword, name='changepassword'),
    path('catpage/(?P<slug>[^/]+)$',views.catpage, name='catpage'),
    path('create',views.create, name='create'),
    path('edit/<int:id>',views.edit, name='edit'),
]
