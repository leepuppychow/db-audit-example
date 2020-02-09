## Resources

* [Install kafka on MacOS with homebrew](https://medium.com/@Ankitthakur/apache-kafka-installation-on-mac-using-homebrew-a367cdefd273)

## Starting Kafka locally:

1. `zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties` - start Zookeeper service 
2. `kafka-server-start /usr/local/etc/kafka/server.properties` - start Kafka server

## Starting Flask server
1. `virtualenv venv` - create virtualenv if you haven't already
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `source env.sh`
5. `python app.py`