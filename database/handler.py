import sqlite3
import time

sqlite = sqlite3.connect('bot.db', check_same_thread=False)
cursor = sqlite.cursor()

def create_tables():
    cursor.execute(" CREATE TABLE IF NOT EXISTS `product` (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                   "`name` VARCHAR(16) NOT NULL, `description` TEXT NOT NULL, `price` INT NOT NULL, "
                   "'min_count' INT default '1', 'max_count' INT default '1', 'count_buys' INT NOT NULL)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `basket` (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, `buyer` INT NOT NULL,"
        "`product` INT NOT NULL, `count` INT NOT NULL, `total_amount` INT NOT NULL, `status` VARCHAR NOT NULL)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `user` (`id` INT NOT NULL, `first_name` VARCHAR(32) NOT NULL, "
        "`latest_buy` INT NOT NULL, `registered` INT NOT NULL, `total_amount` INT NOT NULL, `mailing` INT default '1')")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `admin` (`id` INT NOT NULL, `username` VARCHAR NOT NULL)")

    sqlite.commit()
    pass

# PRODUCT MODEL

def create_product(option: dict):
    list = [
        (option['name'], option['description'], option['price'], option['min_count'],
         option['max_count'], 0)
    ]

    result = cursor.executemany("INSERT INTO `product` VALUES (null, ?, ?, ?, ?, ?, ?)", list)
    sqlite.commit()
    return result

def all_products():
    return cursor.execute('SELECT * FROM `product`')

def range_products(options: dict):
    return cursor.execute(f"SELECT * FROM `product` WHERE `id` BETWEEN '{options['from']}' AND '{options['to']}' ORDER BY `id` DESC")

def get_product(id):
    product = cursor.execute(f"SELECT * FROM `product` WHERE `id`='{id}'")
    return product.fetchone()

def update_product(id, key, value):
    cursor.execute(f"UPDATE `product` SET `{key}`='{value}' WHERE `id`='{id}'")
    sqlite.commit()
    pass

def remove_product(id):
    cursor.execute("DELETE FROM `product` WHERE `id`=?", [(id)])
    sqlite.commit()
    pass

# BASKET MODEL

def create_basket(option: dict):
    list = [
        (option['buyer'], option['product'], option['count'],
         option['total_amount'], option['status'])
    ]

    result = cursor.executemany("INSERT INTO `basket` VALUES (null, ?, ?, ?, ?, ?)", list)
    sqlite.commit()
    return result

def all_baskets():
    return cursor.execute('SELECT * FROM `basket`')

def get_basket(id: int):
    basket = cursor.execute(f"SELECT * FROM `basket` WHERE `id`='{id}'")
    return basket.fetchone()

def get_actived_baskets_on_user(id: int):
    return cursor.execute(f"SELECT * FROM `basket` WHERE `status`='active' AND `buyer`='{id}'")

def get_wait_baskets_on_user(id: int):
    return cursor.execute(f"SELECT * FROM `basket` WHERE `status`='wait' AND `buyer`='{id}'")

def count_actived_baskets_on_user(id: int):
    cursor.execute(f"SELECT * FROM `basket` WHERE `status`='active' AND `buyer`='{id}'")
    return cursor.fetchall()


def update_basket(id, key, value):
    cursor.execute(f"UPDATE `basket` SET `{key}`='{value}' WHERE `id`='{id}'")
    sqlite.commit()
    pass

def remove_basket(id: int):
    cursor.execute("DELETE FROM `basket` WHERE `id`=?", [(id)])
    sqlite.commit()
    pass

# ADMIN MODEL

def all_admins():
    return cursor.execute('SELECT * FROM `admin`')

def add_admin(tid, username):
    list = [
        (tid, username)
    ]
    cursor.executemany("INSERT INTO `admin` VALUES (?, ?)", list)
    sqlite.commit()
    pass

def remove_admin(tid):
    cursor.execute("DELETE FROM `admin` WHERE `id`=?", [(tid)])
    sqlite.commit()
    pass

def get_admin(tid):
    user = cursor.execute(f"SELECT * FROM `admin` WHERE `id`='{tid}'")
    user = user.fetchone()

    if user is None:
        return False

    return user

# USER MODEL

def add_user(id: int, option: dict):
    list = [
        (id, '', 0, int(time.time()), 0, 0)
    ]
    cursor.executemany("INSERT INTO `user` VALUES (?, ?, ?, ?, ?, ?)", list)
    sqlite.commit()
    pass

def update_user(id, key, value):
    cursor.execute(f"UPDATE `user` SET `{key}`='{value}' WHERE `id`='{id}'")
    sqlite.commit()
    pass

def get_user(id):
    user = cursor.execute(f"SELECT * FROM `user` WHERE `id`='{id}'")
    user = user.fetchone()

    if user is None:
        return False

    return user

def all_users():
    return cursor.execute(f"SELECT * FROM `user`")

def reset_sequence(table: str):
    cursor.execute(f"UPDATE `sqlite_sequence` SET `seq`='0' WHERE `name`='{table}'")
    sqlite.commit()

def table_count(table):
    count = cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
    return count.fetchone()[0]

def last_id(table):
    id = cursor.execute(f"SELECT * FROM `{table}` ORDER BY `id` DESC LIMIT 1")

    return id.fetchone()[0]