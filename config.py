import os
import re

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

SPAM_KEYWORDS = [
    "заработок",
    "пассивный доход",
    "криптовалюта",
    "быстрые деньги",
    "инвестиции",
    "доход без вложений",
    "привлекаю",
    "заработать"
]

SPAM_PATTERNS = [
    r"заработать.*без вложений",  # "заработать" и вариации
    r"пассивный доход",           # "пассивный доход"
    r"инвестиции.*биткоин",       # "инвестиции" и "биткоин"
    r"криптовалюта",              # "криптовалюта"
    r"легкие деньги",             # "легкие деньги"
    r"привлекаю",
    r"зараб",
    r"оплатой",
    r"\$",
    r"usd",
    r"в день",
    r"доход",
    r"работа",
    r"легально",
    r"кредит",
    r"работу",
    r"бизнес",
    r"темка",
    r"темку",
    r"доллар",
]

def is_spam(message_text):
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, message_text.lower()):
            return True
    return False
