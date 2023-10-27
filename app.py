
from flask import *
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os, boto3, time

load_dotenv()

app=Flask(__name__)

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

import mysql.connector
from mysql.connector import pooling
config = {
    "host":os.getenv('HOST'),
    "user":os.getenv('USER'),
    "password":os.getenv('PASSWORD'),
    "database":os.getenv('DATABASE'),
    # "host":"db-stage3-week1.cxzjwrl3yccb.us-east-1.rds.amazonaws.com",
    # "port":3306,
    # "user":"root",
    # "password":"12345678",
    # "database":"Stage3",
}
con =  pooling.MySQLConnectionPool(pool_name = "mypool",
                              pool_size = 3,
                              **config)

# 從環境變數中取得 AWS 設定
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
S3_BUCKET_REGION = os.getenv('S3_BUCKET_REGION')
BUCKET_NAME = os.getenv('BUCKET_NAME')

# 建立新的 S3 用戶端實例，設定區域和認證資訊
s3_client = boto3.client('s3', 
                        region_name = S3_BUCKET_REGION,
                        aws_access_key_id = ACCESS_KEY,
                        aws_secret_access_key = SECRET_ACCESS_KEY) 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/getmessage", methods = ["GET","POST"])

def get_message():
    if request.method == "POST":
        try:
            message = request.form.get('message')  
            image = request.files.get('file')

            if not message or message.strip() == "":
                return jsonify({"error":"留言啦"}), 400
            
            image_url = None
            if image and image.filename.endswith(('jpg', 'jpeg', 'png', 'jfif')):
                filename = secure_filename(image.filename)
                key = f"{str(int(time.time()))}-{filename}" # 生成檔案名稱
                s3_client.upload_fileobj(image, BUCKET_NAME, key)
                image_url = f"https://d1hxt3hn1q2xo2.cloudfront.net/{key}"
            
            connection = con.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("INSERT INTO messages(URL_image, message) VALUES(%s, %s)", (image_url, message))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"ok":"True"}), 200
        except mysql.connector.Error:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            return jsonify({"error": True,"message": "databaseError"}), 500
    
    if request.method == "GET":
        try:
            connection = con.get_connection()
            cursor = connection.cursor(dictionary=True)   
            cursor.execute("SELECT * FROM messages")
            data = cursor.fetchall()
            cursor.close()
            connection.close()
            print(data)
            return_data = {
                "data":data
            }
            return jsonify(return_data), 200
        except mysql.connector.Error:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            return jsonify({"error": True,"message": "databaseError"}), 500
        
app.run(debug=True, host="0.0.0.0", port=4000)