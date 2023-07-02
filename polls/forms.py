from django.forms import ModelForm
from .models import Clientes, GastosArr, GastosEspacio, Concepto_arr, UM_arr, Concepto_esp, UM_esp
from django import forms
from .models import IngresoEspacio
from django.forms.widgets import SelectDateWidget

class ClientesForm(ModelForm):

    # No_de_orden = forms.IntegerField(label= 'No_de_orden', initial='')
    # Documento_identidad = forms.CharField(initial='')
    # Nombre = forms.CharField(initial='')
    # Apellidos = forms.CharField(initial='')
    # Ciudadano = forms.CharField(initial='')
    # Fecha_nacimiento = forms.DateField(initial='')
    # Estado = forms.CharField(initial='')
    # Fecha_entrada = forms.DateField(initial='')
    # Fecha_salida = forms.DateField(initial='')
    # Cantidad_noches = forms.IntegerField(initial='')
    # Objeto_arrendamiento = forms.CharField(initial='')
    # Recibo_pago = forms.IntegerField(initial='')
    # Info_registro = forms.IntegerField(initial='')
    # Ingreso_arrendamiento = forms.IntegerField(initial='')
    # Ingreso_desayuno = forms.IntegerField(initial='')
    # Ingreso_almuerzo = forms.IntegerField(initial='')
    # Ingreso_total = forms.IntegerField(initial='')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.is_bound:
    #         self.fields['No_de_orden'].initial = self.data.get('No_de_orden', '')
            

    class Meta:
        model = Clientes 
        fields = ['no_de_orden', 'documento_identidad', 'nombre', 'apellidos', 'citizenship', 'fecha_nacimiento', 
                  'estado', 'fecha_entrada', 'fecha_salida', 'cantidad_noches', 'objeto_arrendamiento', 
                  'recibo_pago', 'info_registro', 'ingreso_alojamiento', 'ingreso_desayuno', 
                  'ingreso_almuerzo', 'ingreso_total', ]
        labels = {
                'no_de_orden': 'No. Orden',
                'documento_identidad': 'Documento de identidad',
                'nombre': 'Nombre',
                'apellidos': 'Apellidos',
                'citizenship': 'Ciudadania',
                'fecha_nacimiento': 'Fecha de nacimiento',
                'estado': 'Estado',
                'fecha_entrada': 'Fecha de entrada',
                'fecha_salida': 'Fecha de salida',
                'cantidad_noches': 'Cantidad de noches',
                'objeto_arrendamiento': 'Objeto de Arrendamiento',
                'recibo_pago': 'Recibo de Pago',
                'info_registro': 'Info de registro', 
                'ingreso_alojamiento': 'Ingreso de arrendamiento', # Sale del precio de la Habitacion
                'ingreso_desayuno': 'Ingreso de desayuno',
                'ingreso_almuerzo': 'Ingreso de almuerzo',
                'ingreso_total': 'Ingreso total', #Suma de ingreso_almuerzo + ingreso_desayuno +ingreso_alojamiento
        }
        widgets = {
            'citizenship': forms.Select(attrs={'class': 'form-control'}),
            'objeto_arrendamiento': forms.Select(attrs={'class': 'form-control'}),
        }

class EspacioForm(ModelForm):
    cantidad_espacios = forms.IntegerField()
    importe_cobrado = forms.FloatField()
    periodo_cobrado = forms.CharField()
    

    class Meta:
        model = IngresoEspacio
        fields = ['cantidad_espacios', 'importe_cobrado', 'periodo_cobrado']
        labels = {
                'cantidad_espacios': 'cantidad de espacios',
                'importe_cobrado': 'importe cobrado',
                'periodo_cobrado': 'periodo cobrado',
                }

class GastoArrForm(ModelForm):

    fecha = forms.DateField()
    detalle_gasto = forms.CharField()
    concepto = forms.ModelChoiceField(queryset=Concepto_arr.objects.all())
    unidad_medida = forms.ModelChoiceField(queryset=UM_arr.objects.all())
    cantidad = forms.IntegerField()
    precio_unitario = forms.FloatField()
    importe = forms.FloatField()

    class Meta: 
        model = GastosArr
        fields = ['fecha', 'detalle_gasto', 'concepto', 'unidad_medida', 
                  'cantidad', 'precio_unitario', 'importe']   
        labels = {
                 'fecha' :  'fecha', 
                 'detalle_gasto' :  'detalle_gasto', 
                 'concepto' :  'Concepto_arr', 
                 'unidad_medida' :  'UM_arr', 
                 'cantidad' :  'cantidad', 
                 'precio_unitario' :  'precio_unitario', 
                 'importe' :  'importe', 

        }
        widgets = {
            'concepto': forms.Select(attrs={'class': 'form-control'}),
        }

class GastoEspacioForm(ModelForm):

    fecha = forms.DateField()
    detalle_gasto = forms.CharField()
    concepto = forms.ModelChoiceField(queryset=Concepto_esp.objects.all())
    unidad_medida = forms.ModelChoiceField(queryset=UM_esp.objects.all())
    cantidad = forms.IntegerField()
    precio_unitario = forms.FloatField()
    importe = forms.FloatField()

    class Meta: 
        model = GastosEspacio
        fields = ['fecha', 'detalle_gasto', 'concepto', 'unidad_medida', 
                  'cantidad', 'precio_unitario', 'importe']   
        labels = {
                 'fecha' :  'fecha', 
                 'detalle_gasto' :  'detalle_gasto', 
                 'concepto' :  'Concepto_esp', 
                 'unidad_medida' :  'UM_esp', 
                 'cantidad' :  'cantidad', 
                 'precio_unitario' :  'precio_unitario', 
                 'importe' :  'importe', 

        }
