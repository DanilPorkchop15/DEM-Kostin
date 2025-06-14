from PyQt5.QtWidgets import (QDialog, QTableView, QVBoxLayout, QHBoxLayout,
                             QAbstractItemView, QPushButton, QLabel, QFrame, QHeaderView)
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QFont, QIcon


class ProductsDialog(QDialog):
    def __init__(self, db, request_id):
        super().__init__()
        self.db = db
        self.request_id = request_id
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        self.setWindowTitle("Продукция в заявке")
        self.setWindowIcon(QIcon("images/app_icon.ico"))
        self.setMinimumWidth(600)

        # Шрифт
        font = QFont("Bahnschrift Light SemiCondensed", 10)
        self.setFont(font)

        # Стили
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
            }
            QLabel {
                color: #0C4882;
            }
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

        # Заголовок
        self.title_label = QLabel("Просмотр продукции в заявке")
        self.title_label.setStyleSheet("font-size: 14pt; font-weight: bold;")

        # Таблица
        self.table = QTableView()
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.model = ProductsTableModel()
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Итоговая сумма
        self.total_frame = QFrame()
        self.total_frame.setStyleSheet("""
            QFrame {
                background-color: #BBDCFA;
                border-radius: 5px;
                padding: 10px;
            }
            QLabel {
                color: #0C4882;
                font-weight: bold;
            }
        """)

        self.total_label = QLabel("Итого: 0.00 руб.")
        self.total_label.setStyleSheet("font-size: 12pt;")

        total_layout = QHBoxLayout()
        total_layout.addWidget(QLabel("Общая сумма:"))
        total_layout.addStretch()
        total_layout.addWidget(self.total_label)
        self.total_frame.setLayout(total_layout)

        # Кнопки
        self.close_btn = QPushButton("Закрыть")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #0C4882;
                color: white;
                border: none;
                padding: 8px 15px;
                min-width: 100px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0A3A6B;
            }
        """)
        self.close_btn.clicked.connect(self.accept)

        # Разметка
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        layout.addWidget(self.title_label)
        layout.addWidget(self.table)
        layout.addWidget(self.total_frame)
        layout.addWidget(self.close_btn, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def load_data(self):
        try:
            products = self.db.get_request_products(self.request_id)
            if products is None:
                products = []
                print("Ошибка: получен None вместо списка продуктов")

            self.model.update_data(products)
            self.calculate_total(products)
        except Exception as e:
            print(f"Ошибка при загрузке продукции: {str(e)}")
            self.model.update_data([])

    def calculate_total(self, products):
        try:
            total = sum(p['product_quantity'] * p['min_cost_for_partner']
                        for p in products if 'product_quantity' in p and 'min_cost_for_partner' in p)
            self.total_label.setText(f"Итого: {total:.2f} руб.")
        except Exception as e:
            print(f"Ошибка расчета суммы: {str(e)}")
            self.total_label.setText("Итого: ошибка расчета")


class ProductsTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.products = []
        self.headers = ["Продукция", "Количество", "Цена за единицу", "Сумма"]

    def update_data(self, products):
        self.beginResetModel()
        self.products = products if products else []
        self.endResetModel()

    def rowCount(self, parent=None):
        return len(self.products)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.products)):
            return None

        product = self.products[index.row()]

        if role == Qt.DisplayRole:
            try:
                quantity = product.get('product_quantity', 0)
                price = product.get('min_cost_for_partner', 0)
                total = quantity * price

                return [
                    product.get('name', ''),
                    str(quantity),
                    f"{price:.2f} руб.",
                    f"{total:.2f} руб."
                ][index.column()]
            except Exception as e:
                print(f"Ошибка форматирования данных: {str(e)}")
                return "Ошибка"

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None