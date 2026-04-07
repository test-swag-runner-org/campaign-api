# 注意：這裡是指從 campaigns 資料夾下的 base_campaign 檔案匯入
from campaigns.base_campaign import BaseCampaign

class Jan26TestCampaign(BaseCampaign):
    def get_config(self):
        return {
            "table_id": "swag-2c052.talent_sandbox.2601_rank_and_vote_campaign_test",
            "sql_template": """
                SELECT
                    username,
                    total_spending_diamonds,
                    total_votes,
                    diamond_rank,
                    vote_rank
                FROM `{table_id}`
            """
        }

    def transform_data(self, rows):
        results = []
        for row in rows:
            results.append({
                "username": row.username,
                "total_spending_diamonds": row.total_spending_diamonds,
                "total_votes": row.total_votes,
                "diamond_rank": row.diamond_rank,
                "vote_rank": row.vote_rank
            })
        return results

    def get_sort_mapping(self):
        return {
            "vote": "vote_rank",
            "diamond": "diamond_rank"
        }

    def get_default_sort(self):
        return "diamond"
