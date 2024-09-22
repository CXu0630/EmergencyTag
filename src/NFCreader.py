from smartcard.util import toHexString
from smartcard.CardConnection import CardConnection
from EmInfoLength import EmInfoLength
import AesCtr

class NfcReader:
    def __init__(self, connection):
        self.nonce = None
        self.connection = connection
        self.read_nonce()

    def read_page(self, page_number):
        """
        Read 4 bytes of data from a specific page.
        """
        # Construct the APDU command
        # Example for ACR122U: CLA=FF, INS=B0, P1=00, P2=page_number, Le=04
        apdu = [0xFF, 0xB0, 0x00, page_number, 0x04]
    
        try:
            response, sw1, sw2 = self.connection.transmit(apdu)
        except:
            print("Trying to reestablish connection.")
            self.connection.reconnect()
            response, sw1, sw2 = self.connection.transmit(apdu)
    
        if sw1 == 0x90 and sw2 == 0x00:
            return response
        else:
            print(f"Failed to read page {page_number}. Status: {sw1:02X} {sw2:02X}")
            return None

    def read_category(self, category):
        """
        Read the string stored on pages allocated to a specific category from the NFC card.
        """
        info_len = EmInfoLength()

        str_bytes = bytearray()
        num_pages = info_len.get_num_pages(category)
        starting_page = info_len.get_start_page(category)
    
        for i in range(num_pages):
            page_number = starting_page + i
            data = self.read_page(page_number)
            if data:
                str_bytes.extend(data)
            else:
                break
    
        print(str_bytes)
        text = None

        try:
            text = AesCtr.aes_ctr_decrypt(self.nonce, str_bytes.replace(b'\x00', b''))
        except:
            text = None
            
        return text
    
    def read_nonce(self):
        info_len = EmInfoLength()

        str_bytes = bytearray()
        num_pages = info_len.get_num_pages("nonce")
        starting_page = info_len.get_start_page("nonce")

        for i in range(num_pages):
            page_number = starting_page + i
            data = self.read_page(page_number)
            if data:
                str_bytes.extend(data)
            else:
                break
           
        self.nonce = str_bytes
