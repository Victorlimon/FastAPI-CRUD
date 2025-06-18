from fastapi import APIRouter,UploadFile , Depends, HTTPException, status, Response
import openpyxl
import pandas as pd
from pydantic import BaseModel
from datetime import date
from typing import Annotated
from models.usuario import Usuario
from typing import Optional
from io import BytesIO
from services.usuario import UsuarioService
from enum import Enum
from core.dependencies import get_current_user_admin

router = APIRouter(tags=["upload"], prefix="/upload")
service = UsuarioService()

data_list = []

class dataframe(BaseModel):
    nombre: str
    apellido: str
    edad: int


class EmpleadoCreate(BaseModel):
    codigo_empleado: str
    nombres: str
    apellidos: str
    cedula_iden: str
    celular: Optional[str]
    fecha_nac: Optional[date]
    area: str

class MotorizadoCreate(BaseModel):
    grupo_sanguineo: Optional[str]
    garantia: Optional[str]
    numero_emer: Optional[str]
    familiar_emer: Optional[str]
    direccion: Optional[str]
    enlace_direccion: Optional[str]

class MotorizadoResponse(BaseModel):
    id: int
    empleado_id: int
    grupo_sanguineo: Optional[str]




@router.post("/upload-db-excel/")
async def create_upload_file(
    file: UploadFile,
    current_user:  Annotated[Usuario, Depends(get_current_user_admin)]
    ):

    if not file.filename.endswith(('.xlsx', 'xls', '.xlsm')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Formato inválido. Solo se aceptan archivos Excel (.xlsx, .xls, .xlsm)"
        )
    
    try:
        wb = openpyxl.load_workbook(file.file)
        datos = wb.active
        
        #cabezera_datos = ["nombre", "apellido", "edad"] # Caebecera de datos definidos y esperados en el archivo excel
        cabezera_datos = ["usuario", "nombre_completo", "correo", "contrasenia", "telefono", "rol", "activo"]
        primera_fila = [cell.value for cell in datos[1]] # Se obtiene la primera fila del archivo que son las cabeceras
        if primera_fila != cabezera_datos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo debe contener las cabeceras: " + ", ".join(cabezera_datos)
            )
            
        data = []
        
        for row in datos.iter_rows(min_row=2, values_only=True):
            data.append(row)
        
        df = pd.DataFrame(data, columns=["nombre", "apellido", "edad"])
        # Limpieza con pandas
        df = df.dropna()
        
        datos = df.to_dict(orient="records")  # Convertir DataFrame a lista de diccionarios
        validated_data = [dataframe(**item).dict() for item in datos]
        data_list.extend(validated_data)
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Archivo procesado exitosamente"
        )
        
    except Exception as e:
        return str(e)


@router.get("/download-db-excel/")
async def download_database_excel(
    current_user:  Annotated[Usuario, Depends(get_current_user_admin)]    
    ):
    
    datos_db = await service.get_all_users()
    
    # Verificar y convertir los datos a DataFrame
    if not datos_db:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="no hay datos para descargar"
        )
    
    datos = [{
        "username": db.username,
        "full_name": db.full_name,
        "email": db.email,
        "telefono": db.telefono,
        "rol": db.rol,
        "activo": db.activo
    }for db in datos_db]
    
    df = pd.DataFrame(datos)
    df["activo"] = df["activo"].astype(str)
    # Esta línea limpia solo la columna 'rol'
    df["rol"] = df["rol"].apply(lambda x: x.value if isinstance(x, Enum) else x)
    
    output = BytesIO() # Crear un un espacio en memoria
    
    # Crear el Excel
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Datos', index=False)
        
    output.seek(0)
    
    headers = {
            "Content-Disposition": "attachment; filename=exportacion_datos.xlsx",
            "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        }
    
    return Response(content=output.read() ,headers=headers, media_type=headers["Content-Type"])





"""

CREATE TYPE rol_usuario AS ENUM ('cliente', 'motorizado', 'admin', 'restaurante');


CREATE TABLE Usuario (
    id SERIAL PRIMARY KEY,
    codigo_empleado VARCHAR(30) UNIQUE NOT NULL, -- ej: MOTORIZADO-001
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    cedula_iden VARCHAR(20) UNIQUE NOT NULL,
    celular VARCHAR(20),
    fecha_nac DATE,
    area VARCHAR(50), -- ejemplo: motorizado, sistemas, marketing
    fecha_ingreso DATE DEFAULT NOW(),
    activo BOOLEAN DEFAULT TRUE
);


CREATE TABLE motorizado (
    empleado_id INTEGER PRIMARY KEY REFERENCES empleados(id) ON DELETE CASCADE,
    grupo_sanguineo VARCHAR(10),
    garantia TEXT,
    numero_emer VARCHAR(20),
    familiar_emer VARCHAR(100),
    barrio VARCHAR(100),
    calle_avenida VARCHAR(100),
    numero_direccion VARCHAR(20),
    enlace_direccion VARCHAR(60)
);

INSERT INTO empleados (codigo_empleado, nombres, apellidos, cedula_iden, celular, fecha_nac, area)
VALUES
('MOT-001', 'Juan', 'Pérez', '12345678', '789654321', '1990-05-12', 'motorizado'),
('MOT-002', 'Luis', 'Ramírez', '87654321', '789321654', '1988-09-25', 'motorizado');


INSERT INTO motorizado (
    empleado_id, grupo_sanguineo, garantia, numero_emer,
    familiar_emer, barrio, calle_avenida, numero_direccion, enlace_direccion
)
VALUES
(1, 'O+', 'Moto en prenda', '777111222', 'Ana Pérez', 'Villa Fátima', 'Av. Principal', '45B', 'ubicacion_enalce'),
(2, 'A-', 'Documento de propiedad', '777333444', 'Carlos Ramírez', 'Zona Sur', 'Calle 12', 'Nro 8', 'ubicacion_enalce');

SELECT 
    e.id,
    e.codigo_empleado,
    e.nombres,
    e.apellidos,
    e.cedula_iden,
    e.celular,
    e.fecha_nac,
    e.area,
    m.grupo_sanguineo,
    m.garantia,
    m.numero_emer,
    m.familiar_emer,
    m.barrio,
    m.calle_avenida,
    m.numero_direccion,
    m.enlace_direccion
FROM motorizado m
JOIN empleados e ON m.empleado_id = e.id;


"""