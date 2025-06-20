
# Проект: Система управления заявками партнеров

Проект представляет собой систему для управления заявками партнеров производственной компании.

github: https://github.com/DanilPorkchop15/DEM-Kostin

## Структура проекта

```
PythonProject/
├── .venv/                     # Виртуальное окружение Python
├── database/                  # Файлы базы данных
├── create_db.sql              # SQL-скрипт для создания БД
├── Диаграмма связей.pdf       # Схема базы данных
├── images/                    # Изображения для интерфейса
│   ├── logo.ico               # Иконка приложения
│   └── logo.png               # Логотип приложения
├── modules/                   # Модули приложения
│   ├── database.py            # Работа с базой данных
│   └── material_calculator.py # Расчеты материалов
├── ui/                        # Пользовательский интерфейс
│   ├── main_window.py         # Главное окно
│   ├── order_edit_dialog.py   # Диалог редактирования заявок
│   ├── partner_edit_dialog.py # Диалог работы с партнерами
│   └── products_dialog.py     # Диалог работы с продукцией
├── main.py                    # Точка входа в приложение
├── README.md                  # Этот файл
└── requirements.txt           # Зависимости проекта
```

## Установка и запуск

1. **Предварительные требования**:
   - Python 3.8+
   - MySQL/MariaDB сервер

2. **Настройка базы данных**:
   ```bash
   mysql -u root -p < create_db.sql
   ```

3. **Установка зависимостей**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Запуск приложения**:
   ```bash
   python main.py
   ```

## Настройка базы данных

Перед запуском необходимо:
1. Создать базу данных, выполнив `create_db.sql`
2. Настроить подключение в `modules/database.py`:
   ```python
   self.connection = pymysql.connect(
       host='localhost',
       user='your_username',
       password='your_password',
       database='partners_production_company',
       charset='utf8mb4',
       cursorclass=pymysql.cursors.DictCursor
   )
   ```

## Функциональность

- Управление партнерами (добавление, редактирование)
- Создание и обработка заявок
- Просмотр продукции и расчет стоимости
- Учет материалов и расчеты

## Лицензия

Проект распространяется под лицензией MIT.

---

Для получения дополнительной информации обратитесь к документации в `Диаграмма связей.pdf`.
