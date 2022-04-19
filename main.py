from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, executor, filters
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests


bot = Bot("5156736281:AAFtXAuMr_ThtnK7VmGDRPGMQ6DCPDZbdcA", parse_mode="HTML")
# bot = Bot("5358139198:AAGC46EOWgnkT8XZYNcTE47vJoqROrAzOp4", parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())


## Getting basic information
async def get_info(name):
    try:
        list_all_data = []

        headers = {"user-agent": UserAgent().random}
        resp = requests.get(url=f"https://mintalytics.com/collection/{name}/",
                            headers=headers)

        soup = BeautifulSoup(resp.text, "html.parser")

        allInfo = soup.find('div', class_="row gx-4 gy-4")

        for data in allInfo:
            info = ((data.text).strip()).split("\n")
            if info == ['']:
                pass
            else:
                list_all_data.append(info)

        return list_all_data

    except Exception as ex:
        pass


## Getting pricing
async def get_price(name):
    try:
        list_all_data = []

        headers = {"user-agent": UserAgent().random}
        resp = requests.get(url=f"https://mintalytics.com/collection/{name}/",
                            headers=headers)

        soup = BeautifulSoup(resp.text, "html.parser")

        allPrice = soup.find("table", class_="sale-stat-table table mb-0 table-borderless").tbody


        for price in allPrice:
            info = ((price.text).strip()).split("\n")
            if info == ['']:
                pass
            else:
                list_all_data.append([value for value in info if value])

        return list_all_data

    except Exception as ex:
        pass


## Creating a message using a template
async def all_response(name):
    try:
        headers = {"user-agent": UserAgent().random}
        resp = requests.get(url=f"https://mintalytics.com/collection/{name}/",
                            headers=headers)

        if 200 <= resp.status_code <= 300:
            list_market_stats = await get_info(name)
            list_price_stats = await get_price(name)

            if "-" in (list_price_stats[0][2]):
                bounce = "🔴"
            else:
                bounce = "🟢"

            mess = f"<b>{bounce} {name.upper()}\n\n" \
                   f"</b><pre>┌────────────────────\n" \
                   f"</pre><code>│</code>       <b><i>MARKET STATS</i></b>\n" \
                   f"<code>├────────────────────\n" \
                   f"│ Floor Price: {list_market_stats[1][1]}\n" \
                   f"├────────────────────\n" \
                   f"│ Owners: {list_market_stats[2][1]}\n" \
                   f"├────────────────────\n" \
                   f"│ Listed: {list_market_stats[3][1]}\n" \
                   f"├────────────────────\n" \
                   f"│ Volume: {list_market_stats[4][1]}\n" \
                   f"└────────────────────\n\n" \
                   f"</code><pre>┌────────────────────\n" \
                   f"</pre><code>│</code>           <b><i>SALE STATS\n" \
                   f"</i></b><code>├────────────────────\n" \
                   f"│</code>  <b>One Day\n" \
                   f"</b><code>│\n" \
                   f"│ Volume: {list_price_stats[0][1]}\n" \
                   f"│ Average: {list_price_stats[0][4]}\n" \
                   f"│ Change: {list_price_stats[0][2]}\n" \
                   f"│ Sales: {list_price_stats[0][3]}\n" \
                   f"├────────────────────\n" \
                   f"│</code>  <b>Seven Days\n" \
                   f"</b><code>│\n" \
                   f"│ Volume: {list_price_stats[1][1]}\n" \
                   f"│ Average: {list_price_stats[1][4]}\n" \
                   f"│ Change: {list_price_stats[1][2]}\n" \
                   f"│ Sales: {list_price_stats[1][3]}\n" \
                   f"├────────────────────\n" \
                   f"│</code>  <b>Thirty Days\n" \
                   f"</b><code>│\n" \
                   f"│ Volume: {list_price_stats[2][1]}\n" \
                   f"│ Average: {list_price_stats[2][4]}\n" \
                   f"│ Change: {list_price_stats[2][2]}\n" \
                   f"│ Sales: {list_price_stats[2][3]}\n" \
                   f"└────────────────────</code>"

            return mess

        else:
            bad_req = "Error, enter the correct name of the collection"
            return bad_req

    except Exception as ex:
        return ex



@dp.message_handler(filters.ContentTypeFilter("text"))
async def cathcer(message: types.Message):
    text = message.text
    if text[0] == "/":
        name = text[1:]
        await bot.send_message(chat_id=message.chat.id,
                               text=f"<b>{name.upper()}</b>\n\n<i>Loading...</i>")

        answer = await all_response(name)

        await message.reply(text=answer)


    status = await bot.get_chat_member(chat_id=message.chat.id,
                                       user_id=message.from_user.id)

    try:
        if message.reply_to_message.sender_chat.type=="channel":
            if any(link in (message.text) for link in ["https://t.me/", "https://clck.ru/", "t.me/", "@"]) and (status.status=="left"):
                await bot.delete_message(chat_id=message.chat.id,
                                         message_id=message.message_id)
                # await bot.ban_chat_member(chat_id=message.chat.id,
                #                           user_id=message.from_user.id)
                await bot.send_message(chat_id=message.chat.id,
                                       text=f"{message.from_user.first_name} your message has been deleted.\n\n"
                                            f"Reason - links are prohibited")
            else:
                pass

    except Exception as ex:
        pass
        # await bot.send_message(chat_id=1095119526,
        #                        text=ex)



if __name__ == '__main__':
    print("Bot work")
    executor.start_polling(dp)