from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from queries import QueriesSQLite

class VentasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_ventas()

    def load_ventas(self):
        conn = QueriesSQLite.create_connection("pdvDB.sqlite")
        ventas_data = QueriesSQLite.get_all_ventas(conn)
        for venta in ventas_data:
            print(venta)  # Aquí podrías actualizar la interfaz con los datos

class MainApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(VentasScreen(name='scrn_ventas'))
        return self.sm

if __name__ == "__main__":
    Builder.load_file('main.kv')  # Cargar el archivo KV
    MainApp().run()
