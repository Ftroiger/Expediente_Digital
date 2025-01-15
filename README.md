# API Documentación

#### DbCreation
crear una base de datos en postgresql

crear archivo .env
URL_BASE_DE_DATOS = DB connection EXAMPLE "postgresql://usuario:contraseña@localhost:5432/nombre_DB"
MICROSERVICIO_USUARIO=http://localhost:8001
MICROSERVICIO_REGISTRO=http://localhost:8001

entrar a la carpeta db y ejecutar
alembic upgrade head 

#### Startup
./start_services.sh

Los API calls se pueden hacer desde el navegador o desde Postman accediendo a la URL http://localhost:8000/<microservicio>

## Microservicios
Todos los requests tienen que ser enviados con una cookie de sesión de VEDI - 'vedi-token'
### Usuario
URL http://localhost:8000/usuario
GET - obtener usuarios: http://localhost:8000/usuario
GET - obtener usuario por id: http://localhost:8000/usuario/{id_usuario}
POST - crear usuario: http://localhost8000/usuario

### TipoNorma
URL http://localhost:8000/tipoNorma
POST - Crear un nuevo tipo de norma: http://localhost:8000/tipoNorma/crear
GET  - Obtener los tipoNorma http://localhost:8000/tipoNorma/get
GET  - Obtener un tipoNorma por su Id http://localhost:8000/tipoNorma/get/:tipoNormaId
PUT  - Modificar un tipoNorma por su Id http://localhost:8000/tipoNorma/update/:tipoNormaId
DELETE - Modificar el estado activo a False de un tipoNorma por su Id http://localhost:8000/tipoNorma/delete/:tipoNormaId

### Norma
URL http://localhost:8000/norma
POST - Crear una nueva norma: http://localhost:8000/norma/crear
GET - Obtener todas las normas: http://localhost:8000/norma/get?pagina=1&cantidad_filas=10
GET - Obtener una norma por su Id: http://localhost:8000/norma/get/:normaId
PUT - Modificar una norma por su Id: http://localhost:8000/norma/update/:normaId
DELETE - Modificar el estado activo a False de una norma por su Id: http://localhost:8000/norma/delete/:normaId

### HistorialEstadoExpediente
URL http://localhost:8000/historialEstadoExpediente
GET - Obtener todos los historialEstadoExpediente segun parametros: http://localhost:8000/historialEstadoExpediente/filter?expedienteId=1&estadoId=1

### Permiso
URL http://localhost:8000/permiso
POST - Crear un nuevo permiso: http://localhost:8000/permiso/crear
GET  - Obtener los permiso http://localhost:8000/permiso
GET  - Obtener un permiso por su Id http://localhost:8000/permiso/{idPermiso}
PUT  - Modificar un permiso por su Id http://localhost:8000/permiso/{idPermiso}
DELETE - Eliminar un permiso por su Id http://localhost:8000/permiso/{idPermiso}
- json para post y put:
{
    "nombrePermiso": "Eliminar",
    "descripcionPermiso": "Permiso que permite eliminar documentos al usuario",
    "activo": true
}

### Expediente
URL http://localhost:8000/expediente
POST - Crear un nuevo expediente: http://localhost:8000/expediente

Para el POST el JSON que se utiliza es el siguiente:

{ "expedientePadreId": null,
    "visibilidadExpediente": "Público",
    "areaIniciadoraId": 1,
    "usuarioCreadorId": 12345,
    "temaNombre": "Consulta General",
    "tramiteId": 1,
    "usuarioAplicacionId": 1,
    "sirad": {
        "IdTema": 1,
        "IniciadorPersonaJuridica": {
            "Cuit": "20-12345678-9",
            "RazonSocial": "Empresa S.A.",
            "Sucursal": {
                "NomenclaturaCatastral": "123456",
                "Representante": {
                    "Sexo": "F",
                    "Nombre": "Ana",
                    "Apellido": "Gómez",
                    "NroDocumento": "87654321"
                }
            }
        },
        "IniciadorPersonaFisica": null,
        "Asunto": "Solicitud de Información",
        "Observaciones": "Requiere atención inmediata"
    }
}

De igual manera, no se debe mandar como raw en POSTMAN, sino que, se debe ir a body, form-data y allí en la columna "Key" debemos poner dos tuplas
La primera, debe decir jsonData, y en la columna "value" se le debe pasar el JSON que insertamos arriba.
La segunda, debe decir files, y en la columna "value" se debe insertar algun archivo (actualmente de formato PDF). 

GET  - Obtener los expediente http://localhost:8000/expediente
GET  - Obtener un expediente por su Id http://localhost:8000/expediente/{idExpediente}
PUT  - Modificar un expediente por su Id http://localhost:8000/expediente/{idExpediente}
DELETE - Eliminar un expediente por su Id http://localhost:8000/expediente/{idExpediente}

{
    "tipoExpedienteId": 1,
    "numeroExpediente": "EXP-2024-011233",
    "usuarioCreadorId": 1,
    "fechaCreacion": "2024-10-25T12:41:02.008837",
    "fechaUltimoMovimiento": "2024-10-25T07:00:00",
    "activo": true,
    "hashTabla": "0cf9f7e0a097cff0af3636f49eefffb7cf690bc70682dc1ccb5d4d7fda1e1563",
    "expedienteId": 3,
    "expedientePadreId": 1,
    "areaIniciadoraId": 2,
    "asuntoExpediente": "Asunto del expediente mi idea",
    "visibilidadExpediente": "Privada"
}

### Movimiento
URL http://localhost:8000/movimiento
POST - Crear un nuevo movimiento: http://localhost:8000/movimiento

Para el POST el JSON que se utiliza es el siguiente:

{
    "tramiteId": 1,
    "numeroExpediente": "EXP-161-2024-1",
    "usuarioAplicacionId": 1,
    "areaIniciadoraId": 2,
    "usuarioOrigenId": 2,
    "areaDestinoId": 2,
    "observacionMovimiento": "Observaciones sobre el movimiento"
}

De igual manera, no se debe mandar como raw en POSTMAN, sino que, se debe ir a body, form-data y allí en la columna "Key" debemos poner dos tuplas
La primera, debe decir jsonData, y en la columna "value" se le debe pasar el JSON que insertamos arriba.
La segunda, debe decir files, y en la columna "value" se debe insertar algun archivo (actualmente de formato PDF). 

GET  - Obtener los movimiento http://localhost:8000/movimiento
GET  - Obtener un movimiento por su Id http://localhost:8000/movimiento/{idMovimiento}
PUT  - Modificar un movimiento por su Id http://localhost:8000/movimiento/{idMovimiento}


### TipoExpediente
URL http://localhost:8000/tipoExpediente
POST - Crear un nuevo tipoExpediente: http://localhost:8000/tipoExpediente
GET  - Obtener los tipoExpediente http://localhost:8000/tipoExpediente
GET  - Obtener un tipoExpediente por su Id http://localhost:8000/tipoExpediente/{idTipoExpediente}
PUT  - Modificar un tipoExpediente por su Id http://localhost:8000/tipoExpediente/{idTipoExpediente}
DELETE - Eliminar un tipoExpediente por su Id http://localhost:8000/tipoExpediente/{idTipoExpediente}

{
  "tipoExpedienteId": 3,
  "nombreTipoExpediente": "Prueba",
  "descripcionTipoExpediente": "Prueba",
  "activo": true
}


## Test
Comando para ejecutar todos los test:
- pytest -v -s
    ó
- python -m pytest -v -s

Comando para ejecutar un test especifico:
- pytest .\test_expedienteRouter.py -v -s
    ó
- python -m pytest .\test_expedienteRouter.py -v -s