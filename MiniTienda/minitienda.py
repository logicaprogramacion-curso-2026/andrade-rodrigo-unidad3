"""
MiniTienda - Registro y análisis de ventas
Lógica de Programación - UIDE

Estructuras usadas:
- Tuplas: cada producto del catálogo es una tupla (id, nombre, categoria)
- Diccionarios: precios y stock (clave = id_producto)
- Listas: catálogo (lista de tuplas) y buffer de ventas (lista de diccionarios)
- Pandas: DataFrame de ventas, groupby para ingresos por producto, lectura/escritura CSV
- NumPy: mean, std, sum sobre arreglos de ingresos/cantidades
- Matplotlib: gráfico de barras de ingresos por producto
"""

import os
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # backend sin ventana, para poder correr en consola/servidor
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------
# 1) CATÁLOGO (lista de tuplas) + PRECIOS / STOCK (diccionarios)
# --------------------------------------------------------------------------
# Cada producto es una tupla inmutable (id, nombre, categoria).
# El catálogo en sí es una lista para poder agregar nuevos productos (Reto A).
catalogo = [
    (1, "Laptop", "Cómputo"),
    (2, "Mouse", "Accesorios"),
    (3, "Teclado", "Accesorios"),
    (4, "Monitor", "Cómputo"),
    (5, "Audífonos", "Accesorios"),
]

precios = {1: 650.00, 2: 15.50, 3: 25.00, 4: 180.00, 5: 35.00}
stock = {1: 10, 2: 50, 3: 40, 4: 15, 5: 30}

# --------------------------------------------------------------------------
# 2) BUFFER DE VENTAS (lista) e IDs de venta
# --------------------------------------------------------------------------
ventas_buffer = []          # lista de diccionarios con cada venta registrada
_contador_id_venta = [0]    # lista usada como "referencia mutable" para el contador

ARCHIVO_VENTAS = "ventas.csv"
ARCHIVO_LOG = "log.txt"


# --------------------------------------------------------------------------
# FUNCIONES AUXILIARES
# --------------------------------------------------------------------------

def escribir_log(mensaje):
    """Escribe una línea con fecha/hora en log.txt (archivo)."""
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensaje}\n")


def buscar_producto(producto_id):
    """Busca un producto en el catálogo (list of tuples) por id. Retorna la tupla o None."""
    for producto in catalogo:
        if producto[0] == producto_id:
            return producto
    return None


def mostrar_catalogo():
    print("\n--- CATÁLOGO DE PRODUCTOS ---")
    print(f"{'ID':<4}{'Nombre':<15}{'Categoría':<15}{'Precio':<10}{'Stock':<6}")
    for producto in catalogo:
        pid, nombre, categoria = producto
        precio = precios.get(pid, 0)
        existencias = stock.get(pid, 0)
        print(f"{pid:<4}{nombre:<15}{categoria:<15}{precio:<10.2f}{existencias:<6}")


# --------------------------------------------------------------------------
# 3) RETO A: agregar producto nuevo / actualizar precio y stock
# --------------------------------------------------------------------------

def agregar_producto(producto_id, nombre, categoria, precio, stock_inicial):
    """Agrega un producto nuevo al catálogo o actualiza uno existente (Reto A)."""
    existente = buscar_producto(producto_id)
    if existente is None:
        catalogo.append((producto_id, nombre, categoria))
        precios[producto_id] = precio
        stock[producto_id] = stock_inicial
        escribir_log(f"Producto nuevo agregado: id={producto_id}, nombre={nombre}")
        print(f"Producto '{nombre}' agregado al catálogo.")
    else:
        precios[producto_id] = precio
        stock[producto_id] = stock_inicial
        escribir_log(f"Producto actualizado: id={producto_id}, nombre={nombre}")
        print(f"Producto '{nombre}' actualizado (precio/stock).")


def actualizar_precio_stock(producto_id, nuevo_precio=None, nuevo_stock=None):
    """Actualiza precio y/o stock de un producto existente."""
    if buscar_producto(producto_id) is None:
        raise ValueError(f"El producto con id {producto_id} no existe en el catálogo.")
    if nuevo_precio is not None:
        precios[producto_id] = nuevo_precio
    if nuevo_stock is not None:
        stock[producto_id] = nuevo_stock


# --------------------------------------------------------------------------
# 4) REGISTRAR VENTA (listas + control de errores + Reto C + Reto D)
# --------------------------------------------------------------------------

def registrar_venta(producto_id, cantidad):
    """
    Registra una venta si el producto existe y hay stock suficiente.
    - Reto C: aplica 5% de descuento si cantidad >= 10.
    - Reto D: si el producto_id no existe, se escribe el intento fallido en log.txt.
    Lanza excepciones controladas para que el menú las capture con try/except.
    """
    producto = buscar_producto(producto_id)

    if producto is None:
        # Reto D: registrar intento fallido en el log
        escribir_log(f"INTENTO FALLIDO - producto_id inexistente: {producto_id}")
        raise KeyError(f"El producto con id {producto_id} no existe en el catálogo.")

    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a 0.")

    disponible = stock.get(producto_id, 0)
    if cantidad > disponible:
        escribir_log(
            f"INTENTO FALLIDO - stock insuficiente: producto_id={producto_id}, "
            f"pedido={cantidad}, disponible={disponible}"
        )
        raise ValueError(f"Stock insuficiente. Disponible: {disponible}")

    pid, nombre, categoria = producto
    precio_unitario = precios[pid]
    subtotal = precio_unitario * cantidad

    # Reto C: descuento del 5% si la cantidad es >= 10
    descuento_pct = 0.05 if cantidad >= 10 else 0.0
    descuento_valor = subtotal * descuento_pct
    total = subtotal - descuento_valor

    # Actualizar stock (diccionario)
    stock[pid] = disponible - cantidad

    _contador_id_venta[0] += 1
    venta = {
        "id_venta": _contador_id_venta[0],
        "producto_id": pid,
        "producto": nombre,
        "categoria": categoria,
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "descuento_pct": descuento_pct,
        "total": round(total, 2),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    ventas_buffer.append(venta)
    escribir_log(f"Venta registrada: {venta}")
    return venta


# --------------------------------------------------------------------------
# 5) ARCHIVOS: guardar / leer ventas.csv con Pandas
# --------------------------------------------------------------------------

def guardar_ventas_csv(nombre_archivo=ARCHIVO_VENTAS):
    """Convierte el buffer de ventas (lista de dicts) en un DataFrame y lo guarda en CSV."""
    if not ventas_buffer:
        print("No hay ventas registradas todavía; no se generó el CSV.")
        return None
    df = pd.DataFrame(ventas_buffer)
    df.to_csv(nombre_archivo, index=False, encoding="utf-8")
    escribir_log(f"CSV guardado: {nombre_archivo} ({len(df)} filas)")
    return df


def leer_ventas_csv(nombre_archivo=ARCHIVO_VENTAS):
    """Lee el CSV de ventas con Pandas. Maneja el error si el archivo no existe."""
    try:
        df = pd.read_csv(nombre_archivo)
        return df
    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no existe todavía. Registra ventas primero.")
        escribir_log(f"ERROR - intento de lectura de archivo inexistente: {nombre_archivo}")
        return None


# --------------------------------------------------------------------------
# 6) MÉTRICAS CON NUMPY
# --------------------------------------------------------------------------

def calcular_metricas(df=None):
    """Calcula métricas (mean, std, sum) sobre los ingresos usando NumPy."""
    if df is None:
        df = pd.DataFrame(ventas_buffer)

    if df is None or df.empty:
        print("No hay datos suficientes para calcular métricas.")
        return None

    ingresos = np.array(df["total"], dtype=float)

    # división por zero controlada: promedio de unidades por venta
    cantidades = np.array(df["cantidad"], dtype=float)
    total_ventas = len(cantidades)
    try:
        promedio_unidades = np.sum(cantidades) / total_ventas
    except ZeroDivisionError:
        promedio_unidades = 0.0

    metricas = {
        "ingreso_total": float(np.sum(ingresos)),
        "ingreso_promedio": float(np.mean(ingresos)),
        "ingreso_desviacion_std": float(np.std(ingresos)),
        "unidades_totales": float(np.sum(cantidades)),
        "promedio_unidades_por_venta": float(promedio_unidades),
    }
    return metricas


def mostrar_metricas(metricas):
    if metricas is None:
        return
    print("\n--- MÉTRICAS (NumPy) ---")
    print(f"Ingreso total:            ${metricas['ingreso_total']:.2f}")
    print(f"Ingreso promedio/venta:   ${metricas['ingreso_promedio']:.2f}")
    print(f"Desviación estándar:      ${metricas['ingreso_desviacion_std']:.2f}")
    print(f"Unidades totales vendidas:{metricas['unidades_totales']:.0f}")
    print(f"Promedio unidades/venta:  {metricas['promedio_unidades_por_venta']:.2f}")


# --------------------------------------------------------------------------
# 7) PANDAS groupby + MATPLOTLIB: gráfico de ingresos por producto
# --------------------------------------------------------------------------

def ingresos_por_producto(df=None):
    """Usa groupby de Pandas para sumar ingresos por producto."""
    if df is None:
        df = pd.DataFrame(ventas_buffer)
    if df is None or df.empty:
        return None
    resumen = df.groupby("producto")["total"].sum().sort_values(ascending=False)
    return resumen


def graficar_ingresos(df=None, guardar_png=False, nombre_png="ingresos.png"):
    """Genera un gráfico de barras de ingresos por producto con Matplotlib."""
    resumen = ingresos_por_producto(df)
    if resumen is None:
        print("No hay ventas para graficar.")
        return

    plt.figure(figsize=(8, 5))
    resumen.plot(kind="bar", color="#4C72B0")
    plt.title("Ingresos por producto - MiniTienda")
    plt.xlabel("Producto")
    plt.ylabel("Ingresos ($)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    if guardar_png:
        plt.savefig(nombre_png)  # Reto B
        print(f"Gráfico exportado como '{nombre_png}'.")
        escribir_log(f"Gráfico exportado a PNG: {nombre_png}")

    plt.savefig("ingresos_preview.png")  # copia siempre disponible para evidencias
    plt.close()


# --------------------------------------------------------------------------
# 8) MENÚ PRINCIPAL (while, if/elif/else, for, break, continue, try/except/else/finally)
# --------------------------------------------------------------------------

def pedir_entero(mensaje):
    """Pide un entero al usuario controlando el error de conversión (ValueError)."""
    while True:
        try:
            valor = int(input(mensaje))
        except ValueError:
            print("Entrada inválida. Debe ingresar un número entero.")
            continue
        else:
            return valor


def menu():
    opciones_validas = {"1", "2", "3", "4", "5", "6", "7", "0"}

    while True:
        print("\n===== MENÚ MINITIENDA =====")
        print("1) Ver catálogo")
        print("2) Registrar venta")
        print("3) Guardar ventas en CSV")
        print("4) Leer ventas desde CSV")
        print("5) Calcular métricas")
        print("6) Exportar gráfico a PNG")   # Reto B
        print("7) Agregar / actualizar producto")  # Reto A
        print("0) Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion not in opciones_validas:
            print("Opción no reconocida, intente de nuevo.")
            continue

        if opcion == "0":
            print("Guardando datos antes de salir...")
            guardar_ventas_csv()
            print("¡Hasta luego!")
            break

        elif opcion == "1":
            mostrar_catalogo()

        elif opcion == "2":
            try:
                pid = pedir_entero("ID del producto: ")
                cant = pedir_entero("Cantidad: ")
                venta = registrar_venta(pid, cant)
            except KeyError as e:
                print(f"Error: {e}")
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")
            else:
                print(f"Venta registrada con éxito: {venta}")
            finally:
                print("Fin del intento de registro de venta.\n")

        elif opcion == "3":
            guardar_ventas_csv()

        elif opcion == "4":
            df = leer_ventas_csv()
            if df is not None:
                print(df)

        elif opcion == "5":
            df = leer_ventas_csv()
            metricas = calcular_metricas(df) if df is not None else calcular_metricas()
            mostrar_metricas(metricas)

        elif opcion == "6":
            df = leer_ventas_csv()
            graficar_ingresos(df, guardar_png=True)

        elif opcion == "7":
            try:
                pid = pedir_entero("ID del producto nuevo/existente: ")
                nombre = input("Nombre: ").strip()
                categoria = input("Categoría: ").strip()
                precio = float(input("Precio: "))
                stock_inicial = pedir_entero("Stock inicial: ")
                agregar_producto(pid, nombre, categoria, precio, stock_inicial)
            except ValueError as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    menu()
