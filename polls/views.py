from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate 
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import ClientesForm
from .models import Clientes, Rooms, Ciudadania, GastosArr, GastosEspacio, Concepto_arr, UM_arr, Concepto_esp, UM_esp
from .models import IngresoEspacio
from .forms import EspacioForm, GastoArrForm, GastoEspacioForm
from datetime import date
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages 
from django.http import Http404
from django.db.models import Sum
from decimal import Decimal
from django.db.models import Q
from datetime import datetime
from calendar import monthrange

# Create your views here.
#---------------------------Generales
def home(request):
    if request.user.is_authenticated:
       return render(request, 'home.html')
    else:
       return redirect ('iniciar_sesion')

def registro_ingresos(request):
    if request.user.is_authenticated:
        return render(request, 'registro_ingresos.html')
    else:
        return redirect('iniciar_sesion')

def registro_gastos(request):
    if request.user.is_authenticated:
       return render(request, 'registro_gastos.html')
    else:
       return redirect ('iniciar_sesion')

def control_inventarios(request):
    if request.user.is_authenticated:
       return render(request, 'control_inventarios.html')
    else:
       return redirect ('iniciar_sesion')

def calculo_impuestos(request):
    if request.user.is_authenticated:
       return render(request, 'calculo_impuestos.html')
    else:
       return redirect ('iniciar_sesion')

def disponibilidad(request):
    if request.user.is_authenticated:
       return render(request, 'disponibilidad.html')
    else:
       return redirect ('iniciar_sesion')

def registro_contable(request):
    if request.user.is_authenticated:
        return render(request, 'registro_contable.html')
    else:
        return redirect('iniciar_sesion')
    
#---------------------------Usuario (registrar)
def registrarse(request):

    if request.method == 'GET':
        return render(request, 'registrarse.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('registro_clientes')
            except IntegrityError:
                return render(request, 'registrarse.html', {
                'form': UserCreationForm,
                "error": 'El usuario ya existe'
                })
        return render(request, 'registrarse.html', {
                'form': UserCreationForm,
                "error": 'Las contraseñas no coinciden'
       })

def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'iniciar_sesion.html', {
        'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'iniciar_sesion.html', {
            'form': AuthenticationForm,
            'error': 'El usuario o la contraseña es incorrecta'
            })   
        else:
            login(request,user)
            return redirect('home')
        
def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion')

#---------------------------Cliente            
class RegistroIngresoView(CreateView):
    model = Clientes
    template_name = 'registro_clientes.html'
    form_class = ClientesForm
    fields=['no_de_orden', 'documento_identidad', 'nombre', 'apellidos', 'citizenship', 'fecha_nacimiento', 
           'estado', 'fecha_entrada', 'fecha_salida', 'cantidad_noches', 'objeto_arrendamiento', 
           'recibo_pago', 'info_registro', 'ingreso_alojamiento','ingreso_desayuno', 
           'ingreso_almuerzo', 'ingreso_total',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'El cliente se ha registrado satisfactoriamente.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'No se ha registrado ningún cliente.')
        return super().form_invalid(form)

def registro_clientes(request):
    rooms = Rooms.objects.all()
    ciudadania = Ciudadania.objects.all()

    if request.method == 'GET':
         return render(request, 'registro_clientes.html', {
            'form': ClientesForm,
            'rooms':rooms,
            'ciudadanias':ciudadania
        })
    else:   
        print(request.POST)
        request.POST = request.POST.copy()
        data = request.POST
                       
        form = ClientesForm(data)    
        print('Form',form)
        print('Data',data)
            
        if form.is_valid():
            nuevo_cliente = form.save(commit=False)  
            nuevo_cliente.user = request.user
            nuevo_cliente.save()  
            messages.success(request, 'El cliente se ha registrado satisfactoriamente.')
            return redirect('registro_clientes')
        else:
                messages.error(request, 'No se ha registrado ningún cliente.')
                form = ClientesForm()
                context = {'form': form}
                return render(request, 'registro_clientes.html', context)
        
def listado_clientes_reg(request):
    if request.user.is_authenticated:
        lista_clientes = Clientes.objects.all()
        ciudadanias = Ciudadania.objects.all()
        rooms = Rooms.objects.all()
        return render(request, 'listado_clientes_reg.html', {'lista_clientes': lista_clientes, 'ciudadania': ciudadanias, 'room': rooms})
    else:
        return redirect('iniciar_sesion')
  
def listado_clientes_act(request):
    if request.user.is_authenticated:
        lista_clientes = Clientes.objects.filter(fecha_salida__gte=date.today())
        ciudadanias = Ciudadania.objects.all()
        rooms = Rooms.objects.all()
        return render(request, 'listado_clientes_act.html', {'lista_clientes': lista_clientes, 'ciudadania': ciudadanias, 'room': rooms})
    else:
        return redirect('iniciar_sesion')

def eliminar_cliente(request, documento_identidad):
    if request.user.is_authenticated:
           
        cliente = get_object_or_404(Clientes, documento_identidad=documento_identidad)
        if request.method == 'POST':
            clientes = Clientes.objects.get(documento_identidad=documento_identidad)
            clientes.delete()
            return redirect('listado_clientes_reg')
        else:
            return render(request, 'confirmar_eliminar_cliente.html', {'cliente': cliente})
    
    else:
        return redirect('iniciar_sesion')

def edicion_cliente(request, documento_identidad):
    if request.user.is_authenticated:
           
        # Obtener el objeto Clientes correspondiente al documento de identidad
        clientes_edit = Clientes.objects.get(documento_identidad=documento_identidad)

        if request.method == 'POST':
            # Crear un formulario con los datos enviados en la solicitud POST
            form = ClientesForm(request.POST, instance=clientes_edit)
            if form.is_valid():
                # Si el formulario es válido, guardar los cambios en la base de datos
                form.save()
                # Redirigir al usuario a la página de detalles del cliente actualizado
                return redirect('detalles_cliente', documento_identidad=documento_identidad)
        else:
            # Si la solicitud no es POST, renderizar el formulario con los datos actuales del cliente
            form = ClientesForm(instance=clientes_edit)

        return render(request, 'editar_cliente.html', {'form': form, 'clientes_edit': clientes_edit})

    else:
        return redirect('iniciar_sesion')

def editar_cliente(request, documento_identidad):
    
    clientes_edit = Clientes.objects.get(documento_identidad=documento_identidad)
    form = ClientesForm(initial={
        'no_de_orden': clientes_edit.no_de_orden,
        'nombre': clientes_edit.nombre,
        'apellidos': clientes_edit.apellidos,
        'documento_identidad': clientes_edit.documento_identidad,
        'citizenship': clientes_edit.citizenship,
        'fecha_nacimiento': clientes_edit.fecha_nacimiento,
        'estado': clientes_edit.estado,
        'fecha_entrada': clientes_edit.fecha_entrada,
        'cantidad_noches': clientes_edit.cantidad_noches,
        'fecha_salida': clientes_edit.fecha_salida,
        'objeto_arrendamiento': clientes_edit.objeto_arrendamiento,
        'recibo_pago': clientes_edit.recibo_pago,
        'info_registro': clientes_edit.info_registro,
        'ingreso_alojamiento': clientes_edit.ingreso_alojamiento,
        'ingreso_desayuno': clientes_edit.ingreso_desayuno,
        'ingreso_almuerzo': clientes_edit.ingreso_almuerzo,
        'ingreso_total': clientes_edit.ingreso_total
    })
    
    return render(request, 'listado_clientes_reg', {'form': form, 'clientes_edit': clientes_edit})
    
class DeleteClientesView(DeleteView): #tabla clientes actuales
    model = Clientes
    template_name = "listado_clientes_act.html"
    success_url = reverse_lazy('listado_clientes_act')

class DeleteClienteView(DeleteView): #tabla clientes registrados
    model = Clientes
    template_name = "listado_clientes_reg.html"
    success_url = reverse_lazy('listado_clientes_reg')  
    
def ver_cliente_reg(request,pk):
        nuevoobjeto = Clientes.objects.get(id = pk)
        return redirect('listado_clientes_reg')  

def ver_cliente_act(request,pk):
        nuevoobjeto = Clientes.objects.get(id = pk)
        return redirect('listado_clientes_act')       

def update_cliente_act(request, pk):
    # Retrieve the client object to update
    cliente = Clientes.objects.get(id=pk)

    if request.method == 'POST':
        
        # Retrieve the form data
        no_de_orden = request.POST.get('no_de_orden')
        documento_identidad = request.POST.get('documento_identidad')
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        citizenship_id = request.POST.get('citizenship')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        estado = request.POST.get('estado')
        fecha_entrada = request.POST.get('fecha_entrada')
        fecha_salida = request.POST.get('fecha_salida')
        cantidad_noches = request.POST.get('cantidad_noches')
        objeto_arrendamiento_id = request.POST.get('objeto_arrendamiento')
        recibo_pago = request.POST.get('recibo_pago')
        info_registro = request.POST.get('info_registro')
        ingreso_alojamiento = request.POST.get('ingreso_alojamiento')
        ingreso_desayuno = request.POST.get('ingreso_desayuno')
        ingreso_almuerzo = request.POST.get('ingreso_almuerzo')
        ingreso_total = request.POST.get('ingreso_total')

        print("Here")
        print(citizenship_id)
        print(request.POST.get('citizenship'))

        # Retrieve the Ciudadania and Rooms objects corresponding to the selected values
        citizenship = Ciudadania.objects.get(id = citizenship_id)
        objeto_arrendamiento = Rooms.objects.get(id =objeto_arrendamiento_id)

        # Update the client object with the form data and associated objects
        cliente.no_de_orden = no_de_orden
        cliente.documento_identidad = documento_identidad
        cliente.nombre = nombre
        cliente.apellidos = apellidos
        cliente.citizenship = citizenship
        cliente.fecha_nacimiento = fecha_nacimiento
        cliente.estado = estado
        cliente.fecha_entrada = fecha_entrada
        cliente.fecha_salida = fecha_salida
        cliente.cantidad_noches = cantidad_noches
        cliente.objeto_arrendamiento = objeto_arrendamiento
        cliente.recibo_pago = recibo_pago
        cliente.info_registro = info_registro
        cliente.ingreso_alojamiento = ingreso_alojamiento
        cliente.ingreso_desayuno = ingreso_desayuno
        cliente.ingreso_almuerzo = ingreso_almuerzo
        cliente.ingreso_total = ingreso_total
        cliente.save()

        # Redirect to the list of clients
        return redirect('listado_clientes_act')

    # Render the update form with the current client object and related objects
    ciudadanias = Ciudadania.objects.all()
    rooms = Rooms.objects.all()
    context = {'cliente': cliente, 'ciudadania': ciudadanias, 'room': rooms}
    return render(request, 'listado_clientes_act.html' , context)

def update_cliente(request, pk):
    # Retrieve the client object to update
    cliente = Clientes.objects.get(id=pk)

    if request.method == 'POST':
        
        # Retrieve the form data
        no_de_orden = request.POST.get('no_de_orden')
        documento_identidad = request.POST.get('documento_identidad')
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        citizenship_id = request.POST.get('citizenship')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        estado = request.POST.get('estado')
        fecha_entrada = request.POST.get('fecha_entrada')
        fecha_salida = request.POST.get('fecha_salida')
        cantidad_noches = request.POST.get('cantidad_noches')
        objeto_arrendamiento_id = request.POST.get('objeto_arrendamiento')
        recibo_pago = request.POST.get('recibo_pago')
        info_registro = request.POST.get('info_registro')
        ingreso_alojamiento = request.POST.get('ingreso_alojamiento')
        ingreso_desayuno = request.POST.get('ingreso_desayuno')
        ingreso_almuerzo = request.POST.get('ingreso_almuerzo')
        ingreso_total = request.POST.get('ingreso_total')

        print("Here")
        print(citizenship_id)
        print(request.POST.get('citizenship'))

        # Retrieve the Ciudadania and Rooms objects corresponding to the selected values
        citizenship = Ciudadania.objects.get(id = citizenship_id)
        objeto_arrendamiento = Rooms.objects.get(id =objeto_arrendamiento_id)

        # Update the client object with the form data and associated objects
        cliente.no_de_orden = no_de_orden
        cliente.documento_identidad = documento_identidad
        cliente.nombre = nombre
        cliente.apellidos = apellidos
        cliente.citizenship = citizenship
        cliente.fecha_nacimiento = fecha_nacimiento
        cliente.estado = estado
        cliente.fecha_entrada = fecha_entrada
        cliente.fecha_salida = fecha_salida
        cliente.cantidad_noches = cantidad_noches
        cliente.objeto_arrendamiento = objeto_arrendamiento
        cliente.recibo_pago = recibo_pago
        cliente.info_registro = info_registro
        cliente.ingreso_alojamiento = ingreso_alojamiento
        cliente.ingreso_desayuno = ingreso_desayuno
        cliente.ingreso_almuerzo = ingreso_almuerzo
        cliente.ingreso_total = ingreso_total
        cliente.save()

        # Redirect to the list of clients
        return redirect('listado_clientes_reg')

    # Render the update form with the current client object and related objects
    ciudadanias = Ciudadania.objects.all()
    rooms = Rooms.objects.all()
    context = {'cliente': cliente, 'ciudadania': ciudadanias, 'room': rooms}
    return render(request, 'listado_clientes_reg.html' , context)
    

#--------------------------Ciudadania

class CreateCiudadanoView(CreateView):
    model = Ciudadania
    template_name = 'create_ciudadano.html'
    # form_class = ClientesForm
    fields=('name',)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ciudadanos"] =  Ciudadania.objects.all()
        return context
    
def update_ciudadania(request,pk):
    if request.method == 'POST':
        name = request.POST.get('name')
        ciudadano = Ciudadania.objects.get(id = pk)
        ciudadano.name = name
        ciudadano.save()
        return redirect('create_ciudadano')

class DeleteCiudadanoView(DeleteView):
    model = Ciudadania
    template_name = "create_ciudadano.html"
    success_url = reverse_lazy('create_ciudadano')

#--------------------------Objeto de arrendamiento
class CreateObjetoArrendamientoView(CreateView):
    model = Rooms
    template_name = 'create_objeto_arrendamiento.html'
    # form_class = ClientesForm
    fields=('habitacion','espacio',)
    # success_url = reverse_lazy('blog_dash')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objetos"] =  Rooms.objects.all()
        return context

def update_objeto_arrendamiento(request,pk):
    if request.method == 'POST':
        habitacion = request.POST.get('habitacion')
        espacio = request.POST.get('espacio')
        objeto = Rooms.objects.get(id = pk)
        objeto.habitacion = habitacion
        objeto.espacio = espacio
        objeto.save()
        return redirect('create_objeto_arr')
    
class DeleteObjetoArrendamientoView(DeleteView):
    model = Rooms
    template_name = "create_objeto_arrendamiento.html"
    success_url = reverse_lazy('create_objeto_arr')

#--------------------------Espacio
def registro_ingreso_espacio(request):
    if request.user.is_authenticated:   

        if request.method == 'GET':
            return render(request, 'registro_ingreso_espacio.html', {
                'form': EspacioForm
        })
        else:
                formespacio = EspacioForm(request.POST)    
                if  formespacio.is_valid():
                    nuevo_espacio = formespacio.save(commit=False)  
                    nuevo_espacio.user = request.user
                    nuevo_espacio.save()  
                    messages.success(request, 'El ingreso se ha registrado satisfactoriamente.')
                    return redirect('registro_ingreso_espacio')            
                else:
                    messages.error(request, 'No se ha registrado ningún ingreso.')
                    formespacio = ClientesForm()
                    context = {'formespacio': formespacio}
                    
                    return render(request, 'registro_ingreso_espacio.html', context)
    else:
        return redirect('iniciar_sesion')

def listado_ingresos_espacio(request):
    if request.user.is_authenticated:
        # return render(request, 'listado_ingresos_espacio.html')
    
        lista_espacio = IngresoEspacio.objects.all()
        return render(request, 'listado_ingresos_espacio.html', {'lista_espacio': lista_espacio})

    else:
        return redirect('iniciar_sesion')

def modificar_espacio(request,pk):
    if request.method == 'POST':
        cantidad_espacios = request.POST.get('cantidad_espacios')
        importe_cobrado = request.POST.get('importe_cobrado')
        periodo_cobrado = request.POST.get('periodo_cobrado')
        objeto = IngresoEspacio.objects.get(id = pk)
        objeto.cantidad_espacios = cantidad_espacios
        objeto.importe_cobrado = importe_cobrado
        objeto.periodo_cobrado = periodo_cobrado
        objeto.save()
        return redirect('listado_ingresos_espacio')    
    
def ver_espacio(request,pk):
        nuevoobjeto = IngresoEspacio.objects.get(id = pk)
        return redirect('listado_ingresos_espacio') 

class DeleteEspacioView(DeleteView):
    model = IngresoEspacio
    template_name = "listado_ingresos_espacio.html"
    success_url = reverse_lazy('listado_ingresos_espacio')  


def listado_ingresos_totales(request):
    if request.user.is_authenticated:
        return render(request, 'listado_ingresos_totales.html')
    else:
        return redirect('iniciar_sesion')


    
#--------------------------Gastos  
def gasto_arren(request):
    concepto = Concepto_arr.objects.all()
    um = UM_arr.objects.all()

    if request.user.is_authenticated:
        if request.method == 'GET':
            form = GastoArrForm()
            return render(request, 'gasto_arren.html', {
                'form': form,
                'conceptos': concepto,
                'ums':um,
            })
        else:
            form = GastoArrForm(request.POST)
            if form.is_valid():
                nuevo_gasto = form.save(commit=False)
                # obtener la instancia del modelo Concepto_arr a partir del ID proporcionado en el formulario
                # concepto_id = form.cleaned_data['concepto']
                concepto_id = form.cleaned_data['concepto'].id
                nuevo_gasto.concepto_id = concepto_id
                concepto = Concepto_arr.objects.get(id=concepto_id)
                nuevo_gasto.concepto = concepto  # asignar la instancia del modelo Concepto_arr al campo concepto
                
                # um_id = form.cleaned_data['um'].id
                # nuevo_gasto.um_id = um_id
                # um = UM_arr.objects.get(id=um_id)
                # nuevo_gasto.um = um  # asignar la instancia del modelo UM_arr al campo concepto
                
                nuevo_gasto.user = request.user
                nuevo_gasto.save()
                messages.success(request, 'El gasto se ha registrado satisfactoriamente.')
                return redirect('gasto_arren')
            else:
                messages.error(request, 'No se ha registrado ningún gasto.')
                return render(request, 'gasto_arren.html', {'form': form, 'conceptos': concepto})
    else:
        return redirect('login')    
 
def gasto_espacio(request):
    concepto_esp = Concepto_esp.objects.all()
    um_esp = UM_esp.objects.all()

    if request.user.is_authenticated:  

        if request.method == 'GET':
            form = GastoEspacioForm()
            return render(request, 'gasto_espacio.html', {
                'form': form,
                'concepto_esps': concepto_esp,
                'um_esps':um_esp,
            })
        else:
                formgasto = GastoEspacioForm(request.POST)    
                if  formgasto.is_valid():
                    nuevo_gasto = formgasto.save(commit=False)  
                
                    concepto_id = formgasto.cleaned_data['concepto'].id
                    nuevo_gasto.concepto_id = concepto_id
                    concepto_esp = Concepto_esp.objects.get(id=concepto_id)
                    nuevo_gasto.concepto_esp = concepto_esp  # asignar la instancia del modelo Concepto_arr al campo concepto
                    
                    nuevo_gasto.user = request.user
                    nuevo_gasto.save()
                    messages.success(request, 'El gasto se ha registrado satisfactoriamente.')
                    return redirect('gasto_espacio')
                else:
                    messages.error(request, 'No se ha registrado ningún gasto.')
                    return render(request, 'gasto_espacio.html', {'form': formgasto, 'concepto_esps': concepto_esp, 'um_esps': um_esp})
    else:
        return redirect('login')    
 

def listado_gastos_esp(request):
    if request.user.is_authenticated:
           
        gastos_esp = GastosEspacio.objects.all()
        concepto_esp = Concepto_esp.objects.all()
        um_esp = UM_esp.objects.all()
        return render(request, 'listado_gastos_esp.html', {'gastos_esp': gastos_esp, 'concepto_esps':concepto_esp, 'um_esps':um_esp})

    else:
        return redirect('iniciar_sesion')

def listado_gastos_arren(request):
    if request.user.is_authenticated:
   
        gastos_arren = GastosArr.objects.all()
        concepto = Concepto_arr.objects.all()
        um = UM_arr.objects.all()
        return render(request, 'listado_gastos_arren.html', {'gastos_arren': gastos_arren, 'conceptos':concepto, 'ums':um})

    else:
        return redirect('iniciar_sesion')

def modificar_gastos_arren(request,pk):

    objeto = GastosArr.objects.get(id=pk)

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        detalle_gasto = request.POST.get('detalle_gasto')
        concepto_id = request.POST.get('concepto')
        unidad_medida_id = request.POST.get('unidad_medida')
        cantidad = request.POST.get('cantidad')
        precio_unitario = request.POST.get('precio_unitario')
        importe = request.POST.get('importe')

        concepto = Concepto_arr.objects.get(id = concepto_id)
        unidad_medida = UM_arr.objects.get(id = unidad_medida_id)

        objeto = GastosArr.objects.get(id = pk)
        objeto.fecha = fecha
        objeto.detalle_gasto = detalle_gasto
        objeto.concepto = concepto
        objeto.unidad_medida = unidad_medida
        objeto.cantidad = cantidad
        objeto.precio_unitario = precio_unitario
        objeto.importe = importe
        objeto.save()
        return redirect('listado_gastos_arren') 

def ver_gasto_arr(request,pk):
        nuevoobjeto = GastosArr.objects.get(id = pk)
        return redirect('listado_gastos_arr')   

def ver_gasto_esp(request,pk):
        nuevoobjeto = GastosEspacio.objects.get(id = pk)
        return redirect('listado_gastos_esp')   
   
def modificar_gastos_esp(request,pk):
    
    objeto = GastosEspacio.objects.get(id=pk)
    
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        detalle_gasto = request.POST.get('detalle_gasto')
        concepto_id = request.POST.get('concepto')
        unidad_medida_id = request.POST.get('unidad_medida')
        cantidad = request.POST.get('cantidad')
        precio_unitario = request.POST.get('precio_unitario')
        importe = request.POST.get('importe')

        concepto = Concepto_esp.objects.get(id = concepto_id)
        unidad_medida = UM_esp.objects.get(id = unidad_medida_id)
        
        objeto = GastosEspacio.objects.get(id = pk)
        objeto.fecha = fecha
        objeto.detalle_gasto = detalle_gasto
        objeto.concepto = concepto
        objeto.unidad_medida = unidad_medida
        objeto.cantidad = cantidad
        objeto.precio_unitario = precio_unitario
        objeto.importe = importe
        objeto.save()
        return redirect('listado_gastos_esp')     

class DeleteGastosArrenView(DeleteView):
    model = GastosArr
    template_name = "listado_gastos_arren.html"
    success_url = reverse_lazy('listado_gastos_arren')  

class DeleteGastosEspView(DeleteView):
    model = GastosEspacio
    template_name = "listado_gastos_esp.html"
    success_url = reverse_lazy('listado_gastos_esp')  

class CreateConceptoArrView(CreateView):
    model = Concepto_arr
    template_name = 'create_concepto_arr.html'
    fields=('name',)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["conceptos"] =  Concepto_arr.objects.all()
        return context
    
class CreateConceptoEspView(CreateView):
    model = Concepto_esp
    template_name = 'create_concepto_esp.html'
    fields=('name',)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["concepto_esps"] =  Concepto_esp.objects.all()
        return context    

class CreateUM_arrView(CreateView):
    model = UM_arr
    template_name = 'create_um_arr.html'
    fields=('name',)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ums"] =  UM_arr.objects.all()
        return context

    
class CreateUM_espView(CreateView):
    model = UM_esp
    template_name = 'create_um_esp.html'
    fields=('name',)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["um_esps"] =  UM_esp.objects.all()
        return context

def gasto_salario(request):
    if request.user.is_authenticated:
        return render(request, 'gasto_salario.html')
    else:
        return redirect('iniciar_sesion')

#------------------------Ingresos mensuales
def ingresos_mensuales(request):
    if request.user.is_authenticated:
        # Filtrar los registros de Clientes correspondientes al mes de enero
        registros_enero = Clientes.objects.filter(fecha_entrada__month=1)
        registros_febrero = Clientes.objects.filter(fecha_entrada__month=2)
        registros_marzo = Clientes.objects.filter(fecha_entrada__month=3)
        registros_abril = Clientes.objects.filter(fecha_entrada__month=4)
        registros_mayo = Clientes.objects.filter(fecha_entrada__month=5)
        registros_junio = Clientes.objects.filter(fecha_entrada__month=6)
        registros_julio = Clientes.objects.filter(fecha_entrada__month=7)
        registros_agosto = Clientes.objects.filter(fecha_entrada__month=8)
        registros_septiembre = Clientes.objects.filter(fecha_entrada__month=9)
        registros_octubre = Clientes.objects.filter(fecha_entrada__month=10)
        registros_noviembre = Clientes.objects.filter(fecha_entrada__month=11)
        registros_diciembre = Clientes.objects.filter(fecha_entrada__month=12)

        # Obtener la suma de los ingresos totales de todos los registros correspondientes al mes de enero
        ingresos_enero = registros_enero.aggregate(Sum('ingreso_total'))['ingreso_total__sum'] or 0
        ingresos_febrero = registros_febrero.aggregate(Sum('ingreso_total'))['ingreso_total__sum'] or 0
        ingresos_marzo = registros_marzo.aggregate(Sum('ingreso_total'))['ingreso_total__sum'] or 0
        ingresos_abril = registros_abril.aggregate(Sum('ingreso_total'))['ingreso_total__sum'] or 0
        ingresos_mayo = registros_mayo.aggregate(Sum('ingreso_total'))['ingreso_total__sum'] or 0
        ingresos_junio = registros_junio.aggregate(Sum('ingreso_total'))['ingreso_total__sum'] or 0
        ingresos_julio = registros_julio.aggregate(Sum('ingreso_total'))['ingreso_total__sum'] or 0
        ingresos_agosto = registros_agosto.aggregate(Sum('ingreso_total'))['ingreso_total__sum'] or 0
        ingresos_septiembre = registros_septiembre.aggregate(Sum('ingreso_total'))['ingreso_total__sum'] or 0
        ingresos_octubre = registros_octubre.aggregate(Sum('ingreso_total'))['ingreso_total__sum'] or 0
        ingresos_noviembre = registros_noviembre.aggregate(Sum('ingreso_total'))['ingreso_total__sum'] or 0
        ingresos_diciembre = registros_diciembre.aggregate(Sum('ingreso_total'))['ingreso_total__sum'] or 0

        registros_enero_esp = IngresoEspacio.objects.filter(periodo_cobrado__icontains='enero')
        registros_febrero_esp = IngresoEspacio.objects.filter(periodo_cobrado__icontains='febrero')
        registros_marzo_esp = IngresoEspacio.objects.filter(periodo_cobrado__icontains='marzo')
        registros_abril_esp = IngresoEspacio.objects.filter(periodo_cobrado__icontains='abril')
        registros_mayo_esp = IngresoEspacio.objects.filter(periodo_cobrado__icontains='mayo')
        registros_junio_esp = IngresoEspacio.objects.filter(periodo_cobrado__icontains='junio')
        registros_julio_esp = IngresoEspacio.objects.filter(periodo_cobrado__icontains='julio')
        registros_agosto_esp = IngresoEspacio.objects.filter(periodo_cobrado__icontains='agosto')
        registros_septiembre_esp = IngresoEspacio.objects.filter(periodo_cobrado__icontains='septiembre')
        registros_octubre_esp = IngresoEspacio.objects.filter(periodo_cobrado__icontains='octubre')
        registros_noviembre_esp = IngresoEspacio.objects.filter(periodo_cobrado__icontains='noviembre')
        registros_diciembre_esp = IngresoEspacio.objects.filter(periodo_cobrado__icontains='diciembre')

        # Obtener la suma de los ingresos totales de todos los registros correspondientes al mes de enero
        ingresos_enero_esp = registros_enero_esp.aggregate(Sum('importe_cobrado'))['importe_cobrado__sum'] or 0
        ingresos_febrero_esp = registros_febrero_esp.aggregate(Sum('importe_cobrado'))['importe_cobrado__sum'] or 0
        ingresos_marzo_esp = registros_marzo_esp.aggregate(Sum('importe_cobrado'))['importe_cobrado__sum'] or 0
        ingresos_abril_esp = registros_abril_esp.aggregate(Sum('importe_cobrado'))['importe_cobrado__sum'] or 0
        ingresos_mayo_esp = registros_mayo_esp.aggregate(Sum('importe_cobrado'))['importe_cobrado__sum'] or 0
        ingresos_junio_esp = registros_junio_esp.aggregate(Sum('importe_cobrado'))['importe_cobrado__sum'] or 0
        ingresos_julio_esp = registros_julio_esp.aggregate(Sum('importe_cobrado'))['importe_cobrado__sum'] or 0
        ingresos_agosto_esp = registros_agosto_esp.aggregate(Sum('importe_cobrado'))['importe_cobrado__sum'] or 0
        ingresos_septiembre_esp = registros_septiembre_esp.aggregate(Sum('importe_cobrado'))['importe_cobrado__sum'] or 0
        ingresos_octubre_esp = registros_octubre_esp.aggregate(Sum('importe_cobrado'))['importe_cobrado__sum'] or 0
        ingresos_noviembre_esp = registros_noviembre_esp.aggregate(Sum('importe_cobrado'))['importe_cobrado__sum'] or 0
        ingresos_diciembre_esp = registros_diciembre_esp.aggregate(Sum('importe_cobrado'))['importe_cobrado__sum'] or 0

        total_esp = ingresos_enero_esp + ingresos_febrero_esp + ingresos_marzo_esp + ingresos_abril_esp + ingresos_mayo_esp + ingresos_junio_esp + ingresos_julio_esp + ingresos_agosto_esp + ingresos_septiembre_esp + ingresos_octubre_esp +  ingresos_noviembre_esp + ingresos_diciembre_esp 

        total = ingresos_enero + ingresos_febrero + ingresos_marzo + ingresos_abril + ingresos_mayo + ingresos_junio + ingresos_julio + ingresos_agosto + ingresos_septiembre + ingresos_octubre +  ingresos_noviembre + ingresos_diciembre 
        
        total_enero = ingresos_enero_esp + ingresos_enero
        total_febrero = ingresos_febrero_esp + ingresos_febrero
        total_marzo = ingresos_marzo_esp + ingresos_marzo
        total_abril =ingresos_abril_esp + ingresos_abril
        total_mayo = ingresos_mayo_esp + ingresos_mayo
        total_junio = ingresos_junio_esp + ingresos_junio
        total_julio = ingresos_julio_esp + ingresos_julio
        total_agosto = ingresos_agosto_esp + ingresos_agosto
        total_septiembre = ingresos_septiembre_esp + ingresos_septiembre
        total_octubre = ingresos_octubre_esp + ingresos_octubre
        total_noviembre = ingresos_noviembre_esp + ingresos_noviembre
        total_diciembre = ingresos_diciembre_esp + ingresos_diciembre
        total_total = total_esp + total
        
        
        return render(request, 'listado_ingresos_totales.html', {'ingresos_enero': ingresos_enero, 'ingresos_febrero': ingresos_febrero, 
                                                                 'ingresos_marzo': ingresos_marzo, 'ingresos_abril': ingresos_abril,  
                                                                 'ingresos_mayo': ingresos_mayo, 'ingresos_junio': ingresos_junio, 
                                                                 'ingresos_julio': ingresos_julio,  'ingresos_agosto': ingresos_agosto,
                                                                 'ingresos_septiembre': ingresos_septiembre,  'ingresos_octubre': ingresos_octubre,
                                                                 'ingresos_noviembre': ingresos_noviembre,  'ingresos_diciembre': ingresos_diciembre, 'total': total, 

                                                                 'ingresos_enero_esp': ingresos_enero_esp, 'ingresos_febrero_esp': ingresos_febrero_esp, 
                                                                 'ingresos_marzo_esp': ingresos_marzo_esp, 'ingresos_abril_esp': ingresos_abril_esp,  
                                                                 'ingresos_mayo_esp': ingresos_mayo_esp, 'ingresos_junio_esp': ingresos_junio_esp, 
                                                                 'ingresos_julio_esp': ingresos_julio_esp,  'ingresos_agosto_esp': ingresos_agosto_esp,
                                                                 'ingresos_septiembre_esp': ingresos_septiembre_esp,  'ingresos_octubre_esp': ingresos_octubre_esp,
                                                                 'ingresos_noviembre_esp': ingresos_noviembre_esp,  'ingresos_diciembre_esp': ingresos_diciembre_esp, 'total_esp': total_esp,
                                                                 
                                                                 'total_enero': total_enero, 'total_febrero': total_febrero,
                                                                 'total_marzo': total_marzo, 'total_abril': total_abril,
                                                                 'total_mayo': total_mayo, 'total_junio': total_junio,
                                                                 'total_julio': total_julio, 'total_agosto': total_agosto,
                                                                 'total_septiembre': total_septiembre, 'total_octubre': total_octubre,
                                                                 'total_noviembre': total_noviembre, 'total_diciembre': total_diciembre,
                                                                 'total_total': total_total})
    
    
    else:
        return redirect('iniciar_sesion')        
    

#------------------------Gastos salario    
def gastos_salario(request):
    if request.user.is_authenticated:
        # Filtrar los registros de Clientes correspondientes al mes de enero
        registros_sal_enero = GastosArr.objects.filter(Q(fecha__month=1) & Q(concepto__name__icontains='salario'))
        registros_sal_febrero= GastosArr.objects.filter(Q(fecha__month=2) & Q(concepto__name__icontains='salario'))
        registros_sal_marzo = GastosArr.objects.filter(Q(fecha__month=3) & Q(concepto__name__icontains='salario'))
        registros_sal_abril = GastosArr.objects.filter(Q(fecha__month=4) & Q(concepto__name__icontains='salario'))
        registros_sal_mayo = GastosArr.objects.filter(Q(fecha__month=5) & Q(concepto__name__icontains='salario'))
        registros_sal_junio = GastosArr.objects.filter(Q(fecha__month=6) & Q(concepto__name__icontains='salario'))
        registros_sal_julio = GastosArr.objects.filter(Q(fecha__month=7) & Q(concepto__name__icontains='salario'))
        registros_sal_agosto = GastosArr.objects.filter(Q(fecha__month=8) & Q(concepto__name__icontains='salario'))
        registros_sal_septiembre = GastosArr.objects.filter(Q(fecha__month=9) & Q(concepto__name__icontains='salario'))
        registros_sal_octubre = GastosArr.objects.filter(Q(fecha__month=10) & Q(concepto__name__icontains='salario'))
        registros_sal_noviembre = GastosArr.objects.filter(Q(fecha__month=11) & Q(concepto__name__icontains='salario'))
        registros_sal_diciembre = GastosArr.objects.filter(Q(fecha__month=12) & Q(concepto__name__icontains='salario'))
        

        # Obtener la suma de los ingresos totales de todos los registros correspondientes al mes de enero
        ingresos_sal_enero = registros_sal_enero.aggregate(Sum('importe'))['importe__sum'] or 0
        ingresos_sal_febrero = registros_sal_febrero.aggregate(Sum('importe'))['importe__sum'] or 0
        ingresos_sal_marzo = registros_sal_marzo.aggregate(Sum('importe'))['importe__sum'] or 0
        ingresos_sal_abril = registros_sal_abril.aggregate(Sum('importe'))['importe__sum'] or 0
        ingresos_sal_mayo = registros_sal_mayo.aggregate(Sum('importe'))['importe__sum'] or 0
        ingresos_sal_junio = registros_sal_junio.aggregate(Sum('importe'))['importe__sum'] or 0
        ingresos_sal_julio = registros_sal_julio.aggregate(Sum('importe'))['importe__sum'] or 0
        ingresos_sal_agosto = registros_sal_agosto.aggregate(Sum('importe'))['importe__sum'] or 0
        ingresos_sal_septiembre = registros_sal_septiembre.aggregate(Sum('importe'))['importe__sum'] or 0
        ingresos_sal_octubre = registros_sal_octubre.aggregate(Sum('importe'))['importe__sum'] or 0
        ingresos_sal_noviembre = registros_sal_noviembre.aggregate(Sum('importe'))['importe__sum'] or 0
        ingresos_sal_diciembre = registros_sal_diciembre.aggregate(Sum('importe'))['importe__sum'] or 0

        total_gasto_sal = ingresos_sal_enero + ingresos_sal_febrero + ingresos_sal_marzo + ingresos_sal_abril + ingresos_sal_mayo + ingresos_sal_junio + ingresos_sal_julio + ingresos_sal_agosto + ingresos_sal_septiembre + ingresos_sal_octubre +  ingresos_sal_noviembre + ingresos_sal_diciembre 
        
        
        return render(request, 'gasto_salario.html', {

                                                                 'ingresos_sal_enero': ingresos_sal_enero, 'ingresos_sal_febrero': ingresos_sal_febrero, 
                                                                 'ingresos_sal_marzo': ingresos_sal_marzo, 'ingresos_sal_abril': ingresos_sal_abril,  
                                                                 'ingresos_sal_mayo': ingresos_sal_mayo, 'ingresos_sal_junio': ingresos_sal_junio, 
                                                                 'ingresos_sal_julio': ingresos_sal_julio,  'ingresos_sal_agosto': ingresos_sal_agosto,
                                                                 'ingresos_sal_septiembre': ingresos_sal_septiembre,  'ingresos_sal_octubre': ingresos_sal_octubre,
                                                                 'ingresos_sal_noviembre': ingresos_sal_noviembre,  'ingresos_sal_diciembre': ingresos_sal_diciembre, 'total_gasto_sal': total_gasto_sal,
                                                                 
                                                                 })
    
    
    else:
        return redirect('iniciar_sesion')     
          
#------------------------Indice ocupacional
  
def indice_ocupacional(request):
    if request.user.is_authenticated:

        now = datetime.now()

        anno_actual = now.year
        capacidad = 34

        # num_days = monthrange(now.year, now.month)[1]
        num_days_enero = monthrange(now.year, 1)[1]
        num_days_febrero = monthrange(now.year, 2)[1]
        num_days_marzo = monthrange(now.year, 3)[1]
        num_days_abril = monthrange(now.year, 4)[1]
        num_days_mayo = monthrange(now.year, 5)[1]
        num_days_junio = monthrange(now.year, 6)[1]
        num_days_julio = monthrange(now.year, 7)[1]
        num_days_agosto = monthrange(now.year, 8)[1]
        num_days_septiembre = monthrange(now.year, 9)[1]
        num_days_octubre = monthrange(now.year, 10)[1]
        num_days_noviembre = monthrange(now.year, 11)[1]
        num_days_diciembre = monthrange(now.year, 12)[1]

        cant_noches_enero = Clientes.objects.filter(fecha_entrada__year=anno_actual, fecha_entrada__month=1)
        cant_noches_febrero = Clientes.objects.filter(fecha_entrada__year=anno_actual,fecha_entrada__month=2)
        cant_noches_marzo = Clientes.objects.filter(fecha_entrada__year=anno_actual,fecha_entrada__month=3)
        cant_noches_abril = Clientes.objects.filter(fecha_entrada__year=anno_actual,fecha_entrada__month=4)
        cant_noches_mayo = Clientes.objects.filter(fecha_entrada__year=anno_actual,fecha_entrada__month=5)
        cant_noches_junio = Clientes.objects.filter(fecha_entrada__year=anno_actual,fecha_entrada__month=6)
        cant_noches_julio = Clientes.objects.filter(fecha_entrada__year=anno_actual,fecha_entrada__month=7)
        cant_noches_agosto = Clientes.objects.filter(fecha_entrada__year=anno_actual,fecha_entrada__month=8)
        cant_noches_septiembre = Clientes.objects.filter(fecha_entrada__year=anno_actual,fecha_entrada__month=9)
        cant_noches_octubre = Clientes.objects.filter(fecha_entrada__year=anno_actual,fecha_entrada__month=10)
        cant_noches_noviembre = Clientes.objects.filter(fecha_entrada__year=anno_actual,fecha_entrada__month=11)
        cant_noches_diciembre = Clientes.objects.filter(fecha_entrada__year=anno_actual,fecha_entrada__month=12)


        suma_noches_enero = cant_noches_enero.aggregate(Sum('cantidad_noches'))['cantidad_noches__sum'] or 0
        suma_noches_febrero = cant_noches_febrero.aggregate(Sum('cantidad_noches'))['cantidad_noches__sum'] or 0
        suma_noches_marzo = cant_noches_marzo.aggregate(Sum('cantidad_noches'))['cantidad_noches__sum'] or 0
        suma_noches_abril = cant_noches_abril.aggregate(Sum('cantidad_noches'))['cantidad_noches__sum'] or 0
        suma_noches_mayo = cant_noches_mayo.aggregate(Sum('cantidad_noches'))['cantidad_noches__sum'] or 0
        suma_noches_junio = cant_noches_junio.aggregate(Sum('cantidad_noches'))['cantidad_noches__sum'] or 0
        suma_noches_julio= cant_noches_julio.aggregate(Sum('cantidad_noches'))['cantidad_noches__sum'] or 0
        suma_noches_agosto = cant_noches_agosto.aggregate(Sum('cantidad_noches'))['cantidad_noches__sum'] or 0
        suma_noches_septiembre = cant_noches_septiembre.aggregate(Sum('cantidad_noches'))['cantidad_noches__sum'] or 0
        suma_noches_octubre = cant_noches_octubre.aggregate(Sum('cantidad_noches'))['cantidad_noches__sum'] or 0
        suma_noches_noviembre = cant_noches_noviembre.aggregate(Sum('cantidad_noches'))['cantidad_noches__sum'] or 0
        suma_noches_diciembre = cant_noches_diciembre.aggregate(Sum('cantidad_noches'))['cantidad_noches__sum'] or 0


        indice_ocupacional_enero = suma_noches_enero / (num_days_enero * capacidad ) * 100
        indice_ocupacional_febrero= suma_noches_febrero / (num_days_febrero * capacidad ) * 100
        indice_ocupacional_marzo = suma_noches_marzo / (num_days_marzo * capacidad ) * 100
        indice_ocupacional_abril = suma_noches_abril / (num_days_abril* capacidad ) * 100
        indice_ocupacional_mayo = suma_noches_mayo / (num_days_mayo* capacidad ) * 100
        indice_ocupacional_junio = suma_noches_junio/ (num_days_junio * capacidad ) * 100
        indice_ocupacional_julio = suma_noches_julio/ (num_days_julio * capacidad ) * 100
        indice_ocupacional_agosto = suma_noches_agosto/ (num_days_agosto * capacidad ) * 100
        indice_ocupacional_septiembre = suma_noches_septiembre/ (num_days_septiembre * capacidad ) * 100
        indice_ocupacional_octubre = suma_noches_octubre/ (num_days_octubre * capacidad ) * 100
        indice_ocupacional_noviembre = suma_noches_noviembre/ (num_days_noviembre * capacidad ) * 100
        indice_ocupacional_diciembre = suma_noches_diciembre/ (num_days_diciembre * capacidad ) * 100
        
        return render(request, 'indice_ocupacional.html', {

                                                                 'num_days_enero': num_days_enero, 'num_days_febrero': num_days_febrero,  
                                                                 'num_days_marzo': num_days_marzo, 'num_days_abril': num_days_abril,
                                                                 'num_days_mayo': num_days_mayo, 'num_days_junio': num_days_junio,
                                                                 'num_days_julio': num_days_julio, 'num_days_agosto': num_days_agosto,
                                                                 'num_days_septiembre': num_days_septiembre, 'num_days_octubre': num_days_octubre,
                                                                 'num_days_noviembre': num_days_noviembre, 'num_days_diciembre': num_days_diciembre,
                                                                 
                                                                 'suma_noches_enero': suma_noches_enero, 'suma_noches_febrero': suma_noches_febrero,
                                                                 'suma_noches_marzo': suma_noches_marzo, 'suma_noches_abril': suma_noches_abril,
                                                                 'suma_noches_mayo': suma_noches_mayo, 'suma_noches_junio': suma_noches_junio,
                                                                 'suma_noches_julio': suma_noches_julio, 'suma_noches_agosto': suma_noches_agosto,
                                                                 'suma_noches_septiembre': suma_noches_septiembre, 'suma_noches_octubre': suma_noches_octubre,
                                                                 'suma_noches_noviembre': suma_noches_noviembre, 'suma_noches_diciembre': suma_noches_diciembre,


                                                                 'indice_ocupacional_enero': indice_ocupacional_enero, 'indice_ocupacional_febrero': indice_ocupacional_febrero,
                                                                 'indice_ocupacional_marzo': indice_ocupacional_marzo, 'indice_ocupacional_abril': indice_ocupacional_abril,
                                                                 'indice_ocupacional_mayo': indice_ocupacional_mayo, 'indice_ocupacional_junio': indice_ocupacional_junio,
                                                                 'indice_ocupacional_julio': indice_ocupacional_julio, 'indice_ocupacional_agosto': indice_ocupacional_agosto,
                                                                 'indice_ocupacional_septiembre': indice_ocupacional_septiembre, 'indice_ocupacional_octubre': indice_ocupacional_octubre,
                                                                 'indice_ocupacional_noviembre': indice_ocupacional_noviembre, 'indice_ocupacional_diciembre': indice_ocupacional_diciembre,

                                                                 'capacidad': capacidad
                                                                 })
      
    else:
        return redirect('iniciar_sesion')