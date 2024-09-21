from NfcConnecter import NfcConnecter
from UI import UserInterface
import sys
from PyQt5.QtWidgets import QApplication

def main():
    nfcConnecter = NfcConnecter()
    nfcConnecter.start()
    
    app = QApplication(sys.argv)
    window = UserInterface()
    window.draw_entry_page()
    window.show()
    sys.exit(app.exec_())
    
    nfcConnecter.observer.subscribe("add_card", window.go_to_access_page)

if __name__ == "__main__":
    main()