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
from django.shortcuts import render, redirect
from django.contrib import messages
from firebase_admin import firestore
from django.conf import settings

db = settings.FIRESTORE_CLIENT 

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 🔍 Buscar usuario en Firestore
        user_query = db.collection("users").where("username", "==", username).limit(1).stream()
        user = None
        for u in user_query:
            user = u.to_dict()
            user["id"] = u.id  # guardamos el id del documento

        # 👌 Validamos usuario y password en texto plano
        if user and user.get("password") == password:
            # Guardamos en la sesión
            request.session["user_id"] = user["id"]
            request.session["username"] = user["username"]
            request.session["is_admin"] = user.get("is_admin", False)

            messages.success(request, f"Bienvenido {user['username']} 👋")
            return redirect("home")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "login.html")