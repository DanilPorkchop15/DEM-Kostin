import traceback
from PyQt5.QtWidgets import (QDialog, QFormLayout, QComboBox, QSpinBox, QLineEdit,
                             QDialogButtonBox, QMessageBox, QHBoxLayout, QPushButton)
from PyQt5.QtCore import Qt


class PartnerEditDialog(QDialog):
    def __init__(self, db, partner_id=None):
        super().__init__()
        self.db = db
        self.partner_id = partner_id
        self.setWindowTitle("Редактирование партнера" if partner_id else "Новый партнер")
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Создаем поля формы
        self.partner_type_combo = QComboBox()
        self.name_edit = QLineEdit()
        self.director_edit = QLineEdit()
        self.address_edit = QLineEdit()
        self.rating_spin = QSpinBox()
        self.rating_spin.setMinimum(0)
        self.rating_spin.setMaximum(100)
        self.phone_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.inn_edit = QLineEdit()

        # Заполняем типы партнеров
        partner_types = self.db.get_partner_types()
        for pt in partner_types:
            self.partner_type_combo.addItem(pt['name'], pt['partner_type_id'])

        # Кнопки
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.validate_and_accept)
        self.buttons.rejected.connect(self.reject)

        # Разметка формы
        layout = QFormLayout()
        layout.addRow("Тип партнера:", self.partner_type_combo)
        layout.addRow("Наименование компании:", self.name_edit)
        layout.addRow("ФИО директора:", self.director_edit)
        layout.addRow("Адрес:", self.address_edit)
        layout.addRow("Рейтинг:", self.rating_spin)
        layout.addRow("Телефон:", self.phone_edit)
        layout.addRow("Email:", self.email_edit)
        layout.addRow("ИНН:", self.inn_edit)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def load_data(self):
        if self.partner_id:
            partner = self.db.get_partner_by_id(self.partner_id)
            if partner:
                index = self.partner_type_combo.findData(partner['partner_type_id'])
                if index >= 0:
                    self.partner_type_combo.setCurrentIndex(index)

                self.name_edit.setText(partner.get('name', ''))
                self.director_edit.setText(partner.get('director_name', ''))
                self.address_edit.setText(partner.get('address', ''))
                self.rating_spin.setValue(partner.get('rating', 0))
                self.phone_edit.setText(partner.get('phone', ''))
                self.email_edit.setText(partner.get('email', ''))
                self.inn_edit.setText(partner.get('inn', ''))

    def validate_and_accept(self):
        try:
            # Получаем данные из формы
            partner_type_id = self.partner_type_combo.currentData()
            name = self.name_edit.text().strip()
            director_name = self.director_edit.text().strip()
            address = self.address_edit.text().strip()
            rating = self.rating_spin.value()
            phone = self.phone_edit.text().strip()
            email = self.email_edit.text().strip()
            inn = self.inn_edit.text().strip()

            # Валидация данных
            if not all([partner_type_id, name, director_name, address, phone, email, inn]):
                QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения")
                return

            if '@' not in email:
                QMessageBox.warning(self, "Ошибка", "Введите корректный email")
                return

            if not (len(inn) in [10, 12] and inn.isdigit()):
                QMessageBox.warning(self, "Ошибка", "ИНН должен содержать 10 или 12 цифр")
                return

            # Сохраняем данные
            if self.partner_id:
                if not self.db.update_partner(self.partner_id, partner_type_id, name,
                                              director_name, address, rating, phone, email, inn):
                    raise Exception("Не удалось обновить данные партнера")
            else:
                partner_id = self.db.add_partner(partner_type_id, name, director_name,
                                                 address, rating, phone, email, inn)
                if not partner_id:
                    raise Exception("Не удалось добавить партнера")
                self.partner_id = partner_id

            super().accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")
            print(traceback.format_exc())


class OrderEditDialog(QDialog):
    def __init__(self, db, request_id=None):
        super().__init__()
        self.db = db
        self.request_id = request_id
        self.setWindowTitle("Редактирование заявки" if request_id else "Новая заявка")
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Виджеты для выбора партнера
        self.partner_combo = QComboBox()
        self.add_partner_btn = QPushButton("+")
        self.add_partner_btn.setFixedWidth(30)
        self.add_partner_btn.setToolTip("Добавить нового партнера")
        self.add_partner_btn.clicked.connect(self.add_new_partner)

        partner_layout = QHBoxLayout()
        partner_layout.addWidget(self.partner_combo)
        partner_layout.addWidget(self.add_partner_btn)

        # Виджеты для выбора продукта и количества
        self.product_combo = QComboBox()
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(999999)

        # Заполняем списки
        self.update_partners_combo()
        self.update_products_combo()

        # Кнопки
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.validate_and_accept)
        self.buttons.rejected.connect(self.reject)

        # Разметка формы
        layout = QFormLayout()
        layout.addRow("Партнер:", partner_layout)
        layout.addRow("Продукт:", self.product_combo)
        layout.addRow("Количество:", self.quantity_spin)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def update_partners_combo(self):
        """Обновить список партнеров в комбобоксе"""
        self.partner_combo.clear()
        partners = self.db.get_partners()
        for partner in partners:
            self.partner_combo.addItem(partner['name'], partner['partner_id'])

    def update_products_combo(self):
        """Обновить список продуктов в комбобоксе"""
        self.product_combo.clear()
        products = self.db.get_products()
        for product in products:
            self.product_combo.addItem(
                f"{product['name']} ({product['min_cost_for_partner']:.2f} руб.)",
                product['product_id'])

    def add_new_partner(self):
        """Открыть диалог добавления нового партнера"""
        dialog = PartnerEditDialog(self.db)
        if dialog.exec_():
            # Обновляем список партнеров и выбираем нового
            self.update_partners_combo()
            new_partner_id = dialog.partner_id
            index = self.partner_combo.findData(new_partner_id)
            if index >= 0:
                self.partner_combo.setCurrentIndex(index)

    def load_data(self):
        """Загрузить данные заявки для редактирования"""
        if self.request_id:
            request = self.db.get_request(self.request_id)
            if request:
                # Устанавливаем значения в поля формы
                partner_index = self.partner_combo.findData(request['partner_id'])
                if partner_index >= 0:
                    self.partner_combo.setCurrentIndex(partner_index)

                product_index = self.product_combo.findData(request['product_id'])
                if product_index >= 0:
                    self.product_combo.setCurrentIndex(product_index)

                self.quantity_spin.setValue(request['product_quantity'])

    def validate_and_accept(self):
        """Валидация и сохранение данных"""
        try:
            partner_id = self.partner_combo.currentData()
            product_id = self.product_combo.currentData()
            quantity = self.quantity_spin.value()

            if not all([partner_id, product_id, quantity > 0]):
                QMessageBox.warning(self, "Ошибка", "Проверьте правильность введенных данных")
                return

            if self.request_id:
                if not self.db.update_request(self.request_id, product_id, quantity):
                    raise Exception("Не удалось обновить заявку")
            else:
                if not self.db.add_request(partner_id, product_id, quantity):
                    raise Exception("Не удалось добавить заявку")

            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")
            print(traceback.format_exc())