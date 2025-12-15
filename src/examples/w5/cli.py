import typer

from examples.w5 import read_file, run


app = typer.Typer()


@app.command()
def w5_read_file(
    file_name: str = typer.Argument("my.pdf", help="""Файл"""),
    count: int = typer.Option(1, min=1, max=3, help="""Количество повторов."""),
):
    """Пример с чтением с Enum"""
    for i in range(count):
        print(i)
        print(read_file(file_name=file_name))


@app.command()
def w5_queues():
    """Пример с очередями"""
    run()


if __name__ == "__main__":
    app()
