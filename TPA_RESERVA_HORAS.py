import tkinter as tk            # para la interfaz gráfica
import json                     # para guardar las reservas en un archivo .json para simular una base de datos
from tkinter import messagebox  # para mostrar mensajes de error o información
from PIL import Image, ImageTk  # para cargar imágenes en la interfaz gráfica





# Clase para realizar reservas
# Se pueden realizar reservas en una cancha de fútbol, tenis o pádel
# Se puede reservar una hora de 08:00 a 23:00
# Se puede reservar solo una hora por día en alguno de los establecimientos
# Se puede reservar solo una vez el mismo horario en el mismo establecimiento
# Se pueden ver las reservas guardadas
# ejemplo: si se reserva la cancha de fútbol a las 08:00, no se puede reservar la cancha de fútbol a las 08:00

class Reservas():

    # Constructor de la clase

    def __init__(self):

        # Creación de la ventana principal, definición de su tamaño y título

        self.ventana = tk.Tk()
        self.ventana.geometry('1600x1200')
        self.ventana.title("Reservaciones ICINF")
        # Estilos de la interfaz gráfica

        self.estilo_principal = ("Helvetica", 24, "bold")
        self.estilo_entry = ("Arial", 10)
        self.estilo_boton = ("Arial", 10, "bold")
        self.color_principal = "#3F4FFF"
        self.color_boton = "#3F4FFF"
        self.color_texto_boton = "white"

        # Creación de los elementos de la interfaz gráfica mejor conocidos como widgets
        # Se crean etiquetas, campos de entrada, menús desplegables y botones
        # Se definen las propiedades de cada widget
        # Se empaquetan los widgets en un frame principal
        # Se empaqueta el frame principal en la ventana principal
        # Se definen los eventos que se ejecutarán al presionar los botones "Reservar", "Cancelar" y "Ver reservas"
        # Estos llamaran a los metodos reservar(), cancelar() y abrir_reserva() respectivamente

        self.frame_principal = tk.Frame(self.ventana)
        self.frame_principal.pack(expand=True, padx=20, pady=20)

        self.titulo = tk.Label(self.frame_principal, text="Bienvenido a tu programa de reservas favorito", font=self.estilo_principal, fg=self.color_principal, bg='#f0f0f0')
        self.titulo.pack(pady=10)
        
        self.nombre_label = tk.Label(self.frame_principal, text="Usuario:", font=self.estilo_entry, bg='#f0f0f0')
        self.nombre_label.pack()
        self.usuario_entry = tk.Entry(self.frame_principal, font=self.estilo_entry, highlightthickness=2)
        self.usuario_entry.pack(pady=5)

        self.recinto_select = tk.StringVar()
        self.recinto_select.set("Seleccione una opción")
        self.recinto_select.trace("w", lambda *args: self.cargar_horas())
        self.recinto_label = tk.Label(self.frame_principal, text="Recinto:", font=self.estilo_entry, bg='#f0f0f0')
        self.recinto_label.pack()
        self.recinto_select_menu = tk.OptionMenu(self.frame_principal, self.recinto_select, "Seleccione una opción", "Cancha de Fútbol", "Cancha de Tenis", "Cancha de Pádel")
        self.recinto_select_menu.config(font=self.estilo_entry, highlightthickness=2)
        self.recinto_select_menu.pack(pady=5)
        
        self.hora_label = tk.Label(self.frame_principal, text="Hora:", font=self.estilo_entry, bg='#f0f0f0')
        self.hora_label.pack()
        
        self.hora_select = tk.StringVar()
        self.hora_select.set("Seleccione hora")
        self.hora_select_menu = tk.OptionMenu(self.frame_principal, self.hora_select, "Seleccione hora")
        self.hora_select_menu.config(font=self.estilo_entry, highlightthickness=2)
        self.hora_select_menu.pack(pady=5)
        
        self.reservar_boton = tk.Button(self.frame_principal, text="Reservar", command=self.reservar, font=self.estilo_boton, bg=self.color_boton, fg=self.color_texto_boton, padx=10, pady=5, bd=0)
        self.reservar_boton.pack(pady=10)

        self.cancelar_boton = tk.Button(self.frame_principal, text="Cancelar", command=self.cancelar, font=self.estilo_boton, bg=self.color_boton, fg=self.color_texto_boton, padx=10, pady=5, bd=0)
        self.cancelar_boton.pack(pady=5)

        self.reservas_guardadas = []  
        self.horarios_reservados = set()

        self.abrir_reserva_boton = tk.Button(self.frame_principal, text="Ver reservas", command=self.abrir_reserva, font=self.estilo_boton, bg=self.color_boton, fg=self.color_texto_boton, padx=10, pady=5, bd=0)
        self.abrir_reserva_boton.pack(pady=10)

        self.ver_recintos_boton = tk.Button(self.frame_principal, text="Ver recintos", command=self.ver_recintos, font=self.estilo_boton, bg=self.color_boton, fg=self.color_texto_boton, padx=10, pady=5, bd=0)
        self.ver_recintos_boton.pack(pady=10)

        # creamos un diccionario con las imagenes de los recintos para que no se borren al ejecutar el programa

        self.imagenes = {

            "Cancha de Fútbol": Image.open("cancha.png"),
            "Cancha de Tenis": Image.open("tenis.png"),
            "Cancha de Pádel": Image.open("padel.png")
        
        }

        self.imagen_label = tk.Label(self.frame_principal, bg='#f0f0f0')
        self.imagen_label.pack()

        # Creamos un diccionario con las descripciones de los recintos

        self.descripcion =  {

            'Cancha de Fútbol': 'Panamá, Osorno, Chile. Cancha de fútbol de césped sintético, baños y vestuarios disponibles, horario de 8:00 hasta 23:00.\n Entrada accesible para personas en silla de ruedas.\n Estacionamiento accesible para personas en silla de ruedas. \n Piscina disponible. \n Ideal para ir con niños.\n $50000 c/h',
            'Cancha de Tenis': 'José Fruto Sáez S/N, Osorno, Chile. Cancha de tenis de arcilla, baños y vestuarios disponibles, horario de 8:00 hasta 23:00. \n $30000 c/h',
            'Cancha de Pádel': 'Camino a Puerto Octay km 1 , Osorno, Chile. Cancha de pádel de cemento, baños y vestuarios disponibles, horario de 8:00 hasta 23:00. \n $25000 c/h'

        }

        self.descripcion_label = tk.Label(self.frame_principal, bg='#f0f0f0')
        self.descripcion_label.pack()

    ###############################################################################
    ########################### MÉTODOS DE LA CLASE ###############################
    ###############################################################################

    # Llamamos a la función reservar() cuando se presiona el botón "Reservar"
    # Esta función se encarga de validar los datos ingresados por el usuario y de realizar la reserva
    # Si los datos son correctos, se guarda la reserva en un archivo .json y se muestra un mensaje de éxito
    # Si hay algún error, se muestra un mensaje de error correspondiente

    def reservar(self): # Método

        nombre = str(self.usuario_entry.get()).lower() # Se obtienen los datos ingresados por el usuario
        recinto = self.recinto_select.get() # Se obtienen los datos ingresados por el usuario x2
        hora = self.hora_select.get() # Se obtienen los datos ingresados por el usuario x3
    
        if not nombre: # Si no se ingresa un nombre de usuario

            messagebox.showerror("Error", "Debe ingresar un nombre de usuario") # Se muestra un mensaje de error
            

        elif len(nombre) < 3 or len(nombre) > 25: # Si el nombre de usuario tiene menos de 3 letras o más de 25
                
            messagebox.showerror("Error", "El nombre de usuario debe tener al menos 3 letras y no más de 25") # Se muestra un mensaje de error
            

        elif any(character.isdigit() for character in nombre): # Si el nombre de usuario contiene números

            messagebox.showerror("Error", "El nombre de usuario no puede contener números") # Se muestra un mensaje de error
            

        elif not recinto or recinto == "Seleccione una opción": # Si no se selecciona un recinto

            messagebox.showerror("Error", "Debe seleccionar un recinto") # Se muestra un mensaje de error
            

        elif not hora or hora == "Seleccione hora": # Si no se selecciona una hora

            messagebox.showerror("Error", "Debe seleccionar una hora") # Se muestra un mensaje de error
            

        elif any(reserva["nombre"] == nombre for reserva in self.reservas_guardadas): # Si el usuario ya ha reservado una hora en algún recinto
        
            messagebox.showerror("Error", "Solo puedes reservar 1 hora por día en alguna de nuestros establecimientos") # Se muestra un mensaje de error
            

        elif any(reserva["recinto"] == recinto and reserva["hora"] == hora for reserva in self.reservas_guardadas): # Si el horario ya ha sido reservado para el recinto seleccionado
        
            messagebox.showerror("Error", "Este horario ya ha sido reservado para este recinto") # Se muestra un mensaje de error
            

        else:

            reserva = {"nombre": nombre, "recinto": recinto, "hora": hora} # Se crea un diccionario con los datos de la reserva
            self.reservas_guardadas.append(reserva) # Se añade la reserva a la lista de reservas guardadas
            self.horarios_reservados.add((recinto, hora)) # Se añade el horario reservado al conjunto de horarios reservados
            messagebox.showinfo("Reserva realizada", f"Reserva realizada con éxito\nNombre: {nombre}\nRecinto: {recinto}\nHora: {hora}") # Se muestra un mensaje de éxito
            self.guardar_reservas() # Se guardan las reservas en el archivo .json
            self.cancelar() # Se llama a la función cancelar() para limpiar los campos de usuario, recinto y hora



    # Método para cargar las horas disponibles según el recinto seleccionado
    # Se cargan las horas disponibles según el recinto seleccionado
    # Si el recinto es una cancha de fútbol, tenis o pádel, se cargan las horas de 08:00 a 23:00
    # Si el recinto es una sala de estudio, se cargan las horas de 08:00 a 20:00

    def cargar_horas(self): # Método

        recinto = self.recinto_select.get() # Se obtiene el recinto seleccionado
        horas = [] # Se crea una lista para almacenar las horas disponibles

        if recinto in ["Cancha de Fútbol", "Cancha de Tenis", "Cancha de Pádel"]: # Si el recinto es una cancha de fútbol, tenis o pádel: # Si el recinto es una cancha de fútbol, tenis o pádel

            horas = ["Seleccione hora", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
                        
            self.mostrar_imagen(recinto) # Se llama a la función mostrar_imagen() para mostrar la imagen del recinto seleccionado

        if recinto == "Seleccione una opción": # Si no se selecciona un recinto

            self.hora_select.set("Seleccione hora")
            self.hora_select_menu['menu'].delete(0, 'end')
            self.imagen_label.config(image=None) # Se muestra la imagen del recinto seleccionado
            self.descripcion_label.config(text="")
            self.imagen_label.image = None
            
        self.hora_select.set(horas[0]) # Se establece la primera hora como la hora seleccionada
        self.hora_select_menu['menu'].delete(0, 'end')
        
        for hora in horas:
        
            self.hora_select_menu['menu'].add_command(label=hora, command=tk._setit(self.hora_select, hora))

        mostrar_descripcion = self.descripcion.get(recinto) # Se obtiene la descripción del recinto seleccionado
        self.descripcion_label.config(text=mostrar_descripcion) # Se muestra la descripción del recinto seleccionado



    # Método para cancelar la reserva
    # Se limpian los campos de usuario, recinto y hora

    def cancelar(self): # Método

        self.usuario_entry.delete(0, tk.END) # Se limpian los campos de usuario, recinto y hora
        self.recinto_select.set("Seleccione una opción") # Se limpian los campos de usuario, recinto y hora
        self.hora_select.set("Seleccione hora") # Se limpian los campos de usuario, recinto y hora
        self.imagen_label.image = None



    # Método para guardar las reservas en un archivo .json
    # Se guardan las reservas en un archivo .json para simular una base de datos

    def guardar_reservas(self): # Método

        with open("reservas.json", "w") as fecha1: # Se abre el archivo .json de reservas

            json.dump(self.reservas_guardadas, fecha1) # Se guardan las reservas en el archivo .json
        # la letra "w" indica que se va a escribir en el archivo .json y si el archivo no existe, se crea uno nuevo
        # por otro lado la letra "r" indica que se va a leer el archivo .json y si el archivo no existe, se produce un error



    # Método para listar las reservas guardadas
    # Se listan las reservas guardadas en el archivo .json
    # Se muestran en un cuadro de texto las reservas guardadas

    def listar_reservas(self): # Método

        self.reservas_text.config(state=tk.NORMAL) # Se habilita la edición del cuadro de texto de reservas
        self.reservas_text.delete(1.0, tk.END) # Se limpia el cuadro de texto de reservas

        for reserva in self.reservas_guardadas: # Se recorren las reservas guardadas

            self.reservas_text.insert(tk.END, f" {self.imagen} \n Nombre: {reserva['nombre']}\nRecinto: {reserva['recinto']}\nHora: {reserva['hora']}\n\n") # Se muestra la reserva en el cuadro de texto de reservas
        
        self.reservas_text.config(state=tk.DISABLED) # Se deshabilita la edición del cuadro de texto de reservas



    # Método para abrir la ventana de visualización de reservas
    # Se cierra la ventana actual y se abre la ventana de visualización de reservas

    def abrir_reserva(self): # Método
        
        self.ventana.destroy() # Se cierra la ventana actual
        app2 = VisualizarReservas() # Se crea una instancia de la clase VisualizarReservas
        app2.ventana.mainloop() # Se inicia la ventana principal



    # Método para mostrar la imagen del recinto seleccionado
    # Se muestra la imagen del recinto seleccionado en la interfaz gráfica
    # Este metodo es llamado por la funcion cargar_horas()
    # cuando esta se ejecuta y se selecciona un recinto

    def mostrar_imagen(self, recinto): # Método

        imagen = self.imagenes.get(recinto) # Se obtiene la imagen del recinto seleccionado
        imagen = imagen.resize((400, 400), Image.ANTIALIAS) # Se redimensiona la imagen del recinto seleccionado
        
        # antialias es un método de suavizado de la imagen para evitar el efecto de escalera
        # se utiliza para mejorar la calidad de la imagen redimensionada
        # para entender mejor el efecto de escalera, se puede ver en la imagen de la cancha de fútbol como las líneas de la cancha se ven pixeladas

        if imagen: # Si se encuentra la imagen del recinto seleccionado

            imagen = ImageTk.PhotoImage(imagen) # Se carga la imagen del recinto seleccionado
            self.imagen_label.config(image=imagen) # Se muestra la imagen del recinto seleccionado
            self.imagen_label.image = imagen  # Referencia necesaria para evitar que la imagen sea eliminada por el recolector de basura
        
        else: # Si no se encuentra la imagen del recinto seleccionado
        
            self.imagen_label.image = None # Se muestra la imagen del recinto seleccionado, o en este caso, no se muestra ninguna imagen



    # Método para ver los recintos disponibles
    # Se cierra la ventana actual y se abre la ventana de recintos

    def ver_recintos(self):
            
            self.ventana.destroy() 
            app3 = Recintos()
            app3.ventana.mainloop()




# clase para visualizar las reservas guardadas
# Se muestra un cuadro de texto con las reservas guardadas
# Se puede buscar una reserva por el nombre del usuario
# Se puede eliminar una reserva por el nombre del usuario
        
class VisualizarReservas():

    # Constructor de la clase

    def __init__(self):

        # Creación de la ventana principal, definición de su tamaño y título
        
        self.ventana = tk.Tk()
        self.ventana.geometry('1600x1200')
        self.ventana.title("Reservaciones ICINF")

        # Estilos de la interfaz gráfica

        self.estilo_principal = ("Helvetica", 24, "bold")
        self.estilo_entry = ("Arial", 10)
        self.estilo_boton = ("Arial", 10, "bold")
        self.color_principal = "#3F4FFF"
        self.color_boton = "#3F4FFF"
        self.color_texto_boton = "white"

        # Creación de los elementos de la interfaz gráfica mejor conocidos como widgets
        # Se crean etiquetas, campos de entrada y botones
        # Se definen las propiedades de cada widget
        # Se empaquetan los widgets en un frame principal
        # Se empaqueta el frame principal en la ventana principal
        # Se definen los eventos que se ejecutarán al presionar los botones "Buscar", "Eliminar reserva" y "Volver"
        # Estos llamaran a los metodos buscar_reserva(), eliminar_reserva() y volver() respectivamente

        self.frame_principal = tk.Frame(self.ventana, bg='#f0f0f0')
        self.frame_principal.pack(expand=True, padx=20, pady=20)

        self.titulo = tk.Label(self.frame_principal, text="Visualizar reservas", font=self.estilo_principal, fg=self.color_principal, bg='#f0f0f0')
        self.titulo.pack(pady=10)
        
        self.dialogo = tk.Label(self.frame_principal, text="Aquí puedes buscar y eliminar reservas por el nombre del usuario", font=self.estilo_entry, bg='#f0f0f0')
        self.dialogo.pack(pady=10)

        self.buscar_label = tk.Label(self.frame_principal, text="Buscar por nombre:", font=self.estilo_entry, bg='#f0f0f0')
        self.buscar_label.pack()

        self.buscar_entry = tk.Entry(self.frame_principal, font=self.estilo_entry, highlightthickness=2)
        self.buscar_entry.pack(pady=5)

        self.buscar_boton = tk.Button(self.frame_principal, text="Buscar", command=self.buscar_reserva, font=self.estilo_boton, bg=self.color_boton, fg=self.color_texto_boton, padx=10, pady=5, bd=0)
        self.buscar_boton.pack(pady=10)

        self.reservas_label = tk.Label(self.frame_principal, text="Reservas:", font=self.estilo_entry, bg='#f0f0f0')
        self.reservas_label.pack()

        self.reservas_text = tk.Text(self.frame_principal, font=self.estilo_entry, height=10, width=50)
        self.reservas_text.pack()
            
        self.eliminar_boton = tk.Button(self.frame_principal, text="Eliminar reserva", command=self.eliminar_reserva, font=self.estilo_boton, bg=self.color_boton, fg=self.color_texto_boton, padx=10, pady=5, bd=0)
        self.eliminar_boton.pack(pady=10)

        self.volver_boton = tk.Button(self.frame_principal, text="Volver", command=self.volver, font=self.estilo_boton, bg=self.color_boton, fg=self.color_texto_boton, padx=10, pady=5, bd=0)
        self.volver_boton.pack(pady=10) 

        # Se cargan las reservas guardadas en el archivo .json
        # Se verifica si hay reservas guardadas
        # Si no hay reservas guardadas, se muestra un mensaje de información y se cierra la ventana
        # Si hay reservas guardadas, se cargan en el cuadro de texto de reservas

        self.cargar_reservas() # Se llama a la función cargar_reservas() para cargar las reservas guardadas en el archivo .json
        self.esta_vacia() # Se llama a la función esta_vacia()

    ###############################################################################
    ########################### MÉTODOS DE LA CLASE ###############################
    ###############################################################################

    # Llamamos a la función esta_vacia() cuando se abre la ventana
    # Esta función verifica si hay reservas guardadas
    # Si no hay reservas guardadas, se muestra un mensaje de información y se cierra la ventana
    # Si hay reservas guardadas, se cargan en el cuadro de texto de reservas

    def esta_vacia(self): # Método

        if not self.reservas: # Si no hay reservas guardadas

            messagebox.showinfo("Información", "No hay reservas guardadas") # Se muestra un mensaje de información
            self.ventana.destroy() # Se cierra la ventana actual
            app = Reservas() # Se crea una instancia de la clase Reservas
            app.ventana.mainloop() # Se inicia la ventana principal

        else: # Si hay reservas guardadas

            self.cargar_reservas() # Se cargan las reservas guardadas en el cuadro de texto de reservas



    # Método para cargar las reservas guardadas
    # Se cargan las reservas guardadas en el archivo .json
    # Se cargan las reservas guardadas en el cuadro de texto de reservas

    def cargar_reservas(self): # Método
        
        self.reservas_text.delete(1.0, tk.END) # Se limpia el cuadro de texto de reservas

        with open("reservas.json", "r") as fecha1: # Se abre el archivo .json de reservas

            self.reservas = json.load(fecha1) # Se cargan las reservas guardadas en el archivo .json
            
            for reserva in self.reservas: # Se recorren las reservas guardadas
            
                self.reservas_text.insert(tk.END, f"Nombre: {reserva['nombre']}\nRecinto: {reserva['recinto']}\nHora: {reserva['hora']}\n\n") # Se muestra la reserva en el cuadro de texto de reservas
            
            self.reservas_text.config(state=tk.DISABLED) # Se deshabilita la edición del cuadro de texto de reservas



    # Método para buscar una reserva por el nombre del usuario
    # Se busca una reserva por el nombre del usuario
    # Se muestra en el cuadro de texto de reservas las reservas encontradas
    # Si no se encuentra ninguna reserva, se muestra un mensaje de información

    def buscar_reserva(self):

        nombre_buscar = self.buscar_entry.get() # Se obtiene el nombre del usuario a buscar
        self.reservas_text.config(state=tk.NORMAL) # Se habilita la edición del cuadro de texto de reservas
        self.reservas_text.delete(1.0, tk.END) # Se limpia el cuadro de texto de reservas
        encontradas = [] # Se crea una lista para almacenar las reservas encontradas
        
        with open("reservas.json", "r") as fecha1: # Se abre el archivo .json de reservas

            self.reservas = json.load(fecha1) # Se cargan las reservas guardadas en el archivo .json

            for reserva in self.reservas: # Se recorren las reservas guardadas

                if nombre_buscar.lower() in reserva['nombre'].lower(): # Se busca la reserva por el nombre del usuario

                    encontradas.append(reserva) # Se agrega la reserva a la lista de reservas encontradas
                    self.reservas_text.insert(tk.END, f"Nombre: {reserva['nombre']}\nRecinto: {reserva['recinto']}\nHora: {reserva['hora']}\n\n") # Se muestra la reserva en el cuadro de texto de reservas

        self.reservas_text.config(state=tk.DISABLED) # Se deshabilita la edición del cuadro de texto de reservas

        if not encontradas: # Si no se encuentra ninguna reserva

            messagebox.showinfo("Información", "No se encontraron reservas con ese nombre.") # Se muestra un mensaje de información



    # Método para eliminar una reserva por el nombre del usuario
    # Se elimina una reserva por el nombre del usuario
    # Se muestra un mensaje de éxito si se elimina la reserva
    # Se muestra un mensaje de información si no se encuentra la reserva
    # Se muestra un mensaje de información si se eliminan todas las reservas
    # Se cierra la ventana actual y se abre la ventana de reservas

    def eliminar_reserva(self): # Método
        
        nombre_buscar = self.buscar_entry.get() # Se obtiene el nombre del usuario a buscar
        
        if not nombre_buscar: # Si no se ingresa un nombre de usuario
        
            messagebox.showinfo("Información", "Debe ingresar un usuario para poder eliminar una reserva") # Se muestra un mensaje de información
            return 
        
        else: # Si se ingresa un nombre de usuario
            
            self.reservas = json.load(open("reservas.json")) # Se cargan las reservas guardadas en el archivo .json

        for reserva in self.reservas: # Se recorren las reservas guardadas

            if nombre_buscar.lower() in reserva['nombre'].lower(): # Se busca la reserva por el nombre del usuario

                self.reservas.remove(reserva) # Se elimina la reserva
                self.reservas_text.config(state=tk.NORMAL) # Se habilita la edición del cuadro de texto de reservas
                self.reservas_text.delete(1.0, tk.END) # Se limpia el cuadro de texto de reservas
                
                for reserva in self.reservas: # Se recorren las reservas guardadas
                    
                    self.reservas_text.insert(tk.END, f"Nombre: {reserva['nombre']}\nRecinto: {reserva['recinto']}\nHora: {reserva['hora']}\n\n") # Se muestra la reserva en el cuadro de texto de reservas
                
                self.reservas_text.config(state=tk.DISABLED) # Se deshabilita la edición del cuadro de texto de reservas
                self.guardar_reservas() # Se guardan las reservas en el archivo .json
                messagebox.showinfo("Información", "Reserva eliminada.") # Se muestra un mensaje de éxito
                
                if not self.reservas: # Si no hay reservas guardadas

                    messagebox.showinfo("Información", "Se han eliminado todas las reservas.") # Se muestra un mensaje de información
                    self.ventana.destroy() # Se cierra la ventana actual
                    app = Reservas() # Se crea una instancia de la clase Reservas
                    app.ventana.mainloop() # Se inicia la ventana principal
                
                return 
            
        messagebox.showinfo("Información", "No existe una reserva con ese nombre") # Se muestra un mensaje de información



    # Método para guardar las reservas en un archivo .json
    # Se guardan las reservas en un archivo .json para simular una base de datos

    def guardar_reservas(self): # Método

        with open("reservas.json", "w") as fecha1: # Se abre el archivo .json de reservas
            
            json.dump(self.reservas, fecha1) # Se guardan las reservas en el archivo .json



    # Método para volver a la ventana de reservas
    # Se cierra la ventana actual y se abre la ventana de reservas
 
    def volver(self): # Método

        self.ventana.destroy() # Se cierra la ventana actual
        app = Reservas() # Se crea una instancia de la clase Reservas
        app.ventana.mainloop() # Se inicia la ventana principal





class Recintos():

    # Constructor de la clase

    def __init__(self):

        # Creación de la ventana principal, definición de su tamaño y título

        self.ventana = tk.Tk()
        self.ventana.geometry('800x600')
        self.ventana.title("Reservaciones ICINF")
        
        # Estilos de la interfaz gráfica

        self.estilo_principal = ("Helvetica", 24, "bold")
        self.estilo_entry = ("Arial", 10)
        self.estilo_boton = ("Arial", 10, "bold")
        self.color_principal = "#3F4FFF"
        self.color_boton = "#3F4FFF"
        self.color_texto_boton = "white"

        # Creación de los elementos de la interfaz gráfica mejor conocidos como widgets
        # Se crean etiquetas, campos de entrada y botones
        # Se definen las propiedades de cada widget
        # Se empaquetan los widgets en un frame principal
        # Se empaqueta el frame principal en la ventana principal
        # Se definen los eventos que se ejecutarán al presionar los botones "Cancha de Fútbol", "Cancha de Tenis" y "Cancha de Pádel"
        # Estos llamaran a los metodos cancha_futbol(), cancha_tenis() y cancha_padel() respectivamente

        self.frame_principal = tk.Frame(self.ventana, bg='#f0f0f0')
        self.frame_principal.pack(expand=True, padx=20, pady=20)

        self.titulo = tk.Label(self.frame_principal, text="Recintos", font=self.estilo_principal, fg=self.color_principal, bg='#f0f0f0')
        self.titulo.pack(pady=10)
        
        self.dialogo = tk.Label(self.frame_principal, text="Selecciona un recinto para ver su descripción", font=self.estilo_entry, bg='#f0f0f0')
        self.dialogo.pack(pady=10)

        self.cancha_futbol_boton = tk.Button(self.frame_principal, text="Cancha de Fútbol", command=self.cancha_futbol , font=self.estilo_boton, bg=self.color_boton, fg=self.color_texto_boton, padx=10, pady=5, bd=0)

        self.cancha_futbol_boton.pack(pady=10)

        self.cancha_tenis_boton = tk.Button(self.frame_principal, text="Cancha de Tenis", command=self.cancha_tenis, font=self.estilo_boton, bg=self.color_boton, fg=self.color_texto_boton, padx=10, pady=5, bd=0)
        self.cancha_tenis_boton.pack(pady=10)

        self.cancha_padel_boton = tk.Button(self.frame_principal, text="Cancha de Pádel", command=self.cancha_padel, font=self.estilo_boton, bg=self.color_boton, fg=self.color_texto_boton, padx=10, pady=5, bd=0)
        self.cancha_padel_boton.pack(pady=10)

        self.volver_boton = tk.Button(self.frame_principal, text="Volver", command=self.volver, font=self.estilo_boton, bg=self.color_boton, fg=self.color_texto_boton, padx=10, pady=5, bd=0)
        self.volver_boton.pack(pady=10)
        
        self.imagen_label = tk.Label(self.frame_principal, bg='#f0f0f0')
        self.imagen_label.pack()

    ###############################################################################
    ########################### MÉTODOS DE LA CLASE ###############################
    ###############################################################################

    # Se muestra la descripción de la cancha de fútbol en la interfaz gráfica

    def cancha_futbol(self): # Método
        
        imagen = Image.open("cancha.png") # Se carga la imagen de la cancha de fútbol
        imagen = imagen.resize((400, 400), Image.ANTIALIAS) # Se redimensiona la imagen de la cancha de fútbol
        imagen = ImageTk.PhotoImage(imagen) # Se carga la imagen de la cancha de fútbol
        self.imagen_label.config(image=imagen) # Se muestra la imagen de la cancha de fútbol
        self.imagen_label.image = imagen  # Referencia necesaria para evitar que la imagen sea eliminada por el recolector de basura

        self.dialogo.config(text="Cancha de Fútbol\nPanamá, Osorno, Chile. Cancha de fútbol de césped sintético, baños y vestuarios disponibles, horario de 8:00 hasta 23:00.\n Entrada accesible para personas en silla de ruedas.\n Estacionamiento accesible para personas en silla de ruedas. \n Piscina disponible. \n Ideal para ir con niños.\n $50000 c/h")



    # Método para mostrar la descripción de la cancha de tenis

    def cancha_tenis(self): # Método
            
        imagen = Image.open("tenis.png") # Se carga la imagen de la cancha de tenis
        imagen = imagen.resize((400, 400), Image.ANTIALIAS) # Se redimensiona la imagen de la cancha de tenis
        imagen = ImageTk.PhotoImage(imagen) # Se carga la imagen de la cancha de tenis
        self.imagen_label.config(image=imagen) # Se muestra la imagen de la cancha de tenis
        self.imagen_label.image = imagen  # Referencia necesaria para evitar que la imagen sea eliminada por el recolector de basura
        
        self.dialogo.config(text="Cancha de Tenis\nJosé Fruto Sáez S/N, Osorno, Chile. Cancha de tenis de arcilla, baños y vestuarios disponibles, horario de 8:00 hasta 23:00. \n $30000 c/h")



    # Método para mostrar la descripción de la cancha de pádel

    def cancha_padel(self): # Método

        imagen = Image.open("padel.png") # Se carga la imagen de la cancha de pádel
        imagen = imagen.resize((400, 400), Image.ANTIALIAS) # Se redimensiona la imagen de la cancha de pádel
        imagen = ImageTk.PhotoImage(imagen) # Se carga la imagen de la cancha de pádel
        self.imagen_label.config(image=imagen) # Se muestra la imagen de la cancha de pádel
        self.imagen_label.image = imagen  # Referencia necesaria para evitar que la imagen sea eliminada por el recolector de basura

        self.dialogo.config(text="Cancha de Pádel\nCamino a Puerto Octay km 1 , Osorno, Chile. Cancha de pádel de cemento, baños y vestuarios disponibles, horario de 8:00 hasta 23:00. \n $25000 c/h")
    


    # Método para mostrar la imagen del recinto seleccionado

    def mostrar_imagen(self, recinto): # Método

        imagen = self.imagenes.get(recinto) # Se obtiene la imagen del recinto seleccionado
        imagen = imagen.resize((400, 400), Image.ANTIALIAS) # Se redimensiona la imagen del recinto seleccionado
        
        # antialias es un método de suavizado de la imagen para evitar el efecto de escalera
        # se utiliza para mejorar la calidad de la imagen redimensionada
        # para entender mejor el efecto de escalera, se puede ver en la imagen de la cancha de fútbol como las líneas de la cancha se ven pixeladas

        if imagen: # Si se encuentra la imagen del recinto seleccionado

            imagen = ImageTk.PhotoImage(imagen) # Se carga la imagen del recinto seleccionado
            self.imagen_label.config(image=imagen) # Se muestra la imagen del recinto seleccionado
            self.imagen_label.image = imagen  # Referencia necesaria para evitar que la imagen sea eliminada por el recolector de basura
        
        else: # Si no se encuentra la imagen del recinto seleccionado
        
            self.imagen_label.image = None # Se muestra la imagen del recinto seleccionado, o en este caso, no se muestra ninguna imagen



    # Método para volver a la ventana de reservas

    def volver(self): # Método
            
            self.ventana.destroy()
            app = Reservas()
            app.ventana.mainloop()
    




# Función principal
# Se crea una instancia de la clase Reservas
# Se inicia la ventana principal

if __name__ == '__main__': # Función principal

    app = Reservas() # Se crea una instancia de la clase Reservas
    app.ventana.mainloop() # Se inicia la ventana principal