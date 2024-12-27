from canlib import canlib, Frame
from kvaser_can import Kvaser
import os

file_dir = "Downloads"

def receive_file():
    transmitter = Kvaser()
    msg = transmitter.read(123)
    
    if msg.id == 123:
        try:
            if msg.data == bytearray(b'\xff\x00\xff\x00\xff\x00\xff\x00'):
                flag = 1
                print("[+] Receiving file...")
                file = bytearray()
                while(flag):
                    msg = transmitter.read(123)
                    if msg.data == bytearray(b'\x00\xff\x00\xff\x00\xff\x00\xff'):
                        flag = 0
                    else:
                        file.extend(msg.data)
                    print("[+] Received Message: ", msg.data)
                
                SplitMessage = file.split(b":", 1)
                file_name = SplitMessage[0].decode("utf-8")
                file_data = SplitMessage[1]

                os.makedirs(file_dir, exist_ok=True)
                with open(os.path.join(file_dir, file_name), "wb") as f:
                    f.write(file_data)
                print("[+] Saved file: ", file_name)
                file.clear()

        except Exception as e:
            print("Error: ", e)

def main():
    while True:
        receive_file()

if __name__ == "__main__":
    main()