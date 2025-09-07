from django.db import models
from django.db import models

class Evento(models.Model):
    nombre = models.CharField(max_length=200)  # Nombre del proyecto/evento
    especificacion = models.TextField(blank=True, null=True)  # Opcional
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)  # Texto libre
    progreso = models.PositiveIntegerField(blank=True, null=True)  # % avance

    creado_en = models.DateTimeField(auto_now_add=True)  # Se guarda al crear
    actualizado_en = models.DateTimeField(auto_now=True)  # Se actualiza al modificar

    def __str__(self):
        return self.nombre
class TechnicalEvaluation(models.Model):
    candidate_name = models.CharField(max_length=200)
    total_points = models.IntegerField(default=0)
    percent = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate_name} - {self.total_points} pts ({self.percent:.2f}%)"
class EvaluationImage(models.Model):
    evaluation = models.ForeignKey(
        TechnicalEvaluation,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="evaluations/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagen de {self.evaluation.candidate_name}"
