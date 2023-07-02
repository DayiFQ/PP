from django.contrib import admin
from django.urls import path, include
from polls import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('home/', views.home, name='home'),
    #path('polls/', include('polls.urls'))

    #----------------------------URLS Cliente
    path('registro_clientes/', views.registro_clientes, name='registro_clientes'),
    path('registro_clientes/', views.RegistroIngresoView.as_view(), name='registro_clientes'),
    path('listado_clientes_reg/', views.listado_clientes_reg, name='listado_clientes_reg'),
    path('listado_clientes_act/', views.listado_clientes_act, name='listado_clientes_act'),

    path('eliminar_cliente/<documento_identidad>/', views.eliminar_cliente),
    path('editar_cliente/<str:documento_identidad>/', views.editar_cliente),
    path('edicion_cliente/<str:documento_identidad>/', views.edicion_cliente),
    path('delete_cliente/<int:pk>/', views.DeleteClienteView.as_view(),name='delete_cliente'),#cliente registrados
    path('delete_clientes/<int:pk>/', views.DeleteClientesView.as_view(),name='delete_clientes'),#cliente actuales
    path('modificar_cliente/<int:pk>', views.update_cliente,name='modificar_cliente'),
    path('ver_cliente_reg/<int:pk>', views.ver_cliente_reg, name='ver_cliente_reg'),
    path('ver_cliente_act/<int:pk>', views.ver_cliente_act, name='ver_cliente_act'),
    path('modificar_cliente_act/<int:pk>', views.update_cliente_act,name='modificar_cliente_act'),

    path('indice_ocupacional/', views.indice_ocupacional, name='indice_ocupacional'),
   

    #-----------------------------URLS Espacio
    path('registro_ingreso_espacio/', views.registro_ingreso_espacio, name='registro_ingreso_espacio'),
    path('listado_ingresos_espacio/', views.listado_ingresos_espacio, name='listado_ingresos_espacio'),

    path('delete_espacio/<int:pk>/', views.DeleteEspacioView.as_view(),name='delete_espacio'),
    path('modificar_espacio/<int:pk>', views.modificar_espacio,name='modificar_espacio'),
    path('ver_espacio/<int:pk>', views.ver_espacio,name='ver_espacio'),


    
    path('listado_ingresos_totales/', views.ingresos_mensuales,name='listado_ingresos_totales'),
    

    #-----------------------------URLS Gastos
    path('gasto_arren/', views.gasto_arren, name='gasto_arren'),
    path('gasto_espacio/', views.gasto_espacio, name='gasto_espacio'),

    path('listado_gastos_esp/', views.listado_gastos_esp, name='listado_gastos_esp'),
    path('listado_gastos_arren/', views.listado_gastos_arren, name='listado_gastos_arren'),

    path('ver_gasto_arr/<int:pk>', views.ver_gasto_arr, name='ver_gasto_arr'),
    path('modificar_gastos_arren/<int:pk>', views.modificar_gastos_arren,name='modificar_gastos_arren'),
    path('delete_gastos_arren/<int:pk>/', views.DeleteGastosArrenView.as_view(),name='delete_gastos_arren'),

    path('ver_gasto_esp/<int:pk>', views.ver_gasto_esp, name='ver_gasto_esp'),
    path('modificar_gastos_esp/<int:pk>', views.modificar_gastos_esp,name='modificar_gastos_esp'),
    path('delete_gastos_esp/<int:pk>/', views.DeleteGastosEspView.as_view(),name='delete_gastos_esp'),
    path('create_concepto_esp/', views.CreateConceptoEspView.as_view(),name='create_concepto_esp'),

    path('create_concepto_arr/', views.CreateConceptoArrView.as_view(),name='create_concepto_arr'),
    path('create_concepto/<int:pk>', views.update_ciudadania,name='create_concepto_id'),
    path('delete_concepto/<int:pk>', views.DeleteCiudadanoView.as_view(),name='delete_concepto'),
   
    path('create_um_esp/', views.CreateUM_espView.as_view(),name='create_um_esp'),

    path('create_um_arr/', views.CreateUM_arrView.as_view(),name='create_um_arr'),
    path('create_um/<int:pk>', views.update_ciudadania,name='create_um_id'),
    path('delete_um/<int:pk>', views.DeleteCiudadanoView.as_view(),name='delete_um'),
   
    
    path('gasto_salario/', views.gastos_salario,name='gasto_salario'),
    
    #-----------------------------URLS Ciudadania
    path('create_ciudadano/', views.CreateCiudadanoView.as_view(),name='create_ciudadano'),
    path('create_ciudadano/<int:pk>', views.update_ciudadania,name='create_ciudadano_id'),
    path('delete_ciudadano/<int:pk>', views.DeleteCiudadanoView.as_view(),name='delete_ciudadano'),

    #-----------------------------URLS Objeto de arrendamiento
    path('create_objeto_arr/', views.CreateObjetoArrendamientoView.as_view(),name='create_objeto_arr'),
    path('create_objeto_arr/<int:pk>', views.update_objeto_arrendamiento,name='create_objeto_arr_id'),
    path('delete_objeto_arr/<int:pk>', views.DeleteObjetoArrendamientoView.as_view(),name='delete_objeto_arr'),
    
    #-----------------------------URLS Generales
    path('registro_ingresos/', views.registro_ingresos, name='registro_ingresos'),
    path('registro_gastos/', views.registro_gastos, name='registro_gastos'),
    path('control_inventarios/', views.control_inventarios, name='control_inventarios'),
    path('calculo_impuestos/', views.calculo_impuestos, name='calculo_impuestos'),
    path('disponibilidad/', views.disponibilidad, name='disponibilidad'),
    path('registro_contable/', views.registro_contable, name='registro_contable'),
      
      

    ]
