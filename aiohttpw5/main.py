import aiohttp
import asyncio
import argparse
from datetime import datetime, timedelta

# Глобальные переменные для валют
TARGET_CURRENCIES = ['EUR', 'USD']

async def main(days):
    # Проверка на количество дней (не более 10)
    if days > 10:
        print("Error: The number of days should not exceed 10.")
        return None

    result_list = []

    # Вычисляем дату, от которой нужно получить курсы
    for day in range(days):
        current_date = datetime.now() - timedelta(days=day)
        formatted_date = current_date.strftime("%d.%m.%Y")

        async with aiohttp.ClientSession() as session:
            url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={formatted_date}&coursid=5'
            async with session.get(url) as response:
                # print("Status:", response.status)
                # print("Content-type:", response.headers['content-type'])
                # print('Cookies: ', response.cookies)
                # print(response.ok)
                result = await response.json()

                # Обработка результата для текущей даты
                formatted_result = process_result(result, formatted_date)
                result_list.append(formatted_result)

    return result_list

# Обработчик результата
def process_result(result, date):
    formatted_result = {}

    # Перебираем элементы exchangeRate в полученных данных
    for entry in result['exchangeRate']:
        currency_code = entry['currency']

        # Проверяем, если текущая валюта в списке TARGET_CURRENCIES
        if currency_code in TARGET_CURRENCIES:
            sale_rate = entry.get('saleRate', entry.get('saleRateNB', None))
            purchase_rate = entry.get('purchaseRate', entry.get('purchaseRateNB', None))

            # Создаем вложенные словари для каждой даты и валюты
            if date not in formatted_result:
                formatted_result[date] = {}
            if currency_code not in formatted_result[date]:
                formatted_result[date][currency_code] = {}

            # Записываем значения продажи и покупки
            formatted_result[date][currency_code]['sale'] = sale_rate
            formatted_result[date][currency_code]['purchase'] = purchase_rate

    return formatted_result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get exchange rates for specified currencies over the last N days.')
    parser.add_argument('days', type=int, help='Number of days to get exchange rates for (not more than 10)')
    args = parser.parse_args()

    # Проверка на количество дней (не более 10)
    if args.days > 10:
        print("Error: The number of days should not exceed 10.")
    else:
        result = asyncio.run(main(args.days))

        # Выводим результат с переносами строк
        print("[")
        for item in result:
            print("  " + str(item) + ",")
        print("]")
