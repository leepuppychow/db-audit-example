## Exploration with Kafka and creating audit logs for transactional DB

## Resources

* [Install kafka on MacOS with homebrew](https://medium.com/@Ankitthakur/apache-kafka-installation-on-mac-using-homebrew-a367cdefd273)

## Start Kafka server locally:

1. `zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties` - start Zookeeper service 
2. `kafka-server-start /usr/local/etc/kafka/server.properties` - start Kafka server

## Start Flask server
0. `virtualenv venv` - create virtualenv if you haven't already
1. `source ./initialize.sh`
2. `python app.py`

## Start Kafka consumer
1. `source ./initialize.sh`
2. `python kafka_consumer.py`

## TODOS:
* [Setup Change Data Capture (CDC) with Debezium?](https://info.crunchydata.com/blog/postgresql-change-data-capture-with-debezium)