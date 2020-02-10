import os, json
from flask import Flask, jsonify, render_template, request, redirect, url_for, abort
import psycopg2
from kafka import KafkaProducer

host = os.environ.get('HOST')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_transactional_name = os.environ.get('DB_TRANSACTIONAL_NAME')
db_audit_name = os.environ.get('DB_AUDIT_NAME')
kafka_server_port = os.environ.get('KAFKA_SERVER_PORT')

transactional_conn = psycopg2.connect(
  dbname=db_transactional_name,
  user=db_user,
  password=db_password,
  host=host
)
transactional_cur = transactional_conn.cursor()
audit_conn = psycopg2.connect(
  dbname=db_audit_name,
  user=db_user,
  password=db_password,
  host=host
)
audit_cur = audit_conn.cursor()

producer = KafkaProducer(bootstrap_servers=f"{host}:{kafka_server_port}")

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
      'schema': row[2],
      'old_data': row[3],
      'new_data': row[4],
      'table_name': row[5],
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

      kafka_message = json.dumps({
        "action": "INSERT",
        "schema": "",
        "table_name": "dog",
        "old_data": {},
        "new_data": {"name": dog_name},
      })
        producer.send('audit', bytes(kafka_message, 'ascii')) # This sends an "audit" topic to the Kafka server
    return redirect(url_for("home"))
  except Exception as err:
    print(err)
    abort(500)

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5000)