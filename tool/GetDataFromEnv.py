# coding=utf-8
import os


def save_data_to_dict(key, value, env_dict):
    """
    组装从环境变量中获取到的data，并判断是否获取到
    :param key:数据的key
    :param value:数据的value
    :param env_dict:数据
    :return:None
    """
    if value:
        env_dict[key] = str(value)
    else:
        raise ValueError("环境变量获取失败，请检查是否设置了环境变量")


def get_data_from_env():
    """
    获取windows环境变量信息
    :return:Node
    """
    # 使用mongodb数据库的设置
    env_dict = {}
    mongodb_host = os.getenv('MONGODB_HOST')
    save_data_to_dict('MONGODB_HOST', mongodb_host, env_dict)
    mongodb_db_name = os.getenv('MONGODB_DBNAME')
    save_data_to_dict('MONGODB_DBNAME', mongodb_db_name, env_dict)
    mongodb_port = os.getenv('MONGODB_PORT')
    save_data_to_dict('MONGODB_PORT', mongodb_port, env_dict)
    mongodb_password = os.getenv('MONGODB_PASSWD')
    save_data_to_dict('MONGODB_PASSWD', mongodb_password, env_dict)
    mongodb_auth_db = os.getenv('MONGODB_AUTHDB')
    save_data_to_dict('MONGODB_AUTHDB', mongodb_auth_db, env_dict)
    mongodb_sheet_name = os.getenv('MONGODB_SHEETNAME_1')
    save_data_to_dict('MONGODB_SHEETNAME_1', mongodb_sheet_name, env_dict)
    mongodb_user = os.getenv('MONGODB_USER')
    save_data_to_dict('MONGODB_USER', mongodb_user, env_dict)

    # 使用mysql数据库的设置
    mysql_host = os.getenv('MYSQL_HOST')
    save_data_to_dict('MYSQL_HOST', mysql_host, env_dict)
    mysql_user = os.getenv('MYSQL_USER')
    save_data_to_dict('MYSQL_USER', mysql_user, env_dict)
    mysql_password = os.getenv('MYSQL_PASSWD')
    save_data_to_dict('MYSQL_PASSWD', mysql_password, env_dict)
    mysql_db = os.getenv('MYSQL_DB')
    save_data_to_dict('MYSQL_DB', mysql_db, env_dict)
    return env_dict


if __name__ == "__main__":
    data_dict = get_data_from_env()
    print(data_dict)
