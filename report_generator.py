#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Report Generation Module
Function: Generate various analysis reports and statistics
Purpose: Analyzes porcelain/ceramic collection data and creates comprehensive reports
"""

import json
import pandas as pd
from datetime import datetime
from collections import Counter
from typing import List, Dict, Any
import matplotlib.pyplot as plt
import numpy as np

class ReportGenerator:
    """
    Report Generator Class
    Handles the generation of detailed analysis reports for porcelain/ceramic collection data
    """
    
    def __init__(self):
        """Initialize the report generator with empty data"""
        self.data = None
    
    def generate_analysis_report(self, data_file: str):
        """
        Generate a detailed data analysis report
        
        Args:
            data_file (str): Path to the JSON file containing porcelain data
            
        Creates:
            - Text analysis report with comprehensive statistics
            - CSV summary file with key metrics
            - Visualization plots (if enabled)
        """
        try:
            # Load the JSON data file
            with open(data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            
            # Create output filename by replacing .json extension
            report_file = data_file.replace('.json', '_analysis_report.txt')
            
            # Write the comprehensive analysis report
            with open(report_file, 'w', encoding='utf-8') as f:
                # Write report header
                f.write("Porcelain Data Comprehensive Analysis Report\n")
                f.write("=" * 100 + "\n")
                f.write(f"Generation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Records: {len(self.data)}\n")
                f.write("=" * 100 + "\n\n")
                
                # Write each analysis section
                # Each method analyzes a specific aspect of the porcelain data
                self._write_quality_overview(f)      # Data quality metrics
                self._write_lda_analysis(f)          # Topic modeling results
                self._write_decoration_analysis(f)   # Decoration patterns and themes
                self._write_shape_analysis(f)        # Vessel shapes and forms
                self._write_function_analysis(f)     # Functional purposes
                self._write_glaze_analysis(f)        # Glaze types and techniques
                self._write_material_analysis(f)     # Material composition
                self._write_production_analysis(f)   # Production locations and kilns
                self._write_period_analysis(f)       # Historical periods and dynasties
                self._write_institution_analysis(f)  # Contributing institutions
                self._write_color_analysis(f)        # Color distributions
                self._write_inscription_analysis(f)  # Marks and inscriptions
                self._write_completeness_analysis(f) # Data completeness metrics
                self._write_combination_analysis(f)  # Cross-category analysis
                self._write_summary(f)               # Overall summary statistics
                
                # Write report footer
                f.write("\n" + "=" * 100 + "\n")
                f.write(f"Report Generation Complete - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            print(f"📄 Detailed analysis report generated: {report_file}")
            
            # Generate CSV summary for easier data manipulation
            self.generate_summary_csv(report_file.replace('.txt', '_summary.csv'))
            
            # Generate visualization charts (currently disabled)
            self.generate_visualizations(data_file.replace('.json', '_plots'))
            
        except Exception as e:
            print(f"Report generation failed: {e}")
            import traceback
            traceback.print_exc()
    
    def _write_quality_overview(self, f):
        """
        Write data quality overview section
        Analyzes quality scores and their distribution
        
        Args:
            f: File handle for writing output
        """
        f.write("【Data Quality Overview】\n")
        f.write("-" * 80 + "\n")
        
        quality_scores = []
        # Define quality score ranges and their labels
        quality_distribution = {
            'Excellent (>0.8)': 0,
            'Good (0.6-0.8)': 0,
            'Medium (0.4-0.6)': 0,
            'Poor (0.2-0.4)': 0,
            'Very Poor (<0.2)': 0
        }
        
        # Collect quality scores and categorize them
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                score = item['DescriptiveMetadata'].get('quality_score', 0)
                quality_scores.append(score)
                
                # Categorize score into appropriate range
                if score > 0.8:
                    quality_distribution['Excellent (>0.8)'] += 1
                elif score > 0.6:
                    quality_distribution['Good (0.6-0.8)'] += 1
                elif score > 0.4:
                    quality_distribution['Medium (0.4-0.6)'] += 1
                elif score > 0.2:
                    quality_distribution['Poor (0.2-0.4)'] += 1
                else:
                    quality_distribution['Very Poor (<0.2)'] += 1
        
        # Write quality statistics if scores exist
        if quality_scores:
            f.write(f"Average Quality Score: {sum(quality_scores)/len(quality_scores):.3f}\n")
            f.write(f"Maximum Quality Score: {max(quality_scores):.3f}\n")
            f.write(f"Minimum Quality Score: {min(quality_scores):.3f}\n\n")
            
            f.write("Quality Distribution:\n")
            # Create visual bar chart in text format
            for category, count in quality_distribution.items():
                percentage = count/len(self.data)*100
                bar = '█' * int(percentage/2)  # Create proportional bar
                f.write(f"  {category:20} {bar:25} {count:5d} ({percentage:5.1f}%)\n")
    
    def _write_lda_analysis(self, f):
        """
        Write LDA (Latent Dirichlet Allocation) topic analysis
        Analyzes topic modeling results to identify thematic patterns
        
        Args:
            f: File handle for writing output
        """
        f.write("\n【LDA Topic Analysis】\n")
        f.write("-" * 80 + "\n")
        
        topic_counter = {}
        items_with_topics = 0
        topic_combinations = {}
        
        # Process each item's LDA topics
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                lda_topics = item['DescriptiveMetadata'].get('lda_topics', [])
                
                if lda_topics:
                    items_with_topics += 1
                    topic_ids = []
                    
                    # Count individual topics
                    for topic in lda_topics:
                        topic_id = topic.get('topic_id', -1)
                        topic_name = f"Topic{topic_id + 1}"
                        topic_counter[topic_name] = topic_counter.get(topic_name, 0) + 1
                        topic_ids.append(topic_name)
                    
                    # Track topic combinations (co-occurring topics)
                    if len(topic_ids) > 1:
                        combo = ' + '.join(topic_ids[:2])  # Take first two topics
                        topic_combinations[combo] = topic_combinations.get(combo, 0) + 1
        
        # Write topic statistics
        f.write(f"Records with LDA topics: {items_with_topics} ({items_with_topics/len(self.data)*100:.2f}%)\n\n")
        
        if topic_counter:
            f.write("Topic Distribution:\n")
            for topic, count in sorted(topic_counter.items(), key=lambda x: x[1], reverse=True):
                f.write(f"  - {topic}: {count}\n")
            
            # Show common topic combinations
            if topic_combinations:
                f.write("\nCommon Topic Combinations (Top 10):\n")
                for combo, count in sorted(topic_combinations.items(), key=lambda x: x[1], reverse=True)[:10]:
                    f.write(f"  - {combo}: {count}\n")
    
    def _write_decoration_analysis(self, f):
        """
        Write decoration type distribution analysis
        Categorizes and counts different decoration themes
        
        Args:
            f: File handle for writing output
        """
        f.write("\n【Decoration Type Distribution】\n")
        f.write("-" * 80 + "\n")
        
        # Define decoration theme categories
        decoration_themes = {
            'floral': [],      # Flower and plant motifs
            'figural': [],     # Human figures
            'animal': [],      # Animal motifs
            'landscape': [],   # Landscape scenes
            'geometric': [],   # Geometric patterns
            'calligraphy': [], # Text and calligraphy
            'symbolic': [],    # Symbolic motifs
            'color': [],       # Color-based decorations
            'other': []        # Uncategorized decorations
        }
        
        # Categorize decorations by theme
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                decorations = item['DescriptiveMetadata'].get('Decorations', [])
                for dec in decorations:
                    if ':' in dec:
                        # Split theme and detail (format: "theme:detail")
                        theme, detail = dec.split(':', 1)
                        if theme in decoration_themes:
                            decoration_themes[theme].append(detail)
                        else:
                            decoration_themes['other'].append(dec)
                    else:
                        decoration_themes['other'].append(dec)
        
        # Print statistics for each theme
        for theme, details in decoration_themes.items():
            if details:
                f.write(f"\n{theme.upper()} Theme (Total: {len(details)} items):\n")
                detail_counter = Counter(details)
                # Show top 10 most common details for this theme
                for detail, count in detail_counter.most_common(10):
                    f.write(f"  - {detail}: {count}\n")
    
    def _write_shape_analysis(self, f):
        """
        Write vessel shape distribution analysis
        Categorizes items by their shape/form
        
        Args:
            f: File handle for writing output
        """
        f.write("\n【Vessel Shape Distribution】\n")
        f.write("-" * 80 + "\n")
        
        shape_main = {}      # Main shape categories
        shape_specific = {}  # Specific shape descriptions
        
        # Define main shape categories
        main_shapes = ['bowl', 'vase', 'jar', 'plate', 'cup', 'pot', 'bottle', 'box', 'censer', 'ewer']
        
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                shapes = item['DescriptiveMetadata'].get('Shape', [])
                for shape in shapes:
                    if shape in main_shapes:
                        shape_main[shape] = shape_main.get(shape, 0) + 1
                    else:
                        # Treat as specific/detailed shape description
                        shape_specific[shape] = shape_specific.get(shape, 0) + 1
        
        # Display main shape categories with visual bars
        f.write("Main Shape Categories:\n")
        for shape, count in sorted(shape_main.items(), key=lambda x: x[1], reverse=True):
            percentage = count/len(self.data)*100
            bar = '█' * int(percentage/2)
            f.write(f"  {shape:12} {bar:20} {count:4d} ({percentage:5.1f}%)\n")
        
        # Display specific shape descriptions
        if shape_specific:
            f.write("\nSpecific Shape Descriptions (Top 20):\n")
            for shape, count in sorted(shape_specific.items(), key=lambda x: x[1], reverse=True)[:20]:
                f.write(f"  - {shape}: {count}\n")
    
    def _write_function_analysis(self, f):
        """
        Write functional purpose distribution analysis
        Analyzes what the porcelain items were used for
        
        Args:
            f: File handle for writing output
        """
        f.write("\n【Functional Distribution】\n")
        f.write("-" * 80 + "\n")
        
        function_counter = {}
        multi_function_count = 0  # Items with multiple functions
        
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                functions = item['DescriptiveMetadata'].get('Function', [])
                if len(functions) > 1:
                    multi_function_count += 1
                for func in functions:
                    function_counter[func] = function_counter.get(func, 0) + 1
        
        if function_counter:
            f.write(f"Multi-function items: {multi_function_count} ({multi_function_count/len(self.data)*100:.1f}%)\n\n")
            f.write("Function Category Distribution:\n")
            # Display functions with visual bars
            for func, count in sorted(function_counter.items(), key=lambda x: x[1], reverse=True):
                percentage = count/len(self.data)*100
                bar = '█' * int(percentage/2)
                f.write(f"  {func:12} {bar:20} {count:4d} ({percentage:5.1f}%)\n")
    
    def _write_glaze_analysis(self, f):
        """
        Write glaze technology distribution analysis
        Analyzes different glaze types and techniques used
        
        Args:
            f: File handle for writing output
        """
        f.write("\n【Glaze Technology Distribution】\n")
        f.write("-" * 80 + "\n")
        
        glaze_counter = {}
        multi_glaze_count = 0  # Items with multiple glazes
        
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                glazes = item['DescriptiveMetadata'].get('Glaze', [])
                if len(glazes) > 1:
                    multi_glaze_count += 1
                for glaze in glazes:
                    glaze_counter[glaze] = glaze_counter.get(glaze, 0) + 1
        
        if glaze_counter:
            f.write(f"Multi-glaze items: {multi_glaze_count} ({multi_glaze_count/len(self.data)*100:.1f}%)\n\n")
            # Show top 20 glaze types
            for glaze, count in sorted(glaze_counter.items(), key=lambda x: x[1], reverse=True)[:20]:
                percentage = count/len(self.data)*100
                f.write(f"  - {glaze}: {count} ({percentage:.1f}%)\n")
    
    def _write_material_analysis(self, f):
        """
        Write material composition distribution analysis
        Analyzes the paste/body materials used in production
        
        Args:
            f: File handle for writing output
        """
        f.write("\n【Material Distribution】\n")
        f.write("-" * 80 + "\n")
        
        material_counter = {}
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                materials = item['DescriptiveMetadata'].get('Paste', [])
                for material in materials:
                    material_counter[material] = material_counter.get(material, 0) + 1
        
        if material_counter:
            # Display materials with visual bars
            for material, count in sorted(material_counter.items(), key=lambda x: x[1], reverse=True):
                percentage = count/len(self.data)*100
                bar = '█' * int(percentage)
                f.write(f"  {material:12} {bar:40} {count:4d} ({percentage:5.1f}%)\n")
    
    def _write_production_analysis(self, f):
        """
        Write production location distribution analysis - hierarchical version
        Analyzes where items were produced, including countries, regions, and specific kilns
        
        Args:
            f: File handle for writing output
        """
        f.write("\n【Production Location Distribution】\n")
        f.write("-" * 80 + "\n")
        
        # Define function to identify Delftware (nested function)
        def identify_delftware(item):
            """
            Enhanced function to identify Delftware ceramics
            Uses multiple indicators to identify Dutch tin-glazed earthenware
            
            Args:
                item: Single item from the dataset
                
            Returns:
                bool: True if item is likely Delftware
            """
            
            # Extract all relevant text fields
            descriptions = item.get('DescriptiveMetadata', {}).get('Descriptions', [])
            production_places = item.get('DescriptiveMetadata', {}).get('ProductionPlace', [])
            glazes = item.get('DescriptiveMetadata', {}).get('Glaze', [])
            decorations = item.get('DescriptiveMetadata', {}).get('Decorations', [])
            colors = item.get('DescriptiveMetadata', {}).get('ColoredDrawing', [])
            materials = item.get('DescriptiveMetadata', {}).get('Paste', [])
            
            # Combine all text for analysis
            all_text = ' '.join([
                ' '.join(descriptions),
                ' '.join(production_places),
                ' '.join(glazes),
                ' '.join(decorations),
                ' '.join(colors),
                ' '.join(materials)
            ]).lower()
            
            # Strong indicators (any single match confirms Delftware)
            strong_indicators = [
                'delft', 'delfts', 'delftware', 'delf',
                'delft blue', 'delfts blauw',
                'royal delft', 'de porceleyne fles',
                'dutch delftware'
            ]
            
            # Check for strong indicators
            if any(indicator in all_text for indicator in strong_indicators):
                return True
            
            # Check for combination features (multiple features needed)
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
            
            # Combined logic for identification
            if has_tin_glaze and (has_dutch_reference or has_blue_white):
                return True
            
            if has_earthenware and has_tin_glaze:
                return True
            
            if has_blue_white and has_dutch_reference:
                return True
            
            return False
        
        # Define production location hierarchy
        # Maps countries to their regions and specific production centers
        place_hierarchy = {
            # China - Major ceramic production country
            'china': {
                'country': 'China',
                'regions': {
                    'jingdezhen': 'Jiangxi',      # Famous porcelain capital
                    'longquan': 'Zhejiang',        # Celadon production center
                    'dehua': 'Fujian',             # White porcelain (Blanc de Chine)
                    'yixing': 'Jiangsu',           # Purple clay teaware
                    'jun': 'Henan',                # Jun ware
                    'ding': 'Hebei',               # Ding ware
                    'cizhou': 'Hebei',             # Cizhou ware
                    'yaozhou': 'Shaanxi',          # Yaozhou ware
                    'ru': 'Henan',                 # Ru ware
                    'guan': 'Zhejiang',            # Guan (official) ware
                    'ge': 'Zhejiang',              # Ge ware
                    'export': 'Export/Canton'      # Export porcelain
                }
            },
            # Netherlands - Important for Delftware
            'netherlands': {
                'country': 'Netherlands',
                'regions': {
                    'delft': 'South Holland',      # Famous for Delftware
                    'amsterdam': 'North Holland',
                    'rotterdam': 'South Holland',
                    'haarlem': 'North Holland',
                    'makkum': 'Friesland'          # Makkum pottery
                }
            },
            # Belgium - Early faience production
            'belgium': {
                'country': 'Belgium',
                'regions': {
                    'brussels': 'Brussels',
                    'antwerp': 'Antwerp',          # Important early center
                    'ghent': 'East Flanders',
                    'tournai': 'Hainaut'
                }
            },
            # Other European production centers
            'germany': {
                'country': 'Germany',
                'regions': {
                    'meissen': 'Saxony',           # Famous for European porcelain
                    'dresden': 'Saxony'
                }
            },
            'france': {
                'country': 'France',
                'regions': {
                    'sevres': 'Île-de-France',     # Royal porcelain
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
        
        # Place name normalization mapping
        # Maps various spellings and languages to standard names
        place_normalization = {
            # Chinese variants in different languages
            'китай': 'china',      # Russian
            'kina': 'china',        # Swedish
            'cina': 'china',        # Italian
            'chine': 'china',       # French
            
            # Chinese kiln name variants
            'jun': 'jun',
            'jun kiln': 'jun',
            'junzhou': 'jun',
            'chun': 'jun',
            'ding kiln': 'ding',
            'dingzhou': 'ding',
            'tz\'u-chou': 'cizhou',
            'te-hua': 'dehua',
            'ching-te-chen': 'jingdezhen',
            
            # Brussels variants in different languages
            'bruxelles': 'brussels',    # French
            'brussel': 'brussels',      # Dutch
            'brusela': 'brussels',      # Spanish
            'bruksela': 'brussels',     # Polish
            'brusel': 'brussels',       # Czech
            'briuselis': 'brussels',    # Lithuanian
            'briuselio': 'brussels',    # Lithuanian
            'brisele': 'brussels',      # Latvian
            'briseles': 'brussels',     # Latvian
            'an bhruiséil': 'brussels', # Irish

            # Delft-related variants
            'delft': 'delft',
            'delfts': 'delft',
            'delftware': 'delft',
            'delf': 'delft',
            'dutch delftware': 'delft',
            'english delftware': 'delft',
            
            # Antwerp variants (important early production center)
            'antwerpen': 'antwerp',     # Dutch/German
            'anvers': 'antwerp',        # French
            
            # Other Dutch cities
            'haarlem': 'haarlem',
            'rotterdam': 'rotterdam',
            'makkum': 'makkum',
            
            # Country name variants
            'nederland': 'netherlands',
            'holland': 'netherlands',
            'belgian': 'belgium',
            'belgique': 'belgium',      # French
            'belgië': 'belgium',        # Dutch
            'english': 'england',
            'uk': 'england',
            'united kingdom': 'england'
        }
        
        # Initialize statistics collections
        item_by_country = {}
        item_by_place = {}
        place_frequency = {}
        
        # Debug statistics for Delftware identification
        delft_identified_count = 0
        tin_glaze_count = 0
        blue_white_dutch_count = 0
        
        # Process each item in the collection
        for idx, item in enumerate(self.data):
            item_country = None
            item_specific_place = None
            
            # First try enhanced Delftware identification
            if identify_delftware(item):
                item_country = 'Netherlands'
                item_specific_place = 'delft'
                delft_identified_count += 1
            
            # Continue processing other production location information
            if 'DescriptiveMetadata' in item:
                places = item['DescriptiveMetadata'].get('ProductionPlace', [])
                
                # Collect and normalize all place names
                normalized_places = []
                for place in places:
                    if place and isinstance(place, str):
                        place_lower = place.lower().strip()
                        
                        # Normalize place name
                        normalized = place_normalization.get(place_lower, place_lower)
                        
                        # Record frequency for debugging
                        place_frequency[normalized] = place_frequency.get(normalized, 0) + 1
                        normalized_places.append(normalized)
                
                # If country not yet determined, continue processing
                if not item_country:
                    # Determine country and specific production site
                    for country, info in place_hierarchy.items():
                        # Check if country name appears
                        if country in normalized_places:
                            item_country = info['country']
                        
                        # Check for specific locations within the country
                        for region, province in info['regions'].items():
                            if region in normalized_places:
                                item_country = info['country']
                                item_specific_place = region
                                break
                        
                        if item_country:
                            break
                
                # Even with country identified, check for more specific location
                if item_country and not item_specific_place:
                    # Check if normalized_places contains specific kiln names
                    for place in normalized_places:
                        # Check corresponding country's specific locations
                        for country, info in place_hierarchy.items():
                            if info['country'] == item_country:
                                for region in info['regions'].keys():
                                    if region == place or region in place:
                                        item_specific_place = region
                                        break
                                break
                
                # If no specific location found yet, try extracting from descriptions (especially for Chinese kilns)
                if item_country == 'China' and not item_specific_place:
                    descriptions = ' '.join(item['DescriptiveMetadata'].get('Descriptions', [])).lower()
                    
                    # Check for kiln information in descriptions
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
                
                # Debug: Count tin glaze and blue-white features
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
            
            # Record classification
            if not item_country:
                item_country = 'Unknown'
                
            # Record by country
            if item_country not in item_by_country:
                item_by_country[item_country] = []
            item_by_country[item_country].append(idx)
            
            # Record by specific location
            if item_specific_place:
                place_key = f"{item_country}-{item_specific_place}"
                if place_key not in item_by_place:
                    item_by_place[place_key] = []
                item_by_place[place_key].append(idx)
            else:
                # Even without specific location, record country-level location
                if item_country != 'Unknown':
                    place_key = f"{item_country}-unspecified"
                    if place_key not in item_by_place:
                        item_by_place[place_key] = []
                    item_by_place[place_key].append(idx)
        
        # Output statistical results
        total = len(self.data)
        
        # 1. Statistics by country
        f.write("【Statistics by Country】\n")
        country_sorted = sorted(item_by_country.items(), key=lambda x: len(x[1]), reverse=True)
        
        for country, items in country_sorted:
            count = len(items)
            percentage = count / total * 100
            f.write(f"  {country:20} {count:5d} ({percentage:5.1f}%)\n")
        
        # 2. China vs Europe comparison
        china_count = len(item_by_country.get('China', []))
        netherlands_count = len(item_by_country.get('Netherlands', []))
        belgium_count = len(item_by_country.get('Belgium', []))
        european_count = netherlands_count + belgium_count + len(item_by_country.get('Germany', [])) + \
                        len(item_by_country.get('France', [])) + len(item_by_country.get('England', []))
        
        f.write("\n【China vs European Porcelain Comparison】\n")
        f.write(f"  Chinese Porcelain: {china_count} ({china_count/total*100:.1f}%)\n")
        f.write(f"  European Porcelain: {european_count} ({european_count/total*100:.1f}%)\n")
        f.write(f"    - Netherlands (incl. Delft): {netherlands_count} ({netherlands_count/total*100:.1f}%)\n")
        f.write(f"    - Belgium: {belgium_count} ({belgium_count/total*100:.1f}%)\n")
        
        if netherlands_count > 0:
            # Count specific Delftware items
            delft_count = len(item_by_place.get('Netherlands-delft', []))
            f.write(f"    - Delftware specifically: {delft_count} ({delft_count/total*100:.1f}%)\n")
        
        # 3. Specific production site statistics
        f.write("\n【Specific Production Site Distribution (Top 30)】\n")
        place_sorted = sorted(item_by_place.items(), key=lambda x: len(x[1]), reverse=True)[:30]
        
        for place, items in place_sorted:
            count = len(items)
            percentage = count / total * 100
            f.write(f"  {place:30} {count:4d} ({percentage:5.1f}%)\n")
        
        # 4. Production site identification details
        f.write("\n【Production Site Identification Details】\n")
        china_unspecified = len(item_by_place.get('China-unspecified', []))
        if china_unspecified > 0:
            f.write(f"  China - Unspecified kiln: {china_unspecified} ({china_unspecified/total*100:.1f}%)\n")
            f.write("  Suggestion: Check original data for more detailed kiln information\n")
        
        netherlands_unspecified = len(item_by_place.get('Netherlands-unspecified', []))
        if netherlands_unspecified > 0:
            f.write(f"  Netherlands - Unspecified location: {netherlands_unspecified} ({netherlands_unspecified/total*100:.1f}%)\n")
        
        # 5. Major Chinese kilns
        china_kilns = [(p, items) for p, items in item_by_place.items() if p.startswith('China-') and not p.endswith('unspecified')]
        if china_kilns:
            f.write("\n【Major Chinese Porcelain Centers】\n")
            china_kilns_sorted = sorted(china_kilns, key=lambda x: len(x[1]), reverse=True)
            for place, items in china_kilns_sorted:
                kiln_name = place.split('-')[1]
                count = len(items)
                f.write(f"  {kiln_name:15} {count:4d}\n")
        
        # 6. Major European production sites
        european_places = [(p, items) for p, items in item_by_place.items() 
                        if any(p.startswith(c) for c in ['Netherlands-', 'Belgium-', 'Germany-', 'France-', 'England-']) 
                        and not p.endswith('unspecified')]
        if european_places:
            f.write("\n【Major European Porcelain Centers】\n")
            european_sorted = sorted(european_places, key=lambda x: len(x[1]), reverse=True)
            for place, items in european_sorted[:10]:
                count = len(items)
                f.write(f"  {place:30} {count:4d}\n")
        
        # 7. Data quality assessment
        unknown_count = len(item_by_country.get('Unknown', []))
        identified_count = total - unknown_count
        
        f.write("\n【Production Site Data Quality Assessment】\n")
        f.write(f"  Successfully identified: {identified_count} ({identified_count/total*100:.1f}%)\n")
        f.write(f"  Unidentified: {unknown_count} ({unknown_count/total*100:.1f}%)\n")
        
        # 8. Delftware identification analysis
        f.write("\n【Delftware Identification Analysis】\n")
        f.write(f"  Identified as Delftware by features: {delft_identified_count} ({delft_identified_count/total*100:.1f}%)\n")
        f.write(f"  Contains tin-glaze related terms: {tin_glaze_count} ({tin_glaze_count/total*100:.1f}%)\n")
        f.write(f"  Contains 'Dutch blue-white' features: {blue_white_dutch_count} ({blue_white_dutch_count/total*100:.1f}%)\n")
        
        # 9. Raw production data frequency (for debugging)
        if place_frequency:
            f.write("\n【Raw Production Data Frequency (Top 20)】\n")
            freq_sorted = sorted(place_frequency.items(), key=lambda x: x[1], reverse=True)[:20]
            for place, freq in freq_sorted:
                f.write(f"  '{place}': {freq}\n")

    def _write_period_analysis(self, f):
        """
        Write historical period distribution analysis - fixed version
        Analyzes dynasties, years, and centuries
        
        Args:
            f: File handle for writing output
        """
        f.write("\n【Period Distribution】\n")
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
                
                # Get period information
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
                        # Ensure year is an integer
                        try:
                            year_int = int(year) if isinstance(year, str) else year
                            # Only count reasonable years
                            if 1000 <= year_int <= 2025:
                                year_counter[year_int] = year_counter.get(year_int, 0) + 1
                                
                                # Calculate century
                                century = (year_int - 1) // 100 + 1
                                century_str = f"{century}th century"
                                century_counter[century_str] = century_counter.get(century_str, 0) + 1
                        except (ValueError, TypeError):
                            continue
                
                # Collect year-dynasty mapping
                if period_summary and 'dynasty_mapping' in period_summary:
                    # Ensure years in mapping are integers
                    for y, d in period_summary['dynasty_mapping'].items():
                        try:
                            year_int = int(y) if isinstance(y, str) else y
                            year_dynasty_mapping[year_int] = d
                        except (ValueError, TypeError):
                            continue
        
        f.write(f"Records with period info: {total_with_period} ({total_with_period/len(self.data)*100:.1f}%)\n")
        f.write(f"Records with year info: {total_with_year} ({total_with_year/len(self.data)*100:.1f}%)\n")
        f.write(f"Records without period info: {len(self.data) - total_with_period} ({(len(self.data) - total_with_period)/len(self.data)*100:.1f}%)\n\n")
        
        # Dynasty distribution
        if dynasty_counter:
            f.write("Dynasty Distribution:\n")
            # Define chronological order for Chinese dynasties
            dynasty_order = ['Tang', 'Song', 'Yuan', 'Ming', 'Qing', 'Republic', 'Modern']
            
            for dynasty in dynasty_order:
                if dynasty in dynasty_counter:
                    count = dynasty_counter[dynasty]
                    percentage = count/total_with_period*100 if total_with_period > 0 else 0
                    total_percentage = count/len(self.data)*100
                    bar = '█' * int(total_percentage/2)
                    f.write(f"  {dynasty:10} {bar:40} {count:4d} ({percentage:5.1f}% of dated, {total_percentage:5.1f}% of total)\n")
        
        # Century distribution
        if century_counter:
            f.write("\nCentury Distribution:\n")
            # Sort by century number
            sorted_centuries = sorted(century_counter.items(), key=lambda x: int(x[0].split('th')[0]))
            for century, count in sorted_centuries:
                percentage = count/len(self.data)*100
                f.write(f"  - {century}: {count} ({percentage:.1f}%)\n")
        
        # Year-dynasty correspondence table
        if year_dynasty_mapping:
            f.write("\nYear-Dynasty Correspondence (Examples):\n")
            # Only show reasonable years, ensure comparison is with integers
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
        
        # Specific year distribution
        if year_counter:
            f.write("\nSpecific Year Distribution (Top 30):\n")
            # Only show reasonable years, ensure all are integers
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
                dynasty = year_dynasty_mapping.get(year, 'Unknown')
                f.write(f"  - {year} ({dynasty}): {count}\n")
    

    def _write_summary(self, f):
        """
        Write comprehensive statistical summary
        Provides overall metrics and data quality recommendations
        
        Args:
            f: File handle for writing output
        """
        f.write("\n【Comprehensive Statistical Summary】\n")
        f.write("=" * 80 + "\n")
        
        # Calculate key metrics
        quality_scores = []
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                score = item['DescriptiveMetadata'].get('quality_score', 0)
                quality_scores.append(score)
        
        # Calculate field fill rates
        field_stats = {
            'Decoration Info': sum(1 for item in self.data if item.get('DescriptiveMetadata', {}).get('Decorations', [])),
            'Shape Info': sum(1 for item in self.data if item.get('DescriptiveMetadata', {}).get('Shape', [])),
            'Function Info': sum(1 for item in self.data if item.get('DescriptiveMetadata', {}).get('Function', [])),
            'Glaze Info': sum(1 for item in self.data if item.get('DescriptiveMetadata', {}).get('Glaze', [])),
            'Material Info': sum(1 for item in self.data if item.get('DescriptiveMetadata', {}).get('Paste', [])),
            'Production Info': sum(1 for item in self.data if item.get('DescriptiveMetadata', {}).get('ProductionPlace', [])),
            'Color Info': sum(1 for item in self.data if item.get('DescriptiveMetadata', {}).get('ColoredDrawing', [])),
            'Inscription Info': sum(1 for item in self.data if item.get('DescriptiveMetadata', {}).get('Inscriptions', []))
        }
        
        avg_fields_per_item = sum(field_stats.values()) / len(self.data) / len(field_stats)
        
        f.write(f"📊 Key Metrics:\n")
        f.write(f"  - Total Records: {len(self.data)}\n")
        f.write(f"  - Average Field Fill Rate: {avg_fields_per_item*100:.1f}%\n")
        if quality_scores:
            f.write(f"  - Average Quality Score: {sum(quality_scores)/len(quality_scores):.3f}\n")
            f.write(f"  - High Quality Records (>0.5): {sum(1 for s in quality_scores if s > 0.5)} ({sum(1 for s in quality_scores if s > 0.5)/len(self.data)*100:.1f}%)\n")
            f.write(f"  - Excellent Records (>0.8): {sum(1 for s in quality_scores if s > 0.8)} ({sum(1 for s in quality_scores if s > 0.8)/len(self.data)*100:.1f}%)\n")
        
        f.write(f"\n📈 Data Characteristics:\n")
        
        # Calculate overall coverage statistics
        total_coverage = {
            'Has Decoration Description': field_stats['Decoration Info'],
            'Has Shape Description': field_stats['Shape Info'],
            'Has Function Description': field_stats['Function Info'],
            'Has Glaze Description': field_stats['Glaze Info'],
            'Has Color Description': field_stats['Color Info']
        }
        
        for desc, count in total_coverage.items():
            f.write(f"  - {desc}: {count} ({count/len(self.data)*100:.1f}%)\n")
        
        # Data quality recommendations
        f.write(f"\n💡 Data Quality Recommendations:\n")
        if avg_fields_per_item < 0.5:
            f.write(f"  - Low average field fill rate ({avg_fields_per_item*100:.1f}%), consider adding more descriptive information\n")
        if field_stats['Function Info'] < len(self.data) * 0.3:
            f.write(f"  - Function info coverage only {field_stats['Function Info']/len(self.data)*100:.1f}%, consider adding function descriptions\n")
        if field_stats['Glaze Info'] < len(self.data) * 0.3:
            f.write(f"  - Glaze info coverage only {field_stats['Glaze Info']/len(self.data)*100:.1f}%, consider adding glaze technology information\n")
    
    
    def _write_institution_analysis(self, f):
        """
        Write contributing institution distribution analysis
        Analyzes which museums/institutions provided the data
        
        Args:
            f: File handle for writing output
        """
        f.write("\n【Contributing Institution Distribution】\n")
        f.write("-" * 80 + "\n")
        
        institution_counter = {}
        country_institution = {}
        
        for item in self.data:
            if 'Metadata_for_Management' in item:
                institution_data = item['Metadata_for_Management'].get('ProvidingInstitution', '')
                country_data = item['Metadata_for_Management'].get('ProvidingInstitutionCountry', '')
                
                # Handle institution data that might be a list
                institutions = []
                if isinstance(institution_data, list):
                    # If list, extract all non-empty strings
                    for inst in institution_data:
                        if isinstance(inst, str) and inst.strip():
                            institutions.append(inst.strip())
                elif isinstance(institution_data, str) and institution_data.strip():
                    # If non-empty string
                    institutions.append(institution_data.strip())
                
                # Handle country data that might be a list
                countries = []
                if isinstance(country_data, list):
                    # If list, extract all non-empty strings
                    for c in country_data:
                        if isinstance(c, str) and c.strip():
                            countries.append(c.strip())
                elif isinstance(country_data, str) and country_data.strip():
                    # If non-empty string
                    countries.append(country_data.strip())
                
                # Count each institution
                for institution in institutions:
                    institution_counter[institution] = institution_counter.get(institution, 0) + 1
                    
                    # Associate country with institution
                    for country in countries:
                        if country not in country_institution:
                            country_institution[country] = {}
                        country_institution[country][institution] = country_institution[country].get(institution, 0) + 1
        
        if institution_counter:
            f.write(f"Total Different Institutions: {len(institution_counter)}\n\n")
            
            # Display institutions grouped by country
            if country_institution:
                f.write("Major Institutions by Country:\n")
                for country in sorted(country_institution.keys())[:10]:
                    institutions = country_institution[country]
                    f.write(f"\n{country}:\n")
                    # Show top 3 institutions per country
                    for inst, count in sorted(institutions.items(), key=lambda x: x[1], reverse=True)[:3]:
                        f.write(f"  - {inst}: {count}\n")
            
            f.write("\nAll Institutions (Top 20):\n")
            for institution, count in sorted(institution_counter.items(), key=lambda x: x[1], reverse=True)[:20]:
                f.write(f"  - {institution}: {count} ({count/len(self.data)*100:.2f}%)\n")
    
    def _write_color_analysis(self, f):
        """
        Write color distribution analysis
        Analyzes color schemes and combinations
        
        Args:
            f: File handle for writing output
        """
        f.write("\n【Color Distribution】\n")
        f.write("-" * 80 + "\n")
        
        color_counter = {}
        color_combinations = {}
        
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                colors = item['DescriptiveMetadata'].get('ColoredDrawing', [])
                for color in colors:
                    color_counter[color] = color_counter.get(color, 0) + 1
                
                # Track color combinations
                if len(colors) > 1:
                    color_combo = ' + '.join(sorted(colors))
                    color_combinations[color_combo] = color_combinations.get(color_combo, 0) + 1
        
        if color_counter:
            f.write("Single Color Statistics:\n")
            for color, count in sorted(color_counter.items(), key=lambda x: x[1], reverse=True):
                percentage = count/len(self.data)*100
                bar = '█' * int(percentage/2)
                f.write(f"  {color:15} {bar:20} {count:4d} ({percentage:5.1f}%)\n")
            
            if color_combinations:
                f.write("\nCommon Color Combinations (Top 10):\n")
                for combo, count in sorted(color_combinations.items(), key=lambda x: x[1], reverse=True)[:10]:
                    f.write(f"  - {combo}: {count}\n")
    
    def _write_inscription_analysis(self, f):
        """
        Write inscription and mark information distribution
        Analyzes marks, signatures, and inscriptions on items
        
        Args:
            f: File handle for writing output
        """
        f.write("\n【Inscription Information Distribution】\n")
        f.write("-" * 80 + "\n")
        
        # Define inscription type categories
        inscription_types = {
            'mark': [],           # General marks
            'inscription': [],    # Text inscriptions
            'character mark': [], # Chinese character marks
            'reign mark': [],     # Imperial reign marks
            'signature': [],      # Artist signatures
            'period mark': [],    # Period/era marks
            'other': []          # Other inscription types
        }
        
        has_inscription_count = 0
        
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                inscriptions = item['DescriptiveMetadata'].get('Inscriptions', [])
                if inscriptions:
                    has_inscription_count += 1
                    
                    for inscription in inscriptions:
                        if ':' in inscription:
                            # Format is "type:detail"
                            ins_type, detail = inscription.split(':', 1)
                            if ins_type in inscription_types:
                                inscription_types[ins_type].append(detail)
                            else:
                                inscription_types['other'].append(inscription)
                        else:
                            inscription_types['other'].append(inscription)
        
        f.write(f"Records with inscriptions: {has_inscription_count} ({has_inscription_count/len(self.data)*100:.2f}%)\n")
        f.write(f"Records without inscriptions: {len(self.data) - has_inscription_count} ({(len(self.data) - has_inscription_count)/len(self.data)*100:.2f}%)\n\n")
        
        # Print each inscription type
        for ins_type, details in inscription_types.items():
            if details:
                f.write(f"\n{ins_type.upper()} (Total: {len(details)} items):\n")
                detail_counter = Counter(details)
                # Show top 5 most common for each type
                for detail, count in detail_counter.most_common(5):
                    f.write(f"  - {detail}: {count}\n")
    
    def _write_completeness_analysis(self, f):
        """
        Write data completeness analysis
        Evaluates how complete the metadata is for each record
        
        Args:
            f: File handle for writing output
        """
        f.write("\n【Data Completeness Analysis】\n")
        f.write("-" * 80 + "\n")
        
        completeness_levels = {}
        field_coverage = {}
        
        # Define fields to check for completeness
        fields_to_check = {
            'Description Info': lambda x: len(x.get('DescriptiveMetadata', {}).get('Descriptions', [])) > 0,
            'Decoration Info': lambda x: len(x.get('DescriptiveMetadata', {}).get('Decorations', [])) > 0,
            'Shape Info': lambda x: len(x.get('DescriptiveMetadata', {}).get('Shape', [])) > 0,
            'Function Info': lambda x: len(x.get('DescriptiveMetadata', {}).get('Function', [])) > 0,
            'Glaze Info': lambda x: len(x.get('DescriptiveMetadata', {}).get('Glaze', [])) > 0,
            'Material Info': lambda x: len(x.get('DescriptiveMetadata', {}).get('Paste', [])) > 0,
            'Production Info': lambda x: len(x.get('DescriptiveMetadata', {}).get('ProductionPlace', [])) > 0,
            'Color Info': lambda x: len(x.get('DescriptiveMetadata', {}).get('ColoredDrawing', [])) > 0,
            'Inscription Info': lambda x: len(x.get('DescriptiveMetadata', {}).get('Inscriptions', [])) > 0,
            'Title Info': lambda x: len(x.get('Metadata_for_Management', {}).get('Title', [])) > 0,
            'Period Info': lambda x: bool(x.get('Metadata_for_Management', {}).get('Period')),
            'Institution Info': lambda x: bool(x.get('Metadata_for_Management', {}).get('ProvidingInstitution')),
            'Digitalization Info': lambda x: bool(x.get('ExtendedMetadata', {}).get('Digitalization', {}).get('edmPreview'))
        }
        
        # Calculate coverage for each field
        for field_name, check_func in fields_to_check.items():
            count = sum(1 for item in self.data if check_func(item))
            field_coverage[field_name] = count
        
        # Track completeness levels
        for item in self.data:
            if 'Metadata_for_Management' in item:
                level = item['Metadata_for_Management'].get('CompletenessLevel', 0)
                completeness_levels[level] = completeness_levels.get(level, 0) + 1
        
        f.write("Field Coverage Rates:\n")
        for field, count in sorted(field_coverage.items(), key=lambda x: x[1], reverse=True):
            percentage = count/len(self.data)*100
            bar = '█' * int(percentage/5)
            f.write(f"  {field:20} {bar:20} {count:5d}/{len(self.data)} ({percentage:5.1f}%)\n")
        
        if completeness_levels:
            f.write("\nCompleteness Level Distribution:\n")
            for level, count in sorted(completeness_levels.items(), reverse=True):
                f.write(f"  - Level {level}: {count} ({count/len(self.data)*100:.2f}%)\n")
    
    def _write_combination_analysis(self, f):
        """
        Write combination analysis
        Analyzes relationships between different attributes
        
        Args:
            f: File handle for writing output
        """
        f.write("\n【Combination Analysis】\n")
        f.write("-" * 80 + "\n")
        
        # Shape-Function combinations
        shape_function_combinations = {}
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                shapes = item['DescriptiveMetadata'].get('Shape', [])
                functions = item['DescriptiveMetadata'].get('Function', [])
                
                # Only use main shape categories
                main_shapes = [s for s in shapes if s in ['bowl', 'vase', 'jar', 'plate', 'cup', 'pot', 'bottle', 'box', 'censer', 'ewer']]
                
                # Create combinations (take first of each for simplicity)
                for shape in main_shapes[:1]:
                    for function in functions[:1]:
                        combo = f"{shape} - {function}"
                        shape_function_combinations[combo] = shape_function_combinations.get(combo, 0) + 1
        
        if shape_function_combinations:
            f.write("Shape-Function Combinations (Top 20):\n")
            for combo, count in sorted(shape_function_combinations.items(), key=lambda x: x[1], reverse=True)[:20]:
                f.write(f"  - {combo}: {count}\n")
        
        # Color-Decoration theme combinations
        color_theme_combinations = {}
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                colors = item['DescriptiveMetadata'].get('ColoredDrawing', [])
                decorations = item['DescriptiveMetadata'].get('Decorations', [])
                
                # Extract decoration themes
                themes = set()
                for dec in decorations:
                    if ':' in dec:
                        theme, _ = dec.split(':', 1)
                        if theme in ['floral', 'figural', 'animal', 'landscape', 'geometric']:
                            themes.add(theme)
                
                # Create combinations (take first of each)
                for color in colors[:1]:
                    for theme in list(themes)[:1]:
                        combo = f"{color} + {theme}"
                        color_theme_combinations[combo] = color_theme_combinations.get(combo, 0) + 1
        
        if color_theme_combinations:
            f.write("\nColor-Decoration Theme Combinations (Top 15):\n")
            for combo, count in sorted(color_theme_combinations.items(), key=lambda x: x[1], reverse=True)[:15]:
                f.write(f"  - {combo}: {count}\n")
    
    
    
    def generate_summary_csv(self, output_file: str):
        """
        Generate CSV format statistical summary
        Creates a structured CSV file with key statistics
        
        Args:
            output_file (str): Path for the output CSV file
        """
        try:
            summary_data = []
            
            # Define categories to collect statistics for
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
            
            # Collect statistics for each category
            for item in self.data:
                # Process descriptive metadata
                if 'DescriptiveMetadata' in item:
                    desc = item['DescriptiveMetadata']
                    
                    # Quality score (special handling)
                    quality_score = desc.get('quality_score', 0)
                    categories['QualityScore'].append(quality_score)
                    
                    # Process list fields
                    for field in ['Decorations', 'Shape', 'Function', 'Glaze', 'Paste', 'ProductionPlace', 'ColoredDrawing', 'Inscriptions']:
                        if field in desc:
                            values = desc.get(field, [])
                            if isinstance(values, list):
                                for value in values:
                                    if value and field in categories:
                                        categories[field][value] = categories[field].get(value, 0) + 1
                
                # Process management metadata
                if 'Metadata_for_Management' in item:
                    mgmt = item['Metadata_for_Management']
                    for field in ['Period', 'ProvidingInstitution', 'ProvidingInstitutionCountry']:
                        value = mgmt.get(field, '')
                        if value and field in categories:
                            categories[field][value] = categories[field].get(value, 0) + 1
            
            # Convert to DataFrame format
            for category, counts in categories.items():
                if category == 'QualityScore':
                    # Special handling for quality scores
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
                   # Process dictionary categories
                   for value, count in counts.items():
                       summary_data.append({
                           'Category': category,
                           'Value': str(value)[:100],  # Limit length to 100 characters
                           'Count': count,
                           'Percentage': f"{count/len(self.data)*100:.2f}%"
                       })
           
           # Save to CSV file
           df = pd.DataFrame(summary_data)
           df.sort_values(['Category', 'Count'], ascending=[True, False], inplace=True)
           df.to_csv(output_file, index=False, encoding='utf-8-sig')  # utf-8-sig for Excel compatibility
           print(f"📊 Statistical summary CSV generated: {output_file}")
           
       except Exception as e:
           print(f"Failed to generate CSV summary: {e}")
   
   def generate_visualizations(self, output_dir: str):
       """
       Generate visualization charts
       Creates various plots to visualize the data
       Note: Currently disabled
       
       Args:
           output_dir (str): Directory path for saving plot images
       """
       # Temporarily disable plotting functionality
       print("📊 Visualization chart generation is temporarily disabled")
       return
       
       # Original plotting code kept for future use...
   
   def _plot_quality_distribution(self, output_dir):
       """
       Plot quality score distribution histogram
       Shows the distribution of data quality scores
       
       Args:
           output_dir: Directory path for saving the plot
       """
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
       """
       Plot vessel shape distribution pie chart
       Shows the proportion of different vessel shapes
       
       Args:
           output_dir: Directory path for saving the plot
       """
       shape_counter = {}
       for item in self.data:
           if 'DescriptiveMetadata' in item:
               shapes = item['DescriptiveMetadata'].get('Shape', [])
               for shape in shapes:
                   if shape in ['bowl', 'vase', 'jar', 'plate', 'cup', 'pot', 'bottle', 'box', 'censer', 'ewer']:
                       shape_counter[shape] = shape_counter.get(shape, 0) + 1
       
       if shape_counter:
           # Show top 8 shapes, combine others
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
       """
       Plot functional purpose distribution bar chart
       Shows the most common functions of porcelain items
       
       Args:
           output_dir: Directory path for saving the plot
       """
       function_counter = {}
       for item in self.data:
           if 'DescriptiveMetadata' in item:
               functions = item['DescriptiveMetadata'].get('Function', [])
               for func in functions:
                   function_counter[func] = function_counter.get(func, 0) + 1
       
       if function_counter:
           # Get top 10 functions
           sorted_functions = sorted(function_counter.items(), key=lambda x: x[1], reverse=True)[:10]
           
           plt.figure(figsize=(10, 6))
           functions = [f[0] for f in sorted_functions]
           counts = [f[1] for f in sorted_functions]
           
           plt.barh(functions, counts, color='skyblue', edgecolor='navy')
           plt.xlabel('Count')
           plt.ylabel('Function')
           plt.title('Top 10 Functions of Porcelain Items')
           plt.gca().invert_yaxis()  # Invert y-axis to show highest count at top
           plt.grid(axis='x', alpha=0.3)
           plt.savefig(f"{output_dir}/function_distribution.png", dpi=300, bbox_inches='tight')
           plt.close()
   
   def _plot_color_distribution(self, output_dir):
       """
       Plot color distribution bar chart
       Shows the frequency of different colors used
       
       Args:
           output_dir: Directory path for saving the plot
       """
       color_counter = {}
       for item in self.data:
           if 'DescriptiveMetadata' in item:
               colors = item['DescriptiveMetadata'].get('ColoredDrawing', [])
               for color in colors:
                   color_counter[color] = color_counter.get(color, 0) + 1
       
       if color_counter:
           # Get top 12 colors
           sorted_colors = sorted(color_counter.items(), key=lambda x: x[1], reverse=True)[:12]
           
           plt.figure(figsize=(12, 6))
           colors = [c[0] for c in sorted_colors]
           counts = [c[1] for c in sorted_colors]
           
           # Map color names to actual colors for visualization
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
           
           # Get bar colors based on color names
           bar_colors = [color_map.get(c, 'gray') for c in colors]
           
           plt.bar(colors, counts, color=bar_colors, edgecolor='black')
           plt.xlabel('Color')
           plt.ylabel('Count')
           plt.title('Distribution of Colors in Porcelain Items')
           plt.xticks(rotation=45, ha='right')  # Rotate labels for better readability
           plt.grid(axis='y', alpha=0.3)
           plt.tight_layout()
           plt.savefig(f"{output_dir}/color_distribution.png", dpi=300, bbox_inches='tight')
           plt.close()
   
   def _plot_period_timeline(self, output_dir):
       """
       Plot dynasty/period timeline
       Shows the distribution of items across different historical periods
       
       Args:
           output_dir: Directory path for saving the plot
       """
       # Initialize dynasty counters
       dynasty_counter = {
           'Song': 0,
           'Yuan': 0,
           'Ming': 0,
           'Qing': 0,
           'Modern': 0
       }
       
       # Count items by dynasty/period
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
               elif any(year in period for year in ['19', '20', '21']):  # Modern periods
                   dynasty_counter['Modern'] += 1
       
       # Create timeline plot if there's data
       if any(dynasty_counter.values()):
           plt.figure(figsize=(10, 6))
           dynasties = list(dynasty_counter.keys())
           counts = list(dynasty_counter.values())
           
           # Create line plot with markers
           plt.plot(dynasties, counts, 'o-', markersize=10, linewidth=2)
           plt.fill_between(range(len(dynasties)), counts, alpha=0.3)  # Add area under line
           plt.xlabel('Dynasty/Period')
           plt.ylabel('Number of Items')
           plt.title('Distribution of Porcelain Items Across Dynasties')
           plt.grid(True, alpha=0.3)
           plt.savefig(f"{output_dir}/period_timeline.png", dpi=300, bbox_inches='tight')
           plt.close()


# Main execution example
if __name__ == "__main__":
   """
   Example usage of the ReportGenerator class
   Run this script directly to generate a report from a JSON file
   """
   # Initialize the report generator
   generator = ReportGenerator()
   
   # Example: Generate report from a JSON file
   # Replace 'porcelain_data.json' with your actual data file path
   data_file = "porcelain_data.json"
   
   try:
       print("Starting report generation...")
       generator.generate_analysis_report(data_file)
       print("Report generation completed successfully!")
   except FileNotFoundError:
       print(f"Error: Data file '{data_file}' not found.")
       print("Please ensure the JSON data file exists in the current directory.")
   except Exception as e:
       print(f"An error occurred: {e}")
       import traceback
       traceback.print_exc()
