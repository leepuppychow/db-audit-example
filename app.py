import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, abort
import psycopg2

db_host = os.environ.get('DB_HOST')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_transactional_name = os.environ.get('DB_TRANSACTIONAL_NAME')
db_audit_name = os.environ.get('DB_AUDIT_NAME')

transactional_conn = psycopg2.connect(
  dbname=db_transactional_name,
  user=db_user,
  password=db_password,
  host=db_host
)
transactional_cur = transactional_conn.cursor()
audit_conn = psycopg2.connect(
  dbname=db_audit_name,
  user=db_user,
  password=db_password,
  host=db_host
)
audit_cur = audit_conn.cursor()

app = Flask(__name__)

@app.route("/ping")
def ping():
  return jsonify({'message': 'yay'})

@app.route("/dog")
def home():
  try:
    transactional_cur.execute("SELECT * FROM dog")
    rows = transactional_cur.fetchall()
    dogs = [{'id': row[0], 'name': row[1]} for row in rows]

    audit_cur.execute("SELECT * FROM audit")
    rows = audit_cur.fetchall()
    audits = [{
      'id': row[0],
      'action': row[1],
      'query': row[2],
      'schema': row[3],
      'old_data': row[4],
      'new_data': row[5],
      'table_name': row[6],
    } for row in rows]

    return render_template('home.html', dogs=dogs, audits=audits)
  except Exception as err:
    print(err)
    abort(500)

@app.route("/dog", methods=['POST'])
def create_dog():
  dog_name = request.form.get('dog_name')
  try:
    if dog_name:
      transactional_cur.execute("INSERT INTO dog (name) values (%s)", (dog_name,))
      transactional_conn.commit()
    return redirect(url_for("home"))
  except Exception as err:
    print(err)
    abort(500)

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5000)