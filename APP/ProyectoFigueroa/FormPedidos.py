import tkinter as tk
from FormBase import FormBase
from clienteApi import api
from tkinter import ttk, messagebox
from models import PedidoCliente

class FormPedidos(FormBase):
    def __init__(self, master):
        super().__init__(master, titulo="Gestión de Pedidos de Clientes")

        self.pedidoSeleccionadoId = None
        self.crearDisenio()
        self.cargarPedidos()

    def crearDisenio(self):
        mainFrame = tk.Frame(self)
        mainFrame.pack(fill="both", expand=True, padx=10, pady=10)

        #Panel Superior: Botones de gestion
        gestionFrame = tk.LabelFrame(mainFrame, text="Gestion de Estado", padx=10, pady=10)
        gestionFrame.pack(side="top", fill="x", pady=5)

        tk.Label(gestionFrame, text="Nuevo Estatus").pack(side="left", padx=5)

        registroFrame = tk.LabelFrame(mainFrame, text="Registro Manual De Pedidos", padx=10, pady=10)
        registroFrame.pack(side="top", fill="x", pady=5)

        tk.Label(registroFrame, text="ID Producto:").pack(side="left", padx=5)
        self.entradaIdProducto = tk.Entry(registroFrame, width=10)
        self.entradaIdProducto.pack(side="left", padx=5)
        self.entradaCantidad = tk.Entry(registroFrame, width=10)
        self.entradaCantidad.pack(side="left", padx=5)

        tk.Button(registroFrame, text="Añadir Pedido", command=self.agregarProductoAPedido).pack(side="left", padx=10)
        tk.Button(registroFrame, text="FINALIZAR VENTA", command=self.registrarPedidoManual).pack(side="left", padx=20, fill="x")

        self.listaProductosLocal = tk.Listbox(registroFrame, height=3, width=40)
        self.listaProductosLocal.pack(side="right", padx=5, fill="both", expand=True)

        self.pedidoEnCurso = []

        #Opciones de estatus = BD
        self.estatusOpcion = ["Pendiente", "En Proceso", "Completado", "Cancelado"]
        self.nuevoEstatus = tk.StringVar(gestionFrame)
        self.nuevoEstatus.set("Listo")

        ttk.OptionMenu(gestionFrame, self.nuevoEstatus, self.nuevoEstatus.get(), *self.estatusOpcion).pack(side="left", padx=10)

        tk.Button(gestionFrame, text="Actualizar Estatus", command=self.actualizarEstatusPedido).pack(side="left", padx=10)
        tk.Button(gestionFrame, text="Cargar Pedidos", command=self.cargarPedidos).pack(side="left", padx=10)
        tk.Button(gestionFrame, text="Volver al menu", command=self.master.destroy).pack(side="right", padx=10)

        #Etiqueta de estado
        self.labelEstatus = tk.Label(mainFrame, text="", fg="black")
        self.labelEstatus.pack(side="bottom", fill="x")

        #Panel Central
        listaFrame = tk.LabelFrame(mainFrame, text="Pedidos Activos", padx=5, pady=5)
        listaFrame.pack(side="top", fill="both", expand=True, pady=5)

        columnas = ("ID", "Cliente ID", "Fecha", "Estatus", "Total", "Detalles")
        self.tabla = ttk.Treeview(listaFrame, columns=columnas, show='headings')

        self.tabla.heading("ID", text="ID", anchor=tk.W)
        self.tabla.heading("Cliente ID", text="Cliente ID", anchor=tk.W)
        self.tabla.heading("Fecha", text="Fecha", anchor=tk.W)
        self.tabla.heading("Estatus", text="Estatus", anchor=tk.W)
        self.tabla.heading("Total", text="Total", anchor=tk.W)
        self.tabla.heading("Detalles", text="Detalles", anchor=tk.W)

        self.tabla.column("ID", width=50, stretch=tk.NO)
        self.tabla.column("Estatus", width=100, stretch=tk.NO)
        self.tabla.column("Total", width=80, stretch=tk.NO)
        self.tabla.column("Detalles", width=300, stretch=tk.NO)

        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionarPedido)

    def cargarPedidos(self):
        self.ejecutrarPorHilo(
            funcionApi=api.obtenerPedidosActivos,
            callbackExito=self.mostrarPedidosEnTabla,
            callbackError=self.manejarErrorCarga,
            mensajeCargando="Cargando pedidos..."
        )
    
    def mostrarPedidosEnTabla(self, pedidos):
        self.tabla.delete(*self.tabla.get_children())

        for pedido in pedidos:
            resumenDetalles = self.ObtenerResumenDetalles(pedido.get("detalles", []))

            self.tabla.insert("", tk.END, values=(
                pedido.get('idPedidoCliente'),
                pedido.get('idUsuario'),
                pedido.get('fechaPedido')[:10],
                pedido.get('estatus'),
                f"${pedido.get('total'):.2f}",
                resumenDetalles
            ))

        self.limparEstado(f"Peiddos activos cargados: {len(pedidos)}")

    def ObtenerResumenDetalles(self, detalles):
        resumen = []
        for detalle in detalles:
            producto = detalle.get("producto")
            nombre = producto.get("nombre") if producto and producto.get('nombre') else "Desconocido"
            resumen.append(f"{detalle.get('cantidad')} x {nombre}")
        return ", ".join(resumen[:3])
    
    def seleccionarPedido(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0], 'values')
            self.pedidoSeleccionadoId = item[0]
            self.limparEstado(f"Pedido seleccionado ID: {self.pedidoSeleccionadoId}")

    def actualizarEstatusPedido(self):
        if not self.pedidoSeleccionadoId:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione un pedido para actualizar su estatus.")
            return

        nuevoEstatus = self.nuevoEstatus.get()
        idPedido = self.pedidoSeleccionadoId

        self.ejecutrarPorHilo(
            funcionApi=api.actualizarEstatusPedido(self.pedidoSeleccionadoId, nuevoEstatus),
            args=(idPedido, nuevoEstatus),
            callbackError=self.manejarExitoActualizacion,
            mensajeCargando=f"Actualizando pedido {idPedido} a {nuevoEstatus}..."
        )

    def manejarExitoActualizacion(self, resultado):
        self.mostrarInfo(f"Pedido #{self.pedidoSeleccionadoId} actualizado correctamente")
        self.pedidoSeleccionadoId = None
        self.cargarPedidos()

    def manejarErrorCarga(self, error):
        self.mostrarError(f"No se pudieron cargar los pedidos: {error}")

    def agregarProductoAPedido(self):
        try:
            IDProducto = int(self.entradaIdProducto.get())
            cantidad = int(self.entradaCantidad.get())

            if IDProducto <= 0 or cantidad <= 0:
                self.mostrarError("ID de producto y Cantidad deben ser números positivos.")
                return
            
            from models import ProductoDetalleRequest
            nuevoDetalle = ProductoDetalleRequest(idProducto=IDProducto, cantidad=cantidad)

            self.pedidoEnCurso.append(nuevoDetalle)

            self.listaProductosLocal.insert(tk.END, f"ID: {IDProducto} x {cantidad}")

            self.entradaIdProducto.delete(0, tk.END)
            self.entradaCantidad.delete(0, tk.END)
            self.limparEstado(f"Producto {IDProducto} añadido al pedido")

        except ValueError:
            self.mostrarError("ID de producto y Cantidad deben ser valores numericos")

    def registrarPedidoManual(self):
        if not self.pedidoEnCurso:
            self.mostrarError("El pedido esta vacio")
            return

        cargaProductos = [vars(p) for p in self.pedidoEnCurso]

        self.ejecutrarPorHilo(
            funcionApi=api.registrarPedidoManual,
            args=(cargaProductos,),
            callbackExito=self.manejarExitoRegistro,
            mensajeCargando="Registrando pedido manual..."
        )

    def manejarExitoRegistro(self, resultadoPedido):
        self.mostrarInfo(f"Venta manual registrada")
        self.pedidoEnCurso = []
        self.listaProductosLocal.delete(0, tk.END)
        self.cargarPedidos()