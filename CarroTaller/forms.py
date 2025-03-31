from django import forms
from CarroTaller.models import DetalleCarro, FotoDetalle, Registro


class RegistroForm(forms.ModelForm):

    cedula_operador = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'La cédula del operador es obligatoria.'}
    )
    
    codigo_operador = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'El código del operador es obligatorio.'}
    )
    
    nombre_operador = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'El nombre del operador es obligatorio.'}
    )
    
    cedula_acompanante = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'La cédula del acompanante es obligatoria.'}
    )
    
    nombre_acompanante = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'El nombre del acompañante es obligatorio.'}
    )
    
    cargo_acompanante = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'El cargo del acompañante es obligatorio.'}
    )
    
    fecha = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        error_messages={'required': 'La fecha es obligatoria.'}
    )
    
    hora_salida = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        error_messages={'required': 'La hora de salida es obligatoria.'}
    )
    
    hora_entrada = forms.TimeField(
        required=False,  # Hacemos que el campo no sea obligatorio
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        error_messages={'required': 'La hora de entrada es obligatoria.'}
    )
    
    kilometraje_salida = forms.CharField(
        required=True,  # Hacemos que el campo no sea obligatorio
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        error_messages={'required': 'El kilometraje de salida es obligatoria.'}
    )
    
    kilometraje_entrada = forms.CharField(
        required=False,  # Hacemos que el campo no sea obligatorio
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        error_messages={'required': 'La hora de entrada es obligatoria.'}
    )
    
    motivo_salida = forms.CharField(
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'El motivo de salida es obligatorio.'}
    )
    
    motivo_otro = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Por favor ingrese un motivo en "Otro".'}
    )
    
    autorizacion = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'La autorización es obligatoria.'}
    )
    
    observaciones = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Registro
        fields = ['cedula_operador', 'codigo_operador', 'nombre_operador', 'cedula_acompanante', 'nombre_acompanante', 'cargo_acompanante', 'fecha', 
                  'hora_salida', 'hora_entrada', 'kilometraje_salida', 'kilometraje_entrada', 'motivo_salida', 'autorizacion', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'format': '%Y-%m-%d'}),
            'hora_salida': forms.TimeInput(attrs={'type': 'time', 'format': '%H:%M'}),
            'hora_entrada': forms.TimeInput(attrs={'type': 'time', 'format': '%H:%M'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.motivo_salida == 'Otro':
            self.fields['motivo_otro'].initial = self.instance.motivo_otro
    
    def clean_cedula_operador(self):
        cedula_operador = self.cleaned_data.get("cedula_operador")
        if not cedula_operador:
            raise forms.ValidationError("Este campo es obligatorio.")
        if len(cedula_operador) < 5 or len(cedula_operador) > 10:
            raise forms.ValidationError("El número de dígitos no son coherentes.")
        return cedula_operador
    
    def clean_nombre_operador(self):
        nombre_operador = self.cleaned_data.get("nombre_operador")
        if not nombre_operador:
            raise forms.ValidationError("Este campo es obligatorio.")
        if len(nombre_operador) < 3 or len(nombre_operador) > 50:
            raise forms.ValidationError("El nombre no cumple con el límite de caracteres.")
        return nombre_operador  
    
    def clean_fecha(self):
        fecha = self.cleaned_data.get("fecha")
        if not fecha:
            raise forms.ValidationError("Este campo es obligatorio.")
        
        return fecha 
    
    def clean_hora_salida(self):
        hora_salida = self.cleaned_data.get("hora_salida")
        if not hora_salida:
            raise forms.ValidationError("Este campo es obligatorio.")
        return hora_salida  
    
    def clean_hora_entrada(self):
        hora_entrada = self.cleaned_data.get("hora_entrada")
        hora_salida = self.cleaned_data.get("hora_salida")

        # Solo validamos si la hora_entrada tiene un valor
        if hora_entrada and hora_salida:
            if hora_entrada <= hora_salida:
                raise forms.ValidationError("La hora de entrada debe ser posterior a la hora de salida")
    
        return hora_entrada
    
    def clean_motivo_salida(self):
        motivo_salida = self.cleaned_data.get('motivo_salida')
        if motivo_salida == 'Otro':
            motivo_otro = self.cleaned_data.get('motivo_otro')
            return motivo_otro
        return motivo_salida
     
    def clean_kilometraje_salida(self):
        kilometraje_salida = self.cleaned_data.get("kilometraje_salida")
        if not kilometraje_salida:
            raise forms.ValidationError("Este campo es obligatorio.")
        
        kilometraje_salida_int = int(kilometraje_salida)
        
        if kilometraje_salida_int < 0:
            raise forms.ValidationError("El número de dígitos no son coherentes.")

        
        ultimo_registro = Registro.objects.exclude(id=self.instance.id).order_by('-id').first()
        if ultimo_registro and kilometraje_salida_int < int(ultimo_registro.kilometraje_entrada):
            raise forms.ValidationError(
                f"El kilometraje ingresado es menor al que tiene el carro actualmente."
            )

        return kilometraje_salida
    
    
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100, 
        label="Usuario", 
        required=True  
    )
    password = forms.CharField(
        widget=forms.PasswordInput, 
        label="Contraseña", 
        required=True  
    )   
    
    
class DetalleCarroForm(forms.ModelForm):
    class Meta:
        model = DetalleCarro
        fields = [
            'puerta_faldon_delantero_conductor', 
            'puerta_trasera_conductor', 
            'puerta_faldon_delantero_copiloto', 
            'puerta_trasera_copiloto', 
            'techo_capot', 
            'boomper_delantero', 
            'boomper_trasero_tapamaleta', 
            'llanta_delantera_izquierda', 
            'llanta_trasera_izquierda', 
            'llanta_delantera_derecha',
            'llanta_trasera_derecha',
            'faldon_trasero_izquierdo',
            'faldon_trasero_derecho'
        ]
        widgets = {
            'puerta_faldon_delantero_conductor': forms.Select(),
            'puerta_trasera_conductor': forms.Select(),
            'puerta_faldon_delantero_copiloto': forms.Select(),
            'puerta_trasera_copiloto': forms.Select(),
            'techo_capot': forms.Select(),
            'boomper_delantero': forms.Select(),
            'boomper_trasero_tapamaleta': forms.Select(),
            'llanta_delantera_izquierda': forms.Select(),
            'llanta_trasera_izquierda': forms.Select(),
            'llanta_delantera_derecha': forms.Select(),
            'llanta_trasera_derecha': forms.Select(),
            'faldon_trasero_izquierdo': forms.Select(),
            'faldon_trasero_derecho': forms.Select(),
        }
        
class FotoCarroForm(forms.ModelForm):
    class Meta:
        model = FotoDetalle
        fields = ['detalle_carro', 'parte', 'imagen']
    
    # Para agregar validaciones adicionales si las necesitas
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            # Validar el tamaño de la imagen, por ejemplo, no más de 5MB
            if imagen.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError("La imagen es demasiado grande. Debe ser de menos de 5MB.")
        return imagen