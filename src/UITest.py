# UserInterface.py

from PyQt5.QtWidgets import (
    QMessageBox, QLineEdit, QMainWindow, QLabel,
    QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget
)
from PyQt5.QtCore import Qt
from EmInfoLength import EmInfoLength
import NfcReader
import NfcConnecter
import NfcWriter

class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the main window
        self.setWindowTitle("EM TAG")
        self.setGeometry(100, 100, 800, 600)  # Adjusted size for testing

        # Create a stacked widget to hold different pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize pages
        self.entry_page = self.create_entry_page()
        self.access_page = self.create_access_page()

        # Add all pages to the stacked widget
        self.stacked_widget.addWidget(self.entry_page)
        self.stacked_widget.addWidget(self.access_page)

        # Show the entry page initially
        self.stacked_widget.setCurrentWidget(self.entry_page)

    def create_entry_page(self):
        entry_page = QWidget()
        layout = QHBoxLayout()
        message = QLabel("No NFC card detected. Please connect to a card.")
        layout.addWidget(message, alignment=Qt.AlignCenter)
        entry_page.setLayout(layout)
        return entry_page

    def create_access_page(self):
        access_page = QWidget()
        layout = QHBoxLayout()
        center_button = QPushButton("Access")
        layout.addWidget(center_button, alignment=Qt.AlignCenter)
        access_page.setLayout(layout)
        #center_button.clicked.connect(self.go_to_info_page)
        return access_page

    def create_info_page(self):
        info_page = QWidget()
        layout = QVBoxLayout()

        em_dict = EmInfoLength().info_page_dict
        self.info_dict = {
            'name': 'Chloe X',
            'blood_type': 'O+',
            'em_contact': '123-456-7890',
            'birth_date': '1990-01-01',
            'allergies': 'None',
            'med_history': 'None'
        }

        try:
            for key in em_dict:
                info = self.info_dict[key]
                category_label = QLabel(f"{key}:")
                text_label = QLabel(info)
                layout.addWidget(category_label)
                layout.addWidget(text_label)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read NFC data: {e}")

        layout.addStretch()

        exit_button = QPushButton("Back")
        edit_button = QPushButton("Edit")
        layout.addWidget(exit_button)
        layout.addWidget(edit_button)

        # Correct connections without parentheses
        edit_button.clicked.connect(self.go_to_edit_page)
        exit_button.clicked.connect(self.go_to_access_page)

        info_page.setLayout(layout)
        return info_page

    def create_edit_page(self):
        edit_page = QWidget()
        layout = QVBoxLayout()

        # Example info_dict; replace with actual data as needed
        self.info_dict = {
            'name': 'Chloe X',
            'blood_type': 'O+',
            'em_contact': '123-456-7890',
            'birth_date': '1990-01-01',
            'allergies': 'None',
            'med_history': 'None'
        }

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

        edit_page.setLayout(layout)
        return edit_page

    def confirm_changes(self):
        # Here, write the updated information back to the NFC card
        writer = NfcWriter.NfcWriter()
        connection = None  # Replace with actual connection if needed

        try:
            for key, line_edit in self.edit_fields.items():
                new_value = line_edit.text()
                # Write the new value to the NFC card
                writer.write_category(connection, key, new_value)

            QMessageBox.information(self, "Success", "Information updated successfully!")
            self.stacked_widget.setCurrentWidget(self.info_page)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update NFC data: {e}")

    def go_to_access_page(self):
        self.stacked_widget.setCurrentWidget(self.access_page)

    def go_to_info_page(self):
        self.stacked_widget.setCurrentWidget(self.info_page)

    def go_to_edit_page(self):
        self.stacked_widget.setCurrentWidget(self.edit_page)

    def go_to_entry_page(self):
        self.stacked_widget.setCurrentWidget(self.entry_page)
