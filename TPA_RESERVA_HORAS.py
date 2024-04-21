import tkinter as tk
import json
from tkinter import messagebox

class Reservas():

    def __init__(self):

        self.ventana = tk.Tk() 
        self.ventana.geometry('800x600')
        self.ventana.title("Reservaciones LOS PEPE ICINF")
        self.ventana.configure(bg='#f0f0f0')  # Fondo gris claro
        self.estilo_principal = ("Helvetica", 24, "bold")
        self.estilo_entry = ("Arial", 10)
        self.estilo_boton = ("Arial", 10, "bold")
        self.color_principal = "#0066cc"
        self.color_boton = "#004080"
        self.color_fondo_boton = "#b3d9ff"
        self.color_texto_boton = "white"

        self.frame_principal = tk.Frame(self.ventana, bg='#f0f0f0')  # Marco principal
        self.frame_principal.pack(expand=True, padx=20, pady=20)

        self.titulo = tk.Label(self.frame_principal, text="Bienvenido a tu programa de reservas favorito", font=self.estilo_principal, fg=self.color_principal, bg='#f0f0f0')
        self.titulo.pack(pady=10)
        
        self.nombre_label = tk.Label(self.frame_principal, text="Usuario:", font=self.estilo_entry, bg='#f0f0f0')
        self.nombre_label.pack()
        self.usuario_entry = tk.Entry(self.frame_principal, font=self.estilo_entry, highlightthickness=2)  # Resaltar borde de la entrada
        self.usuario_entry.pack(pady=5)

        self.recinto_select = tk.StringVar()
        self.recinto_select.set("Seleccione una opción")
        self.recinto_select.trace("w", lambda *args: self.cargar_horas())
        self.recinto_label = tk.Label(self.frame_principal, text="Recinto:", font=self.estilo_entry, bg='#f0f0f0')
        self.recinto_label.pack()
        self.recinto_select_menu = tk.OptionMenu(self.frame_principal, self.recinto_select, "Seleccione una opción", "Cancha de Fútbol", "Cancha de Tenis", "Cancha de Pádel")
        self.recinto_select_menu.config(font=self.estilo_entry, highlightthickness=2)  # Resaltar borde del menú de opción
        self.recinto_select_menu.pack(pady=5)
        
        self.hora_label = tk.Label(self.frame_principal, text="Hora:", font=self.estilo_entry, bg='#f0f0f0')  
        self.hora_label.pack()
        
        self.hora_select = tk.StringVar()
        self.hora_select.set("Seleccione hora")
        self.hora_select_menu = tk.OptionMenu(self.frame_principal, self.hora_select, "Seleccione hora")
        self.hora_select_menu.config(font=self.estilo_entry, highlightthickness=2)  # Resaltar borde del menú de opción
        self.hora_select_menu.pack(pady=5)
        
        self.reservar_boton = tk.Button(self.frame_principal, text="Reservar", command=self.reservar, font=self.estilo_boton, bg=self.color_boton, fg=self.color_texto_boton, padx=10, pady=5, bd=0)  # Sin borde
        self.reservar_boton.pack(pady=10)

        self.cancelar_boton = tk.Button(self.frame_principal, text="Cancelar", command=self.cancelar, font=self.estilo_boton, bg=self.color_boton, fg=self.color_texto_boton, padx=10, pady=5, bd=0)  # Sin borde
        self.cancelar_boton.pack(pady=5)

        self.reservas_guardadas = []  
        self.horarios_reservados = set()

        self.abrir_reserva_boton = tk.Button(self.frame_principal, text="Ver reservas", command=self.abrir_reserva, font=self.estilo_boton, bg=self.color_boton, fg=self.color_texto_boton, padx=10, pady=5, bd=0)
        self.abrir_reserva_boton.pack(pady=10)

    def reservar(self):
        nombre = self.usuario_entry.get()
        recinto = self.recinto_select.get()
        hora = self.hora_select.get()
        
        if nombre == "" or recinto == "Seleccione una opción" or hora == "Seleccione hora":
            messagebox.showerror("Error", "Debe completar todos los campos")
        elif any(reserva["recinto"] == recinto and reserva["hora"] == hora for reserva in self.reservas_guardadas):
            messagebox.showerror("Error", "Este horario ya ha sido reservado para este recinto")
        else:
            reserva = {"nombre": nombre, "recinto": recinto, "hora": hora}
            self.reservas_guardadas.append(reserva)
            self.horarios_reservados.add((recinto, hora))  # Usamos una tupla para guardar recinto y hora juntos
            messagebox.showinfo("Reserva realizada", f"Reserva realizada con éxito\nNombre: {nombre}\nRecinto: {recinto}\nHora: {hora}")
            self.guardar_reservas()
            self.cancelar()

    def cargar_horas(self):
        recinto = self.recinto_select.get()
        horas = []
        if recinto == "Cancha de Fútbol":
            horas = ["Seleccione hora", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
        elif recinto == "Cancha de Tenis":
            horas = ["Seleccione hora", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
        elif recinto == "Cancha de Pádel":
            horas = ["Seleccione hora", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
        self.hora_select.set(horas[0])
        self.hora_select_menu['menu'].delete(0, 'end')
        for hora in horas:
            self.hora_select_menu['menu'].add_command(label=hora, command=tk._setit(self.hora_select, hora))

    def cancelar(self):
        self.usuario_entry.delete(0, tk.END)
        self.recinto_select.set("Seleccione recinto")
        self.hora_select.set("Seleccione hora")

    def guardar_reservas(self):
        with open("reservas.json", "w") as fecha1:
            json.dump(self.reservas_guardadas, fecha1)

    def abrir_reserva(self):
        app2 = VisualizarReservas()
        app2.ventana.mainloop()

class VisualizarReservas():

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.geometry('800x600')
        self.ventana.title("Reservaciones LOS PEPE ICINF")
        self.ventana.configure(bg='#f0f0f0')

        self.estilo_principal = ("Helvetica", 24, "bold")
        self.estilo_entry = ("Arial", 10)
        self.estilo_boton = ("Arial", 10, "bold")
        self.color_principal = "#0066cc"
        self.color_boton = "#004080"
        self.color_fondo_boton = "#b3d9ff"
        self.color_texto_boton = "white"

        self.frame_principal = tk.Frame(self.ventana, bg='#f0f0f0')
        self.frame_principal.pack(expand=True, padx=20, pady=20)

        self.titulo = tk.Label(self.frame_principal, text="Visualizar reservas", font=self.estilo_principal, fg=self.color_principal, bg='#f0f0f0')
        self.titulo.pack(pady=10)

        self.reservas_label = tk.Label(self.frame_principal, text="Reservas:", font=self.estilo_entry, bg='#f0f0f0')
        self.reservas_label.pack()

        self.reservas_text = tk.Text(self.frame_principal, font=self.estilo_entry, height=10, width=50)
        self.reservas_text.pack()

        self.borrar_reservas_boton = tk.Button(self.frame_principal, text="Borrar reservas", command=self.borrar_reservas, font=self.estilo_boton, bg=self.color_boton, fg=self.color_texto_boton, padx=10, pady=5, bd=0)  # Sin borde
        self.borrar_reservas_boton.pack(pady=5)

        self.cargar_reservas()

    def cargar_reservas(self):
        try:
            with open("reservas.json", "r") as fecha1:
                reservas = json.load(fecha1)
                for reserva in reservas:
                    self.reservas_text.insert(tk.END, f"Nombre: {reserva['nombre']}\nRecinto: {reserva['recinto']}\nHora: {reserva['hora']}\n\n")
        except FileNotFoundError:
            self.reservas_text.insert(tk.END, "No hay reservas guardadas")

    def borrar_reservas(self):
        with open("reservas.json", "w") as fecha1:
            json.dump([], fecha1)
        self.reservas_text.delete(1.0, tk.END)
        self.reservas_text.insert(tk.END, "Se han eliminado todas las reservas")

if __name__ == '__main__':
    app = Reservas()
    app.ventana.mainloop()