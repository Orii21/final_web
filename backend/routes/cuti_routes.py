from flask import Blueprint, request, jsonify
from models import mysql

bp = Blueprint('cuti', __name__)

@bp.route('/cuti', methods=['POST'])
def create_cuti():
    try:
        data = request.get_json()
        username = data.get('username')
        tanggal_cuti = data.get('tanggal_cuti')
        tanggal_masuk = data.get('tanggal_masuk')
        alasan = data.get('alasan')
        status = data.get('status')

        if not all([username, tanggal_cuti, tanggal_masuk, alasan, status]):
            return jsonify({'message': 'Missing required parameters'}), 400

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO cuti (username, tanggal_cuti, tanggal_masuk, alasan, status) VALUES (%s, %s, %s, %s, %s)", (username, tanggal_cuti, tanggal_masuk, alasan, status))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Cuti created successfully'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/cuti', methods=['GET'])
def get_all_cuti():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cuti")
        cuti_records = cur.fetchall()
        cur.close()

        cuti_list = []
        for record in cuti_records:
            cuti_list.append({
                'id': record[0],
                'username': record[1],
                'tanggal_cuti': record[2].strftime('%Y-%m-%d'),
                'tanggal_masuk': record[3].strftime('%Y-%m-%d'),
                'alasan': record[4],
                'status': record[5]
            })

        return jsonify(cuti_list)
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/cuti/<int:id>', methods=['GET'])
def get_cuti(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cuti WHERE id = %s", (id,))
        cuti = cur.fetchone()
        cur.close()

        if cuti:
            return jsonify({
                'id': cuti[0],
                'username': cuti[1],
                'tanggal_cuti': cuti[2].strftime('%Y-%m-%d'),
                'tanggal_masuk': cuti[3].strftime('%Y-%m-%d'),
                'alasan': cuti[4],
                'status': cuti[5]
            })
        else:
            return jsonify({'message': 'Cuti not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/cuti/<int:id>', methods=['PUT'])
def update_cuti(id):
    try:
        data = request.get_json()
        status = data.get('status')

        if not status:
            return jsonify({'message': 'Missing status parameter'}), 400

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cuti WHERE id = %s", (id,))
        cuti = cur.fetchone()

        if cuti:
            cur.execute("UPDATE cuti SET status = %s WHERE id = %s", (status, id))
            mysql.connection.commit()
            cur.close()
            return jsonify({'message': 'Cuti updated successfully'})
        else:
            cur.close()
            return jsonify({'message': 'Cuti not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/cuti/<int:id>', methods=['DELETE'])
def delete_cuti(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM cuti WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Cuti deleted successfully'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500
