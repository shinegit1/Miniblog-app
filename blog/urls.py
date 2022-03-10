from django.urls import path
from blog import views

urlpatterns = [
    path('',views.home_page,name='home'),
    path('about/',views.about_page,name='about'),
    path('signup/',views.signup_page,name='signup'),
    path('contact/',views.contact_page,name='contact'),
    path('dash/',views.dashboard_page,name='dashboard'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_page,name='logout'),
    path('update/<int:id>/',views.update_blog,name='update'),
    path('delete/<int:id>/',views.delete_blog,name='delete'),
    path('add/',views.add_blog,name='addblog'),
    path('profile/',views.profile_page,name='profile'),
    path('detail/<int:id>/',views.user_detail,name='detail'),
    path('with_old/',views.change_password,name='change'),
    path('del_user/<int:id>/',views.delete_user,name='del_user'),
]
