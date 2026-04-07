from google.cloud import bigquery

# 請再次確認您的 Table ID 是否完全正確
TABLE_ID = "swag-talents.talent_campaign.2602_valentine"

def test_query():
    print(f"🚀 開始測試查詢: {TABLE_ID}")
    client = bigquery.Client()

    # 直接查 * (所有欄位)，這樣可以列出 BigQuery 實際看到的欄位名稱
    query = f"SELECT * FROM `{TABLE_ID}` LIMIT 1"
    
    try:
        query_job = client.query(query)
        print("⏳ 查詢送出，等待結果...")
        
        # 取得結果
        rows = list(query_job.result())
        
        if not rows:
            print("⚠️ 查詢成功，但資料表是空的 (Empty Table)！")
            return

        row = rows[0]
        print("\n✅ 查詢成功！讀取到的第一筆資料如下：")
        print("------------------------------------------------")
        
        # 顯示所有欄位名稱與值，幫我們檢查拼字
        # Row 物件可以轉成 dict 來查看 key
        row_dict = dict(row)
        for key, value in row_dict.items():
            print(f"📄 欄位 [{key}]: {value}")
            
        print("------------------------------------------------")
        print("請檢查上面的「欄位名稱」是否跟程式碼裡的完全一樣？(大小寫也要一樣)")

    except Exception as e:
        print("\n❌ 查詢失敗！原因如下：")
        print(e)

if __name__ == "__main__":
    test_query()
