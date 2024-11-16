import sqlite3
import datetime
import settings


def prepare_database(
    filename: str,
):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE "amount" (
	        "amount_id" INTEGER,
	        "amount_of_calculations" INTEGER,
	        PRIMARY KEY("amount_id")
        )"""
    )

    cursor.execute(
        """ 
        CREATE TABLE "digits" (
            "digit_id" INTEGER,
            "num_of_digits_per_variable" INTEGER,
            PRIMARY KEY("digit_id")
        )
        """
    )

    cursor.execute(
        """ 
        CREATE TABLE "operation" (
            "operation_id" INTEGER,
            "operation_name" TEXT,
            PRIMARY KEY("operation_id")
        )
        """
    )

    cursor.execute(
        """ 
        CREATE TABLE "flash" (
            "flash_id" INTEGER,
            "flash_time" TEXT,
            PRIMARY KEY("flash_id")
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE "category" (
            "category_id" INTEGER,
            "amount_id" INTEGER,
            "digit_id" INTEGER,
            "operation_id" INTEGER,
            "flash_id" INTEGER,
            PRIMARY KEY("category_id"),
            FOREIGN KEY("amount_id") REFERENCES "amount"("amount_id"),
            FOREIGN KEY("digit_id") REFERENCES "digits"("digit_id"),
            FOREIGN KEY("operation_id") REFERENCES "operation"("operation_id"),
            FOREIGN KEY("flash_id") REFERENCES "flash"("flash_id")
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE "score" (
            "score_id" INTEGER,
            "username" STRING,
            "result" DOUBLE,
            "date" DATE,
            "category_id" INTEGER,
            PRIMARY KEY("score_id"),
            FOREIGN KEY("category_id") REFERENCES "category"("category_id")
        )
        """
    )
    connection.commit()
    connection.close()


def populate_database(
    filename: str,
    num_of_digits: tuple[int, ...],
    amounts_of_calculations: tuple[int | str, ...],
    operations_names: tuple[str, ...],
    flash_times: tuple[str, ...],
):
    # open database if it exists
    connection = sqlite3.connect(f"file:{filename}?mode=rw", uri=True)
    cursor = connection.cursor()
    for amount in amounts_of_calculations:
        cursor.execute(
            f"""
            INSERT INTO amount (amount_of_calculations) values ({amount})
            """
        )
    for name in operations_names:
        cursor.execute(
            f"""
            INSERT INTO operation (operation_name) values ('{name}')
            """
        )
    for num in num_of_digits:
        cursor.execute(
            f"""
            INSERT INTO digits (num_of_digits_per_variable) values ({num})
            """
        )
    for time in flash_times:
        cursor.execute(
            f"""
            INSERT INTO flash (flash_time) values ('{time}')
            """
        )
    for amount_id, amount in enumerate(amounts_of_calculations, start=1):
        for operation_id, operation in enumerate(operations_names, start=1):
            for digit_id, digit in enumerate(num_of_digits, start=1):
                for flash_id, flash in enumerate(flash_times, start=1):
                    cursor.execute(
                        """
                        INSERT INTO category (amount_id, digit_id, operation_id, flash_id) values (?, ?, ?, ?)
                        """,
                        (amount_id, digit_id, operation_id, flash_id),
                    )

    connection.commit()
    connection.close()


def select_category_id(cursor: sqlite3.Cursor, game_args: dict):
    operation = game_args["mode"]
    digit = game_args["num_digits"]
    amount = game_args["num_operations"]
    flash = game_args["flash"]

    cursor.execute(
        "SELECT operation_id FROM operation WHERE operation_name=?",
        (operation,),
    )
    operation_id = cursor.fetchone()[0]

    cursor.execute(
        "SELECT digit_id FROM digits WHERE num_of_digits_per_variable=?",
        (digit,),
    )
    digit_id = cursor.fetchone()[0]

    cursor.execute(
        "SELECT amount_id FROM amount WHERE amount_of_calculations=?",
        (amount,),
    )
    amount_id = cursor.fetchone()[0]

    cursor.execute(
        "SELECT flash_id FROM flash WHERE flash_time=?",
        (flash,),
    )
    flash_id = cursor.fetchone()[0]

    cursor.execute(
        "SELECT category_id FROM category WHERE operation_id=? AND digit_id=? AND amount_id=? AND flash_id=?",
        (operation_id, digit_id, amount_id, flash_id),
    )
    return cursor.fetchone()[0]


def save(game_args: dict, username: str, result: float):
    database = sqlite3.connect("scores.db")
    cursor = database.cursor()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    category_id = select_category_id(cursor, game_args)
    cursor.execute(
        """
                   SELECT COUNT(1) FROM score WHERE username = ? AND result = ? AND date = ? AND category_id = ?
                   """,
        (username, result, date, category_id),
    )
    exists = cursor.fetchall()[0][0]
    if exists:
        return
    cursor.execute(
        """
            INSERT INTO score (username, result, date, category_id) VALUES (?, ?, ?, ?)
        """,
        (username, result, date, category_id),
    )
    database.commit()
    database.close()


def read_results(game_args: dict):
    database = sqlite3.connect("scores.db")
    cursor = database.cursor()
    category_id = select_category_id(cursor, game_args)
    cursor.execute(f"SELECT * FROM score WHERE category_id = {category_id}")
    results = cursor.fetchall()
    to_show = [(result[1], result[2]) for result in results]
    to_show_sorted = sorted(to_show, key=lambda x: x[1])[:10]
    database.close()
    return to_show_sorted
