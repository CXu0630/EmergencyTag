from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.System import readers
from smartcard.util import toHexString
import sys
import nfc
import struct
import time

#print ("helloworld")
class NFCconnection:
    def __init__(self):
        self.reader = None
        self.connection = None
    #establish a connection with the nfc reader
    def connect_reader(self):
        r = readers()
        if len(r) == 0:
            print("No readers detected")
            sys.exit()
        #select the first reader
        self.reader = r[0]
        print(f"Using reader: {self.reader.__str__()}")
        #connect to the card
        reading_loop = True
        while(reading_loop):
            try:
                self.connection = self.reader.createConnection()
                self.connection.connect()
                print("Successfully connected to nfc card!")
                reading_loop = False
            except Exception as e:
                x = 0
            time.sleep(0.2)
    def disconnect(self):
        if self.connection.isConnected():
            self.connection.disconnect()
            print("Connection closed.")
def main():
    waiting_for_card = True
    while waiting_for_card:
        print("Waiting for card tab....")
        nfc_conn = NFCconnection()
        nfc_conn.connect_reader()
        time.sleep(1)
    nfc_conn.disconnect()
if __name__ == "__main__":
    main()