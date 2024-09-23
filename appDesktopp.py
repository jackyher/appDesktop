import tkinter as tk
from tkinter import messagebox
import requests
import socket
from datetime import datetime

# URL de MockAPI
API_URL = "https://66eb023555ad32cda47b5150.mockapi.io/IoTCarStatus"

# Función para obtener la IP del cliente
def get_client_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

# Función para actualizar los valores generados automáticamente (fecha, IP y status)
def actualizar_valores():
    ip_label.config(text=f"IP Cliente: {get_client_ip()}")
    date_label.config(text=f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    status_label.config(text=f"Status: {status_var.get()}")

# Función para insertar registros
def insertar_registro():
    # Obtener valores de la entrada
    name = name_entry.get()
    ip_client = get_client_ip()
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = status_var.get()

    if not name:
        messagebox.showwarning("Error", "El nombre no puede estar vacío")
        return

    # Datos que se enviarán
    data = {
        "status": status,
        "date": date_now,
        "ipClient": ip_client,
        "name": name
    }

    # Envío de datos a MockAPI
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 201:
            messagebox.showinfo("Éxito", "Registro insertado correctamente")
            name_entry.delete(0, tk.END)  # Limpiar el campo de nombre
        else:
            messagebox.showerror("Error", f"No se pudo insertar el registro. Código: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error: {str(e)}")

    # Actualizar los valores después de insertar
    actualizar_valores()

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Inyección de Registros - MockAPI")

# Status por defecto (puedes cambiarlo si lo prefieres)
status_var = tk.StringVar(value="active")

# Etiquetas y campos de entrada
name_label = tk.Label(root, text="Nombre")
name_label.pack(pady=5)

name_entry = tk.Entry(root)
name_entry.pack(pady=5)

# Etiquetas para mostrar los datos automáticos
ip_label = tk.Label(root, text=f"IP Cliente: {get_client_ip()}")
ip_label.pack(pady=5)

date_label = tk.Label(root, text=f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
date_label.pack(pady=5)

status_label = tk.Label(root, text=f"Status: {status_var.get()}")
status_label.pack(pady=5)

# Botón para insertar registro
insert_button = tk.Button(root, text="Insertar Registro", command=insertar_registro)
insert_button.pack(pady=20)

# Al iniciar, mostrar los valores actuales
actualizar_valores()

# Iniciar la aplicación
root.mainloop()
