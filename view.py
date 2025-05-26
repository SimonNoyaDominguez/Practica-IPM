import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import requests


import gettext
_ = gettext.gettext
N_ = gettext.ngettext

class View(Gtk.ApplicationWindow):

    def __init__(self, app):
        super().__init__(application=app)
        self.set_default_size(950, 750)
        self.set_margin_start(10)
        self.set_margin_end(10)
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.connect("destroy", lambda win: app.quit())
        
        self.set_title(("CocktailBar"))  # Cambio aquí

        # Imagen
        self.image = Gtk.Image()
        self.image.set_from_file("cocktail.png")
        self.image.set_size_request(250, 250)
        self.image.set_halign(Gtk.Align.CENTER)
        self.image.set_valign(Gtk.Align.CENTER)

        # Cuadro de búsqueda y botón centrados
        self.search_entry = Gtk.Entry()
        self.search_entry.set_margin_start(310)
        self.search_entry.set_margin_top(10)
        self.search_entry.set_size_request(300, 30)
        self.texto = self.search_entry.get_buffer()
        self.search_button = Gtk.Button(label=_("Watch"))  # Cambio aquí
        self.search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.search_box.append(self.search_entry)
        self.search_box.append(self.search_button)

        # Línea con borde negro
        self.separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.separator.set_margin_top(10)
        self.separator.set_margin_bottom(100)
       

        # Búsqueda aleatoria
        self.random_button = Gtk.Button(label=_("Búsqueda de cóctel aleatorio"))  # Cambio aquí
        self.random_button.set_margin_start(10)

        self.error_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=600)
        self.error_box.append(self.random_button)
                 

        # Frame
        self.frame_description = Gtk.Frame()
        self.frame_description.set_margin_start(10)
        self.frame_description.set_margin_end(10)
        self.frame_description.set_margin_bottom(10)
        self.frame_description.set_margin_top(10)

        self.resultado = Gtk.TextView()
        self.resultado.set_wrap_mode(Gtk.WrapMode.WORD)
        self.resultado.set_cursor_visible(False)
        self.resultado.set_editable(False)

        self.busqueda = Gtk.ScrolledWindow()
        self.busqueda.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)  

        self.busqueda.set_child(self.resultado)
        self.busqueda.set_hexpand(True)
        self.busqueda.set_vexpand(True)
        
        self.description_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.description_box.append(self.busqueda)
                
        # Ajustar el texto a la pantalla
        self.resultado.set_wrap_mode(Gtk.WrapMode.WORD)
        self.resultado.set_cursor_visible(False)
        self.resultado.set_editable(False)

        # Botón "Volver" en el marco de descripción
        self.back_button = Gtk.Button(label=_("Volver"))  # Cambio aquí
        self.back_button.set_margin_end(10)
        self.back_button.set_margin_start(690)
        self.back_button.hide()
        
        self.search_entry_2 = Gtk.Entry()
        self.search_entry_2.set_margin_start(10)
        self.search_entry_2.set_margin_top(25)
        self.search_entry_2.set_size_request(300, 30)
        self.texto_2 = self.search_entry_2.get_buffer()
        self.search_button_2 = Gtk.Button(label=_("Ver"))  # Cambio aquí
        self.search_button_2.set_size_request(10, 10)
        self.search_box_2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.search_box_2.append(self.search_entry_2)
        self.search_box_2.append(self.search_button_2)
        self.search_box_2.hide()
        
        self.description_box.append(self.search_box_2)
        self.description_box.append(self.back_button)  # Agregar el botón "Volver" al final

        self.frame_description.set_child(self.description_box)
        
        self.button_exit = Gtk.Button(label=_("Salir"))  # Cambio aquí
    
        # Contenedor principal
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        main_box.append(self.image)
        main_box.append(self.search_box)
        main_box.append(self.separator)
        main_box.append(self.error_box)
        main_box.append(self.frame_description)
        main_box.set_hexpand(True)
        main_box.set_vexpand(True)
        
        self.set_child(main_box)
        
    def coctel(self) -> str:
        return self.texto.get_text()
        
    def coctel_2(self) -> str:
        return self.texto_2.get_text()
        
    def buscar_coctail_coincidentes(self, data):
        self.image.hide()
        self.search_box.hide()
        self.separator.hide()
        self.error_box.hide()
                
        self.search_entry.set_text('')
        
        self.frame_description.show()
        self.back_button.show()
        self.search_box_2.show()
        respuesta = Gtk.TextBuffer()
        
        # Mostrar información de todas las bebidas encontradas en la respuesta
        for bebida in data:
            nombre = bebida.get("strDrink", _("Nombre no disponible"))
            respuesta.insert_at_cursor(_("Name: ") + nombre + _("\n"))
            
            categoria = bebida.get("strCategory", _("Categoría no disponible"))
            respuesta.insert_at_cursor(_("Category: ") + categoria + _("\n \n"))
            
        self.resultado.set_buffer(respuesta)
        

    def info_coctel(self, data):
        # Esta función se llama cuando se quiere mostrar el frame_description
        self.image.hide()
        self.search_box.hide()
        self.separator.hide()
        self.error_box.hide()
        
        self.back_button.hide()
        self.search_box_2.hide()
    
        self.frame_description.show()
        self.back_button.show()
        respuesta = Gtk.TextBuffer()
        
        self.search_entry.set_text('')
        self.search_entry_2.set_text('')        
          
        # Mostrar todos los campos disponibles del cóctel
        nombre = data.get("strDrink", _("Nombre no disponible"))
        respuesta.insert_at_cursor(_("Name: ") + nombre + _("\n"))

        categoria = data.get("strCategory", _("Categoría no disponible"))
        respuesta.insert_at_cursor(_("Category: ") + categoria + _("\n"))

        tipo_vaso = data.get("strGlass", _("Tipo de vaso no disponible"))
        respuesta.insert_at_cursor(_("Glass type: ") + tipo_vaso + _("\n"))

        instrucciones = data.get("strInstructions", _("Instrucciones no disponibles"))
        respuesta.insert_at_cursor(_("Instructions: ") + instrucciones + _("\n\n"))

        for i in range(1, 16):
            ingrediente = data.get(f"strIngredient{i}", "")
            medida = data.get(f"strMeasure{i}", "")
            if ingrediente and medida:
                respuesta.insert_at_cursor(_("Ingredient") + f" {i}: " + medida + ingrediente + _("\n"))

        self.resultado.set_buffer(respuesta)


    def show_initial_widgets(self, button):
        # Esta función se llama cuando se pulsa el botón "Volver"
        self.image.show()
        self.search_box.show()
        self.separator.show()
        self.error_box.show()
        self.frame_description.hide()
        self.back_button.hide()
        # Limpiar el contenido del TextView
        respuesta = Gtk.TextBuffer()
        self.resultado.set_buffer(respuesta)
    
    def close_error_window(self, button):
        if self.error_window:
           self.error_window.close()   
 
    def display_error_message(self, message):
        # Implementa esta función para mostrar un mensaje de error en la vista
        self.error_window = Gtk.Window()
        self.error_window.set_default_size(900, 400)
        self.error_window.set_title(_("Error"))  # Cambio aquí

        label = Gtk.Label()
        label.set_text(message)
        
        self.image_error = Gtk.Image()
        self.image_error.set_from_file("error.png")
        self.image_error.set_size_request(250, 250)
        self.image_error.set_halign(Gtk.Align.CENTER)
        self.image_error.set_valign(Gtk.Align.CENTER)
        
        box_error = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        box_error.append(self.image_error)
        box_error.append(label)
        box_error.append(self.button_exit)
              
        self.error_window.set_child(box_error)
        self.error_window.show()


