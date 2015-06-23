from django.conf.urls import patterns, url
from learn import views


urlpatterns = patterns('',
	url(r'^$',views.login,name='login'),
	url(r'^login/$',views.login,name='login'),
	url(r'^register/$',views.register,name='register'),
	url(r'^index/$',views.index,name='index'),
	url(r'^logout/$',views.logout,name='logout'),
	url(r'^login_error/$',views.login_error,name='login_error'),
)
