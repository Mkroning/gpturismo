from flask import Blueprint, jsonify, request
from banco import db
from models.modelInteresse import Interesse
from models.modelExcursao import Excursao
from models.modelViagem import Viagem
from flask_jwt_extended import jwt_required
# from datetime import datetime, timedelta
# from flask_cors import CORS, cross_origin
import smtplib

interesses = Blueprint('interesses', __name__)


@interesses.route('/interesses')
def listagem():
    # propostas = Proposta.query.order_by(Proposta.lance).all()
    interesses = Interesse.query.all()
    return jsonify([interesse.to_json() for interesse in interesses])


@interesses.route('/interesses', methods=['POST'])
# @jwt_required
# @cross_origin()
def inclusao():
    interesse = Interesse.from_json(request.json)

    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.starttls()
    # server.login('email', 'senha')
    # server.set_debuglevel(1)
    # nomePessoa = request.json['nomePessoa']
    # email = request.json['email']
    # telefone = request.json['telefone']
    # lance = request.json['lance']
    # modelo = request.json['carro_id']
    # msg = 'Ola senhor(a) ' + nomePessoa + 'o seu lance foi ' + str(lance) + ', tal proposta sera avaliada e retornaremos por email ' + \
    #     email + ' ou telefone ' + telefone + 'sobre o veiculo' + str(modelo)
    # server.sendmail('f{email}', email, msg)
    # server.quit()

    db.session.add(interesse)
    db.session.commit()
    return jsonify(interesse.to_json()), 201


@interesses.route('/interesses/email', methods=['POST'])
# @jwt_required
def aceitar():
    interesse = Interesse.from_json(request.json)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('conta.teste.laravel@gmail.com', 'conta#teste#laravel')
    server.set_debuglevel(1)
    idInteresse = request.json['idInteresse']
    email = request.json['email']
    nome = request.json['nome']
    msg = 'Ola senhor(a) f{nome}, estamos muito felizes com o interesse.'  \
        'esperamos o senhor(a) na nossa agência para realizar o pagamento da viagem e curtir a viagem.   '

    server.sendmail('f{email}', email, msg)
    server.quit()

    return jsonify(interesse.to_json()), 201


@interesses.errorhandler(404)
def id_invalido(error):
    return jsonify({'id': 0, 'message': 'not found'}), 404


@interesses.route('/interesses/<int:id>', methods=['PUT'])
def alteracao(id):
    # obtém o registro a ser alterado (ou gera um erro 404 - not found)
    interesse = Interesse.query.get_or_404(id)

    # recupera os dados enviados na requisição
    interesse.nome = request.json['nome']
    interesse.idExcursoes = request.json['idExcursoes']
    interesse.email = request.json['email']

    # altera (pois o id já existe)
    db.session.add(interesse)
    db.session.commit()
    return jsonify(interesse.to_json()), 204


@interesses.route('/interesses/<int:id>')
def consulta(id):
    # obtém o registro a ser alterado (ou gera um erro 404 - not found)
    interesse = Interesse.query.get_or_404(id)
    return jsonify(interesse.to_json()), 200


@interesses.route('/interesses/<int:id>', methods=['DELETE'])
def exclui(id):
    Interesse.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'id': id, 'message': 'Interesse Removido com sucesso'}), 200
