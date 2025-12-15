import platform
import os
import nox

os_platform = platform.system()


# @nox.session
# def hello(session):
#     """Пример команды."""
#     if os_platform == "Linux":
#         print("hello linux")
#     elif os_platform == "Windows":
#         print("hello windows")

#     print("Just hello")


@nox.session
def postgres(session):
    """Запустить postgres."""

    # Директория для сохранения данных
    session.run(
        "mkdir",
        "-p",
        # "-m",
        # "777",
        "./.postgres_data",
        external=True,
    )
    # Убрать права: sudo chmod -R 777 ./.postgres_data

    # Запуск образа postgres
    session.run(
        "sudo",
        "docker",
        "run",
        "-d",
        "-p",
        "5432:5432",
        "-e",
        "POSTGRES_PASSWORD=pgpwd",
        "-e",
        "POSTGRES_DB=tstbase",
        "-e",
        "PGDATA=/var/lib/postgresql/data/pgdata",
        "-v",
        f"{os.path.abspath('./.postgres_data')}:/var/lib/postgresql/data",
        "-v",
        f"{os.path.abspath('./migrations')}:/docker-entrypoint-initdb.d",
        "postgres:17.0",
        external=True,
    )
    print("---------")
    print("Connect to postgres")
    print("base : tstbase")
    print("POSTGRES_PASSWORD : pgpwd")


# # @nox.session
# # def nginx(session):
# #     """
# #     Заготовка для nginx
# #     """

# #     print("---------")
# #     print("For example: Open http://localhost:8080 in browser")

# #     # Директория для nginx
# #     session.run(
# #         "mkdir",
# #         "-p",
# #         "./data/.example_html",
# #         "./.nginx_conf",
# #         external=True,
# #     )

# #     # Пример создания файла
# #     try:
# #         with open("./data/.example_html/index.html", "x") as f:
# #             f.write(
# #                 """<html>
# #     <body>
# #         Hello from nginx nox docker!
# #     </body>
# # </html>"""
# #             )
# #     except FileExistsError:
# #         print("HTML already exists.")

# #     # TODO:
# #     # Вставить сюда создания nginx.conf (.nginx_conf/nginx.conf)

#     # Запуск образа
#     session.run(
#         # "sudo",
#         "docker",
#         "run",
#         "-d",  # Отключить для отладки
#         "-p",
#         "8080:80",
#         "-v",
#         "./data/.example_html/:/usr/share/nginx/html:ro",
#         # "-v",
#         # ВСТАВИТЬ ПРОБРОС КОНФИГА nginx.conf",
#         "nginx",
#         external=True,
#     )

# @nox.session
# def minio(session):
#     print("api: http://127.0.0.1:9000")
#     print("ui: http://127.0.0.1:9090")
#     print("minioadmin/minioadmin")

#     session.run(
#         # "sudo",
#         "docker",
#         "run",
#         "-d",
#         "-p",
#         "9000:9000",
#         "-p",
#         "9090:9090",
#         "minio/minio",
#         "server",
#         "/export",
#         "--console-address",
#         ":9090"
#     )


# @nox.session
# def rabbit(session):
#     print("api: http://127.0.0.1:5672")
#     print("ui: http://127.0.0.1:15672")
#     print("user/password")

#     session.run(
#         # "sudo",
#         "docker",
#         "run",
#         # "-d",
#         "--rm",
#         "--name",
#         "rabbitmq",
#         "-p",
#         "5672:5672",
#         "-p",
#         "15672:15672",
#         "-e",
#         "RABBITMQ_DEFAULT_USER=user",
#         "-e",
#         "RABBITMQ_DEFAULT_PASS=password",
#         "rabbitmq:3-management"
#     )
