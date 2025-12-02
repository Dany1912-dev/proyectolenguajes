class UsuarioInfo:
    def __init__(self, id, nombre, email, telefono, tipoUsuario, token):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.tipoUsuario = tipoUsuario
        self.token = token

    def __str__(self):
        return f"Usuario: {self.nombre} ({self.tipoUsuario})"
    
class MateriaPrima:
    def __init__(self, idMateriaPrima, nombre, descripcion, stockActual, unidadDeMedida, idProveedor, proveedor = None):
        self.idMateriaPrima = idMateriaPrima
        self.nombre = nombre
        self.descripcion = descripcion
        self.stockActual = stockActual
        self.unidadDeMedida = unidadDeMedida
        self.idProveedor = idProveedor
        self.proveedor = proveedor

    def __str__(self):
        return f"{self.nombre} - {self.stockActual} {self.unidadDeMedida}"
    
class Producto:
    def __init__(self, idProducto, idCategoria, nombre, descripcion, precio, imagenURL):
        self.idProducto = idProducto
        self.idCategoria = idCategoria
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.imagenURL = imagenURL

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class PedidoCliente:
    def __init__(self, idPedidoCliente, idUsuario, fechaPedido, estatus, total, detalles = None):
        self.idPedidoCliente = idPedidoCliente
        self.idUsuario = idUsuario
        self.fechaPedido = fechaPedido
        self.estatus = estatus
        self.total = total
        self.detalles = detalles

    def __str__(self):
        return f"Pedido #{self.id} | Total: ${self.total} | Estatus: {self.estatus}"
        
class DetallePedidoCliente:
    def __init__(self, idDetallePedidoCliente, idPedidoCliente, idProducto, cantidad, precioUnitario, producto = None):
        self.idDetallePedidoCliente = idDetallePedidoCliente
        self.idPedidoCliente = idPedidoCliente
        self.idProducto = idProducto
        self.cantidad = cantidad
        self.precioUnitario = precioUnitario
        self.producto = producto

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre if self.producto else 'Producto Desconocido'}"
    
class ProductoDetalleRequest:
    def __init__(self, idProducto, cantidad):
        self.idProducto = idProducto
        self.cantidad = cantidad