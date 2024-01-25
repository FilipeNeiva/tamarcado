import csv
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics, permissions
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view, permission_classes
from datetime import date, datetime
from agenda.tasks import gera_relatorio_prestadores
from agenda.utils import get_horarios_disponiveis

# Create your views here.


class IsOwnerOrCreatOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        username = request.query_params.get("username", None)
        if request.user.username == username:
            return True
        return False
    

class IsPrestador(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.prestador == request.user:
            return True
        return False


class AgendamentoList(generics.ListCreateAPIView): # /api/agendamentos/
    serializer_class = AgendamentoSerializer
    permission_classes = [IsOwnerOrCreatOnly]

    def get_queryset(self):
        username = self.request.query_params.get("username", None)
        queryset = Agendamento.objects.filter(prestador__username=username)
        return queryset
    

class AgendamentoDetails(generics.RetrieveUpdateDestroyAPIView): # /api/agendamento/<pk>/
    permission_classes = [IsPrestador]
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer


@api_view(http_method_names=["GET"])
@permission_classes([permissions.IsAdminUser])
def relatorio_prestadores(request):
    if request.query_params.get("formato") == "csv":
        # data_hoje = date.today()
        # response = HttpResponse(
        #     content_type="text/csv",
        #     headers={"Content-Disposition": f'attachment; filename="relatorio_{data_hoje}.csv"'},
        # )

        result = gera_relatorio_prestadores.delay()
        return Response({"task_id": result.task_id})
    else:
        prestadores = User.objects.all()
        serializer = PrestadorSerializer(prestadores, many=True)
        return Response(serializer.data)


@api_view(http_method_names=["GET"])
def get_horarios(request):
    data = request.query_params.get("data")
    if not data:
        data = datetime.now().date()
    else:
        data = datetime.fromisoformat(data).date()

    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
    return JsonResponse(horarios_disponiveis, safe=False)