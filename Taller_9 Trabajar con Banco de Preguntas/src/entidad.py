class Pregunta:
    def __init__(self, id_pregunta, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta, dificultad, tema):
        self.id = int(id_pregunta) if id_pregunta is not None else None
        self.pregunta = str(pregunta).strip()
        self.opcion_a = str(opcion_a).strip()
        self.opcion_b = str(opcion_b).strip()
        self.opcion_c = str(opcion_c).strip()
        self.opcion_d = str(opcion_d).strip()
        self.respuesta_correcta = str(respuesta_correcta).strip().upper()
        self.dificultad = str(dificultad).strip().capitalize()
        self.tema = str(tema).strip()

    def to_dict(self):
        return {
            "id": self.id,
            "pregunta": self.pregunta,
            "opcion_a": self.opcion_a,
            "opcion_b": self.opcion_b,
            "opcion_c": self.opcion_c,
            "opcion_d": self.opcion_d,
            "respuesta_correcta": self.respuesta_correcta,
            "dificultad": self.dificultad,
            "tema": self.tema
        }

    def __str__(self):
        return (f"[{self.id}] ({self.tema} - {self.dificultad}) {self.pregunta}\n"
                f"  A) {self.opcion_a}\n  B) {self.opcion_b}\n"
                f"  C) {self.opcion_c}\n  D) {self.opcion_d}")