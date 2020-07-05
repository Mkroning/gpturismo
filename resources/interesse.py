from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse
from banco import db
from flask_cors import CORS, cross_origin
from models.modelInteresse import Interesse
from flask_jwt_extended import jwt_required
import smtplib

interesses = Blueprint('interesses', __name__)

argumentos =reqparse.RequestParser()
argumentos.add_argument('email', type=str, required=True, help="O campo 'email' não pode ficar em branco")
argumentos.add_argument('nome', type=str, required=True, help="O campo 'nome' não ficar em branco")
argumentos.add_argument('idExcursoes', type=int, required=True, help="É necessario o 'id da excursao'")

@interesses.route('/interesses')
@cross_origin()
def readInteresse():
  interesses = Interesse.query.order_by(Interesse.idInteresse).all()
  return jsonify([interesse.to_json() for interesse in interesses])

@interesses.route('/interesses/<int:idInteresse>')
@cross_origin()
def readForId():
  interesse = Interesse.find_interesse(idInteresse)
  if interesse:
    return interesse.json()
  return {'message': 'Car not found'}, 404

@interesses.route('/interesses', methods=['POST'])
@cross_origin()
#@jwt_required
def createInteresse():
  if Interesse.find_interesse(idInteresse):
    return{"message":"Interesse id'{}' já existe".format(idInteresse)}, 400

  dados = Interesse.argumentos.parse_args()

  interesse_objeto = Interesse(idInteresse, **dados)
  try:
    interesse.save_interesse()
  except:
    return{'message':'An internal error ocurred trying to save'}, 500
  return interresse.json()

@interesses.route('/interesses/<int:idInteresses>', methods=['PUT'])
@cross_origin()
#@jwt_required
def updateInteresse(idInteresse):
  dados = Interesse.argumentos.parse_args()

  interesse_encontrado = Interesse.find_interesse(idInteresse)
  if interesse_encontrado:
    interesse_encontrado.updateInteresse(**dados)
    interesse_encontrado.save_interesse()
    return interesse_encontrado.json(), 200
  interesse = Interesse(idInteresse, **dados)
  try:
    interesse.save_interesse()
  except:
    return {'message':'An internal error ocurred tryin to save'}, 500
  return interesse.json(), 201

@interesses.route('/interesses/<int:idInteresses>', methods=['DELETE'])
@cross_origin()
#@jwt_required
def deleteInteresse(idInteresse):
  interesse = Interesse.find_interesse(idInteresse)
  if interesse:
    try:
      interesse.delete_interesse()
    except:
      return {'message':'An error ocurred trying to delete'}, 500
    return {'message':'Interesse Deletado'}
  return {'message':'Interesse não encontrado', 404}  

@interesses.route('/interesse/envia_email')
@cross_origin()
#@jwt_required
def enviaEmail(idInteresse, idExcursoes):
  dados = Interesse.argumentos.parse_args()

  interesse_encontrado = Interesse.find_interesse(idInteresse)

  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login('gordosexy550@gmail.com', 'GordoSexy550@')
  server.set_debuglevel(1)
  msg = 'Olá, notamos o seu interesse na seguinte excursão' + idExcursão
  server.sendmail('gordosexy550@gmail.com', emailInteresse, msg)
  server.quit()
  return json {'message':'Email enviado!'}   



