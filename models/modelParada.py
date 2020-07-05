
from banco import db

class Parada(db.Model):
  __tablename__ = 'paradas'
  idParadas = db.Column(db.Integer, autoincrement=True, primary_key=True)
  nome = db.Column(db.String(45), nullable=False)
  localizacao = db.Column(db.String(200), nullable=False)
  horario = db.Column(db.String(10), nullable=False)


  def to_json(self):
    json_paradas = {
      'idParadas': self.idParadas,
      'nome': self.nome,
      'localizacao': self.localizacao,
      'horario': self.horario
    }
  
    return json_paradas

  @staticmethod
  def from_json(json_paradas):
    nome = json_paradas.get('nome')
    localizacao = json_paradas.get('localizacao')
    horario = json_paradas.get('horario')

    return Parada(nome=nome, localizacao=localizacao, horario=horario)