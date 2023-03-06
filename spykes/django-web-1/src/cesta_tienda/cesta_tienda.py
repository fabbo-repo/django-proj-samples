class Cesta:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cesta = self.session.get('cesta')
        if not cesta:
            cesta = self.session['cesta'] = {}
        self.cesta = cesta

    def agregar(self, producto):
        if str(producto.id) not in self.cesta.keys():
            self.cesta[str(producto.id)] = {
                "producto_id":producto.id,
                "nombre":producto.nombre,
                "precio":str(producto.precio),
                "cantidad":1,
                "imagen":producto.imagen.url
            }
        else:
            for key,  value in self.cesta.items():
                if key == str(producto.id):
                    value["cantidad"] += 1
                    value["precio"] = producto.precio * value["cantidad"]
                    break
        self.guardar_cesta()

    def eliminar(self, producto):
        if str(producto.id) in self.cesta.keys():
            print(self.cesta)
            #del self.cesta[str(producto.id)]
            self.cesta.pop(str(producto.id), None)
            self.guardar_cesta()
            
    def restar_producto(self, producto):
        if str(producto.id) in self.cesta.keys():
            for key,  value in self.cesta.items():
                if key == str(producto.id):
                    if value["cantidad"] > 1:
                        value["cantidad"] -= 1
                        value["precio"] = producto.precio * value["cantidad"]
                    else: self.eliminar(producto) 
                    break
        self.guardar_cesta()

    def guardar_cesta(self):
        self.session['cesta'] = self.cesta
        self.session.modified = True

    def limpiar_cesta(self):
        self.session['cesta'] = {}
        self.session.modified = True
    