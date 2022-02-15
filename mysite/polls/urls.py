from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),   # No need to operate database, use generic view
    path('<int:pk>/', views.DetailView.as_view(), name = 'detail'),   # No need to operate database, use generic view
    path('<int:pk>/results/', views.ResultsView.as_view(), name = 'results'),  # No need to operate database, use generic view
    path('<int:question_id>/vote/', views.vote, name = 'vote')
]