import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib
from view import View
from controller import Controller
import gettext
import locale

class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.example.cocktailapp")
        self.controller = None
        self.locale_error = None

    def do_startup(self):
        Gtk.Application.do_startup(self)
        self.controller = Controller()
        self.view = View(self)
        self.controller.set_view(self.view)

        if self.locale_error:  # Si hubo un error de locale, mostrar el mensaje
            self.view.display_error_message(self.locale_error)

    def do_activate(self):
        self.add_window(self.view)
        self.view.present()

if __name__ == "__main__":
    app = Application()

    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error as e:
        app.locale_error = str("Error de configuración en el locale")

    LOCALE_DIR = "locale"
    locale.bindtextdomain('language', LOCALE_DIR)
    gettext.bindtextdomain('language', LOCALE_DIR)
    gettext.textdomain('language')

    app.run(None)

