from campaigns.base_campaign import BaseCampaign

class Apr26ChildCampaign(BaseCampaign):
    def get_config(self):
        return {
            "table_id": "swag-talents.talent_campaign.2604_child",
            "sql_template": """
                SELECT
                    rank_no,
                    creator_id,
                    creator_name,
                    total_command_diamonds,
                    total_live_diamonds,
                    top15_total_diamonds,
                    prize_pool_ratio,
                    prize_pool_diamonds,
                    rank_pct,
                    reward_diamonds_rounded,
                    raffles
                FROM `{table_id}`
            """
        }

    def transform_data(self, rows):
        results = []
        for row in rows:
            results.append({
                "username": row.creator_name,  
                "rank_no": row.rank_no,
                "creator_id": row.creator_id,
                "creator_name": row.creator_name,
                "total_command_diamonds": row.total_command_diamonds,
                "total_live_diamonds": row.total_live_diamonds,
                "top15_total_diamonds": row.top15_total_diamonds,
                "prize_pool_ratio": row.prize_pool_ratio,
                "prize_pool_diamonds": row.prize_pool_diamonds,
                "rank_pct": row.rank_pct,
                "reward_diamonds_rounded": row.reward_diamonds_rounded,
                "raffles": row.raffles
            })
        return results

    def get_sort_mapping(self):
        return {"rank": "rank_no"}

    def get_default_sort(self):
        return "rank"
