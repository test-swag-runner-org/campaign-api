import os
import sys  # 用於強制輸出錯誤 Log
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from google.cloud import bigquery

# --- 匯入活動邏輯 ---
# 新增活動需改-1
from campaigns.jan26_test import Jan26TestCampaign
from campaigns.jan26_winter_sonata import Jan26WinterSonataCampaign
from campaigns.feb26_valentine import Feb26ValentineCampaign
from campaigns.mar26_white_valentine import Mar26WhiteValentineCampaign
from campaigns.apr26_fool import Apr26FoolCampaign
from campaigns.apr26_child import Apr26ChildCampaign
# 未來新增: from campaigns.feb26_love import Feb26LoveCampaign

app = Flask(__name__)
CORS(app)

# --- 快取設定 (SimpleCache 是存於記憶體) ---
# 設定預設過期時間為 10 秒，確保資料新鮮度
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 10})

bq_client = bigquery.Client()

# --- 更新註冊表 ---
# 新增活動需改-2
CAMPAIGN_REGISTRY = {
    "jan26_test": Jan26TestCampaign(),
    "jan26_winter_sonata": Jan26WinterSonataCampaign(),
    "feb26_valentine": Feb26ValentineCampaign(),
    "mar26_white_valentine": Mar26WhiteValentineCampaign(),
    "apr26_fool": Apr26FoolCampaign(),
    "apr26_child": Apr26ChildCampaign()
    # 未來新增: "feb26_love": Feb26LoveCampaign(),
}

def get_user_identifier():
    # 在 Cloud Run 環境下抓取真實 User IP
    return request.headers.get('X-Forwarded-For', request.remote_addr)

limiter = Limiter(
    key_func=get_user_identifier,
    app=app,
    default_limits=["1000 per day", "100 per hour"],
    storage_uri="memory://"
)

@app.route('/')
def home():
    return jsonify({
        "status": "Campaign API Gateway Running",
        "available_campaigns": list(CAMPAIGN_REGISTRY.keys()),
        "usage": "/api/campaigns/<campaign_id>"
    })

# --- 核心優化：分離「撈資料」與「排序」---

# 1. 專門負責撈資料的函式 (加上快取)
# 這裡設定 key_prefix (自動根據參數)，確保同一個活動 ID 在 10 秒內只會查一次 BigQuery
# 不管後面 sort 參數是什麼，只要 campaign_id 一樣，就用同一份快取
@cache.memoize(timeout=10)
def fetch_campaign_data_from_bq(campaign_id):
    campaign = CAMPAIGN_REGISTRY.get(campaign_id)
    if not campaign:
        return None

    # Log 修復：加上 flush=True 強制輸出到 Cloud Run Log，不要緩衝
    print(f"⚡ [Cache Miss] Querying BigQuery for {campaign_id}...", flush=True)
    
    config = campaign.get_config()
    query = config["sql_template"].format(table_id=config["table_id"])
    
    try:
        query_job = bq_client.query(query)
        rows = query_job.result()
        # 資料轉換
        return campaign.transform_data(rows)
    except Exception as e:
        # Log 修復：錯誤訊息也要 flush，並輸出到 stderr
        print(f"Error: {e}", file=sys.stderr, flush=True)
        return None

# --- 通用 API 入口 ---
@app.route('/api/campaigns/<campaign_id>', methods=['GET'])
@limiter.limit("60 per minute")
def get_campaign_data(campaign_id):
    
    # 1. 呼叫有快取的函式取得原始資料
    # 注意：這裡不傳 request.args 進去，確保快取 Key 只跟 campaign_id 有關
    # 這樣 User A 查 vote，User B 查 diamond，都可以共享同一份 BigQuery 資料
    data = fetch_campaign_data_from_bq(campaign_id)

    if data is None:
        # 如果是 None，可能是 campaign_id 錯了或是 BQ 錯誤
        if campaign_id not in CAMPAIGN_REGISTRY:
            return jsonify({"error": "Campaign not found"}), 404
        return jsonify({"error": "Data fetch failed"}), 500

    # 2. 取得 Campaign 設定
    campaign = CAMPAIGN_REGISTRY.get(campaign_id)
    
    # 3. 搜尋邏輯 (In-Memory 過濾，超快)
    # 複製一份引用進行過濾，不影響原始快取
    search_query = request.args.get('username', '').strip().lower()
    filtered_data = data
    if search_query:
        # 這裡假設所有活動回傳的資料都有 'username' 欄位
        filtered_data = [d for d in data if d.get('username') and search_query in d.get('username').lower()]

    # 4. 排序邏輯 (In-Memory 排序，超快)
    # 從 Campaign 取得對應表，例如 {'vote': 'vote_rank', ...}
    sort_mapping = campaign.get_sort_mapping()
    default_sort = campaign.get_default_sort()
    
    # 取得前端參數，若無則使用預設值
    sort_param = request.args.get('sort', default_sort)
    
    # 找出對應的資料欄位 (key)
    sort_key = sort_mapping.get(sort_param)
    
    # 如果前端傳了不支援的 sort 參數 (如 ?sort=hack)，就 fallback 回預設
    if not sort_key:
        sort_key = sort_mapping.get(default_sort)

    # 執行排序
    # 這裡保留了 "空值墊底 (999999)" 的邏輯
    def get_sort_value(item, key):
        val = item.get(key)
        return val if val is not None else 999999

    # 注意：這裡預設是「由小到大 (Ascending)」，適用於 Rank (1, 2, 3...)
    sorted_data = sorted(filtered_data, key=lambda x: get_sort_value(x, sort_key))

    return jsonify({
        "metadata": {
            "campaign": campaign_id,
            "count": len(sorted_data),
            "sorted_by": sort_param,  # 回傳實際使用的排序依據
            "cache_status": "shared_by_campaign_id" 
        },
        "data": sorted_data
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
