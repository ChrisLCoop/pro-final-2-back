class Cart:
    def __init__(self,request):
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')
        total = self.session.get('cart_total')
        if not cart:
            cart = self.session['cart']={}
            total = self.session['cart_total'] = 0

        self.cart = cart
        self.total = float(total)

    def add(self,curso,cantidad,imagen_url):
        if (str(curso.id) not in self.cart.keys()):  
            self.cart[curso.id] = {
                'curso_id':curso.id,
                'nombre':curso.curso,
                'cantidad':cantidad,
                'precio':str(curso.precio),
                'imagen':imagen_url,
                'categoria':curso.categoria.nombre,
                'area':curso.area.nombre,
                'subtotal':str(cantidad * curso.precio)
            }
        else:
            for key,value in self.cart.items():
                if key == str(curso.id):
                    value['cantidad'] = value['cantidad']+ cantidad
                    value['subtotal'] = str(float(value['cantidad'])* float(value['precio']))
                    break
        self.save()

    def delete(self,curso):
        if str(curso.id) in self.cart:
            del self.cart[str(curso.id)]
            self.save()

    def clear(self):
        self.session['cart']={}
        self.session['cart_total'] = 0

    def save(self):
        total = 0
        for key,value in self.cart.items():
            total += float(value['subtotal'])

        self.session['cart_total'] = total
        self.session['cart'] = self.cart
        self.session.modified = True
