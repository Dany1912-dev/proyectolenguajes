import json
from models import UsuarioInfo, MateriaPrima, Producto, PedidoCliente, DetallePedidoCliente
import urllib.parse
import requests
import threading
class ClienteAPI:
    usuarioActual = None
    urlBase = "http://localhost:5000/api/"

    def __init__(self):
        self.bloqueo = threading.Lock()
            
    def get_headers(self):
        headers = {
            'Content-Type': 'application/json'
        }
        if self.usuarioActual and self.usuarioActual.token:
            headers['Authorization'] = f'Bearer {self.usuarioActual.token}'
        return headers

    def solicitud(self, metodo, endpoint, datos=None):
        with self.bloqueo:
            url = urllib.parse.urljoin(self.urlBase, endpoint)
            headers = self.get_headers()
            datos = json.dumps(datos) if datos else None

            try:
                if metodo == 'GET':
                    respuesta = requests.get(url, headers=headers)
                elif metodo == 'POST':
                    respuesta = requests.post(url, headers=headers, data=datos)
                elif metodo == 'PUT':
                    respuesta = requests.put(url, headers=headers, data=datos)
                elif metodo == 'DELETE':
                    respuesta = requests.delete(url, headers=headers)
                else:
                    raise ValueError(f"Método HTTP no soportado: {metodo}")
                
                if respuesta.status_code == 204:
                    return True
                respuesta.raise_for_status()
                
                return respuesta.json()
            except requests.exceptions.HTTPError as e:
                try:
                    detalleError = e.response.json().get('mensaje', e.response.reason)
                except:
                    detalleError = e.response.reason
                raise Exception(f"Error HTTP {e.response.status_code}: {detalleError}")
            except requests.exceptions.RequestException as e:
                raise Exception(f"Error de conexion con la API: {e}")
        
    def login(self, email, password):
        with self.bloqueo:
            endpoint = "Auth/login"
            datos = {
                "email": email,
                "password": password
            }

            url = urllib.parse.urljoin(self.urlBase, endpoint)
            respuesta = requests.post(url, headers=self.get_headers(), data=json.dumps(datos))

            if respuesta.status_code == 400:
                datosError = respuesta.json()
                raise Exception(f"Inicio de sesion fallido: {datosError.get('mensaje', 'Credenciales inválidas')}")
            respuesta.raise_for_status()
            datosUsuario = respuesta.json()
            if datosUsuario.get('exito'):
                datosUsuarioInfo = datosUsuario.get('usuario', {})

                ClienteAPI.usuarioActual = UsuarioInfo(
                    id=datosUsuarioInfo.get('id'),
                    nombre=datosUsuarioInfo.get('nombre'),
                    email=datosUsuarioInfo.get('email'),
                    telefono=datosUsuarioInfo.get('telefono'),
                    tipoUsuario=datosUsuarioInfo.get('tipoUsuario'),
                    token=datosUsuario.get('token')
                )
                return ClienteAPI.usuarioActual
            else:
                raise Exception("Inicio de sesion fallido: Credenciales inválidas")
        
    # Materias Primas
    def obtenerMateriasPrimas(self):
        datos = self.solicitud('GET', 'MateriasPrimas')
        
        if datos is None or not isinstance(datos, list):
            datos = []
        
        return [MateriaPrima(**item) for item in datos]
    
    def obtenerAlertasBajoStock(self, umbral):
        endpoint = f'MateriasPrimas/stock-bajo/{umbral}'
        datos = self.solicitud('GET', endpoint)
        return [MateriaPrima(**item) for item in datos]
    
    def crearMateriaPrima(self, datosMateriaPrima):
        datos = self.solicitud('POST', 'MateriasPrimas', datosMateriaPrima)
        return MateriaPrima(**datos)
    
    def actualizarMateriaPrima(self, idMateriaPrima, datosMateriaPrima):
        endpoint = f'MateriasPrimas/{idMateriaPrima}'
        datos = self.solicitud('PUT', endpoint, datosMateriaPrima)
        return MateriaPrima(**datos)
    
    def eliminarMateriaPrima(self, idMateriaPrima):
        endpoint = f'MateriasPrimas/{idMateriaPrima}'
        return self.solicitud('DELETE', endpoint)
    
    # Pedidos
    def registrarPedidoManual(self, datosPedido):
        datosLoad = {"productos": datosPedido}
        datos = self.solicitud('POST', 'Pedidos/manual', datosLoad)
        return PedidoCliente(**datos)
    
    def obtenerPedidosActivos(self):
        datos = self.solicitud('GET', 'Pedidos/activos')
        return datos
    
    def actualizarEstatusPedido(self, idPedido, nuevoEstatus):
        endpoint = f'Pedidos/{idPedido}/estatus/{nuevoEstatus}'
        datos = self.solicitud('PUT', endpoint)
        return datos
    
    #Reportes
    def generarReporteVentasDiarias(self):
        return self.solicitud('GET', 'Admin/reporte/ventas-diarias')
    
api = ClienteAPI()