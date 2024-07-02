from flask import Blueprint, request, jsonify
from models import mysql

bp = Blueprint('kritikan', __name__)

@bp.route('/kritikan', methods=['POST'])
def create_kritikan():
    data = request.get_json()
    username = data.get('username')
    kritikan = data.get('kritikan')

    if not all([username, kritikan]):
        return jsonify({'message': 'Missing required parameters'}), 400

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO kritikan (username, kritikan) VALUES (%s, %s)", (username, kritikan))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'kritikan Kerja created successfully'})

@bp.route('/kritikan', methods=['GET'])
def get_all_kritikan():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM kritikan")
    kritikan_records = cur.fetchall()
    cur.close()

    kritikan_list = [{'id': record[0], 'username': record[1], 'kritikan': record[2]} for record in kritikan_records]
    return jsonify(kritikan_list)

@bp.route('/kritikan/<int:id>', methods=['GET'])
def get_kritikan(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM kritikan WHERE id = %s", (id,))
    kritikan = cur.fetchone()
    cur.close()

    if kritikan:
        return jsonify({'id': kritikan[0], 'username': kritikan[1], 'kritikan': kritikan[2]})
    else:
        return jsonify({'message': 'kritikan Kerja not found'}), 404

@bp.route('/kritikan/<int:id>', methods=['PUT'])
def update_kritikan(id):
    data = request.get_json()
    kritikan = data.get('kritikan')

    if not kritikan:
        return jsonify({'message': 'Missing kritikan parameter'}), 400

    cur = mysql.connection.cursor()
    cur.execute("UPDATE kritikan SET kritikan = %s WHERE id = %s", (kritikan, id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'kritikan Kerja updated successfully'})

@bp.route('/kritikan/<int:id>', methods=['DELETE'])
def delete_kritikan(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM kritikan WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'kritikan Kerja deleted successfully'})
