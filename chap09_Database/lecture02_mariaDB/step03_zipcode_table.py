'''
text file -> DB 저장

<작업 순서>
1. table 생성
2. zipcode.txt -> readline(서울) -> 레코드 저장
3. table 저장 -> 동으로 검색

code     city  gu     dong              detail
135-806	서울	강남구	개포1동 경남아파트		1
135-807	서울	강남구	개포1동 우성3차아파트	(1∼6동)	2
'''

import pymysql

config = {
    'host' : '127.0.0.1',
    'user' : 'scott',
    'password' : 'tiger',
    'database' : 'work',
    'port' : 3306,
    'charset':'utf8',
    'use_unicode' : True}

try :
    conn = pymysql.connect(**config)
    cursor = conn.cursor()

    # 테이블 생성
    sql = """create table zipcode_tab(
    code char(14) not null,
    city char(20) not null,
    gu varchar(20) not null,
    dong varchar(80) not null,
    detail varchar(50))"""
    cursor.execute(sql)
    print('1.테이블 작성 완료')

    # 레코드 조회 및 레코드 추가
    sql = "select * from zipcode_tab"
    cursor.execute(sql)
    data = cursor.fetchall()

    if data:  # True : 검색
        for row in data:
            print("[%s]    %s   %s   %s  %s" % row)

        print('전체 레코드 수 : ', len(data))

        ### 1. 동 검색
        dong = input("검색할 동 입력 :")
        sql = f"select * from zipcode_tab where dong like '%{dong}%'"
        cursor.execute(sql)
        data2 = cursor.fetchall()
        if data2:
            for row in data2:
                print("[%s]    %s   %s   %s  %s" % row)

            print('검색된 레코드 수:', len(data2))
        else:
            print('검색된 레코드 없음')

        ### 2. 구 검색
        gu = input("검색할 구 입력 :")
        sql = f"select * from zipcode_tab where gu like '%{gu}%'"
        cursor.execute(sql)
        data3 = cursor.fetchall()
        if data3:
            for row in data3:
                print("[%s]    %s   %s   %s  %s" % row)

            print('검색된 레코드 수:', len(data3))
        else:
            print('검색된 레코드 없음')


    else:  # False : 레코드 추가
        file = open("./chap09_Database/data/zipcode.txt", encoding='utf-8')
        line = file.readline()

        while line:
            row = line.split('\t')
            if row[1] == '서울':
                code = str(row[0])
                city = row[1]
                gu = row[2]
                dong = row[3]
                detail = row[4]  # 세부주소

                if detail:
                    sql = f"""insert into zipcode_tab 
                    values('{code}','{city}','{gu}','{dong}','{detail}')"""
                else:
                    sql = f"""insert into zipcode_tab(code,city,gu,dong) 
                    values('{code}','{city}','{gu}','{dong}')"""

                cursor.execute(sql)
                conn.commit()
            line = file.readline()  # 2~n번
        file.close()
        print('2. 레코드 추가 성공')


except Exception as e:
    print(e)
    conn.rollback()
finally:
    cursor.close()
    conn.close()
