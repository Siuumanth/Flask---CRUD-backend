from flask import Flask,jsonify,request
import requests,json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'


   # crreating db

db = SQLAlchemy(app)

class Drink(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),nullable=False,unique=True)
    desc=db.Column(db.String(120))

    def __repr__(self):
        return f'{self.name} - {self.desc}'

@app.route('/')
def home():
    return 'Nothings here yet'


@app.route('/drinks')
def get_drinks():
    drinks =Drink.query.all()
    output=[]
    for drink in drinks:
        drink_data={'name':drink.name,'desc':drink.desc}
        output.append(drink_data)

    return {"drinks":output}



@app.route('/drinks/<int:id>')
def get_drink(id):
    drink=Drink.query.get_or_404(id)

    return jsonify({"name":drink.name,"desc":drink.desc})


@app.route('/drinks/add',methods=['POST'])
def add_drink():
    drink=Drink(name=request.json['name'],desc=request.json['desc'])
    with app.app_context():
        db.session.add(drink)
        db.session.commit()
        db.session.refresh(drink)

    return {"id":drink.id}
    
@app.route('/drinks/del/',methods=['POST'])
def begone():
    data = request.json
    id=data["id"]


    drink=Drink.query.get(id)
    if drink is None:
        return {"error":"no drink found"}
   
    db.session.delete(drink)
    db.session.commit()
      

    return {"message":"deletion successful"}



    


if __name__=='__main__':
    app.run(debug=True)