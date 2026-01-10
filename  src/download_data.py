import yfinance as yf
import pandas as pd
import os
from datetime import datetime

# Настройки
TIKERS = {
    'Brent_Oil': 'BZ=F',   # Фьючерс на нефть Brent
    'SP500': '^GSPC'       # Индекс S&P 500 (для сравнения динамики)
}
START_DATE = '2020-01-01'
END_DATE = datetime.today().strftime('%Y-%m-%d') # По сегодняшний день
DATA_DIR = 'data'

def download_data(ticker_symbol, name):
    """
    Скачивает данные по тикеру и сохраняет в CSV.
    """
    print(f"⏳ Скачиваю данные для {name} ({ticker_symbol})...")
    
    try:
        # Скачиваем данные
        df = yf.download(ticker_symbol, start=START_DATE, end=END_DATE, progress=False)
        
        if df.empty:
            print(f"⚠️ Внимание: Данные для {name} пустые. Проверьте тикер.")
            return

        # Сбрасываем индекс, чтобы Date стала колонкой
        df = df.reset_index()
        
        # Оставляем только нужные колонки для чистоты (Дата, Закрытие, Объем)
        # Обратите внимание: yfinance может возвращать мульти-индекс, упростим его
        if isinstance(df.columns, pd.MultiIndex):
             df.columns = df.columns.get_level_values(0)

        columns_to_keep = ['Date', 'Close', 'Volume']
        # Проверяем, есть ли такие колонки (иногда названия отличаются)
        available_cols = [c for c in columns_to_keep if c in df.columns]
        df = df[available_cols]

        # Формируем путь сохранения
        file_path = os.path.join(DATA_DIR, f"{name.lower()}_data.csv")
        
        # Сохраняем
        df.to_csv(file_path, index=False)
        print(f"✅ Успешно сохранено: {file_path} (Строк: {len(df)})")
        
    except Exception as e:
        print(f"❌ Ошибка при скачивании {name}: {e}")

def main():
    # Проверяем, существует ли папка data, если нет - создаем
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"📁 Создана папка {DATA_DIR}")

    # Запускаем цикл по всем тикерам
    for name, ticker in TIKERS.items():
        download_data(ticker, name)
    
    print("\n🚀 Сбор данных завершен. Можно переходить к анализу.")

if __name__ == "__main__":
    main()
