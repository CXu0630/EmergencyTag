from smartcard.CardMonitoring import CardMonitor
from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.ATR import ATR
import sys

from EmCardObserver import EmCardObserver

class NfcConnecter:
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
        
        self.observer.subscribe("add_card", self.writeOnConnection)

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
        write_cardholder_name(connection, "Chloe X")
        
def write_page(connection, page_number, data_bytes):
    """
    Write 4 bytes of data to a specific page.
    """
    if len(data_bytes) != 4:
        raise ValueError("Data must be exactly 4 bytes.")
    
    # Construct the APDU command
    # Example for ACR122U: CLA=FF, INS=D6, P1=00, P2=page_number, Lc=04, Data=4 bytes
    apdu = [0xFF, 0xD6, 0x00, page_number, 0x04] + data_bytes
    print(f"Sending APDU: {toHexString(apdu)}")
    
    # Send the APDU
    response, sw1, sw2 = connection.transmit(apdu)
    
    # Check response status
    if sw1 == 0x90 and sw2 == 0x00:
        print(f"Successfully wrote to page {page_number}.")
    else:
        print(f"Failed to write to page {page_number}. Status: {sw1:02X} {sw2:02X}")

def write_cardholder_name(connection, name):
    """
    Write the cardholder's name to the NFC card.
    Assumes the name is short enough to fit within available pages.
    """
    # Convert the name to bytes (UTF-8 encoding)
    name_bytes = name.encode('utf-8')
    
    # Pad the name_bytes to make it a multiple of 4 bytes
    while len(name_bytes) % 4 != 0:
        name_bytes += b'\x00'
    
    # Split the name into 4-byte chunks
    pages = [name_bytes[i:i+4] for i in range(0, len(name_bytes), 4)]
    
    # Starting page (e.g., page 4 for user data in NTAG213)
    starting_page = 4
    
    for i, page in enumerate(pages):
        page_number = starting_page + i
        data = list(page)
        write_page(connection, page_number, data)