import datetime
import sqlite3
import settings
import random
import pygame
import typing

operation_to_operator = {"addition": "+", "subtraction": "-", "multiplication": "*"}


def prepare_database(filename: str):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE "amount" (
	        "amount_id" INTEGER,
	        "num_amount" INTEGER,
	        PRIMARY KEY("amount_id")
        )"""
    )

    cursor.execute(
        """
        CREATE TABLE "category" (
            "category_id" INTEGER,
            "name" TEXT,
            "amount_id" INTEGER,
            PRIMARY KEY("category_id"),
            FOREIGN KEY("amount_id") REFERENCES "amount"("amount_id")
        )
        """
    )
    cursor.execute(
        """ 
        CREATE TABLE "digit" (
            "digit_id" INTEGER,
            "num_digit" INTEGER,
            PRIMARY KEY("digit_id")
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE "category_digit" (
            "category_id" INTEGER,
            "digit_id" INTEGER,
            FOREIGN KEY("category_id") REFERENCES "category"("category_id"),
            FOREIGN KEY("digit_id") REFERENCES "digit"("digit_id")
        )
        """
    )

    cursor.execute(
        """ 
        CREATE TABLE "operation" (
            "operation_id" INTEGER,
            "name" TEXT,
            PRIMARY KEY("operation_id")
        )
        """
    )

    cursor.execute(
        """ 
        CREATE TABLE "category_operation" (
            "category_id" INTEGER,
            "operation_id" INTEGER,
            FOREIGN KEY("category_id") REFERENCES "category"("category_id"),
            FOREIGN KEY("operation_id") REFERENCES "operation"("operation_id")
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE "score" (
            "score_id" INTEGER,
            "name" STRING,
            "result" DOUBLE,
            "date" DATE,
            "category_id" INTEGER,
            PRIMARY KEY("score_id")
        )
        """
    )
    # TODO: add blind time table
    connection.commit()
    connection.close()


def draw_text(
    text,
    x: int,
    y: int,
    screen: pygame.Surface,
    center: bool = True,
<<<<<<< HEAD
    text_color: list[int] = settings.colors.BLACK,
=======
    text_color: tuple[int, int, int] = typing.get_args(settings.Color.BLACK.value),
>>>>>>> 66847b9 (Fix type hinting)
    font: pygame.font.FontType = settings.main_font_small,
):
    text_obj = font.render(str(text), True, text_color)
    text_rect = text_obj.get_rect(topleft=(x, y))
    if center:
        text_rect.center = x, y
    screen.blit(text_obj, text_rect)


# TODO: test function
def select_category_id(cursor: sqlite3.Cursor, game_args: dict):
    operation = game_args["mode"]
    digit = game_args["num_digits"]
    amount = game_args["num_operations"]
    category_name = f"{operation}_digits_{digit}_amount_{amount}"
    cursor.execute(
        "SELECT category_id FROM category WHERE name=?",
        (category_name,),
    )
    return cursor.fetchone()[0]


def save(game_args: dict, username: str, result: float):
    database = sqlite3.connect("scores.db")
    cursor = database.cursor()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    category_id = select_category_id(cursor, game_args)
    cursor.execute(
        """
                   SELECT COUNT(1) FROM score WHERE name = ? AND result = ? AND date = ? AND category_id = ?
                   """,
        (username, result, date, category_id),
    )
    exists = cursor.fetchall()[0][0]
    if exists:
        return
    cursor.execute(
        """
            INSERT INTO score (name, result, date, category_id) VALUES (?, ?, ?, ?)
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


def show_leaderboard(game_args: dict, screen, x: int, y: int):
    leaderboard = read_results(game_args)
    show_leaderboard = min(10, len(leaderboard))

    for i in range(show_leaderboard):
        draw_text(
            text=f"{i+1}. {leaderboard[i][0]} {leaderboard[i][1]}",
            x=x,
            y=y + i * 50,
            screen=screen,
        )


def get_equation(operator, digits: int) -> tuple[int, int, int, str]:
    if operator == "*" and digits == 1:
        # don't multiply by one
        random_digits = "".join([str(random.randint(2, 9)) for _ in range(2 * digits)])
    else:
        random_digits = "".join([str(random.randint(1, 9)) for _ in range(2 * digits)])

    x = int(random_digits[:digits])
    y = int(random_digits[digits:])
    result = 0
    if operator == "+":
        result = x + y
    elif operator == "-":
        result = abs(x - y)
    elif operator == "*":
        result = x * y
    return x, y, result, operator


def get_all_equations(operator, n: int, digits: int) -> list[tuple]:
    return [get_equation(operator, digits) for _ in range(n)]


# TODO: validate answer
def check_equation(answer: str, result: int) -> bool:
    if answer == "":
        return False
    try:
        integer_answer = int(answer)
    except ValueError as _:
        return False
    return integer_answer == result
