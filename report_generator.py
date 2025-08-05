#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据报告生成模块
功能：生成各种分析报告和统计
"""

import json
import pandas as pd
from datetime import datetime
from collections import Counter
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import numpy as np

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self):
        self.data = None
    
    def generate_analysis_report(self, data_file: str):
        """生成详细的数据分析报告"""
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            
            report_file = data_file.replace('.json', '_analysis_report.txt')
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("瓷器数据综合分析报告\n")
                f.write("=" * 100 + "\n")
                f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"总记录数: {len(self.data)}\n")
                f.write("=" * 100 + "\n\n")
                
                # 各部分分析
                self._write_quality_overview(f)
                self._write_lda_analysis(f)
                self._write_decoration_analysis(f)
                self._write_shape_analysis(f)
                self._write_function_analysis(f)
                self._write_glaze_analysis(f)
                self._write_material_analysis(f)
                self._write_production_analysis(f)
                self._write_period_analysis(f)
                self._write_institution_analysis(f)
                self._write_color_analysis(f)
                self._write_inscription_analysis(f)
                self._write_completeness_analysis(f)
                self._write_combination_analysis(f)
                self._write_summary(f)
                
                f.write("\n" + "=" * 100 + "\n")
                f.write(f"报告生成完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            print(f"📄 详细分析报告已生成: {report_file}")
            
            # 同时生成CSV摘要
            self.generate_summary_csv(report_file.replace('.txt', '_summary.csv'))
            
            # 生成可视化图表
            self.generate_visualizations(data_file.replace('.json', '_plots'))
            
        except Exception as e:
            print(f"生成报告失败: {e}")
            import traceback
            traceback.print_exc()
    
    def _write_quality_overview(self, f):
        """写入数据质量概览"""
        f.write("【数据质量概览】\n")
        f.write("-" * 80 + "\n")
        
        quality_scores = []
        quality_distribution = {
            '优秀 (>0.8)': 0,
            '良好 (0.6-0.8)': 0,
            '中等 (0.4-0.6)': 0,
            '较差 (0.2-0.4)': 0,
            '很差 (<0.2)': 0
        }
        
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                score = item['DescriptiveMetadata'].get('quality_score', 0)
                quality_scores.append(score)
                
                if score > 0.8:
                    quality_distribution['优秀 (>0.8)'] += 1
                elif score > 0.6:
                    quality_distribution['良好 (0.6-0.8)'] += 1
                elif score > 0.4:
                    quality_distribution['中等 (0.4-0.6)'] += 1
                elif score > 0.2:
                    quality_distribution['较差 (0.2-0.4)'] += 1
                else:
                    quality_distribution['很差 (<0.2)'] += 1
        
        if quality_scores:
            f.write(f"平均质量分数: {sum(quality_scores)/len(quality_scores):.3f}\n")
            f.write(f"最高质量分数: {max(quality_scores):.3f}\n")
            f.write(f"最低质量分数: {min(quality_scores):.3f}\n\n")
            
            f.write("质量分布:\n")
            for category, count in quality_distribution.items():
                percentage = count/len(self.data)*100
                bar = '█' * int(percentage/2)
                f.write(f"  {category:20} {bar:25} {count:5d} ({percentage:5.1f}%)\n")
    
    def _write_lda_analysis(self, f):
        """写入LDA主题分析"""
        f.write("\n【LDA主题分析】\n")
        f.write("-" * 80 + "\n")
        
        topic_counter = {}
        items_with_topics = 0
        topic_combinations = {}
        
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                lda_topics = item['DescriptiveMetadata'].get('lda_topics', [])
                
                if lda_topics:
                    items_with_topics += 1
                    topic_ids = []
                    
                    for topic in lda_topics:
                        topic_id = topic.get('topic_id', -1)
                        topic_counter[f"主题{topic_id + 1}"] = topic_counter.get(f"主题{topic_id + 1}", 0) + 1
                        topic_ids.append(f"主题{topic_id + 1}")
                    
                    # 统计主题组合
                    if len(topic_ids) > 1:
                        combo = ' + '.join(topic_ids[:2])
                        topic_combinations[combo] = topic_combinations.get(combo, 0) + 1
        
        f.write(f"包含LDA主题的记录: {items_with_topics} ({items_with_topics/len(self.data)*100:.2f}%)\n\n")
        
        if topic_counter:
            f.write("主题分布:\n")
            for topic, count in sorted(topic_counter.items(), key=lambda x: x[1], reverse=True):
                f.write(f"  - {topic}: {count}\n")
            
            if topic_combinations:
                f.write("\n常见主题组合 (前10个):\n")
                for combo, count in sorted(topic_combinations.items(), key=lambda x: x[1], reverse=True)[:10]:
                    f.write(f"  - {combo}: {count}\n")
    
    def _write_decoration_analysis(self, f):
        """写入装饰分析"""
        f.write("\n【装饰类型分布】\n")
        f.write("-" * 80 + "\n")
        
        decoration_themes = {
            'floral': [],
            'figural': [],
            'animal': [],
            'landscape': [],
            'geometric': [],
            'calligraphy': [],
            'symbolic': [],
            'color': [],
            'other': []
        }
        
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                decorations = item['DescriptiveMetadata'].get('Decorations', [])
                for dec in decorations:
                    if ':' in dec:
                        theme, detail = dec.split(':', 1)
                        if theme in decoration_themes:
                            decoration_themes[theme].append(detail)
                        else:
                            decoration_themes['other'].append(dec)
                    else:
                        decoration_themes['other'].append(dec)
        
        # 打印各主题统计
        for theme, details in decoration_themes.items():
            if details:
                f.write(f"\n{theme.upper()} 主题 (共{len(details)}项):\n")
                detail_counter = Counter(details)
                for detail, count in detail_counter.most_common(10):
                    f.write(f"  - {detail}: {count}\n")
    
    def _write_shape_analysis(self, f):
        """写入器形分析"""
        f.write("\n【器形分布】\n")
        f.write("-" * 80 + "\n")
        
        shape_main = {}
        shape_specific = {}
        
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                shapes = item['DescriptiveMetadata'].get('Shape', [])
                for shape in shapes:
                    if shape in ['bowl', 'vase', 'jar', 'plate', 'cup', 'pot', 'bottle', 'box', 'censer', 'ewer']:
                        shape_main[shape] = shape_main.get(shape, 0) + 1
                    else:
                        shape_specific[shape] = shape_specific.get(shape, 0) + 1
        
        f.write("主要器形类别:\n")
        for shape, count in sorted(shape_main.items(), key=lambda x: x[1], reverse=True):
            percentage = count/len(self.data)*100
            bar = '█' * int(percentage/2)
            f.write(f"  {shape:12} {bar:20} {count:4d} ({percentage:5.1f}%)\n")
        
        if shape_specific:
            f.write("\n具体器形描述 (前20个):\n")
            for shape, count in sorted(shape_specific.items(), key=lambda x: x[1], reverse=True)[:20]:
                f.write(f"  - {shape}: {count}\n")
    
    def _write_function_analysis(self, f):
        """写入功能分析"""
        f.write("\n【功能分布】\n")
        f.write("-" * 80 + "\n")
        
        function_counter = {}
        multi_function_count = 0
        
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                functions = item['DescriptiveMetadata'].get('Function', [])
                if len(functions) > 1:
                    multi_function_count += 1
                for func in functions:
                    function_counter[func] = function_counter.get(func, 0) + 1
        
        if function_counter:
            f.write(f"多功能器物数量: {multi_function_count} ({multi_function_count/len(self.data)*100:.1f}%)\n\n")
            f.write("功能类别分布:\n")
            for func, count in sorted(function_counter.items(), key=lambda x: x[1], reverse=True):
                percentage = count/len(self.data)*100
                bar = '█' * int(percentage/2)
                f.write(f"  {func:12} {bar:20} {count:4d} ({percentage:5.1f}%)\n")
    
    def _write_glaze_analysis(self, f):
        """写入釉色分析"""
        f.write("\n【釉色技术分布】\n")
        f.write("-" * 80 + "\n")
        
        glaze_counter = {}
        multi_glaze_count = 0
        
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                glazes = item['DescriptiveMetadata'].get('Glaze', [])
                if len(glazes) > 1:
                    multi_glaze_count += 1
                for glaze in glazes:
                    glaze_counter[glaze] = glaze_counter.get(glaze, 0) + 1
        
        if glaze_counter:
            f.write(f"多釉色器物数量: {multi_glaze_count} ({multi_glaze_count/len(self.data)*100:.1f}%)\n\n")
            for glaze, count in sorted(glaze_counter.items(), key=lambda x: x[1], reverse=True)[:20]:
                percentage = count/len(self.data)*100
                f.write(f"  - {glaze}: {count} ({percentage:.1f}%)\n")
    
    def _write_material_analysis(self, f):
        """写入材质分析"""
        f.write("\n【材质分布】\n")
        f.write("-" * 80 + "\n")
        
        material_counter = {}
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                materials = item['DescriptiveMetadata'].get('Paste', [])
                for material in materials:
                    material_counter[material] = material_counter.get(material, 0) + 1
        
        if material_counter:
            for material, count in sorted(material_counter.items(), key=lambda x: x[1], reverse=True):
                percentage = count/len(self.data)*100
                bar = '█' * int(percentage)
                f.write(f"  {material:12} {bar:40} {count:4d} ({percentage:5.1f}%)\n")
    
    def _write_production_analysis(self, f):
        """写入生产地分析 - 层级化版本"""
        f.write("\n【生产地分布】\n")
        f.write("-" * 80 + "\n")
        
        # 定义identify_delftware函数（在_write_production_analysis函数内部）
        def identify_delftware(item):
            """识别代尔夫特瓷器的增强函数"""
            
            # 获取所有相关文本
            descriptions = item.get('DescriptiveMetadata', {}).get('Descriptions', [])
            production_places = item.get('DescriptiveMetadata', {}).get('ProductionPlace', [])
            glazes = item.get('DescriptiveMetadata', {}).get('Glaze', [])
            decorations = item.get('DescriptiveMetadata', {}).get('Decorations', [])
            colors = item.get('DescriptiveMetadata', {}).get('ColoredDrawing', [])
            materials = item.get('DescriptiveMetadata', {}).get('Paste', [])
            
            # 合并所有文本
            all_text = ' '.join([
                ' '.join(descriptions),
                ' '.join(production_places),
                ' '.join(glazes),
                ' '.join(decorations),
                ' '.join(colors),
                ' '.join(materials)
            ]).lower()
            
            # 代尔夫特强特征（任一出现即识别）
            strong_indicators = [
                'delft', 'delfts', 'delftware', 'delf',
                'delft blue', 'delfts blauw',
                'royal delft', 'de porceleyne fles',
                'dutch delftware'
            ]
            
            # 检查强特征
            if any(indicator in all_text for indicator in strong_indicators):
                return True
            
            # 组合特征检查（需要多个特征同时出现）
            has_tin_glaze = any(term in all_text for term in [
                'tin glaze', 'tin-glaze', 'tin glazed', 'tin-glazed',
                'faience', 'faïence', 'plateel', 'tinglazuur',
                'maiolica', 'majolica', 'galleyware', 'galliware',
                'fayence', 'zinnglasur'
            ])
            
            has_blue_white = 'blue and white' in all_text or 'blue white' in all_text
            
            has_dutch_reference = any(term in all_text for term in [
                'dutch', 'nederlands', 'holland', 'netherlands',
                'amsterdam', 'rotterdam', 'haarlem', 'the hague', 'den haag'
            ])
            
            has_earthenware = 'earthenware' in all_text or 'pottery' in all_text
            
            # 组合判断
            if has_tin_glaze and (has_dutch_reference or has_blue_white):
                return True
            
            if has_earthenware and has_tin_glaze:
                return True
            
            if has_blue_white and has_dutch_reference:
                return True
            
            return False
        
        # 定义产地层级映射
        place_hierarchy = {
            # 中国
            'china': {
                'country': 'China',
                'regions': {
                    'jingdezhen': 'Jiangxi',
                    'longquan': 'Zhejiang', 
                    'dehua': 'Fujian',
                    'yixing': 'Jiangsu',
                    'jun': 'Henan',
                    'ding': 'Hebei',
                    'cizhou': 'Hebei',
                    'yaozhou': 'Shaanxi',
                    'ru': 'Henan',
                    'guan': 'Zhejiang',
                    'ge': 'Zhejiang',
                    'export': 'Export/Canton'
                }
            },
            # 荷兰
            'netherlands': {
                'country': 'Netherlands',
                'regions': {
                    'delft': 'South Holland',
                    'amsterdam': 'North Holland',
                    'rotterdam': 'South Holland',
                    'haarlem': 'North Holland',
                    'makkum': 'Friesland'
                }
            },
            # 比利时
            'belgium': {
                'country': 'Belgium',
                'regions': {
                    'brussels': 'Brussels',
                    'antwerp': 'Antwerp',
                    'ghent': 'East Flanders',
                    'tournai': 'Hainaut'
                }
            },
            # 其他欧洲
            'germany': {
                'country': 'Germany',
                'regions': {
                    'meissen': 'Saxony',
                    'dresden': 'Saxony'
                }
            },
            'france': {
                'country': 'France',
                'regions': {
                    'sevres': 'Île-de-France',
                    'vincennes': 'Île-de-France'
                }
            },
            'england': {
                'country': 'England',
                'regions': {
                    'worcester': 'Worcestershire',
                    'staffordshire': 'Staffordshire'
                }
            }
        }
        
        # 产地名称标准化映射
        place_normalization = {
            # 中国变体
            'китай': 'china',
            'kina': 'china',
            'cina': 'china',
            'chine': 'china',
            
            # 中国窑口
            'jun': 'jun',
            'jun kiln': 'jun',
            'junzhou': 'jun',
            'chun': 'jun',
            'ding kiln': 'ding',
            'dingzhou': 'ding',
            'tz\'u-chou': 'cizhou',
            'te-hua': 'dehua',
            'ching-te-chen': 'jingdezhen',
            
            # 布鲁塞尔变体
            'bruxelles': 'brussels',
            'brussel': 'brussels',
            'brusela': 'brussels',
            'bruksela': 'brussels',
            'brusel': 'brussels',
            'briuselis': 'brussels',
            'briuselio': 'brussels',
            'brisele': 'brussels',
            'briseles': 'brussels',
            'an bhruiséil': 'brussels',

            # Delft相关变体
            'delft': 'delft',
            'delfts': 'delft',
            'delftware': 'delft',
            'delf': 'delft',
            'dutch delftware': 'delft',
            'english delftware': 'delft',
            
            # 安特卫普变体（重要的早期产地）
            'antwerpen': 'antwerp',
            'anvers': 'antwerp',
            
            # 其他荷兰城市
            'haarlem': 'haarlem',
            'rotterdam': 'rotterdam',
            'makkum': 'makkum',
            
            # 其他标准化
            'nederland': 'netherlands',
            'holland': 'netherlands',
            'belgian': 'belgium',
            'belgique': 'belgium',
            'belgië': 'belgium',
            'english': 'england',
            'uk': 'england',
            'united kingdom': 'england'
        }
        
        # 初始化统计
        item_by_country = {}
        item_by_place = {}
        place_frequency = {}
        
        # 调试统计
        delft_identified_count = 0
        tin_glaze_count = 0
        blue_white_dutch_count = 0
        
        # 处理每个藏品
        for idx, item in enumerate(self.data):
            item_country = None
            item_specific_place = None
            
            # 首先使用增强的代尔夫特识别
            if identify_delftware(item):
                item_country = 'Netherlands'
                item_specific_place = 'delft'
                delft_identified_count += 1
            
            # 继续处理其他产地信息
            if 'DescriptiveMetadata' in item:
                places = item['DescriptiveMetadata'].get('ProductionPlace', [])
                
                # 收集并标准化所有产地信息
                normalized_places = []
                for place in places:
                    if place and isinstance(place, str):
                        place_lower = place.lower().strip()
                        
                        # 标准化地名
                        normalized = place_normalization.get(place_lower, place_lower)
                        
                        # 记录频率
                        place_frequency[normalized] = place_frequency.get(normalized, 0) + 1
                        normalized_places.append(normalized)
                
                # 如果还没有确定国家，继续处理
                if not item_country:
                    # 确定国家和具体产地
                    for country, info in place_hierarchy.items():
                        # 检查是否有该国家的产地
                        if country in normalized_places:
                            item_country = info['country']
                        
                        # 检查是否有该国家的具体地点
                        for region, province in info['regions'].items():
                            if region in normalized_places:
                                item_country = info['country']
                                item_specific_place = region
                                break
                        
                        if item_country:
                            break
                
                # 即使已经有国家，也要检查是否有更具体的产地
                if item_country and not item_specific_place:
                    # 检查normalized_places中是否包含具体窑口
                    for place in normalized_places:
                        # 检查对应国家的具体产地
                        for country, info in place_hierarchy.items():
                            if info['country'] == item_country:
                                for region in info['regions'].keys():
                                    if region == place or region in place:
                                        item_specific_place = region
                                        break
                                break
                
                # 如果还没有找到具体产地，尝试从描述中提取（特别是中国窑口）
                if item_country == 'China' and not item_specific_place:
                    descriptions = ' '.join(item['DescriptiveMetadata'].get('Descriptions', [])).lower()
                    
                    # 检查描述中的窑口信息
                    kiln_patterns = {
                        'jingdezhen': ['jingdezhen', 'ching-te-chen', 'porcelain capital', 'imperial kiln'],
                        'longquan': ['longquan', 'celadon', 'lung-ch\'uan'],
                        'dehua': ['dehua', 'blanc de chine', 'te-hua', 'white porcelain', 'fujian white'],
                        'yixing': ['yixing', 'purple clay', 'zisha', 'i-hsing'],
                        'jun': ['jun', 'jun kiln', 'junzhou', 'chun', 'jun ware'],
                        'ding': ['ting', 'ding kiln', 'dingzhou', 'ting ware'],
                        'cizhou': ['cizhou', 'tz\'u-chou', 'magnetic'],
                        'yaozhou': ['yaozhou', 'yao zhou'],
                        'ru': ['ru kiln', 'ru ware', 'ju ware'],
                        'guan': ['guan kiln', 'guan ware', 'kuan ware', 'official kiln'],
                        'ge': ['ge kiln', 'ge ware', 'ko ware', 'crackle glaze']
                    }
                    
                    for kiln, patterns in kiln_patterns.items():
                        if any(pattern in descriptions for pattern in patterns):
                            item_specific_place = kiln
                            break
                
                # 调试：统计锡釉和蓝白瓷特征
                all_text = ' '.join([
                    ' '.join(item['DescriptiveMetadata'].get('Descriptions', [])),
                    ' '.join(item['DescriptiveMetadata'].get('Glaze', [])),
                    ' '.join(item['DescriptiveMetadata'].get('ColoredDrawing', []))
                ]).lower()
                
                if any(term in all_text for term in ['tin', 'faience', 'faïence', 'maiolica']):
                    tin_glaze_count += 1
                
                if ('blue and white' in all_text or 'blue white' in all_text) and \
                any(term in all_text for term in ['dutch', 'netherlands', 'holland']):
                    blue_white_dutch_count += 1
            
            # 记录分类
            if not item_country:
                item_country = 'Unknown'
                
            # 按国家统计
            if item_country not in item_by_country:
                item_by_country[item_country] = []
            item_by_country[item_country].append(idx)
            
            # 按具体产地统计
            if item_specific_place:
                place_key = f"{item_country}-{item_specific_place}"
                if place_key not in item_by_place:
                    item_by_place[place_key] = []
                item_by_place[place_key].append(idx)
            else:
                # 即使没有具体产地，也记录国家级别的产地
                if item_country != 'Unknown':
                    place_key = f"{item_country}-unspecified"
                    if place_key not in item_by_place:
                        item_by_place[place_key] = []
                    item_by_place[place_key].append(idx)
        
        # 输出统计结果
        total = len(self.data)
        
        # 1. 按国家统计
        f.write("【按国家分类统计】\n")
        country_sorted = sorted(item_by_country.items(), key=lambda x: len(x[1]), reverse=True)
        
        for country, items in country_sorted:
            count = len(items)
            percentage = count / total * 100
            f.write(f"  {country:20} {count:5d} ({percentage:5.1f}%)\n")
        
        # 2. 中国vs欧洲对比
        china_count = len(item_by_country.get('China', []))
        netherlands_count = len(item_by_country.get('Netherlands', []))
        belgium_count = len(item_by_country.get('Belgium', []))
        european_count = netherlands_count + belgium_count + len(item_by_country.get('Germany', [])) + \
                        len(item_by_country.get('France', [])) + len(item_by_country.get('England', []))
        
        f.write("\n【中国 vs 欧洲瓷器对比】\n")
        f.write(f"  中国瓷器: {china_count} ({china_count/total*100:.1f}%)\n")
        f.write(f"  欧洲瓷器: {european_count} ({european_count/total*100:.1f}%)\n")
        f.write(f"    - 荷兰(含代尔夫特): {netherlands_count} ({netherlands_count/total*100:.1f}%)\n")
        f.write(f"    - 比利时: {belgium_count} ({belgium_count/total*100:.1f}%)\n")
        
        if netherlands_count > 0:
            # 统计代尔夫特的具体数量
            delft_count = len(item_by_place.get('Netherlands-delft', []))
            f.write(f"    - 其中代尔夫特: {delft_count} ({delft_count/total*100:.1f}%)\n")
        
        # 3. 具体产地统计
        f.write("\n【具体产地分布（前30个）】\n")
        place_sorted = sorted(item_by_place.items(), key=lambda x: len(x[1]), reverse=True)[:30]
        
        for place, items in place_sorted:
            count = len(items)
            percentage = count / total * 100
            f.write(f"  {place:30} {count:4d} ({percentage:5.1f}%)\n")
        
        # 4. 产地识别详情
        f.write("\n【产地识别详情】\n")
        china_unspecified = len(item_by_place.get('China-unspecified', []))
        if china_unspecified > 0:
            f.write(f"  中国-未指定具体窑口: {china_unspecified} ({china_unspecified/total*100:.1f}%)\n")
            f.write("  建议：检查原始数据中是否包含更详细的窑口信息\n")
        
        netherlands_unspecified = len(item_by_place.get('Netherlands-unspecified', []))
        if netherlands_unspecified > 0:
            f.write(f"  荷兰-未指定具体产地: {netherlands_unspecified} ({netherlands_unspecified/total*100:.1f}%)\n")
        
        # 5. 中国主要窑口
        china_kilns = [(p, items) for p, items in item_by_place.items() if p.startswith('China-') and not p.endswith('unspecified')]
        if china_kilns:
            f.write("\n【中国主要产瓷中心】\n")
            china_kilns_sorted = sorted(china_kilns, key=lambda x: len(x[1]), reverse=True)
            for place, items in china_kilns_sorted:
                kiln_name = place.split('-')[1]
                count = len(items)
                f.write(f"  {kiln_name:15} {count:4d}\n")
        
        # 6. 欧洲主要产地
        european_places = [(p, items) for p, items in item_by_place.items() 
                        if any(p.startswith(c) for c in ['Netherlands-', 'Belgium-', 'Germany-', 'France-', 'England-']) 
                        and not p.endswith('unspecified')]
        if european_places:
            f.write("\n【欧洲主要产瓷中心】\n")
            european_sorted = sorted(european_places, key=lambda x: len(x[1]), reverse=True)
            for place, items in european_sorted[:10]:
                count = len(items)
                f.write(f"  {place:30} {count:4d}\n")
        
        # 7. 数据质量评估
        unknown_count = len(item_by_country.get('Unknown', []))
        identified_count = total - unknown_count
        
        f.write("\n【产地数据质量评估】\n")
        f.write(f"  成功识别产地: {identified_count} ({identified_count/total*100:.1f}%)\n")
        f.write(f"  未识别产地: {unknown_count} ({unknown_count/total*100:.1f}%)\n")
        
        # 8. 代尔夫特识别分析
        f.write("\n【代尔夫特瓷器识别分析】\n")
        f.write(f"  通过特征识别为代尔夫特: {delft_identified_count} ({delft_identified_count/total*100:.1f}%)\n")
        f.write(f"  包含锡釉相关词汇: {tin_glaze_count} ({tin_glaze_count/total*100:.1f}%)\n")
        f.write(f"  包含'荷兰蓝白'特征: {blue_white_dutch_count} ({blue_white_dutch_count/total*100:.1f}%)\n")
        
        # 9. 原始产地数据频率统计（调试用）
        if place_frequency:
            f.write("\n【原始产地数据频率（前20个）】\n")
            freq_sorted = sorted(place_frequency.items(), key=lambda x: x[1], reverse=True)[:20]
            for place, freq in freq_sorted:
                f.write(f"  '{place}': {freq}\n")

    def _write_period_analysis(self, f):
        """写入时期分析 - 修复版"""
        f.write("\n【时期分布】\n")
        f.write("-" * 80 + "\n")
        
        dynasty_counter = {}
        year_counter = {}
        century_counter = {}
        year_dynasty_mapping = {}
        
        total_with_period = 0
        total_with_year = 0
        
        for item in self.data:
            if 'Metadata_for_Management' in item:
                mgmt = item['Metadata_for_Management']
                
                # 获取时期信息
                periods = mgmt.get('Period', [])
                years = mgmt.get('Years', [])
                period_summary = mgmt.get('PeriodSummary', {})
                
                if periods:
                    total_with_period += 1
                    for period in periods:
                        dynasty_counter[period] = dynasty_counter.get(period, 0) + 1
                
                if years:
                    total_with_year += 1
                    for year in years:
                        # 确保year是整数
                        try:
                            year_int = int(year) if isinstance(year, str) else year
                            # 只统计合理的年份
                            if 1000 <= year_int <= 2025:
                                year_counter[year_int] = year_counter.get(year_int, 0) + 1
                                
                                # 计算世纪
                                century = (year_int - 1) // 100 + 1
                                century_str = f"{century}th century"
                                century_counter[century_str] = century_counter.get(century_str, 0) + 1
                        except (ValueError, TypeError):
                            continue
                
                # 收集年份-朝代映射
                if period_summary and 'dynasty_mapping' in period_summary:
                    # 确保映射中的年份是整数
                    for y, d in period_summary['dynasty_mapping'].items():
                        try:
                            year_int = int(y) if isinstance(y, str) else y
                            year_dynasty_mapping[year_int] = d
                        except (ValueError, TypeError):
                            continue
        
        f.write(f"有时期信息的记录数: {total_with_period} ({total_with_period/len(self.data)*100:.1f}%)\n")
        f.write(f"有年份信息的记录数: {total_with_year} ({total_with_year/len(self.data)*100:.1f}%)\n")
        f.write(f"无时期信息的记录数: {len(self.data) - total_with_period} ({(len(self.data) - total_with_period)/len(self.data)*100:.1f}%)\n\n")
        
        # 朝代分布
        if dynasty_counter:
            f.write("朝代分布:\n")
            dynasty_order = ['Tang', 'Song', 'Yuan', 'Ming', 'Qing', 'Republic', 'Modern']
            
            for dynasty in dynasty_order:
                if dynasty in dynasty_counter:
                    count = dynasty_counter[dynasty]
                    percentage = count/total_with_period*100 if total_with_period > 0 else 0
                    total_percentage = count/len(self.data)*100
                    bar = '█' * int(total_percentage/2)
                    f.write(f"  {dynasty:10} {bar:40} {count:4d} ({percentage:5.1f}% of dated, {total_percentage:5.1f}% of total)\n")
        
        # 世纪分布
        if century_counter:
            f.write("\n世纪分布:\n")
            # 按世纪数字排序
            sorted_centuries = sorted(century_counter.items(), key=lambda x: int(x[0].split('th')[0]))
            for century, count in sorted_centuries:
                percentage = count/len(self.data)*100
                f.write(f"  - {century}: {count} ({percentage:.1f}%)\n")
        
        # 年份-朝代对应表
        if year_dynasty_mapping:
            f.write("\n年份-朝代对应关系 (示例):\n")
            # 只显示合理的年份，确保比较的是整数
            valid_mappings = []
            for y, d in year_dynasty_mapping.items():
                try:
                    year_int = int(y) if isinstance(y, str) else y
                    if 1000 <= year_int <= 2025:
                        valid_mappings.append((year_int, d))
                except (ValueError, TypeError):
                    continue
                    
            sorted_mappings = sorted(valid_mappings)[:20]
            for year, dynasty in sorted_mappings:
                f.write(f"  - {year}: {dynasty}\n")
        
        # 具体年份分布
        if year_counter:
            f.write("\n具体年份分布 (前30个):\n")
            # 只显示合理的年份，确保都是整数
            valid_years = {}
            for y, c in year_counter.items():
                try:
                    year_int = int(y) if isinstance(y, str) else y
                    if 1000 <= year_int <= 2025:
                        valid_years[year_int] = c
                except (ValueError, TypeError):
                    continue
                    
            sorted_years = sorted(valid_years.items(), key=lambda x: x[1], reverse=True)[:30]
            for year, count in sorted_years:
                dynasty = year_dynasty_mapping.get(year, '未知')
                f.write(f"  - {year} ({dynasty}): {count}\n")
    

    def _write_summary(self, f):
        """写入综合统计摘要"""
        f.write("\n【综合统计摘要】\n")
        f.write("=" * 80 + "\n")
        
        # 计算关键指标
        quality_scores = []
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                score = item['DescriptiveMetadata'].get('quality_score', 0)
                quality_scores.append(score)
        
        # 计算字段填充率
        field_stats = {
            '装饰信息': sum(1 for item in self.data if item.get('DescriptiveMetadata', {}).get('Decorations', [])),
            '器形信息': sum(1 for item in self.data if item.get('DescriptiveMetadata', {}).get('Shape', [])),
            '功能信息': sum(1 for item in self.data if item.get('DescriptiveMetadata', {}).get('Function', [])),
            '釉色信息': sum(1 for item in self.data if item.get('DescriptiveMetadata', {}).get('Glaze', [])),
            '材质信息': sum(1 for item in self.data if item.get('DescriptiveMetadata', {}).get('Paste', [])),
            '生产地信息': sum(1 for item in self.data if item.get('DescriptiveMetadata', {}).get('ProductionPlace', [])),
            '颜色信息': sum(1 for item in self.data if item.get('DescriptiveMetadata', {}).get('ColoredDrawing', [])),
            '款识信息': sum(1 for item in self.data if item.get('DescriptiveMetadata', {}).get('Inscriptions', []))
        }
        
        avg_fields_per_item = sum(field_stats.values()) / len(self.data) / len(field_stats)
        
        f.write(f"📊 关键指标:\n")
        f.write(f"  - 总记录数: {len(self.data)}\n")
        f.write(f"  - 平均字段填充率: {avg_fields_per_item*100:.1f}%\n")
        if quality_scores:
            f.write(f"  - 平均质量分数: {sum(quality_scores)/len(quality_scores):.3f}\n")
            f.write(f"  - 高质量记录 (>0.5): {sum(1 for s in quality_scores if s > 0.5)} ({sum(1 for s in quality_scores if s > 0.5)/len(self.data)*100:.1f}%)\n")
            f.write(f"  - 优质记录 (>0.8): {sum(1 for s in quality_scores if s > 0.8)} ({sum(1 for s in quality_scores if s > 0.8)/len(self.data)*100:.1f}%)\n")
        
        f.write(f"\n📈 数据特征:\n")
        
        # 统计总体覆盖率
        total_coverage = {
            '有装饰描述': field_stats['装饰信息'],
            '有器形描述': field_stats['器形信息'],
            '有功能描述': field_stats['功能信息'],
            '有釉色描述': field_stats['釉色信息'],
            '有颜色描述': field_stats['颜色信息']
        }
        
        for desc, count in total_coverage.items():
            f.write(f"  - {desc}: {count} ({count/len(self.data)*100:.1f}%)\n")
        
        f.write(f"\n💡 数据质量建议:\n")
        if avg_fields_per_item < 0.5:
            f.write(f"  - 平均字段填充率较低({avg_fields_per_item*100:.1f}%)，建议补充更多描述信息\n")
        if field_stats['功能信息'] < len(self.data) * 0.3:
            f.write(f"  - 功能信息覆盖率仅{field_stats['功能信息']/len(self.data)*100:.1f}%，建议增加功能描述\n")
        if field_stats['釉色信息'] < len(self.data) * 0.3:
            f.write(f"  - 釉色信息覆盖率仅{field_stats['釉色信息']/len(self.data)*100:.1f}%，建议补充釉色技术信息\n")
    
    
    def _write_institution_analysis(self, f):
        """写入机构分析"""
        f.write("\n【提供机构分布】\n")
        f.write("-" * 80 + "\n")
        
        institution_counter = {}
        country_institution = {}
        
        for item in self.data:
            if 'Metadata_for_Management' in item:
                institution_data = item['Metadata_for_Management'].get('ProvidingInstitution', '')
                country_data = item['Metadata_for_Management'].get('ProvidingInstitutionCountry', '')
                
                # 处理 institution 可能是列表的情况
                institutions = []
                if isinstance(institution_data, list):
                    # 如果是列表，提取所有非空字符串
                    for inst in institution_data:
                        if isinstance(inst, str) and inst.strip():
                            institutions.append(inst.strip())
                elif isinstance(institution_data, str) and institution_data.strip():
                    # 如果是字符串且非空
                    institutions.append(institution_data.strip())
                
                # 处理 country 可能是列表的情况
                countries = []
                if isinstance(country_data, list):
                    # 如果是列表，提取所有非空字符串
                    for c in country_data:
                        if isinstance(c, str) and c.strip():
                            countries.append(c.strip())
                elif isinstance(country_data, str) and country_data.strip():
                    # 如果是字符串且非空
                    countries.append(country_data.strip())
                
                # 统计每个机构
                for institution in institutions:
                    institution_counter[institution] = institution_counter.get(institution, 0) + 1
                    
                    # 关联国家和机构
                    for country in countries:
                        if country not in country_institution:
                            country_institution[country] = {}
                        country_institution[country][institution] = country_institution[country].get(institution, 0) + 1
        
        if institution_counter:
            f.write(f"总计不同机构数: {len(institution_counter)}\n\n")
            
            # 按国家分组显示
            if country_institution:
                f.write("按国家分组的主要机构:\n")
                for country in sorted(country_institution.keys())[:10]:
                    institutions = country_institution[country]
                    f.write(f"\n{country}:\n")
                    for inst, count in sorted(institutions.items(), key=lambda x: x[1], reverse=True)[:3]:
                        f.write(f"  - {inst}: {count}\n")
            
            f.write("\n所有机构 (前20个):\n")
            for institution, count in sorted(institution_counter.items(), key=lambda x: x[1], reverse=True)[:20]:
                f.write(f"  - {institution}: {count} ({count/len(self.data)*100:.2f}%)\n")
    
    def _write_color_analysis(self, f):
        """写入颜色分析"""
        f.write("\n【颜色分布】\n")
        f.write("-" * 80 + "\n")
        
        color_counter = {}
        color_combinations = {}
        
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                colors = item['DescriptiveMetadata'].get('ColoredDrawing', [])
                for color in colors:
                    color_counter[color] = color_counter.get(color, 0) + 1
                
                # 统计颜色组合
                if len(colors) > 1:
                    color_combo = ' + '.join(sorted(colors))
                    color_combinations[color_combo] = color_combinations.get(color_combo, 0) + 1
        
        if color_counter:
            f.write("单色统计:\n")
            for color, count in sorted(color_counter.items(), key=lambda x: x[1], reverse=True):
                percentage = count/len(self.data)*100
                bar = '█' * int(percentage/2)
                f.write(f"  {color:15} {bar:20} {count:4d} ({percentage:5.1f}%)\n")
            
            if color_combinations:
                f.write("\n常见颜色组合 (前10个):\n")
                for combo, count in sorted(color_combinations.items(), key=lambda x: x[1], reverse=True)[:10]:
                    f.write(f"  - {combo}: {count}\n")
    
    def _write_inscription_analysis(self, f):
        """写入款识分析"""
        f.write("\n【款识信息分布】\n")
        f.write("-" * 80 + "\n")
        
        inscription_types = {
            'mark': [],
            'inscription': [],
            'character mark': [],
            'reign mark': [],
            'signature': [],
            'period mark': [],
            'other': []
        }
        
        has_inscription_count = 0
        
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                inscriptions = item['DescriptiveMetadata'].get('Inscriptions', [])
                if inscriptions:
                    has_inscription_count += 1
                    
                    for inscription in inscriptions:
                        if ':' in inscription:
                            ins_type, detail = inscription.split(':', 1)
                            if ins_type in inscription_types:
                                inscription_types[ins_type].append(detail)
                            else:
                                inscription_types['other'].append(inscription)
                        else:
                            inscription_types['other'].append(inscription)
        
        f.write(f"有款识记录: {has_inscription_count} ({has_inscription_count/len(self.data)*100:.2f}%)\n")
        f.write(f"无款识记录: {len(self.data) - has_inscription_count} ({(len(self.data) - has_inscription_count)/len(self.data)*100:.2f}%)\n\n")
        
        # 打印各类款识
        for ins_type, details in inscription_types.items():
            if details:
                f.write(f"\n{ins_type.upper()} (共{len(details)}项):\n")
                detail_counter = Counter(details)
                for detail, count in detail_counter.most_common(5):
                    f.write(f"  - {detail}: {count}\n")
    
    def _write_completeness_analysis(self, f):
        """写入数据完整性分析"""
        f.write("\n【数据完整性分析】\n")
        f.write("-" * 80 + "\n")
        
        completeness_levels = {}
        field_coverage = {}
        
        # 定义要检查的字段
        fields_to_check = {
            '描述信息': lambda x: len(x.get('DescriptiveMetadata', {}).get('Descriptions', [])) > 0,
            '装饰信息': lambda x: len(x.get('DescriptiveMetadata', {}).get('Decorations', [])) > 0,
            '器形信息': lambda x: len(x.get('DescriptiveMetadata', {}).get('Shape', [])) > 0,
            '功能信息': lambda x: len(x.get('DescriptiveMetadata', {}).get('Function', [])) > 0,
            '釉色信息': lambda x: len(x.get('DescriptiveMetadata', {}).get('Glaze', [])) > 0,
            '材质信息': lambda x: len(x.get('DescriptiveMetadata', {}).get('Paste', [])) > 0,
            '生产地信息': lambda x: len(x.get('DescriptiveMetadata', {}).get('ProductionPlace', [])) > 0,
            '颜色信息': lambda x: len(x.get('DescriptiveMetadata', {}).get('ColoredDrawing', [])) > 0,
            '款识信息': lambda x: len(x.get('DescriptiveMetadata', {}).get('Inscriptions', [])) > 0,
            '标题信息': lambda x: len(x.get('Metadata_for_Management', {}).get('Title', [])) > 0,
            '时期信息': lambda x: bool(x.get('Metadata_for_Management', {}).get('Period')),
            '机构信息': lambda x: bool(x.get('Metadata_for_Management', {}).get('ProvidingInstitution')),
            '数字化信息': lambda x: bool(x.get('ExtendedMetadata', {}).get('Digitalization', {}).get('edmPreview'))
        }
        
        # 统计每个字段的覆盖率
        for field_name, check_func in fields_to_check.items():
            count = sum(1 for item in self.data if check_func(item))
            field_coverage[field_name] = count
        
        # 统计完整度级别
        for item in self.data:
            if 'Metadata_for_Management' in item:
                level = item['Metadata_for_Management'].get('CompletenessLevel', 0)
                completeness_levels[level] = completeness_levels.get(level, 0) + 1
        
        f.write("字段覆盖率:\n")
        for field, count in sorted(field_coverage.items(), key=lambda x: x[1], reverse=True):
            percentage = count/len(self.data)*100
            bar = '█' * int(percentage/5)
            f.write(f"  {field:12} {bar:20} {count:5d}/{len(self.data)} ({percentage:5.1f}%)\n")
        
        if completeness_levels:
            f.write("\n完整度级别分布:\n")
            for level, count in sorted(completeness_levels.items(), reverse=True):
                f.write(f"  - 级别 {level}: {count} ({count/len(self.data)*100:.2f}%)\n")
    
    def _write_combination_analysis(self, f):
        """写入组合分析"""
        f.write("\n【组合分析】\n")
        f.write("-" * 80 + "\n")
        
        # 器形-功能组合
        shape_function_combinations = {}
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                shapes = item['DescriptiveMetadata'].get('Shape', [])
                functions = item['DescriptiveMetadata'].get('Function', [])
                
                # 只取主要器形
                main_shapes = [s for s in shapes if s in ['bowl', 'vase', 'jar', 'plate', 'cup', 'pot', 'bottle', 'box', 'censer', 'ewer']]
                
                for shape in main_shapes[:1]:
                    for function in functions[:1]:
                        combo = f"{shape} - {function}"
                        shape_function_combinations[combo] = shape_function_combinations.get(combo, 0) + 1
        
        if shape_function_combinations:
            f.write("器形-功能组合 (前20个):\n")
            for combo, count in sorted(shape_function_combinations.items(), key=lambda x: x[1], reverse=True)[:20]:
                f.write(f"  - {combo}: {count}\n")
        
        # 颜色-装饰主题组合
        color_theme_combinations = {}
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                colors = item['DescriptiveMetadata'].get('ColoredDrawing', [])
                decorations = item['DescriptiveMetadata'].get('Decorations', [])
                
                # 提取装饰主题
                themes = set()
                for dec in decorations:
                    if ':' in dec:
                        theme, _ = dec.split(':', 1)
                        if theme in ['floral', 'figural', 'animal', 'landscape', 'geometric']:
                            themes.add(theme)
                
                for color in colors[:1]:
                    for theme in list(themes)[:1]:
                        combo = f"{color} + {theme}"
                        color_theme_combinations[combo] = color_theme_combinations.get(combo, 0) + 1
        
        if color_theme_combinations:
            f.write("\n颜色-装饰主题组合 (前15个):\n")
            for combo, count in sorted(color_theme_combinations.items(), key=lambda x: x[1], reverse=True)[:15]:
                f.write(f"  - {combo}: {count}\n")
    
    
    
    def generate_summary_csv(self, output_file: str):
        """生成CSV格式的统计摘要"""
        try:
            summary_data = []
            
            # 收集各类别统计
            categories = {
                'Decorations': {},
                'Shape': {},
                'Function': {},
                'Glaze': {},
                'Paste': {},
                'ProductionPlace': {},
                'ColoredDrawing': {},
                'Period': {},
                'ProvidingInstitution': {},
                'ProvidingInstitutionCountry': {},
                'Inscriptions': {},
                'QualityScore': []
            }
            
            # 统计各类别
            for item in self.data:
                # 描述性元数据
                if 'DescriptiveMetadata' in item:
                    desc = item['DescriptiveMetadata']
                    
                    # 质量分数
                    quality_score = desc.get('quality_score', 0)
                    categories['QualityScore'].append(quality_score)
                    
                    for field in ['Decorations', 'Shape', 'Function', 'Glaze', 'Paste', 'ProductionPlace', 'ColoredDrawing', 'Inscriptions']:
                        if field in desc:
                            values = desc.get(field, [])
                            if isinstance(values, list):
                                for value in values:
                                    if value and field in categories:
                                        categories[field][value] = categories[field].get(value, 0) + 1
                
                # 管理元数据
                if 'Metadata_for_Management' in item:
                    mgmt = item['Metadata_for_Management']
                    for field in ['Period', 'ProvidingInstitution', 'ProvidingInstitutionCountry']:
                        value = mgmt.get(field, '')
                        if value and field in categories:
                            categories[field][value] = categories[field].get(value, 0) + 1
            
            # 转换为DataFrame格式
            for category, counts in categories.items():
                if category == 'QualityScore':
                    # 质量分数特殊处理
                    if counts:
                        summary_data.append({
                            'Category': 'QualityScore',
                            'Value': 'Average',
                            'Count': len(counts),
                            'Percentage': f"{sum(counts)/len(counts):.3f}"
                        })
                        summary_data.append({
                            'Category': 'QualityScore',
                            'Value': 'High Quality (>0.5)',
                            'Count': sum(1 for s in counts if s > 0.5),
                            'Percentage': f"{sum(1 for s in counts if s > 0.5)/len(counts)*100:.2f}%"
                        })
                elif isinstance(counts, dict):
                    for value, count in counts.items():
                        summary_data.append({
                            'Category': category,
                            'Value': str(value)[:100],  # 限制长度
                            'Count': count,
                            'Percentage': f"{count/len(self.data)*100:.2f}%"
                        })
            
            # 保存为CSV
            df = pd.DataFrame(summary_data)
            df.sort_values(['Category', 'Count'], ascending=[True, False], inplace=True)
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"📊 统计摘要CSV已生成: {output_file}")
            
        except Exception as e:
            print(f"生成CSV摘要失败: {e}")
    
    def generate_visualizations(self, output_dir: str):
        """生成可视化图表"""
        # 暂时禁用绘图功能
        print("📊 可视化图表生成已暂时禁用")
        return
        
        # 原来的绘图代码...
    
    def _plot_quality_distribution(self, output_dir):
        """绘制质量分数分布图"""
        quality_scores = []
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                score = item['DescriptiveMetadata'].get('quality_score', 0)
                quality_scores.append(score)
        
        if quality_scores:
            plt.figure(figsize=(10, 6))
            plt.hist(quality_scores, bins=20, edgecolor='black', alpha=0.7)
            plt.xlabel('Quality Score')
            plt.ylabel('Count')
            plt.title('Distribution of Quality Scores')
            plt.grid(axis='y', alpha=0.3)
            plt.savefig(f"{output_dir}/quality_distribution.png", dpi=300, bbox_inches='tight')
            plt.close()
    
    def _plot_shape_distribution(self, output_dir):
        """绘制器形分布饼图"""
        shape_counter = {}
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                shapes = item['DescriptiveMetadata'].get('Shape', [])
                for shape in shapes:
                    if shape in ['bowl', 'vase', 'jar', 'plate', 'cup', 'pot', 'bottle', 'box', 'censer', 'ewer']:
                        shape_counter[shape] = shape_counter.get(shape, 0) + 1
        
        if shape_counter:
            # 只显示前8个，其他归为"其他"
            sorted_shapes = sorted(shape_counter.items(), key=lambda x: x[1], reverse=True)
            top_shapes = dict(sorted_shapes[:8])
            other_count = sum(count for shape, count in sorted_shapes[8:])
            if other_count > 0:
                top_shapes['others'] = other_count
            
            plt.figure(figsize=(10, 8))
            plt.pie(top_shapes.values(), labels=top_shapes.keys(), autopct='%1.1f%%', startangle=90)
            plt.title('Distribution of Main Shape Types')
            plt.savefig(f"{output_dir}/shape_distribution.png", dpi=300, bbox_inches='tight')
            plt.close()
    
    def _plot_function_distribution(self, output_dir):
        """绘制功能分布条形图"""
        function_counter = {}
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                functions = item['DescriptiveMetadata'].get('Function', [])
                for func in functions:
                    function_counter[func] = function_counter.get(func, 0) + 1
        
        if function_counter:
            sorted_functions = sorted(function_counter.items(), key=lambda x: x[1], reverse=True)[:10]
            
            plt.figure(figsize=(10, 6))
            functions = [f[0] for f in sorted_functions]
            counts = [f[1] for f in sorted_functions]
            
            plt.barh(functions, counts, color='skyblue', edgecolor='navy')
            plt.xlabel('Count')
            plt.ylabel('Function')
            plt.title('Top 10 Functions of Porcelain Items')
            plt.gca().invert_yaxis()
            plt.grid(axis='x', alpha=0.3)
            plt.savefig(f"{output_dir}/function_distribution.png", dpi=300, bbox_inches='tight')
            plt.close()
    
    def _plot_color_distribution(self, output_dir):
        """绘制颜色分布图"""
        color_counter = {}
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                colors = item['DescriptiveMetadata'].get('ColoredDrawing', [])
                for color in colors:
                    color_counter[color] = color_counter.get(color, 0) + 1
        
        if color_counter:
            sorted_colors = sorted(color_counter.items(), key=lambda x: x[1], reverse=True)[:12]
            
            plt.figure(figsize=(12, 6))
            colors = [c[0] for c in sorted_colors]
            counts = [c[1] for c in sorted_colors]
            
            # 尝试使用实际颜色
            color_map = {
                'blue and white': 'lightblue',
                'red': 'red',
                'green': 'green',
                'yellow': 'yellow',
                'black': 'black',
                'brown': 'brown',
                'purple': 'purple',
                'gold': 'gold',
                'celadon': 'lightgreen',
                'multicolor': 'rainbow'
            }
            
            bar_colors = [color_map.get(c, 'gray') for c in colors]
            
            plt.bar(colors, counts, color=bar_colors, edgecolor='black')
            plt.xlabel('Color')
            plt.ylabel('Count')
            plt.title('Distribution of Colors in Porcelain Items')
            plt.xticks(rotation=45, ha='right')
            plt.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            plt.savefig(f"{output_dir}/color_distribution.png", dpi=300, bbox_inches='tight')
            plt.close()
    
    def _plot_period_timeline(self, output_dir):
        """绘制时期时间线"""
        dynasty_counter = {
            'Song': 0,
            'Yuan': 0,
            'Ming': 0,
            'Qing': 0,
            'Modern': 0
        }
        
        for item in self.data:
            if 'Metadata_for_Management' in item:
                period = item['Metadata_for_Management'].get('Period', '').lower()
                if 'song' in period:
                    dynasty_counter['Song'] += 1
                elif 'yuan' in period:
                    dynasty_counter['Yuan'] += 1
                elif 'ming' in period:
                    dynasty_counter['Ming'] += 1
                elif 'qing' in period:
                    dynasty_counter['Qing'] += 1
                elif any(year in period for year in ['19', '20', '21']):
                    dynasty_counter['Modern'] += 1
        
        if any(dynasty_counter.values()):
            plt.figure(figsize=(10, 6))
            dynasties = list(dynasty_counter.keys())
            counts = list(dynasty_counter.values())
            
            plt.plot(dynasties, counts, 'o-', markersize=10, linewidth=2)
            plt.fill_between(range(len(dynasties)), counts, alpha=0.3)
            plt.xlabel('Dynasty/Period')
            plt.ylabel('Number of Items')
            plt.title('Distribution of Porcelain Items Across Dynasties')
            plt.grid(True, alpha=0.3)
            plt.savefig(f"{output_dir}/period_timeline.png", dpi=300, bbox_inches='tight')
            plt.close()