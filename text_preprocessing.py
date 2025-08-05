#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本预处理模块
功能：停用词管理、文本清洗、分词等
"""

import re
from typing import Set, List, Dict, Any
import nltk
from nltk.corpus import stopwords

try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

class TextPreprocessor:
    """文本预处理器"""
    
    def __init__(self):
        # 初始化停用词
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = self._get_default_stopwords()
        
        # 领域特定停用词
        self.domain_stopwords = self._get_domain_stopwords()
        
        # 合并所有停用词
        self.all_stopwords = self.stop_words.union(self.domain_stopwords)
        
        # 核心瓷器术语（不被过滤）
        self.core_porcelain_terms = self._get_core_terms()
    
    def _get_default_stopwords(self) -> Set[str]:
        """获取默认英语停用词"""
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
        """获取领域特定停用词"""
        return {
            # 多语言常见词
            'def', 'och', 'som', 'den', 'det', 'ett', 'med', 'par', 'fut',
            'lieu', 'een', 'met', 'del', 'della', 'delle', 'dei', 'nel',
            'pour', 'dans', 'avec', 'sur', 'une', 'les', 'ces', 'von', 'mit',
            'der', 'die', 'das', 'und', 'ist', 'sind', 'wird', 'wurde',
            
            # 元数据相关
            'note', 'vente', 'document', 'genre', 'fotogr', 'dnr', 'email',
            'http', 'edu', 'aat', 'vocab', 'getty', 'url', 'link', 'site',
            'item', 'object', 'artifact', 'collection', 'museum', 'archive',
            'unknown', 'unclear', 'possibly', 'probably', 'various', 'similar',
            
            # 机构相关
            'inst', 'coll', 'inv', 'donated', 'property', 'catalogue',
            'old', 'english', 'furniture', 'art', 'pavillon', 'laeken',
            'inventory', 'acquisition', 'bequest', 'gift', 'purchase',
            'accession', 'provenance', 'formerly', 'estate', 'sale', 'lot',
            'bijlokemuseum', 'kulturstyrelsen', 'gent', 'ghent',
            'stockholm', 'bruxelles', 'amsterdam', 'london', 'paris',
            'sotheby', 'christie', 'puttick', 'simpson', 'woods', 'manson',
            
            # 非英语瓷器通用词
            'porcel', 'kinesisk', 'porslin', 'porselein', 'porcellana',
            'teller', 'coupe', 'schale', 'piatto', 'assiette',
            'bodenmarke', 'dekor', 'fond',
            
            # 其他
            'van', 'het', 'zijn', 'uit', 'aan', 'voor', 'wapen',
            'dames', 'twee', 'sous', 'cor', 'fleur', 'tasse',
            'vdn', 'undercup', 'mus', 'royaux', 'histoire'
        }
    
    def _get_core_terms(self) -> Set[str]:
        """获取核心瓷器术语（不应被过滤）"""
        return {
            # 材质
            'porcelain', 'ceramic', 'pottery', 'stoneware', 'earthenware',
            'paste', 'soft paste', 'hard paste', 'clay',
            
            # 器形
            'vase', 'bowl', 'plate', 'cup', 'jar', 'pot', 'dish',
            'bottle', 'box', 'ewer', 'censer', 'teapot', 'saucer',
            'charger', 'platter', 'beaker', 'container',
            
            # 装饰
            'flower', 'floral', 'dragon', 'phoenix', 'bird', 'figure',
            'landscape', 'geometric', 'pattern', 'decoration', 'painted',
            'decorated', 'design', 'motif', 'depicting',
            
            # 颜色
            'blue', 'white', 'red', 'green', 'yellow', 'black', 'gold',
            'brown', 'purple', 'pink', 'multicolor', 'polychrome',
            
            # 釉色技术
            'glaze', 'underglaze', 'overglaze', 'enamel', 'celadon',
            'famille rose', 'famille verte', 'transfer', 'printed',
            
            # 朝代时期
            'ming', 'qing', 'kangxi', 'qianlong', 'yongzheng', 'dynasty',
            'period', 'century', 'reign',
            
            # 产地
            'china', 'chinese', 'jingdezhen', 'export', 'canton',
            
            # 功能
            'tea', 'wine', 'ceremonial', 'decorative', 'ritual',
            
            # 款识
            'mark', 'base', 'inscription', 'character', 'seal'
        }
    
    def add_stopwords(self, words: List[str]):
        """添加自定义停用词"""
        self.domain_stopwords.update(words)
        self.all_stopwords = self.stop_words.union(self.domain_stopwords)
    
    def remove_stopwords(self, words: List[str]):
        """移除停用词"""
        for word in words:
            self.domain_stopwords.discard(word)
        self.all_stopwords = self.stop_words.union(self.domain_stopwords)
    
    def add_core_terms(self, terms: List[str]):
        """添加核心术语"""
        self.core_porcelain_terms.update(terms)
    
    def simple_language_detect(self, text: str) -> str:
        """简单的语言检测"""
        if not text:
            return 'en'
        
        # 计算非ASCII字符的比例
        non_ascii_count = sum(1 for char in text if ord(char) > 127)
        total_chars = len(text)
        
        if total_chars == 0:
            return 'en'
        
        non_ascii_ratio = non_ascii_count / total_chars
        
        # 如果非ASCII字符超过30%，认为不是英语
        if non_ascii_ratio > 0.3:
            return 'other'
        
        # 检查常见的非英语词汇
        non_english_markers = ['och', 'som', 'den', 'det', 'ett', 'med', 
                             'delle', 'della', 'dans', 'avec', 'pour', 
                             'der', 'die', 'das', 'und']
        
        text_lower = text.lower()
        marker_count = sum(1 for marker in non_english_markers 
                         if f' {marker} ' in f' {text_lower} ')
        
        if marker_count >= 3:
            return 'other'
        
        return 'en'
    
    def preprocess_text(self, text: str) -> str:
        """主要的文本预处理函数"""
        if not text:
            return ""
        
        # 转小写
        text = str(text).lower()
        
        # 移除URLs和email
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'www\.\S+', '', text)
        
        # 移除元数据伪影
        metadata_patterns = [
            r'\bdef\s+\w+\b',
            r'\b\w+\s+def\b',
            r'\bdef\s+def\b',
            r'\bdnr\b',
            r'\bfotogr\b',
            r'\binst\s+coll\b',
            r'\bcoll\s+pavillon\b',
            r'\bpavillon\s+chinois\b',
            r'\bchinois\s+laeken\b',
            r'\bdonated\s+george\b',
            r'\bproperty\s+of\b',
            r'\bcatalogue\s+number\b',
            r'\blot\s+\d+\b',
            r'\bref\s+\d+\b'
        ]
        
        for pattern in metadata_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # 检测语言
        lang = self.simple_language_detect(text)
        
        # 如果不是英语，进行特殊处理
        if lang != 'en':
            # 保留重要的瓷器相关术语
            important_terms = {
                'qinghua', 'ciqi', 'fencai', 'wucai', 'doucai', 'yangcai',
                'jihong', 'guan', 'ge', 'ru', 'ding', 'jun', 'cizhou',
                'longquan', 'jingdezhen', 'dehua', 'yixing', 'guangxu',
                'qianlong', 'kangxi', 'yongzheng', 'ming', 'qing', 'song',
                'yuan', 'tang', 'meiping', 'zun', 'gu', 'hu', 'guan',
                'celadon', 'porcelain', 'ceramic', 'pottery', 'stoneware'
            }
            
            # 保护重要术语
            protected_text = text
            term_placeholders = {}
            for i, term in enumerate(important_terms):
                if term in text:
                    placeholder = f"TERM{i}"
                    term_placeholders[placeholder] = term
                    protected_text = protected_text.replace(term, placeholder)
            
            # 只保留ASCII字符
            protected_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', protected_text)
            
            # 恢复保护的术语
            for placeholder, term in term_placeholders.items():
                protected_text = protected_text.replace(placeholder, term)
            
            text = protected_text
        else:
            # 对于英语文本，移除非字母字符但保留空格
            text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # 移除多余空格
        text = ' '.join(text.split())
        
        # 分词并过滤
        tokens = text.split()
        
        # 过滤tokens
        filtered_tokens = []
        for token in tokens:
            # 保留核心瓷器术语
            if token in self.core_porcelain_terms:
                filtered_tokens.append(token)
                continue
                
            # 跳过停用词
            if token in self.all_stopwords:
                continue
                
            # 跳过太短或太长的词
            if len(token) <= 2 or len(token) > 20:
                continue
                
            # 跳过纯数字
            if token.isdigit():
                continue
                
            # 跳过重复字符的词
            if len(set(token)) == 1:
                continue
            
            filtered_tokens.append(token)
        
        return ' '.join(filtered_tokens)
    
    def extract_text_from_item(self, item: Dict[str, Any]) -> str:
        """从数据项提取文本"""
        text_parts = []
        
        # 优先级顺序
        priority_fields = [
            ('dcDescription', True),
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
                    # 优先选择英语内容
                    english_parts = []
                    other_parts = []
                    
                    for part in field_data:
                        if part and isinstance(part, str):
                            lang = self.simple_language_detect(str(part))
                            if lang == 'en':
                                english_parts.append(str(part))
                            else:
                                other_parts.append(str(part))
                    
                    text_parts.extend(english_parts)
                    if not english_parts:
                        text_parts.extend(other_parts[:2])
                        
                elif field_data and isinstance(field_data, str):
                    text_parts.append(field_data)
        
        # 合并文本
        combined_text = ' '.join([str(t) for t in text_parts if t])
        
        # 限制长度
        max_length = 2000
        if len(combined_text) > max_length:
            combined_text = combined_text[:max_length]
        
        return combined_text