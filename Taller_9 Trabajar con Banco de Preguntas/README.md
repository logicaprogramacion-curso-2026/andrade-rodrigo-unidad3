# 📚 Sistema de Preguntas y Respuestas - Taller 9

## 👥 Integrantes del Grupo
- Rodrigo Andrade - Systems Engineering
- Dylan Santillán - Systems Engineering

## 📅 Fechas
- Inicio: 27/07/2026
- Entrega: 03/08/2026

## 📝 Descripción del Proyecto
Sistema desarrollado en Python para la gestión integral de un banco de preguntas con soporte para entrada/salida multi-archivo (TXT, CSV, JSON), persistencia relacional en SQLite y simulación interactiva de evaluaciones.

---

## 📊 Evidencias de Ejecución por Iteración

### Iteración 1: Estructura Inicial
- Creación de entidades (`Pregunta`) y modularización base en `src/`.

### Iteración 2: Carga de Archivos Base
- Generación exitosa de 50 preguntas validadas en formatos `.txt`, `.csv` y `.json`.

### Iteración 3: Implementación del DAO
- Manejo de SQLite3 mediante patrón Data Access Object para operaciones CRUD complejas.

### Iteración 4 y 5: Gestor e Interacción
- Carga masiva de datos sin redundancia e implementación de consultas agregadas por tema y dificultad.

### Iteración 6 y 7: Simulador y Reportes
- Motor interactivo de evaluación con métricas de acierto y exportación automatizada de reportes estructurados a la carpeta `resultados/`.

### Iteración 8: Integración y Cobertura
- Pruebas unitarias construidas con la librería `unittest`.

---

## 🎯 Conclusiones
- Se logró una clara separación de responsabilidades aislando persistencia (`dao.py`), modelo (`entidad.py`), vista/controlador (`main.py`) y negocio (`gestor.py`/`simulador.py`).
- El uso de SQLite ofrece persistencia ligera y rápida sin depender de infraestructura externa.