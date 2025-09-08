from django.contrib import admin
from .models import TechnicalEvaluation, EvaluationImage,Evento


class EvaluationImageInline(admin.TabularInline):
    model = EvaluationImage
    extra = 1  # cantidad de inputs vacíos para subir imágenes extra
    readonly_fields = ["uploaded_at"]


@admin.register(TechnicalEvaluation)
class TechnicalEvaluationAdmin(admin.ModelAdmin):
    list_display = ("candidate_name", "total_points", "percent", "created_at")
    search_fields = ("candidate_name",)
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)
    inlines = [EvaluationImageInline]


@admin.register(EvaluationImage)
class EvaluationImageAdmin(admin.ModelAdmin):
    list_display = ("evaluation", "image", "uploaded_at")
    readonly_fields = ("uploaded_at",)

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "usuario", "area", "estado", "progreso", "fecha_entrega", "creado_en")
    search_fields = ("nombre", "usuario", "area")
    list_filter = ("estado", "creado_en", "fecha_entrega")
    readonly_fields = ("creado_en", "actualizado_en")