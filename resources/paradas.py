from flask import Blueprint, jsonify, request
from banco import db
from models.modelParada import Parada
from flask_cors import CORS, cross_origin
# from flask_jwt_extended import jwt_required

paradas = Blueprint('paradas', __name__)


@paradas.route('/paradas')
@cross_origin()
def listagemParadas():
    paradas = Parada.query.order_by(Parada.idParadas).all()
    return jsonify([parada.to_json() for parada in paradas])


@paradas.route('/paradas', methods=['POST'])
# Quando colocar o login descomentar essa linha
# @jwt_required
@cross_origin()
def cadastroParadas():
    parada = Parada.from_json(request.json)
    db.session.add(parada)
    db.session.commit()
    return jsonify(parada.to_json()), 201


@paradas.route('/paradas/<int:idParadas>', methods=['PUT'])
@cross_origin()
def alteracaoParadas(idParadas):
    parada = Parada.query.get_or_404(idParadas)
    parada.nome = request.json['nome']
    parada.localizacao = request.json['localizacao']
    parada.horario = request.json['horario']  
    parada.idViagens = request.json['idViagens']  
    db.session.add(parada)
    db.session.commit()
    return jsonify(parada.to_json()), 201   

@paradas.route('/paradas/<int:idParadas>')
@cross_origin()
def getByIdParadas(idParadas):
    parada = Parada.query.get_or_404(idParadas)
    return jsonify(parada.to_json()), 200  


@paradas.route('/paradas/<int:idParadas>', methods=['DELETE'])
@cross_origin()
def exclui(idParadas):
    Parada.query.filter_by(idParadas=idParadas).delete()
    db.session.commit()
    return jsonify({'id': idParadas, 'message': 'Parada excluída com sucesso'}), 200

@paradas.errorhandler(404)
def id_invalido(error):
    return jsonify({'id': 0, 'message': 'Parada não encontrada'}), 404 
