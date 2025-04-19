import csv
from db_config import get_db_connection

def import_products_from_csv(csv_file):
    conn = get_db_connection()
    cursor = conn.cursor()

    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print("Importing:", row)
            cursor.execute("""
                INSERT INTO products (name, price, image, description, rating, deliveryDays, category)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                row['name'],
                int(row['price']),
                row['image'],
                row['description'],
                float(row['rating']),
                int(row['deliveryDays']),
                row['category']
            ))

    conn.commit()
    conn.close()
    print("✅ Products imported successfully!")

if __name__ == "__main__":
    import_products_from_csv("Serene-essence-products.csv")
