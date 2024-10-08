from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.dropdown import DropDown # esto se agrego
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.lang import Builder
from datetime import datetime

from sqlqueries import QueriesSQLite
from datetime import datetime, timedelta
import csv
from pathlib import Path
import os
import psycopg2

Builder.load_file('admin/admin.kv')

def fecha_a_timestamp(fecha_date):
    # Convertir un objeto datetime.date a datetime
    fecha_datetime = datetime.combine(fecha_date, datetime.min.time())
    # Convertir a timestamp
    timestamp = int(fecha_datetime.timestamp())
    return timestamp

# # Supongamos que data['nacimiento'] es una fecha en formato de string 'YYYY-MM-DD'
# data = {'nacimiento': '2000-01-01'}
# # Convertir el string a un objeto datetime
# fecha_nacimiento = datetime.strptime(data['nacimiento'], '%Y-%m-%d')
# # Convertir a timestamp
# timestamp_nacimiento = fecha_nacimiento.timestamp()

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    touch_deselect_last = BooleanProperty(True) 

class SelectableProductoLabel(RecycleDataViewBehavior, BoxLayout):
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)

	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		self.ids['_hashtag'].text = str(1+index)
		self.ids['_codigo'].text = data['codigo']
		self.ids['_articulo'].text = data['nombre'].capitalize()
		self.ids['_cantidad'].text = str(data['cantidad'])
		self.ids['_precio'].text = str("{:.0f}".format(data['precio']))
		return super(SelectableProductoLabel, self).refresh_view_attrs(
            rv, index, data)

	def on_touch_down(self, touch):
		if super(SelectableProductoLabel, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)

	def apply_selection(self, rv, index, is_selected):
		self.selected = is_selected
		if is_selected:
			rv.data[index]['seleccionado']=True
		else:
			rv.data[index]['seleccionado']=False

class SelectableClientesLabel(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_hashtag'].text = str(1 + index)
        self.ids['_ci'].text = str(data['ci'])
        self.ids['_nombre'].text = data['nombre'].capitalize()
        self.ids['_ciudad'].text = data['ciudad'].capitalize()
        self.ids['_telefono'].text = str(data['telefono'])

        # Convertir la fecha en formato cadena a un timestamp
        fecha_nacimiento_str = data['nacimiento']
        try:
            timestamp_nacimiento = fecha_a_timestamp(fecha_nacimiento_str)
            fecha_nacimiento = datetime.fromtimestamp(timestamp_nacimiento)
            self.ids['_nacimiento'].text = fecha_nacimiento.strftime('%Y-%m-%d')
        except ValueError:
            self.ids['_nacimiento'].text = 'Fecha no válida'
        
        return super(SelectableClientesLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableClientesLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            rv.data[index]['seleccionado'] = True
        else:
            rv.data[index]['seleccionado'] = False


class SelectableProveedoresLabel(RecycleDataViewBehavior, BoxLayout):
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)

	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		self.ids['_hashtag'].text = str(1+index)
		self.ids['_id'].text = str(data['id'])
		self.ids['_nombre'].text = data['nombre'].capitalize()
		self.ids['_contacto'].text = data['contacto'].capitalize()
		self.ids['_telefono'].text = str(data['telefono'])
		self.ids['_email'].text = data['email']
		return super(SelectableProveedoresLabel, self).refresh_view_attrs(
            rv, index, data)

	def on_touch_down(self, touch):
		if super(SelectableProveedoresLabel, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)

	def apply_selection(self, rv, index, is_selected):
		self.selected = is_selected
		if is_selected:
			rv.data[index]['seleccionado']=True
		else:
			rv.data[index]['seleccionado']=False

class SelectableUsuarioLabel(RecycleDataViewBehavior, BoxLayout):
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)

	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		self.ids['_hashtag'].text = str(1+index)
		self.ids['_nombre'].text = data['nombre'].title()
		self.ids['_username'].text = data['username']
		self.ids['_tipo'].text = str(data['tipo'])
		return super(SelectableUsuarioLabel, self).refresh_view_attrs(
            rv, index, data)

	def on_touch_down(self, touch):
		if super(SelectableUsuarioLabel, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)

	def apply_selection(self, rv, index, is_selected):
		self.selected = is_selected
		if is_selected:
			rv.data[index]['seleccionado']=True
		else:
			rv.data[index]['seleccionado']=False


# esto es nuevo tambien en kv
class ItemVentaLabel(RecycleDataViewBehavior, BoxLayout):
	index = None

	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		self.ids['_hashtag'].text = str(1+index)
		self.ids['_codigo'].text = data['codigo']
		self.ids['_articulo'].text = data['producto'].capitalize()
		self.ids['_cantidad'].text = str(data['cantidad'])
		self.ids['_precio_por_articulo'].text = str("{:.0f}".format(data['precio']))+" /artículo"
		self.ids['_total'].text= str("{:.0f}".format(data['total']))
		return super(ItemVentaLabel, self).refresh_view_attrs(
            rv, index, data)

# esto es nuevo tambien en kv
class SelectableVentaLabel(RecycleDataViewBehavior, BoxLayout):
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)

	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		self.ids['_hashtag'].text = str(1+index)
		self.ids['_username'].text = data['username']
		self.ids['_cantidad'].text = str(data['productos'])
		self.ids['_total'].text = 'Gs. '+str("{:.0f}".format(data['total']))
		self.ids['_time'].text = str(data['fecha'].strftime("%H:%M:%S"))
		self.ids['_date'].text = str(data['fecha'].strftime("%d/%m/%Y"))
		return super(SelectableVentaLabel, self).refresh_view_attrs(
            rv, index, data)

	def on_touch_down(self, touch):
		if super(SelectableVentaLabel, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)

	def apply_selection(self, rv, index, is_selected):
		self.selected = is_selected
		if is_selected:
			rv.data[index]['seleccionado']=True
		else:
			rv.data[index]['seleccionado']=False


class AdminRV(RecycleView):
    def __init__(self, **kwargs):
        super(AdminRV, self).__init__(**kwargs)
        self.data=[]

    def agregar_datos(self,datos):
        for dato in datos:
            dato['seleccionado']=False
            self.data.append(dato)
        self.refresh_from_data()

    def dato_seleccionado(self):
        indice=-1
        for i in range(len(self.data)):
            if self.data[i]['seleccionado']:
                indice=i
                break
        return indice

class ProductoPopup(Popup):
    def __init__(self, agregar_callback, **kwargs):
        super(ProductoPopup, self).__init__(**kwargs)
        self.agregar_callback = agregar_callback
        self.dropdown = DropDown()

    def abrir(self, agregar, producto=None):
        if agregar:
            self.ids.producto_info_1.text = 'Agregar producto nuevo'
            self.ids.producto_codigo.disabled = False
        else:
            self.ids.producto_info_1.text = 'Modificar producto'
            self.ids.producto_codigo.text = producto['codigo']
            self.ids.producto_codigo.disabled = True
            self.ids.producto_nombre.text = producto['nombre']
            self.ids.producto_cantidad.text = str(producto['cantidad'])
            self.ids.producto_precio.text = str(producto['precio'])
        self.open()

    def mostrar_proveedores(self):
        self.dropdown.clear_widgets()
        connection = QueriesSQLite.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT nombre FROM proveedores")
        proveedores = cursor.fetchall()
        connection.close()

        for proveedor in proveedores:
            btn = Button(text=proveedor[0], size_hint_y=None, height=44)
            btn.bind(on_release=self.seleccionar_proveedor)
            self.dropdown.add_widget(btn)

        self.dropdown.open(self.ids.btn_proveedores)

    def seleccionar_proveedor(self, btn):
        self.ids.btn_proveedores.text = btn.text
        self.dropdown.dismiss()

    def verificar(self, producto_codigo, producto_nombre, producto_cantidad, producto_precio):
        alert1 = 'Falta: '
        alert2 = ''
        validado = {}
        if not producto_codigo:
            alert1 += 'Código. '
            validado['codigo'] = False
        else:
            try:
                numeric = int(producto_codigo)
                validado['codigo'] = producto_codigo
            except:
                alert2 += 'Código no válido. '
                validado['codigo'] = False

        if not producto_nombre:
            alert1 += 'Nombre. '
            validado['nombre'] = False
        else:
            validado['nombre'] = producto_nombre.lower()

        if not producto_precio:
            alert1 += 'Precio. '
            validado['precio'] = False
        else:
            try:
                numeric = float(producto_precio)
                validado['precio'] = producto_precio
            except:
                alert2 += 'Precio no válido. '
                validado['precio'] = False

        if not producto_cantidad:
            alert1 += 'Cantidad. '
            validado['cantidad'] = False
        else:
            try:
                numeric = int(producto_cantidad)
                validado['cantidad'] = producto_cantidad
            except:
                alert2 += 'Cantidad no válida. '
                validado['cantidad'] = False

        valores = list(validado.values())

        if False in valores:
            self.ids.no_valid_notif.text = alert1 + alert2
            return

        self.ids.no_valid_notif.text = 'Validado'
        validado['cantidad'] = int(validado['cantidad'])
        validado['precio'] = float(validado['precio'])
        
        # Conectar a la base de datos
        connection = QueriesSQLite.create_connection()
        cursor = connection.cursor()

        # Verificar si el producto ya existe
        cursor.execute("SELECT COUNT(*) FROM productos WHERE codigo = %s", (validado['codigo'],))
        existe = cursor.fetchone()[0]

        if existe:
            # Si el producto existe, actualizarlo
            actualizar_producto = """
            UPDATE productos
            SET nombre = %s, precio = %s, cantidad = %s
            WHERE codigo = %s
            """
            cursor.execute(actualizar_producto, (validado['nombre'], validado['precio'], validado['cantidad'], validado['codigo']))
			
        else:
            # Si el producto no existe, insertarlo
            insertar_producto = """
            INSERT INTO productos (codigo, nombre, precio, cantidad)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insertar_producto, (validado['codigo'], validado['nombre'], validado['precio'], validado['cantidad']))

        # Insertar en la tabla inventario
        insertar_inventario = """
        INSERT INTO inventario (codigo_producto, tipo_movimiento, cantidad, fecha)
        VALUES (%s, %s, %s, %s)
        """
        tipo_movimiento = 'compra'
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(insertar_inventario, (validado['codigo'], tipo_movimiento, validado['cantidad'], fecha_actual))
        
        # Actualizar o insertar en la tabla compras
        proveedor_seleccionado = self.ids.btn_proveedores.text
        cursor.execute("SELECT COUNT(*) FROM compras WHERE codigo = %s", (validado['codigo'],))
        existe_en_compras = cursor.fetchone()[0]

        if existe_en_compras:
            # Si el producto existe en compras, actualizarlo
            actualizar_compra = """
            UPDATE compras
            SET nombre = %s, precio = %s, cantidad = %s, proveedor = %s
            WHERE codigo = %s
            """
            cursor.execute(actualizar_compra, (validado['nombre'], validado['precio'], validado['cantidad'], proveedor_seleccionado, validado['codigo']))
        else:
            # Si el producto no existe en compras, insertarlo
            insertar_compra = """
            INSERT INTO compras (codigo, nombre, precio, cantidad, proveedor)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insertar_compra, (validado['codigo'], validado['nombre'], validado['precio'], validado['cantidad'], proveedor_seleccionado))

        # Confirmar cambios y cerrar conexión
        connection.commit()
        connection.close()

        # Llamar al callback para actualizar la interfaz después de agregar el producto
        self.agregar_callback(True, validado)
        self.dismiss()



class ClientesPopup(Popup):
    def __init__(self, agregar_callback, **kwargs):
        super(ClientesPopup, self).__init__(**kwargs)
        self.agregar_callback = agregar_callback

    def abrir(self, agregar, clientes=None):
        if agregar:
            self.ids.clientes_info_1.text = 'Nuevo cliente'
            self.ids.clientes_ci.disabled = False
        else:
            self.ids.clientes_info_1.text = 'Modificar cliente'
            self.ids.clientes_ci.text = clientes['ci']
            self.ids.clientes_ci.disabled = True
            self.ids.clientes_nombre.text = clientes['nombre']
            self.ids.clientes_ciudad.text = clientes['ciudad']
            self.ids.clientes_telefono.text = clientes['telefono']
            self.ids.clientes_fecha.text = clientes['nacimiento']
        self.open()

    def verificar(self, clientes_ci, clientes_nombre, clientes_ciudad, clientes_telefono, clientes_nacimiento):
        alert1 = 'Falta: '
        alert2 = ''
        validado = {}

        if not clientes_ci:
            alert1 += 'C.I. '
            validado['ci'] = False
        else:
            try:
                numeric = int(clientes_ci)
                validado['ci'] = clientes_ci
            except:
                alert2 += 'C.I. no válido. '
                validado['ci'] = False

        if not clientes_nombre:
            alert1 += 'Nombre. '
            validado['nombre'] = False
        else:
            validado['nombre'] = clientes_nombre.lower()

        if not clientes_ciudad:
            alert1 += 'Ciudad. '
            validado['ciudad'] = False
        else:
            validado['ciudad'] = clientes_ciudad.lower()

        if not clientes_telefono:
            alert1 += 'Telefono. '
            validado['telefono'] = False
        else:
            validado['telefono'] = clientes_telefono

        if not clientes_nacimiento:
            alert1 += 'Fecha de nac. '
            validado['nacimiento'] = False
        else:
            try:
                # Verificar que la fecha esté en el formato correcto
                fecha_nacimiento = datetime.strptime(clientes_nacimiento, '%Y-%m-%d')
                validado['nacimiento'] = clientes_nacimiento
            except ValueError:
                alert2 += 'Fecha no válida. '
                validado['nacimiento'] = False

        valores = list(validado.values())

        if False in valores:
            self.ids.no_valid_notif.text = alert1 + alert2
        else:
            self.ids.no_valid_notif.text = 'Validado'
            self.agregar_callback(True, validado)
            self.dismiss()



class VistaClientes(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.cargar_clientes, 1)

	def cargar_clientes(self, *args):
		_clientes=[]
		connection = QueriesSQLite.create_connection()
		inventario_sql=QueriesSQLite.execute_read_query(connection, "SELECT * from clientes")
		if inventario_sql:
			for cliente in inventario_sql:
				_clientes.append({
					'ci': cliente[0],
					'nombre': cliente[1],
					'ciudad': cliente[2],
					'telefono': cliente[3],
					'nacimiento': cliente[4]
				})

			self.ids.rv_clientes.data = _clientes  # Asigna los datos cargados al RecycleView
			self.ids.rv_clientes.refresh_from_data()  # Refresca la vista con los nuevos datos
	
	def agregar_clientes(self, agregar=False, validado=None):
		if agregar:
			clientes_tuple=tuple(validado.values())
			connection = QueriesSQLite.create_connection()
			crear_clientes="""
			INSERT INTO
				clientes (ci, nombre, ciudad, telefono, nacimiento)
			VALUES
				(%s, %s, %s, %s, %s);
			"""
			QueriesSQLite.execute_query(connection, crear_clientes, clientes_tuple)
			self.ids.rv_clientes.data.append(validado)
			self.ids.rv_clientes.refresh_from_data()
		else:
			popup=ClientesPopup(self.agregar_clientes)
			popup.abrir(True)

	def modificar_clientes(self, modificar=False, validado=None):
		indice=self.ids.rv_clientes.dato_seleccionado()
		if modificar:
			clientes_tuple=(validado['nombre'], validado['ciudad'], validado['telefono'], validado['nacimiento'], validado['ci'])
			connection = QueriesSQLite.create_connection()
			actualizar="""
			UPDATE
				clientes
			SET
				nombre=%s, ciudad=%s, telefono=%s, nacimiento=%s
			WHERE
				ci=%s
			"""
			QueriesSQLite.execute_query(connection, actualizar, clientes_tuple)
			self.ids.rv_clientes.data[indice]['nombre']=validado['nombre']
			self.ids.rv_clientes.data[indice]['ciudad']=validado['ciudad']
			self.ids.rv_clientes.data[indice]['telefono']=validado['telefono']
			self.ids.rv_clientes.data[indice]['nacimiento']=validado['nacimiento']
			self.ids.rv_clientes.refresh_from_data()
		else:
			if indice>=0:
				clientes=self.ids.rv_clientes.data[indice]
				popup=ClientesPopup(self.modificar_clientes)
				popup.abrir(False, clientes)

	def eliminar_clientes(self):
		indice=self.ids.rv_clientes.dato_seleccionado()
		if indice>=0:
			clientes_tuple=(self.ids.rv_clientes.data[indice]['ci'],)
			connection = QueriesSQLite.create_connection()
			borrar= """DELETE from clientes WHERE ci =? """
			QueriesSQLite.execute_query(connection, borrar, clientes_tuple)
			self.ids.rv_clientes.data.pop(indice)
			self.ids.rv_clientes.refresh_from_data()

	def actualizar_clientes(self, clientes_actualizado):
		for clientes_nuevo in clientes_actualizado:
			for clientes_viejo in self.ids.rv_clientes.data:
				if clientes_nuevo['ci']==clientes_viejo['ci']:
					clientes_viejo['telefono']=clientes_nuevo['telefono']
					break
		self.ids.rv_clientes.refresh_from_data()

#Agregadoproveedores

class ProveedorPopup(Popup):
	def __init__(self, agregar_callback, **kwargs):
		super(ProveedorPopup, self).__init__(**kwargs)
		self.agregar_callback=agregar_callback

	def abrir(self, agregar, proveedor=None):
		if agregar:
			self.ids.proveedores_info_1.text='Agregar proveedor nuevo'
			self.ids.proveedores_id.disabled=False
		else:
			self.ids.proveedores_info_1.text='Modificar proveedor'
			self.ids.proveedores_id.text = str(proveedor['id'])
			self.ids.proveedores_id.disabled=True
			self.ids.proveedores_nombre.text=str(proveedor['nombre'])
			self.ids.proveedores_contacto.text=str(proveedor['contacto'])
			self.ids.proveedores_telefono.text=str(proveedor['telefono'])
			self.ids.proveedores_email.text=str(proveedor['email'])
		self.open()

	def verificar(self, proveedores_id, proveedores_nombre, proveedores_contacto, proveedores_telefono, proveedores_email):
		alert1='Falta: '
		alert2=''
		validado={}
		if not proveedores_id:
			alert1+='id. '
			validado['di']=False
		else:
			try:
				numeric=int(proveedores_id)
				validado['id']=proveedores_id
			except:
				alert2+='id no válido. '
				validado['id']=False

		if not proveedores_nombre:
			alert1+='Nombre. '
			validado['nombre']=False
		else:
			validado['nombre']=proveedores_nombre.lower()

		if not proveedores_contacto:
			alert1+='Contacto. '
			validado['contacto']=False
		else:
			validado['contacto']=proveedores_contacto.lower()

		if not proveedores_telefono:
			alert1+='Telefono. '
			validado['telefono']=False
		else:
			validado['telefono']=proveedores_telefono.lower()
		#	try:
		#		numeric=float(proveedores_telefono)
		#		validado['telefono']=proveedores_telefono
		#	except:
		#		alert2+='Teléfono no válido. '
		#		validado['telefono']=False
			
		if not proveedores_email:
			alert1+='Email. '
			validado['email']=False
		else:
			validado['email']=proveedores_email.lower()

		valores=list(validado.values())

		if False in valores:
			self.ids.no_valid_notif.text=alert1+alert2
		else:
			self.ids.no_valid_notif.text='Validado'
			validado['email']=str(validado['email'])
			validado['telefono']=float(validado['telefono'])
			self.agregar_callback(True, validado)
			self.dismiss()

	
#agregadoProveedores

	def agregar_proveedores(self, agregar=False, validado=None):
		if agregar:
			proveedor_tuple=tuple(validado.values())
			connection = QueriesSQLite.create_connection()
			crear_proveedor="""
			INSERT INTO
				proveedores (id, nombre, contacto, telefono, email)
			VALUES
				(%s, %s, %s, %s, %s);
			"""
			QueriesSQLite.execute_query(connection, crear_proveedor, proveedor_tuple)
			self.ids.rv_proveedores.data.append(validado)
			self.ids.rv_proveedores.refresh_from_data()
		else:
			popup=ProveedorPopup(self.agregar_proveedores)
			popup.abrir(True)

class VistaProductos(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.cargar_productos, 1)

	def cargar_productos(self, *args):
		_productos=[]
		connection = QueriesSQLite.create_connection()
		inventario_sql=QueriesSQLite.execute_read_query(connection, "SELECT * from productos")
		if inventario_sql: # agregado!!!
			for producto in inventario_sql:
				_productos.append({'codigo': producto[0], 'nombre': producto[1], 'precio': producto[2], 'cantidad': producto[3]})
		self.ids.rv_productos.agregar_datos(_productos)

	def agregar_producto(self, agregar=False, validado=None):
		if agregar:
			producto_tuple=tuple(validado.values())
			connection = QueriesSQLite.create_connection()
			crear_producto="""
			INSERT INTO
				productos (codigo, nombre, precio, cantidad)
			VALUES
				(%s, %s, %s, %s);
			"""
			QueriesSQLite.execute_query(connection, crear_producto, producto_tuple)
			self.ids.rv_productos.data.append(validado)
			self.ids.rv_productos.refresh_from_data()
		else:
			popup=ProductoPopup(self.agregar_producto)
			popup.abrir(True)

	def modificar_producto(self, modificar=False, validado=None):
		indice=self.ids.rv_productos.dato_seleccionado()
		if modificar:
			producto_tuple=(validado['nombre'], validado['precio'], validado['cantidad'], validado['codigo'])
			connection = QueriesSQLite.create_connection()
			actualizar="""
			UPDATE
				productos
			SET
				nombre=%s, precio=%s, cantidad=%s
			WHERE
				codigo=%s
			"""
			QueriesSQLite.execute_query(connection, actualizar, producto_tuple)
			self.ids.rv_productos.data[indice]['nombre']=validado['nombre']
			self.ids.rv_productos.data[indice]['cantidad']=validado['cantidad']
			self.ids.rv_productos.data[indice]['precio']=validado['precio']
			self.ids.rv_productos.refresh_from_data()
		else:
			if indice>=0:
				producto=self.ids.rv_productos.data[indice]
				popup=ProductoPopup(self.modificar_producto)
				popup.abrir(False, producto)

	def eliminar_producto(self):
		indice=self.ids.rv_productos.dato_seleccionado()
		if indice>=0:
			producto_tuple=(self.ids.rv_productos.data[indice]['codigo'],)
			connection = QueriesSQLite.create_connection()
			borrar= """DELETE from productos WHERE codigo =%s """
			QueriesSQLite.execute_query(connection, borrar, producto_tuple)
			self.ids.rv_productos.data.pop(indice)
			self.ids.rv_productos.refresh_from_data()

	def actualizar_productos(self, producto_actualizado):
		for producto_nuevo in producto_actualizado:
			for producto_viejo in self.ids.rv_productos.data:
				if producto_nuevo['codigo']==producto_viejo['codigo']:
					producto_viejo['cantidad']=producto_nuevo['cantidad']
					break
		self.ids.rv_productos.refresh_from_data()


class VistaProveedores(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.cargar_proveedores, 1)

	def cargar_proveedores(self, *args):
		_proveedores=[]
		connection = QueriesSQLite.create_connection()
		inventario_sql=QueriesSQLite.execute_read_query(connection, "SELECT * from proveedores")
		if inventario_sql: # agregado!!!
			for proveedores in inventario_sql:
				_proveedores.append({'id': proveedores[0], 'nombre': proveedores[1], 'contacto': proveedores[2], 'telefono': proveedores[3],  'email': proveedores[4]})
		self.ids.rv_proveedores.agregar_datos(_proveedores)

	def agregar_proveedores(self, agregar=False, validado=None):
		if agregar:
			proveedores_tuple=tuple(validado.values())
			connection = QueriesSQLite.create_connection()
			crear_proveedor="""
			INSERT INTO
				proveedores (id, nombre, contacto, telefono, email)
			VALUES
				(%s, %s, %s, %s, %s);
			"""
			QueriesSQLite.execute_query(connection, crear_proveedor, proveedores_tuple)
			self.ids.rv_proveedores.data.append(validado)
			self.ids.rv_proveedores.refresh_from_data()
		else:
			popup=ProveedorPopup(self.agregar_proveedores)
			popup.abrir(True)

	def modificar_proveedores(self, modificar=False, validado=None):
		indice=self.ids.rv_proveedores.dato_seleccionado()
		if modificar:
			proveedores_tuple=(validado['id'], validado['nombre'], validado['contacto'], validado['telefono'], validado['email'])
			connection = QueriesSQLite.create_connection()
			actualizar="""
			UPDATE
				proveedores
			SET
				nombre=%s, contacto=%s, telefono=%s, email=%s
			WHERE
				id=%s
			"""
			QueriesSQLite.execute_query(connection, actualizar, proveedores_tuple)
			self.ids.rv_proveedores.data[indice]['nombre']=validado['nombre']
			self.ids.rv_proveedores.data[indice]['contacto']=validado['contacto']
			self.ids.rv_proveedores.data[indice]['telefono']=validado['telefono']
			self.ids.rv_proveedores.data[indice]['email']=validado['email']
			self.ids.rv_proveedores.refresh_from_data()
		else:
			if indice>=0:
				proveedores=self.ids.rv_proveedores.data[indice]
				popup=ProveedorPopup(self.modificar_proveedores)
				popup.abrir(False, proveedores)

	def eliminar_proveedores(self):
		indice=self.ids.rv_proveedores.dato_seleccionado()
		if indice>=0:
			proveedores_tuple=(self.ids.rv_proveedores.data[indice]['id'],)
			connection = QueriesSQLite.create_connection()
			borrar= """DELETE from proveedores WHERE id =%s """
			QueriesSQLite.execute_query(connection, borrar, proveedores_tuple)
			self.ids.rv_proveedores.data.pop(indice)
			self.ids.rv_proveedores.refresh_from_data()

	def actualizar_proveedores(self, proveedores_actualizado):
		for proveedores_nuevo in proveedores_actualizado:
			for proveedores_viejo in self.ids.rv_proveedores.data:
				if proveedores_nuevo['id']==proveedores_viejo['id']:
					proveedores_viejo['telefono']=proveedores_nuevo['telefono']
					break
		self.ids.rv_proveedores.refresh_from_data()


class UsuarioPopup(Popup):
	def __init__(self, _agregar_callback, **kwargs):
		super(UsuarioPopup, self).__init__(**kwargs)
		self.agregar_usuario=_agregar_callback

	def abrir(self, agregar, usuario=None):
		if agregar:
			self.ids.usuario_info_1.text='Agregar Usuario nuevo'
			self.ids.usuario_username.disabled=False
		else:
			self.ids.usuario_info_1.text='Modificar Usuario'
			self.ids.usuario_username.text=usuario['username']
			self.ids.usuario_username.disabled=True
			self.ids.usuario_nombre.text=usuario['nombre']
			self.ids.usuario_password.text=usuario['password']
			if usuario['tipo']=='admin':
				self.ids.admin_tipo.state='down'
			else:
				self.ids.trabajador_tipo.state='down'
		self.open()

	def verificar(self, usuario_username, usuario_nombre, usuario_password, admin_tipo, trabajador_tipo):
		alert1 = 'Falta: '
		validado = {}
		if not usuario_username:
			alert1+='Username. '
			validado['username']=False
		else:
			validado['username']=usuario_username

		if not usuario_nombre:
			alert1+='Nombre. '
			validado['nombre']=False
		else:
			validado['nombre']=usuario_nombre.lower()

		if not usuario_password:
			alert1+='Password. '
			validado['password']=False
		else:
			validado['password']=usuario_password

		if admin_tipo=='normal' and trabajador_tipo=='normal':
			alert1+='Tipo. '
			validado['tipo']=False
		else:
			if admin_tipo=='down':
				validado['tipo']='admin'
			else:
				validado['tipo']='trabajador'

		valores = list(validado.values())

		if False in valores:
			self.ids.no_valid_notif.text=alert1
		else:
			self.ids.no_valid_notif.text=''
			self.agregar_usuario(True,validado)
			self.dismiss()


class VistaUsuarios(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.cargar_usuarios, 1)

	def cargar_usuarios(self, *args):
		_usuarios=[]
		connection = QueriesSQLite.create_connection()
		usuarios_sql=QueriesSQLite.execute_read_query(connection, "SELECT * from usuarios")
		if usuarios_sql: # agregado!!!
			for usuario in usuarios_sql:
				_usuarios.append({'nombre': usuario[1], 'username': usuario[0], 'password': usuario[2], 'tipo': usuario[3]})
		self.ids.rv_usuarios.agregar_datos(_usuarios)

	def agregar_usuario(self, agregar=False, validado=None):
		if agregar:
			usuario_tuple=tuple(validado.values())
			connection = QueriesSQLite.create_connection()
			crear_usuario = """
			INSERT INTO
				usuarios (username, nombre, password, tipo)
			VALUES
				(%s,%s,%s,%s);
			"""
			QueriesSQLite.execute_query(connection, crear_usuario, usuario_tuple)
			self.ids.rv_usuarios.data.append(validado)
			self.ids.rv_usuarios.refresh_from_data()
		else:
			popup=UsuarioPopup(self.agregar_usuario)
			popup.abrir(True)

	def modificar_usuario(self, modificar=False, validado=None):
		indice = self.ids.rv_usuarios.dato_seleccionado()
		if modificar:
			usuario_tuple=(validado['nombre'],validado['password'],validado['tipo'],validado['username'])
			connection = QueriesSQLite.create_connection()
			actualizar = """
			UPDATE
			  usuarios
			SET
			  nombre=%s, password=%s, tipo = %s
			WHERE
			  username = %s
			"""
			QueriesSQLite.execute_query(connection, actualizar, usuario_tuple)
			self.ids.rv_usuarios.data[indice]['nombre']=validado['nombre']
			self.ids.rv_usuarios.data[indice]['tipo']=validado['tipo']
			self.ids.rv_usuarios.data[indice]['password']=validado['password']
			self.ids.rv_usuarios.refresh_from_data()
		else:
			if indice>=0:
				usuario = self.ids.rv_usuarios.data[indice]
				popup = UsuarioPopup(self.modificar_usuario)
				popup.abrir(False,usuario)
		

	def eliminar_usuario(self):
		indice = self.ids.rv_usuarios.dato_seleccionado()
		if indice>=0:
			usuario_tuple=(self.ids.rv_usuarios.data[indice]['username'],)
			connection = QueriesSQLite.create_connection()
			borrar = """DELETE from usuarios where username = %s"""
			QueriesSQLite.execute_query(connection, borrar, usuario_tuple)
			self.ids.rv_usuarios.data.pop(indice)
			self.ids.rv_usuarios.refresh_from_data()


# igual esto es nuevo tambien en kv
class InfoVentaPopup(Popup):
	connection = QueriesSQLite.create_connection()
	select_item_query=" SELECT nombre FROM productos WHERE codigo = %s  "
	def __init__(self, venta, **kwargs):
		super(InfoVentaPopup, self).__init__(**kwargs)	
		self.venta=[{"codigo": producto[3], "producto": QueriesSQLite.execute_read_query(self.connection, self.select_item_query, (producto[3],))[0][0], "cantidad": producto[4], "precio": producto[2], "total": producto[4]*producto[2]} for producto in venta]

	def mostrar(self):
		self.open()
		total_items=0
		total_dinero=0.0
		for articulo in self.venta:
			total_items+=articulo['cantidad']
			total_dinero+=articulo['total']
		self.ids.total_items.text=str(total_items)
		self.ids.total_dinero.text="Gs. "+str("{:.0f}".format(total_dinero))
		self.ids.info_rv.agregar_datos(self.venta)

# nueva clase creada y tabien en kv
class VistaVentas(Screen):
	productos_actuales=[]
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def crear_csv(self):
		connection = QueriesSQLite.create_connection()
		select_item_query=" SELECT nombre FROM productos WHERE codigo=%s "
		if self.ids.ventas_rv.data:
			path = Path(__file__).absolute().parent

			csv_nombre = path.__str__() + '\\ventas_csv\\'
			isExist = os.path.exists(csv_nombre)
			if not isExist:
				os.makedirs(csv_nombre)
				
			csv_nombre += self.ids.date_id.text+'.csv'
			
			productos_csv=[]
			total=0

			for venta in self.productos_actuales:
				for item in venta:
					item_found=next((producto for producto in productos_csv if producto["codigo"] == item[3]), None)
					total+=item[2]*item[4]
					if item_found:
						item_found['cantidad']+=item[4]
						item_found['precio_total']=item_found['precio']*item_found['cantidad']
					else:
						nombre=QueriesSQLite.execute_read_query(connection, select_item_query, (item[3],))[0][0]
						productos_csv.append({'nombre': nombre, 'codigo': item[3], 'cantidad': item[4], 'precio': item[2], 'precio_total': item[2]*item[4]})
			fieldnames=['nombre', 'codigo', 'cantidad', 'precio', 'precio_total']
			bottom=[{'precio_total': total}]
			with open(csv_nombre, 'w', encoding='UTF8', newline='') as f:
				writer=csv.DictWriter(f, fieldnames=fieldnames)
				writer.writeheader()
				writer.writerows(productos_csv)
				writer.writerows(bottom)
			self.ids.notificacion.text='CSV creada y guardad'
		else:
			self.ids.notificacion.text='No hay datos que guardar'

	def mas_info(self):
		indice=self.ids.ventas_rv.dato_seleccionado()
		if indice>=0:
			venta=self.productos_actuales[indice]
			p=InfoVentaPopup(venta)
			p.mostrar()

	def cargar_venta(self, choice='Default'):
		connection = QueriesSQLite.create_connection()
		valid_input = True
		final_sum = 0
		f_inicio = datetime.strptime('01/01/00', '%d/%m/%y')
		f_fin = datetime.strptime('31/12/2099', '%d/%m/%Y')

		_ventas = []
		_total_productos = []

		select_ventas_query = "SELECT * FROM ventas WHERE fecha BETWEEN %s AND %s"
		selec_productos_query = "SELECT * FROM ventas_detalle WHERE id_venta=%s"

		self.ids.ventas_rv.data = []
		if choice == 'Default':
			f_inicio = datetime.today().date()
			f_fin = f_inicio + timedelta(days=1)
			self.ids.date_id.text = str(f_inicio.strftime("%d-%m-%y"))
		elif choice == 'Date':
			date = self.ids.single_date.text
			try:
				f_elegida = datetime.strptime(date, '%d/%m/%y')
			except:
				valid_input = False
			if valid_input:
				f_inicio = f_elegida
				f_fin = f_elegida + timedelta(days=1)
				self.ids.date_id.text = f_elegida.strftime('%d-%m-%y')
		else:
			if self.ids.initial_date.text:
				initial_date = self.ids.initial_date.text
				try:
					f_inicio = datetime.strptime(initial_date, '%d/%m/%y')
				except:
					valid_input = False
			if self.ids.last_date.text:
				last_date = self.ids.last_date.text
				try:
					f_fin = datetime.strptime(last_date, '%d/%m/%y')
				except:
					valid_input = False
			if valid_input:
				self.ids.date_id.text = f_inicio.strftime("%d-%m-%y") + " - " + f_fin.strftime("%d-%m-%y")

		if valid_input:
			inicio_fin = (f_inicio, f_fin)
			ventas_sql = QueriesSQLite.execute_read_query(connection, select_ventas_query, inicio_fin)
			if ventas_sql:
				for venta in ventas_sql:
					final_sum += venta[1]
					ventas_detalle_sql = QueriesSQLite.execute_read_query(connection, selec_productos_query, (venta[0],))
					_total_productos.append(ventas_detalle_sql)
					count = 0
					for producto in ventas_detalle_sql:
						count += producto[4]
					# Si venta[2] ya es un objeto datetime, usa directamente
					_ventas.append({"username": venta[3], "productos": count, "total": venta[1], "fecha": venta[2]})
				self.ids.ventas_rv.agregar_datos(_ventas)
				self.productos_actuales = _total_productos
		self.ids.final_sum.text = '$ ' + str("{:.0f}".format(final_sum))
		self.ids.initial_date.text = ''
		self.ids.last_date.text = ''
		self.ids.single_date.text = ''
		self.ids.notificacion.text = 'Datos de Ventas'



#import dropdown tambien!!!
#agregado customdropdown y tambien en kv y selectablesale label
class CustomDropDown(DropDown):
	def __init__(self, cambiar_callback, **kwargs):
		self._succ_cb = cambiar_callback
		super(CustomDropDown, self).__init__(**kwargs)

	def vista(self, vista):
		if callable(self._succ_cb):
			self._succ_cb(True, vista)


#agregado self.dropdown = CustomDropdown
# def cambiar_vista modificado
# modificado vista_manager en kv
class AdminWindow(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.vista_actual='Productos'
		self.vista_manager=self.ids.vista_manager
		self.dropdown = CustomDropDown(self.cambiar_vista)				# nuevo
		self.ids.cambiar_vista.bind(on_release=self.dropdown.open)		# nuevo
		
		
	def cambiar_vista(self, cambio=False, vista=None):
		if cambio:
			self.vista_actual=vista
			self.vista_manager.current=self.vista_actual
			self.dropdown.dismiss()

	def signout(self):
		self.parent.parent.current='scrn_signin'

	def venta(self):
		self.parent.parent.current='scrn_ventas'

	def actualizar_productos(self, productos):
		self.ids.vista_productos.actualizar_productos(productos)



class AdminApp(App):
	def build(self):
		return AdminWindow()

if __name__=="__main__":
    AdminApp().run() 