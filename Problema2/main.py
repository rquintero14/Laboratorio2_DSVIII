from utilidades.controlInventario import ControlInventario

try:
    control = ControlInventario("inventario.json")
    control.cargarInventario()

    print("Inventario cargado correctamente.")
    control.menu()

except FileNotFoundError:
    print("Error: no se encontró el archivo inventario.json.")

except (ValueError, KeyError) as e:
    print(f"Error en los datos del inventario: {e}")

except Exception as e:
    print(f"Error en la ejecución => {e}")
