from flask import Blueprint, jsonify, request
from banco import db
from flask_cors import CORS, cross_origin
from models.modelViagem import Viagem
from flask_jwt_extended import jwt_required

viagens = Blueprint('viagens', __name__)


@viagens.route('/viagens')
@cross_origin()
def listagemViagem():
    viagens = Viagem.query.order_by(Viagem.idViagens).all()
    return jsonify([viagem.to_json() for viagem in viagens])
    

@viagens.route('/viagens', methods=['POST'])
# Quando colocar o login descomentar essa linha
@jwt_required
@cross_origin()
def cadastroViagem():
    viagem = Viagem.from_json(request.json)
    db.session.add(viagem)
    db.session.commit()
    return jsonify(viagem.to_json()), 201


@viagens.route('/viagens/<int:idViagens>', methods=['PUT'])
@cross_origin()
def alteracaoViagem(idViagens):
    viagem = Viagem.query.get_or_404(idViagens)
    viagem.horaPartida = request.json['horaPartida']
    viagem.horaChegada = request.json['horaChegada']
    viagem.cidadePartida = request.json['cidadePartida']  
    viagem.cidadeChegada = request.json['cidadeChegada']  
    viagem.valor = request.json['valor']  
    viagem.tipoViagem = request.json['tipoViagem']  
    db.session.add(viagem)
    db.session.commit()
    return jsonify(viagem.to_json()), 200   

@viagens.route('/viagens/<int:idViagens>')
@cross_origin()
def getByIdViagens(idViagens):
    viagem = Viagem.query.get_or_404(idViagens)
    return jsonify(viagem.to_json()), 200   

@viagens.route('/viagens/excursoes/<cidade>')
@cross_origin()
def pesquisaCidade(cidade):
    viagens = Viagem.query.order_by(Viagem.cidadeChegada).filter(Viagem.cidadeChegada.like(f'%{cidade}%')).all()
    if len(viagens):
        return jsonify([viagem.to_json() for viagem in viagens]) 
    else:
        return jsonify({'id': 0, 'message': 'Nenhuma viagem registrada para essa cidade'}), 400 


@viagens.route('/viagens/estatisticas')
def maior():
    totalViagens = Viagem.query.count()
    m = Viagem.query.order_by(Viagem.valor.desc()).limit(1).all()
    mn = Viagem.query.order_by(Viagem.valor.asc()).limit(1).all()
    maior = {
        'id': m[0].idViagens,
        'valor': m[0].valor,
        'tipoViagem': m[0].tipoViagem
        }
    menor = {
        'id': mn[0].idViagens,
        'valor': mn[0].valor,
        'tipoViagem': mn[0].tipoViagem
        }
    lista = []
    lista.append({'totalViagens': totalViagens, 'maior': maior, 'menor': menor})
    
    return jsonify(lista), 201


@viagens.route('/viagens/<int:idViagens>', methods=['DELETE'])
@cross_origin()
def exclui(idViagens):
    Viagem.query.filter_by(idViagens=idViagens).delete()
    db.session.commit()
    return jsonify({'id': idViagens, 'message': 'Viagem excluída com sucesso'}), 200

@viagens.errorhandler(404)
def id_invalido(error):
    return jsonify({'id': 0, 'message': 'Viagem não encontrada'}), 404  