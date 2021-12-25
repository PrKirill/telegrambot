from telebot import types
from settings import drinks

main = types.ReplyKeyboardMarkup(row_width=2)
main.add(
    '! cola   !',
    '! pepsi !',
    '! sprite !',
    '! pulpy !',
    '! crush !',
    '! natakhtari !',
    '! fanta !',
    '! milkis !'
)
btn5 = types.InlineKeyboardButton('Очистить корзину', callback_data='delete')
btn2 = types.InlineKeyboardButton('Назад 🔙', callback_data='back')
btn3 = types.InlineKeyboardButton('Оформить Заказ 💳', callback_data='cheque')
btn4 = types.InlineKeyboardButton('Обновить адрес и контакты', callback_data='adr')

board2 = types.InlineKeyboardMarkup(row_width=2)
board2.add(btn5,btn2)

input_adress = types.InlineKeyboardMarkup(row_width=1)
adr = types.InlineKeyboardButton('Ввести адрес', callback_data='adr')
input_adress.add(adr)

input_money = types.InlineKeyboardMarkup(row_width=1)
btn = types.InlineKeyboardButton('Переходим к оплате 💳', callback_data='pay')
input_money.add(btn, btn2, btn4, btn5)

cola = types.InlineKeyboardMarkup(row_width=2)
for btn in drinks['cocacola']:
    btn1 = types.InlineKeyboardButton(f'   {btn}', callback_data=f'{btn}:cocacola')
    cola.add(btn1)
cola.add(btn2,btn3)

pps = types.InlineKeyboardMarkup(row_width=2)
for btn in drinks['pepsicola']:
    btn1 = types.InlineKeyboardButton(f'   {btn}', callback_data=f'{btn}:pepsicola')
    pps.add(btn1)
pps.add(btn2,btn3)

sprt = types.InlineKeyboardMarkup(row_width=2)
for btn in drinks['sprite']:
    btn1 = types.InlineKeyboardButton(f'   {btn}', callback_data=f'{btn}:sprite')
    sprt.add(btn1)
sprt.add(btn2,btn3)

plp = types.InlineKeyboardMarkup(row_width=2)
for btn in drinks['pulpy']:
    btn1 = types.InlineKeyboardButton(f'   {btn}', callback_data=f'{btn}:pulpy')
    plp.add(btn1)
plp.add(btn2,btn3)

crsh = types.InlineKeyboardMarkup(row_width=2)
for btn in drinks['crush']:
    btn1 = types.InlineKeyboardButton(f'   {btn}', callback_data=f'{btn}:crush')
    crsh.add(btn1)
crsh.add(btn2, btn3)

    ##### = types.InlineKeyboardMarkup(row_width=1)
#   for btn in drinks[######]:
#      btn1 = types.InlineKeyboardButton(f'   {btn}', callback_data=f'{btn}_######')
#      #######.add()



ntkht = types.InlineKeyboardMarkup(row_width=2)
for btn in drinks['natakhtari'][0]:
    i = 1
    btn1 = types.InlineKeyboardButton(f"   {drinks['natakhtari'][0][btn]}", callback_data=f'{i}:natakhtari')
    i += 1
    ntkht.add(btn1)
ntkht.add(btn2,btn3)

fnt = types.InlineKeyboardMarkup(row_width=2)
for btn in drinks['fanta'][0]:
    i = 1
    btn1 = types.InlineKeyboardButton(f"   {drinks['fanta'][0][btn]}", callback_data=f'{i}:fanta')
    i += 1
    fnt.add(btn1)
fnt.add(btn2,btn3)

mlks = types.InlineKeyboardMarkup(row_width=2)
for btn in drinks['milkis']:
    btn1 = types.InlineKeyboardButton(f'   {btn}', callback_data=f'{btn}:milkis')
    mlks.add(btn1)
mlks.add(btn2,btn3)


