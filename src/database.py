
import sqlite3
import os

from .modelos import Tarea, proyecto


DATABASE_NAME = 'tareas.db'


def get_conection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def crear_tablas():
    conn = get_conection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS proyectos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                fecha_inicio TEXT,
                estado TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                fecha_creacion TEXT,
                fecha_limite TEXT,
                prioridad TEXT,
                estado TEXT,
                proyecto_id INTEGER,
                FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
            )
        """)

        cursor.execute("""
            INSERT OR IGNORE INTO proyectos
            (id, nombre, descripcion, estado)
            VALUES (
                0,
                'Tareas generales',
                'Tareas sin clasificar',
                'Activo'
            )
        """)

        conn.commit()

    finally:
        conn.close()


class DBManager:

    def __init__(self):
        crear_tablas()

    def crear_tarea(self, tarea: Tarea) -> Tarea:

        conn = get_conection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO tareas (
                    titulo,
                    descripcion,
                    fecha_creacion,
                    fecha_limite,
                    prioridad,
                    estado,
                    proyecto_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                tarea._titulo,
                tarea._descripcion,
                tarea._fecha_creacion,
                tarea._fecha_limite,
                tarea._prioridad,
                tarea._estado,
                tarea._proyecto_id
            ))

            conn.commit()

            tarea.id = cursor.lastrowid

            return tarea

        finally:
            conn.close()

    def obtener_proyectos(self):

        conn = get_conection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM proyectos")
            filas = cursor.fetchall()

            proyectos = []

            for fila in filas:

                p = proyecto(
                    nombre=fila['nombre'],
                    descripcion=fila['descripcion'],
                    id=fila['id'],
                    estado=fila['estado'],
                    fecha_inicio=fila['fecha_inicio']
                )

                proyectos.append(p)

            return proyectos

        finally:
            conn.close()

    def obtener_tareas(self, estado=None):

        conn = get_conection()
        cursor = conn.cursor()

        try:
            sql = "SELECT * FROM tareas"
            params = []

            if estado:
                sql += " WHERE estado = ?"
                params.append(estado)

            sql += " ORDER BY fecha_limite ASC"

            cursor.execute(sql, params)
            filas = cursor.fetchall()

            tareas = []

            for fila in filas:

                t = Tarea(
                    titulo=fila['titulo'],
                    descripcion=fila['descripcion'],
                    fecha_creacion=fila['fecha_creacion'],
                    fecha_limite=fila['fecha_limite'],
                    prioridad=fila['prioridad'],
                    estado=fila['estado'],
                    proyecto_id=fila['proyecto_id'],
                    id=fila['id']
                )

                tareas.append(t)

            return tareas

        finally:
            conn.close()


if __name__ == '__main__':

    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        print(f"Base de datos {DATABASE_NAME} eliminada.")

    crear_tablas()

    print("Base de datos correctamente creada")

    manager = DBManager()

    tarea_prueba = Tarea(
        titulo="Completar Ejercicio de CRUD",
        fecha_limite="2026-11-30",
        prioridad="Alta",
        proyecto_id=0,
        descripcion="Implementar el módulo database.py"
    )

    tarea_creada = manager.crear_tarea(tarea_prueba)

    print(f"Tarea creada y ID asignado: {tarea_creada.id}")

    print("Tareas registradas:")

    for tarea in manager.obtener_tareas():
        print(tarea.to_dict())
