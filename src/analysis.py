import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime

# Настройки
OIL_FILE = 'data/brent_oil_data.csv'
SP_FILE = 'data/sp500_data.csv'
OUTPUT_DIR = 'output'

def make_analysis():
    if not os.path.exists(OIL_FILE) or not os.path.exists(SP_FILE):
        print("❌ Данные не найдены. Сначала запусти download_data.py")
        return

    # 1. Загрузка и объединение (Merge)
    oil = pd.read_csv(OIL_FILE)[['Date', 'Close']].rename(columns={'Close': 'Oil_Price'})
    sp = pd.read_csv(SP_FILE)[['Date', 'Close']].rename(columns={'Close': 'SP500_Index'})
    df = pd.merge(oil, sp, on='Date')
    df['Date'] = pd.to_datetime(df['Date'])

    # 2. Расчет корреляции
    corr_value = df['Oil_Price'].corr(df['SP500_Index'])
    print(f"\n📊 Связь (корреляция) Нефть vs S&P500: {corr_value:.2f}")

    # 3. График №1: Тренды и прогноз (то, что мы уже делали)
    print("📈 Обновляю основной график...")
    oil_df = pd.read_csv(OIL_FILE)
    oil_df['Date'] = pd.to_datetime(oil_df['Date'])
    oil_df['MA20'] = oil_df['Close'].rolling(window=20).mean()
    oil_df['MA50'] = oil_df['Close'].rolling(window=50).mean()
    
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    plt.plot(oil_df['Date'], oil_df['Close'], label='Цена Brent', alpha=0.4, color='blue')
    plt.plot(oil_df['Date'], oil_df['MA20'], label='Тренд 20 дней', color='orange')
    plt.plot(oil_df['Date'], oil_df['MA50'], label='Тренд 50 дней', color='red')
    plt.title('Динамика цен на нефть Brent (2020-2026)')
    plt.legend()
    plt.savefig(os.path.join(OUTPUT_DIR, 'oil_analysis_chart.png'))

    # 4. График №2: Корреляция (Новый!)
    print("📊 Создаю график сравнения...")
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x='SP500_Index', y='Oil_Price', 
                scatter_kws={'alpha':0.3, 'color':'teal'}, 
                line_kws={'color':'red', 'label':'Линия тренда'})
    plt.title(f'Корреляция цен: Нефть vs S&P500 (Коэффициент: {corr_value:.2f})')
    plt.xlabel('Индекс S&P 500 (Состояние экономики)')
    plt.ylabel('Цена нефти Brent ($)')
    plt.savefig(os.path.join(OUTPUT_DIR, 'oil_sp500_correlation.png'))
    
    print(f"✅ Готово! Все графики в папке {OUTPUT_DIR}")

if __name__ == "__main__":
    make_analysis()
