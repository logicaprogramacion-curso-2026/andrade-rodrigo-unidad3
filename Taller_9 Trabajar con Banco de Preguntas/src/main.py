import os
from dao import PreguntaDAO
from gestor import GestorPreguntas
from simulador import Simulador

def mostrar_menu():
    print("\n" + "="*40)
    print(" 📚 SISTEMA GESTOR DE PREGUNTAS Y EVALUACIÓN")
    print("="*40)
    print("1. Cargar preguntas desde archivo (TXT, CSV, JSON)")
    print("2. Ver todas las preguntas guardadas")
    print("3. Ver estadísticas del banco de preguntas")
    print("4. Iniciar simulación de evaluación")
    print("5. Exportar datos desde SQLite")
    print("6. Salir")
    return input("Seleccione una opción: ").strip()

def main():
    dao = PreguntaDAO()
    gestor = GestorPreguntas(dao)
    simulador = Simulador(dao)

    while True:
        opc = mostrar_menu()
        if opc == '1':
            print("\nFormatos disponibles: 1. TXT | 2. CSV | 3. JSON")
            fmt = input("Seleccione formato: ").strip()
            try:
                if fmt == '1':
                    preguntas = gestor.cargar_desde_txt("preguntas.txt")
                elif fmt == '2':
                    preguntas = gestor.cargar_desde_csv("preguntas.csv")
                elif fmt == '3':
                    preguntas = gestor.cargar_desde_json("preguntas.json")
                else:
                    print("⚠️ Opción no válida.")
                    continue
                
                gestor.guardar_en_base_datos(preguntas)
                print(f"✅ Se cargaron e insertaron {len(preguntas)} preguntas en SQLite.")
            except Exception as e:
                print(f"❌ Error al cargar archivo: {e}")

        elif opc == '2':
            preguntas = dao.obtener_todas()
            print(f"\n--- Banco actual: {len(preguntas)} preguntas ---")
            for p in preguntas:
                print(p)
                print("-" * 30)

        elif opc == '3':
            print("\n--- Estadísticas del Banco ---")
            print(f"Total Preguntas: {dao.contar_preguntas()}")
            print("Por Tema:", dao.estadisticas_por_tema())
            print("Por Dificultad:", dao.estadisticas_por_dificultad())

        elif opc == '4':
            cant = input("¿Cuántas preguntas desea responder?: ").strip()
            if cant.isdigit():
                simulador.iniciar_simulacion(int(cant))
            else:
                print("⚠️ Ingrese un número válido.")

        elif opc == '5':
            gestor.exportar_a_txt()
            gestor.exportar_a_csv()
            gestor.exportar_a_json()
            print("✅ Datos exportados en carpeta 'resultados/' (TXT, CSV, JSON).")

        elif opc == '6':
            print("¡Hasta luego!")
            break
        else:
            print("⚠️ Opción inválida.")

if __name__ == "__main__":
    main()