from datetime import date
import uuid
from examples.w4classes.singleton import Singleton
import psycopg

class Database(metaclass=Singleton):
    def __init__(self, database, host, user, password, port) -> None:
        if "conn" not in self.__dict__:
            if all((database, host, user, password, port)):
                self.database = database
                self.host = host
                self.user = user
                self.password = password
                self.port = port

                self.conn = self.connect()
            else:
                raise AttributeError("DB not initialized")
    
    def connect(self):
        return psycopg.connect(
            dbname=self.database,
            host =        self.host,
            user = self.user,
            password = self.password,
            port = self.port
            )
    # async def init_connect():
    #     self.conn = await aiopg.connect (....)

    def select_t1(self):
        res = {}
        with self.conn.cursor() as cur:
            cur.execute("select id, name from t1")
            for record in cur:
                t1_id = record[0]
                # res["t1"] = t1_id

                cur2 = self.conn.cursor()
                cur2.execute(
                    "select * from t1_details where t1_code=%s",
                    (t1_id,))
                columns = [desc[0] for desc in cur2.description]
                real_dict = [dict(zip(columns,row)) for row in cur2.fetchall()]
                res[t1_id] =real_dict
                cur2.close()
        return res
    
    def insert_t1(self, name, details):
        try:
            insert_t1 = "INSERT INTO t1 (id, name) VALUES (%s, %s)"
            insert_t1_details = "INSERT INTO t1_details (t1_code, from_date, position) VALUES (%s,%s,%s)"
            id = str(uuid.uuid4())
            with self.conn.cursor() as cur:
                cur.execute(insert_t1, (id, name))
                if details:
                    with self.conn.cursor() as cur:
                        data = [(id, from_date, position) for position ,from_date in details.items()]
                        cur.executemany(insert_t1_details, data)
            
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

if __name__ == "__main__":
    db = Database(database="tstbase", host="localhost", user="postgres", password="pgpwd", port=5432)

    db.insert_t1("aaaaa", {"p1": date(2001,2,1), "p2": date(2010, 5,1)})

    data = db.select_t1()

    for i_t1, (t1, t1_detail) in enumerate(data.items(), start=1):
        print(f"{i_t1=} - {t1=}")
        for i_d, detail in enumerate(t1_detail, start=1):
            print(f"\t{i_d} - {detail=}")