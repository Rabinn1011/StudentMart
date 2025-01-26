from store.models import Product, CartProfile


class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def db_add(self, product, quantity=1):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = CartProfile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("'", "\"")

            # Check if cart is empty, set old_cart to None or empty string
            if self.cart:  # If cart has items
                current_user.update(old_cart=str(carty))
            else:  # If cart is empty
                current_user.update(old_cart=None)

    def add(self, product, quantity=1):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = CartProfile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))


    def get_prods(self):
        product_ids=self.cart.keys()
        products=Product.objects.filter(id__in=product_ids)
        return products

    def delete(self,product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = CartProfile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            current_user.update(old_cart=str(carty))

    def __len__(self):
        return len(self.cart)
