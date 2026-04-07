from campaigns.base_campaign import BaseCampaign

class Apr26FoolCampaign(BaseCampaign):
    def get_config(self):
        return {
            "table_id": "swag-talents.talent_campaign.2604_fool",
            "sql_template": """
                SELECT
                    creator_id,
                    creator_name,
                    total_votes,
                    vote_rank,
                    total_diamonds,
                    is_raffle_eligible
                FROM `{table_id}`
            """
        }

    def transform_data(self, rows):
        results = []
        for row in rows:
            results.append({
                "creator_id": row.creator_id,
                "creator_name": row.creator_name,  
                "total_votes": row.total_votes,
                "vote_rank": row.vote_rank,
                "total_diamonds": row.total_diamonds,
                "is_raffle_eligible": row.is_raffle_eligible
            })
        return results

    def get_sort_mapping(self):
        return {"rank": "vote_rank"}

    def get_default_sort(self):
        return "vote_rank"
