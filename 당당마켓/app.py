import os # 경로 표현 패키지
from flask import Flask, request, render_template, redirect
from flask.json import jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/local"
mongo = PyMongo(app)

@app.route('/detail')
def detail():
    product_db = mongo.db.product
    product = product_db.find_one({"title": request.args.get('title')}) # 제목 기준 데이터 찾기(query string 이용)

    return jsonify({ # API 생성
        'title': product.get('title'),
        'content': product.get('content')
    })

@app.route('/writepage')
def writepage():
    return render_template('write.html')

@app.route('/write', methods=['POST'])
def write():

    fileinfo = request.files['image']
    filepath = os.path.dirname(os.path.abspath(__file__)) # 해당 파일이 속해있는 파일의 폴더 경로
    filepath = os.path.join(filepath, 'static') # 앞에서 찾은 경로에다 static 폴더 추가
    fileinfo.save(os.path.join(filepath, fileinfo.filename)) # 주어진 경로에다 파일이름 정보로 저장

    product_db = mongo.db.product

    product_db.insert_one({
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'price': request.form.get('price'),
        'location': request.form.get('location'),
        'image': fileinfo.filename
    })

    return redirect('/')

@app.route('/')
def main():
    product_db = mongo.db.product
    products = product_db.find()
    return render_template('list.html', products=products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')