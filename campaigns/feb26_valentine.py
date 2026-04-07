from campaigns.base_campaign import BaseCampaign

class Feb26ValentineCampaign(BaseCampaign):
    def get_config(self):
        return {
            "table_id": "swag-2c052.talent_sandbox.2602_valentine",
            "sql_template": """
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
                FROM `{table_id}`
            """
        }

    def transform_data(self, rows):
        results = []
        for row in rows:
            results.append({
                "username": row.username,
                "creator_id": row.creator_id,
                "cnt_motel": row.cnt_motel,
                "cnt_marshmallow": row.cnt_marshmallow,
                "cnt_dating": row.cnt_dating,
                "cnt_arrow": row.cnt_arrow,
                "set_cnt_warm": row.set_cnt_warm,
                "set_cnt_pure": row.set_cnt_pure,
                "warm_rank": row.warm_rank,
                "pure_rank": row.pure_rank,
                "warm_reward": row.warm_reward,
                "pure_reward": row.pure_reward,
                "great_reward": row.great_reward,
                "chosen_board": row.chosen_board,
                "warm_rank_final": row.warm_rank_final,
                "pure_rank_final": row.pure_rank_final,
                "warm_reward_final": row.warm_reward_final,
                "pure_reward_final": row.pure_reward_final,
                "final_board": row.final_board,
                "final_reward_diamonds": row.final_reward_diamonds
            })
        return results

    def get_sort_mapping(self):
        return {
            "warm": "warm_rank",
            "pure": "pure_rank"
        }

    def get_default_sort(self):
        return "warm"
