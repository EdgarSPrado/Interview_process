from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TechnicalEvaluation, EvaluationImage
import base64
import uuid
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
import json
from .models import Evento
@csrf_exempt
@require_POST
def crear_evento_user(request):
    try:
        data = json.loads(request.body)

        nombre = data.get("nombre", "").strip()
        especificacion = data.get("especificacion", "").strip()
        usuario = data.get("usuario", "").strip()
        area = data.get("area", "").strip()
        fecha_entrega = data.get("fecha_entrega")  # puede ser null
        estado = data.get("estado", "En cola")     # default user

        if not nombre or not usuario or not area:
            return JsonResponse({"success": False, "error": "Faltan campos obligatorios."}, status=400)

        evento = Evento.objects.create(
            nombre=nombre,
            especificacion=especificacion if especificacion else None,
            usuario=usuario,
            area=area,
            fecha_entrega=fecha_entrega if fecha_entrega else None,
            estado=estado,
            progreso=0,
            fecha_inicio=None,
            fecha_fin=None,
        )

        return JsonResponse({"success": True, "id": evento.id})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@require_GET
def eventos_list(request):
    eventos = Evento.objects.all()
    data = [
        {
            "id": e.id,
            "title": e.nombre,  # Para FullCalendar
            "start": e.fecha_inicio.strftime("%Y-%m-%d"),
            "end": e.fecha_fin.strftime("%Y-%m-%d"),
            # Datos extra para el modal
            "nombre": e.nombre,
            "especificacion": e.especificacion,
            "progreso": e.progreso,
            "estado": e.estado,
        }
        for e in eventos
    ]
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_POST
def crear_evento(request):
    try:
        body = json.loads(request.body.decode("utf-8"))

        evento = Evento.objects.create(
            nombre=body.get("nombre"),
            especificacion=body.get("especificacion", ""),
            fecha_inicio=body.get("fecha_inicio"),
            fecha_fin=body.get("fecha_fin"),
            progreso=body.get("progreso", 0),
            estado=body.get("estado", ""),
        )

        return JsonResponse({"success": True, "id": evento.id})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)




def calendar_admin_view(request):
    return render(request,'calendario_admin.html')
def calendar_user_view(request):
    return render(request,'calendario_user.html')
def calendar_view(request):
    return render(request,'calendario.html')


def process_view(request):
    return render(request,'intermediario.html')
def create_group_view(request):
    return render(request, 'create_group.html')



def logout_view(request):
    logout(request)
    return redirect("login")


def home(request):
    return render(request, "home.html")




def technical_evaluation(request):
    return render(request, "technical_evaluation.html")

