Proceso EvaluacionDocente

    Definir encuestaCompleta, desempenioEsperado Como Logico

    Escribir "===================================================="
    Escribir "   SISTEMA DE EVALUACION DOCENTE - INICIO DEL PROCESO"
    Escribir "===================================================="

    // 1. Planificacion de la evaluacion
    Escribir "Se planifica la evaluacion docente"

    // 2. Comunicacion del proceso al docente
    Escribir "Se comunica al docente sobre el proceso de evaluacion"

    // 3-4. Aplicacion de la encuesta y decision
    Escribir "Los estudiantes responden la encuesta de evaluacion docente"
    Escribir "¿La encuesta se completo con exito? (Verdadero/Falso)"
    Leer encuestaCompleta

    Si NO encuestaCompleta Entonces
        Escribir "Se solicita a los estudiantes completar nuevamente la encuesta"
    FinSi

    // 5. Recoleccion de las respuestas
    Escribir "Se recolectan las respuestas"

    // 6. Revision y analisis
    Escribir "Se revisan y analizan las respuestas"
    Escribir "Se identifican fortalezas y debilidades"

    // 7. Decision de desempeño
    Escribir "¿El desempeño del docente fue el esperado? (Verdadero/Falso)"
    Leer desempenioEsperado

    Si desempenioEsperado Entonces
        Escribir "Se recompensa al profesor por su buen desempeño en las actividades docentes"
    SiNo
        Escribir "Se realiza una reunion para hacer un plan de mejora para el docente"
    FinSi

    // 8. Convergencia: entrega del informe
    Escribir "Se le entrega al docente el informe en donde recalca sus fortalezas y debilidades (con observaciones y sugerencias)"

    // 9. Bloque final de seguimiento (Caja unica del diagrama)
    Escribir "Se realiza seguimiento al docente y se observa si en caso de no cumplir las expectativas hablar con el y darle retroalimentacion, si las cumple felicitarlo y darle recompensa"

    Escribir "===================================================="
    Escribir "   FIN DEL PROCESO DE EVALUACION DOCENTE"
    Escribir "===================================================="

FinProceso