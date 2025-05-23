from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)

# Load your HTML form from file
with open("url.html", "r") as file:
    html_form = file.read()

@app.route('/')
def home():
    return render_template_string(html_form)


@app.route('/submit-url', methods=['POST'])
def submit_url():
    product_url = request.form.get('product_url')
    from amazon_scraper import fetch_price, write_to_db

    product = fetch_price(product_url)
    if product:
        write_to_db(product)
        return f"<h3>Tracked: {product['name']} at ₹{product['price']}</h3><br><a href='/'>Go back</a>"
    else:
        return "<h3>Failed to track the product. Please check the URL.</h3><br><a href='/'>Go back</a>"

@app.route('/api/price-history', methods=['GET'])
def price_history():
    try:
        # Optional: Accept product title as query parameter to filter
        product_title = request.args.get('title')

        conn = sqlite3.connect("price_data.db")
        cursor = conn.cursor()

        if product_title:
            cursor.execute("SELECT price, timestamp FROM prices WHERE product_title = ? ORDER BY timestamp ASC", (product_title,))
        else:
            cursor.execute("SELECT product_title, price, timestamp FROM prices ORDER BY timestamp ASC")

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return jsonify({'message': 'No data found'}), 404

        if product_title:
            data = [{'price': row[0], 'timestamp': row[1]} for row in rows]
        else:
            data = [{'product_title': row[0], 'price': row[1], 'timestamp': row[2]} for row in rows]

        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
