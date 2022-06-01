#!/usr/bin/env python
# coding: utf-8

# In[8]:


import logging
import telegram
from flask import Flask
from telegram import (
    Bot,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup, 
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)
app = Flask(__name__)
bot = telegram.Bot(token='1716788813:AAGYz2QenmyxCioRclXzKsCdPw-8qiwXHtg')
updater = Updater(token='1716788813:AAGYz2QenmyxCioRclXzKsCdPw-8qiwXHtg', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
times = 0
score = 0
fullmark = 0
money = 0

logger = logging.getLogger(__name__)

# Stages
FIRST, SECOND,AGETOJOB,JOBTOONE,Q3, MONEY_ONE, MONEY_TWO, MONEY_THREE, FOUR_THREE_TWO, FIVESC = range(10)

def start(update: Update, context: CallbackContext) -> int:
    global score
    global times
    global money
    global fullmark
    fullmark = 0
    score = 0
    times = 0
    money = 0
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    keyboard = [
        [
            InlineKeyboardButton("開始吧", callback_data='ONE'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('💁‍♂️ 嗨！我是野村理財小幫手，跟我聊天就可以得到適合你的投資組合喔，點下"開始吧" 即可開始囉', reply_markup=reply_markup)
    return FIRST

def age(update, context) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="請問您的年齡(請輸入數字):")
#     context.bot.send_message(chat_id=update.effective_chat.id, text="請問您的年齡(請輸入數字):")
    return AGETOJOB

def agetojob(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    try:
        age = int(update.message.text)
        logger.info("user %s age: %s:", user.first_name, update.message.text)
        return job(update, context)
    except ValueError:
        update.message.reply_text('請輸入整數')
        return AGETOJOB

def job(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [
        ['學生', '餐飲旅遊', '醫療'],
        ['藝文/媒體/傳播','軍公教','金融業'],
        ['服務業','自由業','製造業','資訊/科技']
                     ]

    update.message.reply_text('請問您的職業類別',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                             )
    return JOBTOONE

def jobtoone(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("user %s job: %s:", user.first_name, update.message.text)
    return one(update, CallbackContext)
def one(update: Update, context: CallbackContext) -> int:
    global fullmark
    fullmark += 10
    keyboard = [
        [
            InlineKeyboardButton("創業基金", callback_data='10'),
            InlineKeyboardButton("購屋準備", callback_data='8'),
            InlineKeyboardButton("教育基金", callback_data='6'),
        ],
        [
            InlineKeyboardButton("結婚準備", callback_data='6'),
            InlineKeyboardButton("購車準備", callback_data='8'),
            InlineKeyboardButton("退休基金", callback_data='2'),
        ],
        [
            InlineKeyboardButton("就是想存錢", callback_data='5'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("您的月收入大約為(單位:新台幣)", reply_markup=reply_markup)
    return SECOND

def two(update: Update, context: CallbackContext) -> int:
    global fullmark
    fullmark += 20
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("0-1年", callback_data='10'),
            InlineKeyboardButton("1-2年", callback_data='10'),
            InlineKeyboardButton("2-3年", callback_data='15'),
        ],
        [
            InlineKeyboardButton("3-4年", callback_data='15'),
            InlineKeyboardButton("4-5年", callback_data='20'),
            InlineKeyboardButton("5年以上", callback_data='20'),
        ],
        [
            InlineKeyboardButton("無投資經驗", callback_data='5'),
        ]
        
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="請問您大約有多少年的投資經驗?", reply_markup=reply_markup
    )
    return SECOND


def three(update: Update, context: CallbackContext) -> int:
    global fullmark
    fullmark += 5
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("一筆錢一次投入", callback_data='一筆錢'),
        ],
        [
            InlineKeyboardButton("每個月定期定額投資", callback_data='每月'),
        ],
        [
            InlineKeyboardButton("一筆錢一次投入，搭配每個月定期定額投資", callback_data='一筆加每月'),
        ]
        
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="預計的投資方式", reply_markup=reply_markup
    )
    
    return SECOND

def four_one(update, context) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="您預計投入的金額(單位:新台幣):")
#     context.bot.send_message(chat_id=update.effective_chat.id, text="您預計投入的金額(單位:新台幣):")
    return MONEY_ONE
def money_one(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    try:
        money = int(update.message.text)
        logger.info("investment: %s", update.message.text)
#         update.message.reply_text(update.message.text)
        return button(update, CallbackContext)
    except ValueError:
        update.message.reply_text('請輸入整數')
        return MONEY_ONE

def four_two(update, context) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="您每月定期定額預計投入的金額(單位:新台幣):")
#     context.bot.send_message(chat_id=update.effective_chat.id, text="您每月定期定額預計投入的金額(單位:新台幣):")
    return MONEY_TWO
def money_two(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    global money
    try:
        money = int(update.message.text)
        logger.info("investment: %s", update.message.text)
#         update.message.reply_text(money)
        return button(update, CallbackContext)
    except ValueError:
        update.message.reply_text('請輸入整數')
        return MONEY_TWO
def four_three_one(update, context) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="您預計一筆錢一次投入的金額(單位:新台幣):")
#     context.bot.send_message(chat_id=update.effective_chat.id, text="您預計一筆錢一次投入的金額(單位:新台幣):")
    return FOUR_THREE_TWO
def four_three_two(update, context) -> int:
    user = update.message.from_user
    try:
        money = int(update.message.text)
        logger.info("first investment: %s", update.message.text)
#         update.message.reply_text(update.message.text)
        context.bot.send_message(chat_id=update.effective_chat.id, text="您預計每月定期定額投入的金額(單位:新台幣):")
        return MONEY_THREE
    except ValueError:
        update.message.reply_text('請輸入整數')
        return FOUR_THREE_TWO
def money_three(update, context) -> int:
    user = update.message.from_user
    try:
        money = int(update.message.text)
        logger.info("every month: %s", update.message.text)
#         update.message.reply_text(update.message.text)
        return button(update, CallbackContext)
    except ValueError:
        update.message.reply_text('請輸入整數')
        return MONEY_THREE
    
def five(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [
            InlineKeyboardButton("0-2萬", callback_data='10000'),
            InlineKeyboardButton("2-4萬", callback_data='30000'),
            InlineKeyboardButton("4-6萬", callback_data='50000'),
        ],
        [
            InlineKeyboardButton("6-8萬", callback_data='70000'),
            InlineKeyboardButton("8-10萬", callback_data='90000'),
            InlineKeyboardButton("10萬以上", callback_data='100000'),
        ],
    ]
    AttributeError
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("您的月收入大約為(單位:新台幣)", reply_markup=reply_markup)
    if money == 0:
        return SECOND
    return FIVESC
        
def fivescore(update: Update, context: CallbackContext) -> int:
    global money
    global score
    global fullmark
    fullmark += 20
    query = update.callback_query
    
    proportion = money / int(query.data)
    logger.info("revenue %s ", query.data)
    logger.info("investment/revenue : %s", proportion)
    if proportion < 0.2:
        score += 5
        return button(update, context)
    elif 0.2 <= proportion < 0.4:
        score += 10
        return button(update, context)
    elif 0.4 <= proportion < 0.6:
        score += 15
        return button(update, context)
    elif proportion >= 0.6:
        score += 20
        return button(update, context)
    
    return button(update, context)
def six(update: Update, context: CallbackContext) -> int:
    global fullmark
    fullmark += 10
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("薪資收入", callback_data='7'),
            InlineKeyboardButton("退休金", callback_data='4'),
            InlineKeyboardButton("遺產繼承收入", callback_data='10'),
        ],
        [
            InlineKeyboardButton("投資理財", callback_data='7'),
            InlineKeyboardButton("其他", callback_data='7'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="投資資金的主要來源", reply_markup=reply_markup
    )
    return SECOND


def seven(update: Update, context: CallbackContext) -> int:
    global fullmark
    fullmark += 15
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1-2年", callback_data='3'),
            InlineKeyboardButton("3-4年", callback_data='6'),
            InlineKeyboardButton("5-6年", callback_data='9'),
        ],
        [
            InlineKeyboardButton("7-8年", callback_data='12'),
            InlineKeyboardButton("9-10年", callback_data='15'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="希望在多少時間內達到您的目標", reply_markup=reply_markup
    )
    return SECOND


def eight(update: Update, context: CallbackContext) -> int:
    global fullmark
    fullmark += 30
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("9100 - 12000 (-9% ~ 20%)", callback_data='4.5'),
        ],
        [
            InlineKeyboardButton("8800 - 12500 (-12% ~ 25%)", callback_data='7.5'),
        ],
        [
            InlineKeyboardButton("8500 - 13000 (-15% ~ 30%)", callback_data='15'),
        ],
        [
            InlineKeyboardButton("8100 - 13600 (-19% ~ 36%)", callback_data='22.5'),
        ],
        [
            InlineKeyboardButton("7600 - 14200 (-24% ~ 42%)", callback_data='30'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="假設您年初申購了一10000元的基金，一年內您能接受的淨值變動範圍？", reply_markup=reply_markup
    )
    return SECOND
def nine(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("財經M平方", callback_data='財經M平方')],
        [InlineKeyboardButton("市場先生(Mr.Market)", callback_data='市場先生(Mr.Market)')],
        [InlineKeyboardButton("股魚", callback_data='股魚')],
        [InlineKeyboardButton("商業週刊", callback_data='商業週刊')],
        [InlineKeyboardButton("天下雜誌", callback_data='天下雜誌')],
        [InlineKeyboardButton("鉅亨網", callback_data='鉅亨網')],
        [InlineKeyboardButton("以上皆無", callback_data='以上皆無')],
        [InlineKeyboardButton("其他", callback_data='其他')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="您是否有訂閱或追蹤以下任何財經周刊/ 平台", reply_markup=reply_markup
    )
    return SECOND
def end(update: Update, context: CallbackContext) -> int:
    global score
    global fullmark
    query = update.callback_query
    pic1 = 'https://i.ibb.co/yF0Yb87/image.jpg'
    pic2 = 'https://i.ibb.co/hgxW1Pr/image.jpg'
    pic3 = 'https://i.ibb.co/YTktmvm/image.jpg'
    pic4 = 'https://i.ibb.co/dQgwPWq/image.jpg'
    pic5 = 'https://i.ibb.co/jk63qjg/image.jpg'

    if fullmark != 110:
        logger.info("total score: %s", score)
        score *= 1.25
        logger.info("total score * 1.25: %s", score)
    if score < 41:
        bot.send_message(chat_id=update.effective_chat.id, text="💁‍♂️ 您屬於 保守型 的投資人，代表您個性較穩重，期待投資能夠盡量保本並有穩定的回報，不輕易嘗試波動較大的金融投資工具。\n\n我們提供您的投組建議如下圖")
        bot.send_photo(chat_id=update.effective_chat.id,photo=pic1)
        bot.send_message(chat_id=update.effective_chat.id, text="我們建議保守型的投資人在股票型基金與債券型基金採用以下的比重：\n💡 股票型基金40%\n股票型基金: 主要將資金投入於股票市場上的基金，可投資於各種類型的股票，其流動性高，報酬高，但風險也大，主要目的為賺取資本利得\n\n💡 債券型基金60%\n債券型基金: 主要投資於公司債及政府公債。投資債券的報酬包括利息收入和債券價差，因此利率的變動會影響債券價格。由於債券型基金有固定的利息收益，所以基金的波動不致太過劇烈。\n\n👉 為何要用股債配置？股票和債券的相關性低，不易出現同時下跌的情況，可以幫您進一步分散風險！而其中股票型基金的產業比重如下圖")
        bot.send_photo(chat_id=update.effective_chat.id,photo=pic5)
        bot.send_message(chat_id=update.effective_chat.id, text="看完我們建議的結果有沒有心動了呢? 這邊為我們搭配出最適合您的基金介紹\n\n💰 野村成長基金: 彈性持股 - 網羅權值股與中小型股的菁華，投資組合高彈性\nhttps://www.nomurafunds.com.tw/Web/Content/#/primary/fund/fund-list/introduction?groupId=EE1765BE-D782-4AEF-96FA-4C6970DAAD3E\n\n💰野村環球基金: 全球佈局，減少投資單一國家之風險，以優質成長策略為投資主軸，挑選具成長性之優質企業，掌握中長期投資契機\nhttps://www.nomurafunds.com.tw/Web/Content/#/primary/fund/fund-list/introduction?groupId=741E7108-25A5-48A1-875A-E069E125EDF4\n\n想要了解更多野村的專業基金嗎? 我們也貼心地為您準備了我們的基金清單\n👉 https://www.nomurafunds.com.tw/Web/Content/#/primary/fund/fund-list")
    elif 40 < score < 61:
        bot.send_message(chat_id=update.effective_chat.id, text="💁‍♂️ 您屬於 穩健型 的投資人 代表您願意承受部分風險，追求資產能有成長的機會，但每當作一個決策時，必定會慎重評估其可能隱含的損失風險，風險承受度適中。建議可以多吸收各種投資理財或新金融商品的相關知識，以利在不同的經濟景氣循環下選擇適當的金融投資工具，達成理財目標。\n\n我們提供您的投組建議如下圖")
        bot.send_photo(chat_id=update.effective_chat.id,photo=pic2)
        bot.send_message(chat_id=update.effective_chat.id, text="我們提供您的投組建議為\n💡 股票型基金50%\n股票型基金: 主要將資金投入於股票市場上的基金，可投資於各種類型的股票，其流動性高，報酬高，但風險也大，主要目的為賺取資本利得\n\n💡 債券型基金50%\n債券型基金: 主要投資於公司債及政府公債。投資債券的報酬包括利息收入和債券價差，因此利率的變動會影響債券價格。由於債券型基金有固定的利息收益，所以基金的波動不致太過劇烈。\n\n👉 為何要用股債配置？股票和債券的相關性低，不易出現同時下跌的情況，可以幫您進一步分散風險！而其中股票型基金的產業比重如下圖")
        bot.send_photo(chat_id=update.effective_chat.id,photo=pic5)
        bot.send_message(chat_id=update.effective_chat.id, text="看完我們建議的結果有沒有心動了呢? 這邊為我們搭配出最適合您的基金介紹\n\n💰 野村成長基金: 彈性持股 - 網羅權值股與中小型股的菁華，投資組合高彈性\nhttps://www.nomurafunds.com.tw/Web/Content/#/primary/fund/fund-list/introduction?groupId=EE1765BE-D782-4AEF-96FA-4C6970DAAD3E\n\n💰野村環球基金: 全球佈局，減少投資單一國家之風險，以優質成長策略為投資主軸，挑選具成長性之優質企業，掌握中長期投資契機\nhttps://www.nomurafunds.com.tw/Web/Content/#/primary/fund/fund-list/introduction?groupId=741E7108-25A5-48A1-875A-E069E125EDF4\n\n想要了解更多野村的專業基金嗎? 我們也貼心地為您準備了我們的基金清單\n👉 https://www.nomurafunds.com.tw/Web/Content/#/primary/fund/fund-list")
    elif 60 < score < 81:
        bot.send_message(chat_id=update.effective_chat.id, text="💁‍♂️ 您屬於 成長型 的投資人，代表您願意承受稍高的風險，以獲取較高的報酬，個性較為積極主動，生活中願意嘗試新鮮的事物，對理財相關的產品接受度較高\n\n我們提供您的投組建議如下圖")
        bot.send_photo(chat_id=update.effective_chat.id,photo=pic3)
        bot.send_message(chat_id=update.effective_chat.id, text="我們提供您的投組建議為\n💡 股票型基金60%\n股票型基金: 主要將資金投入於股票市場上的基金，可投資於各種類型的股票，其流動性高，報酬高，但風險也大，主要目的為賺取資本利得\n\n💡 債券型基金40%\n債券型基金: 主要投資於公司債及政府公債。投資債券的報酬包括利息收入和債券價差，因此利率的變動會影響債券價格。由於債券型基金有固定的利息收益，所以基金的波動不致太過劇烈。\n\n👉 為何要用股債配置？\n股票和債券的相關性低，不易出現同時下跌的情況，可以幫您進一步分散風險！其中股票型基金的產業比重如下圖")
        bot.send_photo(chat_id=update.effective_chat.id,photo=pic5)
        bot.send_message(chat_id=update.effective_chat.id, text="看完我們建議的結果有沒有心動了呢? 這邊為我們搭配出最適合您的基金介紹\n\n💰 野村成長基金: 彈性持股 - 網羅權值股與中小型股的菁華，投資組合高彈性\nhttps://www.nomurafunds.com.tw/Web/Content/#/primary/fund/fund-list/introduction?groupId=EE1765BE-D782-4AEF-96FA-4C6970DAAD3E\n\n💰野村環球基金: 全球佈局，減少投資單一國家之風險，以優質成長策略為投資主軸，挑選具成長性之優質企業，掌握中長期投資契機\nhttps://www.nomurafunds.com.tw/Web/Content/#/primary/fund/fund-list/introduction?groupId=741E7108-25A5-48A1-875A-E069E125EDF4\n\n想要了解更多野村的專業基金嗎? 我們也貼心地為您準備了我們的基金清單\n👉 https://www.nomurafunds.com.tw/Web/Content/#/primary/fund/fund-list")                         
    elif 80 < score:
        bot.send_message(chat_id=update.effective_chat.id, text="💁‍♂️  您屬於 積極型 的投資人，代表您較勇於嘗試新觀念新方法新事物，也願意利用風險較高或是新推出的金融商品作為投資工具，來獲取較高的報酬，屬於行為積極的理財投資者，具有較高的投資風險容忍度。\n\n我們提供您的投組建議如下圖")
        bot.send_photo(chat_id=update.effective_chat.id,photo=pic4)
        bot.send_message(chat_id=update.effective_chat.id, text="我們提供您的投組建議為\n💡 股票型基金70%\n股票型基金: 主要將資金投入於股票市場上的基金，可投資於各種類型的股票，其流動性高，報酬高，但風險也大，主要目的為賺取資本利得\n\n💡 債券型基金30%\n債券型基金: 主要投資於公司債及政府公債。投資債券的報酬包括利息收入和債券價差，因此利率的變動會影響債券價格。由於債券型基金有固定的利息收益，所以基金的波動不致太過劇烈。\n\n👉 為何要用股債配置？\n股票和債券的相關性低，不易出現同時下跌的情況，可以幫您進一步分散風險！其中股票型基金的產業比重如下圖")
        bot.send_photo(chat_id=update.effective_chat.id,photo=pic5)
        bot.send_message(chat_id=update.effective_chat.id, text="看完我們建議的結果有沒有心動了呢? 這邊為我們搭配出最適合您的基金介紹\n\n💰 野村成長基金: 彈性持股 - 網羅權值股與中小型股的菁華，投資組合高彈性\nhttps://www.nomurafunds.com.tw/Web/Content/#/primary/fund/fund-list/introduction?groupId=EE1765BE-D782-4AEF-96FA-4C6970DAAD3E\n\n💰野村鴻運基金: 本基金篩選未來營收、獲利具爆發力之個股為目標，追求台股成長機會\nhttps://www.nomurafunds.com.tw/Web/Content/#/primary/fund/fund-list/introduction?groupId=741E7108-25A5-48A1-875A-E069E125EDF4\n\n想要了解更多野村的專業基金嗎? 我們也貼心地為您準備了我們的基金清單\n👉 https://www.nomurafunds.com.tw/Web/Content/#/primary/fund/fund-list")
#     query.edit_message_text(text="See you next time!")
    return ConversationHandler.END

def button(update: Update, context: CallbackContext) -> int:
    global times
    global score
    times += 1 #進這個def一次times就加一(為了要跳題)
    if times == 3:
        query = update.callback_query
        logger.info("invest method: %s", query.data)
        if query.data =='一筆錢':
            score += 3
            logger.info("total score: %s", score)
            return four_one(update, context)
        elif query.data == '每月':
            score += 5
            logger.info("total score: %s", score)
            return four_two(update, context)
        elif query.data == '一筆加每月':
            score += 5
            logger.info("total score: %s", score)
            return four_three_one(update, context)
    if times == 4 :
        return five(update, CallbackContext)
    if times == 5:
        logger.info("total score: %s", score)
        return six(update, CallbackContext)
    if times == 9:
        query = update.callback_query
        logger.info("subscrip: %s", query.data)
        return end(update, CallbackContext)
    query = update.callback_query
    query.answer()
    score += float(query.data)
    logger.info("total score: %s", score)
    
    if times == 0:
        return one(update, CallbackContext)
    elif times == 1:
        return two(update, CallbackContext)
    elif times == 2 :
        return three(update, CallbackContext)
    elif times == 3 :
        return four(update, context)
    elif times == 4 :
        return five(update, CallbackContext)
    elif times == 5 :
        return six(update, CallbackContext)
    elif times == 6 :
        return seven(update, CallbackContext)
    elif times == 7 :
        return eight(update, CallbackContext)
    elif times == 8 :
        return nine(update, CallbackContext)
    elif times == 9 :
        return end(update, CallbackContext)


def main() -> None:
#     # Create the Updater and pass it your bot's token.
#     updater = Updater("1716788813:AAGYz2QenmyxCioRclXzKsCdPw-8qiwXHtg")
#     bot = telegram.Bot(token='1716788813:AAGYz2QenmyxCioRclXzKsCdPw-8qiwXHtg')
#     # Get the dispatcher to register handlers
#     dispatcher = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [CallbackQueryHandler(age, pattern='^' + "ONE" + '$'),],
            SECOND: [CallbackQueryHandler(button),],
            AGETOJOB: [MessageHandler(Filters.text & ~Filters.command, agetojob)],
            JOBTOONE: [MessageHandler(Filters.text & ~Filters.command, jobtoone)],
            Q3:[
                CallbackQueryHandler(age, pattern='^' + "3分" + '$'),
            ],
            MONEY_ONE: [MessageHandler(Filters.text & ~Filters.command, money_one)],
            MONEY_TWO: [MessageHandler(Filters.text & ~Filters.command, money_two)],
            FOUR_THREE_TWO: [MessageHandler(Filters.text & ~Filters.command, four_three_two)],
            MONEY_THREE: [MessageHandler(Filters.text & ~Filters.command, money_three)],
            FIVESC: [CallbackQueryHandler(fivescore)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)
#     four_handler = MessageHandler(Filters.text & (~Filters.command), four)
#     dispatcher.add_handler(four_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
    app.run()


# In[ ]:




