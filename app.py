from flask import Flask, request, jsonify, Response
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    args = request.args
    a = args.get('a')
    b = args.get('b')
    op = args.get('op')
    time_now = datetime.now()
    success_code = Response(status=200, mimetype='application/json')
    bad_req_code = Response(status=400, mimetype='application/json')
    result = ""

    if not a or a == "":
        bad_req_code
        js_arr = jsonify({"status": "error", "reason": "a not found in query string"}), 400
        return js_arr
    elif not b or b == "":
        bad_req_code
        js_arr = jsonify({"status": "error", "reason": "b not found in query string"}), 400
        return js_arr
    elif not op or op == "":
        bad_req_code
        js_arr = jsonify({"status": "error", "reason": "op not found in query string"}), 400
        return js_arr

    if op == "*":
        success_code
        result = float(a) * float(b)
    elif op == "/":
        success_code
        result = float(a) / float(b)
    elif op == "-":
        success_code
        result = float(a) - float(b)
    elif op == "+":
        success_code
        result = float(a) + float(b)

    js_arr = {"status": "ok", "date": time_now.strftime('%Y-%m-%d %H:%M'), "result": result}
    message = jsonify(js_arr)
    return message


if __name__ == "__main__":
    app.run(threaded=True, port=8000)