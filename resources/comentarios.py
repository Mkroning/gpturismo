from flask import Blueprint, jsonify, request
from banco import db
from models.modelComentario import Comentario
from flask_cors import CORS, cross_origin
# from flask_jwt_extended import jwt_required

comentarios = Blueprint('comentarios', __name__)


@comentarios.route('/comentarios')
@cross_origin()
def listagemComentarios():
    comentarios = Comentario.query.order_by(Comentario.idComentarios).all()
    return jsonify([comentario.to_json() for comentario in comentarios])


@comentarios.route('/comentarios', methods=['POST'])
# @jwt_required
@cross_origin()
def cadastroComentarios():
    comentario = Comentario.from_json(request.json)
    db.session.add(comentario)
    db.session.commit()
    return jsonify(comentario.to_json()), 201


@comentarios.route('/comentarios/<int:idComentarios>', methods=['PUT'])
@cross_origin()
def alteracaoComentarios(idComentarios):
    comentario = Comentario.query.get_or_404(idComentarios)
    comentario.nomeComentario = request.json['nomeComentario']
    comentario.notaComentario = request.json['notaComentario']
    comentario.avaliacao = request.json['avaliacao']  
    comentario.idExcursoes = request.json['idExcursoes']  
    db.session.add(comentario)
    db.session.commit()
    return jsonify(comentario.to_json()), 201


@comentarios.route('/comentarios/<int:idComentarios>')
@cross_origin()
def getByIdExcursao(idComentarios):
    comentario = Comentario.query.get_or_404(idComentarios)
    return jsonify(comentario.to_json()), 200 


@comentarios.route('/comentarios/<int:idComentarios>', methods=['DELETE'])
@cross_origin()
def exclui(idComentarios):
    Comentario.query.filter_by(idComentarios=idComentarios).delete()
    db.session.commit()
    return jsonify({'id': idComentarios, 'message': 'Comentário excluído com sucesso'}), 200

@comentarios.errorhandler(404)
def id_invalido(error):
    return jsonify({'id': 0, 'message': 'Comentário não encontrado'}), 404 
