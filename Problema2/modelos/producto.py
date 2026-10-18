
class Producto:
    def __init__(self, codigo, producto, cantidad, precio):
        self.codigo = codigo
        self.producto = producto
        self.cantidad = cantidad
        self.precio = precio

    def calcularValor(self):
        return self.cantidad * self.precio
