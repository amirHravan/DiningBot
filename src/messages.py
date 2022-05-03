start_message = "🍕 غذا می‌قولی؟!"

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

choose_food_priorities_message = """
🍟🍺 به ترتیب علاقت، روی غذایی که می‌خوای کلیک کن. می‌تونی تو صفحه‌ی های دیگه هم دنبال غذاها بگردی
"""