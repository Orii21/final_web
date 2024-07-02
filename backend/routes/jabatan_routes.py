from flask import Blueprint, request, jsonify
from models import mysql

bp = Blueprint('jabatan', __name__)

@bp.route('/jabatan', methods=['POST'])
def create_jabatan():
    data = request.get_json()
    username = data.get('username')
    jabatan = data.get('jabatan')

    if not all([username, jabatan]):
        return jsonify({'message': 'Missing required parameters'}), 400

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO jabatan (username, jabatan) VALUES (%s, %s)", (username, jabatan))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Jabatan created successfully'})

@bp.route('/jabatan', methods=['GET'])
def get_all_jabatan():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jabatan")
    jabatan_records = cur.fetchall()
    cur.close()

    jabatan_list = [{'id': record[0], 'username': record[1], 'jabatan': record[2]} for record in jabatan_records]
    return jsonify(jabatan_list)

@bp.route('/jabatan/<int:id>', methods=['GET'])
def get_jabatan(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jabatan WHERE id = %s", (id,))
    jabatan = cur.fetchone()
    cur.close()

    if jabatan:
        return jsonify({'id': jabatan[0], 'username': jabatan[1], 'jabatan': jabatan[2]})
    else:
        return jsonify({'message': 'Jabatan not found'}), 404

@bp.route('/jabatan/<int:id>', methods=['PUT'])
def update_jabatan(id):
    data = request.get_json()
    jabatan = data.get('jabatan')

    if not jabatan:
        return jsonify({'message': 'Missing jabatan parameter'}), 400

    cur = mysql.connection.cursor()
    cur.execute("UPDATE jabatan SET jabatan = %s WHERE id = %s", (jabatan, id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Jabatan updated successfully'})

@bp.route('/jabatan/<int:id>', methods=['DELETE'])
def delete_jabatan(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM jabatan WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Jabatan deleted successfully'})
