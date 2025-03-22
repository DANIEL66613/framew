from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService

class UserController:
    @staticmethod
    def register_user():
        """Registra um novo usuário"""
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not name or not email or not password:
            return make_response(jsonify({"erro": "Missing required fields"}), 400)

        user = UserService.create_user(name, email, password)
        return make_response(jsonify({
            "mensagem": "User salvo com sucesso",
            "usuarios": user.to_dict()
        }), 201)

    @staticmethod
    def login():
        """Autentica um usuário e retorna um token"""
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return make_response(jsonify({"erro": "Email e senha são obrigatórios"}), 400)

        token = UserService.authenticate_user(email, password)
        if not token:
            return make_response(jsonify({"erro": "Credenciais inválidas"}), 401)

        return make_response(jsonify({"token": token}), 200)

    @staticmethod
    def activate_user():
        """Ativa um usuário com o código recebido"""
        data = request.get_json()
        email = data.get('email')
        code = data.get('code')

        if not email or not code:
            return make_response(jsonify({"erro": "Email e código são obrigatórios"}), 400)

        activated = UserService.activate_user(email, code)
        if not activated:
            return make_response(jsonify({"erro": "Código inválido ou expirado"}), 400)

        return make_response(jsonify({"mensagem": "Conta ativada com sucesso"}), 200)

    @staticmethod
    def get_user(user_id):
        """Retorna um usuário pelo ID"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            return make_response(jsonify({"erro": "Usuário não encontrado"}), 404)

        return make_response(jsonify(user.to_dict()), 200)

    @staticmethod
    def list_users():
        """Lista todos os usuários (somente para admins)"""
        users = UserService.get_all_users()
        return make_response(jsonify([user.to_dict() for user in users]), 200)
