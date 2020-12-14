import os


def get_env(env_name):
    mongodb_password = os.getenv(env_name)
    if isinstance(mongodb_password, str):
        print(mongodb_password)
    if isinstance(int(os.getenv('MONGODB_PORT')), int):
        print(os.getenv('MONGODB_PORT'))
    print(os.getenv('MONGODB_HOST'))
    print(os.getenv('MONGODB_DBNAME'))
    print(os.getenv('MONGODB_PORT'))
    print(os.getenv('MONGODB_AUTHDB'))
    print(os.getenv('MONGODB_USER'))
    print(os.getenv('MONGODB_SHEETNAME_1'))
    print(os.getenv('MYSQL_HOST'))
    print(os.getenv('MYSQL_USER'))
    print(os.getenv('MYSQL_PASSWD'))
    print(os.getenv('MYSQL_DB'))
    print(os.getenv('START_URL'))


if __name__ == '__main__':
    get_env('MONGODB_PASSWD')
