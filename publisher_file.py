import paho.mqtt.client as mqtt
import os
import time
import base64

topic_name = "file_name"
topic_file = "file"
topic_sender = "user"
broker_ip = "192.168.137.106"
username = "admin"
password = "1234"

def on_connect(client, userdata, flags, reasonCode):
    if (reasonCode == 0):
        print("Connected")
    else:
        print("Error: connection failed:", reasonCode)


def on_disconnect(client, userdata, flags, reasonCode = 0):
    print("Disconnected: ", reasonCode)


def on_publish(client, userdata, mid):
    print("Message published: ", mid)


def make_message(file_path):
    try:
        with open(file_path, "rb") as file:
            message = base64.b64encode(file.read())
        return message
    except FileNotFoundError as e:
        print("Error:", e)
        raise
    except Exception as e:
        raise

def send_file_to_broker(publish_file, broker_ip, username, password, port=1883):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

    try:
        client.username_pw_set(username, password)
        client.connect(broker_ip, port)
        client.loop_start()

        print(f"pubfile: {publish_file}")
        message = make_message(publish_file)
        file_name = os.path.basename(publish_file)
        client.publish(topic_sender, username, qos=2)
        client.publish(topic_name, file_name, qos=2)
        client.publish(topic_file, message, qos=2)
        client.loop_stop()

        # client.publish(make_message())

        print(f"Success sending file(file_name): {file_name}")
        print(f"Success sending file(file)")

        client.disconnect()

    except FileNotFoundError as e:
        print("File not found: ", e)

    except Exception as e:
        print("Error: ", e)

