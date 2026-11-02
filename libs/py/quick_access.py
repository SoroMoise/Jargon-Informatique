#!/usr/bin/python3
# coding : utf-8

from libs.py.interaction_bd import interroger_bd
from functools import lru_cache

class QuickAccess:
    """
    Provides quick access to frequently used words and favorites
    """
    
    @lru_cache(maxsize=32)
    def get_recent_words(self, limit: int = 10) -> list:
        """
        Get recently viewed words from history
        :param limit: Number of recent words to return
        :return: List of recent words
        """
        try:
            recent = interroger_bd(
                "mot", 
                "historique, dictionnaire",
                "where historique.id_mot = dictionnaire.idmot ORDER BY historique.numero DESC"
            )
            return [word[0] for word in recent[:limit]]
        except Exception:
            return []
    
    @lru_cache(maxsize=32)
    def get_favorite_words(self, limit: int = 10) -> list:
        """
        Get favorite words
        :param limit: Number of favorite words to return
        :return: List of favorite words
        """
        try:
            favorites = interroger_bd(
                "mot", 
                "aimer, dictionnaire",
                "where aimer.id_mot = dictionnaire.idmot ORDER BY aimer.numero DESC"
            )
            return [word[0] for word in favorites[:limit]]
        except Exception:
            return []
    
    def get_random_word_of_day(self) -> tuple:
        """
        Get a random word for the day (cached based on date)
        :return: Tuple of (word, definition)
        """
        from datetime import date
        from random import seed, choice
        
        # Seed with today's date for consistent daily word
        today = date.today()
        seed(today.toordinal())
        
        try:
            # Get a random word
            all_words = interroger_bd("idmot", "dictionnaire")
            if all_words:
                random_word_id = choice(all_words)[0]
                word_data = interroger_bd(
                    "mot, definition", 
                    "dictionnaire", 
                    f"WHERE idmot = '{random_word_id}'"
                )
                if word_data:
                    return word_data[0]
        except Exception:
            pass
        
        return ("", "")
    
    def clear_cache(self):
        """Clear the cache for fresh data"""
        self.get_recent_words.cache_clear()
        self.get_favorite_words.cache_clear()

# Global instance
quick_access = QuickAccess()