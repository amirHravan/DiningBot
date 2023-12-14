from src.dining import Dining
import logging
from src import messages, static_data
from telegram.ext import ApplicationBuilder
from telegram.error import BadRequest
from src.inline_keyboards_handlers.manual_reserve_keyboard_handler import ManualReserveKeyboardHandler
from src.error_handlers.exceptions import EmptyReserveTableException

USER_DATA_SELECTED_FOODS_KEY = "manual_reserve_selected_foods"


class ManualReserveHandler:
    def __init__(self, token="TOKEN", admin_ids=set(), log_level='INFO', db=None, cache=None) -> None:
        self.db = db
        self.cache = cache
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
            await self.__start_manual_reserve(user_id=admin)

    async def __start_manual_reserve(self, context=None, user_id=None):
        if not context:
            if not self.token: return
            user_context = ApplicationBuilder().token(self.token).build()
        else:
            user_context = context
        users = [self.db.get_user_reserve_info(user_id)] if user_id else []
        logging.debug("users are {}".format(users))
        # user_context.user_data.clear()
        logging.info("ManualReserve :: start")
        for user in users:
            await self.__send_reserve_table(user, user_context)

    async def __send_reserve_table(self, user, context):
        try:
            dining = Dining(user["student_number"], user["password"])
        except Exception as e:
            return

        logging.info("ManualReserve :: sending reserve table for {}".format(user["user_id"]))
        for food_court_id in user['food_courts']:
            food_table = self.__process_reserve_table(dining.get_reserve_table_foods(food_court_id, True))
            logging.debug(food_table)
            self.db.set_food_court_reserve_table(food_court_id, food_table)
            await context.bot.send_message(
                chat_id=user['user_id'],
                text=messages.manual_reserve_food_table_message,
                reply_markup=ManualReserveKeyboardHandler.create_food_list_keyboard(
                    food_table=food_table,
                    selected_foods={},
                    food_court_id=food_court_id,
                    page=0,
                )
            )

    def __process_reserve_table(self, reserve_table: dict):
        result = {}
        reversed_reserve_table = dict(reversed(list(reserve_table.items())))
        for meal in static_data.MEAL_EN_TO_FA.keys():
            for key, value in reversed_reserve_table.items():
                if value.get(meal) and len(value.get(meal)):
                    if not result.get(meal):
                        result[meal] = {}
                    result[meal][key] = value[meal]
        return result


class ManualReserveInlineHandler:
    def __init__(self, db):
        self.db = db

    async def __update_reply_markup(self, context, query, food_court_id, page, food_table=None):
        if not food_table:
            food_table = self.db.get_food_court_reserve_table(food_court_id)['reserve_table']
        try:
            await context.bot.edit_message_reply_markup(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                reply_markup=ManualReserveKeyboardHandler.create_food_list_keyboard(
                    food_table=food_table,
                    food_court_id=food_court_id,
                    selected_foods=context.user_data.get(USER_DATA_SELECTED_FOODS_KEY),
                    page=page,
                )
            )
        except BadRequest as e:
            await context.bot.answer_callback_query(callback_query_id=query.id)
        except EmptyReserveTableException as e:
            await context.bot.answer_callback_query(callback_query_id=query.id)

    async def inline_manual_food_choose_handler(self, update, context, action: str, day, food_id, food_court_id, page):
        query = update.callback_query
        if action == "IGNORE":
            await context.bot.answer_callback_query(callback_query_id=query.id)
        if action == "PREV":
            await self.__update_reply_markup(context, query, food_court_id, page - 1)
        if action == 'NEXT':
            await self.__update_reply_markup(context, query, food_court_id, page + 1)
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
                food_table = self.db.get_food_court_reserve_table(food_court_id)['reserve_table']
                logging.debug(food_table)
                meal, _ = list(food_table.items())[page]
                for food in food_table[meal][day]:
                    if food['food_id'] == food_id:
                        if not context.user_data[USER_DATA_SELECTED_FOODS_KEY].get(meal):
                            context.user_data[USER_DATA_SELECTED_FOODS_KEY][meal] = {}
                        context.user_data[USER_DATA_SELECTED_FOODS_KEY][meal][day] = food_id
                await self.__update_reply_markup(context, query, food_court_id, page, food_table)
            else:
                await context.bot.answer_callback_query(callback_query_id=query.id)
