from smartcard.System import readers
from smartcard.util import toHexString
import sys
import nfc
import struct
import time

#print ("helloworld")
class NFCconnection:
    def _init_(self):
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
        print("Using reader: ", self.reader)
        #connect to the card
        reading_loop = 1
        while(reading_loop):
            try:
                self.connection = self.reader.createConnection()
                self.connection.connect()
                print("Successfully connected to nfc card!")
            except Exception as e:
                print("No connection established. Try again.")
            time.sleep(.2)
    def disconnect(self):
        if self.connection.isConnected():
            self.connection.disconnect()
            print("Connection closed.")