import sys
import os
from flask import jsonify, make_response, request

# Adiciona o diretório 'src' ao caminho de busca do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from Application.Controllers.user_controller import UserController

def init_routes(app):    
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)
    
    # Rota raiz
    @app.route('/', methods=['GET'])
    def welcome():
        return make_response(jsonify({
            "mensagem": "Bem-vindo ao servidor mercado"
        }), 200)
    
    # Cadastro de usuário
    @app.route('/user', methods=['POST'])
    def register_user():
        return UserController.register_user()

    # Autenticação do usuário (Login)
    @app.route('/auth/login', methods=['POST'])
    def login():
        return UserController.login()

    # Ativação do usuário via código
    @app.route('/user/activate', methods=['POST'])
    def activate_user():
        return UserController.activate_user()

    # Obter informações do usuário autenticado
    @app.route('/user/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        return UserController.get_user(user_id)
