import telebot

import requests

import time

import threading



# --- CONFIGURAZIONE ---

TOKEN_TG = '8496190715:AAHWYmyiwXOlV1vlu5xvRziJgmtzTeYn73M'

FIVESIM_KEY = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE4MDg4NDgxMjAsImlhdCI6MTc3NzMxMjEyMCwicmF5IjoiNTUyZmVhYjQ5YWExMGQ4YjdjM2U5OTgwMDBkZDliODMiLCJzdWIiOjQwMTExMDZ9.adxzqFGJ7wslkCI3BDW2Z-n51QKMxlIHd11YfGygGruM56nCd1ziGE_VzsieJBrVeT2_XHYizbjmZuuo2UrfzYs0N8ASqCsVuAEVari6M2AX_g0lS7q7SvDr2rld1btc7QvJF8Ji-OMsXS-Yq1aoq1m2ZPy2sB7ZbW4B3rRyjj5BNgGqrMuwjwMJvbD75t9Gvg4t7pO7-Xc7hiql7MdLIlXUWOYtQ0JK84dVQQ4XWmSk2gIqAXlFmOFscThDqUz3r0_-YIrKBVq4mciBbDtJAWzg-FTAQJcyukiFqYRydZA4oXS5shOjVuddKlIlDnNs0V7zx1ZHrf5Dmm3ap5I3-A'

LTC_ADDR = 'LgNP5eMjsZYNCXTHMSLAZkd5Wrk7xmHf2Z'



bot = telebot.TeleBot(TOKEN_TG)



def buy_number(service):

    # Mapping prodotti

    prod = 'telegram' if 'tg' in service else 'whatsapp'

    url = f"https://5sim.net/v1/user/buy/activation/italy/any/{prod}"

    r = requests.get(url, headers={'Authorization': f'Bearer {FIVESIM_KEY}', 'Accept': 'application/json'})

    return r.json() if r.status_code == 200 else None



@bot.message_handler(commands=['start'])

def start(m):

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn = telebot.types.KeyboardButton("🛍️ APRI REDMAGIC SHOP", web_app=telebot.types.WebAppInfo(url="https://TUOUSER.github.io/REPO/"))

    markup.add(btn)

    bot.send_message(m.chat.id, "🚀 **SISTEMA OPERATIVO**\n\nUsa il tasto sotto per ordinare dal tuo RedMagic.", parse_mode="Markdown", reply_markup=markup)



@bot.message_handler(content_types=['web_app_data'])

def handle_app_data(m):

    service = m.web_app_data.data

    prezzo = 0.05 if service == 'tg_it' else 0.06

    

    bot.send_message(m.chat.id, f"💎 **ORDINE RICEVUTO: {service.upper()}**\n\nInvia `{prezzo}` LTC qui:\n`{LTC_ADDR}`\n\nSto monitorando la blockchain...", parse_mode="Markdown")

    

    # Avviamo il monitoraggio (Simulato per test, poi metti BlockCypher come prima)

    threading.Thread(target=wait_and_deliver, args=(m.chat.id, service)).start()



def wait_and_deliver(cid, service):

    time.sleep(10) # Simuliamo l'attesa pagamento per il test

    bot.send_message(cid, "✅ **PAGAMENTO RILEVATO!** Genero il numero...")

    res = buy_number(service)

    if res:

        bot.send_message(cid, f"📱 **NUMERO:** `{res['phone']}`\n\nAttendo l'SMS...")

        # Loop check SMS (come prima)

    else:

        bot.send_message(cid, "❌ Errore API o Saldo. Controlla il Vaio.")



bot.polling()
