import tkinter as tk # Importamos la libreria principal para crear la interfaz grafica
from tkinter import messagebox # Importamos messagebox para poder mostrar ventanas emergentes (alertas, errores, etc)

# ==========================================
# CLASES DE ESTRUCTURA DE DATOS
# ==========================================

class Nodo:
    """
    Clase Nodo:
    Representa un unico elemento (o circulo) dentro del Arbol Binario.
    Cada nodo guarda un valor (numero entero) y tiene dos 'brazos' (punteros)
    que pueden apuntar a otros nodos (hijo izquierdo e hijo derecho).
    """
    def __init__(self, valor):
        self.valor = valor # El numero que guarda este nodo
        self.izq = None    # Puntero al hijo izquierdo (menores)
        self.der = None    # Puntero al hijo derecho (mayores)

class ArbolBinario:
    """
    Clase ArbolBinario:
    Se encarga de administrar todos los Nodos. Contiene la logica para
    insertar, buscar y recorrer los elementos respetando las reglas de
    un Arbol Binario de Busqueda (los menores a la izquierda, mayores a la derecha).
    """
    def __init__(self):
        self.raiz = None # Al inicio, el arbol esta vacio (sin raiz)

    def insertar(self, valor):
        """
        Metodo principal para agregar un nuevo valor al arbol.
        Si el arbol esta vacio, el nuevo valor se convierte en la raiz.
        Si ya hay raiz, llama a una funcion recursiva para buscar su lugar.
        """
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            # Empezamos a buscar donde insertarlo desde la raiz (que es el nivel 1)
            self._insertar_recursivo(valor, self.raiz, 1)

    def _insertar_recursivo(self, valor, nodo_actual, nivel):
        """
        Metodo recursivo (se llama a si mismo) para encontrar la posicion
        correcta de un nuevo valor. Ademas, controla que no pasemos de 4 niveles.
        """
        # Si el valor es menor que el nodo actual, debemos ir a la izquierda
        if valor < nodo_actual.valor:
            # Si a la izquierda no hay nada, insertamos el nuevo nodo aqui
            if nodo_actual.izq is None:
                if nivel < 4: # Verificamos que no excedamos la profundidad de 4
                    nodo_actual.izq = Nodo(valor)
                else:
                    # Si ya estamos en nivel 4, no podemos bajar mas
                    raise Exception("No se pueden agregar mas niveles. Maximo 4 niveles permitidos.")
            else:
                # Si ya hay un nodo a la izquierda, bajamos de nivel y repetimos el proceso
                self._insertar_recursivo(valor, nodo_actual.izq, nivel + 1)
                
        # Si el valor es mayor que el nodo actual, debemos ir a la derecha
        elif valor > nodo_actual.valor:
            # Si a la derecha no hay nada, insertamos el nuevo nodo aqui
            if nodo_actual.der is None:
                if nivel < 4: # Verificamos limite de profundidad
                    nodo_actual.der = Nodo(valor)
                else:
                    raise Exception("No se pueden agregar mas niveles. Maximo 4 niveles permitidos.")
            else:
                # Si ya hay un nodo a la derecha, bajamos de nivel y repetimos
                self._insertar_recursivo(valor, nodo_actual.der, nivel + 1)
                
        # IMPORTANTE: Si el valor es IGUAL (valor == nodo_actual.valor),
        # no hacemos absolutamente nada, ya que en un ABB puro no se admiten duplicados.

    def buscar(self, valor):
        """
        Metodo principal para buscar un valor.
        Devuelve True si lo encuentra, False si no existe.
        """
        return self._buscar_recursivo(valor, self.raiz)

    def _buscar_recursivo(self, valor, nodo_actual):
        """
        Metodo recursivo para buscar. Navega por las ramas igual que como inserta.
        """
        if nodo_actual is None:
            return False # Llegamos a un punto vacio y no lo encontramos
        if nodo_actual.valor == valor:
            return True  # Lo encontramos!
        if valor < nodo_actual.valor:
            return self._buscar_recursivo(valor, nodo_actual.izq) # Buscamos por la izquierda
        return self._buscar_recursivo(valor, nodo_actual.der)     # Buscamos por la derecha

    def limpiar(self):
        """
        Vacia todo el arbol. Al borrar la raiz, Python se encarga de 
        eliminar automaticamente de la memoria el resto de los nodos (Garbage Collection).
        """
        self.raiz = None

    # --- METODOS DE RECORRIDO ---
    # Todos reciben una lista vacia ('resultado') donde van agregando los valores en texto.

    def preorden(self, nodo, resultado):
        """Recorrido Preorden: Raiz -> Izquierda -> Derecha"""
        if nodo:
            resultado.append(str(nodo.valor)) # Primero la Raiz
            self.preorden(nodo.izq, resultado) # Luego todo lo izquierdo
            self.preorden(nodo.der, resultado) # Finalmente todo lo derecho

    def inorden(self, nodo, resultado):
        """Recorrido Inorden: Izquierda -> Raiz -> Derecha (Los ordena de menor a mayor)"""
        if nodo:
            self.inorden(nodo.izq, resultado)  # Primero todo lo izquierdo
            resultado.append(str(nodo.valor))  # Luego la Raiz
            self.inorden(nodo.der, resultado)  # Finalmente todo lo derecho

    def postorden(self, nodo, resultado):
        """Recorrido Postorden: Izquierda -> Derecha -> Raiz"""
        if nodo:
            self.postorden(nodo.izq, resultado) # Primero todo lo izquierdo
            self.postorden(nodo.der, resultado) # Luego todo lo derecho
            resultado.append(str(nodo.valor))   # Finalmente la Raiz


# ==========================================
# FUNCIONES DE RENDERIZADO GRAFICO (CANVAS)
# ==========================================

def dibujar_lineas(canvas, nodo, x, y, dx):
    """
    Fase 1 del dibujo: Dibuja UNICAMENTE las lineas conectoras.
    Se hace por separado para que las lineas queden en el 'fondo' (z-index mas bajo).
    - x, y: Coordenadas actuales del nodo padre.
    - dx: Cuanto espacio horizontal moverse para los hijos (se va dividiendo entre 2).
    """
    if nodo is not None:
        if nodo.izq:
            # Dibuja linea desde las coordenadas del padre hasta las del hijo izquierdo
            canvas.create_line(x, y, x - dx, y + 80, width=2, fill="black")
            # Llama recursivamente para dibujar las lineas de los "nietos" izquierdos
            dibujar_lineas(canvas, nodo.izq, x - dx, y + 80, dx / 2)
        if nodo.der:
            # Dibuja linea desde las coordenadas del padre hasta las del hijo derecho
            canvas.create_line(x, y, x + dx, y + 80, width=2, fill="black")
            dibujar_lineas(canvas, nodo.der, x + dx, y + 80, dx / 2)

def dibujar_nodos(canvas, nodo, x, y, dx):
    """
    Fase 2 del dibujo: Dibuja los circulos de los nodos y el numero adentro.
    Como se dibuja DESPUES de las lineas, el circulo tapara el inicio/fin de la linea,
    logrando un aspecto visual limpio (la linea parece salir del borde y no del centro).
    """
    if nodo is not None:
        radio = 20 # Tamano del circulo
        
        # Primero mandamos a dibujar los hijos (recursividad)
        if nodo.izq:
            dibujar_nodos(canvas, nodo.izq, x - dx, y + 80, dx / 2)
        if nodo.der:
            dibujar_nodos(canvas, nodo.der, x + dx, y + 80, dx / 2)
        
        # Luego dibujamos el circulo del nodo ACTUAL (las coordenadas delimitan el ovalo)
        canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill="lightblue", outline="black")
        
        # Por ultimo escribimos el numero ('valor') justo en el centro del circulo
        canvas.create_text(x, y, text=str(nodo.valor), font=("Helvetica", 12, "bold"))


# ==========================================
# VENTANA PRINCIPAL DE LA APLICACION
# ==========================================

def abrir_arbol_binario():
    """
    Esta es la funcion gigante que construye toda la interfaz principal
    una vez que el usuario ingresa la contrasena correcta.
    """
    # Creamos la ventana principal
    arbol_binario_ventana = tk.Tk()
    arbol_binario_ventana.title("Arbol Binario")
    arbol_binario_ventana.geometry("1300x650") # Ancho x Alto
    arbol_binario_ventana.resizable(False, False) # Evitar que el usuario la cambie de tamano

    # Creamos la memoria del arbol (una instancia de nuestra clase)
    arbol = ArbolBinario()

    # --- Frame Superior (Controles) ---
    # Un "Frame" es como una caja imaginaria para agrupar elementos (widgets)
    frame_controles = tk.Frame(arbol_binario_ventana)
    frame_controles.pack(pady=10, fill='x') # Lo empaquetamos arriba con algo de margen (pady)

    # Etiqueta y Caja de texto para que el usuario escriba
    tk.Label(frame_controles, text="Nodo (Entero):", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
    entry_nodo = tk.Entry(frame_controles, font=("Helvetica", 12), width=10)
    entry_nodo.pack(side=tk.LEFT, padx=5)

    # Funcion interna para actualizar toda la grafica cuando hay cambios
    def actualizar_graficos():
        # Borra TODO lo que haya en el lienzo
        canvas_arbol.delete("all")
        
        # Si hay algo en el arbol (si la raiz no es None)
        if arbol.raiz:
            # Comenzamos a dibujar desde el centro superior de la pantalla (x=650, y=50)
            # El dx=300 significa que los primeros hijos se separaran 300 pixeles del centro
            dibujar_lineas(canvas_arbol, arbol.raiz, 650, 50, 300)
            dibujar_nodos(canvas_arbol, arbol.raiz, 650, 50, 300)
            
        # ==========================================
        # Actualizacion de los textos de recorridos
        # ==========================================
        # 1. Preorden
        res_pre = []
        arbol.preorden(arbol.raiz, res_pre)
        # Unimos la lista con guiones y actualizamos la etiqueta
        label_preorden.config(text="Preorden: " + " - ".join(res_pre))

        # 2. Inorden
        res_in = []
        arbol.inorden(arbol.raiz, res_in)
        label_inorden.config(text="Inorden: " + " - ".join(res_in))

        # 3. Postorden
        res_pos = []
        arbol.postorden(arbol.raiz, res_pos)
        label_postorden.config(text="Postorden: " + " - ".join(res_pos))

    # --- Funciones atadas a los botones ---
    
    def agregar_nodo():
        """Funcion para el boton 'Agregar Nodo'"""
        try:
            # Intenta convertir el texto a entero. Si el usuario puso letras, va al 'except ValueError'
            valor = int(entry_nodo.get())
            try:
                # Intenta insertarlo. Si choca con el limite de 4 niveles, va al 'except Exception'
                arbol.insertar(valor)
                actualizar_graficos() # Redibujamos todo
                entry_nodo.delete(0, tk.END) # Limpiamos la caja de texto
            except Exception as e:
                # Muestra una ventana de advertencia con el error de los niveles
                messagebox.showwarning("Limite Alcanzado", str(e))
        except ValueError:
            # Muestra error si no ingreso un numero
            messagebox.showerror("Error", "Por favor, ingrese un valor entero valido.")

    def buscar_nodo():
        """Funcion para el boton 'Buscar Nodo'"""
        try:
            valor = int(entry_nodo.get())
            encontrado = arbol.buscar(valor) # Busca en nuestra clase
            if encontrado:
                messagebox.showinfo("Resultado", f"El nodo {valor} se encuentra en el arbol.")
            else:
                messagebox.showinfo("Resultado", f"El nodo {valor} NO se encuentra en el arbol.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un valor entero valido.")

    def limpiar_arbol():
        """Funcion para el boton 'Limpiar'"""
        arbol.limpiar() # Vacia la memoria del arbol
        actualizar_graficos() # Redibuja (lo cual dejara el lienzo y recorridos en blanco)

    # --- Creacion de los Botones ---
    tk.Button(frame_controles, text="Agregar Nodo", command=agregar_nodo, font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_controles, text="Buscar Nodo", command=buscar_nodo, font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_controles, text="Limpiar", command=limpiar_arbol, font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
    
    # El boton salir lo empaquetamos a la derecha
    tk.Button(frame_controles, text="Salir", command=arbol_binario_ventana.destroy, font=("Helvetica", 12)).pack(side=tk.RIGHT, padx=20)

    # ==========================================
    # Canvas (Lienzo para dibujar)
    # ==========================================
    # Este es el espacio blanco grande donde cobra vida nuestro codigo de dibujo
    canvas_arbol = tk.Canvas(arbol_binario_ventana, width=1280, height=450, bg="white", relief=tk.SUNKEN, bd=2)
    canvas_arbol.pack(pady=10)

    # ==========================================
    # Paneles Inferiores (Recorridos)
    # ==========================================
    # Otro Frame contenedor
    frame_recorridos = tk.Frame(arbol_binario_ventana)
    frame_recorridos.pack(fill='x', padx=20, pady=10)

    # Panel Preorden (LabelFrame agrega un borde y un titulo bonito)
    panel_preorden = tk.LabelFrame(frame_recorridos, text="Recorrido Preorden", font=("Helvetica", 10, "bold"), fg="cyan")
    panel_preorden.pack(side=tk.LEFT, fill='both', expand=True, padx=5)
    # Dentro de ese panel, va el Label con el texto en si
    label_preorden = tk.Label(panel_preorden, text="Preorden: ", font=("Helvetica", 11), wraplength=400, justify=tk.LEFT)
    label_preorden.pack(pady=10, padx=10, anchor="w")

    # Panel Inorden
    panel_inorden = tk.LabelFrame(frame_recorridos, text="Recorrido Inorden", font=("Helvetica", 10, "bold"), fg="green")
    panel_inorden.pack(side=tk.LEFT, fill='both', expand=True, padx=5)
    label_inorden = tk.Label(panel_inorden, text="Inorden: ", font=("Helvetica", 11), wraplength=400, justify=tk.LEFT)
    label_inorden.pack(pady=10, padx=10, anchor="w")

    # Panel Postorden
    panel_postorden = tk.LabelFrame(frame_recorridos, text="Recorrido Postorden", font=("Helvetica", 10, "bold"), fg="red")
    panel_postorden.pack(side=tk.LEFT, fill='both', expand=True, padx=5)
    label_postorden = tk.Label(panel_postorden, text="Postorden: ", font=("Helvetica", 11), wraplength=400, justify=tk.LEFT)
    label_postorden.pack(pady=10, padx=10, anchor="w")


# ==========================================
# VENTANA DE INICIO (LOGIN)
# ==========================================
# El programa empieza leyendo desde aqui hacia abajo (despues de leer las clases)

def verificar_contrasena(event=None):
    """
    Verifica si la contrasena ingresada en el campo de texto es correcta ("ARBOL").
    El parametro 'event' nos permite capturar cuando el usuario presiona la tecla Enter.
    """
    # Extraemos el numero final del texto "Intentos restantes: 3"
    intentos_restantes = int(label_intentos.cget("text").split()[-1])
    
    if entry_contrasena.get() == "ARBOL":
        # Contrasena correcta: Mostramos bienvenida, cerramos login y abrimos aplicacion principal
        messagebox.showinfo("Acceso Concedido", "Contrasena correcta. Bienvenido.", parent=ventana)
        ventana.destroy() # Destruye la ventanita
        abrir_arbol_binario() # Llama a la funcion gigante de arriba
    else:
        # Contrasena incorrecta: Restamos un intento
        intentos_restantes -= 1
        if intentos_restantes > 0:
            # Si le quedan intentos, le advertimos y borramos la cajita de texto
            messagebox.showwarning("Acceso Denegado", f"Contrasena incorrecta. Le quedan {intentos_restantes} intentos.", parent=ventana)
            label_intentos.config(text=f"Intentos restantes: {intentos_restantes}")
            entry_contrasena.delete(0, tk.END) 
        else:
            # Si se le acabaron, mostramos error fatal y matamos el programa
            messagebox.showerror("Acceso Bloqueado", "Ha superado el numero de intentos permitidos.", parent=ventana)
            ventana.destroy() 

# Creamos la ventana de inicio
ventana = tk.Tk()
ventana.title("Fase 4 - Juan Garcia")
ventana.geometry("500x250")
ventana.resizable(False, False)

# Agregamos los textos informativos
tk.Label(ventana, text="Aplicacion Arboles Binarios").pack(pady=5)
tk.Label(ventana, text="Estudiante: Juan Garcia").pack(pady=3)
tk.Label(ventana, text="Fecha: 10/05/2026").pack(pady=3)
tk.Label(ventana, text="Ingrese la contrasena de acceso:").pack(pady=3)

# Campo de entrada (Entry) configurado con show="-" para enmascarar los caracteres
entry_contrasena = tk.Entry(ventana, show="-", font=("Helvetica", 12), width=25)
entry_contrasena.pack(pady=5)
# Vinculamos la tecla especial Return (Enter) para que ejecute verificar_contrasena
entry_contrasena.bind('<Return>', verificar_contrasena)

# Etiqueta dinamica para llevar la cuenta de intentos
label_intentos = tk.Label(ventana, text="Intentos restantes: 3")
label_intentos.pack(pady=5)

# Frame para agrupar los botones de la pantalla de login
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=15)

# Botones de Login. Usamos grid para que queden lado a lado (column 0 y column 1)
tk.Button(frame_botones, text="Ingresar", command=verificar_contrasena, font=("Helvetica", 12)).grid(row=0, column=0, padx=10)
tk.Button(frame_botones, text="Salir", command=ventana.destroy, font=("Helvetica", 12)).grid(row=0, column=1, padx=10)

# El 'mainloop' es el motor de Tkinter. Se queda corriendo en bucle infinito
# esperando a que el usuario haga clics o presione teclas.
ventana.mainloop()

"""
Explicacion del Codigo:

Este programa es una aplicacion grafica construida con Tkinter que permite visualizar un Arbol Binario de Busqueda (ABB) con un maximo de 4 niveles.

El codigo se divide en las siguientes partes principales:

1. Clases Estructurales:
   - Nodo: Representa cada elemento del arbol, guardando un valor numerico y referencias a sus hijos izquierdo y derecho.
   - ArbolBinario: Contiene la logica estructural del arbol. Incluye metodos para insertar nuevos valores respetando el limite de 4 niveles y evitando duplicados, buscar si un valor especifico existe, limpiar todo el arbol, y generar los tres recorridos principales (Preorden, Inorden y Postorden) mediante algoritmos recursivos.

2. Funciones Graficas:
   - dibujar_lineas y dibujar_nodos: Se encargan de renderizar el arbol en el lienzo (Canvas). Se dividio en dos funciones para asegurar que las lineas que unen los nodos queden siempre detras de los circulos, mejorando la visualizacion. El color de la linea es negro para asegurar su visibilidad.

3. Interfaz de Usuario (UI):
   - Ventana de Inicio (Login): Solicita una contrasena ('ARBOL') para poder acceder a la aplicacion principal, permitiendo un maximo de 3 intentos.
   - Ventana Principal (abrir_arbol_binario): Contiene un campo de texto para ingresar los valores, botones para ejecutar las acciones (Agregar, Buscar, Limpiar, Salir), un lienzo central grande para dibujar el arbol y tres paneles inferiores que muestran en tiempo real como van quedando los recorridos a medida que se agregan nodos.
"""