# UserInterface.py

from PyQt5.QtWidgets import (
    QMessageBox, QLineEdit, QMainWindow, QLabel,
    QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget, QFormLayout
)
from PyQt5.QtCore import Qt
from EmInfoLength import EmInfoLength
from NfcReader import NfcReader
from NfcWriter import NfcWriter

class UserInterface(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.connection = None

        self.categories = ['name', 'blood_type', 'em_contact', 'birth_date', 'allergies', 
                  'med_history']
        self.cat_strings = ['Name', 'Blood Type', 'Emergency Contact', 'Birth Date',
                            'Allergies', 'Medical History']

        # Initialize the main window
        self.setWindowTitle("EM TAG")
        self.setGeometry(800, 800, 700, 1000)

        # Create a stacked widget to hold different pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize pages
        self.entry_page = self.create_entry_page()
        self.access_page = self.create_access_page()
        self.info_page = self.create_info_page()

        # Add all pages to the stacked widget
        self.stacked_widget.addWidget(self.entry_page)
        self.stacked_widget.addWidget(self.access_page)
        self.stacked_widget.addWidget(self.info_page)

        # Show the entry page initially
        self.stacked_widget.setCurrentWidget(self.entry_page)

    def create_entry_page(self):
        entry_page = QWidget()
        layout = QHBoxLayout()
        message = QLabel("Please tap an EmTag NFC Tag to begin.")
        layout.addWidget(message, alignment=Qt.AlignCenter)
        entry_page.setLayout(layout)
        return entry_page

    def create_access_page(self):
        access_page = QWidget()
        layout = QHBoxLayout()
        center_button = QPushButton("Access")
        layout.addWidget(center_button, alignment=Qt.AlignCenter)
        access_page.setLayout(layout)
        center_button.clicked.connect(self.go_to_info_page)
        return access_page

    def create_info_page(self):
        info_page = QWidget()
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 50, 50, 50)

        info_layout = QFormLayout()  # Use QFormLayout for label-field alignment

        try:
            for key in self.cat_strings:
                info = "None"  # Replace with actual data retrieval logic
                category_label = QLabel(f"{key}:")
                text_label = QLabel(info)
                text_label.setWordWrap(True)  # Enable word wrap for long text

                # Optionally set fixed widths for consistency
                category_label.setFixedWidth(200)  # Adjust as needed
                text_label.setFixedWidth(400)      # Adjust as needed

                # Add the label and text to the form layout
                info_layout.addRow(category_label, text_label)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create base template: {e}")

        # Create a horizontal layout for buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()  # Push buttons to the right

        exit_button = QPushButton("Back")
        edit_button = QPushButton("Edit")

        # Add buttons to the buttons_layout
        buttons_layout.addWidget(exit_button)
        buttons_layout.addWidget(edit_button)

        # Correct connections without calling the methods
        edit_button.clicked.connect(self.go_to_edit_page)
        exit_button.clicked.connect(self.go_to_access_page)

        main_layout.addLayout(info_layout)
        main_layout.addStretch()
        main_layout.addLayout(buttons_layout)

        info_page.setLayout(main_layout)

        return info_page

    def create_edit_page(self):
        edit_page = QWidget()
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

        edit_page.setLayout(layout)
        return edit_page

    def repopulate_info_page(self):
        info_page = QWidget()
        if self.connection == None:
            print('No connection, unable to repopulate info page.')
            return None
        
        reader = NfcReader(self.connection)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 50, 50, 50)

        info_layout = QFormLayout()  # Use QFormLayout for label-field alignment

        try:
            for i in range(len(self.cat_strings)):
                info = reader.read_category(self.categories[i])  # Replace with actual data retrieval logic
                category_label = QLabel(f"{self.cat_strings[i]}:")
                text_label = QLabel(info)
                text_label.setWordWrap(True)  # Enable word wrap for long text

                # Optionally set fixed widths for consistency
                category_label.setFixedWidth(200)  # Adjust as needed
                text_label.setFixedWidth(400)      # Adjust as needed

                # Add the label and text to the form layout
                info_layout.addRow(category_label, text_label)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create base template: {e}")

        # Create a horizontal layout for buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()  # Push buttons to the right

        exit_button = QPushButton("Back")
        edit_button = QPushButton("Edit")

        # Add buttons to the buttons_layout
        buttons_layout.addWidget(exit_button)
        buttons_layout.addWidget(edit_button)

        # Correct connections without calling the methods
        edit_button.clicked.connect(self.go_to_edit_page)
        exit_button.clicked.connect(self.go_to_access_page)

        main_layout.addLayout(info_layout)
        main_layout.addStretch()
        main_layout.addLayout(buttons_layout)

        info_page.setLayout(main_layout)
        
        self.stacked_widget.removeWidget(self.info_page)
        self.info_page = info_page
        self.stacked_widget.addWidget(self.info_page)

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
    
    def add_card_handler(self, connection):
        self.go_to_access_page()
        self.connection = connection
        self.repopulate_info_page()

    def remove_card_handler(self):
        self.go_to_entry_page()
        self.connection = None