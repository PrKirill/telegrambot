import sqlite3
import os
import telebot
from telebot import types
import settings
import keyboards as kb
import func

bot = telebot.TeleBot(settings.api_tg)

try:
    @bot.message_handler(commands=['stats'])
    def stats_func(message):
        if message.from_user.id == settings.my_id:
            conn = sqlite3.connect('db.db')
            q = conn.cursor()
            q = q.execute('SELECT COUNT(*) FROM adresses').fetchone()
            bot.send_message(settings.my_id,f'Всего в боте {q[0]} пользователей')


    @bot.message_handler(commands=['stop'])
    def stats_func(message):
        if message.from_user.id == settings.my_id:
            bot.send_message(settings.my_id, 'Бот выключен.')
            os._exit(0)


    @bot.message_handler(commands=['start'])
    def start_func(message):
        id = message.from_user.id
        if func.get_adr(id) == None:
            print(f'new /start user:{id}')
            bot.send_message(settings.my_id,f'new /start user:{id}')
            bot.send_message(id,'Привет! Так как ты у нас новенький, для покупки нужно уточнить твой адрес\n ⬇️ (кнопка внизу)\n Затем нажми /start, чтобы начать закупаться)', reply_markup=kb.input_adress)
            bot.send_message(id,'Твой адрес: ', {func.get_adr(call.from_user.id)})
        else:
            id = message.from_user.id
            nick = message.from_user.first_name
            bot.send_message(id,f'С возвращением, {nick}!\n выбирай напиток и делай заказ (от двух позиций)\n➖➖➖➖➖➖➖➖➖➖➖\n ☑️ <strong>Актуальный каталог</strong> ☑️\n➖➖➖➖➖➖➖➖➖➖➖\ncola XXL -{settings.cocacola_cost}р\npepsi -{settings.pepsicola_cost}р\nsprite -{settings.sprite_cost}р\nfanta -{settings.fanta_cost}р\ncrush -{settings.crush_cost}р\nnatakhtari -{settings.natakhtari_cost}р\nmilkis -{settings.milkis_cost}р\npulpy -{settings.pulpy_cost}р',reply_markup=kb.main, parse_mode='HTML')
            if func.info_user(id) == 'new':
                func.first_join(id)

    @bot.message_handler(content_types=['text'])
    def start_text(message):
        id = message.from_user.id
        if func.get_adr(id) == None:
            bot.send_message(id, 'Для покупки нужно уточнить адрес для доставки!', reply_markup=kb.adr)
        else:
            id = message.from_user.id
            if message.text == '! cola   !':
                bot.send_message(id, 'Выбери вкус:', reply_markup=kb.cola)
            elif message.text == '! pepsi !':
                bot.send_message(id, 'Выбери вкус:', reply_markup=kb.pps)
            elif message.text == '! sprite !':
                bot.send_message(id, 'Выбери вкус:', reply_markup=kb.sprt)
            elif message.text == '! pulpy !':
                bot.send_message(id, 'Выбери вкус:', reply_markup=kb.plp)
            elif message.text == '! crush !':
                bot.send_message(id, 'Выбери вкус:', reply_markup=kb.crsh)
            elif message.text == '! natakhtari !':
                bot.send_message(id, 'Выбери вкус:', reply_markup=kb.ntkht)
            elif message.text == '! fanta !':
                bot.send_message(id, 'Выбери вкус:', reply_markup=kb.fnt)
            elif message.text == '! milkis !':
                bot.send_message(id, 'Выбери вкус:', reply_markup=kb.mlks)
            else:
                bot.send_message(id, 'Я, Вас, не понимаю!')

    @bot.callback_query_handler(func=lambda call:True)
    def start_call(call):
        id = call.from_user.id
        data = call.data
        if call.data == 'cheque':
            if func.total_cheque(id)[1] >= 2:
                bot.send_message(id, f'Сумма заказа: {func.total_cheque(id)[0]}\n'+ func.include(id)+'\nПроверьте адрес и номер телефона:\n'+func.get_adr(id), reply_markup=kb.input_money, parse_mode='HTML')
            else:
                bot.send_message(id, f'Сумма заказа:{func.total_cheque(id)[0]}\n' + func.include(id)+'<strong>Заказ от двух товаров!</strong>', reply_markup=kb.board2, parse_mode='HTML')


        elif call.data == 'pay':
            func.create_order(call.from_user.id)
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton('Ссылка на оплату', url=func.return_qiwi_link(call.from_user.id))
            button2 = types.InlineKeyboardButton('Проверить оплату', callback_data='check_payment')
            keyboard.add(button,button2)
            bot.send_message(id,'<strong>КОММЕНТАРИЙ НЕ ИЗМЕНЯТЬ!!!</strong>',reply_markup=keyboard, parse_mode='HTML')


        elif call.data == 'check_payment':
            id = call.from_user.id
            if func.check_payment(id) == None:
#                  sum = int(func.total_cheque(id)[1]) * 0.8
                   bot.send_message(id,'Оплата принята! По вопросам доставки обращайтесь к саппорту - @userfiles')
#                  func.pay_seller(sum)
                   bot.send_message(settings.my_id, f'Новый заказ oт {call.from_user.id}:\n' + func.include(call.from_user.id) + f' Адрес: {func.get_adr(call.from_user.id)}')
#                  bot.send_message(settings.seller_id, f'Новый заказ oт {call.from_user.id}:\n' + func.include(call.from_user.id) + f' Адрес: {func.get_adr(call.from_user.id)}')
                   func.reset_cart(id)
                   func.delete_code(id)
            else:
                bot.send_message(id,'Oплата не найдена!')


        elif call.data == 'adr':
            msg = bot.send_message(id,'Введите адрес, для доставки: улица, дом, подъезд, квартира, этаж, код от домофона, номер телефона ')
            bot.register_next_step_handler(msg, func.insert_adr)

        elif call.data == 'back':
            bot.send_message(call.from_user.id,'Главное Меню',reply_markup=kb.main)

        elif call.data == 'delete':
            func.reset_cart(id)
            bot.send_message(id,'Корзина очищена.')

        else:
            data = call.data
            id = call.from_user.id
            func.separator(data,id)
            bot.answer_callback_query(callback_query_id=call.id,text='Товар добавлен в корзину.', show_alert=True,)
    bot.polling(none_stop=True)
except Exception as e:
    print(e)
    bot.polling(none_stop=True)