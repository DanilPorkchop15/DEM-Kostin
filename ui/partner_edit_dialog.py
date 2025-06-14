from PyQt5.QtWidgets import (QDialog, QFormLayout, QComboBox, QSpinBox, QLineEdit,
                             QDialogButtonBox, QMessageBox, QVBoxLayout)
from PyQt5.QtCore import Qt
import traceback


class PartnerEditDialog(QDialog):
    def __init__(self, db, partner_id=None):
        super().__init__()
        self.db = db
        self.partner_id = partner_id
        self.setWindowTitle("Редактирование партнера" if partner_id else "Новый партнер")
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Поля формы
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

        # Разметка
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
        """Загрузить данные партнера для редактирования"""
        if self.partner_id:
            partner = self.db.get_partner_by_id(self.partner_id)
            if partner:
                # Устанавливаем значения в поля формы
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
        """Валидация данных и сохранение"""
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

            # Валидация обязательных полей
            if not all([partner_type_id, name, director_name, address, phone, email, inn]):
                QMessageBox.warning(self, "Ошибка", "Все поля обязательны для заполнения")
                return

            # Валидация email
            if '@' not in email:
                QMessageBox.warning(self, "Ошибка", "Введите корректный email")
                return

            # Валидация ИНН (примерная проверка)
            if not (len(inn) in [10, 12] and inn.isdigit()):
                QMessageBox.warning(self, "Ошибка", "ИНН должен содержать 10 или 12 цифр")
                return

            # Сохраняем данные
            if self.partner_id:
                # Редактирование существующего партнера
                if not self.db.update_partner(self.partner_id, partner_type_id, name,
                                              director_name, address, rating, phone, email, inn):
                    raise Exception("Не удалось обновить данные партнера")
            else:
                # Добавление нового партнера
                partner_id = self.db.add_partner(partner_type_id, name, director_name,
                                                 address, rating, phone, email, inn)
                if not partner_id:
                    raise Exception("Не удалось добавить партнера")
                self.partner_id = partner_id

            super().accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")
            print(traceback.format_exc())