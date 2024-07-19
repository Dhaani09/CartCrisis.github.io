from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    items = [
        {'id': 1, 'name': 'T-Shirt', 'price': 10.0},
        {'id': 2, 'name': 'Jeans', 'price': 20.0}
    ]
    return render_template('index.html', items=items)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = request.form.get('item_id')
    item_name = request.form.get('item_name')
    item_price = request.form.get('item_price')

    new_item = Item(name=item_name, price=item_price)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    items = Item.query.all()
    return render_template('cart.html', items=items)

@app.route('/remove_from_cart/<int:id>')
def remove_from_cart(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('cart'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
