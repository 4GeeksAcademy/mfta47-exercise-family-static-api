"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
john = {
    "id": 1,
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}

jane = {
    "id": 2,
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}

jimmy = {
    "id": 3,
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
}

jackson_family.add_member(john)
jackson_family.add_member(jane)
jackson_family.add_member(jimmy)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_members():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members

    return jsonify(response_body), 200


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"message": "Member not found"}), 404


@app.route('/member', methods=['POST'])
def add_member():
    # this is how you can use the Family datastructure by calling its methods
    body = request.get_json()
    if not body:
        return jsonify({"message": "Invalid data"}), 400
    if "first_name" not in body:
        return jsonify({"message": "first_name is required"}), 400
    if "age" not in body:
        return jsonify({"message": "age is required"}), 400
    if "lucky_numbers" not in body:
        return jsonify({"message": "lucky_numbers is required"}), 400

    additional_info = {
        "id": body.get("id", jackson_family._generateId()),
        "last_name": jackson_family.last_name
    }
    body.update(additional_info)

    member = jackson_family.add_member(body)
    return jsonify(member), 200


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    # this is how you can use the Family datastructure by calling its methods
    deleted = jackson_family.delete_member(member_id)
    if deleted:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"message": "Member not found"}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
