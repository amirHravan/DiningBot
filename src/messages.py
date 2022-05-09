start_message = "🍕 غذا می‌قولی؟!"

main_menu_message = "از منویی که این پایین هست انتخاب کن که چی می‌خوای"
forget_code_menu_message = "منوی کد فراموشی" # TODO
reserve_menu_messsage = "منوی رزرو" # TODO

details_message = """
توضیحات مربوط به انتخاب اولویت‌ها:
"""

help_message = """
/set <student_number> <password> :‌ تنظیم شماره‌ی دانشجویی و رمز عبور داینینگ
/help: مشاهده‌ی راهنما
"""

admin_help_message = """
دستورات کاربران:
{}

دستورات ادمین (این بخش به کاربران عادی نمایش داده نمی‌شود)
/update_foods: به‌روزرسانی غذاها
""".format(help_message)

set_wrong_args_message = """اشتباه زدی. بعد از /set دو تا مقدار باید بذاری، اولی شماره‌دانشجویی، دومی رمز عبور.

این شکلی:
/set 97102111 thisismypassword1234"""

set_result_message = """
✅ اطلاعاتی که بهم دادی: 

👤 شماره دانشجویی: {}
🔑 رمز عبور: {}

اگه اشتباه زدی، دوباره بزن.
"""

update_food_list_result = """
🍟 {} غذای جدید پیدا شد!
"""

next_page_button_message = "< صفحه‌ی بعد"
previous_page_button_message = "صفحه‌ی قبل >"
done_button_message = "حله"
cancel_button_message = "لغو"

choose_food_priorities_message = """
به ترتیب علاقت، روی غذایی که می‌خوای کلیک کن. می‌تونی تو صفحه‌ی های دیگه هم دنبال غذاها بگردی 🍟
هر وقت انتخابت تموم شد، روی «حله» کلیک کن تا لیست غذاهات ثبت بشه و هر وقت منصرف شدی، روی «لغو» کلیک کن تا تغییراتت کنسل بشن 🍗
"""
choosing_food_priorities_done_message = """
غذاهای مورد علاقت به ترتیبی که گفتی (تو پیامای این زیر این پیام هم می‌تونی ببینیشون) انتخاب شد. 🍻
اگه دوباره /my_foods رو بزنی، می‌تونی از اول اولویت غذاهات رو مشخص کنی.
"""
choosing_food_priorities_cancel_message = """
لغو شد.
"""

choose_self_message_to_get = "کدوم سلف می‌خوای غذا بخوری؟"
choose_self_message_to_give = """دمت خیلی گرمه :))
کد فراموشیت برای کدوم سلفه؟"""

get_forget_code_from_user_message = "حالا لطفا کد فراموشیت رو برام بفرست"

not_int_code_error_message = "این چیه دیگه؟ کد بده بهم، کد فراموشی کلش باید عدد باشه"
not_enough_number_error_message = """کد فراموشی زمان ما ۷ رقمی بود، الان عوض شده؟ :))
یه چک بکن ببین کجاشو اشتباه زدی، دوباره بفرست"""
food_court_not_choosed_error_message = "سلف رو هنوز انتخاب نکردی که، انتخاب کن"
forget_code_added_message = "خیلی هم عالی، کد فراموشیت سیو شد. یه گشنه‌ای رو سیر می‌کنی :)"

no_code_for_this_food_court_message = "متاسفم، ولی کسی کد فراموشی واسه این سلف نذاشته :("
forget_code_founded_message = """یه کد برات پیدا کردم! :)
برو بزن به بدن، عشق کن. اینم کد:
{}
"""