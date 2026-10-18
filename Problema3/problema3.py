import polars as pl
import sys

class AnalizadorIoT:
    def __init__(self, ruta_archivo):
        self.ruta = ruta_archivo
        self.df = None
        self.resumen = None
        self.alertas = None

    def cargar_y_validar(self):
        """Lee el archivo CSV y valida los registros."""
        try:
            # Leer archivo de sensores con Polars
            df_crudo = pl.read_csv(self.ruta)
            
            # Validar identificadores y registros incompletos eliminando nulos
            df_validado = df_crudo.drop_nulls()
            
            # Validar humedad entre 0 y 100
            self.df = df_validado.filter(
                (pl.col('humedad') >= 0) & (pl.col('humedad') <= 100)
            )
            print("Datos cargados y validados correctamente.")
            
        except FileNotFoundError:
            print(f"Error: El archivo '{self.ruta}' no existe o no fue encontrado.")
            sys.exit(1)
        except Exception as e:
            print(f"Error inesperado al leer el archivo: {e}")
            sys.exit(1)

    def procesar_alertas(self):
        """Crea la columna de estado y define los motivos de las alertas."""
        if self.df is None: return

        # Crear columna de estado: ALERTA si temp > 32.0 o humedad > 80%; NORMAL en otro caso
        self.df = self.df.with_columns(
            pl.when((pl.col('temperatura') > 32.0) | (pl.col('humedad') > 80))
            .then(pl.lit('ALERTA'))
            .otherwise(pl.lit('NORMAL'))
            .alias('estado')
        )
        
        # Incluir el motivo que activó cada alerta
        self.df = self.df.with_columns(
            pl.when((pl.col('temperatura') > 32.0) & (pl.col('humedad') > 80))
            .then(pl.lit('Temperatura > 32.0°C y Humedad > 80%'))
            .when(pl.col('temperatura') > 32.0)
            .then(pl.lit('Temperatura > 32.0°C'))
            .when(pl.col('humedad') > 80)
            .then(pl.lit('Humedad > 80%'))
            .otherwise(pl.lit('N/A'))
            .alias('motivo')
        )

    def generar_estadisticas(self):
        """Calcula agregaciones por sensor y ubicación."""
        if self.df is None: return
        
        # Agrupar para calcular cantidad, temperatura (promedio, max, min) y humedad promedio
        self.resumen = self.df.group_by(['sensor', 'ubicacion']).agg([
            pl.col('sensor').count().alias('cantidad_mediciones'),
            pl.col('temperatura').mean().alias('temp_promedio'),
            pl.col('temperatura').max().alias('temp_maxima'),
            pl.col('temperatura').min().alias('temp_minima'),
            pl.col('humedad').mean().alias('humedad_promedio')
        ])

    def exportar_archivos(self):
            """Filtra las alertas y exporta los archivos CSV y JSON requeridos."""
            if self.df is None or self.resumen is None: return
            
            # Filtrar solo los registros que tienen estado de alerta
            self.alertas = self.df.filter(pl.col('estado') == 'ALERTA')
            
            try:
                # 1. Exportar alertas.json
                self.alertas.write_json('alertas.json')
                
                # 2. Exportar resumen_sensores.csv
                self.resumen.write_csv('resumen_sensores.csv')
                
                # 3. Exportar sensores_procesados.json
                self.df.write_json('sensores_procesados.json')
                
                print("Los archivos alertas.json, resumen_sensores.csv y sensores_procesados.json fueron generados con éxito.")
            except Exception as e:
                print(f"Error al exportar los archivos: {e}")

# Bloque de ejecución principal
if __name__ == '__main__':
    analizador = AnalizadorIoT('sensores.csv')
    analizador.cargar_y_validar()
    analizador.procesar_alertas()
    analizador.generar_estadisticas()
    analizador.exportar_archivos()