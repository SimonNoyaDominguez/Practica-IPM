import requests
from view import View
import threading
from gi.repository import GLib
from model import Model

import gettext
_ = gettext.gettext
N_ = gettext.ngettext

class Controller:

    def __init__(self):
        self.view = None
        self.model = Model()
        

    def set_view(self, view):
        self.view = view

        # Conecta las señales a los manejadores de eventos en la vista
        self.view.search_button.connect("clicked", self.start_search_thread)
        self.view.random_button.connect("clicked", self.start_random_thread)
        self.view.back_button.connect("clicked", self.view.show_initial_widgets)
        self.view.button_exit.connect("clicked", lambda *args: view.error_window.close())
        self.view.search_button_2.connect("clicked", self.start_cocktail_selection_thread)
        self.view.button_exit.connect("clicked", self.view.close_error_window)

    def search_cocktail_by_name(self):
        cocktail_name = self.view.coctel()
        if not cocktail_name:
            GLib.idle_add(self.view.display_error_message, _("No ha ingresado el nombre del cóctel. Por favor, escriba el nombre del cóctel."))
            return

        # Construir la URL de búsqueda con el nombre del cóctel
        url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={cocktail_name}"

        try:
            cocktails = self.model.search_cocktail_by_name(cocktail_name)

            if cocktails is not None:
                if len(cocktails) > 1:
                    # Si hay más de un cóctel, llamar a la función buscar_coctail_coincidentes en la vista
                    GLib.idle_add(self.view.buscar_coctail_coincidentes, cocktails)
                elif len(cocktails) == 1:
                    # Si hay un solo cóctel, mostrar los detalles de ese cóctel
                     GLib.idle_add(self.view.info_coctel, cocktails[0])
            else:
               GLib.idle_add(self.view.display_error_message, _("Error al buscar el cóctel") + f" {cocktail_name}")
        except requests.exceptions.RequestException:
            # Capturar cualquier error de solicitud y mostrar un mensaje de error
            GLib.idle_add(self.view.display_error_message, _("Error de conexión a la API"))

    def get_random_cocktail(self):

        try:
            cocktail = self.model.get_random_cocktail()
            GLib.idle_add(self.view.info_coctel, cocktail)
        except requests.exceptions.RequestException:
            GLib.idle_add(self.view.display_error_message, _("Error de conexión a la API"))

    def cocktail_selection(self):
        cocktail_name = self.view.coctel_2()
        if not cocktail_name:
            GLib.idle_add(self.view.display_error_message, _("No ha ingresado el nombre del cóctel. Por favor, escriba el nombre del cóctel."))
            return

        try:
            cocktails = self.model.search_cocktail_by_name(cocktail_name)

            if cocktails is not None and len(cocktails) > 0:
                GLib.idle_add(self.view.info_coctel, cocktails[0])
            else:
                GLib.idle_add(self.view.display_error_message, _("Error al buscar el cóctel") + f" {cocktail_name}")
        except requests.exceptions.RequestException:
            GLib.idle_add(self.view.display_error_message, _("Error de conexión a la API"))

    def start_search_thread(self, button):
        # Crear un nuevo hilo para la búsqueda por nombre
        thread = threading.Thread(target=self.search_cocktail_by_name)
        thread.start()

    def start_random_thread(self, button):
        # Crear un nuevo hilo para obtener un cóctel aleatorio
        thread = threading.Thread(target=self.get_random_cocktail)
        thread.start()

    def start_cocktail_selection_thread(self, button):
        # Crear un nuevo hilo para la selección de cóctel
        thread = threading.Thread(target=self.cocktail_selection)
        thread.start()
