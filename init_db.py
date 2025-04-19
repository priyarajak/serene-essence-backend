from db_config import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    price INT,
    image TEXT,
    description TEXT,
    rating FLOAT,
    deliveryDays INT,
    category VARCHAR(50)
)
""")

products = [
    ("Lavender Bliss", 250, "serene-essence/public/images/lavender.jpeg", "Relaxing lavender scent", 4.5, 3, "floral"),
    ("Vanilla Dreams", 200, "serene-essence/public/images/citrius.jpeg", "Cozy vanilla warmth", 4.7, 4, "sweet"),
    ("Citrus Sunset", 300, "https://images.unsplash.com/photo-1630326838381-87e62c6b4531", "Fresh citrus burst", 4.3, 2, "citrus")
]

cursor.executemany("""
INSERT INTO products (name, price, image, description, rating, deliveryDays, category)
VALUES (%s, %s, %s, %s, %s, %s, %s)
""", products)

conn.commit()
conn.close()
