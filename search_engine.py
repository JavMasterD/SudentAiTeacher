import json
import os
import sys

def resource_path(relative_path):
    """ للحصول على المسار الصحيح داخل EXE """
    try:
        # عند التشغيل من ملف exe
        base_path = sys._MEIPASS
    except AttributeError:
        # عند التشغيل العادي من Python
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_book(path="book_data_ar.json"):
    full_path = resource_path(path)
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)
