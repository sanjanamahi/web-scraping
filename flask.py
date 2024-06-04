from flask import Flask, render_template, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run-script')
def run_script():
    result = subprocess.run(['python', 'script_name.py'], capture_output=True, text=True)
    return jsonify(result=result.stdout)

@app.route('/get-latest-trends')
def get_latest_trends():
    latest_trend = collection.find().sort([('_id', -1)]).limit(1)
    return jsonify(latest_trend)

if __name__ == '__main__':
    app.run(debug=True)
