import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from entidad import Pregunta

class TestPregunta(unittest.TestCase):
    def test_creacion_y_formato(self):
        p = Pregunta(1, "¿Qué es Python?", "Lenguaje", "Serpiente", "Auto", "Fruta", "A", "Fácil", "Básicos")
        self.assertEqual(p.respuesta_correcta, "A")
        self.assertEqual(p.dificultad, "Fácil")
        self.assertIsInstance(p.to_dict(), dict)

if __name__ == '__main__':
    unittest.main()