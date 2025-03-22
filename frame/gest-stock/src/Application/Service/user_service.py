from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from src.config.config import SECRET_KEY

class UserService:
    @staticmethod
    def create_user(name, email, password):
        """Cria um novo usuário no banco de dados"""
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = UserDomain(name, email, hashed_password)
        user = User(name=new_user.name, email=new_user.email, password=new_user.password, active=False, activation_code="1234")  # Gera código temporário
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate_user(email, password):
        """Autentica um usuário e retorna um token JWT"""
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None  # Credenciais inválidas

        if not user.active:
            return None  # Conta não ativada

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def activate_user(email, code):
        """Ativa um usuário caso o código de ativação esteja correto"""
        user = User.query.filter_by(email=email).first()
        if user and user.activation_code == code:
            user.active = True
            user.activation_code = None  # Remove código após ativação
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_user_by_id(user_id):
        """Busca um usuário pelo ID"""
        return User.query.get(user_id)

    @staticmethod
    def get_all_users():
        """Lista todos os usuários"""
        return User.query.all()
