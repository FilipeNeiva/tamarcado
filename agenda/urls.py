from django.urls import path
from agenda.views import AgendamentoDetails, AgendamentoList, relatorio_prestadores, get_horarios

urlpatterns = [
    path('agendamentos/', AgendamentoList.as_view()),
    path('agendamentos/<int:pk>/', AgendamentoDetails.as_view()),
    path('horarios/', get_horarios),
    path('prestadores/', relatorio_prestadores),
]
