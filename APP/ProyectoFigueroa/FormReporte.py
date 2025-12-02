import tkinter as tk
from tkinter import messagebox
from FormBase import FormBase
from clienteApi import api
import datetime

class FormReportes(FormBase):
    def __init__(self, master=None):
        super().__init__(master, titulo="Reporte Diario de Ventas")
        self.crearDisenio()


    def crearDisenio(self):
        mainFrame = tk.Frame(self)
        mainFrame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(mainFrame, text="Reporte de ventas diarias", font=("Arial", 16, "bold")).pack(pady=15)
        
        self.totalLabel = tk.Label(mainFrame, text="Cargando Total...", font=("Arial", 24), fg="gray")
        self.totalLabel.pack(pady=30)

        self.fechaCorteLabel = tk.Label(mainFrame, text="Ultimas 24 horas", font=("Arial", 10))
        self.fechaCorteLabel.pack(pady=5)

        tk.Button(mainFrame, text="Actualizar Reporte", command=self.generarReporte).pack(pady=15)
        tk.Button(mainFrame, text="Volver al Menu", command=self.master.destroy).pack(pady=10)

        self.labelEstatus = tk.Label(mainFrame, text="Listo.", fg="black")
        self.labelEstatus.pack(side="bottom", fill="x")


    def generarReporte(self):
        self.totalLabel.config(text="Cargando Total...", fg="gray")
        self.fechaCorteLabel.config(text="Ultimas 24 horas")

        self.ejecutrarPorHilo(
            funcionApi=api.generarReporteVentasDiarias,
            callbackExito=self.mostrarReporte,
            callbackError=self.manejarErrorReporte,
            mensajeCargando="Generando Reporte..."
        )

    def mostrarReporte(self, resultado):
        try:
            if not isinstance(resultado, dict):
                raise TypeError(f"La API devolvio un tipo inesperado: {type(resultado).__name__}. Se esperaba un diccionario")
            total = resultado.get('total24Horas', 0.0)
            fechaCorteStr = resultado.get('fechaCorte', 'N/A')

            totalFormato = f"${total:,.2f}"
            self.totalLabel.config(text=totalFormato, font=("Arial", 36, "bold"), fg="green")

            self.fechaCorteLabel.config(text=f"Ventas Totales de las Ultimas 24 horas hasta {fechaCorteStr[11:19]}")

            self.limparEstado("Reporte cargado con exito")

        except Exception as e:
            self.manejarErrorReporte(e)

    def manejarErrorReporte(self, error):
        self.totalLabel.config(text="ERROR", font=("Arial", 36, "bold"), fg="red")
        self.mostrarError(f"No se pudo generar el reporte: {error}")