import tkinter as tk
import json
from tkinter import messagebox



class Reservas():

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



    def reservar(self):

        nombre = str(self.usuario_entry.get())
        recinto = self.recinto_select.get()
        hora = self.hora_select.get()
        nombre.lower()

        # chequear si no existe otro usuario con el mismo nombre

        while True:

            if not nombre:

                messagebox.showerror("Error", "Debe ingresar un nombre de usuario")
                break

            elif not nombre.isalpha() and nombre.isspace() or nombre.isnumeric():

                messagebox.showerror("Error", "El nombre de usuario solo puede contener letras")
                break
            
            elif not recinto:

                messagebox.showerror("Error", "Debe seleccionar un recinto")
                break

            elif not hora:

                messagebox.showerror("Error", "Debe seleccionar una hora")
                break

            elif any(reserva["nombre"] == nombre for reserva in self.reservas_guardadas):
            
                messagebox.showerror("Error", "Solo puedes reservar 1 hora por día en alguna de nuestros establecimientos")
                break

            elif any(reserva["recinto"] == recinto and reserva["hora"] == hora for reserva in self.reservas_guardadas):
            
                messagebox.showerror("Error", "Este horario ya ha sido reservado para este recinto")
                break

            else:

                reserva = {"nombre": nombre, "recinto": recinto, "hora": hora}
                self.reservas_guardadas.append(reserva)
                self.horarios_reservados.add((recinto, hora))
                messagebox.showinfo("Reserva realizada", f"Reserva realizada con éxito\nNombre: {nombre}\nRecinto: {recinto}\nHora: {hora}")
                self.guardar_reservas()
                self.cancelar()
                break



    def cargar_horas(self):

        recinto = self.recinto_select.get()
        horas = []

        if recinto in ["Cancha de Fútbol", "Cancha de Tenis", "Cancha de Pádel"]:

            horas = ["Seleccione hora", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]

        self.hora_select.set(horas[0])
        self.hora_select_menu['menu'].delete(0, 'end')

        for hora in horas:

            self.hora_select_menu['menu'].add_command(label=hora, command=tk._setit(self.hora_select, hora))



    def cancelar(self):

        self.usuario_entry.delete(0, tk.END)
        self.recinto_select.set("Seleccione una opción")
        self.hora_select.set("Seleccione hora")



    def guardar_reservas(self):

        with open("reservas.json", "w") as fecha1:

            json.dump(self.reservas_guardadas, fecha1)



    def listar_reservas(self):

        self.reservas_text.config(state=tk.NORMAL)
        self.reservas_text.delete(1.0, tk.END)

        for reserva in self.reservas_guardadas:

            self.reservas_text.insert(tk.END, f"Nombre: {reserva['nombre']}\nRecinto: {reserva['recinto']}\nHora: {reserva['hora']}\n\n")
        
        self.reservas_text.config(state=tk.DISABLED)



    def abrir_reserva(self):
        
        self.ventana.destroy()
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
        
        self.cargar_reservas()
        self.esta_vacia()



    def esta_vacia(self):

        if not self.reservas:

            messagebox.showinfo("Información", "No hay reservas guardadas")
            self.ventana.destroy()
            app = Reservas()
            app.ventana.mainloop()

        else:

            self.cargar_reservas()



    def cargar_reservas(self):
        
        self.reservas_text.delete(1.0, tk.END)

        with open("reservas.json", "r") as fecha1:

            self.reservas = json.load(fecha1)
            
            for reserva in self.reservas:
            
                self.reservas_text.insert(tk.END, f"Nombre: {reserva['nombre']}\nRecinto: {reserva['recinto']}\nHora: {reserva['hora']}\n\n")
            
            self.reservas_text.config(state=tk.DISABLED)



    def buscar_reserva(self):

        nombre_buscar = self.buscar_entry.get()
        self.reservas_text.config(state=tk.NORMAL)
        self.reservas_text.delete(1.0, tk.END)
        encontradas = []
        
        with open("reservas.json", "r") as fecha1:

            self.reservas = json.load(fecha1)

            for reserva in self.reservas:

                if nombre_buscar.lower() in reserva['nombre'].lower():

                    encontradas.append(reserva)
                    self.reservas_text.insert(tk.END, f"Nombre: {reserva['nombre']}\nRecinto: {reserva['recinto']}\nHora: {reserva['hora']}\n\n")

        self.reservas_text.config(state=tk.DISABLED)

        if not encontradas:

            messagebox.showinfo("Información", "No se encontraron reservas con ese nombre.")



    def eliminar_reserva(self):
        
        nombre_buscar = self.buscar_entry.get()
        if not nombre_buscar:
        
            messagebox.showinfo("Información", "Debe ingresar un usuario para poder eliminar una reserva")
            return
        
        else:
            
            self.reservas = json.load(open("reservas.json"))

        for reserva in self.reservas:

            if nombre_buscar.lower() in reserva['nombre'].lower():

                self.reservas.remove(reserva)
                self.reservas_text.config(state=tk.NORMAL)
                self.reservas_text.delete(1.0, tk.END)
                
                for reserva in self.reservas:
                    
                    self.reservas_text.insert(tk.END, f"Nombre: {reserva['nombre']}\nRecinto: {reserva['recinto']}\nHora: {reserva['hora']}\n\n")
                
                self.reservas_text.config(state=tk.DISABLED)
                self.guardar_reservas()
                messagebox.showinfo("Información", "Reserva eliminada.")
                
                if not self.reservas:
                    messagebox.showinfo("Información", "Se han eliminado todas las reservas.")
                    self.ventana.destroy()
                    app = Reservas()
                    app.ventana.mainloop()
                return
        messagebox.showinfo("Información", "No existe una reserva con ese nombre")



    def guardar_reservas(self):
        with open("reservas.json", "w") as fecha1:
            json.dump(self.reservas, fecha1)



if __name__ == '__main__':
    app = Reservas()
    app.ventana.mainloop()