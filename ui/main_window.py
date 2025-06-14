from PyQt5.QtWidgets import (QMainWindow, QTableView, QVBoxLayout, QWidget,
                             QPushButton, QHBoxLayout, QLabel, QFrame,
                             QMessageBox, QHeaderView)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QAbstractTableModel
from ui.order_edit_dialog import OrderEditDialog
from ui.products_dialog import ProductsDialog


class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.model = RequestsTableModel()  # Инициализация модели сразу
        self.setup_ui()

    def setup_ui(self):
        # Основные настройки окна
        self.setWindowTitle("Управление заявками партнеров")
        try:
            self.setWindowIcon(QIcon("images/logo.ico"))
        except:
            print("Не удалось загрузить иконку приложения")

        self.setGeometry(100, 100, 1200, 800)

        # Шрифт
        font = QFont("Bahnschrift Light SemiCondensed", 10)
        self.setFont(font)

        # Главный виджет
        main_widget = QWidget()
        main_widget.setStyleSheet("background-color: #FFFFFF;")
        self.setCentralWidget(main_widget)

        # Логотип
        self.logo = QLabel()
        try:
            self.logo.setPixmap(QPixmap("images/logo.png").scaled(200, 60, Qt.KeepAspectRatio))
        except:
            print("Не удалось загрузить логотип")
            self.logo.setText("Логотип")
        self.logo.setAlignment(Qt.AlignCenter)

        # Карточка партнера
        self.partner_card = QFrame()
        self.partner_card.setStyleSheet("""
            QFrame {
                background-color: #BBDCFA;
                border-radius: 5px;
                padding: 15px;
            }
            QLabel {
                color: #0C4882;
                margin: 3px;
            }
        """)
        self.partner_card.setLayout(QVBoxLayout())  # Инициализация layout

        # Таблица заявок
        self.table = QTableView()
        self.table.setStyleSheet("""
            QTableView {
                background-color: white;
                gridline-color: #BBDCFA;
                alternate-background-color: #F5F9FF;
            }
            QHeaderView::section {
                background-color: #0C4882;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
        """)
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        # Кнопки управления
        btn_style = """
            QPushButton {
                background-color: #0C4882;
                color: white;
                border: none;
                padding: 8px 15px;
                min-width: 120px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0A3A6B;
            }
        """

        self.add_btn = QPushButton("Добавить заявку")
        self.edit_btn = QPushButton("Редактировать")
        self.delete_btn = QPushButton("Удалить")
        self.view_products_btn = QPushButton("Просмотр продукции")

        for btn in [self.add_btn, self.edit_btn, self.delete_btn, self.view_products_btn]:
            btn.setStyleSheet(btn_style)

        # Подключение сигналов
        self.add_btn.clicked.connect(self.add_request)
        self.edit_btn.clicked.connect(self.edit_selected_request)
        self.delete_btn.clicked.connect(self.delete_request)
        self.view_products_btn.clicked.connect(self.view_products)

        # Разметка
        layout = QVBoxLayout()
        layout.addWidget(self.logo)
        layout.addSpacing(20)

        # Панель кнопок
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.view_products_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)
        layout.addSpacing(15)
        layout.addWidget(self.partner_card)
        layout.addSpacing(10)
        layout.addWidget(self.table)

        main_widget.setLayout(layout)

        # Загрузка данных
        self.load_requests()

        # Подключение сигнала после загрузки данных
        if self.table.selectionModel():
            self.table.selectionModel().currentChanged.connect(self.update_partner_card)
        else:
            print("Не удалось подключить сигнал currentChanged")

    def load_requests(self):
        try:
            requests = self.db.get_requests()
            if requests is None:
                requests = []
                print("Получен None вместо списка заявок")

            self.model.update_data(requests)

            if requests:
                self.table.selectRow(0)
                # Безопасное получение partner_id
                first_row_data = requests[0]
                partner_id = first_row_data.get('partner_id') or first_row_data.get('partner_pk') or None
                if partner_id:
                    self.show_partner_info(partner_id)
                else:
                    print("Не удалось получить partner_id из первой строки")
        except Exception as e:
            print(f"Ошибка при загрузке заявок: {str(e)}")
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить данные")

    def update_partner_card(self, current):
        try:
            if not current.isValid():
                return

            row = current.row()
            if 0 <= row < len(self.model.requests):
                request = self.model.requests[row]
                partner_id = request.get('partner_id')
                if partner_id:
                    self.show_partner_info(partner_id)
                else:
                    print("Не найден partner_id в выбранной строке")
        except Exception as e:
            print(f"Ошибка при обновлении карточки: {str(e)}")

    def show_partner_info(self, partner_id):
        try:
            # Очищаем карточку
            while self.partner_card.layout().count():
                item = self.partner_card.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            partner = self.db.get_partner_by_id(partner_id)
            if not partner:
                print(f"Партнер с ID {partner_id} не найден")
                return

            layout = self.partner_card.layout()

            # Тип и название
            title = QLabel(f"# {partner.get('type_name', 'Тип не указан')} | {partner.get('name', 'Без названия')}")
            title.setStyleSheet("font-size: 14pt; font-weight: bold;")

            # Контакты
            address = QLabel(partner.get('address', 'Адрес не указан'))
            phone = QLabel(f"Телефон: {partner.get('phone', 'не указан')}")
            email = QLabel(f"Email: {partner.get('email', 'не указан')}")
            rating = QLabel(f"Рейтинг: {partner.get('rating', 'не указан')}")

            # Стоимость
            cost_label = QLabel("## Стоимость заявок")
            cost_label.setStyleSheet("font-size: 12pt; margin-top: 10px;")

            layout.addWidget(title)
            layout.addWidget(address)
            layout.addWidget(phone)
            layout.addWidget(email)
            layout.addWidget(rating)
            layout.addWidget(cost_label)
            layout.addStretch()

        except Exception as e:
            print(f"Ошибка при отображении информации о партнере: {str(e)}")
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные партнера")

    # Остальные методы остаются без изменений
    def add_request(self):
        dialog = OrderEditDialog(self.db)
        if dialog.exec_():
            self.load_requests()

    def edit_selected_request(self):
        index = self.table.currentIndex()
        if index.isValid():
            self.edit_request(index)

    def edit_request(self, index):
        request_id = self.model.data(index, Qt.UserRole)
        dialog = OrderEditDialog(self.db, request_id)
        if dialog.exec_():
            self.load_requests()

    def delete_request(self):
        index = self.table.currentIndex()
        if index.isValid():
            request_id = self.model.data(index, Qt.UserRole)
            reply = QMessageBox.question(
                self, 'Подтверждение',
                'Вы уверены, что хотите удалить эту заявку?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                if self.db.delete_request(request_id):
                    self.load_requests()
                else:
                    QMessageBox.critical(self, 'Ошибка', 'Не удалось удалить заявку')

    def view_products(self):
        index = self.table.currentIndex()
        if index.isValid():
            request_id = self.model.data(index, Qt.UserRole)
            dialog = ProductsDialog(self.db, request_id)
            dialog.exec_()


class RequestsTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.requests = []
        self.headers = ["ID", "Партнер", "Продукт", "Кол-во", "Цена", "Сумма"]

    def update_data(self, requests):
        self.beginResetModel()
        self.requests = requests if requests else []
        self.endResetModel()

    def rowCount(self, parent=None):
        return len(self.requests)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.requests)):
            return None

        request = self.requests[index.row()]

        if role == Qt.DisplayRole:
            quantity = request.get('product_quantity', 0)
            price = request.get('min_cost_for_partner', 0)
            total = quantity * price

            return [
                str(request.get('partner_products_request_id', '')),
                request.get('partner_name', ''),
                request.get('product_name', ''),
                str(quantity),
                f"{price:.2f} руб.",
                f"{total:.2f} руб."
            ][index.column()]

        if role == Qt.UserRole:
            return request.get('partner_products_request_id')

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None