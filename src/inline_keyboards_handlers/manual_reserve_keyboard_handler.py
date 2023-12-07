import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from src.messages import (
    next_page_button_message,
    previous_page_button_message,
    done_button_message,
    cancel_button_message
)

class ManualReserveKeyboardHandler:
    @staticmethod
    def create_food_list_keyboard(food_table: dict) -> InlineKeyboardMarkup:
        keyboard = []
        food_list: list = [value["lunch"] for value in food_table.values()]
        food_list.reverse()
        for food_row in food_list:
            row = []
            for food in food_row:
                food_name = food["food"]
                food_id = food["food_id"]
                day = food["program_date"]
                logging.debug("MANUAL_RESERVE :: {}".format(food_name))
                row.append(
                    InlineKeyboardButton(
                        food_name,
                        callback_data=ManualReserveKeyboardHandler.create_callback_data(action="SELECT", food_id=food_id, day = day)
                    ))
            keyboard.append(row)

        row = [
            InlineKeyboardButton(
                " ", callback_data=ManualReserveKeyboardHandler.create_callback_data("IGNORE")),
            InlineKeyboardButton(
                done_button_message, callback_data=ManualReserveKeyboardHandler.create_callback_data("DONE")),
            InlineKeyboardButton(
                cancel_button_message, callback_data=ManualReserveKeyboardHandler.create_callback_data("CANCEL")),
            InlineKeyboardButton(
                " ", callback_data=ManualReserveKeyboardHandler.create_callback_data("IGNORE")),
        ]
        keyboard.append(row)

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def create_callback_data(action: str, food_id: str = "-", day: str = "-") -> str:
        return "MANUAL_RESERVE" + ";" + ";".join([action, food_id, day])

    @staticmethod
    def separate_callback_data(data: str) -> list:
        return data.split(";")