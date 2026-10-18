
import json
import csv
from modelos.producto import Producto


class ControlInventario:
    def __init__(self, archivoEntrada):
        self.archivoEntrada = archivoEntrada
        self.productos = []
        self.movimientos = []

    def cargarInventario(self):
        with open(self.archivoEntrada, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        codigos = []

        for dato in datos:
            codigo = dato["codigo"]

            if codigo in codigos:
                raise ValueError("Hay códigos duplicados en el JSON.")

            cantidad = int(dato["cantidad"])
            precio = float(dato["precio"])

            if cantidad < 0 or precio < 0:
                raise ValueError("La cantidad y el precio no pueden ser negativos.")

            producto = Producto(
                codigo,
                dato["producto"],
                cantidad,
                precio
            )

            self.productos.append(producto)
            codigos.append(codigo)

    def listarProductos(self):
        print("\n--- INVENTARIO ---")

        for producto in self.productos:
            print(
                producto.codigo,
                producto.producto,
                "Cantidad:", producto.cantidad,
                "Precio:", producto.precio
            )

    def buscarProducto(self, codigo):
        for producto in self.productos:
            if producto.codigo == codigo:
                return producto

        return None

    def registrarMovimiento(self, codigo, tipo, cantidad):
        producto = self.buscarProducto(codigo)

        if producto is None:
            print("Producto no encontrado.")
            return

        if cantidad <= 0:
            print("La cantidad del movimiento debe ser positiva.")
            return

        if tipo == "entrada":
            producto.cantidad += cantidad

        elif tipo == "salida":
            if cantidad > producto.cantidad:
                print("No hay suficientes existencias.")
                return

            producto.cantidad -= cantidad

        else:
            print("Tipo de movimiento inválido.")
            return

        movimiento = {
            "codigo": producto.codigo,
            "tipo": tipo,
            "cantidad": cantidad,
            "existencia_final": producto.cantidad
        }

        self.movimientos.append(movimiento)
        print("Movimiento registrado correctamente.")

    def calcularValorInventario(self):
        total = 0

        for producto in self.productos:
            total += producto.calcularValor()

        return total

    def mostrarExistenciasBajas(self):
        print("\n--- PRODUCTOS CON MENOS DE 15 UNIDADES ---")
        encontrados = 0

        for producto in self.productos:
            if producto.cantidad < 15:
                print(producto.codigo, producto.producto,
                      "Cantidad:", producto.cantidad)
                encontrados += 1

        if encontrados == 0:
            print("No hay productos con existencias bajas.")

    def guardarInventarioJSON(self):
        datos = []

        for producto in self.productos:
            registro = {
                "codigo": producto.codigo,
                "producto": producto.producto,
                "cantidad": producto.cantidad,
                "precio": producto.precio
            }
            datos.append(registro)

        with open("inventario_actualizado.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

    def guardarInventarioCSV(self):
        with open("inventario.csv", "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["codigo", "producto", "cantidad", "precio"])

            for producto in self.productos:
                escritor.writerow([
                    producto.codigo,
                    producto.producto,
                    producto.cantidad,
                    producto.precio
                ])

    def guardarMovimientosCSV(self):
        with open("movimientos.csv", "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([
                "codigo", "tipo", "cantidad", "existencia_final"
            ])

            for movimiento in self.movimientos:
                escritor.writerow([
                    movimiento["codigo"],
                    movimiento["tipo"],
                    movimiento["cantidad"],
                    movimiento["existencia_final"]
                ])

    def menu(self):
        opcion = ""

        while opcion != "6":
            print("\n===== MENU DE INVENTARIO =====")
            print("1. Listar productos")
            print("2. Buscar producto por código")
            print("3. Registrar entrada")
            print("4. Registrar salida")
            print("5. Mostrar valor y existencias bajas")
            print("6. Guardar archivos y salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.listarProductos()

            elif opcion == "2":
                codigo = input("Ingrese el código: ")
                producto = self.buscarProducto(codigo)

                if producto is None:
                    print("Producto no encontrado.")
                else:
                    print(
                        producto.codigo,
                        producto.producto,
                        "Cantidad:", producto.cantidad,
                        "Precio:", producto.precio
                    )

            elif opcion == "3" or opcion == "4":
                codigo = input("Ingrese el código del producto: ")

                try:
                    cantidad = int(input("Ingrese la cantidad: "))

                    if opcion == "3":
                        self.registrarMovimiento(codigo, "entrada", cantidad)
                    else:
                        self.registrarMovimiento(codigo, "salida", cantidad)

                except ValueError:
                    print("Debe ingresar una cantidad entera válida.")

            elif opcion == "5":
                print(
                    "Valor total del inventario:",
                    round(self.calcularValorInventario(), 2)
                )
                self.mostrarExistenciasBajas()

            elif opcion == "6":
                self.guardarInventarioJSON()
                self.guardarInventarioCSV()
                self.guardarMovimientosCSV()
                print("Archivos guardados correctamente.")

            else:
                print("Opción inválida.")
