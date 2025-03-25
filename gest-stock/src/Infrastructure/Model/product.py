from src.config.data_base import db

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Ativo')
    image = db.Column(db.String(255), nullable=True)  # Caminho ou URL da imagem
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Relacionamento com o seller

    seller = db.relationship('User', backref=db.backref('products', lazy=True))
    
    def __init__(self, name, price, quantity, status, image, seller_id):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.status = status
        self.image = image
        self.seller_id = seller_id

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade_em_estoque = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Ativo')
    
    # Relacionamento com as vendas
    vendas = db.relationship('Venda', back_populates='produto')
    
    def __init__(self, nome, preco, quantidade_em_estoque, status='Ativo'):
        self.nome = nome
        self.preco = preco
        self.quantidade_em_estoque = quantidade_em_estoque
        self.status = status