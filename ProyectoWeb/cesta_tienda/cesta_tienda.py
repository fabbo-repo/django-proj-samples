class Cesta:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cesta = self.session.get('cesta')
        if not cesta:
            cesta = self.session['cesta'] = {}
        else: 
            self.cesta = cesta

    def agregar(self, producto):
        if str(producto.id) not in self.cesta.keys():
            self.cesta[producto.id] = {
                "producto_id":producto.id,
                "nombre":producto.nombre,
                "precio":str(producto.precio),
                "cantidad":1,
                "imagen":producto.imagen.url
            }