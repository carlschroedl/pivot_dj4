from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.PollIndexView.as_view(), name='index'),
    path('<int:pk>/', views.PollView.as_view(), name='detail'),
    path('<int:pk>/ballots/', views.BallotIndexView.as_view(), name='ballots'),
    path('<int:poll_id>/result/', views.result, name='result'),
    path('<int:poll_id>/vote/', views.vote, name='vote'),
]
