import traceback
from google.cloud import bigquery

# 您的目標 Table
TABLE_ID = "swag-talents.talent_campaign.2602_valentine"

def debug_connection():
    print("🕵️‍♂️ 開始深入診斷 BigQuery 連線...")
    
    try:
        # 1. 測試 Client 初始化
        print("   1. 正在初始化 BigQuery Client...")
        client = bigquery.Client()
        print(f"      -> 成功 (Project: {client.project})")

        # 2. 測試最簡單的查詢 (確認連線與權限沒壞)
        print("   2. 測試基本查詢 (SELECT 1)...")
        query_job = client.query("SELECT 1")
        result = list(query_job.result())
        print(f"      -> 成功 (Result: {result})")

        # 3. 測試讀取目標 View
        print(f"   3. 測試讀取目標 View ({TABLE_ID})...")
        query = f"SELECT * FROM `{TABLE_ID}` LIMIT 1"
        query_job = client.query(query)
        rows = list(query_job.result())
        
        if not rows:
            print("      -> 警告：查詢成功但沒有資料 returned (Empty)")
            return

        row = rows[0]
        print(f"      -> 成功取得第一筆資料 (Type: {type(row)})")
        print(f"      -> 資料內容預覽: {row}")

        # 4. 測試字典轉換 (這裡是上次報錯的嫌疑犯)
        print("   4. 測試資料轉換 (dict conversion)...")
        row_dict = dict(row)
        print("      -> 轉換成功！")
        print("      -> 欄位清單:", list(row_dict.keys()))

        print("\n🎉 恭喜！診斷全部通過，看來環境是正常的。")

    except Exception:
        print("\n💥 抓到兇手了！詳細錯誤報告如下：")
        print("==================================================")
        traceback.print_exc()
        print("==================================================")
        print("請把上面這一段 'Traceback' 貼給我，我馬上就能知道是哪一行出錯！")

if __name__ == "__main__":
    debug_connection()