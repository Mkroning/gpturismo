from banco import db

class Comentario(db.Model):
  __tablename__ = 'comentarios'
  idComentarios = db.Column(db.Integer, autoincrement=True, primary_key=True)
  nomeComentario = db.Column(db.String(60), nullable=False)
  notaComentario = db.Column(db.Integer, nullable=False)
  avaliacao = db.Column(db.String(250), nullable=False)

  idExcursoes = db.Column(db.Integer, db.ForeignKey(
    'excursoes.idExcursoes'), nullable=False)

  excursoes = db.relationship('Excursao')

  def to_json(self):
    json_comentarios = {
      'idComentarios': self.idComentarios,
      'nomeComentario': self.nomeComentario,
      'notaComentario': self.notaComentario,
      'avaliacao': self.avaliacao,  
      'idExcursoes': self.idExcursoes
    }

    return json_comentarios

  @staticmethod
  def from_json(json_comentarios):
    nomeComentario = json_comentarios.get('nomeComentario')
    notaComentario = json_comentarios.get('notaComentario')
    avaliacao = json_comentarios.get('avaliacao')
    idExcursoes = json_comentarios.get('idExcursoes')
    return Comentario(nomeComentario=nomeComentario, notaComentario=notaComentario, avaliacao=avaliacao, idExcursoes=idExcursoes)
