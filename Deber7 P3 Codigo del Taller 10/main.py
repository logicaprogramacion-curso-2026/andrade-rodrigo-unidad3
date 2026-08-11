"""
Taller 10 - Sistema de Evaluación Docente
Código en Python desarrollado a partir del pseudocódigo del Deber 6.

Estudiante: Rodrigo Alejandro Andrade Espinoza
Curso: 1er Semestre, Paralelo "A" - Sistemas
Materia: Lógica de Programación
Docente: Ing. Samuel Ojeda
"""


def leer_booleano(mensaje: str) -> bool:
    """Solicita al usuario una respuesta V/F y la valida hasta obtener un dato correcto."""
    while True:
        respuesta = input(f"{mensaje} (V/F): ").strip().upper()
        if respuesta in ("V", "VERDADERO", "S", "SI"):
            return True
        if respuesta in ("F", "FALSO", "N", "NO"):
            return False
        print("Entrada no válida. Escriba V (verdadero) o F (falso).")


def planificar_evaluacion() -> None:
    print("Se planifica la evaluación docente")


def comunicar_docente() -> None:
    print("Se comunica al docente sobre el proceso de evaluación")


def aplicar_encuesta() -> bool:
    """Simula la aplicación de la encuesta y devuelve si se completó con éxito."""
    print("Los estudiantes responden la encuesta de evaluación docente")
    return leer_booleano("¿La encuesta se completó con éxito?")


def recolectar_respuestas() -> None:
    print("Se recolectan las respuestas")


def analizar_respuestas() -> None:
    print("Se revisan y analizan las respuestas")
    print("Se identifican fortalezas y debilidades del docente")


def evaluar_desempenio() -> bool:
    return leer_booleano("¿El desempeño del docente fue el esperado?")


def recompensar_docente() -> None:
    print("Se recompensa al profesor por su buen desempeño en las actividades docentes")


def planificar_mejora() -> None:
    print("Se realiza una reunión para elaborar un plan de mejora para el docente")


def entregar_informe() -> None:
    print("Se entrega al docente el informe con sus fortalezas y debilidades")
    print("El informe incluye observaciones y sugerencias")


def realizar_seguimiento() -> bool:
    print("Se realiza seguimiento al docente")
    return leer_booleano("En el seguimiento, ¿el docente cumple las expectativas?")


def dar_retroalimentacion() -> None:
    print("Se habla con el docente y se le da retroalimentación")


def felicitar_docente() -> None:
    print("Se felicita al docente y se le otorga una recompensa")


def main() -> None:
    print("=" * 55)
    print("   SISTEMA DE EVALUACIÓN DOCENTE - INICIO DEL PROCESO")
    print("=" * 55)

    # 1-2. Preparación
    planificar_evaluacion()
    comunicar_docente()

    # 3-4. Aplicación de la encuesta (se repite hasta completarse con éxito)
    encuesta_completa = False
    while not encuesta_completa:
        encuesta_completa = aplicar_encuesta()
        if not encuesta_completa:
            print("Se solicita a los estudiantes completar nuevamente la encuesta")

    # 5-6. Recolección y análisis
    recolectar_respuestas()
    analizar_respuestas()

    # 7. Decisión sobre el desempeño
    if evaluar_desempenio():
        recompensar_docente()
    else:
        planificar_mejora()

    # 8. Entrega del informe (punto de convergencia de ambas ramas)
    entregar_informe()

    # 9. Seguimiento y decisión final
    if realizar_seguimiento():
        felicitar_docente()
    else:
        dar_retroalimentacion()

    print("=" * 55)
    print("   FIN DEL PROCESO DE EVALUACIÓN DOCENTE")
    print("=" * 55)


if __name__ == "__main__":
    main()
