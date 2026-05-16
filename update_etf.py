import yfinance as yf
import json
import os

def update_prices():
    json_path = 'etf_data.json'
    
    # 1. 讀取現有的 JSON 資料
    if not os.path.exists(json_path):
        print("找不到 json 檔案！")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        etf_data = json.load(f)
    
    # 2. 遍歷每檔 ETF，抓取最新股價
    for code in list(etf_data.keys()):
        ticker_code = f"{code}.TW"  # 台股代碼在 yfinance 需要加上 .TW
        print(f"正在獲取 {code} 的最新股價...")
        
        try:
            ticker = yf.Ticker(ticker_code)
            # 抓取最近一天的歷史數據
            df = ticker.history(period='1d')
            if not df.empty:
                # 取得最新一筆收盤價，並四捨五入到小數點後兩位
                latest_price = round(df['Close'].iloc[-1], 2)
                etf_data[code]['price'] = latest_price
                print(f"➔ {code} 股價成功更新為: {latest_price}")
            else:
                print(f"⚠️ 找不到 {code} 的當日數據，維持原價。")
        except Exception as e:
            print(f"❌ 抓取 {code} 失敗: {e}")
            
    # 3. 將更新後的資料寫回 JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(etf_data, f, ensure_ascii=False, indent=4)
    print("🎉 所有 ETF 股價更新完成！")

if __name__ == '__main__':
    update_prices()
