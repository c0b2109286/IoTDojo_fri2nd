import sqlite3
import csv
if __name__ == "__main__":
    # データベースへの接続（データベースが存在しない場合は新規作成）
    conn = sqlite3.connect("./instance/location.db")
    # カーソルオブジェクトの作成
    c = conn.cursor()

    # テーブルの作成
    c.execute('''CREATE TABLE sensor (id text,val text,date text,time text)''')

    # # テーブルにデータを追加
    # c.execute("INSERT INTO stocks VALUES ('2023-07-06','BUY','RHAT',100,35.14)")

    # テーブルの削除
    #c.execute("DROP TABLE VAL")
    
    # # 変更をコミット（保存）
    # conn.commit()

    # # カラムの追加
    # c.execute("ALTER TABLE VAL ADD COLUMN 'd' ")

    # # 新しいカラムにデータを追加
    # c.execute("UPDATE stocks SET extra = 20.53 WHERE symbol = 'RHAT'")
    


    # CSVファイルを開く
    with open('sampleuser.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)  # CSVリーダーオブジェクトを作成

        for row in reader:  # CSVファイルの各行をイテレート
            if len(row)==4:
                # 同じIDのデータがすでに存在する場合、それを削除
                c.execute("DELETE FROM sensor WHERE id = ?", (row[0],))

                # 新しいデータを挿入
                c.execute("INSERT INTO sensor VALUES (?, ?, ?, ?)", (row[0], row[1], row[2], row[3]))

    # 変更をコミット（保存）
    conn.commit()

    # # データベースからデータを取得して表示
    # c.execute('SELECT * FROM VAL WHERE (gps)')
    # print(c.fetchall())

    # 接続を閉じる
    conn.close()