from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)
with open("url.html", "r", encoding="utf-8") as file:
    html_form = file.read()

@app.route('/')
def home():
    return render_template_string(html_form)

@app.route('/api/price-history', methods=['GET'])
def price_history():
    try:
        product_url = request.args.get('url')
        if not product_url:
            return jsonify({'error': 'Missing URL'}), 400

        conn = sqlite3.connect("price_data.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT product_title, price, timestamp FROM prices
            WHERE url = ?
            ORDER BY timestamp ASC
        """, (product_url,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return jsonify({'message': 'No data found'}), 404

        data = [{'product_title': row[0], 'price': row[1], 'timestamp': row[2]} for row in rows]
        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
