from banco import db

class ViagensParada(db.Model):
  __tablename__ = 'viagensParadas'
  idViagensParadas = db.Column(db.Integer, autoincrement=True, primary_key=True)
  idViagens = db.Column(db.Integer, db.ForeignKey(
  'viagens.idViagens'), nullable=False)

  viagens = db.relationship('Viagem')

  idParadas = db.Column(db.Integer, db.ForeignKey(
  'paradas.idParadas'), nullable=False)

  paradas = db.relationship('Parada')

  def to_json(self):
    json_viagensParadas = {
      'idViagens': self.idViagens,
      'idParadas': self.idParadas,
      'idViagensParadas': self.idViagensParadas
    }
    return json_viagensParadas

  @staticmethod
  def from_json(json_viagensParadas):
    idViagens = json_viagensParadas.get('idViagens')
    idParadas = json_viagensParadas.get('idParadas')
    # idViagensParadas = json_viagensParadas.get('idViagensParadas')
    return ViagensParada(idViagens=idViagens, idParadas=idParadas)

  