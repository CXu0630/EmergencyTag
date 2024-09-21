from smartcard.System import readers
from smartcard.util import toHexString
import sys
import nfc
import struct
import time

def into_byte(info):
    if type(info) != str:
        print("Value input should be a string.")
        exit()
    b = info.to('utf-8')
    return b

def write_info(card, page, info_byte):
    return
    
