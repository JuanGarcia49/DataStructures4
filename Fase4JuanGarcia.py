import tkinter as tk

from tkinter import messagebox

def abrir_arbol_binario():
    arbol_binario = tk.Tk()
    arbol_binario.title("Arbol Binario")
    arbol_binario.geometry("1300x650")
    arbol_binario.resizable(False, False)

def verificar_contrasena(event=None):
    """
    Verifica si la contraseña ingresada en el campo de texto es correcta.
    El parametro 'event' es para permitir la vinculacion con eventos de teclado.
    """
    intentos_restantes = int(label_intentos.cget("text").split()[-1])
    
    if entry_contrasena.get() == "ARBOL":
        messagebox.showinfo("Acceso Concedido", "Contraseña correcta. Bienvenido.", parent=ventana)
        ventana.destroy() # Cierra la ventana de login
        abrir_arbol_binario()
    else:
        intentos_restantes -= 1
        if intentos_restantes > 0:
            messagebox.showwarning("Acceso Denegado", f"Contraseña incorrecta. Le quedan {intentos_restantes} intentos.", parent=ventana)
            label_intentos.config(text=f"Intentos restantes: {intentos_restantes}")
            entry_contrasena.delete(0, tk.END) # Limpia el campo de contraseña
        else:
            messagebox.showerror("Acceso Bloqueado", "Ha superado el número de intentos permitidos.", parent=ventana)
            ventana.destroy() # Cierra la aplicación


ventana = tk.Tk()
ventana.title("Fase 4 — Juan Garcia")
ventana.geometry("500x250")
ventana.resizable(False, False)

# --- Creación de Widgets ---
tk.Label(ventana, text="Aplicacion Arboles Binarios").pack(pady=10)
tk.Label(ventana, text="Estudiante: Juan Garcia").pack(pady=10)
tk.Label(ventana, text="Fecha: 10/05/2026").pack(pady=10)
tk.Label(ventana, text="Ingrese la contraseña de acceso:").pack(pady=10)

# Este es el campo de entrada para la contraseña. La opción show="*" oculta el texto.
entry_contrasena = tk.Entry(ventana, show="-", font=("Helvetica", 12), width=25)
entry_contrasena.pack(pady=5)
# Vinculamos la tecla "Enter" (Return) al campo de contraseña para llamar a la función de verificación.
entry_contrasena.bind('<Return>', verificar_contrasena)

label_intentos = tk.Label(ventana, text="Intentos restantes: 3")
label_intentos.pack(pady=5)

# --- Contenedor para los botones ---
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=15)

tk.Button(frame_botones, text="Ingresar", command=verificar_contrasena, font=("Helvetica", 12)).grid(row=0, column=0, padx=10) # Columna 0
tk.Button(frame_botones, text="Salir", command=ventana.destroy, font=("Helvetica", 12)).grid(row=0, column=1, padx=10) # Columna 1

# Iniciar el bucle de eventos para que la ventana aparezca y sea interactiva
ventana.mainloop()