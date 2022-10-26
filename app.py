from flask import Flask , request, render_template, redirect
from dbconn import selectUsers
import pymysql

db=None
cur=None
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('./login/login.html')

@app.route('/logman')  # 요청
def okhome():
    db = pymysql.connect(host='192.168.1.45', user='swcore', password='core2020', db='logger', charset='utf8')
    cur = db.cursor()
    sql = "select * from inoutT order by d002 desc limit 500"
    cur.execute(sql)
    result = cur.fetchall()
    db.close()
    return render_template("stat/indexok.html", result=result)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('./login/login.html')
    else:
        uid = request.form.get('uid')
        upw = request.form.get('upw')
        row = selectUsers(uid, upw)
        if row:
            return redirect('/logman')
        else:
            return '''
                <script>
                    // 경고창 
                    alert("로그인 실패, 다시 시도하세요")
                    // 이전페이지로 이동
                    history.back()
                </script>
            '''

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
