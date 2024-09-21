from NfcConnecter import NfcConnecter
import UI
import sys
from PyQt5.QtWidgets import QApplication

def main():
    nfcConnecter = NfcConnecter()
    nfcConnecter.start()
    
    app = QApplication(sys.argv)
    window = UserInterface()
    window.draw_entry_page()
    window.show()
    # nfcConnecter.observer.subscribe("add_card", window.go_to_access_page)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()