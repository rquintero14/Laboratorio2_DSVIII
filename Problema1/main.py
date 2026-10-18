
from utilidades.controlEstudiante import ControlEstudiante

archivoEntrada = "estudiantes.csv"
archivoJSON = "estudiantes.json"
archivoResumen = "resumen.txt"

control = ControlEstudiante(
    archivoEntrada,
    archivoJSON,
    archivoResumen
)

try:
    control.leerArchivo()
    control.mostrarResultados()
    control.generarJSON()
    control.generarResumen()

    print("\nArchivos generados exitosamente.")

except Exception as e:
    print(f"Error en la ejecución => {e}")
