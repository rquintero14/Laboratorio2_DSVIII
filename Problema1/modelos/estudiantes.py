
class Estudiantes:
    def __init__(self, cedula, nombre, parcial1, parcial2, proyecto):
        self.cedula = cedula
        self.nombre = nombre
        self.parcial1 = parcial1
        self.parcial2 = parcial2
        self.proyecto = proyecto

    def calcularNotaFinal(self):
        notaFinal = (
            self.parcial1 * 0.30
            + self.parcial2 * 0.30
            + self.proyecto * 0.40
        )
        return round(notaFinal, 2)

    def obtenerCondicion(self):
        if self.calcularNotaFinal() >= 71:
            return "APROBADO"
        else:
            return "REPROBADO"
