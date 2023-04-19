from flask import Flask
from flask import jsonify
from flask import request
import pymysql
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_cors import CORS
#WSGIRequestHandler.protocol_version = "HTTP/1.1"


USER = "root"
PW = "1q2w3e4r!"
URL = "127.0.0.1"
PORT = "3306"
DB = "lol_item"
engine = create_engine("mysql+pymysql://root:1q2w3e4r!@127.0.0.1:3306/lol_item")#.format(USER, PW, URL, PORT, DB)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


app = Flask(__name__)

CORS(app)

class item(Base):
    __tablename__ = 'item_recommand'
    my_champ = Column(Integer, primary_key=True)
    vs_champ = Column(Integer, primary_key=True)
    recommand_craft_1 = Column(Integer)
    recommand_craft_2 = Column(Integer)
    recommand_craft_3 = Column(Integer)
    recommand_value_1 = Column(Integer)
    recommand_value_2 = Column(Integer)
    recommand_value_3 = Column(Integer)


@app.route("/recommend", methods = ['GET'])
def get_itemname():
    my_champion = int(request.args.get('my_champion'))
    enemy_champion = int(request.args.get('enemy_champion'))
    result = db_session.query(item).all()
    for i in result:
        if i.my_champ == my_champion and i.vs_champ == enemy_champion :
            return jsonify(recommand_craft_1 = i.recommand_craft_1 , recommand_craft_2 = i.recommand_craft_2,recommand_craft_3 = i.recommand_craft_3,
                           recommand_value_1 = i.recommand_value_1 , recommand_value_2 = i.recommand_value_2,recommand_value_3 = i.recommand_value_3)
    return  jsonify(None)


if __name__ == "__main__":
    app.run(host='localhost', port=8080)