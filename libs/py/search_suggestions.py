#!/usr/bin/python3
# coding : utf-8

from libs.py.interaction_bd import interroger_bd
from functools import lru_cache

class SearchSuggestions:
    """
    Provides search suggestions for better user experience
    """
    
    def __init__(self):
        self._word_cache = None
    
    @property
    def word_cache(self):
        """Lazy load word cache"""
        if self._word_cache is None:
            self._word_cache = [word[0].lower() for word in interroger_bd("idmot", "dictionnaire")]
        return self._word_cache
    
    @lru_cache(maxsize=64)
    def get_suggestions(self, query: str, limit: int = 10) -> list:
        """
        Get search suggestions based on user input
        :param query: User's search query
        :param limit: Maximum number of suggestions
        :return: List of suggestions
        """
        if not query or len(query) < 2:
            return []
        
        query = query.lower().strip()
        suggestions = []
        
        # Exact matches first
        for word in self.word_cache:
            if word.startswith(query):
                suggestions.append(word)
                if len(suggestions) >= limit:
                    break
        
        # Partial matches if we need more suggestions
        if len(suggestions) < limit:
            for word in self.word_cache:
                if query in word and not word.startswith(query):
                    suggestions.append(word)
                    if len(suggestions) >= limit:
                        break
        
        return suggestions
    
    def get_popular_searches(self, limit: int = 5) -> list:
        """
        Get popular/recommended searches
        :param limit: Number of popular searches to return
        :return: List of popular search terms
        """
        # Get some common tech terms that are likely in the dictionary
        popular_terms = ['serveur', 'application', 'base de données', 'réseau', 'sécurité']
        
        # Filter to only include terms that exist in the dictionary
        existing_terms = []
        for term in popular_terms:
            if any(term.lower() in word for word in self.word_cache[:100]):  # Check first 100 for performance
                existing_terms.append(term)
                if len(existing_terms) >= limit:
                    break
        
        return existing_terms

# Global instance
search_suggestions = SearchSuggestions()