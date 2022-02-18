import telebot
import json, os

api_key_file = open(os.path.join(os.getcwd(), 'credentials', 'api_key.json'))
api_key = json.load(api_key_file)["key"]
bot = telebot.TeleBot(api_key, parse_mode=None)

incident_report = {
    "nature_of_incident": "",
    "description": "",
    "status_update": "",
    "date_time": "",
    "location": "",
    "coy_dept": "",
    "follow_up": "",
    "verbal_report": "",
    "written_report": "",
    "reported_by": "",
    "travel_history": "",
    "close_contact": "",
    "dormitory": "",
    "high_risk_area": "",
    "prolong_ari_with_fever": "",
    "pnuemonia": ""
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # bot.reply_to(message, "Howdy, how are you doing?")
    welcome_message = "Welcome to 30SCE Incident Report Bot. \n\nTo start type `/report`."
    bot.send_message(message.chat.id, welcome_message, parse_mode="Markdown")


@bot.message_handler(commands=['report'])
def report(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('New Incident Report', 'Update Incident Report')
    reply = bot.send_message(
        message.chat.id, "What would you like to do?", reply_markup=markup)
    bot.register_next_step_handler(reply, start_handler)


def start_handler(message):
    if message.text == 'New Incident Report':
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Non-Training Related', 'Training Related')
        reply = bot.send_message(
            message.chat.id, "1. Nature of incident", reply_markup=markup)
        bot.register_next_step_handler(reply, description_handler)
    elif message.text == 'Update Incident Report':
        bot.reply_to(message, "This feature is not yet available")


def description_handler(message):
    incident_report["nature_of_incident"] = message.text
    reply = bot.send_message(message.chat.id, "2. Description of incident")
    bot.register_next_step_handler(reply, status_update_handler)


def status_update_handler(message):
    incident_report["description"] = message.text
    reply = bot.send_message(message.chat.id, "3. Status Update")
    bot.register_next_step_handler(reply, date_time_handler)


def date_time_handler(message):
    incident_report["status_update"] = message.text
    reply = bot.send_message(message.chat.id, "4. Date / Time of incident")
    bot.register_next_step_handler(reply, location_handler)


def location_handler(message):
    incident_report["date_time"] = message.text
    reply = bot.send_message(message.chat.id, "5. Location of incident")
    bot.register_next_step_handler(reply, coy_dept_handler)


def coy_dept_handler(message):
    incident_report["location"] = message.text
    reply = bot.send_message(message.chat.id, "6. Coy/Dept involved:")
    bot.register_next_step_handler(reply, follow_up_handler)

def follow_up_handler(message):
    incident_report["coy_dept"] = message.text
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Yes', 'No')
    bot.send_message(message.chat.id, "7. Follow-up action")
    reply = bot.send_message(
        message.chat.id, "Informed NOK?", reply_markup=markup)
    bot.register_next_step_handler(reply, verbal_report_handler)


def verbal_report_handler(message):
    incident_report["follow_up_action"] = message.text
    reply = bot.send_message(
        message.chat.id, "8. Date/Time of verbal report to GSOC/HQ 3DIV/ HQSCE:")
    bot.register_next_step_handler(reply, written_report_handler)


def written_report_handler(message):
    incident_report["verbal_report"] = message.text
    reply = bot.send_message(
        message.chat.id, "9. Date/Time of written report to GSOC/HQ 3DIV/ HQSCE:")
    bot.register_next_step_handler(reply, reported_by_handler)


def reported_by_handler(message):
    incident_report["written_report"] = message.text
    reply = bot.send_message(message.chat.id, "10. Reported by")
    bot.register_next_step_handler(reply, travel_history_handler)


def travel_history_handler(message):
    incident_report["reported_by"] = message.text
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Yes', 'No')
    reply = bot.send_message(
        message.chat.id, "Travel history for 14 days?", reply_markup=markup)
    bot.register_next_step_handler(reply, close_contact_handler)


def close_contact_handler(message):
    incident_report["travel_history"] = message.text
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Yes', 'No')
    reply = bot.send_message(
        message.chat.id, "Close contact with confirmed COVID-19 case?", reply_markup=markup)
    bot.register_next_step_handler(reply, dormitory_handler)


def dormitory_handler(message):
    incident_report["close_contact"] = message.text
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Yes', 'No')
    reply = bot.send_message(
        message.chat.id, "Did he/she stay in foreign worker dormitory", reply_markup=markup)
    bot.register_next_step_handler(reply, high_risk_area_handler)


def high_risk_area_handler(message):
    incident_report["dormitory"] = message.text
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Yes', 'No')
    reply = bot.send_message(
        message.chat.id, "Did he/she work in a high risk area?", reply_markup=markup)
    bot.register_next_step_handler(reply, prolong_ari_with_fever_handler)


def prolong_ari_with_fever_handler(message):
    incident_report["high_risk_area"] = message.text
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Yes', 'No')
    reply = bot.send_message(
        message.chat.id, "Prolonged ARI for more than 4 days with fever more than 37.5 degrees?", reply_markup=markup)
    bot.register_next_step_handler(reply, pnuemonia_handler)


def pnuemonia_handler(message):
    incident_report["prolong_ari"] = message.text
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Yes', 'No')
    reply = bot.send_message(
        message.chat.id, "Pneumonia?", reply_markup=markup)
    bot.register_next_step_handler(reply, generate_report)


def generate_report(message):
    incident_report["pnuemonia"] = message.text
    incident_report_text = f"*NEW*\n\n*1) Nature of incident:*\n{incident_report['nature_of_incident']}\n\n*2) Brief description:*\n{incident_report['description']}\n\n*3) Status Update:*\n{incident_report['status_update']}\n\n*4) Date/Time of incident:*\n{incident_report['date_time']}\n\n*5) Location of incident:*\n{incident_report['location']}\n\n*6) Coy/Dept involved:*\n{incident_report['coy_dept']}\n\n*7) Follow-up action:*\n-Informed NOK? *{incident_report['follow_up_action']}*\n\n*8) Date/Time of verbal report to GSOC/HQ 3DIV/ HQSCE:*\n{incident_report['verbal_report']}\n\n*9) Date/Time of written report to GSOC/HQ 3DIV/ HQSCE:*\n{incident_report['written_report']}\n\n*10) Reported by:*\n{incident_report['reported_by']}\n\n*Travel history for 14 days?*\n{incident_report['travel_history']}\n\n*Close contact with confirmed COVID-19 case?:*\n{incident_report['close_contact']}\n\n*Did he/she stay in foreign worker dormitory?*\n{incident_report['dormitory']}\n\n*Did he/she work in a high risk area?*\n{incident_report['high_risk_area']}\n\n*Prolonged ARI for more than 4 days with fever more than 37.5 degrees?*\n{incident_report['prolong_ari']}\n\n*Pneumonia?*\n{incident_report['pnuemonia']}"
    bot.send_message(message.chat.id, 
                    "Generating report...",
                     parse_mode="Markdown")
    bot.send_message(message.chat.id, 
                    incident_report_text,
                     parse_mode="Markdown")

bot.infinity_polling()