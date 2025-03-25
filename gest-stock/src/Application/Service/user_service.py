from src.Domain.user import UserDomain
from src.Infrastructure.Model.user import User
from src.config.data_base import db
from werkzeug.security import generate_password_hash
import jwt
import datetime
from src.config.config import SECRET_KEY
from src.Infrastructure.http.whatsapp import WhatsAppService  # Alterado para importar a classe

class UserService:
    @staticmethod
    def create_user(name, email, password, phone_number, cnpj):
        """Cria um novo usuário no banco de dados e envia código de ativação via WhatsApp"""
        
        # Gerar código de ativação de 4 dígitos
        activation_code = str(random.randint(1000, 9999))

        # Hash da senha
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Criando o novo usuário no domínio
        new_user = UserDomain(name, email, hashed_password)
        
        # Criar a entrada do usuário no banco de dados
        user = User(
            name=new_user.name,
            email=new_user.email,
            password=new_user.password,
            phone_number=phone_number,  # Novo campo
            cnpj=cnpj,  # Novo campo
            active=False,
            activation_code=activation_code  # Código de ativação
        )

        # Salvar no banco de dados
        db.session.add(user)
        db.session.commit()

        # Enviar o código via WhatsApp
        WhatsAppService.enviar_mensagem(phone_number, activation_code)  # Alterado para usar a classe e função corretas

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
