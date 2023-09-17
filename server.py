import logging

from config import TOKEN, PAYMENTS_TOKEN

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.message import ContentType

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

PRICE = types.LabeledPrice(label="your_label", amount=500*100)


@dp.message_handler(commands=['buy'])
async def buy(message: types.Message):
    if PAYMENTS_TOKEN.split(':')[1] == "TEST":
        await bot.send_message(message.chat.id, "Тестовый платёж")

    await bot.send_invoice(message.chat.id,
                           title="your_title",
                           description="your_description",
                           provider_token=PAYMENTS_TOKEN,
                           currency="your_currency",
                           photo_url="your/photo/url",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="your_start_parameter",
                           payload="test-invoice-payload")


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id,
                           f"Платёж на сумму {message.successful_payment.total_amount // 100} "
                           f"{message.successful_payment.currency} прошёл успешно")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
