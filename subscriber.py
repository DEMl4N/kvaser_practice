import paho.mqtt.client as mqtt
import os, base64, time
from kvaser_can import Kvaser, split_data_into_chunks

topic_name = "file_name"
topic_file = "file"
topic_sender = "user"
userId = "admin"
userPw = "1234"
broker_ip = "192.168.0.3"

file_name = None
file_data = None
sender = None

def on_connect(client, userdata, flags, reasonCode):
    if (reasonCode == 0):
        print("Connected")
        client.subscribe(topic_name)
        client.subscribe(topic_file)
        client.subscribe(topic_sender)

    else:
        print("Error: connection failed:", reasonCode)


def on_disconnect(client, userdata, flags, reasonCode = 0):
    print("Disconnected: ", reasonCode)


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        topic = msg.topic

        global file_name, file_data, sender
        if (topic == topic_file):
            file_data = base64.b64decode(payload)
        elif (topic == topic_name):
            file_name = payload
        elif (topic == topic_sender):
            sender = payload
            print("[+] Sender: ", sender)

        if file_data and file_name and sender:
            user_confirm = input("[!] Update file received. Press 'y' to continue: ")
            if (user_confirm != 'y'):
                return
            tmp_dir = os.path.join(os.getcwd(), "temporary")
            os.makedirs(tmp_dir, exist_ok=True)
            file_path = os.path.join(tmp_dir, file_name)
            with open(file_path, "wb") as file:
                file.write(file_data)
            print("[+] File Received: ", file_name)

            with open(file_path, "rb") as file:
                data = file.read()
            
            message = file_name.encode('utf-8') + b':' + file_data
            flag = 1
            while(flag):
                try:
                    send_file(message)
                    flag = 0
                except:
                    print("Retrying sending file")
                    time.sleep(3)
            
    except Exception as e:
        print("Error: ", e)


def send_file(message):
    transmitter = Kvaser()
    chunks = split_data_into_chunks(message)
    for chunk in chunks:
        transmitter.transmit_data(123, chunk)
        print(chunk)
        time.sleep(0.02)

def main():
    client = mqtt.Client()
    client.username_pw_set(userId, userPw)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(broker_ip, port=1883, keepalive=60)
    client.loop_forever()

if __name__ == "__main__":
    main()