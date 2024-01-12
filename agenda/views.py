from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics, permissions
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from datetime import datetime
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


class PrestadorList(generics.ListAPIView): # /api/prestadores/
    permission_classes = [permissions.IsAdminUser]
    serializer_class = PrestadorSerializer
    queryset = User.objects.all()


@api_view(http_method_names=["GET"])
def get_horarios(request):
    data = request.query_params.get("data")
    if not data:
        data = datetime.now().date()
    else:
        data = datetime.fromisoformat(data).date()

    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
    return JsonResponse(horarios_disponiveis, safe=False)