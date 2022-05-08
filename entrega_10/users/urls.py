from django.urls import path

from .views import UserView, loginView

urlpatterns = [
    path('accounts/', UserView.as_view()),
    path('login/', loginView),
]