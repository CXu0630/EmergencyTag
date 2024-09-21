from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from smartcard.System import readers
from smartcard.ATR import ATR
import sys
import os
import AesCtr
from UI import UserInterface
import EmTag

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


def genKey():
    print(os.urandom(32))
    
def test_aes_ctr():
    nonce = AesCtr.gen_nonce()
    
    text = "this is the test text"
    
    cipher = AesCtr.aes_ctr_encrypt(nonce, text)
    print(cipher)
    print(len(cipher))

    decoded = AesCtr.aes_ctr_decrypt(nonce, cipher)
    print(decoded)
    print(len(decoded))




if __name__ == "__main__":
    test_aes_ctr()
