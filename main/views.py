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
def process_view(request):
    return render(request,'intermediario.html')
def create_group_view(request):
    return render(request, 'create_group.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")


@csrf_exempt
def guardar_evaluacion(request):
    if request.method == "POST":
        try:
            # Si el frontend manda JSON
            if request.content_type == "application/json":
                data = json.loads(request.body)

                candidate_name = data.get("candidate_name")
                total_points = data.get("total_points", 0)
                percent = data.get("percent", 0.0)

                evaluation = TechnicalEvaluation.objects.create(
                    candidate_name=candidate_name,
                    total_points=total_points,
                    percent=percent,
                )

                # Procesar imágenes en base64 si existen
                images = data.get("images", [])
                for img_str in images:
                    if img_str.startswith("data:image/"):
                        # Ejemplo: data:image/png;base64,iVBORw0KGgoAAAANS...
                        format, img_b64 = img_str.split(";base64,")
                        ext = format.split("/")[-1]
                        file_name = f"{uuid.uuid4()}.{ext}"
                        file_data = ContentFile(base64.b64decode(img_b64), name=file_name)

                        EvaluationImage.objects.create(
                            evaluation=evaluation,
                            image=file_data
                        )

            else:  
                # Si usas FormData (con archivos en request.FILES)
                candidate_name = request.POST.get("candidate_name")
                total_points = int(request.POST.get("total_points", 0))
                percent = float(request.POST.get("percent", 0.0))

                evaluation = TechnicalEvaluation.objects.create(
                    candidate_name=candidate_name,
                    total_points=total_points,
                    percent=percent,
                )

                for file in request.FILES.getlist("images"):
                    EvaluationImage.objects.create(
                        evaluation=evaluation,
                        image=file
                    )

            return JsonResponse({
                "success": True,
                "message": "Evaluación guardada correctamente",
                "id": evaluation.id,
            })

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)
def home(request):
    return render(request, "home.html")




def technical_evaluation(request):
    return render(request, "technical_evaluation.html")

