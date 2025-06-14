def calculate_material(db, product_id, material_id, required_quantity, in_stock):
    try:
        with db.connection.cursor() as cursor:
            cursor.execute("""
                           SELECT pt.coef, pm.param1, pm.param2, mt.defect_percentage
                           FROM product_materials pm
                                    JOIN products p ON pm.product_id = p.product_id
                                    JOIN product_types pt ON p.product_type_id = pt.product_type_id
                                    JOIN materials m ON pm.material_id = m.material_id
                                    JOIN material_types mt ON m.material_type_id = mt.material_type_id
                           WHERE pm.product_id = %s
                             AND pm.material_id = %s""",
                           (product_id, material_id))
            data = cursor.fetchone()
            if not data: return -1

            production_quantity = max(0, required_quantity - in_stock)
            if production_quantity == 0: return 0

            material_needed = (data['param1'] * data['param2'] * data['coef'] *
                               production_quantity * (1 + data['defect_percentage'] / 100))
            return int(material_needed) + (1 if material_needed % 1 > 0 else 0)
    except Exception as e:
        print(f"Calculation error: {e}")
        return -1