from flask import Blueprint, request, jsonify
from models import mysql

bp = Blueprint('absensi', __name__)

@bp.route('/absensi', methods=['POST'])
def create_absensi():
    data = request.get_json()
    username = data.get('username')
    date = data.get('date')
    status = data.get('status')

    if not all([username, date, status]):
        return jsonify({'message': 'Missing required parameters'}), 400

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO absensi (username, date, status) VALUES (%s, %s, %s)", (username, date, status))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'absensi created successfully'})

@bp.route('/absensi', methods=['GET'])
def get_all_absensi():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM absensi")
    absensi_records = cur.fetchall()
    cur.close()

    absensi_list = []
    for record in absensi_records:
        absensi_list.append({
            'id': record[0],
            'username': record[1],
            'date': record[2],
            'status': record[3]
        })

    return jsonify(absensi_list)

@bp.route('/absensi/<int:id>', methods=['GET'])
def get_absensi(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM absensi WHERE id = %s", (id,))
    absensi = cur.fetchone()
    cur.close()

    if absensi:
        return jsonify({'id': absensi[0], 'username': absensi[1], 'date': absensi[2], 'status': absensi[3]})
    else:
        return jsonify({'message': 'absensi not found'}), 404

@bp.route('/absensi/<int:id>', methods=['PUT'])
def update_absensi(id):
    data = request.get_json()
    status = data.get('status')

    if not status:
        return jsonify({'message': 'Missing status parameter'}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM absensi WHERE id = %s", (id,))
    absensi = cur.fetchone()

    if absensi:
        cur.execute("UPDATE absensi SET status = %s WHERE id = %s", (status, id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'absensi updated successfully'})
    else:
        cur.close()
        return jsonify({'message': 'absensi not found'}), 404

@bp.route('/absensi/<int:id>', methods=['DELETE'])
def delete_absensi(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM absensi WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'absensi deleted successfully'})
