import threading

from src.dining import Dining
import logging
from src import messages, static_data
from telegram.ext import ApplicationBuilder
from telegram.error import BadRequest
from src.inline_keyboards_handlers.manual_reserve_keyboard_handler import ManualReserveKeyboardHandler
from src.error_handlers.exceptions import EmptyReserveTableException, AlreadyReserved, NotEnoughCreditToReserve, \
    NoSuchFoodSchedule

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

    async def handle_manual_reserve(self, update, context):
        await self.start_manual_reserve(context, update.effective_chat.id)
        return static_data.RESERVE_MENU_CHOOSING

    async def start_manual_reserve(self, context=None, user_id=None):
        if not context:
            if not self.token: return
            user_context = ApplicationBuilder().token(self.token).build()
        else:
            user_context = context
        # Todo implement if user_id == None
        users = [self.db.get_user_reserve_info(user_id)] if user_id else []
        # user_context.user_data.clear()
        logging.info("ManualReserve :: start sending tables")
        for user in users:
            await self.__send_reserve_table(user, user_context)

    async def __send_reserve_table(self, user, context):
        dining = Dining(user["student_number"], user["password"])
        logging.info("ManualReserve :: sending reserve table for {}".format(user["user_id"]))
        for food_court_id in user['food_courts']:
            food_table = dining.get_reserve_table_foods(food_court_id)
            self.db.set_food_court_reserve_table(food_court_id, food_table)
            message = await context.bot.send_message(
                chat_id=user['user_id'],
                text=messages.manual_reserve_food_table_message,
                reply_markup=ManualReserveKeyboardHandler.create_food_list_keyboard(
                    food_table=food_table,
                    selected_foods={},
                    food_court_id=food_court_id,
                    page=0,
                )
            )
            self.db.add_garbage_message(message.message_id, message.chat.id)

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
            # await context.bot.edit_message_text(
            #     text=messages.manual_reserve_select_food_done,
            #     chat_id=query.message.chat_id,
            #     message_id=query.message.message_id
            # )
            target_user_id = query.from_user.id
            try:
                await self.__reserve_food(
                    food_court_id,
                    self.db.get_user_login_info(target_user_id),
                    context.user_data.get(USER_DATA_SELECTED_FOODS_KEY, {})
                )
            except AlreadyReserved as e:
                logging.debug(e.message)
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=messages.already_reserved_message.format(
                        static_data.PLACES_NAME_BY_ID[food_court_id]
                    )
                )
                # If user has already reserved his food, we should set his next_week_reserve status to True
                threading.Thread(target=self.db.set_user_next_week_reserve_status, args=(target_user_id, True)).start()
            except NotEnoughCreditToReserve as e:
                logging.debug(e.message)
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=messages.not_enough_credit_to_reserve_message.format(
                        static_data.PLACES_NAME_BY_ID[food_court_id]
                    )
                )
            except NoSuchFoodSchedule as e:
                logging.error("Error on reserving food for user {} with message {}".format(target_user_id, e.message))
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=messages.reserve_was_failed_message.format(static_data.PLACES_NAME_BY_ID[food_court_id]))
        elif action == "CANCEL":
            if context.user_data: context.user_data.clear()
            await context.bot.delete_message(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id
            )
        elif action == "SELECT":
            if food_id != "-":
                context.user_data[USER_DATA_SELECTED_FOODS_KEY] = context.user_data.get(USER_DATA_SELECTED_FOODS_KEY, {})
                food_table = self.db.get_food_court_reserve_table(food_court_id)['reserve_table']
                meal = 'lunch'
                for food in food_table[day][meal]:
                    if food['food_id'] == food_id:
                        context.user_data[USER_DATA_SELECTED_FOODS_KEY][meal] = context.user_data[USER_DATA_SELECTED_FOODS_KEY].get(meal, {})
                        if context.user_data[USER_DATA_SELECTED_FOODS_KEY][meal].get(day) == food_id:
                            context.user_data[USER_DATA_SELECTED_FOODS_KEY][meal][day] = None
                        else:
                            context.user_data[USER_DATA_SELECTED_FOODS_KEY][meal][day] = food_id
                await self.__update_reply_markup(context, query, food_court_id, page, food_table)
            else:
                await context.bot.answer_callback_query(callback_query_id=query.id)

    async def __reserve_food(self, food_court_id: int, login_info: dict, selected_food_map: dict):
        dining = Dining(login_info['student_number'], login_info['password'])
        logging.debug("reserve food debug: {}, {}, {}".format(food_court_id, login_info, selected_food_map))
        foods = dining.get_reserve_table_foods(food_court_id)
        selected_food_indices = {}
        food_names = []
        for day in foods:
            selected_food_indices[day] = selected_food_indices.get(day, {})
            for meal in dining.meals:
                selected_food_indices[day][meal] = selected_food_indices[day].get(meal, {})
                day_food_ids = list(map(lambda food: food['food_id'], foods[day][meal]))
                if not day_food_ids: continue
                if selected_food_map.get(meal).get(day) is not None:
                    selected_food_indices[day][meal] = day_food_ids.index(selected_food_map[meal][day])
                    food_names.append(
                        (foods[day][meal][day_food_ids.index(selected_food_map[meal][day])].get('food'), day, meal))
        return dining.reserve_food(int(food_court_id), foods, selected_food_indices)