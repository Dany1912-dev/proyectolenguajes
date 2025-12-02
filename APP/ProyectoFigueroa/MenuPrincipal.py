import tkinter as tk
from FormBase import FormBase
from clienteApi import api
from FormMateriaPrima import FormMateriaPrima 
from FormPedidos import FormPedidos
from FormReporte import FormReportes

class MenuPrincipal(FormBase):
    def __init__(self, master=None):
        super().__init__(master, titulo="Menú Principal - Sistema Gestor")
        self.pack(padx=20, pady=20, fill="both", expand=True)
        self.crearDisenio()

    def crearDisenio(self):
        user_info = api.usuarioActual
        
        tk.Label(self, text="BIENVENIDO, ENCARGADO", font=("Arial", 18, "bold")).pack(pady=10)
        
        tk.Label(self, text="--- MÓDULOS DE GESTIÓN ---", font=("Arial", 12)).pack(pady=15)

        tk.Button(self, text="1. Gestión de Materias Primas", width=40, 
                  command=self.abrirGestionMateriaPrima).pack(pady=5)
        
        tk.Button(self, text="2. Gestión de Pedidos de Clientes", width=40, 
                  command=self.abrirGestionPedidos).pack(pady=5)
        
        tk.Button(self, text="3. Reporte Diario de Ventas", width=40, 
                  command=self.abrirReporteVentas).pack(pady=5)
        
        tk.Button(self, text="4. Chat y Notificaciones", width=40, 
                  command=lambda: self.mostrarInfo("Aun no esta hecho, es el apartado de Sockets e hilos sincronizados")).pack(pady=5)
        
        tk.Button(self, text="Cerrar Sesión", fg="red", command=self.cerrarSesion).pack(pady=30)
        
        self.labelEstatus = tk.Label(self, text="Listo.", fg="black")
        self.labelEstatus.pack(side="bottom", fill="x")

    def abrirGestionMateriaPrima(self):
        new_window = tk.Toplevel(self.master)
        FormMateriaPrima(master=new_window)

    def abrirGestionPedidos(self):
        new_window = tk.Toplevel(self.master)
        FormPedidos(master=new_window)
        
    def cerrarSesion(self):
        api.usuarioActual = None
        self.master.destroy()

    def abrirReporteVentas(self):
        nuevaVentana = tk.Toplevel(self.master)
        FormReportes(master=nuevaVentana)