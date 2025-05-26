# Diseño software

En este documento, se presenta el diseño realizado en leguaje UML mediante Mermaid para los diagramas tanto de la parte estática como dinámica de la primera practica de la asignatura de Interfaz Persona Máquina.


##Diagrama de Clases

A contunuación se representa mediante un digrama de clases, las distinas clases que se emplean. Este diagrma representa la parte estática.
```mermaid
classDiagram
    class aplication {
        +__init__()
        +do_activate()
        +do_startup()
        -controller: Controller
    }
    class Controller {
        +__init__()
        +set_view(view)
        +search_cocktail_by_name()
        +get_random_cocktail()
        +cocktail_selection()
        +start_search_thread(button)
        +start_random_thread(button)
        +start_cocktail_selection_thread(button)
    }
    class Model {
        +__init__()
        +search_cocktail_by_name(cocktail_name: str)
        +get_random_cocktail()
    }
    class View {
        +__init__(app)
        +coctel(): str
        +coctel_2(): str
        +buscar_coctail_coincidentes(data)
        +info_coctel(data)
        +show_initial_widgets(button)
        +error_connection(button)
        +display_error_message(message)
        -search_entry: Gtk.Entry
        -search_button: Gtk.Button
        -search_box: Gtk.Box
        -separator: Gtk.Separator
        -random_button: Gtk.Button
        -error_box: Gtk.Box
        -frame_description: Gtk.Frame
        -description_box: Gtk.Box
        -resultado: Gtk.TextView
        -back_button: Gtk.Button
        -search_entry_2: Gtk.Entry
        -search_button_2: Gtk.Button
        -search_box_2: Gtk.Box
        -button_exit: Gtk.Button
        -image: Gtk.Image
        -image_error: Gtk.Image
        -texto: Gtk.TextBuffer
        -texto_2: Gtk.TextBuffer
    }

    aplication --> Controller
    Controller --> Model
    Controller --> View : depends
```

##Diagramas de flujo:

Los siguentes diagrmas de secuencia representa la parte dinámica del proyecto. 

A continuación se muestra uno de los casos de uso de la aplicación, el caso de busqueda. 

```mermaid
sequenceDiagram
    participant Cliente
    participant App
    participant Controller
    participant Model
    participant View

    Cliente ->> App: Ejecutar la aplicación
    App ->> Controller: Llama a do_activate()
    Controller ->> View: Llama a set_view(view)
    Note over Controller: Inicializa la vista\ny establece controlador
    Controller ->> View: Conecta señales de botón
    Cliente ->> View: Ingresa el nombre del cóctel y pulsa el botón
    View ->> Controller: Llama a start_search_thread()
    Controller ->> Controller: se crea un hilo
    Controller ->> Model: Llama a search_cocktail_by_name()
    Model ->> TheCocktailDB: Llama a search_cocktail_by_name() 
    TheCocktailDB-->>Model: Retorna los datos de cócteles
    Model-->>Controller: Retorna los cócteles encontrados
    Controller->>View: Llama a buscar_coctail_coincidentes(data)
    View ->> Cliente: Muestra los resultados de la búsqueda
    Cliente ->> View: Ingresa el nombre del cóctel y pulsa el botón
    View ->> Controller: Llama a start_cocktail_selection_thread()
    Controller ->> Controller: se crea un hilo
    Controller ->> Model: Llama a cocktail_selection()
    Model ->> TheCocktailDB: Llama a search_cocktail_by_name() 
    TheCocktailDB-->>Model: Retorna los detalles del cóctel
    Model-->>Controller: Retorna los detalles del cóctel
    Controller->>View: Llama a info_coctel(data)
    View ->> Cliente: Muestra la información del cóctel

```

y el siguiente muestra el otro caso de uso, el caso de busqueda random:

```mermaid
sequenceDiagram
    participant Cliente
    participant App
    participant Controller
    participant Model
    participant View

    Cliente ->> App: Ejecutar la aplicación
    App ->> Controller: Llama a do_activate()
    Controller ->> View: Llama a set_view(view)
    Note over Controller: Inicializa la vista y establece controlador
    Controller ->> View: Conecta señales de botón
    Cliente ->> View: Presiona el botón de búsqueda aleatoria
    View ->> Controller: Llama a start_random_thread()
    Controller ->> Controller: se crea un hilo
    Controller ->> Model: Llama a get_random_cocktail() 
    Model ->> TheCocktailDB: Llama a get_random_cocktail() 
    TheCocktailDB-->>Model: Retorna un cóctel aleatorio
    Model-->>Controller: Retorna el cóctel aleatorio
    Controller->>View: Llama a info_coctel(data)
    View ->> Cliente: Muestra la información del cóctel aleatorio

```

##Conclusiones:

Este documento proporciona una visión general de tanto la parte estática como dinámica del proyecto, todo expuesto mediante diagrmas UML para facilitar su entendimiento.
