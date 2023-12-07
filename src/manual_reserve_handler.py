import logging
from src import messages, static_data

USER_DATA_SELECTED_FOODS_KEY = "manual_reserve_selected_foods"

class ManualReserveInlineHandler:
    def __init__(self, db):
        self.db = db

    async def inline_manual_food_choose_handler(self, update, context, action: str, day, food_id):
        query = update.callback_query
        if action == "IGNORE":
            await context.bot.answer_callback_query(callback_query_id=query.id)
        elif action == "DONE":
            logging.debug(context.user_data[USER_DATA_SELECTED_FOODS_KEY])
            await context.bot.edit_message_text(
                text=messages.manual_reserve_select_food_done,
                chat_id=query.message.chat_id,
                message_id=query.message.message_id
            )
            return static_data.RESERVE_MENU_CHOOSING
        elif action == "CANCEL":
            if context.user_data: context.user_data.clear()
            await context.bot.edit_message_text(
                text=messages.manual_reserve_select_food_canceled,
                chat_id=query.message.chat_id,
                message_id=query.message.message_id
            )
            return static_data.RESERVE_MENU_CHOOSING
        elif action == "SELECT":
            if food_id != "-":
                if not context.user_data.get(USER_DATA_SELECTED_FOODS_KEY):
                    context.user_data[USER_DATA_SELECTED_FOODS_KEY] = {}
                context.user_data.get(USER_DATA_SELECTED_FOODS_KEY)[day] = food_id
                await context.bot.answer_callback_query(callback_query_id=query.id)
            else:
                await context.bot.answer_callback_query(callback_query_id=query.id)
