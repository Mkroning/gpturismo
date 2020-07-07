
from banco import db


class Interesse(db.Model):
  __tablename__ = 'interesses'
  idInteresse = db.Column(db.Integer, autoincrement=True, primary_key=True)
  email = db.Column(db.String(100), nullable=False)
  nome = db.Column(db.String(45), nullable=False)
  
  idExcursoes = db.Column(db.Integer, db.ForeignKey('excursao.idExcursoes'), nullable=False)
  excursao = db.relationship('Excursao')

  def to_json(self):
    json_interesses = {
      'idInteresse': self.idInteresse,
      'email': self.email,
      'nome': self.nome,
      'idExcursoes': self.idExcursoes
    }
    return json_interesses

  @staticmethod
  def from_json(json_interesses):
    email = json_interesses.get('email')
    nome = json_interesses.get('nome')
    idExcursoes = json_interesses.get('idExcursoes')
    return Interesse(email=email, nome=nome, idExcursoes=idExcursoes)
    
