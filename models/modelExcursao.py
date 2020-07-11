from banco import db

class Excursao(db.Model):
    __tablename__ = 'excursoes'
    idExcursoes = db.Column(db.Integer, autoincrement=True, primary_key=True)
    dataPartida = db.Column(db.String(10), nullable=False)
    dataChegada = db.Column(db.String(10), nullable=False)
    detalheExcursoes = db.Column(db.String(200), nullable=False)
    foto = db.Column(db.String(300), nullable=False)
    numeroClics = db.Column(db.Integer, nullable=True)

    idViagens = db.Column(db.Integer, db.ForeignKey(
        'viagens.idViagens'), nullable=False)

    viagens = db.relationship('Viagem')

    def to_json(self):
        json_excursoes = {
            'idExcursoes': self.idExcursoes,
            'dataPartida': self.dataPartida,
            'dataChegada': self.dataChegada,
            'detalheExcursoes': self.detalheExcursoes,
            'idViagens': self.idViagens,
            'foto': self.foto,
            'numeroClics': self.numeroClics,
        }
        return json_excursoes

    @staticmethod
    def from_json(json_excursoes):
        dataPartida = json_excursoes.get('dataPartida')
        dataChegada = json_excursoes.get('dataChegada')
        detalheExcursoes = json_excursoes.get('detalheExcursoes')
        idViagens = json_excursoes.get('idViagens')
        foto = json_excursoes.get('foto')
        numeroClics = json_excursoes.get('numeroClics')
        return Excursao(dataPartida=dataPartida, dataChegada=dataChegada, detalheExcursoes=detalheExcursoes, idViagens=idViagens, foto=foto, numeroClics=numeroClics)