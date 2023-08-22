from flask import Flask, request, jsonify, make_response, render_template, redirect
from flask_pymongo import PyMongo
from os import environ

app = Flask(__name__)

# Configure the MongoDB URI
app.config['MONGO_URI'] = environ.get('MONGO_URI')

mongo = PyMongo(app)  # Initialize PyMongo with your Flask app

@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)

# Create a new patient
@app.route('/patients', methods=['POST'])
def create_patient():
    try:
        data = request.get_json()
        patients_collection = mongo.db.patients  # Access the 'patients' collection in MongoDB
        new_patient = {
            'name': data['name'],
            'age': data['age'],
            'gender': data['gender'],
            # Add other patient information as needed
        }
        result = patients_collection.insert_one(new_patient)  # Insert the new patient document
        patient_id = str(result.inserted_id)  # Convert the ObjectId to a string
        return make_response(jsonify({'message': 'patient created', 'id': patient_id}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'error creating patient', 'error': str(e)}), 500)

# Get all patients
@app.route('/get-patients', methods=['GET'])
def get_patients():
    try:
        patients_collection = mongo.db.patients  # Access the 'patients' collection in MongoDB
        patients = patients_collection.find()  # Retrieve all patient documents
        patient_list = [{'id': str(patient['_id']), 'name': patient['name'], 'age': patient['age'], 'gender': patient['gender']} for patient in patients]
        return make_response(jsonify({'patients': patient_list}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting patients', 'error': str(e)}), 500)

# Get a specific patient by ID
@app.route('/patients/<string:id>', methods=['GET'])
def get_patient(id):
    try:
        patients_collection = mongo.db.patients  # Access the 'patients' collection in MongoDB
        patient = patients_collection.find_one({'_id': id})  # Find a patient by ID
        if patient:
            patient_data = {'id': str(patient['_id']), 'name': patient['name'], 'age': patient['age'], 'gender': patient['gender']}
            return make_response(jsonify({'patient': patient_data}), 200)
        return make_response(jsonify({'message': 'patient not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting patient', 'error': str(e)}), 500)

# Update a specific patient by ID
@app.route('/patients/<string:id>', methods=['PUT'])
def update_patient(id):
    try:
        data = request.get_json()
        patients_collection = mongo.db.patients  # Access the 'patients' collection in MongoDB
        updated_patient = {
            'name': data['name'],
            'age': data['age'],
            'gender': data['gender'],
            # Update other patient information as needed
        }
        result = patients_collection.update_one({'_id': id}, {'$set': updated_patient})  # Update the patient document
        if result.modified_count > 0:
            return make_response(jsonify({'message': 'patient updated'}), 200)
        return make_response(jsonify({'message': 'patient not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error updating patient', 'error': str(e)}), 500)

# Delete a specific patient by ID
@app.route('/patients/delete/<string:id>', methods=['DELETE'])
def delete_patient(id):
    try:
        patients_collection = mongo.db.patients  # Access the 'patients' collection in MongoDB
        result = patients_collection.delete_one({'_id': id})  # Delete the patient document
        if result.deleted_count > 0:
            return make_response(jsonify({'message': 'patient deleted'}), 200)
        return make_response(jsonify({'message': 'patient not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting patient', 'error': str(e)}), 500)
    

@app.route('/create', methods=['GET'])
def create_patient_form():
    # Add a link to the patients page
    patients_link = '<a href="/patients-list" class="btn btn-primary">View Patients</a>'
    
    # Combine the link with your HTML template (assuming your existing template is stored in 'index.html')
    return render_template('index.html', patients_link=patients_link)
    



@app.route('/delete-patients', methods=['POST'])
def delete_patients():
    try:
        patient_id = request.form.get('patient_id')
        if patient_id:
            patients_collection = mongo.db.patients
            result = patients_collection.delete_one({'_id': patient_id})
            if result.deleted_count > 0:
                return redirect('/patients-list')  # Redirect back to the patient list page after deletion
            return make_response(jsonify({'message': 'patient not found'}), 404)
        else:
            return make_response(jsonify({'message': 'invalid request'}), 400)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting patient', 'error': str(e)}), 500)

        

@app.route('/patients-list', methods=['GET'])
def patients_list():
    try:
        patients_collection = mongo.db.patients
        patients = patients_collection.find()
        patient_list = [{'id': str(patient['_id']), 'name': patient['name'], 'age': patient['age'], 'gender': patient['gender']} for patient in patients]
        return render_template('patients.html', patients=patient_list)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting patients', 'error': str(e)}), 500)







        
        
        
