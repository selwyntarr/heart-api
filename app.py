from flask import Flask
from flask import request, jsonify
from flask import render_template
import pandas as pd 
import numpy as np
import json

app = Flask(__name__)

@app.route("/heart", methods=["POST"])
def add_heart_record():
    #read data from json file
    with open("heart.json", "r") as read_file:
        dataset = json.load(read_file)
    
    #read data from request body 
    data = request.get_json()

    #append the data to json file
    counter = len(dataset)+1
    data["heart_id"] = counter
    dataset.append(data)
    with open("heart.json", "w") as write_file:
        json.dump(dataset, write_file)

    return 'New heart record added, heart_id: {counter}', 204

@app.route("/heart/all", methods=["GET"])
def get_heart_record_all():
    #read data from json file
    with open("heart.json", "r") as read_file:
        dataset = json.load(read_file)
    
    return jsonify(dataset), 201

@app.route("/heart/<id>", methods=["GET"])
def get_heart_record(id):
    #read data from json file
    with open("heart.json", "r") as read_file:
        dataset = json.load(read_file)

    #search heart_id
    for data in dataset:
        if data["heart_id"] == int(id):
            return jsonify(data), 200
    
    return 'No Matching Record', 403

@app.route("/heart/update/<id>", methods=["PUT"])
def update_heart_record(id):
    #read data from json file
    with open("heart.json", "r") as read_file:
        dataset = json.load(read_file)

    #read data from request body
    updated_data = request.get_json()

    #search heart_id
    for data in dataset:
        if data["heart_id"] == int(id):
            #update the data from body
            data["heart_rate"] = updated_data["heart_rate"]
            data["date"] = updated_data["date"]

            #overwrite heart.json with updated data
            with open("heart.json", "w") as write_file:
                json.dump(dataset, write_file)
            return f'Heart record with heart_id: {id} has been updated', 204
        
    return 'No Matching Record', 403

@app.route("/heart/delete/<id>", methods=["DELETE"])
def delete_heart_record(id):
    #read data from json file
    with open("heart.json", "r") as read_file:
        dataset = json.load(read_file)

    #search heart_id
    for data in dataset:
        if data["heart_id"] == int(id):
            #delete with matching heart id
            dataset.pop(dataset.index(data))

        #overwrite heart.json with updated data
        with open("heart.json", "w") as write_file:
            json.dump(dataset, write_file)

        return f'Heart record with heart_id: {id} has been deleted', 204

    return 'No Matching Record', 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)