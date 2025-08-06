#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Processing Module

Integrates all modules to execute the complete data processing pipeline
for Chinese porcelain metadata analysis.
"""
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='joblib')

import json
from typing import Dict, Any
from text_preprocessing import TextPreprocessor
from lda_trainer import LDATrainer
from keyword_dictionary import KeywordDictionary
from data_mapper import DataMapper
from report_generator import ReportGenerator

class PorcelainProcessor:
    """
    Main processor for Chinese porcelain data
    
    This class orchestrates the entire processing pipeline including:
    - Text preprocessing
    - LDA topic modeling
    - Keyword extraction
    - Data mapping and structuring
    - Report generation
    """
    
    def __init__(self, keyword_config: str = None):
        """
        Initialize all processing modules
        
        Args:
            keyword_config: Optional path to keyword configuration file
        """
        # Initialize all processing modules
        self.preprocessor = TextPreprocessor()
        self.lda_trainer = LDATrainer()
        self.keyword_dict = KeywordDictionary(keyword_config)
        self.mapper = DataMapper(self.keyword_dict)
        self.report_gen = ReportGenerator()
    
    def process_dataset(self, input_file: str, output_file: str, 
                       use_optimal_topics: bool = True) -> Dict[str, Any]:
        """
        Process the entire dataset through the complete pipeline
        
        Args:
            input_file: Path to input JSON file containing raw porcelain data
            output_file: Path where processed data will be saved
            use_optimal_topics: Whether to automatically determine optimal topic count for LDA
            
        Returns:
            Dictionary containing processing statistics
        """
        try:
            print(f"📁 Loading data: {input_file}")
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"📊 Data volume: {len(data)} records")
            
        except Exception as e:
            print(f"❌ Failed to load file: {e}")
            return {}
        
        # 1. Text Preprocessing Phase
        print("\n🔍 Preparing text data...")
        all_texts = []  # Store all raw texts
        processed_texts = []  # Store preprocessed texts for LDA
        
        for item in data:
            # Extract raw text from item
            raw_text = self.preprocessor.extract_text_from_item(item)
            all_texts.append(raw_text)
            
            # Preprocess text (tokenization, cleaning, etc.)
            processed_text = self.preprocessor.preprocess_text(raw_text)
            if processed_text:
                processed_texts.append(processed_text)
        
        print(f"Total texts: {len(all_texts)}")
        print(f"Valid processed texts: {len(processed_texts)}")
        
        # 2. LDA Training Phase
        if processed_texts:
            self.lda_trainer.train_lda(processed_texts, use_optimal_topics)
        
        # 3. Data Mapping Phase
        processed_data = []
        stats = self._init_stats()
        
        print("\n🔄 Starting data mapping...")
        for i, item in enumerate(data):
            # Progress indicator for large datasets
            if i % 100 == 0:
                print(f"Processing progress: {i}/{len(data)} ({i/len(data)*100:.1f}%)")
            
            # Get text for current item
            raw_text = all_texts[i]
            processed_text = self.preprocessor.preprocess_text(raw_text)
            
            # Extract LDA topics if model is trained
            lda_topics = None
            if self.lda_trainer.lda_model and processed_text:
                lda_topics = self.lda_trainer.get_document_topics(processed_text)
            
            # Map item to structured format
            result = self.mapper.process_item(item, raw_text, lda_topics)
            
            # Update statistics based on processing results
            if 'error' not in result.get('ProcessingMetadata', {}):
                processed_data.append(result)
                self._update_stats(stats, result)
            else:
                stats['errors'] += 1
        
        # 4. Save Results Phase
        self._save_results(output_file, processed_data, stats)
        
        # 5. Print Statistics Summary
        self._print_statistics(stats)
        
        return stats
    
    def _init_stats(self) -> Dict[str, Any]:
        """
        Initialize statistics tracking dictionary
        
        Returns:
            Dictionary with initialized counters for various metrics
        """
        return {
            'total': 0,  # Total number of records
            'processed': 0,  # Successfully processed records
            'with_decorations': 0,  # Records with decoration information
            'with_shape': 0,  # Records with shape information
            'with_function': 0,  # Records with function information
            'with_inscriptions': 0,  # Records with inscription marks
            'with_color': 0,  # Records with color information
            'with_glaze': 0,  # Records with glaze information
            'with_place': 0,  # Records with production place
            'with_topics': 0,  # Records with LDA topics
            'high_quality': 0,  # Records with high quality score
            'errors': 0  # Processing errors
        }
    
    def _update_stats(self, stats: Dict[str, Any], result: Dict[str, Any]):
        """
        Update statistics based on processed item
        
        Args:
            stats: Statistics dictionary to update
            result: Processed item result containing extracted metadata
        """
        stats['processed'] += 1
        desc_meta = result.get('DescriptiveMetadata', {})
        
        # Check presence of various fields
        if desc_meta.get('Decorations'):
            stats['with_decorations'] += 1
        if desc_meta.get('Shape'):
            stats['with_shape'] += 1
        if desc_meta.get('Function'):
            stats['with_function'] += 1
        if desc_meta.get('Inscriptions'):
            stats['with_inscriptions'] += 1
        if desc_meta.get('ColoredDrawing'):
            stats['with_color'] += 1
        if desc_meta.get('Glaze'):
            stats['with_glaze'] += 1
        if desc_meta.get('ProductionPlace'):
            stats['with_place'] += 1
        if desc_meta.get('lda_topics'):
            stats['with_topics'] += 1
        
        # Track high quality records
        quality_score = desc_meta.get('quality_score', 0)
        if quality_score > 0.5:  # Quality threshold
            stats['high_quality'] += 1
    
    def _save_results(self, output_file: str, processed_data: list[Dict], 
                     stats: Dict[str, Any]):
        """
        Save processing results to files
        
        Args:
            output_file: Main output file path
            processed_data: List of processed items
            stats: Processing statistics
        """
        try:
            # Save main processed data
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=2)
            print(f"\n💾 Processing results saved to: {output_file}")
            
            # Save statistics summary
            stats_file = output_file.replace('.json', '_stats.json')
            stats['total'] = len(processed_data) + stats['errors']
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            print(f"📊 Statistics saved to: {stats_file}")
            
            # Save LDA model information
            if self.lda_trainer.lda_model:
                lda_info = {
                    'n_topics': self.lda_trainer.n_topics,
                    'optimal_topics': self.lda_trainer.optimal_topics,
                    'vocabulary_size': len(self.lda_trainer.vectorizer.get_feature_names_out())
                        if self.lda_trainer.vectorizer else 0
                }
                lda_file = output_file.replace('.json', '_lda_info.json')
                with open(lda_file, 'w', encoding='utf-8') as f:
                    json.dump(lda_info, f, ensure_ascii=False, indent=2)
                print(f"🏷️  LDA information saved to: {lda_file}")
            
        except Exception as e:
            print(f"❌ Failed to save files: {e}")
    
    def _print_statistics(self, stats: Dict[str, Any]):
        """
        Print formatted statistics summary to console
        
        Args:
            stats: Dictionary containing processing statistics
        """
        print(f"\n📊 Processing Statistics Overview:")
        print("=" * 80)
        print(f"📝 Total records: {stats['total']}")
        print(f"✅ Successfully processed: {stats['processed']} ({stats['processed']/stats['total']*100:.1f}%)")
        if stats['errors'] > 0:
            print(f"❌ Processing errors: {stats['errors']} ({stats['errors']/stats['total']*100:.1f}%)")
        
        print(f"\n📊 Field Extraction Statistics:")
        print("-" * 80)
        
        # Define fields to display with their labels and icons
        fields = [
            ('Decorations', 'with_decorations', '🎨'),
            ('Shape info', 'with_shape', '🏺'),
            ('Function info', 'with_function', '🔧'),
            ('Inscriptions', 'with_inscriptions', '📜'),
            ('Color info', 'with_color', '🎨'),
            ('Glaze info', 'with_glaze', '✨'),
            ('Production place', 'with_place', '📍'),
            ('Topic info', 'with_topics', '🏷️')
        ]
        
        # Display progress bar for each field
        for field_name, field_key, icon in fields:
            count = stats.get(field_key, 0)
            percentage = count/stats['total']*100 if stats['total'] > 0 else 0
            # Create visual progress bar
            bar_length = int(percentage / 5)
            bar = '█' * bar_length + '░' * (20 - bar_length)
            print(f"{icon} {field_name:16} {bar} {count:5d} ({percentage:5.1f}%)")
        
        print(f"\n🏆 High quality records (quality score > 0.5): {stats['high_quality']} ({stats['high_quality']/stats['total']*100:.1f}%)")
    
    def generate_report(self, data_file: str):
        """
        Generate analysis report from processed data
        
        Args:
            data_file: Path to processed data file
        """
        print("\n📝 Generating analysis report...")
        self.report_gen.generate_analysis_report(data_file)


def main():
    """
    Main execution function
    
    Orchestrates the complete processing pipeline from raw data
    to structured output with analysis reports.
    """
    # Configuration settings
    input_file = 'chinese_porcelain_metadata.json'  # Input data file
    output_file = 'porcelain_final_structured.json'  # Output structured data
    keyword_config = None  # Optional keyword configuration file path
    
    # Create processor instance
    processor = PorcelainProcessor(keyword_config)
    
    # Execute data processing
    print("🚀 Starting porcelain data processing...")
    print("=" * 80)
    
    stats = processor.process_dataset(
        input_file=input_file,
        output_file=output_file,
        use_optimal_topics=True  # Auto-determine optimal LDA topics
    )
    
    print("\n✅ Data processing completed!")
    
    # Generate analysis report
    processor.generate_report(output_file)
    
    print("\n🎉 All processing completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()
