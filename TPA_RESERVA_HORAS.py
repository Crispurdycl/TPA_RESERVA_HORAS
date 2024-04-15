import tkinter as tk
import json
from tkinter import messagebox

class Reservas():

    def __init__(self):
        self.ventana = tk.Tk() 
        self.ventana.geometry('800x600')
        self.ventana.title("Reserva de horas en centro deportivo")
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

        self.titulo = tk.Label(self.frame_principal, text="Reserva de horas en centro deportivo", font=self.estilo_principal, fg=self.color_principal, bg='#f0f0f0')
        self.titulo.pack(pady=10)
        
        self.nombre_label = tk.Label(self.frame_principal, text="Usuario:", font=self.estilo_entry, bg='#f0f0f0')
        self.nombre_label.pack()
        self.usuario_entry = tk.Entry(self.frame_principal, font=self.estilo_entry, highlightthickness=2)  # Resaltar borde de la entrada
        self.usuario_entry.pack(pady=5)

        self.recinto_select = tk.StringVar()
        self.recinto_select.set("Seleccione recinto")
        self.recinto_select.trace("w", lambda *args: self.cargar_horas())
        self.recinto_label = tk.Label(self.frame_principal, text="Recinto:", font=self.estilo_entry, bg='#f0f0f0')
        self.recinto_label.pack()
        self.recinto_select_menu = tk.OptionMenu(self.frame_principal, self.recinto_select, "Seleccione recinto", "Recinto 1", "Recinto 2", "Recinto 3")
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

    def reservar(self):
        nombre = self.usuario_entry.get()
        recinto = self.recinto_select.get()
        hora = self.hora_select.get()
        if nombre == "" or recinto == "Seleccione recinto" or hora == "Seleccione hora":
            messagebox.showerror("Error", "Debe completar todos los campos")
        elif hora in self.horarios_reservados:
            messagebox.showerror("Error", "Este horario ya ha sido reservado")
        else:
            reserva = {"nombre": nombre, "recinto": recinto, "hora": hora}
            self.reservas_guardadas.append(reserva)  
            self.horarios_reservados.add(hora)
            messagebox.showinfo("Reserva realizada", f"Reserva realizada con éxito\nNombre: {nombre}\nRecinto: {recinto}\nHora: {hora}")
            self.guardar_reservas()  
            self.cancelar()

    def cargar_horas(self):
        recinto = self.recinto_select.get()
        horas = []
        if recinto == "Recinto 1":
            horas = ["Seleccione hora", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00"]
        elif recinto == "Recinto 2":
            horas = ["Seleccione hora", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"]
        elif recinto == "Recinto 3":
            horas = ["Seleccione hora", "20:00", "21:00", "22:00", "23:00"]
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

if __name__ == '__main__':
    app = Reservas()
    app.ventana.mainloop()