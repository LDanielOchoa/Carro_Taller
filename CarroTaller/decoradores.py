from django.shortcuts import redirect
from CarroTaller.models import Registro

def solo_para_administradores(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_staff:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def verificar_registro_pendiente(view_func):
    def wrapper(request, *args, **kwargs):
        # Verifica si hay un registro pendiente
        if Registro.objects.filter(hora_entrada__isnull=True).exists():
            # Solo redirigir si la vista no es 'home'
            if request.resolver_match.url_name != 'home':
                return redirect('home')  # Redirige a home si hay un registro pendiente
        return view_func(request, *args, **kwargs)
    return wrapper
