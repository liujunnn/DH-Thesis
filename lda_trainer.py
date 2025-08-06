#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from typing import List, Dict, Tuple, Optional
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from collections import Counter

class LDATrainer:
    """
    Latent Dirichlet Allocation (LDA) Trainer
    
    This class provides functionality for training LDA topic models,
    finding optimal number of topics, and extracting topic distributions
    and keywords from documents.
    """
    
    def __init__(self, n_topics: Optional[int] = None):
        """
        Initialize the LDA Trainer
        
        Args:
            n_topics: Number of topics for LDA model. If None, will be determined automatically.
        """
        self.n_topics = n_topics
        self.lda_model = None
        self.vectorizer = None
        self.tfidf_vectorizer = None
        self.optimal_topics = None
        self.topic_labels = {}
    
    def find_optimal_topics(self, texts: List[str], 
                        min_topics: int = 5, 
                        max_topics: int = 20) -> int:
        """
        Find optimal number of topics using perplexity and coherence scores
        
        Args:
            texts: List of document texts
            min_topics: Minimum number of topics to evaluate
            max_topics: Maximum number of topics to evaluate
            
        Returns:
            Optimal number of topics based on elbow method
        """
        print(f"\n🔍 Finding optimal number of topics (range: {min_topics}-{max_topics})...")
        
        # Check if we have enough documents for meaningful topic modeling
        if len(texts) < 50:
            print("⚠️  Insufficient text samples, using default topic count: 10")
            return 10
        
        # Create bag-of-words model for topic evaluation
        temp_vectorizer = CountVectorizer(
            max_df=0.7,  # Ignore terms that appear in more than 70% of documents
            min_df=5,    # Ignore terms that appear in less than 5 documents
            max_features=500,  # Limit vocabulary size
            ngram_range=(1, 2),  # Use both unigrams and bigrams
            token_pattern=r'\b[a-zA-Z]{3,}\b'  # Words with at least 3 letters
        )
        
        doc_term_matrix = temp_vectorizer.fit_transform(texts)
        
        # Calculate perplexity and coherence for different topic counts
        perplexities = []
        coherences = []
        topic_range = range(min_topics, max_topics + 1)
        
        for n_topic in topic_range:
            print(f"  Testing topic count: {n_topic}", end='')
            
            # Train LDA model with current topic count
            lda = LatentDirichletAllocation(
                n_components=n_topic,
                random_state=42,  # For reproducibility
                max_iter=100,
                learning_method='batch',
                doc_topic_prior=0.05,  # Alpha parameter - document-topic density
                topic_word_prior=0.001,  # Beta parameter - topic-word density
                n_jobs=-1  # Use all available CPU cores
            )
            
            lda.fit(doc_term_matrix)
            
            # Calculate perplexity (lower is better)
            perplexity = lda.perplexity(doc_term_matrix)
            perplexities.append(perplexity)
            
            # Calculate topic coherence (higher is better)
            coherence = self._calculate_topic_coherence(lda, temp_vectorizer, texts)
            coherences.append(coherence)
            
            print(f" - Perplexity: {perplexity:.2f}, Coherence: {coherence:.3f}")
        
        # Find optimal topic count using elbow method
        optimal_topics = self._find_elbow_point(topic_range, perplexities, coherences)
        
        print(f"\n✅ Optimal number of topics: {optimal_topics}")
        
        return optimal_topics
    
    def _calculate_topic_coherence(self, lda_model, vectorizer, texts: List[str]) -> float:
        """
        Calculate topic coherence score
        
        Topic coherence measures how semantically similar the top words
        in a topic are to each other. Higher coherence indicates better topics.
        
        Args:
            lda_model: Trained LDA model
            vectorizer: Fitted CountVectorizer
            texts: Original text documents
            
        Returns:
            Average coherence score across all topics
        """
        feature_names = vectorizer.get_feature_names_out()
        coherence_scores = []
        
        for topic_idx in range(lda_model.n_components):
            # Get top 10 words with highest probability in this topic
            top_word_indices = lda_model.components_[topic_idx].argsort()[-10:][::-1]
            top_words = [feature_names[i] for i in top_word_indices]
            
            # Calculate co-occurrence for word pairs
            word_pairs = [(top_words[i], top_words[j]) 
                         for i in range(len(top_words)) 
                         for j in range(i+1, len(top_words))]
            
            # Calculate PMI (Pointwise Mutual Information) based coherence
            pair_scores = []
            for w1, w2 in word_pairs[:10]:  # Use top 10 pairs
                co_occur = sum(1 for text in texts if w1 in text and w2 in text)
                occur_w1 = sum(1 for text in texts if w1 in text)
                
                if occur_w1 > 0:
                    score = co_occur / occur_w1
                    pair_scores.append(score)
            
            if pair_scores:
                coherence_scores.append(np.mean(pair_scores))
        
        return np.mean(coherence_scores) if coherence_scores else 0.0
    
    def _find_elbow_point(self, topic_range, perplexities, coherences) -> int:
        """
        Find elbow point (optimal number of topics) using combined metrics
        
        Args:
            topic_range: Range of topic numbers tested
            perplexities: List of perplexity scores
            coherences: List of coherence scores
            
        Returns:
            Optimal number of topics
        """
        # Normalize metrics to [0, 1] range
        perp_normalized = (np.array(perplexities) - np.min(perplexities)) / (np.max(perplexities) - np.min(perplexities))
        coh_normalized = (np.array(coherences) - np.min(coherences)) / (np.max(coherences) - np.min(coherences))
        
        # Combine metrics (minimize perplexity, maximize coherence)
        combined_score = perp_normalized - coh_normalized
        
        # Find elbow point using second derivative
        if len(combined_score) > 2:
            second_derivative = np.diff(np.diff(combined_score))
            elbow_index = np.argmax(second_derivative) + 2
            elbow_index = min(elbow_index, len(topic_range) - 1)
        else:
            elbow_index = len(topic_range) // 2
        
        return list(topic_range)[elbow_index]
    
    def train_lda(self, texts: List[str], use_optimal_topics: bool = True):
        """
        Train LDA model on provided texts
        
        Args:
            texts: List of document texts for training
            use_optimal_topics: Whether to automatically determine optimal topic count
        """
        print("\n🚀 Training LDA model...")
        
        # Check minimum document requirement
        if len(texts) < 10:
            print("⚠️  Too few valid texts, skipping LDA training")
            return
        
        print(f"📊 Number of training documents: {len(texts)}")
        
        # Determine number of topics
        if use_optimal_topics and self.n_topics is None:
            self.n_topics = self.find_optimal_topics(texts, min_topics=8, max_topics=20)
        elif self.n_topics is None:
            self.n_topics = 15  # Default fallback
        
        # Create Bag-of-Words model
        self.vectorizer = CountVectorizer(
            max_df=0.7,  # Remove words appearing in >70% of docs (too common)
            min_df=5,    # Remove words appearing in <5 docs (too rare)
            max_features=500,  # Limit vocabulary for computational efficiency
            ngram_range=(1, 2),  # Include both single words and bigrams
            token_pattern=r'\b[a-zA-Z]{3,}\b'  # Only words with 3+ letters
        )
        
        # Create TF-IDF model for keyword extraction
        self.tfidf_vectorizer = TfidfVectorizer(
            max_df=0.7,
            min_df=5,
            max_features=500,
            ngram_range=(1, 2),
            token_pattern=r'\b[a-zA-Z]{3,}\b'
        )
        
        try:
            # Fit vectorizer and transform documents to term-document matrix
            doc_term_matrix = self.vectorizer.fit_transform(texts)
            
            # Check vocabulary size
            vocab_size = len(self.vectorizer.get_feature_names_out())
            print(f"📖 Vocabulary size: {vocab_size}")
            
            # Fit TF-IDF model
            self.tfidf_vectorizer.fit_transform(texts)
            
            # Train LDA model
            self.lda_model = LatentDirichletAllocation(
                n_components=self.n_topics,
                random_state=42,  # Ensure reproducibility
                max_iter=200,  # Maximum iterations for convergence
                learning_method='batch',  # Use batch learning for better accuracy
                learning_offset=10.0,  # Learning rate offset
                doc_topic_prior=0.05,  # Alpha - controls document-topic sparsity
                topic_word_prior=0.001,  # Beta - controls topic-word sparsity
                n_jobs=-1  # Utilize all CPU cores
            )
            
            self.lda_model.fit(doc_term_matrix)
            
            print("✅ LDA model training completed")
            
            # Print topic summary
            print(f"\n📋 Topic Summary ({self.n_topics} topics):")
            for topic_id in range(self.n_topics):
                top_words = self.get_topic_words(topic_id, n_words=5)
                words = [word for word, _ in top_words]
                print(f"  Topic {topic_id + 1}: {', '.join(words)}")
            
        except Exception as e:
            print(f"❌ LDA training failed: {e}")
            self.lda_model = None
    
    def get_document_topics(self, text: str) -> List[Dict]:
        """
        Get topic distribution for a single document
        
        Args:
            text: Document text to analyze
            
        Returns:
            List of dictionaries containing topic_id and probability,
            sorted by probability in descending order
        """
        if not self.lda_model or not self.vectorizer:
            return []
        
        try:
            # Transform document to vector representation
            doc_vector = self.vectorizer.transform([text])
            
            # Check if document contains known vocabulary
            if doc_vector.nnz > 0:  # nnz = number of non-zero elements
                # Get topic distribution for this document
                topic_dist = self.lda_model.transform(doc_vector)[0]
                
                topics = []
                for idx, prob in enumerate(topic_dist):
                    if prob > 0.15:  # Threshold for significant topics
                        topics.append({
                            'topic_id': idx,
                            'probability': float(prob)
                        })
                
                # Sort by probability and return top 3 topics
                topics.sort(key=lambda x: x['probability'], reverse=True)
                return topics[:3]
                
        except:
            pass
        
        return []
    
    def get_topic_words(self, topic_id: int, n_words: int = 10) -> List[Tuple[str, float]]:
        """
        Get top words for a specific topic
        
        Args:
            topic_id: Index of the topic
            n_words: Number of top words to return
            
        Returns:
            List of (word, weight) tuples sorted by weight
        """
        if not self.lda_model or not self.vectorizer:
            return []
        
        # Get vocabulary
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Get word distribution for this topic
        topic = self.lda_model.components_[topic_id]
        
        # Get indices of top words
        top_indices = topic.argsort()[-n_words:][::-1]
        
        # Create list of (word, weight) pairs
        words_weights = []
        for idx in top_indices:
            words_weights.append((feature_names[idx], topic[idx]))
        
        return words_weights
    
    def extract_keywords_tfidf(self, texts: List[str], top_n: int = 20) -> List[Tuple[str, float]]:
        """
        Extract keywords using TF-IDF scores
        
        TF-IDF (Term Frequency-Inverse Document Frequency) identifies
        words that are important in the document collection.
        
        Args:
            texts: List of documents to extract keywords from
            top_n: Number of top keywords to return
            
        Returns:
            List of (keyword, tfidf_score) tuples sorted by score
        """
        if not texts or not self.tfidf_vectorizer:
            return []
        
        try:
            # Transform texts to TF-IDF matrix
            tfidf_matrix = self.tfidf_vectorizer.transform(texts)
            feature_names = self.tfidf_vectorizer.get_feature_names_out()
            
            # Calculate average TF-IDF score across all documents
            avg_tfidf = np.mean(tfidf_matrix.toarray(), axis=0)
            
            # Get indices of top_n keywords
            top_indices = avg_tfidf.argsort()[-top_n:][::-1]
            
            # Create list of (keyword, score) pairs
            keywords = [(feature_names[i], avg_tfidf[i]) for i in top_indices]
            return keywords
        except:
            # Return empty list if extraction fails
            return []
