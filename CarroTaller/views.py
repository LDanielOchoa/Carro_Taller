import json
import re
from django.contrib import messages
from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from CarroTaller.models import FotoDetalle, Persona, Registro, DetalleCarro
from CarroTaller.forms import LoginForm, RegistroForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .decoradores import solo_para_administradores, verificar_registro_pendiente
import pyodbc


@login_required
@verificar_registro_pendiente
def insertarRegistros(request):
    if request.method == "POST":
        motivo_salida = request.POST.get("motivo_salida")
        motivo_salida_otro = request.POST.get("motivo_salida_otro", "").strip()
        
        
        request.POST = request.POST.copy()
        observaciones = request.POST.get("observaciones")
        if not observaciones:
            request.POST["observaciones"] = "Ninguna"
            
        codigo_operador = request.POST.get("codigo_operador")
        if not codigo_operador:
            request.POST["codigo_operador"] = "Ninguna"
            
        cedula_acompanante = request.POST.get("cedula_acompanante")
        if not cedula_acompanante:
            request.POST["cedula_acompanante"] = "Ninguna"
            
        nombre_acompanante = request.POST.get("nombre_acompanante")
        if not nombre_acompanante:
            request.POST["nombre_acompanante"] = "Ninguna"

        cargo_acompanante = request.POST.get("cargo_acompanante")
        if not cargo_acompanante:
            request.POST["cargo_acompanante"] = "Ninguna"
        
        # Si se selecciona "Otro", reemplazar motivo_salida con el valor de motivo_salida_otro
        if motivo_salida == "Otro" and motivo_salida_otro:
            request.POST = request.POST.copy() 
            request.POST["motivo_salida"] = motivo_salida_otro


        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.vigilante_asignado = request.user
            registro.save()
            return redirect('home')

    else:
        form = RegistroForm()

    return render(request, 'registros/insertar.html', {
        'form': form,
    })





@login_required
def listadoRegistros(request):
    registros = Registro.objects.filter(estado_registro=1).select_related('vigilante_asignado').order_by('-fecha', '-hora_salida')
    return render(request, 'registros/listado.html', {'registros': registros})





@login_required
def listadoRegistrosInactivos(request):
    registros = Registro.objects.filter(estado_registro = 0).select_related('vigilante_asignado').order_by('-fecha','-hora_salida')
    return render(request, 'registros/listadoInactivos.html', {'registros': registros})





@login_required
@verificar_registro_pendiente
def home(request):

    # Busca el registro pendiente
    registro_pendiente = Registro.objects.filter(hora_entrada__isnull=True).first()

    context = {
        'registro_pendiente': registro_pendiente,
    }

    return render(request, 'home/home.html', context)





@solo_para_administradores
@login_required
def actualizarRegistro(request, id):
    registro = get_object_or_404(Registro, id=id)
    print("Valor de motivo_salida del registro: ", registro.motivo_salida)
    if request.method == "POST":
        motivo_salida = request.POST.get("motivo_salida")
        motivo_salida_otro = request.POST.get("motivo_salida_otro", "").strip()  # Captura "Otro" si se ingresa
        
        request.POST = request.POST.copy()
        observaciones = request.POST.get("observaciones")
        if not observaciones:
            request.POST["observaciones"] = "Ninguna"

        # Si se selecciona "Otro", reemplazar motivo_salida con el valor de motivo_salida_otro
        if motivo_salida == "Otro" and motivo_salida_otro:
            request.POST = request.POST.copy() 
            request.POST["motivo_salida"] = motivo_salida_otro 

        form = RegistroForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('listado')
    else:
        # Ajustar los formatos antes de renderizar
        if registro.fecha:
            registro.fecha = registro.fecha.strftime('%Y-%m-%d')
        if registro.hora_salida:
            registro.hora_salida = registro.hora_salida.strftime('%H:%M')
        if registro.hora_entrada:
            registro.hora_entrada = registro.hora_entrada.strftime('%H:%M')

        form = RegistroForm(instance=registro)

    # Obtener el valor de 'motivo_salida' desde la instancia 'registro'
    mostrar_motivo_otro = registro.motivo_salida == 'Otro' if registro.motivo_salida else False

    return render(request, 'registros/actualizar.html', {'form': form, 'mostrar_motivo_otro': mostrar_motivo_otro})





@login_required
def informacionRegistro(request, id):
    try:
        registro = Registro.objects.get(id=id)
        
        formato_fecha = registro.fecha.strftime('%d/%m/%Y')
        formato_hora_s = registro.hora_salida.strftime('%H:%M')
        formato_hora_e = registro.hora_entrada.strftime('%H:%M')
        data = {
            'id': registro.id,
            'vigilante_asignado': registro.vigilante_asignado.first_name,
            'cedula_operador': registro.cedula_operador,
            'codigo_operador': registro.codigo_operador,
            'nombre_operador': registro.nombre_operador,
            'cedula_acompanante': registro.cedula_acompanante,
            'nombre_acompanante': registro.nombre_acompanante,
            'cargo_acompanante': registro.cargo_acompanante,
            'fecha': formato_fecha,
            'hora_salida': formato_hora_s,
            'hora_entrada': formato_hora_e,
            'kilometraje_salida': registro.kilometraje_salida,
            'kilometraje_entrada': registro.kilometraje_entrada,
            'motivo_salida': registro.motivo_salida,
            'autorizacion': registro.autorizacion,
            'observaciones': registro.observaciones,
            'ultimo_vigilante': registro.ultimo_vigilante.first_name,
        }
        
        return JsonResponse(data)
    except Registro.DoesNotExist:
        return JsonResponse({'error': 'Registro no encontrado'}, status=404)
    




@login_required 
def buscarRegistros(request):
    query = request.GET.get('q', '')
    registros = Registro.objects.filter(nombre_operador__icontains=query) 
    resultados = []

    for registro in registros:
        resultados.append({
            'id': registro.id,
            'nombre_operador': registro.nombre_operador,
            'fecha': registro.fecha,
            'hora_salida': registro.hora_salida,
            'hora_entrada': registro.hora_entrada,
            'motivo_salida': registro.motivo_salida,
            'autorizacion': registro.autorizacion,
            'observaciones': registro.observaciones,
        })

    return JsonResponse({'registros': resultados})





def iniciarSesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            # Obtener datos de autenticación
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Autenticar usuario
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)  # Iniciar sesión del usuario
                
                # Redirigir según el rol del usuario
                if user.is_staff:  # Administrador
                    return redirect('admin:index')  # Redirige al panel de administración
                else:  # Vigilante
                    return redirect('insertar')  # Redirige al formulario de insertar registro
            else:
                # Si las credenciales no son válidas
                messages.error(request, "Credenciales incorrectas.")
        else:
            # Si el formulario no es válido
            messages.error(request, "Todos los campos son obligatorios.")
    else:
        form = LoginForm() 

    return render(request, 'registration/login.html', {'form': form})





@login_required 
def cerrarSesion(request):
    logout(request)
    return redirect('login')





@solo_para_administradores
@login_required
def crearVigilante(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        nombre = request.POST.get('nombre')
        password = request.POST.get('password')

        # Validar si los campos están vacíos
        if not cedula or not nombre or not password:
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('crear')

        # Validar formato de la cédula 
        if not re.match(r'^\d+$', cedula): 
            messages.error(request, 'La cédula debe contener solo números.')
            return redirect('crear')

        # Verificar si ya existe un usuario con la misma cédula
        if User.objects.filter(username=cedula).exists():
            messages.error(request, 'Ya existe un usuario con esta cédula.')
            return redirect('crear')

        # Validar que la contraseña sea segura
        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return redirect('crear')

        # Crear el usuario vigilante
        try:
            user = User.objects.create_user(
                username=cedula,  # Usamos la cédula como nombre de usuario
                password=password
            )
            user.first_name = nombre  # Guardamos el nombre en el campo 'first_name'
            user.is_staff = False  # No es personal administrativo
            user.save()

            messages.success(request, 'Usuario creado con éxito.')
            return redirect('crear')

        except ValidationError as e:
            messages.error(request, f'Error al crear el usuario: {str(e)}')
            return redirect('crear')

    return render(request, 'usuarios/crear.html')





@solo_para_administradores
@login_required
def listadoVigilantes(request):
    vigilantes = Registro.objects.all()    
    return render(request, 'usuarios/listado.html', {'vigilantes': vigilantes}) 





def guardarDetalles(request, registro_id):
    # Obtener el registro asociado desde la URL
    registro = get_object_or_404(Registro, id=registro_id)
    
    # Obtener el detalle del último registro anterior si existe
    detalle_carro = DetalleCarro.objects.filter(registro_carro__lt=registro_id).order_by('-registro_carro').first()

    if request.method == 'GET':
        # Verificar si hay un registro previo
        if detalle_carro:
            estados_partes = {
                'puerta_faldon_delantero_conductor': detalle_carro.puerta_faldon_delantero_conductor,
                'puerta_trasera_conductor': detalle_carro.puerta_trasera_conductor,
                'puerta_faldon_delantero_copiloto': detalle_carro.puerta_faldon_delantero_copiloto,
                'puerta_trasera_copiloto': detalle_carro.puerta_trasera_copiloto,
                'techo_capot': detalle_carro.techo_capot,
                'boomper_delantero': detalle_carro.boomper_delantero,
                'boomper_trasero_tapamaleta': detalle_carro.boomper_trasero_tapamaleta,
                'llanta_delantera_izquierda': detalle_carro.llanta_delantera_izquierda,
                'llanta_trasera_izquierda': detalle_carro.llanta_trasera_izquierda,
                'llanta_delantera_derecha': detalle_carro.llanta_delantera_derecha,
                'llanta_trasera_derecha': detalle_carro.llanta_trasera_derecha,
                'faldon_trasero_izquierdo': detalle_carro.faldon_trasero_izquierdo,
                'faldon_trasero_derecho': detalle_carro.faldon_trasero_derecho,
            }
        else:
            # Si no hay registro previo, inicializar con 'Ninguna'
            estados_partes = {campo: 'Ninguna' for campo in [
                'puerta_faldon_delantero_conductor', 'puerta_trasera_conductor', 'puerta_faldon_delantero_copiloto',
                'puerta_trasera_copiloto', 'techo_capot', 'boomper_delantero', 'boomper_trasero_tapamaleta',
                'llanta_delantera_izquierda', 'llanta_trasera_izquierda', 'llanta_delantera_derecha',
                'llanta_trasera_derecha', 'faldon_trasero_izquierdo', 'faldon_trasero_derecho'
            ]}

        return render(request, 'registros/detallesRegistro.html', {
            'registro': registro,
            'estados_partes': estados_partes,
        })

    elif request.method == 'POST':
        try:
            # Procesar los datos enviados en el POST
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST  # Si el formulario usa POST estándar

            detalles = data.get('detalles', [])

            if not detalles:
                return JsonResponse({'error': 'Faltan los detalles del registro'}, status=400)

            # Validar que los detalles sean válidos
            campos_validos = {
                'Puerta y faldon delantero conductor': 'puerta_faldon_delantero_conductor',
                'Puerta trasera conductor': 'puerta_trasera_conductor',
                'Puerta y faldon delantero copiloto': 'puerta_faldon_delantero_copiloto',
                'Puerta trasera copiloto': 'puerta_trasera_copiloto',
                'Techo y capot': 'techo_capot',
                'Boomper delantero': 'boomper_delantero',
                'Boomper trasero y tapamaleta': 'boomper_trasero_tapamaleta',
                'Llanta delantera izquierda': 'llanta_delantera_izquierda',
                'Llanta trasera izquierda': 'llanta_trasera_izquierda',
                'Llanta delantera derecha': 'llanta_delantera_derecha',
                'Llanta trasera derecha': 'llanta_trasera_derecha',
                'Faldon trasero izquierdo': 'faldon_trasero_izquierdo',
                'Faldon trasero derecho': 'faldon_trasero_derecho',
            }

            for detalle in detalles:
                parte = detalle.get('parte')
                estado = detalle.get('estado')

                if parte not in campos_validos:
                    return JsonResponse({'error': f'Parte inválida: {parte}'}, status=400)

                if estado not in dict(DetalleCarro.ESTADOS):
                    return JsonResponse({'error': f'Estado inválido: {estado}'}, status=400)

            # Buscar o crear el detalle del carro
            detalle_carro, created = DetalleCarro.objects.get_or_create(
                registro_carro=registro
            )

            # Actualizar los campos del modelo
            for detalle in detalles:
                parte = detalle.get('parte')
                estado = detalle.get('estado')
                setattr(detalle_carro, campos_validos[parte], estado)

            # Guardar los cambios
            detalle_carro.save()

            # Obtener las partes dañadas
            partes_danadas = detalle_carro.obtener_partes_danadas()

            return JsonResponse({
                'message': 'Detalles guardados con éxito',
                'partes_danadas': partes_danadas,
                'redirect_url': reverse('subir_fotos', kwargs={'detalle_carro_id': detalle_carro.id})
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'El cuerpo de la solicitud debe ser un JSON válido.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)





def subirFotos(request, detalle_carro_id):
    detalle_carro = get_object_or_404(DetalleCarro, id=detalle_carro_id)

    # Obtener las partes dañadas del detalle actual
    partes_danadas = detalle_carro.obtener_partes_danadas()

    # 🔹 Intentar obtener fotos del detalle actual
    fotos = FotoDetalle.objects.filter(detalle_carro=detalle_carro)

    # 🔹 Si NO hay fotos en el detalle actual, buscar en el detalle anterior
    if not fotos.exists():
        registro_anterior = Registro.objects.filter(id__lt=detalle_carro.registro_carro.id).order_by('-id').first()
        
        if registro_anterior:
            detalle_anterior = DetalleCarro.objects.filter(registro_carro=registro_anterior).first()
            
            if detalle_anterior:
                fotos = FotoDetalle.objects.filter(detalle_carro=detalle_anterior)

    # Si después de buscar no hay fotos, se asigna None para evitar errores
    fotos = fotos if fotos.exists() else None

    if request.method == 'GET':
        return render(request, 'registros/fotosDetalle.html', {
            'detalle_carro': detalle_carro,
            'partes_danadas': partes_danadas,
            'error_general': '',  
            'fotos': fotos  # Puede ser una queryset de fotos o None si no hay
        })

    elif request.method == 'POST':
        errores = []
        mime_permitidos = ['image/jpeg', 'image/png', 'image/jpg']

        for parte in partes_danadas:
            imagenes = request.FILES.getlist(f'imagenes_{parte}')

            if not imagenes:
                errores.append(f"Es obligatorio subir al menos una foto para la parte dañada: {parte}.")
            else:
                for imagen in imagenes:
                    if imagen.content_type not in mime_permitidos:
                        errores.append(f"El archivo subido para {parte} no es una imagen válida (JPEG o PNG).")

        # Guardar imágenes si no hay errores
        for parte in partes_danadas:
            imagenes = request.FILES.getlist(f'imagenes_{parte}')
            
            if imagenes:
                for imagen in imagenes:
                    foto = FotoDetalle(detalle_carro=detalle_carro, parte=parte, imagen=imagen)
                    foto.save()
            
            else:
                foto_anterior_id = request.POST.get(f'fotoanterior_{parte}')
                if foto_anterior_id:
                    try:
                        foto_existente = FotoDetalle.objects.get(id=foto_anterior_id)
                        foto = FotoDetalle(detalle_carro=detalle_carro, parte=parte, imagen=foto_existente.imagen)
                        foto.save()
                    except FotoDetalle.DoesNotExist:
                        print(f"No se encontró la foto anterior para la parte {parte}.")

        registro = detalle_carro.registro_carro 
        return redirect('/', registro_id=registro.id)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)






def ingresarHoraEntrada(request, registro_id):
    registro = get_object_or_404(Registro, id=registro_id)

    if request.method == 'POST':
        
        kilometraje_entrada = request.POST.get('kilometraje_entrada')
        hora_entrada = request.POST.get('hora_entrada')

        if not hora_entrada:
            messages.error(request, "La hora de entrada es obligatoria.")
        
        if not kilometraje_entrada:
            messages.error(request, "El kilometraje de entrada es obligatorio.")

        else:
            try:
                from datetime import datetime
                hora_entrada_obj = datetime.strptime(hora_entrada, "%H:%M").time()
                
                if registro.hora_salida and hora_entrada_obj <= registro.hora_salida:
                    messages.error(request, "La hora de entrada debe ser posterior a la hora de salida.")

                kilometraje_entrada = int(kilometraje_entrada)  # Convertimos a entero
                if int(registro.kilometraje_salida) is not None and kilometraje_entrada <= int(registro.kilometraje_salida):
                    messages.error(request, "El kilometraje de entrada debe ser mayor al kilometraje de salida.")
                
                if not messages.get_messages(request):  # Si no hay errores, guardamos
                    registro.hora_entrada = hora_entrada_obj
                    registro.kilometraje_entrada = kilometraje_entrada
                    registro.ultimo_vigilante = request.user
                    registro.save()
                    return redirect('detalle_registro', registro_id=registro.id) 

            except ValueError:
                messages.error(request, "Formato de hora inválido. Usa HH:MM.")

    return render(request, 'registros/ingresarHoraEntrada.html', {
        'registro': registro,
    })
    
    



def listadoDetallesYFotos(request, registro_id):
    # Obtener el registro específico
    registro = get_object_or_404(Registro, id=registro_id)

    # Obtener el detalle del carro asociado al registro
    try:
        detalle_carro = DetalleCarro.objects.get(registro_carro=registro)
    except DetalleCarro.DoesNotExist:
        detalle_carro = None

    partes_danadas = []
    fotos_relacionadas = []

    if detalle_carro:
        # Obtener todas las partes dañadas con su estado
        partes_actuales = detalle_carro.obtener_partes_danadas_estados()

        for parte in partes_actuales:
            descripcion_parte = parte['descripcion']
            estado_parte = parte['estado']

            # Buscar fotos relacionadas para la parte en el registro actual
            fotos = FotoDetalle.objects.filter(detalle_carro=detalle_carro, parte=descripcion_parte)

            if fotos.exists():
                # Si existen fotos para esta parte en el registro actual, usarlas
                for foto in fotos:
                    fotos_relacionadas.append({
                        'parte': descripcion_parte,
                        'url': foto.imagen.url,
                        'estado': estado_parte,
                    })
            else:
                # Si no hay fotos en el registro actual, buscar en registros anteriores
                ultimo_registro = Registro.objects.filter(id__lt=registro.id).order_by('-id').first()
                if ultimo_registro:
                    detalle_anterior = DetalleCarro.objects.filter(registro_carro=ultimo_registro).first()
                    if detalle_anterior:
                        foto_anterior = FotoDetalle.objects.filter(detalle_carro=detalle_anterior, parte=descripcion_parte).first()
                        if foto_anterior:
                            fotos_relacionadas.append({
                                'parte': descripcion_parte,
                                'url': foto_anterior.imagen.url,
                                'estado': estado_parte,
                            })
            partes_danadas.append({
                'descripcion': descripcion_parte,
                'estado': estado_parte,
            })

    context = {
        'registro': registro,
        'detalle_carro': detalle_carro,
        'partes_danadas': partes_danadas,
        'fotos_relacionadas': fotos_relacionadas,
    }

    return render(request, 'registros/listadoDetallesFotos.html', context)





def buscarOperador(request):
    cedula = request.GET.get("cedula_operador", None)
    if cedula:
        try:
            connection = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=192.168.90.64;"
                "DATABASE=UNOEE;"
                "UID=power-bi;"
                "PWD=Z1x2c3v4*;"
            )
            cursor = connection.cursor()

            # Ejecuta la consulta
            cursor.execute("SELECT f200_razon_social FROM BI_W0550 WHERE F200_ID = ?", cedula)
            row = cursor.fetchone()

            if row:
                return JsonResponse({"nombre": row[0]})
            else:
                return JsonResponse({"error": "No se encontró un operador con esta cédula."})
        except pyodbc.Error as e:
            print(f"Error interno: {e}")
            return JsonResponse({"error": "Ocurrió un error interno al procesar la solicitud."}, status=500)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({"error": "Ocurrió un error inesperado al procesar la solicitud."}, status=500)
    return JsonResponse({"error": "Cédula no proporcionada."}, status=400)





def buscarAcompanante(request):
    cedula = request.GET.get("cedula_acompanante", None)
    if cedula:
        try:
            connection = pyodbc.connect(
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=192.168.90.64;"
                "DATABASE=UNOEE;"
                "UID=power-bi;"
                "PWD=Z1x2c3v4*;"
            )
            cursor = connection.cursor()

            # Ejecuta la consulta
            cursor.execute("SELECT f200_razon_social, C0763_DESCRIPCION FROM BI_W0550 WHERE F200_ID = ?", cedula)
            row = cursor.fetchone()
            print(row)
            if row:
                return JsonResponse({"nombre": row[0], "cargo": row[1]})
            else:
                 return JsonResponse({"error": "No se encontró un acompañante con esa cédula."})
        except pyodbc.Error as e:
            print(f"Error interno: {e}")
            return JsonResponse({"error": "Ocurrió un error interno al procesar la solicitud."}, status=500)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({"error": "Ocurrió un error inesperado al procesar la solicitud."}, status=500)
    return JsonResponse({"error": "Cédula no proporcionada."}, status=400)

