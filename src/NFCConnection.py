from smartcard.CardMonitoring import CardMonitor
from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.ATR import ATR
import sys

import EmCardObserver

class NfcConnection:
    def __init__(self):
        self.monitor = None
        self.observer = None

    def start(self):
        available_readers = readers()
        if not available_readers:
            print("No smart card readers found. Please connect a reader and try again.")
            sys.exit(1)

        print("Available readers:")
        for reader in available_readers:
            print(f" - {reader}")

        # Set up the card monitor and observer
        self.monitor = CardMonitor()
        self.observer = EmCardObserver()
        self.monitor.addObserver(self.observer)

        print("\nMonitoring card events. Press Ctrl+C to exit.\n")

        try:
            while True:
                pass  # Keep the script running
        except KeyboardInterrupt:
            self.exit()
    
    def exit(self):
        print("\nExiting...")
        self.monitor.deleteObserver(self.observer)
        sys.exit(0)

    # #establish a connection with the nfc reader
    # def connect_reader(self):
    #     r = readers()
    #     if len(r) == 0:
    #         print("No readers detected")
    #         sys.exit()
    #     #select the first reader
    #     self.reader = r[0]
    #     print(f"Using reader: {self.reader.__str__()}")
    #     #connect to the card
    #     reading_loop = True
    #     while(reading_loop):
    #         try:
    #             self.connection = self.reader.createConnection()
    #             self.connection.connect()
    #             print("Successfully connected to nfc card!")
    #             reading_loop = False
    #         except Exception as e:
    #             x = 0
    #         time.sleep(0.2)
    # def disconnect(self):
    #     if self.connection.isConnected():
    #         self.connection.disconnect()
    #         print("Connection closed.")