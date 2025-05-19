import sys
import os
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QScrollArea, QFrame, QLabel, QDialog, QFormLayout, QLineEdit,
    QStackedWidget, QMessageBox, QSpacerItem, QSizePolicy, QDialogButtonBox,
    QGridLayout, QListWidget, QTextEdit
)
from PyQt6.QtCore import Qt
from datetime import datetime, timedelta

# Define global button style
BUTTON_STYLE = """
    QPushButton {
        background-color: #fbe9b2;
        color: #d32f26;
        font-family: 'Comic Sans MS';
        border-radius: 10px;
        padding: 4px 8px;
        font-size: 14px;
        font-weight: bold;
        margin: 5px;
    }
    QPushButton:hover {
        background-color: rgba(239, 203, 92, 0.9);
        border: 2px solid #D4A017;
    }
    QPushButton:pressed {
        background-color: rgba(200, 170, 76, 0.9);
    }
"""

class WelcomeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fridge Manager")
        self.setGeometry(200, 200, 1200, 675)

        self.setStyleSheet("""
            QDialog {
                background-image: url(assets/1.png);
                background-repeat: no-repeat;
                background-position: center;
            }
            QPushButton {
                background-color: #fbe9b2;
                color: #d32f26;
                font-family: 'Comic Sans MS';
                border-radius: 20px;
                padding: 8px 16px;
                font-size: 18px;
                font-weight: bold;
                width: 110px;
                height: 50px;
            }
            QPushButton:hover {
                background-color: rgba(239, 203, 92, 0.9);
                border: 2px solid #D4A017;
            }
            QPushButton:pressed {
                background-color: rgba(200, 170, 76, 0.9);
            }
            QLineEdit {
                font-family: 'Comic Sans MS';
                font-size: 14px;
                background-color: rgba(255, 255, 255, 0.95);
                border: 1px solid #D4A017;
                border-radius: 4px;
                padding: 4px;
            }
            QLabel {
                font-family: 'Comic Sans MS';
                font-size: 24px;
                color: #efcb5c;
            }
        """)

        self.username = None
        self.stacked_widget = QStackedWidget()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stacked_widget)

        welcome_widget = QWidget()
        welcome_layout = QHBoxLayout()
        welcome_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        button_layout.setSpacing(10)

        signup_button = QPushButton("Sign Up")
        signup_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        button_layout.addWidget(signup_button)

        login_button = QPushButton("Log In")
        login_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        button_layout.addWidget(login_button)

        welcome_layout.addLayout(button_layout)
        welcome_layout.addSpacerItem(QSpacerItem(100, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        welcome_widget.setLayout(welcome_layout)
        self.stacked_widget.addWidget(welcome_widget)

        signup_widget = QWidget()
        signup_layout = QHBoxLayout()
        signup_layout.addSpacerItem(QSpacerItem(100, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        signup_form_container = QVBoxLayout()
        signup_form_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        signup_form = QFormLayout()
        signup_form.setObjectName("signupForm")
        signup_form.setFormAlignment(Qt.AlignmentFlag.AlignRight)
        self.signup_username = QLineEdit()
        self.signup_password = QLineEdit()
        self.signup_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.signup_confirm_password = QLineEdit()
        self.signup_confirm_password.setEchoMode(QLineEdit.EchoMode.Password)

        signup_form.addRow("Username:", self.signup_username)
        signup_form.addRow("Password:", self.signup_password)
        signup_form.addRow("Confirm Password:", self.signup_confirm_password)

        signup_buttons = QHBoxLayout()
        signup_buttons.setAlignment(Qt.AlignmentFlag.AlignRight)
        signup_submit = QPushButton("Submit")
        signup_submit.clicked.connect(self.validate_signup)
        signup_back = QPushButton("Back")
        signup_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        signup_buttons.addWidget(signup_submit)
        signup_buttons.addWidget(signup_back)

        signup_form_container.addLayout(signup_form)
        signup_form_container.addLayout(signup_buttons)
        signup_form_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        signup_layout.addLayout(signup_form_container)
        signup_layout.addSpacerItem(QSpacerItem(100, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))

        signup_widget.setLayout(signup_layout)
        self.stacked_widget.addWidget(signup_widget)

        login_widget = QWidget()
        login_layout = QHBoxLayout()
        login_layout.addSpacerItem(QSpacerItem(100, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        login_form_container = QVBoxLayout()
        login_form_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        login_form = QFormLayout()
        login_form.setObjectName("loginForm")
        login_form.setFormAlignment(Qt.AlignmentFlag.AlignRight)
        self.login_username = QLineEdit()
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)

        login_form.addRow("Username:", self.login_username)
        login_form.addRow("Password:", self.login_password)

        login_buttons = QHBoxLayout()
        login_buttons.setAlignment(Qt.AlignmentFlag.AlignRight)
        login_submit = QPushButton("Submit")
        login_submit.clicked.connect(self.validate_login)
        login_back = QPushButton("Back")
        login_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        login_buttons.addWidget(login_submit)
        login_buttons.addWidget(login_back)

        login_form_container.addLayout(login_form)
        login_form_container.addLayout(login_buttons)
        login_form_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        login_layout.addLayout(login_form_container)
        login_layout.addSpacerItem(QSpacerItem(100, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))

        login_widget.setLayout(login_layout)
        self.stacked_widget.addWidget(login_widget)

    def validate_signup(self):
        username = self.signup_username.text().strip()
        password = self.signup_password.text().strip()
        confirm_password = self.signup_confirm_password.text().strip()

        if not all([username, password, confirm_password]):
            QMessageBox.warning(self, "Input Error", "All fields must be filled.")
            return

        if ',' in username or ',' in password:
            QMessageBox.warning(self, "Input Error", "Username and password cannot contain commas.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Input Error", "Passwords do not match.")
            return

        try:
            os.makedirs('database/accounts', exist_ok=True)
            accounts_file = 'database/accounts/Accounts.txt'
            if os.path.exists(accounts_file):
                with open(accounts_file, 'r') as file:
                    for line in file:
                        stored_username, _ = [item.strip() for item in line.split(',')]
                        if username == stored_username:
                            QMessageBox.warning(self, "Input Error", "Username already exists.")
                            return

            with open(accounts_file, 'a') as file:
                file.write(f"{username},{password}\n")

            os.makedirs('database/fridges', exist_ok=True)
            user_data_file = f'database/fridges/{username}_Food_Data.txt'
            with open(user_data_file, 'a'):
                pass

            QMessageBox.information(self, "Success", "Account created successfully. Please log in.")
            self.signup_username.clear()
            self.signup_password.clear()
            self.signup_confirm_password.clear()
            self.stacked_widget.setCurrentIndex(0)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create account: {e}")

    def validate_login(self):
        username = self.login_username.text().strip()
        password = self.login_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and password must not be empty.")
            return

        try:
            with open('database/accounts/Accounts.txt', 'r') as file:
                for line in file:
                    stored_username, stored_password = [item.strip() for item in line.split(',')]
                    if username == stored_username and password == stored_password:
                        self.username = username
                        self.accept()
                        return
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Accounts file not found. Please create an account first.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error reading accounts: {e}")

    def get_username(self):
        return self.username

class ClickableFrame(QFrame):
    def __init__(self, record, app, parent=None):
        super().__init__(parent)
        self.record = record
        self.app = app
        self.setMouseTracking(True)
        self.selected = False

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.app.select_frame(self)

class GridLayoutApp(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.data_file = f'database/fridges/{username}_Food_Data.txt'
        self.setWindowTitle(f"Fridge Manager - {username}")
        self.setGeometry(200, 200, 1200, 675)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #fff6de;
            }
            QLabel {
                font-family: 'Comic Sans MS';
            }
        """)

        self.current_sort_key = 'expiry_day'
        self.selected_frame = None
        self.recipe_ingredients = []

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.main_widget = QWidget()
        main_layout = QHBoxLayout()
        self.main_widget.setLayout(main_layout)

        first_layout = QVBoxLayout()
        first_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        first_layout.setSpacing(5)

        first_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        self.add_button = QPushButton("Add")
        self.add_button.setStyleSheet(BUTTON_STYLE)
        self.add_button.clicked.connect(self.show_add_food)
        first_layout.addWidget(self.add_button)

        self.find_recipe_button = QPushButton("Find Recipe")
        self.find_recipe_button.setStyleSheet(BUTTON_STYLE)
        self.find_recipe_button.clicked.connect(self.show_find_recipe)
        first_layout.addWidget(self.find_recipe_button)

        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet(BUTTON_STYLE)
        self.back_button.clicked.connect(self.back_to_welcome)
        first_layout.addWidget(self.back_button)

        first_layout.addStretch()
        first_layout_widget = QWidget()
        first_layout_widget.setLayout(first_layout)
        main_layout.addWidget(first_layout_widget)

        second_layout = QVBoxLayout()
        second_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)

        self.owner_search_bar = QLineEdit()
        self.owner_search_bar.setPlaceholderText("Search owner...")
        self.owner_search_bar.setStyleSheet("""
            QLineEdit {
                font-family: 'Comic Sans MS';
                font-size: 14px;
                background-color: rgba(255, 255, 255, 0.95);
                border: 1px solid #D4A017;
                border-radius: 4px;
                padding: 4px;
                margin: 5px;
            }
        """)
        self.owner_search_bar.textChanged.connect(self.search_frames)
        search_layout.addWidget(self.owner_search_bar)

        self.food_search_bar = QLineEdit()
        self.food_search_bar.setPlaceholderText("Search food...")
        self.food_search_bar.setStyleSheet("""
            QLineEdit {
                font-family: 'Comic Sans MS';
                font-size: 14px;
                background-color: rgba(255, 255, 255, 0.95);
                border: 1px solid #D4A017;
                border-radius: 4px;
                padding: 4px;
                margin: 5px;
            }
        """)
        self.food_search_bar.textChanged.connect(self.search_frames)
        search_layout.addWidget(self.food_search_bar)

        second_layout.addLayout(search_layout)

        self.view_all_button = QPushButton("View All")
        self.view_all_button.setStyleSheet(BUTTON_STYLE)
        self.view_all_button.clicked.connect(self.show_gallery)
        second_layout.addWidget(self.view_all_button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.scroll_content)

        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: transparent;
                width: 10px;
                height: 10px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: rgba(211, 47, 38, 0.5);
                border-radius: 5px;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                background: none;
            }
        """)
        self.scroll_area.viewport().setStyleSheet("background-color: transparent;")

        second_layout.addWidget(self.scroll_area)
        second_layout_widget = QWidget()
        second_layout_widget.setLayout(second_layout)
        main_layout.addWidget(second_layout_widget)

        third_layout = QVBoxLayout()
        third_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        third_layout.setSpacing(5)

        sort_label = QLabel("Sort by:")
        sort_label.setStyleSheet("""
            QLabel {
                font-family: 'Comic Sans MS';
                font-size: 14px;
                color: #d32f26;
            }
        """)
        third_layout.addWidget(sort_label)

        self.sort_owner_button = QPushButton("Owner")
        self.sort_owner_button.setStyleSheet(BUTTON_STYLE)
        self.sort_owner_button.clicked.connect(lambda: self.sort_frames('owner_name'))
        third_layout.addWidget(self.sort_owner_button)

        self.sort_expiry_button = QPushButton("Expiry Day")
        self.sort_expiry_button.setStyleSheet(BUTTON_STYLE)
        self.sort_expiry_button.clicked.connect(lambda: self.sort_frames('expiry_day'))
        third_layout.addWidget(self.sort_expiry_button)

        third_layout.addStretch()
        third_layout_widget = QWidget()
        third_layout_widget.setLayout(third_layout)
        main_layout.addWidget(third_layout_widget)

        main_layout.setSpacing(10)

        self.gallery_widget = QWidget()
        gallery_layout = QVBoxLayout()
        self.gallery_widget.setLayout(gallery_layout)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        back_to_home_button = QPushButton("Back to Home")
        back_to_home_button.setStyleSheet(BUTTON_STYLE)
        back_to_home_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_widget))
        button_layout.addWidget(back_to_home_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.setStyleSheet(BUTTON_STYLE + """
            QPushButton:disabled {
                background-color: #d3d3d3;
                color: #666666;
            }
        """)
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_selected_frame)
        button_layout.addWidget(self.delete_button)

        gallery_layout.addLayout(button_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)

        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: transparent;
                width: 10px;
                height: 10px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: rgba(211, 47, 38, 0.5);
                border-radius: 5px;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                background: none;
            }
        """)
        scroll_area.viewport().setStyleSheet("background-color: transparent;")

        self.gallery_grid_layout = QGridLayout()
        self.gallery_grid_layout.setSpacing(10)

        scroll_layout.addLayout(self.gallery_grid_layout)
        scroll_layout.addStretch()
        gallery_layout.addWidget(scroll_area)

        self.add_food_widget = QWidget()
        self.add_food_widget.setStyleSheet("""
            QWidget {
                background-image: url(assets/2.jpg);
                background-repeat: no-repeat;
                background-position: center;
            }
        """)
        add_food_layout = QVBoxLayout()
        self.add_food_widget.setLayout(add_food_layout)

        back_to_home_button_add = QPushButton("Back to Home")
        back_to_home_button_add.setStyleSheet(BUTTON_STYLE)
        back_to_home_button_add.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_widget))
        add_food_layout.addWidget(back_to_home_button_add, alignment=Qt.AlignmentFlag.AlignLeft)

        add_food_layout.addStretch()

        form_widget = QWidget()
        form_layout = QFormLayout()
        form_widget.setStyleSheet("""
            QWidget {
                max-width: 300px;
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        self.owner_name_input = QLineEdit()
        self.food_input = QLineEdit()
        self.expiry_day_input = QLineEdit()
        self.expiry_day_input.setPlaceholderText("YYYY-MM-DD")
        self.unit_input = QLineEdit()

        self.owner_name_input.setStyleSheet("""
            QLineEdit {
                font-family: 'Comic Sans MS';
                font-size: 14px;
                background-color: rgba(255, 255, 255, 0.95);
                border: 1px solid #D4A017;
                border-radius: 4px;
                padding: 4px;
            }
        """)
        self.food_input.setStyleSheet("""
            QLineEdit {
                font-family: 'Comic Sans MS';
                font-size: 14px;
                background-color: rgba(255, 255, 255, 0.95);
                border: 1px solid #D4A017;
                border-radius: 4px;
                padding: 4px;
            }
        """)
        self.expiry_day_input.setStyleSheet("""
            QLineEdit {
                font-family: 'Comic Sans MS';
                font-size: 14px;
                background-color: rgba(255, 255, 255, 0.95);
                border: 1px solid #D4A017;
                border-radius: 4px;
                padding: 4px;
            }
        """)
        self.unit_input.setStyleSheet("""
            QLineEdit {
                font-family: 'Comic Sans MS';
                font-size: 14px;
                background-color: rgba(255, 255, 255, 0.95);
                border: 1px solid #D4A017;
                border-radius: 4px;
                padding: 4px;
            }
        """)

        form_layout.addRow("Owner Name:", self.owner_name_input)
        form_layout.addRow("Food:", self.food_input)
        form_layout.addRow("Expiry Day:", self.expiry_day_input)
        form_layout.addRow("Unit:", self.unit_input)

        button_box = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.setStyleSheet(BUTTON_STYLE)
        ok_button.clicked.connect(self.validate_and_add)
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet(BUTTON_STYLE)
        cancel_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_widget))
        button_box.addWidget(ok_button)
        button_box.addWidget(cancel_button)

        form_layout.addRow(button_box)
        form_widget.setLayout(form_layout)
        add_food_layout.addWidget(form_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        add_food_layout.addStretch()

        self.find_recipe_widget = QWidget()
        self.find_recipe_widget.setStyleSheet("""
            QWidget {
                background-image: url(assets/3.jpg);
                background-repeat: no-repeat;
                background-position: center;
            }
        """)
        find_recipe_layout = QVBoxLayout()
        self.find_recipe_widget.setLayout(find_recipe_layout)

        back_to_home_button_recipe = QPushButton("Back to Home")
        back_to_home_button_recipe.setStyleSheet(BUTTON_STYLE)
        back_to_home_button_recipe.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_widget))
        find_recipe_layout.addWidget(back_to_home_button_recipe, alignment=Qt.AlignmentFlag.AlignLeft)

        recipe_form_widget = QWidget()
        recipe_form_widget.setStyleSheet("""
            QWidget {
                max-width: 500px;
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        recipe_form_layout = QVBoxLayout()

        self.recipe_food_input = QLineEdit()
        self.recipe_food_input.setPlaceholderText("Enter food item (e.g., chicken, rice)...")
        self.recipe_food_input.setStyleSheet("""
            QLineEdit {
                font-family: 'Comic Sans MS';
                font-size: 14px;
                background-color: rgba(255, 255, 255, 0.95);
                border: 1px solid #D4A017;
                border-radius: 4px;
                padding: 4px;
            }
        """)
        recipe_form_layout.addWidget(self.recipe_food_input)

        add_food_button = QPushButton("Add Food")
        add_food_button.setStyleSheet(BUTTON_STYLE)
        add_food_button.clicked.connect(self.add_recipe_food)
        recipe_form_layout.addWidget(add_food_button)

        self.ingredients_list = QListWidget()
        self.ingredients_list.setStyleSheet("""
            QListWidget {
                font-family: 'Comic Sans MS';
                font-size: 14px;
                background-color: rgba(255, 255, 255, 0.95);
                border: 1px solid #D4A017;
                border-radius: 4px;
                padding: 4px;
            }
        """)
        recipe_form_layout.addWidget(self.ingredients_list)

        generate_button = QPushButton("Generate")
        generate_button.setStyleSheet(BUTTON_STYLE)
        generate_button.clicked.connect(self.generate_recipes)
        recipe_form_layout.addWidget(generate_button)

        self.recipe_output = QTextEdit()
        self.recipe_output.setReadOnly(True)
        self.recipe_output.setStyleSheet("""
            QTextEdit {
                font-family: 'Comic Sans MS';
                font-size: 14px;
                background-color: rgba(255, 255, 255, 0.95);
                border: 1px solid #D4A017;
                border-radius: 4px;
                padding: 4px;
            }
        """)
        recipe_form_layout.addWidget(self.recipe_output)

        recipe_form_widget.setLayout(recipe_form_layout)
        find_recipe_layout.addWidget(recipe_form_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        find_recipe_layout.addStretch()

        self.stacked_widget.addWidget(self.main_widget)
        self.stacked_widget.addWidget(self.gallery_widget)
        self.stacked_widget.addWidget(self.add_food_widget)
        self.stacked_widget.addWidget(self.find_recipe_widget)

        data = self.load_data()
        self.load_frames(data, "", "")

    def load_data(self):
        if not os.path.exists(self.data_file):
            try:
                os.makedirs('database/fridges', exist_ok=True)
                with open(self.data_file, 'a'):
                    pass
            except Exception as e:
                print(f"Error creating {self.data_file}: {e}")
                return []

        try:
            with open(self.data_file, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"Error: {self.data_file} not found.")
            return []
        except Exception as e:
            print(f"Error reading {self.data_file}: {e}")
            return []

        valid_records = []
        for line in lines:
            data = [item.strip() for item in line.split(',')]
            if len(data) == 4:
                try:
                    expiry_date = datetime.strptime(data[2], '%Y-%m-%d')
                    valid_records.append((data[0], data[1], data[2], data[3], expiry_date))
                except ValueError:
                    continue
        return valid_records

    def load_frames(self, data, owner_search, food_search):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        owner_search = owner_search.lower()
        food_search = food_search.lower()
        filtered_records = [
            record for record in data
            if (not owner_search or owner_search in record[0].lower()) and
               (not food_search or food_search in record[1].lower())
        ]

        if self.current_sort_key == 'owner_name':
            sorted_records = sorted(filtered_records, key=lambda x: x[0])
        else:
            sorted_records = sorted(filtered_records, key=lambda x: x[4])

        for record in sorted_records:
            frame = QFrame()
            frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
            frame.setStyleSheet("""
                QFrame {
                    border: 1px solid gray;
                    padding: 5px;
                    margin: 5px;
                    background-color: #d32f26;
                    border-radius: 10px;
                }
                QLabel {
                    color: white;
                    font-family: 'Comic Sans MS';
                    font-size: 12px;
                }
            """)

            frame_layout = QVBoxLayout()
            frame_layout.addWidget(QLabel(f"Owner: {record[0]}"))
            frame_layout.addWidget(QLabel(f"Food: {record[1]}"))
            frame_layout.addWidget(QLabel(f"Unit: {record[3]}"))
            frame_layout.addWidget(QLabel(f"Expiry: {record[2]}"))
            frame.setLayout(frame_layout)

            self.scroll_layout.addWidget(frame)

    def load_gallery(self, data):
        for i in reversed(range(self.gallery_grid_layout.count())):
            layout_item = self.gallery_grid_layout.itemAt(i)
            if layout_item.widget():
                layout_item.widget().deleteLater()

        self.selected_frame = None
        self.delete_button.setEnabled(False)

        expired_label = QLabel("Expired")
        expired_label.setObjectName("header")
        expired_label.setStyleSheet("""
            QLabel.header {
                font-family: 'Comic Sans MS';
                font-size: 14px;
                color: #d32f26;
                font-weight: bold;
            }
        """)
        self.gallery_grid_layout.addWidget(expired_label, 0, 0, Qt.AlignmentFlag.AlignCenter)

        near_expired_label = QLabel("Near Expired")
        near_expired_label.setObjectName("header")
        near_expired_label.setStyleSheet("""
            QLabel.header {
                font-family: 'Comic Sans MS';
                font-size: 14px;
                color: #d32f26;
                font-weight: bold;
            }
        """)
        self.gallery_grid_layout.addWidget(near_expired_label, 0, 1, Qt.AlignmentFlag.AlignCenter)

        safe_label = QLabel("Safe to Use")
        safe_label.setObjectName("header")
        safe_label.setStyleSheet("""
            QLabel.header {
                font-family: 'Comic Sans MS';
                font-size: 14px;
                color: #d32f26;
                font-weight: bold;
            }
        """)
        self.gallery_grid_layout.addWidget(safe_label, 0, 2, Qt.AlignmentFlag.AlignCenter)

        today = datetime.now()  # Dynamically tracks the current date and time
        near_expiry_threshold = today + timedelta(days=5)  # 5 days from today

        expired = []
        near_expired = []
        safe = []

        for record in data:
            expiry_date = record[4]
            if expiry_date < today:
                expired.append(record)
            elif today <= expiry_date <= near_expiry_threshold:
                near_expired.append(record)
            else:
                safe.append(record)

        max_rows = max(len(expired), len(near_expired), len(safe))

        for row in range(max_rows):
            if row < len(expired):
                frame = self.create_frame(expired[row], "expired")
                self.gallery_grid_layout.addWidget(frame, row + 1, 0)

            if row < len(near_expired):
                frame = self.create_frame(near_expired[row], "near_expired")
                self.gallery_grid_layout.addWidget(frame, row + 1, 1)

            if row < len(safe):
                frame = self.create_frame(safe[row], "safe")
                self.gallery_grid_layout.addWidget(frame, row + 1, 2)

    def create_frame(self, record, status="normal"):
        frame = ClickableFrame(record, self, parent=self.scroll_content)
        frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)

        if status == "expired":
            bg_color = "#d32f26"
        elif status == "near_expired":
            bg_color = "#efcb5c"
        elif status == "safe":
            bg_color = "#2f6d4d"
        else:
            bg_color = "#d32f26"

        base_style = f"""
            QFrame {{
                border: 1px solid gray;
                padding: 5px;
                margin: 5px;
                background-color: {bg_color};
                border-radius: 10px;
            }}
            QLabel {{
                color: white;
                font-family: 'Comic Sans MS';
                font-size: 12px;
            }}
        """
        frame.setStyleSheet(base_style)

        frame_layout = QVBoxLayout()
        frame_layout.addWidget(QLabel(f"Owner: {record[0]}"))
        frame_layout.addWidget(QLabel(f"Food: {record[1]}"))
        frame_layout.addWidget(QLabel(f"Unit: {record[3]}"))
        frame_layout.addWidget(QLabel(f"Expiry: {record[2]}"))
        frame.setLayout(frame_layout)

        return frame

    def select_frame(self, frame):
        if self.selected_frame and self.selected_frame != frame:
            self.selected_frame.selected = False
            status = self.get_frame_status(self.selected_frame)
            bg_color = {"expired": "#d32f26", "near_expired": "#efcb5c", "safe": "#2f6d4d"}.get(status, "#d32f26")
            self.selected_frame.setStyleSheet(f"""
                QFrame {{
                    border: 1px solid gray;
                    padding: 5px;
                    margin: 5px;
                    background-color: {bg_color};
                    border-radius: 10px;
                }}
                QLabel {{
                    color: white;
                    font-family: 'Comic Sans MS';
                    font-size: 12px;
                }}
            """)

        self.selected_frame = frame
        frame.selected = True
        status = self.get_frame_status(frame)
        bg_color = {"expired": "#d32f26", "near_expired": "#efcb5c", "safe": "#2f6d4d"}.get(status, "#d32f26")
        frame.setStyleSheet(f"""
            QFrame {{
                border: 3px solid #D4A017;
                padding: 5px;
                margin: 5px;
                background-color: {bg_color};
                border-radius: 10px;
            }}
            QLabel {{
                color: white;
                font-family: 'Comic Sans MS';
                font-size: 12px;
            }}
        """)
        self.delete_button.setEnabled(True)

    def get_frame_status(self, frame):
        for row in range(1, self.gallery_grid_layout.rowCount()):
            for col in range(self.gallery_grid_layout.columnCount()):
                item = self.gallery_grid_layout.itemAtPosition(row, col)
                if item and item.widget() == frame:
                    return {0: "expired", 1: "near_expired", 2: "safe"}[col]
        return "normal"

    def delete_selected_frame(self):
        if not self.selected_frame:
            return

        record = self.selected_frame.record
        record_str = f"{record[0]},{record[1]},{record[2]},{record[3]}"

        try:
            with open(self.data_file, 'r') as file:
                lines = file.readlines()

            with open(self.data_file, 'w') as file:
                for line in lines:
                    if line.strip() != record_str:
                        file.write(line)

            data = self.load_data()
            self.load_gallery(data)
            self.selected_frame = None
            self.delete_button.setEnabled(False)
            QMessageBox.information(self, "Success", "Item deleted successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete item: {e}")

    def sort_frames(self, sort_key):
        self.current_sort_key = sort_key
        data = self.load_data()
        self.load_frames(data, self.owner_search_bar.text(), self.food_search_bar.text())

    def search_frames(self):
        data = self.load_data()
        self.load_frames(data, self.owner_search_bar.text(), self.food_search_bar.text())

    def show_gallery(self):
        data = self.load_data()
        if not data:
            QMessageBox.information(self, "No Data", "No food items in the fridge.")
            return
        self.load_gallery(data)
        self.stacked_widget.setCurrentWidget(self.gallery_widget)

    def show_add_food(self):
        self.owner_name_input.clear()
        self.food_input.clear()
        self.expiry_day_input.clear()
        self.unit_input.clear()
        self.stacked_widget.setCurrentWidget(self.add_food_widget)

    def show_find_recipe(self):
        self.recipe_food_input.clear()
        self.ingredients_list.clear()
        self.recipe_output.clear()
        self.recipe_ingredients = []
        self.stacked_widget.setCurrentWidget(self.find_recipe_widget)

    def add_recipe_food(self):
        food = self.recipe_food_input.text().strip()
        if not food:
            QMessageBox.warning(self, "Input Error", "Please enter a food item.")
            return
        if food not in self.recipe_ingredients:
            self.recipe_ingredients.append(food)
            self.ingredients_list.addItem(food)
            self.recipe_food_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Food item already added.")

    def generate_recipes(self):
        if not self.recipe_ingredients:
            QMessageBox.warning(self, "Input Error", "Please add at least one food item.")
            return

        app_id = "856618a1"
        app_key = "edcbe20b5566ae77b870b13bfd923e2a"
        query = ",".join(self.recipe_ingredients)

        try:
            url = f"https://api.edamam.com/api/recipes/v2?type=public&q={query}&app_id={app_id}&app_key={app_key}&from=0&to=5"
            print(f"Requesting URL: {url}")
            response = requests.get(url)
            print(f"Status Code: {response.status_code}")
            response.raise_for_status()  # Raises exception for 4xx/5xx errors
            data = response.json()
            print(f"Response Data: {data}")

            recipes = data.get("hits", [])
            if not recipes:
                self.recipe_output.setText("No recipes found for the given ingredients.")
                return

            output = "Suggested Recipes (Powered by Edamam):\n\n"
            for recipe in recipes:
                recipe_data = recipe.get("recipe")
                title = recipe_data.get("label", "Unknown")
                url = recipe_data.get("url", "#")
                output += f"- {title}\n  Link: {url}\n\n"

            self.recipe_output.setText(output)

        except requests.exceptions.HTTPError as e:
            error_msg = f"Failed to fetch recipes: {e}"
            print(f"Request Error: {e}")
            if response.status_code == 404:
                error_msg += "\nThe requested resource was not found. Please contact Edamam support at https://developer.edamam.com/."
            elif response.status_code == 401:
                error_msg += "\nInvalid API credentials. Please verify your app_id and app_key."
            elif response.status_code == 429:
                error_msg += "\nToo many requests. Please wait until UTC midnight (7:00 PM +07) or check your usage at https://developer.edamam.com/."
            QMessageBox.critical(self, "Error", error_msg)
            self.recipe_output.setText("Error fetching recipes. Please check your internet connection or API credentials.")
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            QMessageBox.critical(self, "Error", f"Failed to fetch recipes: {e}")
            self.recipe_output.setText("Error fetching recipes. Please check your internet connection or API credentials.")

    def validate_and_add(self):
        owner_name = self.owner_name_input.text().strip()
        food = self.food_input.text().strip()
        expiry_day = self.expiry_day_input.text().strip()
        unit = self.unit_input.text().strip()

        if not all([owner_name, food, expiry_day, unit]):
            QMessageBox.warning(self, "Input Error", "All fields must be filled.")
            return

        try:
            datetime.strptime(expiry_day, '%Y-%m-%d')
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Expiry Day must be in YYYY-MM-DD format.")
            return

        try:
            with open(self.data_file, 'a') as file:
                file.write(f"{owner_name},{food},{expiry_day},{unit}\n")
            data = self.load_data()
            self.load_frames(data, self.owner_search_bar.text(), self.food_search_bar.text())
            self.stacked_widget.setCurrentWidget(self.main_widget)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to write to file: {e}")

    def back_to_welcome(self):
        self.close()
        welcome_dialog = WelcomeDialog()
        if welcome_dialog.exec():
            username = welcome_dialog.get_username()
            if username:
                new_window = GridLayoutApp(username)
                new_window.show()
                new_window.app = app
        else:
            QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("QMessageBox { font-family: 'Comic Sans MS'; }")
    while True:
        welcome_dialog = WelcomeDialog()
        if welcome_dialog.exec():
            username = welcome_dialog.get_username()
            if username:
                window = GridLayoutApp(username)
                window.show()
                sys.exit(app.exec())
        else:
            sys.exit(0)