import telebot

import requests

import time

import threading



# --- DATI FISSI ---

TOKEN_TG = '8496190715:AAHWYmyiwXOlV1vlu5xvRziJgmtzTeYn73M'

FIVESIM_KEY = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE4MDg4NDgxMjAsImlhdCI6MTc3NzMxMjEyMCwicmF5IjoiNTUyZmVhYjQ5YWExMGQ4YjdjM2U5OTgwMDBkZDliODMiLCJzdWIiOjQwMTExMDZ9.adxzqFGJ7wslkCI3BDW2Z-n51QKMxlIHd11YfGygGruM56nCd1ziGE_VzsieJBrVeT2_XHYizbjmZuuo2UrfzYs0N8ASqCsVuAEVari6M2AX_g0lS7q7SvDr2rld1btc7QvJF8Ji-OMsXS-Yq1aoq1m2ZPy2sB7ZbW4B3rRyjj5BNgGqrMuwjwMJvbD75t9Gvg4t7pO7-Xc7hiql7MdLIlXUWOYtQ0JK84dVQQ4XWmSk2gIqAXlFmOFscThDqUz3r0_-YIrKBVq4mciBbDtJAWzg-FTAQJcyukiFqYRydZA4oXS5shOjVuddKlIlDnNs0V7zx1ZHrf5Dmm3ap5I3-A'

LTC_ADDR = 'LgNP5eMjsZYNCXTHMSLAZkd5Wrk7xmHf2Z-' # Cambialo con il tuo!

URL_MINIAPP = 'https://tuousername.github.io/tuo-repo/' # Il link al file HTML sopra



bot = telebot.TeleBot(TOKEN_TG)



# --- LOGICA 5SIM ---

def get_num():

    url = "https://5sim.net/v1/user/buy/activation/italy/any/telegram"

    r = requests.get(url, headers={'Authorization': f'Bearer {FIVESIM_KEY}', 'Accept': 'application/json'})

    return r.json() if r.status_code == 200 else None



# --- LOGICA PAGAMENTO (BlockCypher API) ---

def check_pay(addr, val):

    r = requests.get(f"https://api.blockcypher.com/v1/ltc/main/addrs/{addr}/balance").json()

    # Verifica se il saldo finale è aumentato del valore atteso (in Satoshi)

    return r.get('final_balance', 0) >= (val * 100000000)



@bot.message_handler(commands=['start'])

def start(m):

    kb = telebot.types.InlineKeyboardMarkup()

    kb.add(telebot.types.InlineKeyboardButton("🛍️ APRI SHOP", web_app=telebot.types.WebAppInfo(url=URL_MINIAPP)))

    bot.send_message(m.chat.id, "☢️ **REDMAGIC AUTO-SHOP** ☢️\n\nClicca sotto per iniziare.", parse_mode="Markdown", reply_markup=kb)



@bot.message_handler(content_types=['web_app_data'])

def web_app_data(m):

    if m.web_app_data.data == 'tg_it':

        prezzo = 0.05

        bot.send_message(m.chat.id, f"💳 **PAGAMENTO RICHIESTO**\n\nInvia `{prezzo}` LTC a:\n`{LTC_ADDR}`\n\nVerifica in corso...", parse_mode="Markdown")

        

        # Monitoraggio silente

        threading.Thread(target=wait_for_cash, args=(m.chat.id, prezzo)).start()



def wait_for_cash(cid, amt):

    start_bal = requests.get(f"https://api.blockcypher.com/v1/ltc/main/addrs/{LTC_ADDR}/balance").json().get('final_balance', 0)

    for _ in range(40): # 20 minuti di attesa

        time.sleep(30)

        curr_bal = requests.get(f"https://api.blockcypher.com/v1/ltc/main/addrs/{LTC_ADDR}/balance").json().get('final_balance', 0)

        if curr_bal >= start_bal + (amt * 100000000):

            bot.send_message(cid, "✅ **PAGAMENTO RICEVUTO!**\nErogazione numero...")

            res = get_num()

            if res:

                bot.send_message(cid, f"📱 NUMERO: `{res['phone']}`\n\nIn attesa dell'SMS...")

                # Loop finale per SMS

                for _ in range(30):

                    time.sleep(10)

                    check = requests.get(f"https://5sim.net/v1/user/check/{res['id']}", headers={'Authorization': f'Bearer {FIVESIM_KEY}'}).json()

                    if check.get('sms'):

                        bot.send_message(cid, f"📩 **CODICE:** `{check['sms'][0]['code']}`\n\nGG Socio! 🍗")

                        return

            return

    bot.send_message(cid, "❌ Timeout. Contatta il supporto.")



bot.polling()
