from django.contrib import admin
from .models import TechnicalEvaluation, EvaluationImage


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
