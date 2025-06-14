import pymysql
from pymysql import Error


class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host='localhost',
                user='root',
                password='toor',
                database='partners_production_company',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)
            return True
        except Error as e:
            print(f"Database connection error: {e}")
            return False

    def delete_request(self, request_id):
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM partner_products_requests WHERE partner_products_request_id = %s"
                cursor.execute(sql, (request_id,))
                self.connection.commit()
                return cursor.rowcount > 0
        except Error as e:
            self.connection.rollback()
            print(f"Ошибка при удалении заявки: {e}")
            return False

    def get_partners(self):
        """Получить список всех партнеров"""
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT partner_id, name FROM partners ORDER BY name"
                cursor.execute(sql)
                return cursor.fetchall()
        except Error as e:
            print(f"Ошибка при получении списка партнеров: {e}")
            return []

    def get_products(self):
        """Получить список всей продукции"""
        try:
            with self.connection.cursor() as cursor:
                sql = """
                      SELECT p.product_id, p.name, p.min_cost_for_partner, pt.name as type_name
                      FROM products p
                               JOIN product_types pt ON p.product_type_id = pt.product_type_id
                      ORDER BY p.name \
                      """
                cursor.execute(sql)
                return cursor.fetchall()
        except Error as e:
            print(f"Ошибка при получении списка продукции: {e}")
            return []

    def get_request(self, request_id):
        """Получить данные конкретной заявки"""
        try:
            with self.connection.cursor() as cursor:
                sql = """
                      SELECT partner_id, product_id, product_quantity
                      FROM partner_products_requests
                      WHERE partner_products_request_id = %s \
                      """
                cursor.execute(sql, (request_id,))
                return cursor.fetchone()
        except Error as e:
            print(f"Ошибка при получении заявки: {e}")
            return None
    def get_request_products(self, request_id):
        """Получить список продукции в заявке"""
        try:
            with self.connection.cursor() as cursor:
                sql = """
                      SELECT p.name, ppr.product_quantity, p.min_cost_for_partner
                      FROM partner_products_requests ppr
                               JOIN products p ON ppr.product_id = p.product_id
                      WHERE ppr.partner_products_request_id = %s \
                      """
                cursor.execute(sql, (request_id,))
                return cursor.fetchall()
        except Error as e:
            print(f"Ошибка при получении продукции заявки: {e}")
            return []

    def get_requests(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                SELECT 
                    ppr.partner_products_request_id,
                    p.name as partner_name,
                    pr.name as product_name,
                    ppr.product_quantity,
                    pr.min_cost_for_partner
                FROM partner_products_requests ppr
                JOIN partners p ON ppr.partner_id = p.partner_id
                JOIN products pr ON ppr.product_id = pr.product_id
                ORDER BY ppr.partner_products_request_id;
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Error as e:
            print(f"Ошибка при получении заявок: {str(e)}")
            return []

    def add_request(self, partner_id, product_id, quantity):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                INSERT INTO partner_products_requests 
                (partner_id, product_id, product_quantity)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (partner_id, product_id, quantity))
                self.connection.commit()
                return cursor.lastrowid
        except Error as e:
            self.connection.rollback()
            print(f"Ошибка при добавлении заявки: {e}")
            return None

    def update_request(self, request_id, product_id, quantity):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                      UPDATE partner_products_requests
                      SET product_id       = %s, \
                          product_quantity = %s
                      WHERE partner_products_request_id = %s \
                      """
                params = (product_id, quantity, request_id)
                cursor.execute(sql, params)
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.connection.rollback()
            print(f"Ошибка при обновлении заявки: {str(e)}")
            return False

    def get_partner_by_id(self, partner_id):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                      SELECT p.*, pt.name as type_name
                      FROM partners p
                               JOIN partner_types pt ON p.partner_type_id = pt.partner_type_id
                      WHERE p.partner_id = %s \
                      """
                cursor.execute(sql, (partner_id,))
                return cursor.fetchone()
        except Error as e:
            print(f"Ошибка при получении партнера: {e}")
            return None

    def get_request_products_summary(self, partner_id):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                      SELECT SUM(ppr.product_quantity * pr.min_cost_for_partner) as total_sum, \
                             COUNT(*)                                            as request_count
                      FROM partner_products_requests ppr
                               JOIN products pr ON ppr.product_id = pr.product_id
                      WHERE ppr.partner_id = %s \
                      """
                cursor.execute(sql, (partner_id,))
                return cursor.fetchone()
        except Error as e:
            print(f"Ошибка при расчете стоимости: {e}")
            return None

    def get_partner_types(self):
        """Получить список типов партнеров"""
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT partner_type_id, name FROM partner_types ORDER BY name"
                cursor.execute(sql)
                return cursor.fetchall()
        except Error as e:
            print(f"Ошибка при получении типов партнеров: {e}")
            return []

    def add_partner(self, partner_type_id, name, director_name, address, rating, phone, email, inn):
        """Добавить нового партнера"""
        try:
            with self.connection.cursor() as cursor:
                sql = """
                      INSERT INTO partners
                      (partner_type_id, name, director_name, address, rating, phone, email, inn)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
                      """
                cursor.execute(sql, (partner_type_id, name, director_name, address,
                                     rating, phone, email, inn))
                self.connection.commit()
                return cursor.lastrowid
        except Error as e:
            self.connection.rollback()
            print(f"Ошибка при добавлении партнера: {e}")
            return None

    def update_partner(self, partner_id, partner_type_id, name, director_name, address, rating, phone, email, inn):
        """Обновить данные партнера"""
        try:
            with self.connection.cursor() as cursor:
                sql = """
                      UPDATE partners
                      SET partner_type_id = %s,
                          name            = %s,
                          director_name   = %s,
                          address         = %s,
                          rating          = %s,
                          phone           = %s,
                          email           = %s,
                          inn             = %s
                      WHERE partner_id = %s \
                      """
                cursor.execute(sql, (partner_type_id, name, director_name, address,
                                     rating, phone, email, inn, partner_id))
                self.connection.commit()
                return cursor.rowcount > 0
        except Error as e:
            self.connection.rollback()
            print(f"Ошибка при обновлении партнера: {e}")
            return False

    def close(self):
        if self.connection:
            self.connection.close()