from flask import *
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os, boto3
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
                        access_key = ACCESS_KEY,
                        secret_access_key = SECRET_ACCESS_KEY)

@app.route("/api/getmessage", methods = ["POST"])

def get_message():
    try:
        message = request.form.get('message')  # 获取文本信息
        image = request.files.get('image')

        if message == "":
            return '留言啦', 400
        
        if image.filename:
            return '沒有上傳檔案', 400
        
        if image and image.filename.endswith(('jpg', 'jpeg', 'png', 'jfif')):
            filename = secure_filename(image.filename)
            key = f"{str(int(time.time()))}-{filename}" # 生成檔案名稱

        s3_client.upload_fileobj(image, BUCKET_NAME, key)
        image_url = f"https://{BUCKET_NAME}.s3.{S3_BUCKET_REGION}.amazonaws.com/{key}"

        connection = con.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("INSERT INTO messages(URL_image, message) VALUES(%s, %s)", (message, image_url))
        connection.commit()
        
        cursor.execute("SELECT * FROM messages")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify({"message": data['message'], "URL_image": data['URL_image']}), 200
    except mysql.connector.Error:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        return jsonify({"error": True,"message": "databaseError"}), 500

app.run(debug=None, host="0.0.0.0", port=4000)