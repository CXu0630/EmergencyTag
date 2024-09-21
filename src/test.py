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
                
                # You can add more interactions with the card here
            except Exception as e:
                print(f"Failed to connect to the card: {e}")

        for card in removedCards:
            print(f"Card removed from reader: {card.reader}")

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
