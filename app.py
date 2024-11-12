from flask import Flask, jsonify, request, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
import io
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fuel_prices.db'
db = SQLAlchemy(app)

class FuelPrice(db.Model):
    __tablename__ = 'fuel_price'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(2), nullable=False)
    fuel_type = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prices', methods=['GET'])
def get_prices():
    year = request.args.get('year')
    fuel_type = request.args.get('fuel_type')

    query = FuelPrice.query
    if year:
        query = query.filter(FuelPrice.year == int(year))
    if fuel_type:
        query = query.filter(FuelPrice.fuel_type == fuel_type)

    results = [{"year": p.year, "state": p.state, "fuel_type": p.fuel_type, "price": p.price} for p in query.all()]
    return jsonify(results)

@app.route('/price_variation', methods=['GET'])
def price_variation():
    state = request.args.get('state', 'GERAL')
    fuel_type = request.args.get('fuel_type', 'GERAL')

    plt.figure(figsize=(10, 5))

    if fuel_type == 'GERAL':
        fuel_types = db.session.query(FuelPrice.fuel_type).distinct().all()
        fuel_types = [f[0] for f in fuel_types]

        for f_type in fuel_types:
            query = FuelPrice.query
            if state != 'GERAL':
                query = query.filter(FuelPrice.state == state)
            
            query = query.filter(FuelPrice.fuel_type == f_type)
            data = query.order_by(FuelPrice.year).all()

            if data:
                years = [p.year for p in data]
                prices = [p.price for p in data]
                plt.plot(years, prices, 'o-', label=f_type)

    else:
        query = FuelPrice.query
        if state != 'GERAL':
            query = query.filter(FuelPrice.state == state)
        
        query = query.filter(FuelPrice.fuel_type == fuel_type)
        data = query.order_by(FuelPrice.year).all()

        if data:
            years = [p.year for p in data]
            prices = [p.price for p in data]
            plt.plot(years, prices, 'o-', label=fuel_type, color='blue')

    plt.title(f'Variação de Preço por Estado ({state})' if state != 'GERAL' else 'Variação de Preço por Estado (GERAL)')
    plt.xlabel('Ano')
    plt.ylabel('Preço')
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()  
    return send_file(img, mimetype='image/png')


@app.route('/average_price_per_year', methods=['GET'])
def average_price_per_year():
    fuel_type = request.args.get('fuel_type', 'GERAL')

    query = db.session.query(FuelPrice.year, db.func.avg(FuelPrice.price)).group_by(FuelPrice.year)
    if fuel_type != 'GERAL':
        query = query.filter(FuelPrice.fuel_type == fuel_type)

    data = query.all()
    years = [year for year, _ in data]
    avg_prices = [avg for _, avg in data]

    plt.figure(figsize=(10, 5))
    plt.plot(years, avg_prices, 'o-', color='green', label=fuel_type)
    plt.title('Média de Preços por Ano')
    plt.xlabel('Ano')
    plt.ylabel('Preço Médio')
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')

@app.route('/fuel_price_comparison', methods=['GET'])
def fuel_price_comparison():
    year = request.args.get('year', 'GERAL')

    query = db.session.query(FuelPrice.fuel_type, db.func.avg(FuelPrice.price)).group_by(FuelPrice.fuel_type)
    if year != 'GERAL':
        query = query.filter(FuelPrice.year == int(year))

    data = query.all()
    fuel_types = [fuel for fuel, _ in data]
    avg_prices = [avg for _, avg in data]

    plt.figure(figsize=(10, 5))
    plt.bar(fuel_types, avg_prices, color=['blue', 'green', 'red'])
    plt.title(f'Comparação de Preços por Tipo de Combustível para {year}')
    plt.xlabel('Tipo de Combustível')
    plt.ylabel('Preço Médio')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')

@app.route('/dashboard')
def dashboard():
    timestamp = datetime.now().timestamp()
    return render_template('dashboard.html', timestamp=timestamp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5001)

