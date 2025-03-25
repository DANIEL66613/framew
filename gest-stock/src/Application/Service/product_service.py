from src.Infrastructure.Model.product import Product
from src.config.data_base import db

class ProductService:
    
    @staticmethod
    def create_product(name, price, quantity, status, image, seller_id):
        """Cria um novo produto para o seller"""
        product = Product(name=name, price=price, quantity=quantity, status=status, image=image, seller_id=seller_id)
        db.session.add(product)
        db.session.commit()
        return product
    
    @staticmethod
    def list_products_by_seller(seller_id):
        """Lista os produtos de um seller específico"""
        return Product.query.filter_by(seller_id=seller_id).all()

    @staticmethod
    def get_product_details(product_id):
        """Obtém os detalhes de um produto específico"""
        return Product.query.get(product_id)
    
    @staticmethod
    def update_product(product_id, name=None, price=None, quantity=None, status=None, image=None):
        """Edita as informações de um produto"""
        product = Product.query.get(product_id)
        if product:
            if name:
                product.name = name
            if price:
                product.price = price
            if quantity:
                product.quantity = quantity
            if status:
                product.status = status
            if image:
                product.image = image
            db.session.commit()
            return product
        return None
    
    @staticmethod
    def deactivate_product(product_id):
        """Inativa um produto"""
        product = Product.query.get(product_id)
        if product:
            product.status = 'Inativo'
            db.session.commit()
            return product
        return None
