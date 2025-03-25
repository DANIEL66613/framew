from flask import Blueprint, request, jsonify
from src.Application.Service.product_service import ProductService
from flask_jwt_extended import jwt_required, get_jwt_identity

product_controller = Blueprint('product_controller', __name__)

@product_controller.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    """Endpoint para criar um novo produto"""
    data = request.get_json()
    seller_id = get_jwt_identity()  # Obtém o ID do seller a partir do JWT
    product = ProductService.create_product(
        name=data['name'],
        price=data['price'],
        quantity=data['quantity'],
        status=data.get('status', 'Ativo'),
        image=data.get('image', ''),
        seller_id=seller_id
    )
    return jsonify({"message": "Produto criado com sucesso!", "product": product.id}), 201

@product_controller.route('/products', methods=['GET'])
@jwt_required()
def list_products():
    """Endpoint para listar os produtos de um seller"""
    seller_id = get_jwt_identity()  # Obtém o ID do seller a partir do JWT
    products = ProductService.list_products_by_seller(seller_id)
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity,
        'status': product.status,
        'image': product.image
    } for product in products])

@product_controller.route('/products/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    """Endpoint para obter os detalhes de um produto"""
    product = ProductService.get_product_details(product_id)
    if product:
        return jsonify({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': product.quantity,
            'status': product.status,
            'image': product.image
        })
    return jsonify({"message": "Produto não encontrado"}), 404

@product_controller.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """Endpoint para editar um produto"""
    data = request.get_json()
    product = ProductService.update_product(
        product_id,
        name=data.get('name'),
        price=data.get('price'),
        quantity=data.get('quantity'),
        status=data.get('status'),
        image=data.get('image')
    )
    if product:
        return jsonify({"message": "Produto atualizado com sucesso!"})
    return jsonify({"message": "Produto não encontrado"}), 404

@product_controller.route('/products/<int:product_id>/deactivate', methods=['PUT'])
@jwt_required()
def deactivate_product(product_id):
    """Endpoint para inativar um produto"""
    product = ProductService.deactivate_product(product_id)
    if product:
        return jsonify({"message": "Produto inativado com sucesso!"})
    return jsonify({"message": "Produto não encontrado"}), 404
