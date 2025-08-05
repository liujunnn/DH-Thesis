#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LDA训练模块
功能：LDA模型训练、困惑度分析、参数优化
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from collections import Counter

class LDATrainer:
    """LDA训练器"""
    
    def __init__(self, n_topics: Optional[int] = None):
        self.n_topics = n_topics
        self.lda_model = None
        self.vectorizer = None
        self.tfidf_vectorizer = None
        self.optimal_topics = None
        self.topic_labels = {}
    
    def find_optimal_topics(self, texts: List[str], 
                        min_topics: int = 5, 
                        max_topics: int = 20) -> int:
        """使用困惑度找到最佳主题数"""
        print(f"\n🔍 寻找最佳主题数 (范围: {min_topics}-{max_topics})...")
        
        if len(texts) < 50:
            print("⚠️  文本数量太少，使用默认主题数: 10")
            return 10
        
        # 创建词袋模型
        temp_vectorizer = CountVectorizer(
            max_df=0.7,
            min_df=5,
            max_features=500,
            ngram_range=(1, 2),
            token_pattern=r'\b[a-zA-Z]{3,}\b'
        )
        
        doc_term_matrix = temp_vectorizer.fit_transform(texts)
        
        # 计算不同主题数的困惑度
        perplexities = []
        coherences = []
        topic_range = range(min_topics, max_topics + 1)
        
        for n_topic in topic_range:
            print(f"  测试主题数: {n_topic}", end='')
            
            # 训练LDA模型
            lda = LatentDirichletAllocation(
                n_components=n_topic,
                random_state=42,
                max_iter=100,
                learning_method='batch',
                doc_topic_prior=0.05,  # alpha
                topic_word_prior=0.001,  # beta
                n_jobs=-1
            )
            
            lda.fit(doc_term_matrix)
            
            # 计算困惑度
            perplexity = lda.perplexity(doc_term_matrix)
            perplexities.append(perplexity)
            
            # 计算主题一致性
            coherence = self._calculate_topic_coherence(lda, temp_vectorizer, texts)
            coherences.append(coherence)
            
            print(f" - 困惑度: {perplexity:.2f}, 一致性: {coherence:.3f}")
        
        # 找到最佳主题数
        optimal_topics = self._find_elbow_point(topic_range, perplexities, coherences)
        
        print(f"\n✅ 最佳主题数: {optimal_topics}")
        
        return optimal_topics
    
    def _calculate_topic_coherence(self, lda_model, vectorizer, texts: List[str]) -> float:
        """计算主题一致性"""
        feature_names = vectorizer.get_feature_names_out()
        coherence_scores = []
        
        for topic_idx in range(lda_model.n_components):
            # 获取主题中概率最高的10个词
            top_word_indices = lda_model.components_[topic_idx].argsort()[-10:][::-1]
            top_words = [feature_names[i] for i in top_word_indices]
            
            # 计算词对共现
            word_pairs = [(top_words[i], top_words[j]) 
                         for i in range(len(top_words)) 
                         for j in range(i+1, len(top_words))]
            
            pair_scores = []
            for w1, w2 in word_pairs[:10]:
                co_occur = sum(1 for text in texts if w1 in text and w2 in text)
                occur_w1 = sum(1 for text in texts if w1 in text)
                
                if occur_w1 > 0:
                    score = co_occur / occur_w1
                    pair_scores.append(score)
            
            if pair_scores:
                coherence_scores.append(np.mean(pair_scores))
        
        return np.mean(coherence_scores) if coherence_scores else 0.0
    
    def _find_elbow_point(self, topic_range, perplexities, coherences) -> int:
        """找到肘部点（最佳主题数）"""
        # 标准化指标
        perp_normalized = (np.array(perplexities) - np.min(perplexities)) / (np.max(perplexities) - np.min(perplexities))
        coh_normalized = (np.array(coherences) - np.min(coherences)) / (np.max(coherences) - np.min(coherences))
        
        # 组合指标
        combined_score = perp_normalized - coh_normalized
        
        # 计算二阶导数找拐点
        if len(combined_score) > 2:
            second_derivative = np.diff(np.diff(combined_score))
            elbow_index = np.argmax(second_derivative) + 2
            elbow_index = min(elbow_index, len(topic_range) - 1)
        else:
            elbow_index = len(topic_range) // 2
        
        return list(topic_range)[elbow_index]
    
    def train_lda(self, texts: List[str], use_optimal_topics: bool = True):
        """训练LDA模型"""
        print("\n🚀 训练LDA模型...")
        
        if len(texts) < 10:
            print("⚠️  有效文本太少，跳过LDA训练")
            return
        
        print(f"📊 训练文本数: {len(texts)}")
        
        # 确定主题数
        if use_optimal_topics and self.n_topics is None:
            self.n_topics = self.find_optimal_topics(texts, min_topics=8, max_topics=20)
        elif self.n_topics is None:
            self.n_topics = 15
        
        # 创建词袋模型
        self.vectorizer = CountVectorizer(
            max_df=0.7,
            min_df=5,
            max_features=500,
            ngram_range=(1, 2),
            token_pattern=r'\b[a-zA-Z]{3,}\b'
        )
        
        # 创建TF-IDF模型
        self.tfidf_vectorizer = TfidfVectorizer(
            max_df=0.7,
            min_df=5,
            max_features=500,
            ngram_range=(1, 2),
            token_pattern=r'\b[a-zA-Z]{3,}\b'
        )
        
        try:
            # 训练词袋模型
            doc_term_matrix = self.vectorizer.fit_transform(texts)
            
            # 检查词汇表大小
            vocab_size = len(self.vectorizer.get_feature_names_out())
            print(f"📖 词汇表大小: {vocab_size}")
            
            # 训练TF-IDF模型
            self.tfidf_vectorizer.fit_transform(texts)
            
            # 训练LDA模型
            self.lda_model = LatentDirichletAllocation(
                n_components=self.n_topics,
                random_state=42,
                max_iter=200,
                learning_method='batch',
                learning_offset=10.0,
                doc_topic_prior=0.05,  # alpha
                topic_word_prior=0.001,  # beta
                n_jobs=-1
            )
            
            self.lda_model.fit(doc_term_matrix)
            
            print("✅ LDA模型训练完成")
            
            # 打印主题摘要
            print(f"\n📋 主题摘要 ({self.n_topics} 个主题):")
            for topic_id in range(self.n_topics):
                top_words = self.get_topic_words(topic_id, n_words=5)
                words = [word for word, _ in top_words]
                print(f"  主题 {topic_id + 1}: {', '.join(words)}")
            
        except Exception as e:
            print(f"❌ LDA训练失败: {e}")
            self.lda_model = None
    
    def get_document_topics(self, text: str) -> List[Dict]:
        """获取文档的主题分布"""
        if not self.lda_model or not self.vectorizer:
            return []
        
        try:
            doc_vector = self.vectorizer.transform([text])
            
            if doc_vector.nnz > 0:
                topic_dist = self.lda_model.transform(doc_vector)[0]
                
                topics = []
                for idx, prob in enumerate(topic_dist):
                    if prob > 0.15:  # 阈值
                        topics.append({
                            'topic_id': idx,
                            'probability': float(prob)
                        })
                
                topics.sort(key=lambda x: x['probability'], reverse=True)
                return topics[:3]
                
        except:
            pass
        
        return []
    
    def get_topic_words(self, topic_id: int, n_words: int = 10) -> List[Tuple[str, float]]:
        """获取主题的关键词"""
        if not self.lda_model or not self.vectorizer:
            return []
        
        feature_names = self.vectorizer.get_feature_names_out()
        topic = self.lda_model.components_[topic_id]
        top_indices = topic.argsort()[-n_words:][::-1]
        
        words_weights = []
        for idx in top_indices:
            words_weights.append((feature_names[idx], topic[idx]))
        
        return words_weights
    
    def extract_keywords_tfidf(self, texts: List[str], top_n: int = 20) -> List[Tuple[str, float]]:
        """使用TF-IDF提取关键词"""
        if not texts or not self.tfidf_vectorizer:
            return []
        
        try:
            tfidf_matrix = self.tfidf_vectorizer.transform(texts)
            feature_names = self.tfidf_vectorizer.get_feature_names_out()
            
            # 计算平均TF-IDF分数
            avg_tfidf = np.mean(tfidf_matrix.toarray(), axis=0)
            
            # 获取top_n个关键词
            top_indices = avg_tfidf.argsort()[-top_n:][::-1]
            
            keywords = [(feature_names[i], avg_tfidf[i]) for i in top_indices]
            return keywords
        except:
            return []