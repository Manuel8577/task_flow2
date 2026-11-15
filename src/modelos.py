
from datetime import datetime


class proyecto:

    def __init__(
        self,
        nombre: str,
        descripcion: str = "",
        id: int = None,
        estado: str = "Activo",
        fecha_inicio: str = None
    ):
        self._id = id
        self._nombre = nombre
        self._descripcion = descripcion

        self._fecha_inicio = (
            fecha_inicio if fecha_inicio
            else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        self._estado = estado

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    def to_dict(self):
        return {
            'id': self._id,
            'nombre': self._nombre,
            'descripcion': self._descripcion,
            'fecha_inicio': self._fecha_inicio,
            'estado': self._estado
        }


class Tarea:

    def __init__(
        self,
        titulo: str,
        fecha_limite: str,
        prioridad: str,
        proyecto_id: int,
        descripcion: str,
        id: int = None,
        estado: str = "pendiente",
        fecha_creacion: str = None
    ):

        self._id = id
        self._titulo = titulo
        self._descripcion = descripcion

        self._fecha_creacion = (
            fecha_creacion if fecha_creacion
            else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        self._fecha_limite = fecha_limite
        self._prioridad = prioridad
        self._estado = estado
        self._proyecto_id = proyecto_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    def marcar_como_completada(self):
        if self._estado != "completada":
            self._estado = "completada"
            return True

        return False

    def to_dict(self):
        return {
            'id': self._id,
            'titulo': self._titulo,
            'descripcion': self._descripcion,
            'fecha_creacion': self._fecha_creacion,
            'fecha_limite': self._fecha_limite,
            'prioridad': self._prioridad,
            'estado': self._estado,
            'proyecto_id': self._proyecto_id
        }
