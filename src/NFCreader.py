from smartcard.util import toHexString
from EmInfoLength import EmInfoLength

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

def read_category(connection, category):
    """
    Read the string stored on pages allocated to a specific category from the NFC card.
    """
    info_len = EmInfoLength()

    str_bytes = bytearray()
    num_pages = info_len.get_num_pages(category)
    starting_page = info_len.get_start_page(category)
    
    for i in range(num_pages):
        page_number = starting_page + i
        data = read_page(connection, page_number)
        if data:
            str_bytes.extend(data)
        else:
            break
    
    # Remove padding null bytes
    text = str_bytes.decode('utf-8').rstrip('\x00')
    return text