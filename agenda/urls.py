from django.urls import path
from agenda.views import AgendamentoDetails, AgendamentoList, PrestadorList, get_horarios

urlpatterns = [
    path('agendamentos/', AgendamentoList.as_view()),
    path('agendamentos/<int:pk>/', AgendamentoDetails.as_view()),
    path('horarios/', get_horarios),
    path('prestadores/', PrestadorList.as_view()),
]
