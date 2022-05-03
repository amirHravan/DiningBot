start_message = "🍕 غذا می‌قولی؟!"

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