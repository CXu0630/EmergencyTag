from smartcard.System import readers
from smartcard.util import toHexString
import sys
import nfc
import struct
import time
import EmInfoLength

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

def process_info_str(category, info):
    em_info = EmInfoLength()
    #trim string
    trimmed_info = em_info.trim_string(category, info)
    #convert the processed string to byte
    info_byte = trimmed_info.encode('utf-8')
    return info_byte

def write_category(connection, category, info):
    """
    Write the information into the given category to the NFC card.
    """
    em_info_dict = EmInfoLength()
    info_bytes = process_info_str(category, info)

    # Pad the info_bytes to make it a multiple of 4 bytes
    while len(info_bytes) % 4 != 0:
        info_bytes += b'\x00'
    
    # Split the info_bytes into 4-byte chunks
    pages = [info_bytes[i:i+4] for i in range(0, len(info_bytes), 4)]
    
    # Starting page (e.g., page 4 for user data in NTAG213)
    starting_page = em_info_dict[category][0]
    
    for i, page in enumerate(pages):
        page_number = starting_page + i
        data = list(page)
        write_page(connection, page_number, data)
        
    
