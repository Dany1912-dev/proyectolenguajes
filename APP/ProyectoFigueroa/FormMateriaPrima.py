import tkinter as tk
from tkinter import ttk, messagebox
from FormBase import FormBase
from clienteApi import api

class FormMateriaPrima(FormBase):
    def __init__(self, master):
        super().__init__(master, titulo="Gestión de Materia Prima")

        self.materiaSeleccionada = None
        self.crearDisenio()
        self.cargarMateriasPrimas()

    def crearDisenio(self):
            mainFrame = tk.Frame(self)
            mainFrame.pack(fill="both", expand=True, padx=10, pady=10)

            #Panel izquierdo - Lista y Alertas
            listaFrame = tk.LabelFrame(mainFrame, text="Inventario Actual y Alertas", padx=5, pady=5)
            listaFrame.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=5)

            #Tabla de Materias Primas
            self.tabla = ttk.Treeview(listaFrame, columns=("ID", "Nombre", "Descripción", "Stock", "Unidad de Medida", "Proveedor"), show='headings')
            self.tabla.heading("ID", text="ID", anchor=tk.W)
            self.tabla.heading("Nombre", text="Nombre", anchor=tk.W)
            self.tabla.heading("Descripción", text="Descripción", anchor=tk.W)
            self.tabla.heading("Stock", text="Stock", anchor=tk.W)
            self.tabla.heading("Unidad de Medida", text="Unidad de Medida", anchor=tk.W)
            self.tabla.heading("Proveedor", text="Proveedor", anchor=tk.W)
            self.tabla.column("ID", width=40, stretch=tk.NO)
            self.tabla.column("Stock", width=60, stretch=tk.NO)
            self.tabla.pack(fill=tk.BOTH, expand=True)

            self.tabla.bind("<<TreeviewSelect>>", self.seleccionarMateriaPrima)

            #Boton de alertas
            tk.Button(listaFrame, text="Ver Alertas de Stock Bajo", command=self.mostrarAlertas).pack(pady=5, fill="x")

            #Panel derecho: Formulario ABC
            formFrame = tk.LabelFrame(mainFrame, text="Crear / Actualizar Materia Prima", padx=5, pady=5)
            formFrame.pack(side="right", fill="y", padx=10, pady=5)

            #Campos del formulario
            self.entradas = {}

            tk.Label(formFrame, text="ID:").grid(row=0, column=0, sticky=tk.W, pady=2)
            id_entry = tk.Entry(formFrame, width=40)
            id_entry.grid(row=0, column=1, pady=5)
            self.entradas["ID"] = id_entry

            campos = ["Nombre", "Descripción", "Stock Actual", "Unidad de Medida", "ID Proveedor"]
            
            for i, campo in enumerate(campos):
                tk.Label(formFrame, text=f"{campo}:").grid(row=i, column=0, sticky=tk.W, pady=2)
                entrada = tk.Entry(formFrame)
                entrada.grid(row=i, column=1, pady=5)
                self.entradas[campo] = entrada

            self.entradas["ID"].config(state=tk.DISABLED)

            #Botones de acciones
            btnFrame = tk.Frame(formFrame)
            btnFrame.grid(row=len(campos),column=0, columnspan=2, pady=10)

            tk.Button(btnFrame, text="Crear Nuevo", command=self.crearMateriaPrima).pack(side="left", padx=5)
            tk.Button(btnFrame, text="Actualizar", command=self.actualizarMateriaPrima).pack(side="left", padx=5)
            tk.Button(btnFrame, text="Eliminar", command=self.eliminarMateriaPrima).pack(side="left", padx=5)
            tk.Button(btnFrame, text="Limpiar Formulario", command=self.limpiarFormulario).pack(side="left", padx=5)

            self.labelEstatus = tk.Label(formFrame, text="", fg="black")
            self.labelEstatus.grid(row=len(campos)+1, column=0, columnspan=2, pady=10)

            tk.Button(formFrame, text="Volver al Menú Principal", command=self.master.destroy).grid(row=len(campos)+2, column=0, columnspan=2, pady=20)

    def cargarMateriasPrimas(self):
        self.ejecutrarPorHilo(
            funcionApi=api.obtenerMateriasPrimas,
            callbackExito=self.llenarTabla,
            callbackError=self.manejarErrorCarga,
            mensajeCargando="Cargando inventario..."
        )

    def llenarTabla(self, materias_primas):
        self.tabla.delete(*self.tabla.get_children())
        for mp in materias_primas:
            self.tabla.insert("", tk.END, values=(
                mp.idMateriaPrima, 
                mp.nombre, 
                mp.descripcion,
                mp.stockActual, 
                mp.unidadDeMedida,
                mp.idProveedor
            ), tags=('normal',))
        
        self.limparEstado(f"Inventario cargado. Total: {len(materias_primas)}")

    def manejarErrorCarga(self, error):
        self.mostrarError(f"No se pudo cargar el inventario: {error}")
        self.limparEstado("Error al cargar inventario")

    def seleccionarMateriaPrima(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0], 'values')
            
            self.ejecutrarPorHilo(
                funcionApi=lambda id: api.solicitud('GET', f'MateriasPrimas/{id}'),
                args=(item[0],),
                callbackExito=self.llenarFormularioSeleccion,
                mensajeCargando="Obteniendo detalles..."
            )

    def llenarFormularioSeleccion(self, datos_json):
        self.limpiarFormulario()
        self.entradas["ID"].config(state=tk.NORMAL)
        self.entradas["ID"].delete(0, tk.END)
        self.entradas["ID"].insert(0, datos_json['idMateriaPrima'])
        self.entradas["ID"].config(state=tk.DISABLED)

        self.entradas["Nombre"].insert(0, datos_json['nombre'])
        self.entradas["Descripción"].insert(0, datos_json['descripcion'])
        self.entradas["Stock Actual"].insert(0, datos_json['stockActual'])
        self.entradas["Unidad de Medida"].insert(0, datos_json['unidadDeMedida'])
        self.entradas["ID Proveedor"].insert(0, datos_json['idProveedor'])
        self.materia_seleccionada = datos_json['idMateriaPrima']
        self.limparEstado("Materia prima seleccionada, lista para edición.")

    def obtenerDatosFormulario(self):
        try:
            datos = {
                "idMateriaPrima": int(self.entradas["ID"].cget('state') == tk.DISABLED and self.entradas["ID"].get() or 0),
                "nombre": self.entradas["Nombre"].get(),
                "descripcion": self.entradas["Descripción"].get(),
                "stockActual": int(self.entradas["Stock Actual"].get()),
                "unidadDeMedida": self.entradas["Unidad de Medida"].get(),
                "idProveedor": int(self.entradas["ID Proveedor"].get())
            }
            if not datos["nombre"] or datos["stockActual"] < 0:
                 raise ValueError("Nombre y Stock son campos requeridos y Stock debe ser positivo.")
            return datos
        except ValueError as e:
            self.mostrarError(f"Error en los datos: {e}")
            return None

    def crearMateriaPrima(self):
        datos = self.obtenerDatosFormulario()
        if datos is None or datos['idMateriaPrima'] != 0:
            self.mostrarError("Por favor, limpie el formulario antes de crear un nuevo registro.")
            return

        datos.pop('idMateriaPrima')

        self.ejecutrarPorHilo(
            funcionApi=api.crearMateriaPrima,
            args=(datos,),
            callbackExito=lambda mp: self.manejarExitoABC("Creada", mp),
            mensajeCargando="Creando materia prima..."
        )

    def actualizarMateriaPrima(self):
        datos = self.obtenerDatosFormulario()
        if datos is None or datos['idMateriaPrima'] == 0:
            self.mostrarError("Seleccione una materia prima para actualizar.")
            return

        self.ejecutrarPorHilo(
            funcionApi=api.actualizarMateriaPrima,
            args=(datos['idMateriaPrima'], datos,),
            callbackExito=lambda mp: self.manejarExitoABC("Actualizada", mp),
            mensajeCargando="Actualizando materia prima..."
        )

    def eliminarMateriaPrima(self):
        id_mp = self.entradas["ID"].get()
        if not id_mp:
            self.mostrarError("Seleccione una materia prima para eliminar.")
            return
        
        if not messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar la Materia Prima ID: {id_mp}?"):
            return

        self.ejecutrarPorHilo(
            funcionApi=api.eliminarMateriaPrima,
            args=(int(id_mp),),
            callbackExito=lambda _: self.manejarExitoABC("Eliminada", None),
            mensajeCargando="Eliminando materia prima..."
        )

    def manejarExitoABC(self, operacion, resultado):
        self.mostrarInfo(f"Materia Prima {operacion} exitosamente.")
        self.limpiarFormulario()
        self.cargarMateriasPrimas()

    def limpiarFormulario(self):
        for entrada in self.entradas.values():
            entrada.config(state=tk.NORMAL)
            entrada.delete(0, tk.END)
        self.materia_seleccionada = None
        self.entradas["ID"].config(state=tk.DISABLED)
        self.limparEstado("Listo.")

    def mostrarAlertas(self):
        self.ejecutrarPorHilo(
            funcionApi=lambda: api.obtenerAlertasBajoStock(10),
            callbackExito=self.mostrarVentanaDeAlertas,
            mensajeCargando="Obteniendo alertas de stock bajo..."
        )

    def mostrarVentanaDeAlertas(self, alertas):
        self.limparEstado(f"Alertas de stock obtenidas. {len(alertas)} ítems en riesgo.")
        
        if not alertas:
            messagebox.showinfo("Alertas de Stock", "No hay materias primas con stock bajo (>= 10).")
            return
            
        mensaje = "--- ALERTA DE STOCK BAJO ---\n\n"
        for mp in alertas:
            mensaje += f"{mp.nombre}: {mp.stockActual} {mp.unidadDeMedida}\n"
        
        messagebox.showwarning("Stock Bajo: ", mensaje)