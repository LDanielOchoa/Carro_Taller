# models.py
from django.db import models
from django.contrib.auth.models import User  

class Registro(models.Model):
    cedula_operador = models.CharField(max_length=25)
    codigo_operador = models.CharField(max_length=50, default="Ninguna")
    nombre_operador = models.CharField(max_length=50)
    cedula_acompanante = models.CharField(max_length=25, default="Ninguna")
    nombre_acompanante = models.CharField(max_length=50, default="Ninguna")
    cargo_acompanante = models.CharField(max_length=50, default="Ninguna")
    fecha = models.DateField(null=False)
    hora_salida = models.TimeField()
    hora_entrada = models.TimeField()
    kilometraje_salida = models.CharField(max_length=50)
    kilometraje_entrada = models.CharField(max_length=50)
    motivo_salida = models.CharField(max_length=30)
    autorizacion = models.CharField(max_length=50)
    observaciones = models.CharField(max_length=100, default="Ninguna")
    estado_registro = models.IntegerField(default=1)  
    vigilante_asignado = models.ForeignKey(
        User, 
            on_delete=models.SET_NULL, 
            null=True, 
            blank=True, 
            related_name='registros_vigilante_asignado_id'
        )
    ultimo_vigilante = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='registros_ultimo_vigilante'
    )

    class Meta:
        db_table = "registros"
    
    

class DetalleCarro(models.Model):
    ESTADOS = [
        ('Rayón', 'Rayón'),
        ('Fisura', 'Fisura'),
        ('Ninguna', 'Ninguna'),  
        ('Manchado', 'Manchado'),     
    ]

    registro_carro = models.ForeignKey('Registro', on_delete=models.CASCADE)

    puerta_faldon_delantero_conductor = models.CharField(max_length=20, choices=ESTADOS, default='Ninguna')
    puerta_trasera_conductor = models.CharField(max_length=20, choices=ESTADOS, default='Ninguna')
    puerta_faldon_delantero_copiloto = models.CharField(max_length=20, choices=ESTADOS, default='Ninguna')
    puerta_trasera_copiloto = models.CharField(max_length=20, choices=ESTADOS, default='Ninguna')
    techo_capot = models.CharField(max_length=20, choices=ESTADOS, default='Ninguna')
    boomper_delantero = models.CharField(max_length=20, choices=ESTADOS, default='Ninguna')
    boomper_trasero_tapamaleta = models.CharField(max_length=20, choices=ESTADOS, default='Ninguna')
    llanta_delantera_izquierda = models.CharField(max_length=20, choices=ESTADOS, default='Ninguna')
    llanta_trasera_izquierda = models.CharField(max_length=20, choices=ESTADOS, default='Ninguna')
    llanta_delantera_derecha = models.CharField(max_length=20, choices=ESTADOS, default='Ninguna')
    llanta_trasera_derecha = models.CharField(max_length=20, choices=ESTADOS, default='Ninguna')
    faldon_trasero_izquierdo = models.CharField(max_length=20, choices=ESTADOS, default='Ninguna')
    faldon_trasero_derecho = models.CharField(max_length=20, choices=ESTADOS, default='Ninguna')
    
    class Meta:
        db_table = "detallecarro"

    def __str__(self):
        return f"Detalles carro - {self.registro_carro}"
    
    def obtener_partes_danadas(self):
        """Obtiene las partes que tienen rayón, manchado o fisura."""
        partes_danadas = []
        campos = [
            ('puerta_faldon_delantero_conductor', 'Puerta y faldón delantero conductor'),
            ('puerta_trasera_conductor', 'Puerta trasera conductor'),
            ('puerta_faldon_delantero_copiloto', 'Puerta y faldón delantero copiloto'),
            ('puerta_trasera_copiloto', 'Puerta trasera copiloto'),
            ('techo_capot', 'Techo y capó'),
            ('boomper_delantero', 'Bómper delantero'),
            ('boomper_trasero_tapamaleta', 'Bómper trasero y tapa maleta'),
            ('llanta_delantera_izquierda', 'Llanta delantera izquierda'),
            ('llanta_trasera_izquierda', 'Llanta trasera izquierda'),
            ('llanta_delantera_derecha', 'Llanta delantera derecha'),
            ('llanta_trasera_derecha', 'Llanta trasera derecha'),
            ('faldon_trasero_izquierdo', 'Faldón trasero izquierdo'),
            ('faldon_trasero_derecho', 'Faldón trasero derecho'),
        ]

        for campo, descripcion in campos:
            if getattr(self, campo) in ['Rayón', 'Fisura', 'Manchado']:
                partes_danadas.append(descripcion)

        return partes_danadas
    
    
    def obtener_partes_danadas_estados(self):
        """Obtiene las partes que tienen rayón, manchado o fisura y su estado."""
        partes_danadas = []
        estados = {
            'puerta_faldon_delantero_conductor': 'Puerta y faldón delantero conductor',
            'puerta_trasera_conductor': 'Puerta trasera conductor',
            'puerta_faldon_delantero_copiloto': 'Puerta y faldón delantero copiloto',
            'puerta_trasera_copiloto': 'Puerta trasera copiloto',
            'techo_capot': 'Techo y capó',
            'boomper_delantero': 'Bómper delantero',
            'boomper_trasero_tapamaleta': 'Bómper trasero y tapa maleta',
            'llanta_delantera_izquierda': 'Llanta delantera izquierda',
            'llanta_trasera_izquierda': 'Llanta trasera izquierda',
            'llanta_delantera_derecha': 'Llanta delantera derecha',
            'llanta_trasera_derecha': 'Llanta trasera derecha',
            'faldon_trasero_izquierdo': 'Faldón trasero izquierdo',
            'faldon_trasero_derecho': 'Faldón trasero derecho',
        }

        for campo, descripcion in estados.items():
            estado = getattr(self, campo)
            if estado in ['Rayón', 'Fisura', 'Manchado']:
                partes_danadas.append({'descripcion': descripcion, 'estado': estado})

        return partes_danadas
    
    
    

class FotoDetalle(models.Model):
    detalle_carro = models.ForeignKey('DetalleCarro', on_delete=models.CASCADE, related_name='fotos')
    parte = models.CharField(max_length=100)  
    imagen = models.ImageField(upload_to='fotosDetalle/')  

    class Meta:
        db_table = "fotosdetalle"

    def __str__(self):
        return f"Foto de {self.parte} - Detalle {self.detalle_carro.id}"
    

    


class Persona(models.Model):
    cedula = models.CharField(max_length=50, db_column="F200_ID")
    nombre = models.CharField(max_length=50, db_column="f200_razon_social")
    cargo = models.CharField(max_length=50, db_column="C0763_DESCRIPCION")
    
    class Meta:
        db_table = "BI_W0550"