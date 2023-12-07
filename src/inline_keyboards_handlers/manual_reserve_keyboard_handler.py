import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from src.error_handlers import EmptyReserveTableException
from src.messages import (
    next_page_button_message,
    previous_page_button_message,
    done_button_message,
    cancel_button_message
)

class ManualReserveKeyboardHandler:
    @staticmethod
    def create_food_list_keyboard(food_table: dict, food_court_id, selected_foods=None,page: int=0) -> InlineKeyboardMarkup:
        if selected_foods is None:
            selected_foods = {}
        keyboard = []
        if not len(food_table.items()):
            return InlineKeyboardMarkup(keyboard)

        meal, reserve_dict = list(food_table.items())[page]
        for day, foods in reserve_dict.items():
            row = []
            for food in foods:
                food_name = food['food']
                food_id = food['food_id']
                if selected_foods.get(meal):
                    if selected_foods.get(meal).get(day) == food_id:
                        food_name = '✅ '+food_name
                row.append(
                    InlineKeyboardButton(
                        food_name,
                        callback_data=ManualReserveKeyboardHandler.create_callback_data(
                            action="SELECT",
                            food_id=food_id,
                            day=day,
                            food_court_id=food_court_id,
                            page=page,
                        )
                    )
                )
            keyboard.append(row)
        row = []
        if page > 0:
            row.append(
                InlineKeyboardButton(
                    previous_page_button_message, callback_data=ManualReserveKeyboardHandler.create_callback_data("PREV")),
            )
        else:
            row.append(InlineKeyboardButton(
                ' ', callback_data=ManualReserveKeyboardHandler.create_callback_data("IGNORE")))
        row.append(
            InlineKeyboardButton(
                done_button_message, callback_data=ManualReserveKeyboardHandler.create_callback_data("DONE")))
        row.append(
            InlineKeyboardButton(
                cancel_button_message, callback_data=ManualReserveKeyboardHandler.create_callback_data("CANCEL")))
        if page+1< len(food_table):
            row.append(
                InlineKeyboardButton(
                next_page_button_message, callback_data=ManualReserveKeyboardHandler.create_callback_data("NEXT")))
        else:
            row.append(
                InlineKeyboardButton(
                    ' ', callback_data=ManualReserveKeyboardHandler.create_callback_data("IGNORE")))
        keyboard.append(row)

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def create_callback_data(action: str, food_id: str = '-', day: str = '-', food_court_id: str = '-', page: int = 0) -> str:
        return "MANUAL_RESERVE" + ";" + ";".join([action, day, food_id, food_court_id, str(page)])

    @staticmethod
    def separate_callback_data(data: str) -> list:
        return data.split(";")