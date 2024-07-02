from flask import Blueprint, request, jsonify
from models import mysql  # Pastikan import model mysql sesuai dengan struktur aplikasi Anda

bp = Blueprint('gaji', __name__)

@bp.route('/gaji', methods=['POST'])
def create_gaji():
    data = request.get_json()
    username = data.get('username')
    gaji = data.get('gaji')
    status = data.get('status')

    if not all([username, gaji, status]):
        return jsonify({'message': 'Missing required parameters'}), 400

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO gaji (username, gaji, status) VALUES (%s, %s, %s)", (username, gaji, status))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Gaji created successfully'})

@bp.route('/gaji', methods=['GET'])
def get_all_gaji():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM gaji")
    gaji_records = cur.fetchall()
    cur.close()

    gaji_list = [{'id': record[0], 'username': record[1], 'gaji': record[2], 'status': record[3]} for record in gaji_records]
    return jsonify(gaji_list)

@bp.route('/gaji/<int:id>', methods=['GET'])
def get_gaji(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM gaji WHERE id = %s", (id,))
    gaji = cur.fetchone()
    cur.close()

    if gaji:
        return jsonify({'id': gaji[0], 'username': gaji[1], 'gaji': gaji[2], 'status': gaji[3]})
    else:
        return jsonify({'message': 'Gaji not found'}), 404

@bp.route('/gaji/<int:id>', methods=['PUT'])
def update_gaji(id):
    data = request.get_json()
    gaji = data.get('gaji')
    status = data.get('status')

    if not gaji and not status:
        return jsonify({'message': 'Missing parameters'}), 400

    cur = mysql.connection.cursor()
    if gaji:
        cur.execute("UPDATE gaji SET gaji = %s WHERE id = %s", (gaji, id))
    if status:
        cur.execute("UPDATE gaji SET status = %s WHERE id = %s", (status, id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Gaji updated successfully'})

@bp.route('/gaji/<int:id>', methods=['DELETE'])
def delete_gaji(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM gaji WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Gaji deleted successfully'})
