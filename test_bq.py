from google.cloud import bigquery
import sys

# 您提供的 Table ID
TABLE_ID = "swag-talents.talent_campaign.2602_valentine"

def test_connection():
    print(f"🔍 正在嘗試連線到 BigQuery Table: {TABLE_ID} ...")
    
    try:
        client = bigquery.Client()
        
        # 1. 測試是否能抓到 Table (確認 ID 正確 & 有權限)
        table = client.get_table(TABLE_ID)
        print(f"✅ 成功找到 Table！")
        print(f"   - 專案: {table.project}")
        print(f"   - 資料集: {table.dataset_id}")
        print(f"   - 表格: {table.table_id}")
        print(f"   - 總筆數: {table.num_rows}")
        
        # 2. 測試查詢與欄位名稱 (確認 Schema)
        print("\n🔍 正在測試讀取 1 筆資料並檢查欄位...")
        query = f"""
            SELECT
                username,
                creator_id,
                cnt_motel,
                cnt_marshmallow,
                cnt_dating,
                cnt_arrow,
                set_cnt_warm,
                set_cnt_pure,
                warm_rank,
                pure_rank,
                warm_reward,
                pure_reward,
                great_reward,
                chosen_board,
                warm_rank_final,
                pure_rank_final,
                warm_reward_final,
                pure_reward_final,
                final_board,
                final_reward_diamonds
            FROM `{TABLE_ID}`
            LIMIT 1
        """
        query_job = client.query(query)
        rows = list(query_job.result())
        
        if not rows:
            print("⚠️ 查詢成功但沒有資料 (Empty Result)")
            return

        row = rows[0]
        print("✅ 資料讀取成功！第一筆資料預覽：")
        print(f"   - username: {row.username}")
        print(f"   - warm_rank: {row.warm_rank}")
        print(f"   - final_board: {row.final_board}")
        
        print("\n🎉 恭喜！資料表路徑與欄位定義完全正確！")

    except Exception as e:
        print("\n❌ 發生錯誤！請將以下錯誤訊息貼給 AI：")
        print("------------------------------------------------")
        print(e)
        print("------------------------------------------------")

if __name__ == "__main__":
    test_connection()
