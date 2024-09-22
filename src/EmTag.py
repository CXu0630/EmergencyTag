from os import write
from NfcConnecter import NfcConnecter
from UITest import UserInterface
import sys
from PyQt5.QtWidgets import QApplication

from NfcWriter import NfcWriter

def main():
    nfcConnecter = NfcConnecter()
    nfcConnecter.start()
    
    app = QApplication(sys.argv)
    window = UserInterface()
    window.show()

    nfcConnecter.observer.add_card_signal.connect(window.add_card_handler)
    nfcConnecter.observer.remove_card_signal.connect(window.remove_card_handler)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()