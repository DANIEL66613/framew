from src.config.data_base import db
from datetime import datetime

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)  # Referência ao produto
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)  # Preço do produto no momento da venda
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)  # Data e hora da venda
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Referência ao seller

    produto = db.relationship('Produto', backref=db.backref('vendas', lazy=True))  # Relacionamento com Produto
    seller = db.relationship('User', backref=db.backref('vendas', lazy=True))
