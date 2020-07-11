from flask import Flask
from flask_cors import CORS, cross_origin
from config import config
from banco import db
from blacklist import blacklist
from resources.excursoes import excursoes
from resources.viagens import viagens
from resources.paradas import paradas
from resources.comentarios import comentarios
from resources.viagensParadas import viagensParadas
from resources.interesses import interesses
from resources.usuarios import usuarios
from blacklist import blacklist
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
jwt = JWTManager(app)
CORS(app)

app.register_blueprint(excursoes)
app.register_blueprint(viagens)
app.register_blueprint(paradas)
app.register_blueprint(comentarios)
app.register_blueprint(viagensParadas)
app.register_blueprint(usuarios)
app.register_blueprint(interesses)

# with app.app_context():
#     api = Api(app)
#     db.init_app(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('/')
def raiz():
    db.create_all()
    return '<h2>GP Turismo</h2>'


if __name__ == '__main__':
    app.run(debug=True)
