from smartcard.CardMonitoring import CardMonitor
from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.ATR import ATR
import sys

from EmCardObserver import EmCardObserver
import NfcWriter
import NfcReader

class NfcConnecter:
    def __init__(self):
        self.monitor = None
        self.observer = None

    def start(self):
        available_readers = None
        try:
            available_readers= readers()
        except:
            print('error listing readers')

        if not available_readers:
            print("No smart card readers found. Please connect a reader and try again.")
            sys.exit(1)

        # print("Available readers:")
        # for reader in available_readers:
        #     print(f" - {reader}")

        # Set up the card monitor and observer
        try:    
            self.monitor = CardMonitor()
            self.observer = EmCardObserver()
            self.monitor.addObserver(self.observer)
        
            self.observer.subscribe("add_card", self.readOnConnection)
        except Exception as e:
            print(f"\nError creating monitor and observer, {e}")

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

    def writeOnConnection(self, connection):
        NfcWriter.write_category(connection, "name", "Chloe X")
        
    def readOnConnection(self, connection):
        print(NfcReader.read_category(connection, "name"))