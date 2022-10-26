import pymysql as my

def selectUsers(uid, upw):
    row = None
    connection = None
    try:
        connection = my.connect(host='192.168.1.45',
                                user='swcore',
                                password='core2020',  # 사용자가 지정한 비밀번호
                                database='logger',
                                cursorclass=my.cursors.DictCursor
                                )
        cursor = connection.cursor()
        sql = '''SELECT * FROM userAccount WHERE userId=%s AND userPasswd=password(%s)'''
        cursor.execute(sql, (uid, upw))
        row = cursor.fetchone()
    except Exception as e:
        print('접속오류', e)
    finally:
        if connection:
            connection.close()
    return row
if __name__ == '__main__':
    row = selectUsers('guest', '1')
    print('쿼리회원조회결과 : ', row)
    row = selectUsers('guest', '2')
    print('회원조회결과 : ', row)