from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from smartcard.System import readers
from smartcard.ATR import ATR
import sys

class PrintCardObserver(CardObserver):
    def update(self, observable, actions):
        (addedCards, removedCards) = actions
        for card in addedCards:
            print(f"Card inserted into reader: {card.reader}")
            try:
                # Connect to the card
                connection = card.createConnection()
                connection.connect()
                
                # Example: Get the ATR (Answer to Reset)
                lstatr = connection.getATR()
                atr = ATR(lstatr)
                print (type(atr))
                print(f"ATR: {toHexString(lstatr)}")
                print('historical bytes: ', toHexString(atr.getHistoricalBytes()))
                print('checksum: ', "0x%X" % atr.getChecksum())
                print('checksum OK: ', atr.checksumOK)
                print('T0  supported: ', atr.isT0Supported())
                print('T1  supported: ', atr.isT1Supported())
                print('T15 supported: ', atr.isT15Supported())
                
                #write_cardholder_name(connection, "Chloe X")
                print(read_cardholder_name(connection))
                
                # You can add more interactions with the card here
            except Exception as e:
                print(f"Failed to connect to the card: {e}")

        for card in removedCards:
            print(f"Card removed from reader: {card.reader}")

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
        
def read_page(connection, page_number):
    """
    Read 4 bytes of data from a specific page.
    """
    # Construct the APDU command
    # Example for ACR122U: CLA=FF, INS=B0, P1=00, P2=page_number, Le=04
    apdu = [0xFF, 0xB0, 0x00, page_number, 0x04]
    print(f"Sending APDU: {toHexString(apdu)}")
    
    # Send the APDU
    response, sw1, sw2 = connection.transmit(apdu)
    
    if sw1 == 0x90 and sw2 == 0x00:
        return response
    else:
        print(f"Failed to read page {page_number}. Status: {sw1:02X} {sw2:02X}")
        return None

def read_cardholder_name(connection, starting_page=4, num_pages=5):
    """
    Read the cardholder's name from the NFC card.
    """
    name_bytes = bytearray()
    
    for i in range(num_pages):
        page_number = starting_page + i
        data = read_page(connection, page_number)
        if data:
            name_bytes.extend(data)
        else:
            break
    
    # Remove padding null bytes
    name = name_bytes.decode('utf-8').rstrip('\x00')
    return name

def main():
    available_readers = readers()
    if not available_readers:
        print("No smart card readers found. Please connect a reader and try again.")
        sys.exit(1)

    print("Available readers:")
    for reader in available_readers:
        print(f" - {reader}")

    # Set up the card monitor and observer
    monitor = CardMonitor()
    observer = PrintCardObserver()
    monitor.addObserver(observer)

    print("\nMonitoring card events. Press Ctrl+C to exit.\n")

    try:
        while True:
            pass  # Keep the script running
    except KeyboardInterrupt:
        print("\nExiting...")
        monitor.deleteObserver(observer)
        sys.exit(0)

if __name__ == "__main__":
    main()
