from paho.mqtt import client as mqtt_client
import time
import random
import requests
import os

sourceurl = os.environ.get("SOURCEURL", "http://nginx")
broker = os.environ.get("MQTTHOST", "mqtt")
port = 1883
topic = "test/topic"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt() -> mqtt_client:

    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    # client.loop_forever()
    client.loop_start()

    i = 0
    while True:
        i=i+1
        print(f"hello {i}")

        msg="Empty"
        try:
           # Make an HTTP GET request to http://nginx/
            response = requests.get(sourceurl)
            response.raise_for_status()   # If not a 200 code throw exception
            # Extract up to the first 40 characters from the response text
            msg = response.text[:40]
            print(f"HTTP GET request successful. Response: {msg}")
        except requests.exceptions.RequestException as e:
            print(f"HTTP GET request failed: {e}")

        msg=f"Message {i}: {msg}"
        client.publish("test/topic", msg)
        time.sleep(10)

if __name__ == '__main__':
    run()

