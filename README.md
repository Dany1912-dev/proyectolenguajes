# Sistema de Gestión — Proyecto escolar

> **Proyecto académico de la materia de Lenguajes de Programación.** Fue mi primer acercamiento a los sistemas distribuidos y la arquitectura cliente-servidor: la primera vez que construí un Web Service, usé ASP.NET con Entity Framework y conecté dos aplicaciones distintas a través de una API REST. El frontend en Python con Tkinter fue una elección pragmática — era la herramienta más rápida para armar una interfaz de escritorio sin complicar el aprendizaje principal. El proyecto es sencillo y genérico por diseño: el objetivo era entender los conceptos, no construir un sistema complejo.

![ASP.NET Core](https://img.shields.io/badge/ASP.NET_Core-Web_API-512BD4?logo=dotnet&logoColor=white)
![Python](https://img.shields.io/badge/Python-Tkinter-3776AB?logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white)
![EF Core](https://img.shields.io/badge/Entity_Framework-Core-512BD4?logo=dotnet&logoColor=white)

---

## ¿Qué es?

Un sistema de gestión básico para un negocio ficticio con dos tipos de usuarios:

- **Clientes** — se registran, inician sesión y pueden hacer pedidos de productos
- **Encargados** — usan la aplicación de escritorio (Python/Tkinter) para gestionar el inventario de materias primas, administrar los pedidos activos y ver el reporte de ventas del día

La parte interesante del proyecto es la comunicación entre piezas: la app de escritorio llama a la API REST para operar sobre los datos, y la API le envía notificaciones en tiempo real a la app usando **sockets TCP** cuando ocurre algún evento relevante.

---

## Estructura del proyecto

```
ProyectoLenguajesProgramacion/
│
├── API/APIMetodologia/             # Backend — ASP.NET Core Web API
│   └── APIMetodologia/
│       ├── Controllers/
│       │   ├── AuthController.cs           # Registro y login de clientes
│       │   ├── ProductosController.cs      # Catálogo de productos y categorías
│       │   ├── PedidosController.cs        # Registrar pedidos y actualizar estatus
│       │   ├── MateriasPrimasController.cs # CRUD de inventario + alertas de stock bajo
│       │   └── AdminController.cs          # Reporte de ventas diarias
│       ├── Services/
│       │   ├── Interfaces/                 # IAuthService, IProductoService...
│       │   ├── Implementations/            # AuthService, PedidoService, ReporteService...
│       │   └── NotificadorSocket.cs        # Envía notificaciones a la app via TCP
│       ├── Models/
│       │   ├── Entities/                   # Usuario, Producto, MateriaPrima, PedidoCliente...
│       │   ├── Request/                    # LoginRequest, RegistroClienteRequest...
│       │   └── Responses/                  # AuthResponse
│       └── Data/
│           └── AppDbContext.cs             # DbContext con EF Core + MySQL
│
└── APP/ProyectoFigueroa/           # Frontend — Python + Tkinter (app de escritorio)
    ├── login.py                    # Pantalla de inicio de sesión
    ├── MenuPrincipal.py            # Menú con los tres módulos
    ├── FormMateriaPrima.py         # CRUD de materias primas con tabla y formulario
    ├── FormPedidos.py              # Vista de pedidos activos + cambio de estatus
    ├── FormReporte.py              # Reporte de ventas diarias
    ├── FormBase.py                 # Clase base con utilidades compartidas (hilos, mensajes)
    ├── clienteApi.py               # Wrapper HTTP para consumir la API REST
    ├── models.py                   # Dataclasses: UsuarioInfo, MateriaPrima, Producto...
    └── Socket.py                   # Servidor TCP que recibe notificaciones de la API
```

---

## Cómo funciona

### Backend (ASP.NET Core)

API REST mínima con cinco controllers. Usa **Entity Framework Core** para mapear las entidades a MySQL. La autenticación es con **JWT** enviado en el header `Authorization: Bearer <token>` — el cliente lo guarda en memoria y lo adjunta en cada petición.

No hay arquitectura en capas sofisticada: es un solo proyecto con controllers, servicios (con interfaces) y el DbContext. Suficiente para el alcance del proyecto.

### Frontend (Python / Tkinter)

Aplicación de escritorio que actúa como cliente de la API. `clienteApi.py` centraliza todas las llamadas HTTP usando la librería `requests` con un `threading.Lock` para serializar las peticiones. Cada formulario llama a la API en un hilo separado para no congelar la interfaz mientras espera la respuesta.

### Notificaciones via socket TCP

Esta fue la parte de sistemas distribuidos del proyecto:

```
API (ASP.NET)                    App escritorio (Python)
       │                                  │
       │  TCP a 127.0.0.1:65432           │
       │ ─────────────────────────────►   │
       │  { "accion": "INFO",             │  Socket.py escucha en
       │    "contenido": "..." }          │  un hilo en segundo plano
                                          │  y muestra messagebox
```

Cuando la API procesa un pedido o detecta algo relevante, `NotificadorSocket.cs` abre una conexión TCP al puerto 65432 y envía un JSON. La app en Python tiene un servidor TCP corriendo en un hilo `daemon` que recibe ese mensaje y lo muestra como alerta en la interfaz.

---

## Conceptos practicados

- Arquitectura cliente-servidor con una API REST como punto central
- Primer uso de ASP.NET Core y Entity Framework Core
- JWT para autenticación (token en memoria, sin cookies)
- Patrón de servicios con interfaces en C#
- Consumir una API HTTP desde Python con `requests`
- Comunicación entre procesos distintos con sockets TCP
- Aplicación de escritorio con Tkinter como cliente de una API

---

## Requisitos

**Backend:**
- .NET 8+ SDK
- MySQL 8.0
- Configurar la cadena de conexión y la clave JWT en `appsettings.json`

**Frontend:**
- Python 3.x
- `pip install requests`
- La API corriendo en `http://localhost:5000`

## Ejecución

```bash
# Backend
cd API/APIMetodologia
dotnet run

# Frontend (en otra terminal)
cd APP/ProyectoFigueroa
python login.py
```
