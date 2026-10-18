
import csv
import json
from modelos.estudiantes import Estudiantes


class ControlEstudiante:
    def __init__(self, archivoEntrada, archivoJSON, archivoResumen):
        self.archivoEntrada = archivoEntrada
        self.archivoJSON = archivoJSON
        self.archivoResumen = archivoResumen
        self.estudiantes = []
        self.errores = []

    def leerArchivo(self):
        self.estudiantes = []
        cedulas = set()

        with open(self.archivoEntrada, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for numero, fila in enumerate(lector, start=2):
                try:
                    cedula = fila["cedula"].strip()
                    nombre = fila["nombre"].strip()

                    if cedula == "" or nombre == "":
                        raise ValueError("La cédula o el nombre están vacíos.")

                    if cedula in cedulas:
                        raise ValueError("Cédula duplicada.")

                    parcial1 = float(fila["parcial1"])
                    parcial2 = float(fila["parcial2"])
                    proyecto = float(fila["proyecto"])

                    if not (0 <= parcial1 <= 100):
                        raise ValueError("Parcial 1 debe estar entre 0 y 100.")

                    if not (0 <= parcial2 <= 100):
                        raise ValueError("Parcial 2 debe estar entre 0 y 100.")

                    if not (0 <= proyecto <= 100):
                        raise ValueError("El proyecto debe estar entre 0 y 100.")

                    estudiante = Estudiantes(
                        cedula, nombre, parcial1, parcial2, proyecto
                    )

                    self.estudiantes.append(estudiante)
                    cedulas.add(cedula)

                except (ValueError, KeyError) as error:
                    self.errores.append(
                        f"Fila {numero}: {error}"
                    )

        if len(self.estudiantes) < 20:
            self.errores.append(
                "Advertencia: hay menos de 20 estudiantes válidos."
            )

    def calcularEstadisticas(self):
        notas = []

        for estudiante in self.estudiantes:
            notas.append(estudiante.calcularNotaFinal())

        if len(notas) == 0:
            raise ValueError("No hay estudiantes válidos para calcular.")

        promedio = sum(notas) / len(notas)
        notaMayor = max(notas)
        notaMenor = min(notas)

        aprobados = 0
        reprobados = 0

        for estudiante in self.estudiantes:
            if estudiante.obtenerCondicion() == "APROBADO":
                aprobados += 1
            else:
                reprobados += 1

        return {
            "total_estudiantes": len(self.estudiantes),
            "promedio_general": round(promedio, 2),
            "nota_mayor": notaMayor,
            "nota_menor": notaMenor,
            "aprobados": aprobados,
            "reprobados": reprobados
        }

    def generarJSON(self):
        datos = []

        for estudiante in self.estudiantes:
            registro = {
                "cedula": estudiante.cedula,
                "nombre": estudiante.nombre,
                "parcial1": estudiante.parcial1,
                "parcial2": estudiante.parcial2,
                "proyecto": estudiante.proyecto,
                "nota_final": estudiante.calcularNotaFinal(),
                "condicion": estudiante.obtenerCondicion()
            }

            datos.append(registro)

        with open(self.archivoJSON, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

    def generarResumen(self):
        estadisticas = self.calcularEstadisticas()

        with open(self.archivoResumen, "w", encoding="utf-8") as archivo:
            archivo.write("RESUMEN GENERAL DE CALIFICACIONES\n")
            archivo.write("----------------------------------\n")
            archivo.write(
                f"Total de estudiantes: {estadisticas['total_estudiantes']}\n"
            )
            archivo.write(
                f"Promedio general: {estadisticas['promedio_general']}\n"
            )
            archivo.write(f"Nota mayor: {estadisticas['nota_mayor']}\n")
            archivo.write(f"Nota menor: {estadisticas['nota_menor']}\n")
            archivo.write(f"Aprobados: {estadisticas['aprobados']}\n")
            archivo.write(f"Reprobados: {estadisticas['reprobados']}\n")

            if self.errores:
                archivo.write("\nErrores y advertencias:\n")

                for error in self.errores:
                    archivo.write(f"- {error}\n")

    def mostrarResultados(self):
        for estudiante in self.estudiantes:
            print(
                estudiante.cedula,
                estudiante.nombre,
                estudiante.calcularNotaFinal(),
                estudiante.obtenerCondicion()
            )

        print("\nEstadísticas:")
        estadisticas = self.calcularEstadisticas()

        for clave, valor in estadisticas.items():
            print(f"{clave}: {valor}")

        if self.errores:
            print("\nErrores y advertencias:")

            for error in self.errores:
                print(error)
