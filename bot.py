import telebot
from telebot import types
import random
import json
import os
from datetime import datetime, timedelta

# ═══════════════════════════════════════════
# НАСТРОЙКИ
# ═══════════════════════════════════════════
TOKEN = "8899609680:AAHvHn1owhapJkCcFktDmwl61OR6DCxXw2Q"
ADMIN_IDS = [8205213837]

bot = telebot.TeleBot(TOKEN, threaded=False)

# ═══════════════════════════════════════════
# ПАПКИ И ФАЙЛЫ
# ═══════════════════════════════════════════
DB_FILE = "brawlers_db.json"
PROMO_FILE = "promocodes.json"
SONGS_FILE = "songs.json"
SONGS_DIR = "songs_mp3"

if not os.path.exists(SONGS_DIR):
    os.makedirs(SONGS_DIR)

# ═══════════════════════════════════════════
# КАРТИНКИ
# ═══════════════════════════════════════════
MENU_IMAGES = {
    "main": "https://cdn.brawlify.com/backgrounds/Brawl_Stars_Background.jpg",
    "arena": "https://cdn.brawlify.com/backgrounds/Arena_Background.jpg",
    "shop": "https://cdn.brawlify.com/backgrounds/Shop_Background.jpg",
    "profile": "https://cdn.brawlify.com/backgrounds/Profile_Background.jpg",
    "guide": "https://cdn.brawlify.com/backgrounds/Guide_Background.jpg",
    "bpass": "https://cdn.brawlify.com/backgrounds/Brawl_Pass_Background.jpg",
    "top": "https://cdn.brawlify.com/backgrounds/Leaderboard_Background.jpg",
    "secret": "https://cdn.brawlify.com/brawler/Spike_Sakura.png",
    "skins": "https://cdn.brawlify.com/backgrounds/Skins_Background.jpg",
    "brawlers_shop": "https://cdn.brawlify.com/backgrounds/Brawlers_Background.jpg",
    "win": "https://cdn.brawlify.com/backgrounds/Win_Background.jpg",
    "lose": "https://cdn.brawlify.com/backgrounds/Lose_Background.jpg",
    "daily": "https://cdn.brawlify.com/backgrounds/Daily_Background.jpg",
    "premium": "https://cdn.brawlify.com/backgrounds/Premium_Background.jpg",
    "song": "https://cdn.brawlify.com/backgrounds/Music_Background.jpg"
}

BRAWLER_IMAGES = {
    "Shelly": "https://cdn.brawlify.com/brawler/Shelly.png",
    "Colt": "https://cdn.brawlify.com/brawler/Colt.png",
    "Bull": "https://cdn.brawlify.com/brawler/Bull.png",
    "Jessie": "https://cdn.brawlify.com/brawler/Jessie.png",
    "Brock": "https://cdn.brawlify.com/brawler/Brock.png",
    "Spike": "https://cdn.brawlify.com/brawler/Spike.png",
    "Crow": "https://cdn.brawlify.com/brawler/Crow.png",
    "MEBY_BABY": "https://cdn.brawlify.com/brawler/Spike_Sakura.png"
}

EMOJI = {
    "cups": "🏆", "coins": "💰", "gems": "💎", "blings": "💠", "credits": "⭐",
    "level": "⬆️", "win": "✅", "lose": "❌", "box": "📦", "brawler": "🎯",
    "skin": "🎨", "shop": "🛒", "battle": "⚔️", "profile": "👤", "guide": "📚",
    "top": "🏅", "bpass": "🎫", "secret": "👶", "daily": "☀️", "promo": "🎁",
    "premium": "👑", "back": "🔙", "star": "🌟", "music": "🎵"
}

# ═══════════════════════════════════════════
# БАЗА ДАННЫХ
# ═══════════════════════════════════════════
DEFAULT_USER = {
    "cups": 0, "brawlers": ["Shelly"], "skins": {},
    "wins": 0, "losses": 0,
    "coins": 500, "gems": 10, "blings": 100, "credits": 50,
    "level": 1, "exp": 0,
    "pass_level": 0, "pass_premium": False,
    "boxes_opened": 0, "total_donated": 0,
    "last_daily": None
}

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(db, f, ensure_ascii=False, indent=2)

def get_user(uid):
    db = load_db()
    uid = str(uid)
    if uid not in db: db[uid] = DEFAULT_USER.copy(); save_db(db)
    return db[uid]

def update_user(uid, data):
    db = load_db(); db[str(uid)] = data; save_db(db)

def is_admin(uid): return uid in ADMIN_IDS

def gain_exp(user, amt):
    user["exp"] += amt
    old = user["level"]
    user["level"] = 1 + user["exp"] // 100
    return user["level"] - old

# ═══════════════════════════════════════════
# БОЙЦЫ
# ═══════════════════════════════════════════
ALL_BRAWLERS = {
    "Shelly": {"rarity": "Начальный", "hp": 3800, "damage": 300, "price_credits": 0, "icon": "🔫",
        "image": BRAWLER_IMAGES["Shelly"],
        "attacks": {
            "basic": {"name": "Дробовик", "dmg_mult": 1.0},
            "skill1": {"name": "Картечь", "dmg_mult": 1.5, "cooldown": 2},
            "skill2": {"name": "Рывок", "dmg_mult": 0, "cooldown": 3, "effect": "dodge"}},
        "skins": {"default": {"name": "Обычная", "price": 0, "image": BRAWLER_IMAGES["Shelly"]},
                  "bandita": {"name": "Бандитка Шелли", "price": 2750, "image": "https://cdn.brawlify.com/brawler/Shelly_Bandita.png"}}},
    "Colt": {"rarity": "Обычный", "hp": 2800, "damage": 400, "price_credits": 100, "icon": "🤠",
        "image": BRAWLER_IMAGES["Colt"],
        "attacks": {
            "basic": {"name": "Револьвер", "dmg_mult": 1.0},
            "skill1": {"name": "Очередь", "dmg_mult": 1.8, "cooldown": 2},
            "skill2": {"name": "Перезарядка", "dmg_mult": 0, "cooldown": 3, "effect": "double_next"}},
        "skins": {"default": {"name": "Обычный", "price": 0, "image": BRAWLER_IMAGES["Colt"]},
                  "rockstar": {"name": "Рок-звезда", "price": 5000, "image": "https://cdn.brawlify.com/brawler/Colt_Rockstar.png"}}},
    "Bull": {"rarity": "Обычный", "hp": 5200, "damage": 280, "price_credits": 100, "icon": "🐂",
        "image": BRAWLER_IMAGES["Bull"],
        "attacks": {
            "basic": {"name": "Двустволка", "dmg_mult": 1.0},
            "skill1": {"name": "Берсерк", "dmg_mult": 1.3, "cooldown": 2, "effect": "shield"},
            "skill2": {"name": "Таран", "dmg_mult": 1.6, "cooldown": 3, "effect": "stun"}},
        "skins": {"default": {"name": "Обычный", "price": 0, "image": BRAWLER_IMAGES["Bull"]},
                  "viking": {"name": "Викинг", "price": 5000, "image": "https://cdn.brawlify.com/brawler/Bull_Viking.png"}}},
    "Jessie": {"rarity": "Обычный", "hp": 3200, "damage": 260, "price_credits": 100, "icon": "⚡",
        "image": BRAWLER_IMAGES["Jessie"],
        "attacks": {
            "basic": {"name": "Электрошок", "dmg_mult": 1.0},
            "skill1": {"name": "Турель", "dmg_mult": 0.7, "cooldown": 2, "effect": "turret"},
            "skill2": {"name": "Перегрузка", "dmg_mult": 1.4, "cooldown": 3, "effect": "burn"}},
        "skins": {"default": {"name": "Обычная", "price": 0, "image": BRAWLER_IMAGES["Jessie"]},
                  "summer": {"name": "Летняя", "price": 5000, "image": "https://cdn.brawlify.com/brawler/Jessie_Summer.png"}}},
    "Brock": {"rarity": "Обычный", "hp": 2600, "damage": 500, "price_credits": 100, "icon": "🚀",
        "image": BRAWLER_IMAGES["Brock"],
        "attacks": {
            "basic": {"name": "Ракета", "dmg_mult": 1.0},
            "skill1": {"name": "Залп", "dmg_mult": 1.7, "cooldown": 3},
            "skill2": {"name": "Зажигалка", "dmg_mult": 0.8, "cooldown": 2, "effect": "burn"}},
        "skins": {"default": {"name": "Обычный", "price": 0, "image": BRAWLER_IMAGES["Brock"]},
                  "lion": {"name": "Лев", "price": 7500, "image": "https://cdn.brawlify.com/brawler/Brock_Lion.png"}}},
    "Spike": {"rarity": "Легендарный", "hp": 3000, "damage": 420, "price_credits": 2000, "icon": "🌵",
        "image": BRAWLER_IMAGES["Spike"],
        "attacks": {
            "basic": {"name": "Кактус", "dmg_mult": 1.0},
            "skill1": {"name": "Шипы", "dmg_mult": 1.3, "cooldown": 2, "effect": "burn"},
            "skill2": {"name": "Цветение", "dmg_mult": 0, "cooldown": 3, "effect": "heal"}},
        "skins": {"default": {"name": "Обычный", "price": 0, "image": BRAWLER_IMAGES["Spike"]},
                  "sakura": {"name": "Сакура", "price": 25000, "image": "https://cdn.brawlify.com/brawler/Spike_Sakura.png"}}},
    "Crow": {"rarity": "Легендарный", "hp": 2400, "damage": 380, "price_credits": 2000, "icon": "🦅",
        "image": BRAWLER_IMAGES["Crow"],
        "attacks": {
            "basic": {"name": "Кинжалы", "dmg_mult": 1.0},
            "skill1": {"name": "Яд", "dmg_mult": 0.8, "cooldown": 2, "effect": "burn"},
            "skill2": {"name": "Полёт", "dmg_mult": 0, "cooldown": 3, "effect": "counter"}},
        "skins": {"default": {"name": "Обычный", "price": 0, "image": BRAWLER_IMAGES["Crow"]},
                  "phoenix": {"name": "Феникс", "price": 25000, "image": "https://cdn.brawlify.com/brawler/Crow_Phoenix.png"}}},
    "MEBY_BABY": {"rarity": "Секретный", "hp": 9999, "damage": 999, "price_credits": 9999, "icon": "👶",
        "secret": True, "image": BRAWLER_IMAGES["MEBY_BABY"],
        "attacks": {
            "basic": {"name": "👶 Плач Мэйби", "dmg_mult": 1.5},
            "skill1": {"name": "🍼 Бутылочка", "dmg_mult": 0, "cooldown": 2, "effect": "heal_big"},
            "skill2": {"name": "💫 МЭЙБИ БЭЙБИ", "dmg_mult": 3.0, "cooldown": 4, "effect": "stun"}},
        "skins": {"default": {"name": "Мэйби Бэйби", "price": 0, "image": BRAWLER_IMAGES["MEBY_BABY"]},
                  "golden": {"name": "Золотой", "price": 100000, "image": BRAWLER_IMAGES["MEBY_BABY"]}}}
}

# ═══════════════════════════════════════════
# СИСТЕМА MP3 ПЕСЕН
# ═══════════════════════════════════════════
def load_songs():
    if os.path.exists(SONGS_FILE):
        with open(SONGS_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {}

def save_songs(data):
    with open(SONGS_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)

@bot.message_handler(commands=["songs"])
def songs_menu(msg):
    songs = load_songs()
    text = f"{EMOJI['music']} 🎵 *MP3 ПЛЕЙЛИСТ*\n\n"
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    if not songs:
        text += "📭 Плейлист пуст. Админ может добавить MP3 через /addsong"
    else:
        for i, (name, info) in enumerate(songs.items(), 1):
            text += f"*{i}. {name}*\n👤 {info['author']}\n\n"
            markup.add(types.InlineKeyboardButton(f"▶️ {name}", callback_data=f"mp3_{name}"))
    
    markup.add(types.InlineKeyboardButton(f"{EMOJI['back']} Назад", callback_data="back_menu"))
    if is_admin(msg.from_user.id):
        markup.add(types.InlineKeyboardButton("➕ Добавить MP3", callback_data="add_mp3_menu"))
    
    send_photo_menu(msg.chat.id, "song", text, markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("mp3_"))
def play_mp3(call):
    songs = load_songs()
    name = call.data.replace("mp3_", "")
    
    if name in songs:
        file_path = songs[name]["file"]
        if os.path.exists(file_path):
            try:
                with open(file_path, "rb") as audio:
                    bot.send_audio(
                        call.message.chat.id,
                        audio,
                        title=name,
                        performer=songs[name]["author"],
                        caption=f"🎵 *{name}* — {songs[name]['author']}",
                        parse_mode="Markdown"
                    )
            except Exception as e:
                bot.send_message(call.message.chat.id, f"❌ Ошибка воспроизведения: {e}")
        else:
            bot.send_message(call.message.chat.id, "❌ Файл не найден!")
    else:
        bot.answer_callback_query(call.id, "Песня не найдена!")

@bot.callback_query_handler(func=lambda c: c.data == "add_mp3_menu")
def add_mp3_menu(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ Только админ!"); return
    
    msg = bot.send_message(call.message.chat.id,
        f"{EMOJI['music']} ➕ *ДОБАВИТЬ MP3*\n\n"
        "Отправь MP3-файл с подписью:\n"
        "`НАЗВАНИЕ | АВТОР`\n\n"
        "*Пример:* Отправь файл song.mp3 с подписью `Моя песня | Я`",
        parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_add_mp3_file)

@bot.message_handler(commands=["addsong"])
def addsong_cmd(msg):
    if not is_admin(msg.from_user.id):
        bot.send_message(msg.chat.id, "❌ Нет доступа!"); return
    
    msg = bot.send_message(msg.chat.id,
        f"{EMOJI['music']} ➕ *ДОБАВИТЬ MP3*\n\n"
        "Отправь MP3-файл с подписью:\n"
        "`НАЗВАНИЕ | АВТОР`",
        parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_add_mp3_file)

@bot.message_handler(content_types=["audio"])
def receive_mp3(msg):
    """Принимает MP3 от админа"""
    if not is_admin(msg.from_user.id):
        bot.send_message(msg.chat.id, "❌ Только админ может добавлять песни!")
        return
    
    if msg.caption:
        try:
            parts = msg.caption.split("|", 1)
            name = parts[0].strip()
            author = parts[1].strip() if len(parts) > 1 else "Неизвестен"
        except:
            name = msg.audio.title or "Без названия"
            author = msg.audio.performer or "Неизвестен"
    else:
        name = msg.audio.title or f"Трек_{random.randint(1000,9999)}"
        author = msg.audio.performer or "Неизвестен"
    
    # Скачиваем файл
    file_info = bot.get_file(msg.audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Сохраняем
    safe_name = "".join(c for c in name if c.isalnum() or c in " _-")
    file_path = os.path.join(SONGS_DIR, f"{safe_name}.mp3")
    
    with open(file_path, "wb") as f:
        f.write(downloaded_file)
    
    # Сохраняем в JSON
    songs = load_songs()
    songs[name] = {"file": file_path, "author": author}
    save_songs(songs)
    
    bot.send_message(msg.chat.id, f"✅ MP3 *'{name}'* добавлен в плейлист!\n🎵 /songs", parse_mode="Markdown")

def process_add_mp3_file(msg):
    """Обработчик для register_next_step_handler"""
    if msg.content_type == "audio":
        receive_mp3(msg)
    else:
        bot.send_message(msg.chat.id, "❌ Отправь MP3-файл!")

@bot.message_handler(commands=["deletesong"])
def deletesong_cmd(msg):
    if not is_admin(msg.from_user.id): return
    try:
        name = msg.text.replace("/deletesong", "").strip()
        songs = load_songs()
        if name in songs:
            # Удаляем файл
            if os.path.exists(songs[name]["file"]):
                os.remove(songs[name]["file"])
            del songs[name]
            save_songs(songs)
            bot.send_message(msg.chat.id, f"✅ Песня '{name}' удалена!")
        else:
            bot.send_message(msg.chat.id, "❌ Не найдена!")
    except:
        bot.send_message(msg.chat.id, "❌ /deletesong НАЗВАНИЕ")

# ═══════════════════════════════════════════
# КНОПКИ
# ═══════════════════════════════════════════
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(f"{EMOJI['battle']} Арена", f"{EMOJI['box']} Ящики")
    markup.add(f"{EMOJI['shop']} Магазин", f"{EMOJI['profile']} Профиль")
    markup.add(f"{EMOJI['guide']} Гид", f"{EMOJI['bpass']} Brawl Pass")
    markup.add(f"{EMOJI['top']} Топ", f"{EMOJI['secret']} Секрет")
    markup.add(f"{EMOJI['music']} Песни", f"🎁 Промокод")
    return markup

def send_photo_menu(chat_id, image_key, text, reply_markup=None):
    try:
        bot.send_photo(chat_id, MENU_IMAGES.get(image_key, MENU_IMAGES["main"]),
                       caption=text, parse_mode="Markdown", reply_markup=reply_markup)
    except:
        bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=reply_markup)

# ═══════════════════════════════════════════
# СТАРТ
# ═══════════════════════════════════════════
@bot.message_handler(commands=["start"])
def start(msg):
    user = get_user(msg.from_user.id)
    text = (f"🥊 *BRAWL STARS BOT*\n\n"
            f"👤 {EMOJI['cups']} Кубки: *{user['cups']}*\n"
            f"{EMOJI['level']} Уровень: *{user['level']}*\n"
            f"{EMOJI['brawler']} Бойцов: *{len(user['brawlers'])}*\n\n"
            f"💰 {EMOJI['coins']} *{user['coins']}* | {EMOJI['gems']} *{user['gems']}*\n"
            f"{EMOJI['blings']} *{user['blings']}* | {EMOJI['credits']} *{user['credits']}*\n\n"
            f"/daily /promo /songs /admin")
    send_photo_menu(msg.chat.id, "main", text, main_menu())

@bot.message_handler(commands=["daily"])
def daily(msg):
    user = get_user(msg.from_user.id)
    today = datetime.now().strftime("%Y-%m-%d")
    if user.get("last_daily") == today:
        bot.send_message(msg.chat.id, "❌ Уже получил!"); return
    rtype = random.choice(["coins","blings","credits"])
    amt = {"coins":25,"blings":15,"credits":10}[rtype]
    user[rtype] = user.get(rtype,0) + amt
    user["last_daily"] = today
    lvl = gain_exp(user, 10)
    update_user(msg.from_user.id, user)
    text = f"☀️ +{amt} {rtype}"
    if lvl: text += f"\n⬆️ Ур.{user['level']}!"
    send_photo_menu(msg.chat.id, "daily", text)

@bot.message_handler(commands=["promo"])
def promo(msg):
    user = get_user(msg.from_user.id)
    try:
        code = msg.text.split()[1].upper()
        ok, txt = use_promo(msg.from_user.id, code, user)
        update_user(msg.from_user.id, user)
        bot.send_message(msg.chat.id, f"{'🎁 ' if ok else ''}{txt}", parse_mode="Markdown")
    except: bot.send_message(msg.chat.id, "❌ /promo КОД")

# ═══════════════════════════════════════════
# МЕНЮ
# ═══════════════════════════════════════════
@bot.message_handler(func=lambda m: any(x in m.text for x in ["Арена","Ящики","Магазин","Профиль","Гид","Brawl Pass","Топ","Секрет","Песни","Промокод"]))
def menu(msg):
    user = get_user(msg.from_user.id)
    if "Арена" in msg.text: arena_menu(msg, user)
    elif "Ящики" in msg.text: open_box(msg, user)
    elif "Магазин" in msg.text: shop(msg, user)
    elif "Профиль" in msg.text: profile(msg, user)
    elif "Гид" in msg.text: guide(msg)
    elif "Brawl Pass" in msg.text: bpass(msg, user)
    elif "Топ" in msg.text: top(msg)
    elif "Секрет" in msg.text: secret(msg, user)
    elif "Песни" in msg.text: songs_menu(msg)
    elif "Промокод" in msg.text: bot.send_message(msg.chat.id, "/promo КОД")

# ═══════════════════════════════════════════
# АРЕНА
# ═══════════════════════════════════════════
class Battle:
    def __init__(self, uid, pname, ename):
        self.uid = uid; self.pname = pname; self.ename = ename
        self.pdata = ALL_BRAWLERS[pname].copy(); self.edata = ALL_BRAWLERS[ename].copy()
        self.php = self.pdata["hp"]; self.ehp = self.edata["hp"]
        self.pmax = self.pdata["hp"]; self.emax = self.edata["hp"]
        self.pcd = {"skill1":0,"skill2":0}; self.ecd = {"skill1":0,"skill2":0}
        self.peff = []; self.eeff = []
        self.turn = 1; self.log = []; self.over = False

battles = {}

def hp_bar(cur, mx):
    n = max(0, int((cur/mx)*10)) if mx>0 else 0
    return "🟥"*n + "⬛"*(10-n) + f" {cur}/{mx}❤️"

def arena_menu(msg, user):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for b in user["brawlers"]:
        d = ALL_BRAWLERS[b]
        markup.add(types.InlineKeyboardButton(f"{d['icon']} {b}", callback_data=f"pick_{b}"))
    markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_menu"))
    send_photo_menu(msg.chat.id, "arena", "⚔️ *ВЫБЕРИ БОЙЦА*", markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("pick_"))
def battle_start(call):
    user = get_user(call.from_user.id)
    name = call.data.replace("pick_","")
    if name not in user["brawlers"]: return
    enemies = [n for n in ALL_BRAWLERS if n != name and n != "MEBY_BABY"]
    enemy = random.choice(enemies)
    battle = Battle(call.from_user.id, name, enemy)
    battles[call.from_user.id] = battle
    battle.log.append(f"⚔️ {battle.pname} VS {battle.ename}")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    show_battle(call.message.chat.id, battle)

def show_battle(cid, b):
    if b.over: return
    text = (f"⚔️ *ХОД {b.turn}*\n\n"
            f"{b.pdata['icon']} *ТЫ:* {hp_bar(b.php, b.pmax)}\n"
            f"👾 *ВРАГ:* {hp_bar(b.ehp, b.emax)}\n\n📜 {b.log[-1] if b.log else 'Начинай!'}")
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🔫 Базовая атака", callback_data="bat_basic"))
    cd1 = b.pcd["skill1"]
    markup.add(types.InlineKeyboardButton(f"⚡ Скилл 1 {'✅' if cd1==0 else f'⏳{cd1}'}", callback_data="bat_skill1" if cd1==0 else "none"))
    cd2 = b.pcd["skill2"]
    markup.add(types.InlineKeyboardButton(f"💥 Скилл 2 {'✅' if cd2==0 else f'⏳{cd2}'}", callback_data="bat_skill2" if cd2==0 else "none"))
    markup.add(types.InlineKeyboardButton("🏳️ Сбежать", callback_data="bat_flee"))
    try:
        bot.send_photo(cid, b.edata["image"], caption=text, parse_mode="Markdown", reply_markup=markup)
    except:
        bot.send_message(cid, text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("bat_"))
def battle_act(call):
    uid = call.from_user.id
    if uid not in battles: return
    b = battles[uid]
    if b.over: return
    act = call.data.replace("bat_","")
    if act == "flee":
        b.over = True
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "🏃 Сбежал!", reply_markup=main_menu())
        del battles[uid]; return
    if act == "none": return
    
    user = get_user(uid)
    dmg = 0
    if act == "basic":
        atk = b.pdata["attacks"]["basic"]
        dmg_mult = atk["dmg_mult"]
        for e in list(b.peff):
            if e["type"] == "double_next": dmg_mult *= 2; b.peff.remove(e); b.log.append("💥 х2!")
        dmg = int(b.pdata["damage"] * dmg_mult * random.uniform(0.9,1.1))
        b.ehp -= dmg; b.log.append(f"🔫 {atk['name']}: -{dmg}HP")
    elif act == "skill1":
        atk = b.pdata["attacks"]["skill1"]
        if b.pcd["skill1"] > 0: return
        dmg = int(b.pdata["damage"] * atk["dmg_mult"] * random.uniform(0.9,1.1))
        b.ehp -= dmg; b.pcd["skill1"] = atk["cooldown"]
        b.log.append(f"⚡ {atk['name']}: -{dmg}HP")
        if "effect" in atk: apply_effect(b, atk["effect"], dmg)
    elif act == "skill2":
        atk = b.pdata["attacks"]["skill2"]
        if b.pcd["skill2"] > 0: return
        dmg = int(b.pdata["damage"] * atk["dmg_mult"] * random.uniform(0.9,1.1))
        b.ehp -= dmg; b.pcd["skill2"] = atk["cooldown"]
        b.log.append(f"💥 {atk['name']}: -{dmg}HP")
        if "effect" in atk: apply_effect(b, atk["effect"], dmg)
    
    for e in list(b.eeff):
        if e["type"] == "shield": b.ehp += int(dmg*0.5); b.eeff.remove(e); b.log.append("🛡️ Щит врага!")
    if b.ehp <= 0: b.over = True; end_battle(call.message.chat.id, b, user, "win"); return
    
    enemy_turn(b)
    if b.php <= 0: b.over = True; end_battle(call.message.chat.id, b, user, "lose"); return
    
    for k in ["skill1","skill2"]:
        if b.pcd[k] > 0: b.pcd[k] -= 1
        if b.ecd[k] > 0: b.ecd[k] -= 1
    for e in list(b.peff):
        if e["type"] == "burn": b.php -= e["dmg"]; b.log.append(f"🔥 -{e['dmg']}HP"); e["dur"]-=1
        elif e["type"] == "turret": b.ehp -= e["dmg"]; b.log.append(f"🔧 -{e['dmg']}HP"); e["dur"]-=1
        if e["dur"] <= 0: b.peff.remove(e)
    for e in list(b.eeff):
        if e["type"] == "burn": b.ehp -= e["dmg"]; b.log.append(f"🔥 Враг -{e['dmg']}HP"); e["dur"]-=1
        if e["dur"] <= 0: b.eeff.remove(e)
    b.turn += 1
    bot.delete_message(call.message.chat.id, call.message.message_id)
    show_battle(call.message.chat.id, b)

def apply_effect(b, effect, dmg):
    if effect == "burn": b.eeff.append({"type":"burn","dmg":int(dmg*0.3),"dur":3}); b.log.append("🔥 Враг горит!")
    elif effect == "dodge": b.peff.append({"type":"dodge","dur":1}); b.log.append("💨 Уклонение!")
    elif effect == "shield": b.peff.append({"type":"shield","dur":2}); b.log.append("🛡️ Щит!")
    elif effect == "stun": b.eeff.append({"type":"stun","dur":1}); b.log.append("💫 Враг оглушён!")
    elif effect == "heal": h = int(b.pmax*0.3); b.php = min(b.pmax,b.php+h); b.log.append(f"💚 +{h}HP")
    elif effect == "heal_big": h = int(b.pmax*0.5); b.php = min(b.pmax,b.php+h); b.log.append(f"🍼 +{h}HP")
    elif effect == "double_next": b.peff.append({"type":"double_next","dur":1}); b.log.append("💪 х2!")
    elif effect == "turret": b.peff.append({"type":"turret","dmg":int(dmg*0.5),"dur":2}); b.log.append("🔧 Турель!")
    elif effect == "counter": b.peff.append({"type":"counter","dur":1}); b.log.append("🔄 Контратака!")

def enemy_turn(b):
    for e in list(b.eeff):
        if e["type"] == "stun": b.log.append("💫 Враг оглушён!"); b.eeff.remove(e); return
    for e in list(b.peff):
        if e["type"] == "dodge": b.log.append("💨 Уклонение!"); b.peff.remove(e); return
    atk = b.edata["attacks"]["basic"]
    dmg = int(b.edata["damage"] * atk["dmg_mult"] * random.uniform(0.9,1.1))
    b.php -= dmg; b.log.append(f"💢 Враг: {atk['name']} -{dmg}HP")
    for e in list(b.peff):
        if e["type"] == "counter": b.ehp -= int(dmg*0.5); b.log.append(f"🔄 Контратака! -{int(dmg*0.5)}HP"); b.peff.remove(e)

def end_battle(cid, b, user, result):
    if result == "win":
        cups = random.randint(8,15); coins = random.randint(20,50); exp = random.randint(20,40)
        user["cups"] += cups; user["coins"] += coins; user["wins"] += 1
        lvl = gain_exp(user, exp)
        text = f"🏆 *ПОБЕДА!*\n+{cups}🏆 +{coins}💰 +{exp}✨"
        if lvl > 0: text += f"\n⬆️ Уровень {user['level']}!"; user["gems"] += lvl*5
        img = "win"
        ok, msg = check_secret(user)
        if ok: update_user(b.uid, user); bot.send_message(cid, f"👶 {msg}", parse_mode="Markdown")
    else:
        cups = random.randint(5,10); user["cups"] = max(0,user["cups"]-cups); user["losses"] += 1
        exp = random.randint(5,15); gain_exp(user, exp)
        text = f"💀 *ПОРАЖЕНИЕ*\n-{cups}🏆 +{exp}✨"
        img = "lose"
    update_user(b.uid, user)
    send_photo_menu(cid, img, f"⚔️ *БОЙ ОКОНЧЕН*\n\n{text}")
    bot.send_message(cid, "Готов к битвам!", reply_markup=main_menu())
    if b.uid in battles: del battles[b.uid]

def check_secret(user):
    if "MEBY_BABY" in user["brawlers"]: return False, ""
    if user.get("boxes_opened",0) >= 500: user["brawlers"].append("MEBY_BABY"); return True, "🎉 *500 ЯЩИКОВ!*"
    if user.get("cups",0) >= 5000: user["brawlers"].append("MEBY_BABY"); return True, "🎉 *5000 КУБКОВ!*"
    if user.get("wins",0) >= 100: user["brawlers"].append("MEBY_BABY"); return True, "🎉 *100 ПОБЕД!*"
    return False, ""

def open_box(msg, user):
    if user["coins"] < 50: bot.send_message(msg.chat.id, "❌ 50💰"); return
    user["coins"] -= 50; user["boxes_opened"] += 1
    if "MEBY_BABY" not in user["brawlers"] and random.random() < 0.001:
        user["brawlers"].append("MEBY_BABY"); update_user(msg.from_user.id, user)
        send_photo_menu(msg.chat.id, "secret", "🎉👶 *МЭЙБИ БЭЙБИ!*"); return
    roll = random.randint(1,100)
    if roll <= 5: rarity = "Легендарный"
    elif roll <= 30: rarity = "Эпический"
    elif roll <= 90: rarity = "Обычный"
    else: rarity = "Начальный"
    pool = [n for n,d in ALL_BRAWLERS.items() if d.get("rarity")==rarity and n!="MEBY_BABY"]
    name = random.choice(pool) if pool else "Shelly"
    if name in user["brawlers"]:
        bonus = {"Начальный":10,"Обычный":25,"Эпический":50,"Легендарный":100}
        user["coins"] += bonus.get(rarity,20)
        bot.send_message(msg.chat.id, f"📦 Дубль! +{bonus.get(rarity,20)}💰")
    else:
        user["brawlers"].append(name)
        bot.send_message(msg.chat.id, f"🎉 *{name}!* ({rarity})", parse_mode="Markdown")
    update_user(msg.from_user.id, user)

def profile(msg, user):
    text = (f"👤 *ПРОФИЛЬ*\n{EMOJI['cups']} Кубки: *{user['cups']}*\n"
            f"{EMOJI['level']} Уровень: *{user['level']}*\n"
            f"{EMOJI['win']} Побед: *{user['wins']}* | {EMOJI['lose']} *{user['losses']}*\n\n"
            f"💰 {user['coins']} | 💎 {user['gems']}\n💠 {user['blings']} | ⭐ {user['credits']}\n"
            f"📦 Ящиков: *{user['boxes_opened']}* | 🎯 Бойцов: *{len(user['brawlers'])}*")
    send_photo_menu(msg.chat.id, "profile", text)

def shop(msg, user):
    text = (f"🛒 *МАГАЗИН*\n💰 {user['coins']} | 💎 {user['gems']}\n💠 {user['blings']} | ⭐ {user['credits']}\n")
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("📦 Ящик 80💰", callback_data="shop_box1"),
               types.InlineKeyboardButton("📦📦 3 ящика 200💰", callback_data="shop_box3"),
               types.InlineKeyboardButton("🎨 Скины", callback_data="shop_skins"),
               types.InlineKeyboardButton("🎯 Бойцы", callback_data="shop_brawlers"),
               types.InlineKeyboardButton("👶 Секретный", callback_data="shop_secret"),
               types.InlineKeyboardButton("🔙 Назад", callback_data="back_menu"))
    send_photo_menu(msg.chat.id, "shop", text, markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("shop_"))
def shop_act(call):
    user = get_user(call.from_user.id)
    act = call.data
    if act == "shop_box1":
        if user["coins"] < 80: bot.answer_callback_query(call.id, "❌ 80💰"); return
        user["coins"] -= 80; open_box(call.message, user)
    elif act == "shop_box3":
        if user["coins"] < 200: bot.answer_callback_query(call.id, "❌ 200💰"); return
        user["coins"] -= 200
        for _ in range(3): open_box(call.message, user)
        bot.send_message(call.message.chat.id, "📦 3 ящика!")
    elif act == "shop_skins":
        markup = types.InlineKeyboardMarkup()
        for bn, bd in ALL_BRAWLERS.items():
            if bn not in user["brawlers"]: continue
            for sn, sd in bd["skins"].items():
                if sn == "default": continue
                if sn not in user.get("skins",{}).get(bn,[]):
                    markup.add(types.InlineKeyboardButton(f"{sd['name']} {sd['price']}💠", callback_data=f"skin_{bn}_{sn}"))
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_shop"))
        send_photo_menu(call.message.chat.id, "skins", f"🎨 *СКИНЫ*\n💠 {user['blings']}", markup)
    elif act == "shop_brawlers":
        markup = types.InlineKeyboardMarkup()
        for name, data in ALL_BRAWLERS.items():
            if name == "MEBY_BABY": continue
            if name not in user["brawlers"] and data["price_credits"] > 0:
                markup.add(types.InlineKeyboardButton(f"{data['icon']} {name} {data['price_credits']}⭐", callback_data=f"braw_{name}"))
        markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_shop"))
        send_photo_menu(call.message.chat.id, "brawlers_shop", f"🎯 *БОЙЦЫ*\n⭐ {user['credits']}", markup)
    elif act == "shop_secret": secret(call.message, user)

@bot.callback_query_handler(func=lambda c: c.data.startswith("skin_"))
def buy_skin(call):
    user = get_user(call.from_user.id)
    _, bn, sn = call.data.split("_",2)
    price = ALL_BRAWLERS[bn]["skins"][sn]["price"]
    if user["blings"] < price: bot.answer_callback_query(call.id, "❌"); return
    user["blings"] -= price; user.setdefault("skins",{}).setdefault(bn,[]).append(sn)
    update_user(call.from_user.id, user)
    bot.send_message(call.message.chat.id, "🎨 Куплен!")

@bot.callback_query_handler(func=lambda c: c.data.startswith("braw_"))
def buy_brawler(call):
    user = get_user(call.from_user.id)
    name = call.data.replace("braw_","")
    price = ALL_BRAWLERS[name]["price_credits"]
    if user["credits"] < price: bot.answer_callback_query(call.id, "❌"); return
    user["credits"] -= price; user["brawlers"].append(name)
    update_user(call.from_user.id, user)
    bot.send_message(call.message.chat.id, f"🎯 *{name}* куплен!", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: c.data == "back_shop")
def back_shop(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    shop(call.message, get_user(call.from_user.id))

def guide(msg):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for name, data in ALL_BRAWLERS.items():
        markup.add(types.InlineKeyboardButton(f"{data['icon']} {name}", callback_data=f"guide_{name}"))
    send_photo_menu(msg.chat.id, "guide", "📚 *ГИД*", markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("guide_"))
def guide_info(call):
    name = call.data.replace("guide_","")
    d = ALL_BRAWLERS[name]
    text = f"{d['icon']} *{name}* ({d['rarity']})\n❤️ {d['hp']} | 💥 {d['damage']}"
    try: bot.send_photo(call.message.chat.id, d["image"], caption=text, parse_mode="Markdown")
    except: bot.send_message(call.message.chat.id, text, parse_mode="Markdown")

def top(msg):
    db = load_db()
    top10 = sorted(db.items(), key=lambda x: x[1].get("cups",0), reverse=True)[:10]
    text = "🏆 *ТОП-10*\n\n" + "\n".join(f"{i}. ID{u}: {d['cups']}🏆" for i,(u,d) in enumerate(top10,1))
    send_photo_menu(msg.chat.id, "top", text)

def bpass(msg, user):
    text = f"🎫 *BRAWL PASS*\nУр.{user['pass_level']}/30\n{'👑 Premium' if user['pass_premium'] else '🆓 Бесплатный'}"
    markup = types.InlineKeyboardMarkup()
    if not user["pass_premium"]:
        markup.add(types.InlineKeyboardButton("👑 Купить 200💎", callback_data="buy_prem"))
    send_photo_menu(msg.chat.id, "bpass", text, markup)

@bot.callback_query_handler(func=lambda c: c.data == "buy_prem")
def buy_prem(call):
    user = get_user(call.from_user.id)
    if user["gems"] < 200: bot.answer_callback_query(call.id, "❌"); return
    user["gems"] -= 200; user["pass_premium"] = True; user["total_donated"] += 200
    update_user(call.from_user.id, user)
    send_photo_menu(call.message.chat.id, "premium", "👑 *Premium!*")

def secret(msg, user):
    has = "MEBY_BABY" in user["brawlers"]
    text = (f"👶 *МЭЙБИ БЭЙБИ*\n❤️ 9999 | 💥 999\n"
            f"{'✅ У ТЕБЯ ЕСТЬ!' if has else '🔒 500 ящиков / 5000🏆 / 100 побед'}")
    send_photo_menu(msg.chat.id, "secret", text)

@bot.callback_query_handler(func=lambda c: c.data == "back_menu")
def back_menu(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "📋 Меню:", reply_markup=main_menu())

# ═══════════════════════════════════════════
# ПРОМОКОДЫ
# ═══════════════════════════════════════════
def load_promos():
    if os.path.exists(PROMO_FILE):
        with open(PROMO_FILE, "r") as f: return json.load(f)
    return {}

def save_promos(data):
    with open(PROMO_FILE, "w") as f: json.dump(data, f)

def use_promo(uid, code, user):
    promos = load_promos()
    code = code.upper()
    if code not in promos: return False, "❌ Не найден!"
    p = promos[code]
    if "expires" in p and datetime.now() > datetime.fromisoformat(p["expires"]): return False, "❌ Истёк!"
    if "max_uses" in p and p.get("uses",0) >= p["max_uses"]: return False, "❌ Лимит!"
    p.setdefault("used_by", [])
    if str(uid) in p["used_by"]: return False, "❌ Уже использован!"
    rtype, amt = p["type"], p["amount"]
    if rtype == "coins": user["coins"] += amt; msg = f"+{amt}💰"
    elif rtype == "gems": user["gems"] += amt; msg = f"+{amt}💎"
    elif rtype == "blings": user["blings"] += amt; msg = f"+{amt}💠"
    elif rtype == "credits": user["credits"] += amt; msg = f"+{amt}⭐"
    elif rtype == "cups": user["cups"] += amt; msg = f"+{amt}🏆"
    elif rtype == "brawler":
        if amt not in user["brawlers"]: user["brawlers"].append(amt); msg = f"🎯 {amt}!"
        else: user["coins"] += 100; msg = "Уже есть! +100💰"
    else: msg = f"+{amt} {rtype}"
    p["used_by"].append(str(uid)); p["uses"] = p.get("uses",0)+1
    save_promos(promos)
    return True, msg

@bot.message_handler(commands=["create_promo"])
def create_promo(msg):
    if not is_admin(msg.from_user.id): return
    bot.send_message(msg.chat.id, "📝 Формат: `КОД ТИП КОЛ-ВО [ЛИМИТ] [ЧАСЫ]`\nТипы: coins,gems,blings,credits,cups,brawler", parse_mode="Markdown")
    bot.register_next_step_handler(msg, proc_create_promo)

def proc_create_promo(msg):
    try:
        p = msg.text.split(); code = p[0].upper(); rtype = p[1]
        amt = int(p[2]) if p[2].isdigit() else p[2]
        promos = load_promos()
        promos[code] = {"type":rtype,"amount":amt,"uses":0,"used_by":[]}
        if len(p)>3: promos[code]["max_uses"]=int(p[3])
        if len(p)>4: promos[code]["expires"]=(datetime.now()+timedelta(hours=int(p[4]))).isoformat()
        save_promos(promos)
        bot.send_message(msg.chat.id, f"✅ `{code}` создан!", parse_mode="Markdown")
    except: bot.send_message(msg.chat.id, "❌ Ошибка!")

# ═══════════════════════════════════════════
# АДМИН-ПАНЕЛЬ
# ═══════════════════════════════════════════
@bot.message_handler(commands=["admin"])
def admin(msg):
    if not is_admin(msg.from_user.id): return
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
        types.InlineKeyboardButton("👥 Игроки", callback_data="admin_users"),
        types.InlineKeyboardButton("💰 Выдать валюту", callback_data="admin_give_coins"),
        types.InlineKeyboardButton("🎁 Выдать бойца", callback_data="admin_give_brawler"),
        types.InlineKeyboardButton("🎨 Выдать скин", callback_data="admin_give_skin"),
        types.InlineKeyboardButton("📢 Рассылка", callback_data="admin_broadcast"),
        types.InlineKeyboardButton("🎫 Промокоды", callback_data="admin_promos"),
        types.InlineKeyboardButton("🔄 Сброс сезона", callback_data="admin_reset_season"),
        types.InlineKeyboardButton("❌ Бан игрока", callback_data="admin_ban")
    )
    bot.send_message(msg.chat.id, "🔐 *АДМИН-ПАНЕЛЬ*", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith("admin_"))
def admin_handler(call):
    if not is_admin(call.from_user.id): return
    if call.data == "admin_stats":
        db = load_db()
        text = f"📊 Игроков: {len(db)}\n🏆 Кубков: {sum(u.get('cups',0) for u in db.values())}\n💰 Монет: {sum(u.get('coins',0) for u in db.values())}"
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    elif call.data == "admin_users":
        db = load_db()
        top20 = sorted(db.items(), key=lambda x: x[1].get("cups",0), reverse=True)[:20]
        text = "👥 *ТОП-20*\n" + "\n".join(f"{i}. ID{u}: {d['cups']}🏆" for i,(u,d) in enumerate(top20,1))
        bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    elif call.data == "admin_give_coins":
        msg = bot.send_message(call.message.chat.id, "Формат: `ID сумма`", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_give_coins)
    elif call.data == "admin_give_brawler":
        msg = bot.send_message(call.message.chat.id, "Формат: `ID Боец`")
        bot.register_next_step_handler(msg, process_give_brawler)
    elif call.data == "admin_give_skin":
        msg = bot.send_message(call.message.chat.id, "Формат: `ID Боец Скин`")
        bot.register_next_step_handler(msg, process_give_skin)
    elif call.data == "admin_broadcast":
        msg = bot.send_message(call.message.chat.id, "Текст рассылки:")
        bot.register_next_step_handler(msg, process_broadcast)
    elif call.data == "admin_promos":
        bot.send_message(call.message.chat.id, "/create_promo /promos /delete_promo КОД")
    elif call.data == "admin_reset_season":
        db = load_db()
        for uid in db: db[uid]["cups"] = 0
        save_db(db)
        bot.send_message(call.message.chat.id, "✅ Сезон сброшен!")
    elif call.data == "admin_ban":
        msg = bot.send_message(call.message.chat.id, "ID для бана:")
        bot.register_next_step_handler(msg, process_ban)

def process_give_coins(msg):
    try:
        p = msg.text.split(); uid = p[0]; amt = int(p[1])
        u = get_user(uid); u["coins"] += amt; update_user(uid, u)
        bot.send_message(msg.chat.id, f"✅ +{amt}💰")
    except: bot.send_message(msg.chat.id, "❌ Ошибка!")

def process_give_brawler(msg):
    try:
        p = msg.text.split(); uid = p[0]; name = p[1]
        if name not in ALL_BRAWLERS: bot.send_message(msg.chat.id, "❌ Не найден!"); return
        u = get_user(uid)
        if name not in u["brawlers"]: u["brawlers"].append(name); update_user(uid, u); bot.send_message(msg.chat.id, "✅ Выдан!")
        else: bot.send_message(msg.chat.id, "❌ Уже есть!")
    except: bot.send_message(msg.chat.id, "❌ Ошибка!")

def process_give_skin(msg):
    try:
        p = msg.text.split(); uid = p[0]; bn = p[1]; sn = p[2]
        u = get_user(uid)
        u.setdefault("skins",{}).setdefault(bn,[])
        if sn not in u["skins"][bn]: u["skins"][bn].append(sn); update_user(uid, u); bot.send_message(msg.chat.id, "✅ Выдан!")
        else: bot.send_message(msg.chat.id, "❌ Уже есть!")
    except: bot.send_message(msg.chat.id, "❌ Ошибка!")

def process_broadcast(msg):
    db = load_db(); sent = 0
    for uid in db:
        try: bot.send_message(int(uid), f"📢 {msg.text}"); sent += 1
        except: pass
    bot.send_message(msg.chat.id, f"✅ {sent}/{len(db)}")

def process_ban(msg):
    try:
        uid = msg.text.strip()
        db = load_db()
        if uid in db: del db[uid]; save_db(db); bot.send_message(msg.chat.id, "✅ Забанен!")
        else: bot.send_message(msg.chat.id, "❌ Не найден!")
    except: bot.send_message(msg.chat.id, "❌ Ошибка!")

@bot.message_handler(commands=["give"])
def give_cmd(msg):
    if not is_admin(msg.from_user.id): return
    try:
        parts = msg.text.split(); uid = parts[1]; cur = parts[2]; amt = int(parts[3])
        u = get_user(uid); u[cur] = u.get(cur,0) + amt; update_user(uid, u)
        bot.send_message(msg.chat.id, f"✅ {amt} {cur} → {uid}")
    except: bot.send_message(msg.chat.id, "❌ /give ID валюта кол-во")

# ═══════════════════════════════════════════
# ЗАПУСК
# ═══════════════════════════════════════════
print("""
╔══════════════════════════════════╗
║   🤖 BRAWL STARS BOT v10.0    ║
║  🎵 MP3 песни                  ║
║  📤 Отправь MP3 админу         ║
║  ▶️ /songs — плейлист          ║
║  👑 Старая админ-панель        ║
╚══════════════════════════════════╝
""")
bot.polling(none_stop=True)