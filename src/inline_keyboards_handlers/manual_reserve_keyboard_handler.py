import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from src.error_handlers import EmptyReserveTableException
from src.static_data import (
    MEAL_EN_TO_FA
)
from src.messages import (
    next_page_button_message,
    previous_page_button_message,
    done_button_message,
    cancel_button_message
)

class ManualReserveKeyboardHandler:
    @staticmethod
    def create_food_list_keyboard(food_table: dict, food_court_id, selected_foods=None, page:int=0) -> InlineKeyboardMarkup:
        if selected_foods is None:
            selected_foods = {}

        keyboard = []
        meal = 'lunch'
        logging.debug(food_table)
        food_list = [(day, food_values[meal]) for day, food_values in food_table.items()]
        food_list.reverse()
        if len(food_list) == 0:
            return InlineKeyboardMarkup(keyboard)
        for day, foods in food_list:
            row = []
            for food in foods:
                food_name = food['food']
                food_id = food['food_id']
                if selected_foods.get(meal):
                    if selected_foods.get(meal).get(day) == food_id:
                        food_name = '✅ ' + food_name
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
        row.append(InlineKeyboardButton(
            ' ', callback_data=ManualReserveKeyboardHandler.create_callback_data("IGNORE")))
        row.append(
            InlineKeyboardButton(
                done_button_message, callback_data=ManualReserveKeyboardHandler.create_callback_data(
                    action="DONE",
                    food_court_id=food_court_id,
                    page=page)
            )
        )
        row.append(
            InlineKeyboardButton(
                cancel_button_message, callback_data=ManualReserveKeyboardHandler.create_callback_data("CANCEL")))
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