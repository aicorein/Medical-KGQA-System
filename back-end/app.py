from flask import Flask, request, jsonify, make_response, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import Query


app = Flask(__name__, template_folder='templates', static_folder='./static', \
                static_url_path='/static')
limiter = Limiter(app, key_func=get_remote_address, default_limits=["1/second"])


@app.route('/')
@limiter.limit("3/second")
def index():
    return render_template('index.html')


@app.route('/query', methods=['POST'])
@limiter.limit("3/second")
def query():
    if request.form.get('query'):
        data = Query.query(request.form.get('query'))
        data['status'] = 200
        resp = make_response(jsonify(data))
    else:
        template = jsonify({"status": 400, "type": 'none', "content": {}})
        resp = make_response(template, 400)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    # 监听在所有 IP 地址上
    app.run(host='0.0.0.0', port=80, debug=True)
