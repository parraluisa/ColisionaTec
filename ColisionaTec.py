import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#TODO: Revisar la animación de colisiones tanto elasticas como inelasticas, especialmente en el choque
#TODO: Revisar que las colisiones perfectamente inelasticas se comporten correctamente (Solo vamos a aplicar totalmente inelasticas)
#TODO: Para la animación agrandar o disminuir el tamaño de las masas dependiendo de su masa (masa1 y masa2)
#TODO: Mostrar las ecuaciones de energías y momentos
#TODO: Mostrar las energías y momentos iniciales y finales
#TODO: Mejorar el flujo de la aplicación para asegurarse de que el botón de cerrar aplicación funcione en todos los casos

# Parámetros para la simulación
total_time = 5.0
dt = 0.01

# Variables globales para almacenar datos de la simulación
time_data = []
initial_momentum_data = []
final_momentum_data = []
initial_energy_data = []
final_energy_data = []
x1_data = []
x2_data = []
v1_data = []  
v2_data = []  

# Función de cálculo de colisiones
def calculate_collision(mass1, mass2, v1_initial, v2_initial, e):
    v1_final = (mass1 * v1_initial + mass2 * v2_initial + mass2 * e * (v2_initial - v1_initial)) / (mass1 + mass2)
    v2_final = (mass1 * v1_initial + mass2 * v2_initial + mass1 * e * (v1_initial - v2_initial)) / (mass1 + mass2)
    return v1_final, v2_final

# Función de inicialización para la animación
def init():
    object1.set_data([], [])
    object2.set_data([], [])
    time_text.set_text('')
    momentum_text.set_text('')
    energy_text.set_text('')
    return object1, object2, time_text, momentum_text, energy_text

# Función de actualización para la animación
def update(frame, mass1, mass2, v1_initial, v2_initial, v1_final, v2_final):
    global x1, x2
    t = frame * dt
    if t < 1:
        x1 = v1_initial * t
        x2 = 5 + v2_initial * t
        if x1 >= x2:
            v1_initial, v2_initial = v1_final, v2_final
    else:
        x1 += v1_initial * dt
        x2 += v2_initial * dt

    object1.set_data(x1, 0)
    object2.set_data(x2, 0)
    time_text.set_text('Tiempo = %.1f s' % t)

    # Calcular y actualizar impulso, momento y energía
    current_momentum = mass1 * v1_initial + mass2 * v2_initial
    current_energy = 0.5 * mass1 * v1_initial**2 + 0.5 * mass2 * v2_initial**2
    momentum_text.set_text(f'Momentum: {initial_momentum:.2f} -> {current_momentum:.2f}')
    energy_text.set_text(f'Energía: {initial_energy:.2f} -> {current_energy:.2f}')

    # Guardar datos para graficar
    time_data.append(t)
    initial_momentum_data.append(initial_momentum)
    final_momentum_data.append(current_momentum)
    initial_energy_data.append(initial_energy)
    final_energy_data.append(current_energy)
    x1_data.append(x1)
    x2_data.append(x2)

    # Calcular velocidades actuales
    v1_current = v1_initial
    v2_current = v2_initial
    if t >= 1:
        v1_current = v1_final
        v2_current = v2_final

    v1_data.append(v1_current)
    v2_data.append(v2_current)

    return object1, object2, time_text, momentum_text, energy_text

# Función para detener la animación
def stop_animation():
    ani.event_source.stop()

def continue_animation():
    ani.event_source.start()

def show_data():
    global time_data, initial_momentum_data, final_momentum_data, initial_energy_data, final_energy_data, x1_data, x2_data, v1_data, v2_data

    # Crear una nueva ventana para los datos
    data_window = tk.Toplevel(root)
    data_window.title("Datos de la simulación")
    data_window.geometry("800x600")

    # Crear un marco de desplazamiento
    scroll_frame = ttk.Frame(data_window)
    scroll_frame.pack(fill=tk.BOTH, expand=True)

    # Añadir un lienzo para los datos
    canvas = tk.Canvas(scroll_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Añadir una barra de desplazamiento
    scrollbar = ttk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Crear un marco interno para el contenido del lienzo
    data_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=data_frame, anchor="nw")

    # Crear una tabla para mostrar los datos
    data_table = ttk.Treeview(data_frame, columns=('time', 'momentum', 'energy', 'x1', 'x2', 'v1', 'v2'), show='headings', height=25)
    data_table.heading('time', text='Tiempo (s)')
    data_table.heading('momentum', text='Momentum')
    data_table.heading('energy', text='Energía')
    data_table.heading('x1', text='Posición Masa 1')
    data_table.heading('x2', text='Posición Masa 2')
    data_table.heading('v1', text='Velocidad Masa 1')
    data_table.heading('v2', text='Velocidad Masa 2')

    # Ajustar el ancho de las columnas
    data_table.column('time', width=100)
    data_table.column('momentum', width=100)
    data_table.column('energy', width=100)
    data_table.column('x1', width=100)
    data_table.column('x2', width=100)
    data_table.column('v1', width=100)
    data_table.column('v2', width=100)

    for i in range(len(time_data)):
        data_table.insert('', 'end', values=(time_data[i], initial_momentum_data[i], final_momentum_data[i], initial_energy_data[i], final_energy_data[i], x1_data[i], x2_data[i], v1_data[i], v2_data[i]))

    data_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Actualizar el lienzo con el tamaño del contenido
    data_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Configurar la barra de desplazamiento para que funcione correctamente
    data_window.update()
    canvas.config(scrollregion=canvas.bbox("all"))

# Función para cerrar la animación
def close_animation():
    #Esta función detiene la animación, borra los datos y cierra la ventana para volver a la pantalla principal
    stop_animation()
    clear_data()
    ani.event_source.stop()
    #eliminar la ventana de la animación
    anim_window.destroy()
    #volver a la pantalla principal
    root.deiconify()
    
    
#Fucnión para borrar los datos
def clear_data():
    time_data.clear()
    initial_momentum_data.clear()
    final_momentum_data.clear()
    initial_energy_data.clear()
    final_energy_data.clear()
    x1_data.clear()
    x2_data.clear()
    v1_data.clear()
    v2_data.clear()

# Función para iniciar la animación
def start_animation():

    #Borrar todo en caso de que haya algo
    clear_data()

    global initial_momentum, initial_energy, ani, fig, ax, canvas

    # Validar los valores de entrada
    mass1_value = mass1_entry.get()
    mass2_value = mass2_entry.get()
    v1_value = v1_entry.get()
    v2_value = v2_entry.get()

    if not mass1_value or not mass2_value or not v1_value or not v2_value:
        messagebox.showinfo("Alerta", "Debe ingresar todos los valores requeridos.")
        return

    try:
        mass1 = float(mass1_value)
        mass2 = float(mass2_value)
        v1_initial = float(v1_value)
        v2_initial = float(v2_value)
    except ValueError:
        messagebox.showinfo("Alerta", "Los valores de masa y velocidad deben ser números válidos.")
        return

    if mass1 <= 0 or mass2 <= 0:
        messagebox.showinfo("Alerta", "Las masas deben ser mayores a 0.")
        return
    if v1_initial == v2_initial and v1_initial == 0:
        messagebox.showinfo("Alerta", "Al menos una de las velocidades iniciales debe ser diferente de 0.")
        return

    e = 1.0 if elastic_var.get() else 0.5

    # Calcular las velocidades finales
    v1_final, v2_final = calculate_collision(mass1, mass2, v1_initial, v2_initial, e)

    # Conservación del impulso y energía inicial
    global initial_momentum, initial_energy
    initial_momentum = mass1 * v1_initial + mass2 * v2_initial
    initial_energy = 0.5 * mass1 * v1_initial**2 + 0.5 * mass2 * v2_initial**2

    # Crear ventana de animación
    global anim_window
    anim_window = tk.Toplevel(root)
    anim_window.title("Animación de colisión")
    anim_window.geometry("800x600")

    # Crear figura de matplotlib
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-1, 1)
    ax.set_xlabel('Posición')

    global object1, object2, time_text, momentum_text, energy_text
    object1, = ax.plot([], [], 'bo', ms=20)
    object2, = ax.plot([], [], 'ro', ms=20)
    time_template = 'Tiempo = %.1f s'
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
    momentum_text = ax.text(0.05, 0.8, '', transform=ax.transAxes)
    energy_text = ax.text(0.05, 0.7, '', transform=ax.transAxes)

    ani = animation.FuncAnimation(fig, update, fargs=(mass1, mass2, v1_initial, v2_initial, v1_final, v2_final),
                                  frames=int(total_time / dt), init_func=init, blit=True)
    
    # Crear canvas para matplotlib
    canvas = FigureCanvasTkAgg(fig, master=anim_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Crear frame para controles
    control_frame = ttk.Frame(anim_window)
    control_frame.pack(fill=tk.BOTH, expand=True)

    # Botón para detener la animación
    btn_stop_animation = ttk.Button(control_frame, text="Detener animación", command=stop_animation)
    btn_stop_animation.pack(side=tk.LEFT, padx=5, pady=5)

    # Botón para continuar la animación
    btn_continue_animation = ttk.Button(control_frame, text="Continuar animación", command=continue_animation)
    btn_continue_animation.pack(side=tk.LEFT, padx=5, pady=5)

    # Botón para ver gráficas
    btn_show_graphs = ttk.Button(control_frame, text="Ver gráficas", command=show_graphs)
    btn_show_graphs.pack(side=tk.LEFT, padx=5, pady=5)

    # Botón para ver datos
    btn_show_data = ttk.Button(control_frame, text="Ver datos", command=show_data)
    btn_show_data.pack(side=tk.LEFT, padx=5, pady=5)

    # Botón para cerrar la animación
    btn_close_animation = ttk.Button(control_frame, text="Cerrar animación", command=close_animation)
    btn_close_animation.pack(side=tk.LEFT, padx=5, pady=5)

# Función para mostrar las gráficas después de la animación
def show_graphs():
    global time_data, initial_momentum_data, final_momentum_data, initial_energy_data, final_energy_data, x1_data, x2_data, v1_data, v2_data

    # Crear una nueva ventana para las gráficas
    graph_window = tk.Toplevel(root)
    graph_window.title("Gráficas")
    graph_window.geometry("825x500")

    # Crear un marco de desplazamiento
    scroll_frame = ttk.Frame(graph_window)
    scroll_frame.pack(fill=tk.BOTH, expand=True)

    # Añadir un lienzo para las gráficas
    canvas = tk.Canvas(scroll_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Añadir una barra de desplazamiento
    scrollbar = ttk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Crear un marco interno para el contenido del lienzo
    graph_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=graph_frame, anchor="nw")

    # Mostrar gráficas
    fig, axs = plt.subplots(4, 1, figsize=(8, 10))
    axs[0].plot(time_data, initial_momentum_data, 'y-', marker='o', label='Momentum Inicial')
    axs[0].plot(time_data, final_momentum_data, 'm-', marker='x', label='Momentum Final')
    axs[0].set_xlabel('Tiempo (s)')
    axs[0].set_ylabel('Momentum (kg m/s)')
    axs[0].legend()

    axs[1].plot(time_data, initial_energy_data, 'g-', marker='s', label='Energía Inicial')
    axs[1].plot(time_data, final_energy_data, 'c-', marker='D', label='Energía Final')
    axs[1].set_xlabel('Tiempo (s)')
    axs[1].set_ylabel('Energía (J)')
    axs[1].legend()

    axs[2].plot(time_data, x1_data, 'g-', marker='^', label='Posición Masa 1')
    axs[2].plot(time_data, x2_data, 'm-', marker='v', label='Posición Masa 2')
    axs[2].set_xlabel('Tiempo (s)')
    axs[2].set_ylabel('Posición (m)')
    axs[2].legend()

    axs[3].plot(time_data, v1_data, 'y-', marker='p', label='Velocidad Masa 1')
    axs[3].plot(time_data, v2_data, 'c-', marker='*', label='Velocidad Masa 2')
    axs[3].set_xlabel('Tiempo (s)')
    axs[3].set_ylabel('Velocidad (m/s)')
    axs[3].legend()

    plt.tight_layout()

    # Convertir la figura de Matplotlib en un widget de Tkinter
    canvas_fig = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas_fig.draw()
    canvas_fig.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Actualizar el lienzo con el tamaño del contenido
    graph_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))



# Crear la interfaz gráfica con tkinter
root = tk.Tk()
root.title("Simulación de colisión")
root.geometry("400x200")

# Crear un marco para los controles
control_frame = ttk.Frame(root)
control_frame.pack(fill=tk.BOTH, expand=True)

# Etiquetas y campos de entrada
ttk.Label(control_frame, text="Masa 1:").grid(row=0, column=0)
mass1_entry = ttk.Entry(control_frame)
mass1_entry.grid(row=0, column=1)

ttk.Label(control_frame, text="Masa 2:").grid(row=1, column=0)
mass2_entry = ttk.Entry(control_frame)
mass2_entry.grid(row=1, column=1)

ttk.Label(control_frame, text="Velocidad 1:").grid(row=2, column=0)
v1_entry = ttk.Entry(control_frame)
v1_entry.grid(row=2, column=1)

ttk.Label(control_frame, text="Velocidad 2:").grid(row=3, column=0)
v2_entry = ttk.Entry(control_frame)
v2_entry.grid(row=3, column=1)

elastic_var = tk.BooleanVar(value=True)
ttk.Checkbutton(control_frame, text="Colisión Elástica", variable=elastic_var).grid(row=4, columnspan=2)

# Botón para iniciar la animación
ttk.Button(control_frame, text="Iniciar animación", command=start_animation).grid(row=5, columnspan=2)

# Botón para cerrar la aplicación
ttk.Button(control_frame, text="Cerrar aplicación", command=root.destroy).grid(row=6, columnspan=2)

root.mainloop()