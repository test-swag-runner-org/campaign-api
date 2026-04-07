# 檔案位置：campaigns/base_campaign.py

from abc import ABC, abstractmethod

class BaseCampaign(ABC):
    """
    所有活動邏輯的父類別 (介面)
    """
    
    @abstractmethod
    def get_config(self):
        """回傳該活動的基本設定 (如 Table ID)"""
        pass

    @abstractmethod
    def transform_data(self, rows):
        """將 BigQuery 的資料轉換成前端需要的 JSON 格式"""
        pass

    @abstractmethod
    def get_sort_mapping(self):
        """
        回傳排序參數對應表
        Format: {'URL參數值': '資料欄位key'}
        Example: {'vote': 'vote_rank', 'diamond': 'diamond_rank'}
        """
        pass
    
    @abstractmethod
    def get_default_sort(self):
        """回傳預設的排序參數值 (如 'diamond')"""
        pass