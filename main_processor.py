#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主处理程序
整合所有模块，执行完整的数据处理流程
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
    """瓷器数据处理主程序"""
    
    def __init__(self, keyword_config: str = None):
        # 初始化各模块
        self.preprocessor = TextPreprocessor()
        self.lda_trainer = LDATrainer()
        self.keyword_dict = KeywordDictionary(keyword_config)
        self.mapper = DataMapper(self.keyword_dict)
        self.report_gen = ReportGenerator()
    
    def process_dataset(self, input_file: str, output_file: str, 
                       use_optimal_topics: bool = True) -> Dict[str, Any]:
        """处理整个数据集"""
        try:
            print(f"📁 加载数据: {input_file}")
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"📊 数据量: {len(data)} 条记录")
            
        except Exception as e:
            print(f"❌ 加载文件失败: {e}")
            return {}
        
        # 1. 文本预处理
        print("\n🔍 准备文本数据...")
        all_texts = []
        processed_texts = []
        
        for item in data:
            # 提取原始文本
            raw_text = self.preprocessor.extract_text_from_item(item)
            all_texts.append(raw_text)
            
            # 预处理文本
            processed_text = self.preprocessor.preprocess_text(raw_text)
            if processed_text:
                processed_texts.append(processed_text)
        
        print(f"总文本数: {len(all_texts)}")
        print(f"有效处理文本数: {len(processed_texts)}")
        
        # 2. LDA训练
        if processed_texts:
            self.lda_trainer.train_lda(processed_texts, use_optimal_topics)
        
        # 3. 数据映射
        processed_data = []
        stats = self._init_stats()
        
        print("\n🔄 开始数据映射...")
        for i, item in enumerate(data):
            if i % 100 == 0:
                print(f"处理进度: {i}/{len(data)} ({i/len(data)*100:.1f}%)")
            
            # 获取文本
            raw_text = all_texts[i]
            processed_text = self.preprocessor.preprocess_text(raw_text)
            
            # 获取LDA主题
            lda_topics = None
            if self.lda_trainer.lda_model and processed_text:
                lda_topics = self.lda_trainer.get_document_topics(processed_text)
            
            # 映射数据
            result = self.mapper.process_item(item, raw_text, lda_topics)
            
            # 更新统计
            if 'error' not in result.get('ProcessingMetadata', {}):
                processed_data.append(result)
                self._update_stats(stats, result)
            else:
                stats['errors'] += 1
        
        # 4. 保存结果
        self._save_results(output_file, processed_data, stats)
        
        # 5. 打印统计
        self._print_statistics(stats)
        
        return stats
    
    def _init_stats(self) -> Dict[str, Any]:
        """初始化统计数据"""
        return {
            'total': 0,
            'processed': 0,
            'with_decorations': 0,
            'with_shape': 0,
            'with_function': 0,
            'with_inscriptions': 0,
            'with_color': 0,
            'with_glaze': 0,
            'with_place': 0,
            'with_topics': 0,
            'high_quality': 0,
            'errors': 0
        }
    
    def _update_stats(self, stats: Dict[str, Any], result: Dict[str, Any]):
        """更新统计数据"""
        stats['processed'] += 1
        desc_meta = result.get('DescriptiveMetadata', {})
        
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
        
        quality_score = desc_meta.get('quality_score', 0)
        if quality_score > 0.5:
            stats['high_quality'] += 1
    
    def _save_results(self, output_file: str, processed_data: list[Dict], 
                     stats: Dict[str, Any]):
        """保存处理结果"""
        try:
            # 保存主数据
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=2)
            print(f"\n💾 处理结果已保存到: {output_file}")
            
            # 保存统计信息
            stats_file = output_file.replace('.json', '_stats.json')
            stats['total'] = len(processed_data) + stats['errors']
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            print(f"📊 统计信息已保存到: {stats_file}")
            
            # 保存LDA信息
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
                print(f"🏷️  LDA信息已保存到: {lda_file}")
            
        except Exception as e:
            print(f"❌ 保存文件失败: {e}")
    
    def _print_statistics(self, stats: Dict[str, Any]):
        """打印统计信息"""
        print(f"\n📊 处理统计总览:")
        print("=" * 80)
        print(f"📝 总记录数: {stats['total']}")
        print(f"✅ 成功处理: {stats['processed']} ({stats['processed']/stats['total']*100:.1f}%)")
        if stats['errors'] > 0:
            print(f"❌ 处理错误: {stats['errors']} ({stats['errors']/stats['total']*100:.1f}%)")
        
        print(f"\n📊 字段提取统计:")
        print("-" * 80)
        fields = [
            ('装饰信息', 'with_decorations', '🎨'),
            ('形状信息', 'with_shape', '🏺'),
            ('功能信息', 'with_function', '🔧'),
            ('款识信息', 'with_inscriptions', '📜'),
            ('颜色信息', 'with_color', '🎨'),
            ('釉色信息', 'with_glaze', '✨'),
            ('产地信息', 'with_place', '📍'),
            ('主题信息', 'with_topics', '🏷️')
        ]
        
        for field_name, field_key, icon in fields:
            count = stats.get(field_key, 0)
            percentage = count/stats['total']*100 if stats['total'] > 0 else 0
            bar_length = int(percentage / 5)
            bar = '█' * bar_length + '░' * (20 - bar_length)
            print(f"{icon} {field_name:12} {bar} {count:5d} ({percentage:5.1f}%)")
        
        print(f"\n🏆 高质量记录 (质量分数>0.5): {stats['high_quality']} ({stats['high_quality']/stats['total']*100:.1f}%)")
    
    def generate_report(self, data_file: str):
        """生成分析报告"""
        print("\n📝 正在生成分析报告...")
        self.report_gen.generate_analysis_report(data_file)


def main():
    """主函数"""
    # 配置
    input_file = 'chinese_porcelain_metadata.json'
    output_file = 'porcelain_final_structured.json'
    keyword_config = None  # 可选的关键词配置文件
    
    # 创建处理器
    processor = PorcelainProcessor(keyword_config)
    
    # 处理数据
    print("🚀 开始瓷器数据处理...")
    print("=" * 80)
    
    stats = processor.process_dataset(
        input_file=input_file,
        output_file=output_file,
        use_optimal_topics=True
    )
    
    print("\n✅ 数据处理完成！")
    
    # 生成报告
    processor.generate_report(output_file)
    
    print("\n🎉 所有处理完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()