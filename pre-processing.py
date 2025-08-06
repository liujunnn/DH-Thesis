#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Preprocessing Module

Functions: Stopword management, text cleaning, tokenization, and language detection
for processing multilingual porcelain metadata descriptions.
"""

import re
from typing import Set, List, Dict, Any
import nltk
from nltk.corpus import stopwords

# Attempt to download required NLTK data silently
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

class TextPreprocessor:
    """
    Text Preprocessor for Porcelain Metadata
    
    Handles multilingual text cleaning, stopword removal, and tokenization
    with special consideration for domain-specific porcelain terminology.
    """
    
    def __init__(self):
        """
        Initialize the text preprocessor with stopwords and core terms
        """
        # Initialize English stopwords from NLTK
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            # Fallback to predefined stopwords if NLTK fails
            self.stop_words = self._get_default_stopwords()
        
        # Domain-specific stopwords (museum/porcelain context)
        self.domain_stopwords = self._get_domain_stopwords()
        
        # Combine all stopwords
        self.all_stopwords = self.stop_words.union(self.domain_stopwords)
        
        # Core porcelain terms that should NOT be filtered out
        self.core_porcelain_terms = self._get_core_terms()
    
    def _get_default_stopwords(self) -> Set[str]:
        """
        Get default English stopwords
        
        Returns:
            Set of common English stopwords
        """
        return {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 
            'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 
            'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 
            'itself', 'they', 'them', 'their', 'theirs', 'themselves', 
            'what', 'which', 'who', 'whom', 'this', 'that', 'these', 
            'those', 'am', 'is', 'are', 'was', 'were', 'been', 'being', 
            'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 
            'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 
            'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
            'between', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
            'on', 'off', 'over', 'under', 'again', 'further', 'then',
            'once', 'here', 'there', 'when', 'where', 'why', 'how',
            'all', 'both', 'each', 'few', 'more', 'most', 'other',
            'some', 'such', 'only', 'own', 'same', 'so', 'than',
            'too', 'very', 'can', 'will', 'just', 'should', 'now'
        }
    
    def _get_domain_stopwords(self) -> Set[str]:
        """
        Get domain-specific stopwords for museum/porcelain contexts
        
        Returns:
            Set of domain-specific stopwords including multilingual terms,
            metadata artifacts, and museum-related terminology
        """
        return {
            # Multilingual common words (Swedish, Dutch, French, German, Italian)
            'def', 'och', 'som', 'den', 'det', 'ett', 'med', 'par', 'fut',
            'lieu', 'een', 'met', 'del', 'della', 'delle', 'dei', 'nel',
            'pour', 'dans', 'avec', 'sur', 'une', 'les', 'ces', 'von', 'mit',
            'der', 'die', 'das', 'und', 'ist', 'sind', 'wird', 'wurde',
            
            # Metadata-related terms
            'note', 'vente', 'document', 'genre', 'fotogr', 'dnr', 'email',
            'http', 'edu', 'aat', 'vocab', 'getty', 'url', 'link', 'site',
            'item', 'object', 'artifact', 'collection', 'museum', 'archive',
            'unknown', 'unclear', 'possibly', 'probably', 'various', 'similar',
            
            # Museum and institution related
            'inst', 'coll', 'inv', 'donated', 'property', 'catalogue',
            'old', 'english', 'furniture', 'art', 'pavillon', 'laeken',
            'inventory', 'acquisition', 'bequest', 'gift', 'purchase',
            'accession', 'provenance', 'formerly', 'estate', 'sale', 'lot',
            'bijlokemuseum', 'kulturstyrelsen', 'gent', 'ghent',
            'stockholm', 'bruxelles', 'amsterdam', 'london', 'paris',
            'sotheby', 'christie', 'puttick', 'simpson', 'woods', 'manson',
            
            # Non-English generic porcelain terms
            'porcel', 'kinesisk', 'porslin', 'porselein', 'porcellana',
            'teller', 'coupe', 'schale', 'piatto', 'assiette',
            'bodenmarke', 'dekor', 'fond',
            
            # Other multilingual terms
            'van', 'het', 'zijn', 'uit', 'aan', 'voor', 'wapen',
            'dames', 'twee', 'sous', 'cor', 'fleur', 'tasse',
            'vdn', 'undercup', 'mus', 'royaux', 'histoire'
        }
    
    def _get_core_terms(self) -> Set[str]:
        """
        Get core porcelain terminology that should be preserved
        
        Returns:
            Set of important porcelain-related terms that should not be filtered out
        """
        return {
            # Materials
            'porcelain', 'ceramic', 'pottery', 'stoneware', 'earthenware',
            'paste', 'soft paste', 'hard paste', 'clay',
            
            # Vessel shapes
            'vase', 'bowl', 'plate', 'cup', 'jar', 'pot', 'dish',
            'bottle', 'box', 'ewer', 'censer', 'teapot', 'saucer',
            'charger', 'platter', 'beaker', 'container',
            
            # Decorative elements
            'flower', 'floral', 'dragon', 'phoenix', 'bird', 'figure',
            'landscape', 'geometric', 'pattern', 'decoration', 'painted',
            'decorated', 'design', 'motif', 'depicting',
            
            # Colors
            'blue', 'white', 'red', 'green', 'yellow', 'black', 'gold',
            'brown', 'purple', 'pink', 'multicolor', 'polychrome',
            
            # Glaze and techniques
            'glaze', 'underglaze', 'overglaze', 'enamel', 'celadon',
            'famille rose', 'famille verte', 'transfer', 'printed',
            
            # Dynasties and periods
            'ming', 'qing', 'kangxi', 'qianlong', 'yongzheng', 'dynasty',
            'period', 'century', 'reign',
            
            # Production places
            'china', 'chinese', 'jingdezhen', 'export', 'canton',
            
            # Functions
            'tea', 'wine', 'ceremonial', 'decorative', 'ritual',
            
            # Marks and inscriptions
            'mark', 'base', 'inscription', 'character', 'seal'
        }
    
    def add_stopwords(self, words: List[str]):
        """
        Add custom stopwords to the filter list
        
        Args:
            words: List of words to add as stopwords
        """
        self.domain_stopwords.update(words)
        self.all_stopwords = self.stop_words.union(self.domain_stopwords)
    
    def remove_stopwords(self, words: List[str]):
        """
        Remove words from the stopword list
        
        Args:
            words: List of words to remove from stopwords
        """
        for word in words:
            self.domain_stopwords.discard(word)
        self.all_stopwords = self.stop_words.union(self.domain_stopwords)
    
    def add_core_terms(self, terms: List[str]):
        """
        Add terms to the core terminology list (protected from filtering)
        
        Args:
            terms: List of important terms to preserve
        """
        self.core_porcelain_terms.update(terms)
    
    def simple_language_detect(self, text: str) -> str:
        """
        Simple language detection based on character analysis
        
        Args:
            text: Text to analyze
            
        Returns:
            'en' for English text, 'other' for non-English text
        """
        if not text:
            return 'en'
        
        # Calculate ratio of non-ASCII characters
        non_ascii_count = sum(1 for char in text if ord(char) > 127)
        total_chars = len(text)
        
        if total_chars == 0:
            return 'en'
        
        non_ascii_ratio = non_ascii_count / total_chars
        
        # If more than 30% non-ASCII characters, likely not English
        if non_ascii_ratio > 0.3:
            return 'other'
        
        # Check for common non-English marker words
        non_english_markers = ['och', 'som', 'den', 'det', 'ett', 'med', 
                             'delle', 'della', 'dans', 'avec', 'pour', 
                             'der', 'die', 'das', 'und']
        
        text_lower = text.lower()
        marker_count = sum(1 for marker in non_english_markers 
                         if f' {marker} ' in f' {text_lower} ')
        
        # If 3 or more non-English markers found, classify as non-English
        if marker_count >= 3:
            return 'other'
        
        return 'en'
    
    def preprocess_text(self, text: str) -> str:
        """
        Main text preprocessing function
        
        Performs comprehensive text cleaning including:
        - URL and email removal
        - Metadata artifact removal
        - Language-specific processing
        - Stopword filtering
        - Token validation
        
        Args:
            text: Raw text to preprocess
            
        Returns:
            Cleaned and tokenized text string
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = str(text).lower()
        
        # Remove URLs and emails
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'www\.\S+', '', text)
        
        # Remove metadata artifacts
        metadata_patterns = [
            r'\bdef\s+\w+\b',  # Definition patterns
            r'\b\w+\s+def\b',
            r'\bdef\s+def\b',
            r'\bdnr\b',  # Document numbers
            r'\bfotogr\b',  # Photography references
            r'\binst\s+coll\b',  # Institution collection
            r'\bcoll\s+pavillon\b',  # Collection pavilion
            r'\bpavillon\s+chinois\b',  # Chinese pavilion
            r'\bchinois\s+laeken\b',  # Laeken Chinese
            r'\bdonated\s+george\b',  # Donation info
            r'\bproperty\s+of\b',  # Ownership info
            r'\bcatalogue\s+number\b',  # Catalog references
            r'\blot\s+\d+\b',  # Auction lot numbers
            r'\bref\s+\d+\b'  # Reference numbers
        ]
        
        for pattern in metadata_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Detect language
        lang = self.simple_language_detect(text)
        
        # Language-specific processing
        if lang != 'en':
            # Preserve important Chinese porcelain terms in non-English text
            important_terms = {
                'qinghua', 'ciqi', 'fencai', 'wucai', 'doucai', 'yangcai',
                'jihong', 'guan', 'ge', 'ru', 'ding', 'jun', 'cizhou',
                'longquan', 'jingdezhen', 'dehua', 'yixing', 'guangxu',
                'qianlong', 'kangxi', 'yongzheng', 'ming', 'qing', 'song',
                'yuan', 'tang', 'meiping', 'zun', 'gu', 'hu', 'guan',
                'celadon', 'porcelain', 'ceramic', 'pottery', 'stoneware'
            }
            
            # Protect important terms with placeholders
            protected_text = text
            term_placeholders = {}
            for i, term in enumerate(important_terms):
                if term in text:
                    placeholder = f"TERM{i}"
                    term_placeholders[placeholder] = term
                    protected_text = protected_text.replace(term, placeholder)
            
            # Keep only ASCII characters and spaces
            protected_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', protected_text)
            
            # Restore protected terms
            for placeholder, term in term_placeholders.items():
                protected_text = protected_text.replace(placeholder, term)
            
            text = protected_text
        else:
            # For English text, remove non-alphabetic characters but keep spaces
            text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Remove excess whitespace
        text = ' '.join(text.split())
        
        # Tokenize
        tokens = text.split()
        
        # Filter tokens
        filtered_tokens = []
        for token in tokens:
            # Always preserve core porcelain terms
            if token in self.core_porcelain_terms:
                filtered_tokens.append(token)
                continue
                
            # Skip stopwords
            if token in self.all_stopwords:
                continue
                
            # Skip tokens that are too short or too long
            if len(token) <= 2 or len(token) > 20:
                continue
                
            # Skip pure numbers
            if token.isdigit():
                continue
                
            # Skip tokens with all identical characters
            if len(set(token)) == 1:
                continue
            
            filtered_tokens.append(token)
        
        return ' '.join(filtered_tokens)
    
    def extract_text_from_item(self, item: Dict[str, Any]) -> str:
        """
        Extract text from a data item
        
        Extracts and combines text from multiple fields with priority ordering
        and language preference for English content.
        
        Args:
            item: Dictionary containing metadata fields
            
        Returns:
            Combined text string from relevant fields
        """
        text_parts = []
        
        # Priority order for field extraction
        priority_fields = [
            ('dcDescription', True),  # (field_name, is_list)
            ('description', True),
            ('dcTitle', True),
            ('title', True),
            ('edmConceptLabel', True),
            ('conceptLabel', True)
        ]
        
        for field_name, is_list in priority_fields:
            if field_name in item:
                field_data = item[field_name]
                if is_list and isinstance(field_data, list):
                    # Prioritize English content
                    english_parts = []
                    other_parts = []
                    
                    for part in field_data:
                        if part and isinstance(part, str):
                            lang = self.simple_language_detect(str(part))
                            if lang == 'en':
                                english_parts.append(str(part))
                            else:
                                other_parts.append(str(part))
                    
                    # Add English parts first
                    text_parts.extend(english_parts)
                    # If no English content, add up to 2 non-English parts
                    if not english_parts:
                        text_parts.extend(other_parts[:2])
                        
                elif field_data and isinstance(field_data, str):
                    text_parts.append(field_data)
        
        # Combine all text parts
        combined_text = ' '.join([str(t) for t in text_parts if t])
        
        # Limit text length to prevent memory issues
        max_length = 2000
        if len(combined_text) > max_length:
            combined_text = combined_text[:max_length]
        
        return combined_text
