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
    @staticmethod
    def realizar_venda(produto_id, quantidade_vendida):
        """Realiza a venda de um produto e registra no banco de dados"""
        
        # Obter o produto
        produto = Produto.query.filter_by(id=produto_id).first()

        if not produto:
            raise Exception("Produto não encontrado.")
        
        if produto.status != 'Ativo':
            raise Exception("Produto inativo, não pode ser vendido.")
        
        if produto.quantidade_em_estoque < quantidade_vendida:
            raise Exception("Quantidade em estoque insuficiente para a venda.")
        
        # Calcular o preço total da venda
        preco_unitario = produto.preco
        total_venda = preco_unitario * quantidade_vendida

        # Criar a venda
        nova_venda = Venda(
            produto_id=produto.id,
            quantidade_vendida=quantidade_vendida,
            preco_unitario=preco_unitario
        )
        
        # Atualizar o estoque do produto
        produto.quantidade_em_estoque -= quantidade_vendida
        
        try:
            # Salvar a venda no banco de dados
            db.session.add(nova_venda)
            db.session.commit()

            # Atualizar o estoque do produto
            db.session.commit()

            return nova_venda
        except IntegrityError:
            db.session.rollback()
            raise Exception("Erro ao registrar a venda.")