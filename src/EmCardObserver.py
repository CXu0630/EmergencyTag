from smartcard.CardMonitoring import CardObserver
from smartcard.util import toHexString
from smartcard.ATR import ATR

class EmCardObserver(CardObserver):
    def __init__(self):
        super().__init__() 
        self._events = {}
        self._events['add_card'] = []
        self._events['remove_card'] = []

    def update(self, observable, actions):
        (addedCards, removedCards) = actions
        for card in addedCards:
            print(f"Card inserted into reader: {card.reader}")
            try:
                # Connect to the card
                connection = card.createConnection()
                connection.connect()
                
                self.notify('add_card', connection)
                
                # Example: Get the ATR (Answer to Reset)
                # lstatr = connection.getATR()
                # atr = ATR(lstatr)
                # print (type(atr))
                # print(f"ATR: {toHexString(lstatr)}")
                # print('historical bytes: ', toHexString(atr.getHistoricalBytes()))
                # print('checksum: ', "0x%X" % atr.getChecksum())
                # print('checksum OK: ', atr.checksumOK)
                # print('T0  supported: ', atr.isT0Supported())
                # print('T1  supported: ', atr.isT1Supported())
                # print('T15 supported: ', atr.isT15Supported())
                
                # You can add more interactions with the card here
            except Exception as e:
                print(f"Failed to connect to the card: {e}")

        for card in removedCards:
            print(f"Card removed from reader: {card.reader}")
            self.notify('remove_card', None)
            
    def subscribe(self, event_name, fn):
        """Subscribe a function to a specific event."""
        if event_name not in self._events:
            self.register_event(event_name)
        if fn not in self._events[event_name]:
            self._events[event_name].append(fn)
            print(f"Subscribed '{fn.__name__}' to event '{event_name}'.")
        else:
            print(f"'{fn.__name__}' is already subscribed to event '{event_name}'.")

    def unsubscribe(self, event_name, fn):
        """Unsubscribe a function from a specific event."""
        if event_name in self._events and fn in self._events[event_name]:
            self._events[event_name].remove(fn)
            print(f"Unsubscribed '{fn.__name__}' from event '{event_name}'.")
        else:
            print(f"Subscription not found for '{fn.__name__}' in event '{event_name}'.")

    def notify(self, event_name, connection):
        """Notify all subscribers of a specific event."""
        if event_name in self._events:
            print(f"Event '{event_name}' triggered!")
            for subscriber in self._events[event_name]:
                subscriber(connection)
        else:
            print(f"No such event registered: '{event_name}'")