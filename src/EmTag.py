from os import write
from NfcConnecter import NfcConnecter
from UITest import UserInterface
import sys
from PyQt5.QtWidgets import QApplication

from NfcWriter import NfcWriter

def write_on_tap(connection):
    temp_writer = NfcWriter(connection)
    
    temp_writer.write_nonce()
    temp_writer.write_category("name", "Chloe X")
    temp_writer.write_category("blood_type", "O")
    temp_writer.write_category("em_contact", "1231231234")
    temp_writer.write_category("birth_date", "20000630")
    temp_writer.write_category("allergies", "mango")
    temp_writer.write_category("med_history", "diabetes")

def main():
    nfcConnecter = NfcConnecter()
    nfcConnecter.start()
    
    app = QApplication(sys.argv)
    window = UserInterface()
    window.show()

    nfcConnecter.observer.add_card_signal.connect(write_on_tap)
    nfcConnecter.observer.add_card_signal.connect(window.add_card_handler)
    nfcConnecter.observer.remove_card_signal.connect(window.remove_card_handler)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()