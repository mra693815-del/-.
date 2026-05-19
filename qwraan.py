import os
import json
import random
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'hbbas_quran_2025'

# ============================================
# ملفات التخزين
# ============================================
USERS_FILE = 'users.json'
EXAMS_FILE = 'exams.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"admin": "123456", "teacher": "quran2024"}

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def load_exams():
    if os.path.exists(EXAMS_FILE):
        with open(EXAMS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_exams(exams):
    with open(EXAMS_FILE, 'w', encoding='utf-8') as f:
        json.dump(exams, f, ensure_ascii=False, indent=2)

USERS = load_users()

# ============================================
# بيانات السور والأجزاء (حسب التقسيم الصحيح)
# ============================================

# الجزء 30: من النبأ إلى الناس (37 سورة كاملة)
PART_30 = [
    ("النبأ", 1, 40), ("النازعات", 1, 46), ("عبس", 1, 42), ("التكوير", 1, 29),
    ("الانفطار", 1, 19), ("المطففين", 1, 36), ("الانشقاق", 1, 25), ("البروج", 1, 22),
    ("الطارق", 1, 17), ("الأعلى", 1, 19), ("الغاشية", 1, 26), ("الفجر", 1, 30),
    ("البلد", 1, 20), ("الشمس", 1, 15), ("الليل", 1, 21), ("الضحى", 1, 11),
    ("الشرح", 1, 8), ("التين", 1, 8), ("العلق", 1, 19), ("القدر", 1, 5),
    ("البينة", 1, 8), ("الزلزلة", 1, 8), ("العاديات", 1, 11), ("القارعة", 1, 11),
    ("التكاثر", 1, 8), ("العصر", 1, 3), ("الهمزة", 1, 9), ("الفيل", 1, 5),
    ("قريش", 1, 4), ("الماعون", 1, 7), ("الكوثر", 1, 3), ("الكافرون", 1, 6),
    ("النصر", 1, 3), ("المسد", 1, 5), ("الإخلاص", 1, 4), ("الفلق", 1, 5),
    ("الناس", 1, 6)
]

# الجزء 29: من الملك إلى المرسلات (11 سورة)
PART_29 = [
    ("الملك", 1, 30), ("القلم", 1, 52), ("الحاقة", 1, 52), ("المعارج", 1, 44),
    ("نوح", 1, 28), ("الجن", 1, 28), ("المزمل", 1, 20), ("المدثر", 1, 56),
    ("القيامة", 1, 40), ("الإنسان", 1, 31), ("المرسلات", 1, 50)
]

# الجزء 28: من المجادلة إلى التحريم (9 سور)
PART_28 = [
    ("المجادلة", 1, 22), ("الحشر", 1, 24), ("الممتحنة", 1, 13), ("الصف", 1, 14),
    ("الجمعة", 1, 11), ("المنافقون", 1, 11), ("التغابن", 1, 18), ("الطلاق", 1, 12),
    ("التحريم", 1, 12)
]

# الجزء 27: الذاريات إلى الحديد (7 سور)
PART_27 = [
    ("الذاريات", 1, 60), ("الطور", 1, 49), ("النجم", 1, 62), ("القمر", 1, 55),
    ("الرحمن", 1, 78), ("الواقعة", 1, 96), ("الحديد", 1, 29)
]

# الجزء 26: الأحقاف إلى ق (5 سور)
PART_26 = [
    ("الأحقاف", 1, 35), ("محمد", 1, 38), ("الفتح", 1, 29), ("الحجرات", 1, 18),
    ("ق", 1, 45)
]

# الجزء 25: الجاثية إلى الشورى (4 سور)
PART_25 = [
    ("الجاثية", 1, 37), ("الدخان", 1, 59), ("الزخرف", 1, 89), ("الشورى", 1, 53)
]

# الجزء 24: غافر إلى فصلت (2 سورة) + الزمر (باقي)
PART_24 = [
    ("غافر", 1, 85), ("فصلت", 1, 54), ("الزمر", 1, 75)
]

# الجزء 23: يس (باقي) إلى الصافات إلى ص إلى الزمر (أول)
PART_23 = [
    ("يس", 1, 83), ("الصافات", 1, 182), ("ص", 1, 88), ("الزمر", 1, 75)
]

# الجزء 22: الأحزاب (باقي) إلى سبأ إلى فاطر إلى يس (أول)
PART_22 = [
    ("الأحزاب", 1, 73), ("سبأ", 1, 54), ("فاطر", 1, 45), ("يس", 1, 83)
]

# الجزء 21: العنكبوت (باقي) إلى الروم إلى لقمان إلى السجدة إلى الأحزاب (أول)
PART_21 = [
    ("العنكبوت", 1, 69), ("الروم", 1, 60), ("لقمان", 1, 34), ("السجدة", 1, 30),
    ("الأحزاب", 1, 73)
]

# الجزء 20: النمل (باقي) إلى القصص إلى العنكبوت (أول)
PART_20 = [
    ("النمل", 1, 93), ("القصص", 1, 88), ("العنكبوت", 1, 69)
]

# الجزء 19: الشعراء إلى النمل (أول) إلى الفرقان (باقي)
PART_19 = [
    ("الشعراء", 1, 227), ("النمل", 1, 93), ("الفرقان", 1, 77)
]

# الجزء 18: المؤمنون إلى النور إلى الفرقان (أول)
PART_18 = [
    ("المؤمنون", 1, 118), ("النور", 1, 64), ("الفرقان", 1, 77)
]

# الجزء 17: الأنبياء إلى الحج (2 سورة)
PART_17 = [
    ("الأنبياء", 1, 112), ("الحج", 1, 78)
]

# الجزء 16: الكهف (باقي) إلى مريم إلى طه
PART_16 = [
    ("الكهف", 1, 110), ("مريم", 1, 98), ("طه", 1, 135)
]

# الجزء 15: الإسراء إلى الكهف (أول)
PART_15 = [
    ("الإسراء", 1, 111), ("الكهف", 1, 110)
]

# الجزء 14: الحجر إلى النحل (2 سورة)
PART_14 = [
    ("الحجر", 1, 99), ("النحل", 1, 128)
]

# الجزء 13: يوسف (باقي) إلى الرعد إلى إبراهيم
PART_13 = [
    ("يوسف", 1, 111), ("الرعد", 1, 43), ("إبراهيم", 1, 52)
]

# الجزء 12: هود (باقي) إلى يوسف (أول)
PART_12 = [
    ("هود", 1, 123), ("يوسف", 1, 111)
]

# الجزء 11: التوبة (باقي) إلى يونس إلى هود (أول)
PART_11 = [
    ("التوبة", 1, 129), ("يونس", 1, 109), ("هود", 1, 123)
]

# الجزء 10: الأنفال (باقي) إلى التوبة (أول)
PART_10 = [
    ("الأنفال", 1, 75), ("التوبة", 1, 129)
]

# الجزء 9: الأعراف (باقي) إلى الأنفال (أول)
PART_9 = [
    ("الأعراف", 1, 206), ("الأنفال", 1, 75)
]

# الجزء 8: الأنعام (باقي) إلى الأعراف (أول)
PART_8 = [
    ("الأنعام", 1, 165), ("الأعراف", 1, 206)
]

# الجزء 7: المائدة (باقي) إلى الأنعام (أول)
PART_7 = [
    ("المائدة", 1, 120), ("الأنعام", 1, 165)
]

# الجزء 6: النساء (باقي) إلى المائدة (أول)
PART_6 = [
    ("النساء", 1, 176), ("المائدة", 1, 120)
]

# الجزء 4 و 5: تابع سورة النساء
PART_4 = [("النساء", 1, 176)]
PART_5 = [("النساء", 1, 176)]

# الجزء 3: آل عمران (باقي) إلى البقرة (باقي)
PART_3 = [
    ("آل عمران", 1, 200), ("البقرة", 1, 286)
]

# الجزء 2: تابع سورة البقرة
PART_2 = [("البقرة", 142, 252)]

# الجزء 1: الفاتحة إلى البقرة (أول)
PART_1 = [
    ("الفاتحة", 1, 7), ("البقرة", 1, 141)
]

# تجميع كل الأجزاء في قاموس واحد
PARTS_DATA = {
    1: PART_1,
    2: PART_2,
    3: PART_3,
    4: PART_4,
    5: PART_5,
    6: PART_6,
    7: PART_7,
    8: PART_8,
    9: PART_9,
    10: PART_10,
    11: PART_11,
    12: PART_12,
    13: PART_13,
    14: PART_14,
    15: PART_15,
    16: PART_16,
    17: PART_17,
    18: PART_18,
    19: PART_19,
    20: PART_20,
    21: PART_21,
    22: PART_22,
    23: PART_23,
    24: PART_24,
    25: PART_25,
    26: PART_26,
    27: PART_27,
    28: PART_28,
    29: PART_29,
    30: PART_30
}

# صفحات تقريبية لكل سورة
PAGE_MAP = {
    "الفاتحة": 1, "البقرة": 2, "آل عمران": 50, "النساء": 80, "المائدة": 110,
    "الأنعام": 130, "الأعراف": 150, "الأنفال": 180, "التوبة": 190, "يونس": 210,
    "هود": 230, "يوسف": 250, "الرعد": 270, "إبراهيم": 280, "الحجر": 290,
    "النحل": 300, "الإسراء": 310, "الكهف": 320, "مريم": 330, "طه": 340,
    "الأنبياء": 350, "الحج": 360, "المؤمنون": 370, "النور": 380, "الفرقان": 390,
    "الشعراء": 400, "النمل": 410, "القصص": 420, "العنكبوت": 430, "الروم": 440,
    "لقمان": 450, "السجدة": 455, "الأحزاب": 460, "سبأ": 470, "فاطر": 480,
    "يس": 490, "الصافات": 500, "ص": 510, "الزمر": 520, "غافر": 530,
    "فصلت": 540, "الشورى": 550, "الزخرف": 560, "الدخان": 570, "الجاثية": 580,
    "الأحقاف": 585, "محمد": 590, "الفتح": 595, "الحجرات": 598, "ق": 600,
    "الذاريات": 602, "الطور": 603, "النجم": 604, "القمر": 605, "الرحمن": 606,
    "الواقعة": 607, "الحديد": 608, "المجادلة": 609, "الحشر": 610, "الممتحنة": 611,
    "الصف": 612, "الجمعة": 613, "المنافقون": 614, "التغابن": 615, "الطلاق": 616,
    "التحريم": 617, "الملك": 618, "القلم": 619, "الحاقة": 620, "المعارج": 621,
    "نوح": 622, "الجن": 623, "المزمل": 624, "المدثر": 625, "القيامة": 626,
    "الإنسان": 627, "المرسلات": 628, "النبأ": 629, "النازعات": 630, "عبس": 631,
    "التكوير": 632, "الانفطار": 633, "المطففين": 634, "الانشقاق": 635, "البروج": 636,
    "الطارق": 637, "الأعلى": 638, "الغاشية": 639, "الفجر": 640, "البلد": 641,
    "الشمس": 642, "الليل": 643, "الضحى": 644, "الشرح": 645, "التين": 646,
    "العلق": 647, "القدر": 648, "البينة": 649, "الزلزلة": 650, "العاديات": 651,
    "القارعة": 652, "التكاثر": 653, "العصر": 654, "الهمزة": 655, "الفيل": 656,
    "قريش": 657, "الماعون": 658, "الكوثر": 659, "الكافرون": 660, "النصر": 661,
    "المسد": 662, "الإخلاص": 663, "الفلق": 664, "الناس": 665
}

def get_page_for_verse(surah_name, verse_num):
    base_page = PAGE_MAP.get(surah_name, 600)
    return base_page + ((verse_num - 1) // 15)

def generate_all_verses_for_part(part_number):
    """توليد كل آيات الجزء"""
    if part_number not in PARTS_DATA:
        return []
    verses = []
    for surah_name, start_verse, end_verse in PARTS_DATA[part_number]:
        for verse in range(start_verse, end_verse + 1):
            page = get_page_for_verse(surah_name, verse)
            verses.append({
                "surah": surah_name,
                "verse": verse,
                "page": page,
                "part": part_number
            })
    return verses

def generate_random_questions_for_part(part_number, num_questions):
    all_verses = generate_all_verses_for_part(part_number)
    if len(all_verses) <= num_questions:
        return all_verses
    return random.sample(all_verses, num_questions)

def generate_full_questions(num_questions=30):
    all_verses = []
    for part in range(1, 31):
        all_verses.extend(generate_all_verses_for_part(part))
    if len(all_verses) <= num_questions:
        return all_verses
    return random.sample(all_verses, num_questions)

# ============================================
# باقي الكود (نفسه مع إزالة الإموجيات)
# ============================================

LOGIN_PAGE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>نور البيان - تسجيل الدخول</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI','Amiri',sans-serif}
        body{background:linear-gradient(135deg,#0a3b2a,#146b4e);min-height:100vh;display:flex;justify-content:center;align-items:center}
        .login-card{background:#fffef7;border-radius:60px;padding:40px;width:450px;text-align:center;box-shadow:0 25px 50px rgba(0,0,0,0.3)}
        h1{color:#2b6e3c;margin-bottom:10px}
        .logo{color:#c97e2a;border-bottom:2px solid #d4af37;width:fit-content;margin:0 auto 30px auto;padding:5px 20px}
        input{width:100%;padding:14px;margin:10px 0;border-radius:60px;border:1px solid #ddd;font-size:1rem}
        button{width:100%;padding:14px;background:#2b6e3c;color:#fff;border:none;border-radius:60px;font-size:1.1rem;font-weight:bold;cursor:pointer;margin-top:15px}
        .error{color:#c62828;margin-top:10px}
        .success{color:#2b6e3c;margin-top:10px}
        .register-link{margin-top:20px;color:#666}
        .register-link a{color:#2b6e3c;text-decoration:none;font-weight:bold}
    </style>
</head>
<body>
<div class="login-card">
    <h1>نور البيان</h1>
    <div class="logo">جمعية تحفيظ القرآن - الروضة هباس</div>
    {% if register_success %}
    <div class="success">تم إنشاء الحساب بنجاح يمكنك الآن تسجيل الدخول</div>
    {% endif %}
    <form method="POST" action="{{ url_for('login_post') }}">
        <input type="text" name="username" placeholder="اسم المستخدم" required>
        <input type="password" name="password" placeholder="كلمة المرور" required>
        <button type="submit">دخول</button>
    </form>
    <div class="register-link">ليس لديك حساب <a href="{{ url_for('register') }}">إنشاء حساب جديد</a></div>
    {% if error %}<div class="error">{{ error }}</div>{% endif %}
</div>
</body>
</html>
'''

REGISTER_PAGE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>نور البيان - إنشاء حساب</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI','Amiri',sans-serif}
        body{background:linear-gradient(135deg,#0a3b2a,#146b4e);min-height:100vh;display:flex;justify-content:center;align-items:center}
        .register-card{background:#fffef7;border-radius:60px;padding:40px;width:450px;text-align:center;box-shadow:0 25px 50px rgba(0,0,0,0.3)}
        h1{color:#2b6e3c;margin-bottom:10px}
        .logo{color:#c97e2a;border-bottom:2px solid #d4af37;width:fit-content;margin:0 auto 30px auto;padding:5px 20px}
        input{width:100%;padding:14px;margin:10px 0;border-radius:60px;border:1px solid #ddd;font-size:1rem}
        button{width:100%;padding:14px;background:#2b6e3c;color:#fff;border:none;border-radius:60px;font-size:1.1rem;font-weight:bold;cursor:pointer;margin-top:15px}
        .error{color:#c62828;margin-top:10px}
        .login-link{margin-top:20px;color:#666}
        .login-link a{color:#2b6e3c;text-decoration:none;font-weight:bold}
    </style>
</head>
<body>
<div class="register-card">
    <h1>نور البيان</h1>
    <div class="logo">إنشاء حساب جديد</div>
    <form method="POST">
        <input type="text" name="username" placeholder="اسم المستخدم" required>
        <input type="password" name="password" placeholder="كلمة المرور" required>
        <input type="password" name="confirm_password" placeholder="تأكيد كلمة المرور" required>
        <button type="submit">إنشاء حساب</button>
    </form>
    <div class="login-link">لديك حساب بالفعل <a href="{{ url_for('login') }}">تسجيل الدخول</a></div>
    {% if error %}<div class="error">{{ error }}</div>{% endif %}
</div>
</body>
</html>
'''

MAIN_APP_PAGE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نور البيان - لوحة التحكم</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI','Amiri',sans-serif}
        body{background:linear-gradient(135deg,#0a3b2a,#146b4e);min-height:100vh;padding:20px}
        .container{max-width:1400px;margin:0 auto}
        .header{background:#fffef7;border-radius:48px;padding:20px 30px;margin-bottom:25px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap}
        h1{color:#2b6e3c;font-size:1.8rem}
        .logo{color:#c97e2a;font-size:0.9rem}
        .user-info{display:flex;gap:15px;align-items:center}
        .logout-btn{background:#c62828;color:#fff;padding:8px 20px;border-radius:40px;text-decoration:none}
        .tabs{display:flex;gap:5px;margin-bottom:25px;flex-wrap:wrap}
        .tab{background:#e8e0c8;padding:12px 25px;border-radius:60px;cursor:pointer;font-weight:bold;transition:0.2s}
        .tab.active{background:#2b6e3c;color:#fff}
        .tab-content{display:none}
        .tab-content.active{display:block}
        .card{background:#fffef7;border-radius:48px;padding:30px;margin-bottom:25px;box-shadow:0 15px 30px rgba(0,0,0,0.15)}
        .card h2{color:#2b6e3c;margin-bottom:20px;border-right:4px solid #d4af37;padding-right:15px}
        button{padding:12px 25px;border:none;border-radius:60px;font-weight:bold;cursor:pointer;margin:5px;transition:0.2s}
        .btn-primary{background:#2b6e3c;color:#fff;box-shadow:0 3px 0 #1c4a28}
        .btn-primary:active{transform:translateY(2px)}
        .btn-secondary{background:#e6b422;color:#2d2d2d}
        .btn-danger{background:#c62828;color:#fff}
        .btn-outline{background:transparent;border:2px solid #2b6e3c;color:#2b6e3c}
        .btn-sm{padding:6px 12px;font-size:0.8rem}
        input,select{width:100%;padding:12px;margin:8px 0;border-radius:30px;border:1px solid #ddd;font-size:1rem}
        .flex-row{display:flex;gap:15px;flex-wrap:wrap;align-items:center}
        .students-list{background:#f0e8d0;border-radius:30px;padding:20px;margin:15px 0;max-height:300px;overflow-y:auto}
        .student-item{display:flex;justify-content:space-between;align-items:center;padding:12px;border-bottom:1px solid #ddd}
        .criteria-item{background:#e8f0e8;border-radius:30px;padding:15px;margin:10px 0}
        .quiz-question{background:#fef9e6;border-radius:35px;padding:25px;margin:20px 0;text-align:center}
        .page-badge{background:#2b6e3c;color:#fff;display:inline-block;padding:5px 15px;border-radius:50px;margin:10px 0}
        .error-input{width:80px;padding:8px;text-align:center;border-radius:30px;margin-right:10px}
        .leaderboard-table{width:100%;border-collapse:collapse;margin-top:20px}
        .leaderboard-table th,.leaderboard-table td{padding:12px;border-bottom:1px solid #ddd;text-align:center}
        .leaderboard-table th{background:#2b6e3c;color:#fff}
        .rank-1{background:#ffd70020}
        .rank-2{background:#c0c0c020}
        .rank-3{background:#cd7f3220}
        .hidden{display:none}
        .badge{background:#2b6e3c;color:#fff;padding:4px 12px;border-radius:50px;font-size:0.8rem}
        .exam-card{background:#f0e8d0;border-radius:30px;padding:20px;margin-bottom:15px}
        .exam-title{font-size:1.2rem;font-weight:bold;color:#2b6e3c;margin-bottom:10px}
        .exam-info{display:flex;gap:20px;flex-wrap:wrap;margin-bottom:15px;font-size:0.9rem;color:#666}
        .exam-actions{display:flex;gap:10px;flex-wrap:wrap}
        .pending-students{background:#e8f0e8;border-radius:30px;padding:15px;margin:15px 0}
        .student-select-item{padding:10px 20px;margin:5px;background:#fff;border-radius:30px;cursor:pointer;display:inline-block;border:1px solid #ddd}
        .student-select-item:hover{background:#2b6e3c;color:#fff}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div><h1>نور البيان</h1><div class="logo">جمعية تحفيظ القرآن الكريم - الروضة هباس</div></div>
        <div class="user-info"><span>مرحبا {{ username }}</span><a href="/logout" class="logout-btn">تسجيل خروج</a></div>
    </div>
    
    <div class="tabs">
        <div class="tab active" data-tab="exams">الاختبارات الحالية</div>
        <div class="tab" data-tab="create">إنشاء اختبار جديد</div>
        <div class="tab" data-tab="results">نتائج سابقة</div>
    </div>
    
    <div id="tab-exams" class="tab-content active"><div class="card"><h2>الاختبارات المتاحة</h2><div id="exams-list"></div></div></div>
    
    <div id="tab-create" class="tab-content">
        <div class="card">
            <h2>إنشاء اختبار جديد</h2>
            <div class="flex-row"><div style="flex:1"><label>اسم الاختبار</label><input type="text" id="exam-name" placeholder="مثال: اختبار رمضان 1446"></div></div>
            <div class="flex-row">
                <div style="flex:1"><label>نوع الاختبار</label><select id="exam-type"><option value="part">جزء محدد</option><option value="full">القرآن كامل</option></select></div>
                <div style="flex:1" id="part-select-container"><label>اختر الجزء</label><select id="part-select"><option value="">-- اختر الجزء --</option>{% for i in range(1, 31) %}<option value="{{ i }}">الجزء {{ i }}</option>{% endfor %}</select></div>
            </div>
            <div class="flex-row"><div style="flex:1"><label>عدد الأسئلة</label><input type="number" id="num-questions" value="10" min="1" max="50"></div><div style="flex:1"><label>كم ينقص الخطأ الواحد (نسبة مئوية)</label><input type="number" id="error-deduction" value="2" step="0.5" min="0" max="100"></div></div>
            <div><label>المعايير الإضافية (تلاوة، تجويد، ترتيل، إلخ)</label><div id="criteria-container"></div><button type="button" class="btn-outline btn-sm" id="add-criteria-btn" style="margin-top:10px">+ إضافة معيار جديد</button></div>
            <div><label>الطلاب المتسابقون</label><div id="students-container" class="students-list"></div><div class="flex-row"><input type="text" id="new-student-name" placeholder="اسم الطالب الجديد" style="flex:2"><button id="add-student-btn" class="btn-secondary btn-sm">+ إضافة طالب</button></div></div>
            <div class="flex-row" style="justify-content:space-between"><button id="create-exam-btn" class="btn-primary">إنشاء الاختبار</button></div>
        </div>
    </div>
    
    <div id="tab-results" class="tab-content"><div class="card"><h2>نتائج الاختبارات السابقة</h2><div id="old-exams-list"></div></div></div>
    
    <div id="edit-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1000; justify-content:center; align-items:center">
        <div style="background:#fffef7; border-radius:48px; padding:30px; max-width:600px; width:90%; max-height:80vh; overflow-y:auto"><h2>تعديل الاختبار</h2><div id="edit-content"></div><div class="flex-row" style="justify-content:space-between; margin-top:20px"><button id="close-edit-btn" class="btn-secondary">إلغاء</button><button id="save-edit-btn" class="btn-primary">حفظ التعديلات</button></div></div>
    </div>
    
    <div id="student-select-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1000; justify-content:center; align-items:center">
        <div style="background:#fffef7; border-radius:48px; padding:30px; max-width:500px; width:90%"><div id="student-select-content"></div></div>
    </div>
    
    <div id="quiz-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1000; justify-content:center; align-items:center">
        <div style="background:#fffef7; border-radius:48px; padding:30px; max-width:700px; width:90%; max-height:85vh; overflow-y:auto"><div id="quiz-content"></div></div>
    </div>
    
    <div id="results-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1000; justify-content:center; align-items:center">
        <div style="background:#fffef7; border-radius:48px; padding:30px; max-width:800px; width:90%; max-height:85vh; overflow-y:auto"><div id="results-content"></div></div>
    </div>
</div>

<script>
    let currentExamId = null;
    let currentExamConfig = null;
    let currentQuestions = [];
    let currentStudent = null;
    let currentQuestionIndex = 0;
    let studentErrors = [];
    let currentCriteriaScores = {};
    let pendingStudents = [];
    
    function loadExams() {
        fetch('/api/exams').then(r=>r.json()).then(data=>{renderExamsList(data);renderOldExamsList(data);});
    }
    function renderExamsList(exams) {
        const container = document.getElementById('exams-list');
        if(Object.keys(exams).length===0){container.innerHTML='<div style="text-align:center;padding:40px">لا توجد اختبارات حالية</div>';return;}
        let html='';
        for(let id in exams){
            const exam=exams[id];
            const completedCount=exam.results?exam.results.filter(r=>r.finalPercent!==null).length:0;
            const totalStudents=exam.students?exam.students.length:0;
            html+=`<div class="exam-card"><div class="exam-title">${exam.name}</div><div class="exam-info"><span>نوع: ${exam.type==='part'?'جزء '+exam.part:'القرآن كامل'}</span><span>الطلاب: ${completedCount}/${totalStudents}</span><span>تاريخ: ${exam.date}</span></div><div class="exam-actions"><button class="btn-primary btn-sm" onclick="startExam('${id}')">بدء الاختبار</button><button class="btn-secondary btn-sm" onclick="editExam('${id}')">تعديل</button><button class="btn-danger btn-sm" onclick="deleteExam('${id}')">حذف</button><button class="btn-outline btn-sm" onclick="viewExamResults('${id}')">عرض النتائج</button></div></div>`;
        }
        container.innerHTML=html;
    }
    function renderOldExamsList(exams){
        const container=document.getElementById('old-exams-list');
        if(Object.keys(exams).length===0){container.innerHTML='<div style="text-align:center;padding:40px">لا توجد اختبارات سابقة</div>';return;}
        let html='';
        for(let id in exams){
            const exam=exams[id];
            html+=`<div class="exam-card"><div class="exam-title">${exam.name}</div><div class="exam-info"><span>نوع: ${exam.type==='part'?'جزء '+exam.part:'القرآن كامل'}</span><span>التاريخ: ${exam.date}</span></div><div class="exam-actions"><button class="btn-outline btn-sm" onclick="viewExamResults('${id}')">عرض النتائج</button></div></div>`;
        }
        container.innerHTML=html;
    }
    
    window.editExam=function(examId){
        fetch(`/api/exam/${examId}`).then(r=>r.json()).then(exam=>{
            document.getElementById('edit-content').innerHTML=`
                <label>اسم الاختبار</label><input type="text" id="edit-exam-name" value="${exam.name}">
                <label>نوع الاختبار</label><select id="edit-exam-type"><option value="part" ${exam.type==='part'?'selected':''}>جزء محدد</option><option value="full" ${exam.type==='full'?'selected':''}>القرآن كامل</option></select>
                <div id="edit-part-container" style="${exam.type==='part'?'':'display:none'}"><label>الجزء</label><select id="edit-part-select">${[...Array(30)].map((_,i)=>`<option value="${i+1}" ${exam.part==i+1?'selected':''}>الجزء ${i+1}</option>`).join('')}</select></div>
                <label>عدد الأسئلة</label><input type="number" id="edit-num-questions" value="${exam.numQuestions}">
                <label>نسبة الخطأ الواحد</label><input type="number" id="edit-error-deduction" value="${exam.errorDeduction}" step="0.5">
                <label>الطلاب</label><div id="edit-students-list"></div>
                <div class="flex-row"><input type="text" id="edit-new-student" placeholder="اسم طالب جديد" style="flex:2"><button class="btn-secondary btn-sm" onclick="addEditStudent()">+ إضافة</button></div>
            `;
            const studentsContainer=document.getElementById('edit-students-list');
            exam.students.forEach((s,idx)=>{const div=document.createElement('div');div.className='student-item';div.innerHTML=`<span>${s}</span><button class="btn-danger btn-sm" onclick="this.parentElement.remove(); removeEditStudent(${idx})">حذف</button>`;studentsContainer.appendChild(div);});
            window.editExamData={students:[...exam.students],examId:examId};
            window.addEditStudent=function(){const name=document.getElementById('edit-new-student').value.trim();if(name){const div=document.createElement('div');div.className='student-item';div.innerHTML=`<span>${name}</span><button class="btn-danger btn-sm" onclick="this.parentElement.remove()">حذف</button>`;studentsContainer.appendChild(div);window.editExamData.students.push(name);document.getElementById('edit-new-student').value='';}};
            window.removeEditStudent=function(idx){window.editExamData.students.splice(idx,1);};
            document.getElementById('edit-exam-type').onchange=function(){document.getElementById('edit-part-container').style.display=this.value==='part'?'block':'none';};
            document.getElementById('edit-modal').style.display='flex';
            document.getElementById('save-edit-btn').onclick=()=>{
                const updatedExam={name:document.getElementById('edit-exam-name').value,type:document.getElementById('edit-exam-type').value,part:document.getElementById('edit-part-select')?.value,numQuestions:parseInt(document.getElementById('edit-num-questions').value),errorDeduction:parseFloat(document.getElementById('edit-error-deduction').value),students:window.editExamData.students};
                fetch(`/api/exam/${examId}`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(updatedExam)}).then(()=>{document.getElementById('edit-modal').style.display='none';loadExams();});
            };
        });
    };
    
    window.deleteExam=function(examId){if(confirm('هل أنت متأكد من حذف هذا الاختبار؟')){fetch(`/api/exam/${examId}`,{method:'DELETE'}).then(()=>loadExams());}};
    
    window.viewExamResults=function(examId){
        fetch(`/api/exam/${examId}`).then(r=>r.json()).then(exam=>{
            if(!exam.results||exam.results.length===0){alert('لا توجد نتائج لهذا الاختبار');return;}
            const sorted=[...exam.results].sort((a,b)=>b.finalPercent-a.finalPercent);
            let html=`<h2>نتائج ${exam.name}</h2><table class="leaderboard-table"><thead><tr><th>#</th><th>الاسم</th><th>النسبة</th><th>الأخطاء</th></tr></thead><tbody>`;
            sorted.forEach((r,idx)=>{html+=`<tr><td>${idx+1}</td><td>${r.name}</td><td><strong>${r.finalPercent.toFixed(1)}%</strong></td><td>${r.totalErrors}</td></tr>`;});
            html+=`</tbody></table><button id="close-results" class="btn-primary" style="margin-top:20px">إغلاق</button>`;
            document.getElementById('results-content').innerHTML=html;
            document.getElementById('results-modal').style.display='flex';
            document.getElementById('close-results').onclick=()=>document.getElementById('results-modal').style.display='none';
        });
    };
    
    let studentsList=[];
    let criteriaList=[];
    
    function renderStudentsList(){
        const container=document.getElementById('students-container');
        container.innerHTML='';
        studentsList.forEach((student,idx)=>{const div=document.createElement('div');div.className='student-item';div.innerHTML=`<span>${student}</span><button class="btn-danger btn-sm" onclick="removeStudent(${idx})">حذف</button>`;container.appendChild(div);});
    }
    window.removeStudent=function(idx){studentsList.splice(idx,1);renderStudentsList();};
    document.getElementById('add-student-btn').onclick=()=>{const name=document.getElementById('new-student-name').value.trim();if(name){studentsList.push(name);renderStudentsList();document.getElementById('new-student-name').value='';}else{alert('أدخل اسم الطالب');}};
    document.getElementById('add-criteria-btn').onclick=()=>{const container=document.getElementById('criteria-container');const idx=criteriaList.length;criteriaList.push({name:''});const div=document.createElement('div');div.className='criteria-item';div.innerHTML=`<div class="flex-row"><input type="text" placeholder="اسم المعيار" style="flex:2" data-criteria-name="${idx}"><button class="btn-danger btn-sm" onclick="this.parentElement.parentElement.remove(); criteriaList.splice(${idx},1)">حذف</button></div>`;container.appendChild(div);div.querySelector('[data-criteria-name]').onchange=(e)=>criteriaList[idx].name=e.target.value;};
    document.getElementById('exam-type').onchange=()=>{const type=document.getElementById('exam-type').value;document.getElementById('part-select-container').style.display=type==='part'?'block':'none';};document.getElementById('exam-type').onchange();
    document.getElementById('create-exam-btn').onclick=()=>{
        const examName=document.getElementById('exam-name').value||'اختبار جديد';
        const examType=document.getElementById('exam-type').value;
        const errorDeduction=parseFloat(document.getElementById('error-deduction').value);
        const numQuestions=parseInt(document.getElementById('num-questions').value);
        if(studentsList.length===0){alert('أضف طالباً واحداً على الأقل');return;}
        const criteria=criteriaList.filter(c=>c.name);
        let examData={name:examName,type:examType,errorDeduction:errorDeduction,numQuestions:numQuestions,students:studentsList,criteria:criteria};
        if(examType==='part'){const partNum=parseInt(document.getElementById('part-select').value);if(!partNum){alert('اختر الجزء');return;}examData.part=partNum;}
        fetch('/api/exams',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(examData)}).then(()=>{studentsList=[];criteriaList=[];renderStudentsList();document.getElementById('criteria-container').innerHTML='';document.getElementById('exam-name').value='';document.getElementById('num-questions').value='10';document.getElementById('error-deduction').value='2';loadExams();document.querySelector('.tab[data-tab="exams"]').click();});
    };
    
    window.startExam=function(examId){
        fetch(`/api/exam/${examId}`).then(r=>r.json()).then(exam=>{
            currentExamId=examId;
            currentExamConfig=exam;
            let url=exam.type==='part'?`/api/questions/part/${exam.part}?num=${exam.numQuestions}`:`/api/questions/full?num=${exam.numQuestions}`;
            fetch(url).then(r=>r.json()).then(questions=>{
                currentQuestions=questions;
                const completedNames=(exam.results||[]).map(r=>r.name);
                pendingStudents=exam.students.filter(s=>!completedNames.includes(s));
                if(pendingStudents.length===0){alert('جميع الطلاب قد اختبروا بالفعل');return;}
                let html=`<h2>اختر الطالب</h2><div style="text-align:center; margin:20px 0">`;
                for(let student of pendingStudents){html+=`<div style="display:inline-block; margin:8px; padding:12px 25px; background:#fff; border:1px solid #2b6e3c; border-radius:60px; cursor:pointer" onclick="selectStudent('${student}')">${student}</div>`;}
                html+=`</div><button id="close-student-select" class="btn-secondary" style="width:100%">إلغاء</button>`;
                document.getElementById('student-select-content').innerHTML=html;
                document.getElementById('student-select-modal').style.display='flex';
                document.getElementById('close-student-select').onclick=()=>document.getElementById('student-select-modal').style.display='none';
            });
        });
    };
    
    window.selectStudent=function(studentName){
        document.getElementById('student-select-modal').style.display='none';
        currentStudent=studentName;
        currentQuestionIndex=0;
        studentErrors=new Array(currentQuestions.length).fill(0);
        currentCriteriaScores={};
        for(let c of currentExamConfig.criteria||[]){currentCriteriaScores[c.name]=100;}
        renderQuizQuestion();
    };
    
    function renderQuizQuestion(){
        const q=currentQuestions[currentQuestionIndex];
        let html=`<h2>اختبار: ${currentExamConfig.name}</h2><div style="background:#e9e0c8; padding:15px; border-radius:60px; margin-bottom:20px"><span>الطالب: <strong>${currentStudent}</strong></span><span style="float:left">الأخطاء: <strong id="total-errors">${studentErrors.reduce((a,b)=>a+b,0)}</strong></span></div><div class="quiz-question"><div class="page-badge">الصفحة ${q.page}</div><div style="font-size:1.5rem; margin:20px 0">سورة ${q.surah}<br>الآية ${q.verse}</div></div><div class="flex-row"><label>عدد الأخطاء في هذا السؤال:</label><input type="number" id="question-errors" class="error-input" value="${studentErrors[currentQuestionIndex]}" min="0" max="10"></div><div class="flex-row" style="justify-content:space-between; margin-top:20px"><button id="prev-question" class="btn-secondary">السابق</button><span>السؤال ${currentQuestionIndex+1} من ${currentQuestions.length}</span><button id="next-question" class="btn-primary">التالي</button></div><button id="finish-student" class="btn-primary" style="width:100%; margin-top:20px">إنهاء اختبار هذا الطالب</button>`;
        document.getElementById('quiz-content').innerHTML=html;
        document.getElementById('question-errors').onchange=()=>{studentErrors[currentQuestionIndex]=parseInt(document.getElementById('question-errors').value)||0;document.getElementById('total-errors').innerText=studentErrors.reduce((a,b)=>a+b,0);};
        document.getElementById('prev-question').onclick=()=>{if(currentQuestionIndex>0){currentQuestionIndex--;renderQuizQuestion();}};
        document.getElementById('next-question').onclick=()=>{if(currentQuestionIndex+1<currentQuestions.length){currentQuestionIndex++;renderQuizQuestion();}};
        document.getElementById('finish-student').onclick=()=>{showCriteriaInput();};
        document.getElementById('quiz-modal').style.display='flex';
    }
    
    function showCriteriaInput(){
        const totalErrors=studentErrors.reduce((a,b)=>a+b,0);
        const errorPercent=totalErrors*currentExamConfig.errorDeduction;
        const baseScore=Math.max(0,100-errorPercent);
        let html=`<h2>نتيجة ${currentStudent}</h2><div style="background:#eef3e9; border-radius:35px; padding:20px; margin:15px 0"><p>إجمالي الأخطاء: ${totalErrors}</p><p>نسبة الأخطاء: ${errorPercent}% (ينقص كل خطأ ${currentExamConfig.errorDeduction}%)</p><p>الدرجة الأساسية: ${baseScore.toFixed(1)}%</p></div><div style="background:#fff5e0; border-radius:35px; padding:20px; margin:15px 0"><h3>المعايير الإضافية</h3>`;
        for(let c of currentExamConfig.criteria||[]){html+=`<div class="flex-row" style="margin:10px 0"><span style="width:150px">${c.name}:</span><input type="number" id="criteria-${c.name}" class="error-input" value="${currentCriteriaScores[c.name]}" min="0" max="100" step="0.5"><span>%</span></div>`;}
        html+=`</div><button id="save-criteria" class="btn-primary" style="width:100%">حفظ وحساب النسبة النهائية</button>`;
        document.getElementById('quiz-content').innerHTML=html;
        for(let c of currentExamConfig.criteria||[]){document.getElementById(`criteria-${c.name}`).onchange=(e)=>{currentCriteriaScores[c.name]=parseFloat(e.target.value)||0;};}
        document.getElementById('save-criteria').onclick=()=>{
            let criteriaSum=0;
            for(let c of currentExamConfig.criteria||[]){criteriaSum+=currentCriteriaScores[c.name];}
            const criteriaAvg=currentExamConfig.criteria.length?criteriaSum/currentExamConfig.criteria.length:100;
            const finalPercent=(baseScore+criteriaAvg)/2;
            fetch(`/api/exam/${currentExamId}/result`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:currentStudent,totalErrors:totalErrors,finalPercent:finalPercent,date:new Date().toLocaleDateString('ar-EG')})}).then(()=>{
                document.getElementById('quiz-modal').style.display='none';
                fetch(`/api/exam/${currentExamId}`).then(r=>r.json()).then(exam=>{
                    const completedCount=(exam.results||[]).length;
                    if(completedCount===exam.students.length){showFinalRanking(exam);}
                    else{alert(`تم حفظ نتيجة ${currentStudent}`);startExam(currentExamId);}
                });
            });
        };
    }
    
    function showFinalRanking(exam){
        const sorted=[...exam.results].sort((a,b)=>b.finalPercent-a.finalPercent);
        let html=`<h2>الترتيب النهائي - ${exam.name}</h2><table class="leaderboard-table"><thead><tr><th>#</th><th>الاسم</th><th>النسبة</th><th>الأخطاء</th></tr></thead><tbody>`;
        sorted.forEach((r,idx)=>{let rankClass='';if(idx===0)rankClass='rank-1';else if(idx===1)rankClass='rank-2';else if(idx===2)rankClass='rank-3';html+=`<tr class="${rankClass}"><td>${idx+1}</td><td>${r.name}</td><td><strong>${r.finalPercent.toFixed(1)}%</strong></td><td>${r.totalErrors}</td></tr>`;});
        html+=`</tbody></table><button id="close-final" class="btn-primary" style="margin-top:20px">إغلاق</button>`;
        document.getElementById('results-content').innerHTML=html;
        document.getElementById('results-modal').style.display='flex';
        document.getElementById('close-final').onclick=()=>{document.getElementById('results-modal').style.display='none';loadExams();};
    }
    
    document.querySelectorAll('.tab').forEach(tab=>{tab.onclick=()=>{document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active'));tab.classList.add('active');document.getElementById(`tab-${tab.dataset.tab}`).classList.add('active');if(tab.dataset.tab==='exams')loadExams();};});
    document.getElementById('close-edit-btn').onclick=()=>{document.getElementById('edit-modal').style.display='none';};
    loadExams();
</script>
</body>
</html>
'''

# ============================================
# API Routes
# ============================================
@app.route('/login')
def login():
    return render_template_string(LOGIN_PAGE)

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if username in USERS and USERS[username] == password:
        session['logged_in'] = True
        session['username'] = username
        return redirect(url_for('main_app'))
    return render_template_string(LOGIN_PAGE, error="اسم المستخدم أو كلمة المرور غير صحيحة")

@app.route('/register')
def register():
    return render_template_string(REGISTER_PAGE)

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if not username or not password:
        return render_template_string(REGISTER_PAGE, error="جميع الحقول مطلوبة")
    if password != confirm_password:
        return render_template_string(REGISTER_PAGE, error="كلمتا المرور غير متطابقتين")
    if username in USERS:
        return render_template_string(REGISTER_PAGE, error="اسم المستخدم موجود بالفعل")
    USERS[username] = password
    save_users(USERS)
    return render_template_string(LOGIN_PAGE, register_success=True)

@app.route('/app')
def main_app():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template_string(MAIN_APP_PAGE, username=session.get('username', ''))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/exams')
def api_exams():
    return jsonify(load_exams())

@app.route('/api/exam/<exam_id>')
def api_exam(exam_id):
    exams = load_exams()
    return jsonify(exams.get(exam_id, {}))

@app.route('/api/exams', methods=['POST'])
def api_create_exam():
    exams = load_exams()
    exam_id = str(len(exams) + 1)
    data = request.json
    data['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    data['results'] = []
    exams[exam_id] = data
    save_exams(exams)
    return jsonify({"status": "success", "id": exam_id})

@app.route('/api/exam/<exam_id>', methods=['PUT'])
def api_update_exam(exam_id):
    exams = load_exams()
    if exam_id in exams:
        data = request.json
        exams[exam_id].update(data)
        save_exams(exams)
    return jsonify({"status": "success"})

@app.route('/api/exam/<exam_id>', methods=['DELETE'])
def api_delete_exam(exam_id):
    exams = load_exams()
    if exam_id in exams:
        del exams[exam_id]
        save_exams(exams)
    return jsonify({"status": "success"})

@app.route('/api/exam/<exam_id>/result', methods=['POST'])
def api_add_result(exam_id):
    exams = load_exams()
    if exam_id in exams:
        result = request.json
        if 'results' not in exams[exam_id]:
            exams[exam_id]['results'] = []
        existing = next((r for r in exams[exam_id]['results'] if r['name'] == result['name']), None)
        if existing:
            existing.update(result)
        else:
            exams[exam_id]['results'].append(result)
        save_exams(exams)
    return jsonify({"status": "success"})

@app.route('/api/questions/part/<int:part_num>')
def api_part_questions(part_num):
    num = request.args.get('num', default=10, type=int)
    return jsonify(generate_random_questions_for_part(part_num, num))

@app.route('/api/questions/full')
def api_full_questions():
    num = request.args.get('num', default=30, type=int)
    return jsonify(generate_full_questions(num))

if __name__ == '__main__':
    print("\n" + "="*60)
    print("نور البيان - نظام الاختبارات القرآنية")
    print("="*60)
    print("\nافتح الرابط في المتصفح:")
    print("   http://127.0.0.1:5000/login")
    print("\nحسابات مسبقة:")
    print("   admin / 123456")
    print("   teacher / quran2024")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)