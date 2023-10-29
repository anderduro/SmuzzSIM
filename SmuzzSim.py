import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
import pyautogui
import time
import threading
import keyboard

# Variables globales para llevar el estado del script
is_running = False
stop_event = threading.Event()
script_thread = None 

# Función para iniciar el script
def start_script():
    global is_running
    is_running = True
    start_button.config(state="disabled")
    stop_button.config(state="active")

    # Start the script in a separate thread
    script_thread = threading.Thread(target=main_script)
    script_thread.start()

# Función para detener el script
def stop_script():
    global is_running, stop_event
    is_running = False
    stop_event.set()
    start_button.config(state="active")
    stop_button.config(state="disabled")

# Función para iniciar o detener el script
def toggle_script():
    global is_running, stop_event
    global script_thread  # Access the script_thread variable in the global scope

    if is_running:
        is_running = False
        stop_event.set()
        stop_event = threading.Event()
        start_button.config(state="active")
        stop_button.config(state="disabled")
    else:
        is_running = True
        start_button.config(state="disabled")
        stop_button.config(state="active")
        script_thread = threading.Thread(target=main_script)
        script_thread.start()
# Función principal del script
def main_script():
    global is_running, stop_event

    # Variable para llevar la cuenta de cuántas imágenes se han detectado
    image_count = 0

    # Variable para indicar si se encontró alguna de las imágenes 4 o 5
    found_image_4_or_5 = False

    # Variable para realizar un clic en la última ubicación si no se encuentra 6 o 7 en 10 segundos
    last_click_time = time.time()

    while is_running and not stop_event.is_set(): 
            if not is_running:
                break  # Sal del bucle si se detiene el script

            screenshot = pyautogui.screenshot()
            screenshot = np.array(screenshot)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)

            if image_count < 3:
                # Reemplaza 'image1.png', 'image2.png', 'image3.png' con las imágenes que debes hacer clic
                for image_file in ['image1.png', 'image2.png', 'image3.png']:
                    target_image = cv2.imread(image_file)
                    h, w, _ = target_image.shape

                    result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
                    _, _, _, max_loc = cv2.minMaxLoc(result)

                    if result[max_loc[1], max_loc[0]] > 0.7:  # Ajusta el umbral de coincidencia según tus necesidades
                        x, y = max_loc[0] + w // 2, max_loc[1] + h // 2
                        pyautogui.click(x, y)
                        image_count += 1

            else:
                # Después de detectar la tercera imagen, escribe "2146"
                pyautogui.typewrite("2146")
                time.sleep(3)  # Agrega un segundo de espera después de escribir

                # Reinicia el contador
                image_count = 0

                # Reemplaza 'image4.png' y 'image5.png' con las imágenes que debes hacer clic
                for image_file in ['image4.png', 'image5.png']:
                    target_image = cv2.imread(image_file)
                    h, w, _ = target_image.shape

                    result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
                    _, _, _, max_loc = cv2.minMaxLoc(result)

                    if result[max_loc[1], max_loc[0]] > 0.6:  # Ajusta el umbral de coincidencia según tus necesidades
                        x, y = max_loc[0] + w // 2, max_loc[1] + h // 2
                        pyautogui.click(x, y)

                        found_image_4_or_5 = True  # Indica que se encontró al menos una de las imágenes 4 o 5
    

                # Si se encontró al menos una de las imágenes 4 o 5, busca en bucle la imagen 6 y 7
                while found_image_4_or_5 and is_running and not stop_event.is_set():
                    for image_file in ['image6.png', 'image7.png']:
                        target_image = cv2.imread(image_file)
                        h, w, _ = target_image.shape

                        result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
                        _, _, _, max_loc = cv2.minMaxLoc(result)

                        if result[max_loc[1], max_loc[0]] > 0.9:  # Ajusta el umbral de coincidencia según tus necesidades
                            x, y = max_loc[0] + w // 2, max_loc[1] + h // 2
                            pyautogui.click(x, y)

                        # Verifica si han pasado 10 segundos desde el último clic
                        current_time = time.time()
                        if current_time - last_click_time >= 10:
                            # Realiza un clic en la última ubicación
                            pyautogui.click(x, y)
                            last_click_time = current_time

                        # Verifica si se encuentra la imagen "button.png" y haz clic para salir del bucle
                        button_image = cv2.imread('button.png')
                        result_button = cv2.matchTemplate(screenshot, button_image, cv2.TM_CCOEFF_NORMED)
                        _, _, _, max_loc_button = cv2.minMaxLoc(result_button)

                        if result_button[max_loc_button[1], max_loc_button[0]] > 0.8:
                            x_button, y_button = max_loc_button[0] + w // 2, max_loc_button[1] + h // 2
                            pyautogui.click(x_button, y_button)
                            found_image_4_or_5 = False  # Sal del bucle

                        # Puedes agregar un segundo de espera aquí si lo deseas

                    # Vuelve a tomar una captura de pantalla para la próxima iteración
                    screenshot = pyautogui.screenshot()
                    screenshot = np.array(screenshot)
                    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
            pass


# Crear la ventana de la aplicación
window = tk.Tk()
window.title("Ark ASA SIM by Smuzz")

# Set the window icon (replace 'icon.ico' with your icon file)
window.iconbitmap('icon.ico')

# Configurar el fondo de la ventana con un color oscuro
window.configure(bg='#1f1f1f')

# Estilo personalizado para los botones con grises oscuros casi negros
button_style = ttk.Style()

# Color de fondo ligeramente más claro que el fondo de la ventana
button_background = '#724C00'

button_style.configure("TButton", font=("Helvetica", 12), foreground="gray",
                      padding=(5, 5), background=button_background)
button_style.map('TButton', foreground=[('disabled', 'white'),('active', 'gray')])

# Botón para iniciar el script
start_button = ttk.Button(window, text="Start (F6)", command=start_script, state="active")
start_button.pack(side="left", padx=10, pady=10, ipadx=10, ipady=5)

# Botón para detener el script
stop_button = ttk.Button(window, text="Stop (F6)", command=stop_script, state="disabled")
stop_button.pack(side="left", padx=10, pady=10, ipadx=10, ipady=5)

# Add a hotkey to toggle the script with F6
keyboard.add_hotkey('F6', lambda: toggle_script())
# Iniciar la ventana principal de la aplicación
window.mainloop()