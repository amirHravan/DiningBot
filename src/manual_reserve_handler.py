from src.dining import Dining
import logging
from src import messages, static_data
from telegram.ext import ApplicationBuilder
from src.inline_keyboards_handlers.manual_reserve_keyboard_handler import  ManualReserveKeyboardHandler

USER_DATA_SELECTED_FOODS_KEY = "manual_reserve_selected_foods"

class ManualReserveHandler:
    def __init__(self, token="TOKEN", admin_ids=set(), log_level='INFO', db=None) -> None:
        self.db = db
        self.token = token
        self.admin_ids = admin_ids
        self.food_table = {}

        logging.basicConfig(
            format='%(asctime)s - %(levelname)s - %(message)s',
            level={
                'INFO': logging.INFO,
                'DEBUG': logging.DEBUG,
                'ERROR': logging.ERROR,
            }[log_level])

    async def handle_manual_reserve(self):
        for admin in self.admin_ids:
            await self.__start_manual_reserve(user_id = admin)

    async def __start_manual_reserve(self, context=None, user_id=None):
        if not context:
            if not self.token: return
            user_context = ApplicationBuilder().token(self.token).build()
        else:
            user_context = context
        users = [self.db.get_user_reserve_info(user_id)] if user_id else []
        logging.debug("users are {}".format(users))
        logging.info("ManualReserve :: start")
        for user in users:
            await self.__send_reserve_table(user, user_context)

    async def __send_reserve_table(self, user, context):
        try:
            dining = Dining(user["student_number"], user["password"])
        except Exception as e:
            return
        logging.info("ManualReserve :: sending reserve table for {}".format(user["user_id"]))
        for food_court_id in user["food_courts"]:
            food_table = dining.get_reserve_table_foods(food_court_id)
            await context.bot.send_message(
                chat_id=user["user_id"],
                text=messages.manual_reserve_food_table_message,
                reply_markup=ManualReserveKeyboardHandler.create_food_list_keyboard(
                    food_table=food_table,
                )
            )


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
