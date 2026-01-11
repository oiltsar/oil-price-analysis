import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime

# Настройки
DATA_FILE = 'data/brent_oil_data.csv'
OUTPUT_DIR = 'output'

def make_analysis():
    if not os.path.exists(DATA_FILE):
        print(f"❌ Файл {DATA_FILE} не найден!")
        return

    # Загрузка и подготовка данных
    df = pd.read_csv(DATA_FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    # Расчет метрик (как в вашем курсе по Pandas)
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()

    # Построение графика
    print("📊 Строю графики...")
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    
    plt.plot(df['Date'], df['Close'], label='Цена Brent', alpha=0.5, color='blue')
    plt.plot(df['Date'], df['MA20'], label='Тренд 20 дней', color='orange')
    plt.plot(df['Date'], df['MA50'], label='Тренд 50 дней', color='red')
    
    plt.title('Анализ цен на нефть Brent (2020-2026)', fontsize=15)
    plt.xlabel('Дата')
    plt.ylabel('Цена ($)')
    plt.legend()

    # Сохранение результата
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    chart_path = os.path.join(OUTPUT_DIR, 'oil_analysis_chart.png')
    plt.savefig(chart_path)
    print(f"✅ График успешно сохранен: {chart_path}")

    # Мини-прогноз
    X = np.array(range(len(df))).reshape(-1, 1)
    y = df['Close'].values
    model = LinearRegression().fit(X, y)
    future_price = model.predict([[len(df) + 30]])
    print(f"🔮 Линейный прогноз на месяц: ~${future_price[0]:.2f}")

if __name__ == "__main__":
    make_analysis()
