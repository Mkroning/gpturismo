from flask import Blueprint, jsonify, request
from banco import db
from models.modelInteresse import Interesse
from flask_cors import CORS, cross_origin
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
# Quando colocar o login descomentar essa linha
# @jwt_required
@cross_origin()
def cadastraInteresse():
    interesse = Interesse.from_json(request.json)
    db.session.add(interesse)
    db.session.commit()
    return jsonify(interesse.to_json()), 201


@interesses.route('/interesses/envia_email/<int:id>', methods=['POST'])
def envia(id):
    interesse = Interesse.query.get_or_404(id)
    print(interesse)
    nome = interesse.nome
    emailInteresse = interesse.email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('gordosexy550@gmail.com', 'GordoSexy550@')
    server.set_debuglevel(1)
    msg = 'Ola senhor(a) ' + nome + ', a nossa empresa fica muito feliz com seu interesse.'  \
        'Esperamos o senhor(a) na nossa agencia para realizar o pagamento e curtir a sua excursao.   '
    server.sendmail('gordosexy550@gmail.com',emailInteresse, msg)
    server.quit()
    return jsonify({"Message": "E-mail enviado..."})


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


@interesses.errorhandler(404)
def id_invalido(error):
    return jsonify({'id': 0, 'message': 'not found'}), 404


@interesses.route('/interesses/<int:id>', methods=['DELETE'])
def exclui(id):
    Interesse.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'id': id, 'message': 'Interesse Removido com sucesso'}), 200
