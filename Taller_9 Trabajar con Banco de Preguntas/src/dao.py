import sqlite3
from entidad import Pregunta

class PreguntaDAO:
    def __init__(self, db_path="database/preguntas.db"):
        self.db_path = db_path
        self.crear_tabla()

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def crear_tabla(self):
        query = """
        CREATE TABLE IF NOT EXISTS preguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta TEXT NOT NULL,
            opcion_a TEXT NOT NULL,
            opcion_b TEXT NOT NULL,
            opcion_c TEXT NOT NULL,
            opcion_d TEXT NOT NULL,
            respuesta_correcta TEXT NOT NULL,
            dificultad TEXT NOT NULL,
            tema TEXT NOT NULL
        );
        """
        with self._conectar() as conn:
            conn.execute(query)

    def insertar(self, pregunta: Pregunta):
        query = """
        INSERT INTO preguntas (pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta, dificultad, tema)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                pregunta.pregunta, pregunta.opcion_a, pregunta.opcion_b,
                pregunta.opcion_c, pregunta.opcion_d, pregunta.respuesta_correcta,
                pregunta.dificultad, pregunta.tema
            ))
            pregunta.id = cursor.lastrowid
            return pregunta.id

    def insertar_muchas(self, preguntas):
        datos = [
            (p.pregunta, p.opcion_a, p.opcion_b, p.opcion_c, p.opcion_d, p.respuesta_correcta, p.dificultad, p.tema)
            for p in preguntas
        ]
        query = """
        INSERT INTO preguntas (pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta, dificultad, tema)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, datos)
            conn.commit()

    def obtener_todas(self):
        query = "SELECT id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta, dificultad, tema FROM preguntas"
        with self._conectar() as conn:
            cursor = conn.cursor()
            rows = cursor.execute(query).fetchall()
            return [Pregunta(*row) for row in rows]

    def obtener_por_id(self, id_pregunta):
        query = "SELECT id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta, dificultad, tema FROM preguntas WHERE id = ?"
        with self._conectar() as conn:
            cursor = conn.cursor()
            row = cursor.execute(query, (id_pregunta,)).fetchone()
            return Pregunta(*row) if row else None

    def obtener_por_tema(self, tema):
        query = "SELECT id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta, dificultad, tema FROM preguntas WHERE LOWER(tema) = LOWER(?)"
        with self._conectar() as conn:
            cursor = conn.cursor()
            rows = cursor.execute(query, (tema,)).fetchall()
            return [Pregunta(*row) for row in rows]

    def obtener_por_dificultad(self, dificultad):
        query = "SELECT id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta, dificultad, tema FROM preguntas WHERE LOWER(dificultad) = LOWER(?)"
        with self._conectar() as conn:
            cursor = conn.cursor()
            rows = cursor.execute(query, (dificultad,)).fetchall()
            return [Pregunta(*row) for row in rows]

    def actualizar(self, pregunta: Pregunta):
        query = """
        UPDATE preguntas
        SET pregunta=?, opcion_a=?, opcion_b=?, opcion_c=?, opcion_d=?, respuesta_correcta=?, dificultad=?, tema=?
        WHERE id=?
        """
        with self._conectar() as conn:
            conn.execute(query, (
                pregunta.pregunta, pregunta.opcion_a, pregunta.opcion_b,
                pregunta.opcion_c, pregunta.opcion_d, pregunta.respuesta_correcta,
                pregunta.dificultad, pregunta.tema, pregunta.id
            ))

    def eliminar(self, id_pregunta):
        query = "DELETE FROM preguntas WHERE id = ?"
        with self._conectar() as conn:
            conn.execute(query, (id_pregunta,))

    def contar_preguntas(self):
        query = "SELECT COUNT(*) FROM preguntas"
        with self._conectar() as conn:
            return conn.cursor().execute(query).fetchone()[0]

    def estadisticas_por_tema(self):
        query = "SELECT tema, COUNT(*) FROM preguntas GROUP BY tema"
        with self._conectar() as conn:
            return dict(conn.cursor().execute(query).fetchall())

    def estadisticas_por_dificultad(self):
        query = "SELECT dificultad, COUNT(*) FROM preguntas GROUP BY dificultad"
        with self._conectar() as conn:
            return dict(conn.cursor().execute(query).fetchall())