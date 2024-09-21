import sys
from PyQt5.QtWidgets import QMessageBox, QApplication, QLineEdit, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget
from PyQt5.QtCore import Qt
from EmInfoLength import EmInfoLength
import NfcReader
import NfcConnecter
import NfcWriter
import cryptography
import dotenv

class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize a desktop window
        self.setWindowTitle("EM TAG")
        self.setGeometry(800, 800, 1600, 800)

        # Create a stacked widget to hold different pages
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
    
    def draw_entry_page(self):
        self.entry_page = QWidget()
        layout = QHBoxLayout()
        message = QLabel("No NFC card detected. Please connect to a card.")
        layout.addWidget(message, alignment=Qt.AlignCenter)
        self.entry_page.setLayout(layout)
        self.stacked_widget.addWidget(self.entry_page) # Add page to the stacked widget

    def draw_access_page(self):
        self.access_page = QWidget()
        layout = QHBoxLayout()
        center_button = QPushButton("Access")
        layout.addWidget(center_button, alignment=Qt.AlignCenter)
        self.access_page.setLayout(layout)
        self.stacked_widget.addWidget(self.access_page) # Add page to the stacked widget
        center_button.clicked.connect(self.go_to_info_page) # connect to the info page
    
    def draw_info_page(self):
        self.info_page = QWidget()
        layout = QVBoxLayout() 

        em_dict = EmInfoLength().info_page_dict 
        reader = NfcReader()
        connection = NfcConnecter()

        for key in em_dict:
            info = reader.read_category(connection, key)
            category_label = QLabel(f"{key}:")
            text_label = QLabel(info)
            layout.addWidget(category_label)
            layout.addWidget(text_label)
        
        layout.addStretch()

        exit_button = QPushButton("Back")
        edit_button = QPushButton("Edit")
        layout.addWidget(exit_button)
        layout.addWidget(edit_button)

        edit_button.clicked.connect(self.go_to_edit_page()) #connect to the edit page
        exit_button.clicked.connect(self.go_to_access_page()) #connect to the access page

        self.info_page.setLayout(layout)
        self.stacked_widget.addWidget(self.info_page) # Add page to the stacked widget
    
    def draw_edit_page(self):
        self.edit_page = QWidget()
        layout = QVBoxLayout()

        self.edit_fields = {}
        for key, value in self.info_dict.items():
            layout.addWidget(QLabel(f"Edit {key}:"))
            line_edit = QLineEdit(value)  # Pre-fill with current info
            layout.addWidget(line_edit)
            self.edit_fields[key] = line_edit  # Store references to line edits

        layout.addStretch()

        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.confirm_changes)  # Connect confirm button
        layout.addWidget(confirm_button)

        self.edit_page.setLayout(layout)
        self.stacked_widget.addWidget(self.edit_page)  # Add to stacked widget

    def confirm_changes(self):
        # Here, write the updated information back to the NFC card
        writer = NfcWriter()
        connection = NfcConnecter()

        for key, line_edit in self.edit_fields.items():
            new_value = line_edit.text()
            # Write the new value to the NFC card
            writer.write_category(connection, key, new_value)

        QMessageBox.information(self, "Success", "Information updated successfully!")
        self.stacked_widget.setCurrentWidget(self.info_page)  
    
    def go_to_access_page(self, connector):
        self.draw_access_page()
        self.stacked_widget.setCurrentWidget(self.access_page)
    
    def go_to_info_page(self):
        self.draw_info_page()
        self.stacked_widget.setCurrentWidget(self.info_page)
    
    def go_to_edit_page(self):
        self.draw_edit_page()
        self.stacked_widget.setCurrentWidget(self.edit_page)
