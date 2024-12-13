from django.urls import path
from .views import UserRegisterView, UserLoginView, TakeQuizView, QuizResultsView

urlpatterns = [
    path('api/register', UserRegisterView.as_view(), name='user_register'),
    path('api/login', UserLoginView.as_view(), name='user_login'),
    path('api/quiz', TakeQuizView.as_view(), name='take_quiz'),
    path('api/results', QuizResultsView.as_view(), name='quiz_results'),
]