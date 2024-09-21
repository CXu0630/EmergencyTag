from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.ATR import ATR

class EmCardObserver(CardObserver):
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