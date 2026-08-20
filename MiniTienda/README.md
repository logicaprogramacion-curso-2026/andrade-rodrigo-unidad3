# MiniTienda - Registro y análisis de ventas

Proyecto de la asignación de **Lógica de Programación** (UIDE), desafío MiniTienda.

## De qué se trata

Es un programa de consola que simula una tienda pequeña: tiene un catálogo de
productos, permite registrar ventas, guarda todo en un CSV y después calcula
algunas métricas y saca un gráfico de cuánto se vendió por producto. Lo hice
usando las estructuras de datos que hemos visto en clase (tuplas, listas,
diccionarios) combinadas con Pandas, NumPy y Matplotlib.

## Qué archivos hay en esta carpeta

| Archivo | Qué es |
|---|---|
| `MiniTienda.ipynb` | El notebook con todo el código, para correrlo en Colab o Jupyter. Tiene celdas de prueba al final que corren todo el programa solas. |
| `minitienda.py` | El mismo programa pero como script de consola normal (con `input()`), para correrlo directo en la terminal. |
| `evidencia_minitienda.pdf` | El PDF con el membrete, las capturas de cuando corrí el programa y la explicación de cómo funciona. |
| `README.md` | Este archivo. |
| `ventas.csv` | El CSV que se genera con las ventas de prueba. |
| `log.txt` | El log donde queda registrado lo que va pasando (ventas, errores, etc). |
| `ingresos.png` | El gráfico de barras de ingresos por producto. |

## Cómo organicé el código

- Los productos del catálogo los guardé como **tuplas** `(id, nombre, categoria)`, y el catálogo completo es una lista de esas tuplas.
- `precios` y `stock` son **diccionarios**, porque necesito buscar rápido por el id del producto.
- Cada venta que se registra es un diccionario, y todas se van guardando en una **lista** (`ventas_buffer`). Cuando quiero analizar los datos, esa lista se convierte en un **DataFrame de Pandas**.
- Con Pandas hago el `groupby` para sumar ingresos por producto, y también uso `to_csv`/`read_csv` para guardar y leer el archivo.
- Con NumPy saco el promedio, la suma y la desviación estándar de los ingresos.
- Con Matplotlib hago el gráfico de barras y lo exporto a PNG.
- Todo el programa está separado en funciones (una para cada cosa: mostrar catálogo, registrar venta, guardar CSV, calcular métricas, graficar, etc), para que no quede todo amontonado.

## Cómo correrlo

**Desde el notebook (más fácil):** abrir `MiniTienda.ipynb` en Colab o Jupyter y darle "Ejecutar todo". Las últimas celdas simulan varias ventas solas, no hay que escribir nada a mano.

**Desde consola:**
```
python minitienda.py
```
Y sale un menú:
```
1) Ver catálogo
2) Registrar venta
3) Guardar ventas en CSV
4) Leer ventas desde CSV
5) Calcular métricas
6) Exportar gráfico a PNG
7) Agregar / actualizar producto
0) Salir
```

## Los retos que agregué

- **Reto A:** la opción 7 del menú deja agregar un producto nuevo al catálogo o cambiarle el precio/stock a uno que ya existe.
- **Reto B:** la opción 6 exporta el gráfico como PNG usando `plt.savefig("ingresos.png")`.
- **Reto C:** si alguien compra 10 unidades o más de un producto, se le aplica automáticamente un 5% de descuento.
- **Reto D:** si alguien trata de vender un producto que no existe en el catálogo, aparte de que sale el error, ese intento fallido queda anotado en el `log.txt`.

## Respuestas

**¿Qué parte la hizo Pandas y qué parte NumPy?**

Pandas lo usé para pasar la lista de ventas a un DataFrame, para guardar y leer el `ventas.csv`, y para agrupar las ventas por producto con `groupby` y sacar el total de ingresos de cada uno (eso es lo que después se grafica). NumPy lo usé para los cálculos numéricos en sí: la suma, el promedio y la desviación estándar de los ingresos y las cantidades vendidas.

**¿Dónde usé try/except y por qué?**

Lo usé en tres partes: cuando pido un número al usuario (por si escribe algo que no es número), alrededor de `registrar_venta()` en el menú (por si el producto no existe o no hay stock suficiente) y cuando leo el CSV (por si todavía no existe el archivo). En el registro de venta usé el try/except/else/finally completo: el `else` corre solo si la venta se guardó bien, y el `finally` siempre imprime un mensaje al final, haya salido bien o mal.

**¿Qué estructuras son tuplas, listas y diccionarios en el código?**

Tuplas: cada producto individual `(id, nombre, categoria)`. Listas: el catálogo completo y el buffer de ventas. Diccionarios: `precios`, `stock`, y cada venta guardada dentro del buffer también es un diccionario.

## Autor

Andrade Espinoza Rodrigo Alejandro - Lógica de Programación, UIDE
