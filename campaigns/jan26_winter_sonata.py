# 注意：這裡是指從 campaigns 資料夾下的 base_campaign 檔案匯入
from campaigns.base_campaign import BaseCampaign

class Jan26WinterSonataCampaign(BaseCampaign):
    def get_config(self):
        return {
            "table_id": "swag-2c052.talent_sandbox.2601_winter_sonata",
            "sql_template": """
                SELECT
                    username,
                    total_diamonds,
                    diamond_rank,
                    leaderboard_reward_diamonds,
                    is_raffle_eligible
                FROM `{table_id}`
            """
        }

    def transform_data(self, rows):
        results = []
        for row in rows:
            results.append({
                "username": row.username,
                "total_diamonds": row.total_diamonds,
                "diamond_rank": row.diamond_rank,
                "leaderboard_reward_diamonds": row.leaderboard_reward_diamonds,
                "is_raffle_eligible": row.is_raffle_eligible
            })
        return results

    def get_sort_mapping(self):
        return {
            "diamond": "diamond_rank"
        }

    def get_default_sort(self):
        return "diamond"
