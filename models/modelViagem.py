
from banco import db

class Viagem(db.Model):
  __tablename__ = 'viagens'
  idViagens = db.Column(db.Integer, autoincrement=True, primary_key=True)
  horaPartida = db.Column(db.String(10), nullable=False)
  horaChegada = db.Column(db.String(10), nullable=False)
  cidadePartida = db.Column(db.String(45), nullable=False)
  cidadeChegada = db.Column(db.String(45), nullable=False)
  valor = db.Column(db.Float, nullable=False)
  tipoViagem = db.Column(db.Integer, nullable=False)

  def to_json(self):
    json_viagens = {
      'idViagens': self.idViagens,
      'horaPartida': self.horaPartida,
      'horaChegada': self.horaChegada,
      'cidadePartida': self.cidadePartida,
      'cidadeChegada': self.cidadeChegada,
      'valor': self.valor,
      'tipoViagem': self.tipoViagem
    }
    return json_viagens

  @staticmethod
  def from_json(json_viagens):
    horaPartida = json_viagens.get('horaPartida')
    horaChegada = json_viagens.get('horaChegada')
    cidadePartida = json_viagens.get('cidadePartida')
    cidadeChegada = json_viagens.get('cidadeChegada')
    valor = json_viagens.get('valor')
    tipoViagem = json_viagens.get('tipoViagem')
    return Viagem(horaPartida=horaPartida, horaChegada=horaChegada, cidadePartida=cidadePartida, cidadeChegada=cidadeChegada, valor=valor, tipoViagem=tipoViagem)
