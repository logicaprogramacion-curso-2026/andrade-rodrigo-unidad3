import csv
import json
from entidad import Pregunta
from dao import PreguntaDAO

class GestorPreguntas:
    def __init__(self, dao: PreguntaDAO = None):
        self.dao = dao or PreguntaDAO()

    def cargar_desde_txt(self, ruta="preguntas.txt"):
        preguntas = []
        with open(ruta, 'r', encoding='utf-8') as f:
            lineas = [l.strip() for l in f if l.strip()]
            for linea in lineas:
                p = linea.split('|')
                if len(p) == 8:
                    preguntas.append(Pregunta(None, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7]))
        return preguntas

    def cargar_desde_csv(self, ruta="preguntas.csv"):
        preguntas = []
        with open(ruta, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                preguntas.append(Pregunta(
                    None, row['pregunta'], row['opcion_a'], row['opcion_b'],
                    row['opcion_c'], row['opcion_d'], row['respuesta_correcta'],
                    row['dificultad'], row['tema']
                ))
        return preguntas

    def cargar_desde_json(self, ruta="preguntas.json"):
        preguntas = []
        with open(ruta, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                preguntas.append(Pregunta(
                    item.get('id'), item['pregunta'], item['opcion_a'], item['opcion_b'],
                    item['opcion_c'], item['opcion_d'], item['respuesta_correcta'],
                    item['dificultad'], item['tema']
                ))
        return preguntas

    def guardar_en_base_datos(self, preguntas):
        self.dao.insertar_muchas(preguntas)

    def exportar_a_txt(self, ruta="resultados/preguntas_exportadas.txt"):
        preguntas = self.dao.obtener_todas()
        with open(ruta, 'w', encoding='utf-8') as f:
            for p in preguntas:
                f.write(f"{p.pregunta}|{p.opcion_a}|{p.opcion_b}|{p.opcion_c}|{p.opcion_d}|{p.respuesta_correcta}|{p.dificultad}|{p.tema}\n")

    def exportar_a_csv(self, ruta="resultados/preguntas_exportadas.csv"):
        preguntas = self.dao.obtener_todas()
        fieldnames = ["id", "pregunta", "opcion_a", "opcion_b", "opcion_c", "opcion_d", "respuesta_correcta", "dificultad", "tema"]
        with open(ruta, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for p in preguntas:
                writer.writerow(p.to_dict())

    def exportar_a_json(self, ruta="resultados/preguntas_exportadas.json"):
        preguntas = self.dao.obtener_todas()
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump([p.to_dict() for p in preguntas], f, indent=4, ensure_ascii=False)