import yfinance as yf
import json
import os

def update_prices():
    json_path = 'etf_data.json'
    
    if not os.path.exists(json_path):
        print("找不到 json 檔案！")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        etf_data = json.load(f)
    
    for code in list(etf_data.keys()):
        ticker_code = f"{code}.TW"
        print(f"正在獲取 {code} 的最新股價...")
        
        try {
            ticker = yf.Ticker(ticker_code)
            df = ticker.history(period='1d')
            if not df.empty:
                latest_price = round(df['Close'].iloc[-1], 2)
                etf_data[code]['price'] = latest_price
                print(f"➔ {code} 股價成功更新為: {latest_price}")
            else:
                print(f"⚠️ 找不到 {code} 的當日數據，維持原價。")
        except Exception as e:
            print(f"❌ 抓取 {code} 失敗: {e}")
            
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(etf_data, f, ensure_ascii=False, indent=4)
    print("🎉 所有 ETF 股價更新完成！")

if __name__ == '__main__':
    update_prices()
