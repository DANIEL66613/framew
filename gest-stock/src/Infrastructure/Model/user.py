from src.config.data_base import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # A senha será armazenada com hash
    phone_number = db.Column(db.String(20), nullable=False)  # Número de celular
    cnpj = db.Column(db.String(20), nullable=False)  # CNPJ do seller
    active = db.Column(db.Boolean, default=False, nullable=False)
    activation_code = db.Column(db.String(10), nullable=True)  # Código de ativação

    def to_dict(self):
        """Retorna os dados do usuário sem expor a senha"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "cnpj": self.cnpj,
            "active": self.active
        }