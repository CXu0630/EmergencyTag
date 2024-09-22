from smartcard.util import toHexString
from smartcard.CardConnection import CardConnection
from EmInfoLength import EmInfoLength
import AesCtr

class NfcWriter:
    def __init__(self, connection, nonce = None):
        self.connection = connection
        if nonce == None:
            nonce = AesCtr.gen_nonce()
        self.nonce = nonce

    def write_page(self, page_number, data_bytes):
        """
        Write 4 bytes of data to a specific page.
        """
        if len(data_bytes) != 4:
            raise ValueError("Data must be exactly 4 bytes.")
    
        # Construct the APDU command
        # Example for ACR122U: CLA=FF, INS=D6, P1=00, P2=page_number, Lc=04, Data=4 bytes
        apdu = [0xFF, 0xD6, 0x00, page_number, 0x04] + data_bytes
    
        # Send the APDU
        try:
            response, sw1, sw2 = self.connection.transmit(apdu)
        except:
            print("Trying to reestablish connection.")
            self.connection.reconnect()
            response, sw1, sw2 = self.connection.transmit(apdu)
    
        # Check response status
        if sw1 == 0x90 and sw2 == 0x00:
            print(f"Successfully wrote to page {page_number}.")
        else:
            print(f"Failed to write to page {page_number}. Status: {sw1:02X} {sw2:02X}")

    def process_info_str(self, category, info):
        """
        trims input information to correct size, encryptes it with aes-ctr
        """
        em_info = EmInfoLength()
        #trim string
        trimmed_info = em_info.trim_string(category, info)
        #encrypt with aes into bytes
        info_byte = AesCtr.aes_ctr_encrypt(self.nonce, trimmed_info)
        return info_byte

    def write_category(self, category, info):
        """
        Write the information into the given category to the NFC card.
        """
        em_info = EmInfoLength()
        info_bytes = self.process_info_str(category, info)

        # Pad the info_bytes to make it a multiple of 4 bytes
        while len(info_bytes) < (em_info.get_num_pages(category) * 4):
            info_bytes += b'\x00'
    
        # Split the info_bytes into 4-byte chunks
        pages = [info_bytes[i:i+4] for i in range(0, len(info_bytes), 4)]
    
        # Starting page (e.g., page 4 for user data in NTAG213)
        starting_page = em_info.get_start_page(category)
    
        for i, page in enumerate(pages):
            page_number = starting_page + i
            data = list(page)
            self.write_page(page_number, data)
        
    def write_nonce(self):
        em_info = EmInfoLength()
        # Split the info_bytes into 4-byte chunks
        pages = [self.nonce[i:i+4] for i in range(0, len(self.nonce), 4)]
    
        # Starting page (e.g., page 4 for user data in NTAG213)
        starting_page = em_info.get_start_page('nonce')

        for i, page in enumerate(pages):
            page_number = starting_page + i
            data = list(page)
            self.write_page(page_number, data)