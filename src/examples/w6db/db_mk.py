from pathlib import Path
from examples.w6db.database import Database


def load_file(file_name):
    try:
        with open(file_name, "rb") as f:
            file_data = f.read()

            db = Database()
            with db.conn.cursor() as cur:
                cur.execute("INSERT INTO files(filename, file_data) VALUES (%s,%s) RETURNING id",
                            (Path(file_name).name, file_data),
                )
                id = cur.fetchone()[0]
                db.conn.commit()
        return id
    except Exception as e:
        print(e)

def save_file(file_name, file_id) -> None:
    db = Database()
    with open(file_name, "wb") as f:
        with db.conn.cursor() as cur:
            cur.execute("SELECT file_data, filename FROM files WHERE id = %s",
                        (int(file_id),))
            (file_data, file_name ) = cur.fetchone()
            f.write(file_data)


if __name__ == "__main__":
    Database(database="tstbase", host="localhost", user="postgres", password="pgpwd", port=5432)
    file_id = load_file("data/cv_examples/Васильев Дмитрий Андреевич.docx")
    print(file_id)
    if file_id:
        save_file("/tmp/Васильев Дмитрий Андреевич.docx", file_id)