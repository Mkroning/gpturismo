from flask import Blueprint, jsonify, request
from banco import db
from flask_cors import CORS, cross_origin
from models.modelExcursao import Excursao
from models.modelViagem import Viagem
# from flask_jwt_extended import jwt_required

excursoes = Blueprint('excursoes', __name__)


@excursoes.route('/excursoes')
@cross_origin()
def listagemExcursao():
    excursoes = Excursao.query.order_by(Excursao.idExcursoes).all()
    return jsonify([excursao.to_json() for excursao in excursoes])


@excursoes.route('/excursoes', methods=['POST'])
# Quando colocar o login descomentar essa linha
# @jwt_required
@cross_origin()
def cadastroExcursao():
    excursao = Excursao.from_json(request.json)
    db.session.add(excursao)
    db.session.commit()
    return jsonify(excursao.to_json()), 201


@excursoes.route('/excursoes/<int:idExcursoes>', methods=['PUT'])
@cross_origin()
def alteracaoExcursao(idExcursoes):
    excursao = Excursao.query.get_or_404(idExcursoes)
    excursao.dataPartida = request.json['dataPartida']
    excursao.dataChegada = request.json['dataChegada']
    excursao.detalheExcursoes = request.json['detalheExcursoes']
    excursao.foto = request.json['foto']
    excursao.idViagens = request.json['idViagens']
    db.session.add(excursao)
    db.session.commit()
    return jsonify(excursao.to_json()), 201


@excursoes.route('/excursoes/<int:idExcursoes>')
@cross_origin()
def getByIdExcursao(idExcursoes):
    excursao = Excursao.query.get_or_404(idExcursoes)
    return jsonify(excursao.to_json()), 200


@excursoes.route('/excursoes/viagem/<int:idViagens>')
@cross_origin()
def getByIdViagens(idViagens):
    excursoes = Excursao.query.order_by(Excursao.idExcursoes).filter(Excursao.idViagens.like(f'%{idViagens}%')).all()
    if len(excursoes):
        return jsonify([excursao.to_json() for excursao in excursoes]) 


@excursoes.route('/excursoes/<int:idExcursoes>', methods=['DELETE'])
@cross_origin()
def exclui(idExcursoes):
    Excursao.query.filter_by(idExcursoes=idExcursoes).delete()
    db.session.commit()
    return jsonify({'id': idExcursoes, 'message': 'Excursão excluída com sucesso'}), 200


@excursoes.errorhandler(404)
def id_invalido(error):
    return jsonify({'id': 0, 'message': 'Excursão não encontrada'}), 404

@excursoes.route('/excursoes_qtd')
def excursoesgraf():
    excursoes = db.session.query(Viagem.cidadeChegada).filter(Viagem.tipoViagem ==2).group_by(Viagem.cidadeChegada).all()
    clic = db.session.query(Excursao.numeroClics).group_by(Excursao.numeroClics).all()
    print(excursoes)
    print(clic)

    num =0
    lista = []
    for excursao in excursoes:
        lista.append({'destino': excursao[0], 'num': clic[num][0]})
        num=num +1

    print(lista)    
    return jsonify(lista), 201


@excursoes.route('/excursoes/numeroClics/<int:idExcursoes>', methods=['PUT'])
@cross_origin()
def Excursaoclics(idExcursoes):
    excursao = Excursao.query.get_or_404(idExcursoes)
    if excursao.numeroClics == None:
        excursao.numeroClics = 1
    else:
        excursao.numeroClics = excursao.numeroClics +1
    db.session.add(excursao)
    db.session.commit()
    return jsonify(excursao.to_json()), 201