from flask import Flask
from flask import request,jsonify
import pymysql
from config import *
app = Flask(__name__)

class MySqlPipeline():
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=Mysql_host,
            db=Mysql_db,
            user=Mysql_user,
            passwd=Mysql_password,
            charset='utf8mb4',
            port=MYSQL_PORT,
            use_unicode=True
        )
        self.top_n=10

        self.cursor = self.connect.cursor()
    def get_top_music(self):
        self.cursor.execute(
            "SELECT video_url FROM video_meta ORDER BY RAND() LIMIT %d" % (self.top_n)
        )
        result = self.cursor.fetchall()
        return [r[0] for r in result]
    def get_top_up(self):
        self.cursor.execute(
            "SELECT up_id FROM video_detail ORDER BY RAND() LIMIT %d" % (self.top_n)
        )
        result = self.cursor.fetchall()
        return [r[0] for r in result]

db = MySqlPipeline()
@app.route('/alo/music_recommend_video',methods=['GET','POST'])
def get_music_recommend():
    try:
        if request.method=='POST':
            uid=request.form.get('uid')
            follows=request.form.get('follows')
            weibos=request.form.get('weibo')
            res={'code':0,"video_urls":db.get_top_music()}
            return jsonify(res)
    except Exception as error:
        print(error)

@app.route('/alo/music_recommend_up',methods=['GET','POST'])
def get_up_recommend():
    try:
        if request.method=='POST':
            uid=request.form.get('uid')
            follows=request.form.get('follows')
            weibos=request.form.get('weibo')
            res={'code':0,"up_master":db.get_top_up()}
            return jsonify(res)
    except Exception as error:
        print(error)

if __name__ == '__main__':
    app.run()
