import json
import uuid
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import firestore, storage
from django.conf import settings

db = settings.FIRESTORE_CLIENT 
bucket = settings.FIREBASE_BUCKET 

@csrf_exempt
def guardar_evaluacion(request):
    if request.method == "POST":
        try:
            if request.content_type == "application/json":
                data = json.loads(request.body)

                candidate_name = data.get("candidate_name")
                total_points = data.get("total_points", 0)
                percent = data.get("percent", 0.0)
                evaluations = data.get("evaluations", [])
                group_id = data.get("group_id")  # ✅ Nuevo campo

                # Guardar evaluación en Firestore
                eval_ref = db.collection("technical_evaluations").document()
                eval_data = {
                    "candidate_name": candidate_name,
                    "total_points": total_points,
                    "percent": percent,
                    "evaluations": evaluations,
                    "group_id": group_id,            # ✅ se guarda el grupo
                    "created_at": firestore.SERVER_TIMESTAMP,
                    "images": []
                }

                # Procesar imágenes en base64
                images = data.get("images", [])
                image_urls = []
                for img_str in images:
                    if img_str.startswith("data:image/"):
                        format, img_b64 = img_str.split(";base64,")
                        ext = format.split("/")[-1]
                        file_name = f"evaluations/{uuid.uuid4()}.{ext}"

                        # Subir a Firebase Storage
                        blob = bucket.blob(file_name)
                        blob.upload_from_string(base64.b64decode(img_b64), content_type=f"image/{ext}")

                        # URL pública
                        blob.make_public()
                        image_urls.append(blob.public_url)

                eval_data["images"] = image_urls
                eval_ref.set(eval_data)

                return JsonResponse({
                    "success": True,
                    "message": "Evaluación guardada en Firestore",
                    "id": eval_ref.id,
                    "images": image_urls,
                })

            else:
                # 📂 FormData
                candidate_name = request.POST.get("candidate_name")
                total_points = int(request.POST.get("total_points", 0))
                percent = float(request.POST.get("percent", 0.0))
                evaluations = json.loads(request.POST.get("evaluations", "[]"))
                group_id = request.POST.get("group_id")  # ✅ FormData

                eval_ref = db.collection("technical_evaluations").document()
                eval_data = {
                    "candidate_name": candidate_name,
                    "total_points": total_points,
                    "percent": percent,
                    "evaluations": evaluations,
                    "group_id": group_id,            # ✅ se guarda el grupo
                    "created_at": firestore.SERVER_TIMESTAMP,
                    "images": []
                }

                image_urls = []
                for file in request.FILES.getlist("images"):
                    ext = file.name.split(".")[-1]
                    file_name = f"evaluations/{uuid.uuid4()}.{ext}"

                    blob = bucket.blob(file_name)
                    blob.upload_from_file(file, content_type=file.content_type)
                    blob.make_public()
                    image_urls.append(blob.public_url)

                eval_data["images"] = image_urls
                eval_ref.set(eval_data)

                return JsonResponse({
                    "success": True,
                    "message": "Evaluación guardada en Firestore",
                    "id": eval_ref.id,
                    "images": image_urls,
                })

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)

@csrf_exempt
def crear_grupo(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")

            if not name:
                return JsonResponse({"success": False, "message": "El nombre del grupo es obligatorio."}, status=400)

            # Crear documento en la colección "groups"
            group_ref = db.collection("groups").document()
            group_ref.set({
                "name": name,
                "created_at": firestore.SERVER_TIMESTAMP
            })

            return JsonResponse({"success": True, "message": "Grupo creado", "id": group_ref.id})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)

def get_groups(request):
    try:
        groups_ref = db.collection("groups")
        docs = groups_ref.stream()

        groups = []
        for doc in docs:
            data = doc.to_dict()
            groups.append({
                "id": doc.id,
                "name": data.get("name", "Grupo sin nombre")
            })

        return JsonResponse({"success": True, "groups": groups})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)