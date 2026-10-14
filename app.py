from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicialización
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///almacen.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo Product
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)  # Valor por defecto 0

    def __repr__(self):
        return f"Producto('{self.name}', Bs. {self.price}, Stock: {self.stock})"

# 1. Crear tablas
def init_db():
    with app.app_context():
        db.create_all()
        print(" Tablas creadas exitosamente")

# 2. CREATE — Insertar productos
def create_products():
    with app.app_context():
        p1 = Product(name="Cuadernos", price=12.50, stock=50)
        p2 = Product(name="Lápices", price=1.80, stock=200)
        p3 = Product(name="Borradores", price=0.90)  # stock = 0 por defecto
        
        db.session.add_all([p1, p2, p3])
        db.session.commit()
        print(" Productos insertados")

# 3. READ — Consultas
def read_products():
    with app.app_context():
        todos = Product.query.all()
        print("\n Todos los productos:")
        for p in todos:
            print(p)

        # Por ID
        prod = Product.query.filter_by(id=2).first()
        if prod:
            print(f"\n Producto con ID=2: {prod}")

        # Con filtro personalizado
        bajo_stock = Product.query.filter(Product.stock < 100).all()
        print(f"\n Productos con stock menor a 100: {[p.name for p in bajo_stock]}")

# 4. UPDATE — Actualizar
def update_product(prod_id=1):
    with app.app_context():
        prod = Product.query.filter_by(id=prod_id).first()
        if prod:
            prod.price = 13.00
            prod.stock = 45
            db.session.commit()
            print(f" Producto actualizado: {prod}")
        else:
            print(" Producto no encontrado")

# 5. DELETE — Eliminar
def delete_product(prod_id=3):
    with app.app_context():
        prod = Product.query.filter_by(id=prod_id).first()
        if prod:
            db.session.delete(prod)
            db.session.commit()
            print(f" Producto eliminado: {prod.name}")
        else:
            print(" Producto no encontrado")

# Ejecución completa
if __name__ == "__main__":
    #init_db()
    create_products()
    read_products()
    update_product()
    read_products()
    delete_product()
    read_products()