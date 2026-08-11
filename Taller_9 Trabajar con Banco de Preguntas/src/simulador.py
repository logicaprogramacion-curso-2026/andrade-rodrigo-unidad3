import random
import os
import json
import csv
from datetime import datetime
from dao import PreguntaDAO

class Simulador:
    def __init__(self, dao: PreguntaDAO = None):
        self.dao = dao or PreguntaDAO()

    def iniciar_simulacion(self, cantidad=5):
        todas = self.dao.obtener_todas()
        if not todas:
            print("⚠️ No hay preguntas registradas en la base de datos.")
            return

        cantidad = min(cantidad, len(todas))
        preguntas_seleccionadas = random.sample(todas, cantidad)

        respuestas_usuario = []
        aciertos = 0

        print("\n=== 📝 INICIO DE EVALUACIÓN SIMULADA ===")
        for idx, p in enumerate(preguntas_seleccionadas, 1):
            print(f"\nPregunta {idx}/{cantidad}:")
            print(p)
            resp = self.validar_respuesta()
            es_correcta = (resp == p.respuesta_correcta)
            if es_correcta:
                aciertos += 1
                print("✨ ¡Correcto!")
            else:
                print(f"❌ Incorrecto. La opción correcta era: {p.respuesta_correcta}")

            respuestas_usuario.append({
                "pregunta_id": p.id,
                "enunciado": p.pregunta,
                "tema": p.tema,
                "dificultad": p.dificultad,
                "respuesta_dada": resp,
                "respuesta_correcta": p.respuesta_correcta,
                "es_correcta": es_correcta
            })

        puntaje = (aciertos / cantidad) * 10
        print(f"\n🎯 Resultado Final: {aciertos}/{cantidad} aciertos | Puntaje: {puntaje:.2f}/10")
        self.generar_reportes(respuestas_usuario, puntaje)

    def validar_respuesta(self):
        while True:
            resp = input("Tu respuesta (A, B, C, D): ").strip().upper()
            if resp in ['A', 'B', 'C', 'D']:
                return resp
            print("⚠️ Entrada inválida. Ingrese únicamente A, B, C o D.")

    def generar_reportes(self, respuestas, puntaje):
        os.makedirs("resultados", exist_ok=True)
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 1. Archivo TXT
        with open("resultados/respuestas_usuario.txt", "w", encoding="utf-8") as f:
            f.write(f"REPORTE DE EVALUACIÓN - {fecha_hora}\n")
            f.write(f"Puntaje Final: {puntaje:.2f}/10\n\n")
            for r in respuestas:
                estado = "CORRECTO" if r['es_correcta'] else "INCORRECTO"
                f.write(f"ID: {r['pregunta_id']} | {r['enunciado']}\n")
                f.write(f"Tu respuesta: {r['respuesta_dada']} | Correcta: {r['respuesta_correcta']} -> {estado}\n\n")

        # 2. Archivo CSV
        with open("resultados/estadisticas.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Fecha", "PreguntaID", "Tema", "Dificultad", "Correcta"])
            for r in respuestas:
                writer.writerow([fecha_hora, r['pregunta_id'], r['tema'], r['dificultad'], r['es_correcta']])

        # 3. Archivo JSON
        reporte_json = {
            "fecha": fecha_hora,
            "puntaje_sobre_10": round(puntaje, 2),
            "total_preguntas": len(respuestas),
            "detalles": respuestas
        }
        with open("resultados/reporte.json", "w", encoding="utf-8") as f:
            json.dump(reporte_json, f, indent=4, ensure_ascii=False)

        print("📊 Reportes generados exitosamente en la carpeta 'resultados/'.")