import os, json
from kafka import KafkaConsumer
import psycopg2
from psycopg2.extras import Json

host = os.environ.get('HOST')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_audit_name = os.environ.get('DB_AUDIT_NAME')

audit_conn = psycopg2.connect(
  dbname=db_audit_name,
  user=db_user,
  password=db_password,
  host=host
)
audit_cur = audit_conn.cursor()

consumer = KafkaConsumer('audit')

for message in consumer:
    data = json.loads(message.value)
    audit_cur.execute(
      "INSERT INTO audit (action, schema, old_data, new_data, table_name) values (%s,%s,%s,%s,%s)",
      (
        data.get('action'),
        data.get('schema'),
        Json(data.get('old_data')),
        Json(data.get('new_data')),
        data.get('table_name'),
      )
    )
    audit_conn.commit()