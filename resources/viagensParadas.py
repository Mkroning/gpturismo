from flask import Blueprint, jsonify, request
from banco import db
from models.modelViagensParadas import ViagensParada
from flask_cors import CORS, cross_origin
# from flask_jwt_extended import jwt_required

viagensParadas = Blueprint('viagensParadas', __name__)


@viagensParadas.route('/viagensParadas')
@cross_origin()
def listagemParadas():
    viagensParadas = ViagensParada.query.order_by(ViagensParada.idViagensParadas).all()
    return jsonify([viagensParada.to_json() for viagensParada in viagensParadas])


@viagensParadas.route('/viagensParadas', methods=['POST'])
# Quando colocar o login descomentar essa linha
# @jwt_required
@cross_origin()
def cadastroParadas():
    viagensParada = ViagensParada.from_json(request.json)
    db.session.add(viagensParada)
    db.session.commit()
    return jsonify(viagensParada.to_json()), 201


@viagensParadas.route('/viagensParadas/<int:idViagensParadas>', methods=['PUT'])
@cross_origin()
def alteracaoParadas(idViagensParadas):
    viagensParada = ViagensParada.query.get_or_404(idViagensParadas)
    viagensParada.idViagens = request.json['idViagens']
    viagensParada.idParadas = request.json['idParadas']
    db.session.add(viagensParada)
    db.session.commit()
    return jsonify(viagensParada.to_json()), 201 


@viagensParadas.route('/viagensParadas/<int:idViagensParadas>', methods=['DELETE'])
@cross_origin()
def exclui(idViagensParadas):
    ViagensParada.query.filter_by(idViagensParadas=idViagensParadas).delete()
    db.session.commit()
    return jsonify({'id': idViagensParadas, 'message': 'ViagensParada excluída com sucesso'}), 200

@viagensParadas.errorhandler(404)
def id_invalido(error):
    return jsonify({'id': 0, 'message': 'Não encontrado'}), 404 