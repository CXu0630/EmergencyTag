# UserInterface.py

from PyQt5.QtWidgets import (
    QApplication, QMessageBox, QLineEdit, QMainWindow, QLabel, QToolBar, QSizePolicy, QSpacerItem,
    QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget, QFormLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QFontDatabase, QFont
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
        self.setWindowTitle("emtag")
        self.setGeometry(800, 800, 700, 1000)
        # Set window icon (logo)
        self.setWindowIcon(QIcon("E:\EmergencyTag\logo ai-02.png"))

        # Add a tool bar at the top of the window
        self.toolbar = QToolBar()
        self.toolbar.setFixedHeight(250) # Set height of the top tool bar
        self.toolbar.setStyleSheet("QToolBar { border: none; }")
        self.addToolBar(self.toolbar)

        # Create spacer widgets
        spacer_left = QWidget()
        spacer_left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        spacer_right = QWidget()
        spacer_right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        

        # Load the logo image
        logo_pixmap = QPixmap("E:\EmergencyTag\logo ai-01.png")
        logo_label = QLabel()
        logo_label.setPixmap(logo_pixmap)

        # Add spacer widgets and the logo to the toolbar
        self.toolbar.addWidget(spacer_left)  # Left spacer
        self.toolbar.addWidget(logo_label)    # Logo
        self.toolbar.addWidget(spacer_right)  # Right spacer

        # Create a stacked widget to hold different pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize pages
        self.entry_page = self.create_entry_page()
        self.access_page = self.create_access_page()
        self.info_page = self.create_info_page()
        self.edit_page = self.create_edit_page()

        # Add all pages to the stacked widget
        self.stacked_widget.addWidget(self.entry_page)
        self.stacked_widget.addWidget(self.access_page)
        self.stacked_widget.addWidget(self.info_page)
        self.stacked_widget.addWidget(self.edit_page)

        # Show the entry page initially
        self.stacked_widget.setCurrentWidget(self.entry_page)

    def create_entry_page(self):
        entry_page = QWidget()
        layout = QHBoxLayout()
        message = QLabel("Please tap an EmTag NFC Tag to begin.")

        #set a font for prompt message
        # prompt_msg_font = QFont('Century Gothic', 10)
        # message.setFont(prompt_msg_font)
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
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 50, 50, 50)

        edit_layout = QFormLayout()  # Use QFormLayout for label-field alignment

        # self.edit_fields = {}

        try:
            for key in self.cat_strings:
                category_label = QLabel(f"{key}:")
                edit_info = QLabel("Replace with prefilled information from nfc")
                # edit_line = QLineEdit("replace with prefilled information from nfc")

                category_label.setFixedWidth(200)  # Adjust as needed

                edit_layout.addRow(category_label, edit_info)
                # self.edit_fields[key] = edit_line # Map the edited text to category

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create base template: {e}")
            return edit_page

        buttons_layout = QHBoxLayout() # Create a horizontal layout for buttons
        buttons_layout.addStretch()  # Push buttons to the right

        confirm_button = QPushButton("Confirm")
        buttons_layout.addWidget(confirm_button) # add confirm button to button layout

        # confirm_button.clicked.connect(self.confirm_changes)  # Connect confirm button

        main_layout.addLayout(edit_layout)
        main_layout.addStretch()
        main_layout.addLayout(buttons_layout)

        edit_page.setLayout(main_layout)
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

    #     try:
    #         for key, line_edit in self.edit_fields.items():
    #             new_value = line_edit.text()
    #             # Write the new value to the NFC card
    #             writer.write_category(connection, key, new_value)

    #         QMessageBox.information(self, "Success", "Information updated successfully!")
    #         self.stacked_widget.setCurrentWidget(self.info_page)
    #     except Exception as e:
    #         QMessageBox.critical(self, "Error", f"Failed to update NFC data: {e}")

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

# app = QApplication([])

# # Get available font families
# font_database = QFontDatabase()
# font_families = font_database.families()

# # Print the list of available fonts
# for font in font_families:
#     print(font)