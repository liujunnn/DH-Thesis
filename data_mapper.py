#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据映射模块 - 优化版
功能：提取字段信息，映射到目标数据结构
增强：更好的产地和时期信息提取
"""

import re
from typing import Dict, List, Any, Union, Tuple  # 添加Tuple导入
from datetime import datetime
import json

class DataMapper:
    """数据映射器"""
    
    def __init__(self, keyword_dict):
        self.keyword_dict = keyword_dict
    
    def _flatten_list(self, lst: Union[List, Any]) -> List[str]:
        """递归展平嵌套列表"""
        result = []
        if isinstance(lst, list):
            for item in lst:
                if isinstance(item, list):
                    result.extend(self._flatten_list(item))
                elif item is not None:
                    result.append(str(item))
        elif lst is not None:
            result.append(str(lst))
        return result
    
    def extract_colored_drawing(self, text: str) -> List[str]:
        """提取颜色信息"""
        if not text:
            return []
            
        text_lower = text.lower()
        colors_found = []
        
        for color_name, keywords in self.keyword_dict.color_keywords.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    colors_found.append(color_name)
                    break
        
        return list(set(colors_found))
    
    def extract_decorations(self, text: str) -> List[str]:
        """提取装饰信息"""
        if not text:
            return []
            
        text_lower = text.lower()
        decorations = []
        
        # 提取装饰主题
        for theme, keywords in self.keyword_dict.decoration_themes.items():
            theme_decorations = []
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    theme_decorations.append(keyword)
            
            # 只保留每个主题最多3个关键词
            for keyword in theme_decorations[:3]:
                decorations.append(f"{theme}:{keyword}")
        
        # 提取颜色作为装饰的一部分
        colors = self.extract_colored_drawing(text)
        decorations.extend([f"color:{c}" for c in colors])
        
        # 使用正则表达式提取特定装饰模式
        decoration_patterns = [
            (r'decorated with ([\w\s,]+?)(?:\.|,|;|and)', 'decorated'),
            (r'depicting ([\w\s,]+?)(?:\.|,|;|and)', 'depicting'),
            (r'painted with ([\w\s,]+?)(?:\.|,|;|and)', 'painted'),
            (r'design of ([\w\s,]+?)(?:\.|,|;|and)', 'design'),
            (r'motif of ([\w\s,]+?)(?:\.|,|;|and)', 'motif'),
            (r'pattern of ([\w\s,]+?)(?:\.|,|;|and)', 'pattern')
        ]
        
        for pattern, prefix in decoration_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches[:2]:
                if len(match) < 50:
                    decorations.append(f"{prefix}:{match.strip()}")
        
        # 去重并限制总数
        unique_decorations = []
        seen = set()
        for dec in decorations:
            dec_lower = dec.lower()
            if dec_lower not in seen:
                unique_decorations.append(dec)
                seen.add(dec_lower)
        
        return unique_decorations[:15]
    
    def extract_shape(self, text: str) -> List[str]:
        """提取形状信息"""
        if not text:
            return []
            
        text_lower = text.lower()
        shapes_found = []
        shape_details = []
        
        for shape_type, keywords in self.keyword_dict.shape_keywords.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    shapes_found.append(shape_type)
                    if keyword != shape_type:
                        shape_details.append(keyword)
        
        # 合并结果
        result = list(set(shapes_found))
        result.extend([d for d in set(shape_details) if d not in result])
        
        return result[:5]
    
    def extract_function(self, text: str) -> List[str]:
        """提取功能信息"""
        if not text:
            return []
            
        text_lower = text.lower()
        functions_found = []
        
        for function_type, keywords in self.keyword_dict.function_keywords.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    functions_found.append(function_type)
                    break
        
        return list(set(functions_found))
    
    def extract_material(self, text: str) -> List[str]:
        """提取材质信息"""
        if not text:
            return []
            
        text_lower = text.lower()
        materials_found = []
        
        for material_type, keywords in self.keyword_dict.material_keywords.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    materials_found.append(material_type)
        
        # 默认材质推断
        if not materials_found:
            if any(word in text_lower for word in ['ceramic', 'pottery', 'clay']):
                materials_found.append('ceramic')
            elif any(word in text_lower for word in ['porcelain', 'china']):
                materials_found.append('porcelain')
        
        return list(set(materials_found))
    
    def extract_glaze(self, text: str) -> List[str]:
        """提取釉色信息"""
        if not text:
            return []
            
        text_lower = text.lower()
        glazes_found = []
        
        for glaze_type, keywords in self.keyword_dict.glaze_keywords.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    normalized_type = glaze_type.replace('_', ' ')
                    glazes_found.append(normalized_type)
                    if keyword != glaze_type and keyword != normalized_type:
                        glazes_found.append(keyword)
        
        return list(set(glazes_found))[:5]
    
    def extract_production_place(self, item: Dict[str, Any], text: str) -> List[str]:
        """提取生产地信息 - 修复版"""
        places = []
        normalized_places = set()
        
        # 1. 从专门的地点字段提取
        place_fields = ['edmPlaceLabel', 'placeLabel', 'place', 'origin', 'provenance', 'production']
        for field in place_fields:
            if field in item:
                place_data = item[field]
                if isinstance(place_data, list):
                    for p in self._flatten_list(place_data):
                        if p and isinstance(p, str):
                            # 处理字典格式 {'def': 'place_name'}
                            if p.startswith('{') and 'def' in p:
                                try:
                                    p_dict = json.loads(p.replace("'", '"'))
                                    if 'def' in p_dict:
                                        p = p_dict['def']
                                except:
                                    pass
                            
                            # 标准化地名
                            normalized = self.keyword_dict.normalize_place(p)
                            if normalized and len(normalized) < 50:
                                normalized_places.add(normalized)
                                
                elif isinstance(place_data, str) and place_data:
                    normalized = self.keyword_dict.normalize_place(place_data)
                    if normalized and len(normalized) < 50:
                        normalized_places.add(normalized)
                        
                elif isinstance(place_data, dict) and 'def' in place_data:
                    # 直接处理字典格式
                    p = place_data['def']
                    normalized = self.keyword_dict.normalize_place(p)
                    if normalized and len(normalized) < 50:
                        normalized_places.add(normalized)
        
        # 2. 从文本中提取产地信息
        if text:
            text_lower = text.lower()
            
            # 检查各个产地关键词
            for place_type, keywords in self.keyword_dict.production_keywords.items():
                for keyword in keywords:
                    if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                        normalized_places.add(place_type)
                        break
            
            # 特殊模式识别
            delft_patterns = [
                r'delft(?:ware|se?)?',
                r'dutch\s+(?:delft|pottery|ceramic)',
                r'hollants\s+porceleyn',
                r'de\s+porceleyne\s+fles',
                r'royal\s+delft'
            ]
            
            for pattern in delft_patterns:
                if re.search(pattern, text_lower):
                    normalized_places.add('delft')
                    # 不再自动添加 netherlands，避免重复计数
                    break
            
            # 比利时模式
            belgian_patterns = [
                r'belgian\s+(?:pottery|ceramic|porcelain)',
                r'brussels\s+(?:pottery|ceramic)',
                r'antwerp\s+(?:pottery|ceramic)',
                r'tournai\s+(?:pottery|ceramic)'
            ]
            
            for pattern in belgian_patterns:
                if re.search(pattern, text_lower):
                    normalized_places.add('belgium')
                    break
        
        # 3. 清理结果
        # 移除可能的博物馆位置
        museum_locations = ['vienna', 'stockholm', 'london', 'paris', 'new york']
        normalized_places = {p for p in normalized_places if p not in museum_locations}
        
        # 合并布鲁塞尔变体到比利时
        if 'brussels' in normalized_places:
            normalized_places.add('belgium')
            normalized_places.remove('brussels')
        
        # 4. 优先级排序
        final_places = []
        
        # 优先级排序
        priority_order = [
            'jingdezhen', 'delft', 'longquan', 'dehua', 'yixing', 'jun', 'ding', 'cizhou',
            'amsterdam', 'rotterdam', 'haarlem', 'makkum',
            'antwerp', 'tournai', 'ghent',
            'china', 'netherlands', 'belgium',
            'meissen', 'sevres', 'worcester',
            'export'
        ]
        
        # 先添加高优先级的产地
        for place in priority_order:
            if place in normalized_places:
                final_places.append(place)
                normalized_places.remove(place)
        
        # 添加剩余的产地
        final_places.extend(sorted(normalized_places))
        
        return final_places[:10]  # 限制最多10个产地

    def extract_period_info(self, item: Dict[str, Any]) -> Tuple[List[str], List[int], Dict[str, Any]]:
        """提取时期信息 - 修复版"""
        periods = []
        years = []
        dynasty_info = {}
        
        # 1. 从Period字段提取
        period_data = item.get('Metadata_for_Management', {}).get('Period', '')
        if not period_data and 'edmTimespanLabel' in item:
            period_data = item['edmTimespanLabel']
        
        # 处理period数据
        period_strings = []
        if isinstance(period_data, list):
            for p in period_data:
                if isinstance(p, str) and p.strip():
                    # 过滤掉URL和其他无用信息
                    if not p.startswith('http') and not p.startswith('https'):
                        period_strings.append(p.strip())
                elif isinstance(p, dict) and 'def' in p:
                    p_str = p['def'].strip()
                    if not p_str.startswith('http'):
                        period_strings.append(p_str)
        elif isinstance(period_data, str) and period_data.strip():
            if not period_data.startswith('http'):
                period_strings.append(period_data.strip())
        elif isinstance(period_data, dict) and 'def' in period_data:
            p_str = period_data['def'].strip()
            if not p_str.startswith('http'):
                period_strings.append(p_str)
        
        # 2. 解析时期字符串
        for period_str in period_strings:
            # 提取年份
            # 先尝试提取4位数年份
            year_matches = re.findall(r'\b(1[0-9]{3}|20[0-2][0-9])\b', period_str)
            for year_str in year_matches:
                year = int(year_str)
                if 1000 <= year <= 2025:
                    years.append(year)
            
            # 提取世纪并转换为年份
            century_patterns = [
                (r'\b(\d{1,2})(?:st|nd|rd|th)\s+century\b', 'en'),
                (r'\b(\d{1,2})[èe]me\s+siècle\b', 'fr'),
                (r'\b(\d{1,2})\.\s+Jahrhundert\b', 'de'),
                (r'\b(\d{1,2})[º°]\s+século\b', 'pt'),
                (r'\b(\d{1,2})\s+век\b', 'ru'),
                (r'\b(\d{1,2})-luku\b', 'fi'),
                (r'\b(\d{1,2})\.\s+gadsimts\b', 'lv'),
                (r'\b(\d{1,2})\s+amžius\b', 'lt'),
            ]
            
            for pattern, lang in century_patterns:
                matches = re.findall(pattern, period_str, re.IGNORECASE)
                for match in matches:
                    century = int(match)
                    if 1 <= century <= 21:
                        # 使用世纪中期作为代表年份
                        year = (century - 1) * 100 + 50
                        years.append(year)
                        periods.append(f"{century}th century")
            
            # 提取朝代信息
            period_lower = period_str.lower()
            for dynasty, keywords in self.keyword_dict.period_keywords.items():
                for keyword in keywords:
                    if keyword in period_lower:
                        periods.append(dynasty.capitalize())
                        break
        
        # 3. 根据年份推断朝代
        for year in years:
            dynasty = self.keyword_dict.get_dynasty_from_year(year)
            if dynasty != 'Unknown':
                dynasty_info[year] = dynasty
                if dynasty not in periods:
                    periods.append(dynasty)
        
        # 4. 清理和去重
        # 移除重复和无效年份
        unique_years = []
        for year in years:
            if 1000 <= year <= 2025 and year not in unique_years:
                unique_years.append(year)
        
        unique_periods = []
        seen = set()
        for period in periods:
            if period and period not in seen and len(period) < 50:
                unique_periods.append(period)
                seen.add(period.lower())
        
        # 5. 生成综合时期信息
        period_summary = {
            'periods': unique_periods[:5],
            'years': sorted(unique_years)[:10],
            'dynasty_mapping': dynasty_info,
            'century': self.keyword_dict.get_century_from_year(unique_years[0]) if unique_years else None,
            'date_range': f"{min(unique_years)}-{max(unique_years)}" if len(unique_years) > 1 else str(unique_years[0]) if unique_years else None
        }
        
        return unique_periods, unique_years, period_summary

    def extract_inscriptions(self, text: str) -> List[str]:
        """提取款识信息"""
        if not text:
            return []
            
        text_lower = text.lower()
        inscriptions = []
        
        # 款识相关关键词
        inscription_keywords = [
            'mark', 'marked', 'inscription', 'inscribed', 'character',
            'seal', 'signature', 'signed', 'reign mark', 'nianzhi',
            'nianzhao', 'tang', 'zhi', 'zao', 'six character', 
            'four character', 'seal mark', 'reign title', 'base mark'
        ]
        
        found_keywords = []
        for keyword in inscription_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        inscriptions.extend(found_keywords[:3])
        
        # 尝试提取具体的款识内容
        inscription_patterns = [
            (r'mark(?:ed)?\s+(?:of|with|reading)\s+([\w\s]+?)(?:\.|,|;)', 'mark'),
            (r'inscription\s+(?:of|reading)\s+([\w\s]+?)(?:\.|,|;)', 'inscription'),
            (r'(?:six|four|two)\s+character\s+mark\s+(?:of|reading)?\s*([\w\s]+?)(?:\.|,|;)', 'character mark'),
            (r'reign\s+mark\s+of\s+([\w\s]+?)(?:\.|,|;)', 'reign mark'),
            (r'signed\s+([\w\s]+?)(?:\.|,|;)', 'signature')
        ]
        
        for pattern, prefix in inscription_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches[:2]:
                if len(match) < 30:
                    inscriptions.append(f"{prefix}:{match.strip()}")
        
        # 检查朝代款识
        for period, keywords in self.keyword_dict.period_keywords.items():
            for keyword in keywords:
                if keyword in text_lower and 'mark' in text_lower:
                    inscriptions.append(f"period mark:{period}")
                    break
        
        return list(set(inscriptions))[:5]
    
    def extract_period_info(self, item: Dict[str, Any]) -> Tuple[List[str], List[int], Dict[str, Any]]:
        """提取时期信息 - 完全重写"""
        periods = []
        years = []
        dynasty_info = {}
        
        # 1. 从Period字段提取
        period_data = item.get('Metadata_for_Management', {}).get('Period', '')
        if not period_data and 'edmTimespanLabel' in item:
            period_data = item['edmTimespanLabel']
        
        # 处理period数据
        period_strings = []
        if isinstance(period_data, list):
            for p in period_data:
                if isinstance(p, str) and p.strip():
                    # 过滤掉URL和其他无用信息
                    if not p.startswith('http') and not p.startswith('https'):
                        period_strings.append(p.strip())
                elif isinstance(p, dict) and 'def' in p:
                    p_str = p['def'].strip()
                    if not p_str.startswith('http'):
                        period_strings.append(p_str)
        elif isinstance(period_data, str) and period_data.strip():
            if not period_data.startswith('http'):
                period_strings.append(period_data.strip())
        elif isinstance(period_data, dict) and 'def' in period_data:
            p_str = period_data['def'].strip()
            if not p_str.startswith('http'):
                period_strings.append(p_str)
        
        # 2. 解析时期字符串
        for period_str in period_strings:
            # 提取年份
            year_patterns = [
                r'\b(\d{4})\b',  # 4位数字年份
                r'\b(\d{1,2})th\s+century\b',  # 世纪
                r'\b(\d{1,2})[èe]me\s+siècle\b',  # 法语世纪
                r'\b(\d{1,2})\.\s+Jahrhundert\b',  # 德语世纪
                r'\b(\d{1,2})[º°]\s+século\b',  # 葡萄牙语世纪
                r'\b(\d{1,2})\s+век\b',  # 俄语世纪
                r'\b(\d{1,2})-luku\b',  # 芬兰语世纪
                r'\b(\d{1,2})\.\s+gadsimts\b',  # 拉脱维亚语世纪
                r'\b(\d{1,2})\s+amžius\b',  # 立陶宛语世纪
            ]
            
            for pattern in year_patterns:
                matches = re.findall(pattern, period_str, re.IGNORECASE)
                for match in matches:
                    try:
                        if 'century' in period_str.lower() or 'siècle' in period_str.lower() or \
                           'jahrhundert' in period_str.lower() or 'século' in period_str.lower() or \
                           'век' in period_str.lower() or any(suffix in period_str for suffix in ['-luku', 'gadsimts', 'amžius']):
                            # 世纪转年份（使用世纪中期）
                            century = int(match)
                            year = (century - 1) * 100 + 50
                            years.append(year)
                            periods.append(f"{century}th century")
                        else:
                            # 直接年份
                            year = int(match)
                            if 1000 <= year <= 2025:
                                years.append(year)
                    except:
                        pass
            
            # 提取朝代信息
            period_lower = period_str.lower()
            for dynasty, keywords in self.keyword_dict.period_keywords.items():
                for keyword in keywords:
                    if keyword in period_lower:
                        periods.append(dynasty.capitalize())
                        break
        
        # 3. 根据年份推断朝代
        for year in years:
            dynasty = self.keyword_dict.get_dynasty_from_year(year)
            if dynasty != 'Unknown':
                dynasty_info[year] = dynasty
                if dynasty not in periods:
                    periods.append(dynasty)
        
        # 4. 清理和去重
        unique_periods = []
        seen = set()
        for period in periods:
            if period and period not in seen and len(period) < 50:
                unique_periods.append(period)
                seen.add(period.lower())
        
        # 5. 生成综合时期信息
        period_summary = {
            'periods': unique_periods[:5],
            'years': sorted(set(years))[:10],
            'dynasty_mapping': dynasty_info,
            'century': self.keyword_dict.get_century_from_year(years[0]) if years else None,
            'date_range': f"{min(years)}-{max(years)}" if len(years) > 1 else str(years[0]) if years else None
        }
        
        return unique_periods, years, period_summary
    
    def map_to_descriptive_metadata(self, item: Dict[str, Any], text: str, 
                                  lda_topics: List[Dict] = None) -> Dict[str, Any]:
        """映射到描述性元数据结构"""
        # 安全获取描述
        descriptions = []
        if 'dcDescription' in item:
            desc_data = item['dcDescription']
            descriptions = self._flatten_list(desc_data)
        
        # 基础描述性元数据
        descriptive_metadata = {
            'Descriptions': descriptions[:3],
            'ColoredDrawing': self.extract_colored_drawing(text),
            'Decorations': self.extract_decorations(text),
            'Shape': self.extract_shape(text),
            'ShapeDescription': [],
            'Function': self.extract_function(text),
            'FunctionCategory': [],
            'Paste': self.extract_material(text),
            'PasteMaterial': self.extract_material(text),
            'Glaze': self.extract_glaze(text),
            'ProductionPlace': self.extract_production_place(item, text),
            'ProductionPlaceLocation': self.extract_production_place(item, text),
            'Inscriptions': self.extract_inscriptions(text)
        }
        
        # 添加LDA主题信息
        if lda_topics:
            descriptive_metadata['lda_topics'] = lda_topics
        
        # 添加提取质量指标
        extraction_quality = {
            'has_color': len(descriptive_metadata['ColoredDrawing']) > 0,
            'has_decoration': len(descriptive_metadata['Decorations']) > 0,
            'has_shape': len(descriptive_metadata['Shape']) > 0,
            'has_function': len(descriptive_metadata['Function']) > 0,
            'has_material': len(descriptive_metadata['Paste']) > 0,
            'has_glaze': len(descriptive_metadata['Glaze']) > 0,
            'has_place': len(descriptive_metadata['ProductionPlace']) > 0,
            'has_inscription': len(descriptive_metadata['Inscriptions']) > 0
        }
        
        descriptive_metadata['extraction_quality'] = extraction_quality
        descriptive_metadata['quality_score'] = sum(extraction_quality.values()) / len(extraction_quality)
        
        return descriptive_metadata
    
    def map_to_management_metadata(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """映射到管理元数据结构 - 优化版"""
        # 安全获取标题
        title_value = []
        if 'title' in item:
            if isinstance(item['title'], list):
                title_value = self._flatten_list(item['title'])
            elif isinstance(item['title'], str):
                title_value = [item['title']]
        elif 'dcTitle' in item:
            if isinstance(item['dcTitle'], list):
                title_value = self._flatten_list(item['dcTitle'])
            elif isinstance(item['dcTitle'], str):
                title_value = [item['dcTitle']]
        
        # 提取时期信息
        periods, years, period_summary = self.extract_period_info(item)
        
        management_metadata = {
            'Title': title_value,
            'Used_Titles': [],
            'Identifier': item.get('id', ''),
            'Period': periods,  # 清理后的时期列表
            'Years': years,  # 提取的年份
            'PeriodSummary': period_summary,  # 综合时期信息
            'CompletenessLevel': item.get('europeanaCompleteness', 
                                        item.get('completeness', 0)),
            'ProvidingInstitution': item.get('dataProvider', ''),
            'ProvidingInstitutionCountry': item.get('country', ''),
            'DateofStorage': item.get('timestamp_created', ''),
            'PreservationRecords': {
                'rights': item.get('rights', ''),
                'timestamp_created': item.get('timestamp_created', ''),
                'timestamp_updated': item.get('timestamp_update', ''),
                'quality_score': item.get('description_quality', {}).get('score', 0) 
                               if isinstance(item.get('description_quality'), dict) else 0
            }
        }
        
        # 处理标题变体
        all_titles = []
        
        if 'dcTitle' in item:
            dc_titles = self._flatten_list(item['dcTitle'])
            all_titles.extend(dc_titles)
        
        if 'title' in item:
            titles = self._flatten_list(item['title'])
            all_titles.extend(titles)
        
        # 去重
        unique_titles = []
        seen = set()
        for title in all_titles:
            if isinstance(title, str) and title and title not in seen:
                unique_titles.append(title)
                seen.add(title)
        
        management_metadata['Used_Titles'] = unique_titles
        
        return management_metadata
    
    def map_to_extended_metadata(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """映射到扩展元数据结构"""
        extended_metadata = {
            'RelatedPeople': [],
            'RelatedCollections': [],
            'Digitalization': {
                'edmIsShownAt': item.get('edmIsShownAt', ''),
                'edmIsShownBy': item.get('edmIsShownBy', ''),
                'edmPreview': item.get('edmPreview', '')
            },
            'DocumentationsAPI': item.get('link', ''),
            'OriginalData': {
                'guid': item.get('guid', ''),
                'europeanaCollectionName': item.get('europeanaCollectionName', ''),
                'provider': item.get('provider', ''),
                'type': item.get('type', ''),
                'language': item.get('language', [])
            }
        }
        
        # 提取相关人员
        if 'dcCreator' in item:
            creators = self._flatten_list(item['dcCreator'])
            extended_metadata['RelatedPeople'].extend(creators)
        
        # 相关收藏
        if 'europeanaCollectionName' in item:
            collections = self._flatten_list(item['europeanaCollectionName'])
            extended_metadata['RelatedCollections'].extend(collections)
        
        return extended_metadata
    
    def process_item(self, item: Dict[str, Any], text: str, 
                    lda_topics: List[Dict] = None) -> Dict[str, Any]:
        """处理单个数据项，生成完整的映射结构"""
        try:
            result = {
                'id': item.get('id', ''),
                'DescriptiveMetadata': self.map_to_descriptive_metadata(item, text, lda_topics),
                'Metadata_for_Management': self.map_to_management_metadata(item),
                'ExtendedMetadata': self.map_to_extended_metadata(item),
                'ProcessingMetadata': {
                    'processed_date': datetime.now().isoformat(),
                    'preprocessing_metadata': item.get('preprocessing_metadata', {})
                }
            }
            return result
        except Exception as e:
            print(f"处理项目时出错 {item.get('id', 'unknown')}: {e}")
            return {
                'id': item.get('id', ''),
                'DescriptiveMetadata': {},
                'Metadata_for_Management': {},
                'ExtendedMetadata': {},
                'ProcessingMetadata': {
                    'processed_date': datetime.now().isoformat(),
                    'error': str(e)
                }
            }