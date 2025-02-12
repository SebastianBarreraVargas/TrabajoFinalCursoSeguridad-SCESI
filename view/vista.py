# view/vista.py
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb

class Vista:
    def __init__(self, controlador):
        self.controlador = controlador
        self.root = tb.Window(themename="superhero")
        self.root.title("Interfaz con CMS Detector")
        self.root.geometry("600x400")

        # Frame para contener los elementos
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.pack(fill='both', expand=True)

        # Barra de entrada de texto
        self.entry = ttk.Entry(self.frame, width=30)
        self.entry.pack(pady=10)

        # Botón
        self.button = ttk.Button(
            self.frame,
            text="Detectar CMS",
            command=self.detectar_cms
        )
        self.button.pack()

        # Etiqueta para mostrar el resultado
        self.result_label = ttk.Label(self.frame, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

    def detectar_cms(self):
        url = self.entry.get()  # Obtener la URL desde el campo de entrada
        if url:
            # Llamar al controlador para detectar el CMS
            resultado = self.controlador.detectar_cms(url)
            self.result_label.config(text=f"CMS Detectado: {resultado}")
        else:
            self.result_label.config(text="Por favor, ingresa una URL.")

    def iniciar(self):
        self.root.mainloop()