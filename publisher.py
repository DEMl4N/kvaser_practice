import paho.mqtt.client as mqtt
import os
import time
import base64

name_topic = "updates/name"
file_topic = "updates/file"
broker_ip = "192.168.65.223"


def on_connect(client, userdata, flags, reasonCode):
    if (reasonCode == 0):
        print("Connected")
    else:
        print("Error: connection failed:", reasonCode)


def on_disconnect(client, userdata, flags, reasonCode = 0):
    print("Disconnected: ", reasonCode)


def on_publish(client, userdata, mid):
    print("Message published: ", mid)


# def make_message(file_path):
#     try:
#         with open(file_path, "rb") as file:
#             message = base64.b64encode(file.read())
#         return message
#     except FileNotFoundError as e:
#         print("Error:", e)
#         raise

def make_message(msg):
    try:
        message = base64.b64encode(msg)
        return message
    except Exception as e:
        print("Error:", e)
        raise

def main(broker_ip, username, password, port=1883):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

    try:
        client.username_pw_set(username, password)
        client.connect(broker_ip, port)
        client.loop()
        
        message = ""
        while (message != "exit"):
            client.publish(make_message(message))
            print(f"Success sending message: ", message)

        client.disconnect()

    except Exception as e:
        print("Disconnected: ", e)

def send_file_to_broker(publish_file, broker_ip, username, password, port=1883):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

    try:
        client.username_pw_set(username, password)
        client.connect(broker_ip, port)
        client.loop_start()

        # message = make_message(publish_file)
        # file_name = os.path.basename(publish_file)
        # client.publish(name_topic, file_name, qos=0)
        # client.publish(file_topic, message, qos=1)
        # client.loop_stop()

        client.publish(make_message())

        print(f"Success sending file(updates/name): {file_name}")
        print(f"Success sending file(updates/file)")

        client.disconnect()

    except FileNotFoundError as e:
        print("File not found: ", e)

    except Exception as e:
        print("Error: ", e)

if __name__ == "__main__":
    main(broker_ip, "ABCDE", "HIHI")
