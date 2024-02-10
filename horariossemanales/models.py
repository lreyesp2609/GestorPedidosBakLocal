from django.db import models

# Create your models here.
class Horariossemanales(models.Model):
    id_horarios = models.AutoField(primary_key=True)
    hordescripcion = models.CharField(max_length=500, blank=True, null=True)
    tipohorario = models.CharField(max_length=1)
    nombreh = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'horariossemanales'
class DetalleHorariosSemanales(models.Model):
    id_dethorarios = models.AutoField(primary_key=True)
    id_horarios =models.ForeignKey(Horariossemanales, on_delete=models.CASCADE, db_column='id_horarios')
    dia = models.CharField(max_length=1, choices=[('L', 'Lunes'), ('M', 'Martes'), ('X', 'Miércoles'), ('J', 'Jueves'), ('V', 'Viernes'), ('S', 'Sábado'), ('D', 'Domingo')])
    horainicio = models.TimeField()
    horafin = models.TimeField()

    class Meta:
        managed = False
        db_table = 'detallehorariossemanales'