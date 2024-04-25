from flask  import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from marshmallow import Schema, fields


app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:myadmin123*/@localhost/petdb' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __init__(self, name, category, status):
        self.name = name
        self.category = category
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'status': self.status
        }  

class PetSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    category = fields.String()
    status = fields.String()

pet_schema = PetSchema(many=True)

@app.route('/pet',methods=['POST'])
def add_pet():
    name=request.json['name']
    category=request.json['category']
    status=request.json['status']

    new_pet=Pet(name,category,status)

    db.session.add(new_pet)
    db.session.commit()
    return jsonify({'message': 'Pet added successfully'}), 200

@app.route('/pet', methods=['GET'])
def get_all_pets():
    pets = Pet.query.all()
    pet_dict = [pet.to_dict() for pet in pets]
    return jsonify({'pets': pet_dict}), 200


@app.route('/pet/<id>', methods=['GET'])
def get_pet(id):
    pet = db.session.get(Pet,id)
    if pet is None:
        return jsonify({'message': 'Pet not found'}), 404
    #pet_data = pet_schema.dump(pet)
    #return jsonify({'pet': pet_data})
    return jsonify({'pet': pet.to_dict()})


   # db.session.commit()



@app.route('/pet/<id>', methods=['PUT'])
def change_pet(id):
    pet = Pet.query.get(id)
    if pet is None:
        return jsonify({'message': 'Pet not found'}), 404

    name = request.json['name']
    category = request.json['category']
    status = request.json['status']

    pet.name = name
    pet.category = category
    pet.status = status

    db.session.commit()

    return pet_schema.jsonify(pet)



@app.route('/pet/<id>', methods=['POST'])
def update_pet(id):
    pet = Pet.query.get(id)
    if pet is None:
        return jsonify({'message': 'Pet not found'}), 404
    
    
    pet.name = request.form.get('name', pet.name)
    pet.category = request.form.get('category', pet.category)
    pet.status = request.form.get('status', pet.status)

    db.session.commit()
    return jsonify({'message': 'Pet updated successfully'}), 200


@app.route('/pet/<id>', methods=['DELETE'])
def delete_pet(id):
    pet = Pet.query.get(id)
    if pet is None:
        return jsonify({'message': 'Pet not found'}), 404
    
    db.session.delete(pet)
    db.session.commit()
    return jsonify({'message': 'Pet deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)

