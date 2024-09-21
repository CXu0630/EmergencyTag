from NfcConnecter import NfcConnecter
from UITest import UserInterface
import sys
from PyQt5.QtWidgets import QApplication

def main():
    nfcConnecter = NfcConnecter()
    nfcConnecter.start()
    
    app = QApplication(sys.argv)
    window = UserInterface()
    window.show()
    nfcConnecter.observer.add_card_signal.connect(window.go_to_access_page)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()