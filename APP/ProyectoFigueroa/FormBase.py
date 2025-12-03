import tkinter as tk
from tkinter import messagebox
import threading

class FormBase(tk.Frame):
    def __init__(self, master=None, titulo = "Formulario Base"):
        super().__init__(master)
        self.master = master
        self.master.title(titulo)
        self.pack(fill=tk.BOTH, expand=True)
        
    def ejecutrarPorHilo(self, funcionApi, args=(), callbackExito=None, callbackError=None, mensajeCargando = "Procesando..."):
        if hasattr(self, 'labelEstatus'):
            self.master.after(0, lambda: self.labelEstatus.config(text=mensajeCargando, fg="blue"))

        def tarea():
            try:
                resultado = funcionApi(*args)

                if hasattr(self, 'labelEstatus'):
                    self.master.after(0, lambda: self.labelEstatus.config(text="Operación completada.", fg="green"))

                if callbackExito:
                    self.master.after(0, lambda: callbackExito(resultado))

            except Exception as e:

                if hasattr(self, 'labelEstatus'):
                    self.master.after(0, lambda: self.labelEstatus.config(text="Error durante la operación.", fg="red"))

                if callbackError:
                    self.master.after(0, callbackError, e)
                else:
                    self.master.after(0, lambda: messagebox.showerror("Error", str(e)))

        threading.Thread(target=tarea).start()

    def mostrarInfo(self, mensaje):
        self.master.after(0, lambda: messagebox.showinfo("Información", mensaje))

    def mostrarError(self, mensaje):
        self.master.after(0, lambda: messagebox.showerror("Error", mensaje))

    def limparEstado(self, mensaje):
        if hasattr(self, 'labelEstatus'):
            self.master.after(0, lambda: self.labelEstatus.config(text=mensaje, fg="black"))