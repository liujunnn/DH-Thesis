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

class ReportGenerator:
    """
    Report Generator Class
    Handles the generation of detailed analysis reports for porcelain/ceramic collection data
    """
    
    def __init__(self):
        """Initialize the report generator with empty data"""
        self.data = None
        self.stats_cache = {}  # Cache for calculated statistics
    
    def generate_analysis_report(self, data_file: str):
        """
        Generate a detailed data analysis report
        
        Args:
            data_file (str): Path to the JSON file containing porcelain data
            
        Creates:
            - Text analysis report with comprehensive statistics
            - CSV summary file with key metrics
        """
        try:
            # Load the JSON data file
            with open(data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            
            # Create output filename by replacing .json extension
            report_file = data_file.replace('.json', '_analysis_report.txt')
            
            # Calculate all statistics once
            self._calculate_all_statistics()
            
            # Write the comprehensive analysis report
            with open(report_file, 'w', encoding='utf-8') as f:
                # Write report header
                f.write("Porcelain Data Comprehensive Analysis Report\n")
                f.write("=" * 100 + "\n")
                f.write(f"Generation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Records: {len(self.data)}\n")
                f.write("=" * 100 + "\n\n")
                
                # Write each analysis section
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
                
                # Write report footer
                f.write("\n" + "=" * 100 + "\n")
                f.write(f"Report Generation Complete - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            print(f"📄 Detailed analysis report generated: {report_file}")
            
            # Generate CSV summary for easier data manipulation
            self.generate_summary_csv(report_file.replace('.txt', '_summary.csv'))
            
        except Exception as e:
            print(f"Report generation failed: {e}")
            import traceback
            traceback.print_exc()
    
    def _calculate_all_statistics(self):
        """Calculate all statistics once and cache them"""
        self.stats_cache = {
            'quality_scores': [],
            'decorations': {},
            'shapes': {},
            'functions': {},
            'glazes': {},
            'materials': {},
            'production_places': {},
            'colors': {},
            'inscriptions': {},
            'periods': {},
            'institutions': {},
            'field_coverage': {}
        }
        
        # Process each item once
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                desc = item['DescriptiveMetadata']
                
                # Quality scores
                score = desc.get('quality_score', 0)
                self.stats_cache['quality_scores'].append(score)
                
                # Collect all field data
                self._collect_field_data(desc, 'Decorations', 'decorations')
                self._collect_field_data(desc, 'Shape', 'shapes')
                self._collect_field_data(desc, 'Function', 'functions')
                self._collect_field_data(desc, 'Glaze', 'glazes')
                self._collect_field_data(desc, 'Paste', 'materials')
                self._collect_field_data(desc, 'ProductionPlace', 'production_places')
                self._collect_field_data(desc, 'ColoredDrawing', 'colors')
                self._collect_field_data(desc, 'Inscriptions', 'inscriptions')
            
            if 'Metadata_for_Management' in item:
                mgmt = item['Metadata_for_Management']
                
                # Periods
                periods = mgmt.get('Period', [])
                if isinstance(periods, list):
                    for period in periods:
                        self.stats_cache['periods'][period] = self.stats_cache['periods'].get(period, 0) + 1
                elif periods:
                    self.stats_cache['periods'][periods] = self.stats_cache['periods'].get(periods, 0) + 1
                
                # Institutions
                institution = mgmt.get('ProvidingInstitution', '')
                if institution:
                    self.stats_cache['institutions'][institution] = self.stats_cache['institutions'].get(institution, 0) + 1
    
    def _collect_field_data(self, desc: dict, field_name: str, cache_key: str):
        """Helper method to collect field data into cache"""
        values = desc.get(field_name, [])
        if isinstance(values, list):
            for value in values:
                if value:
                    self.stats_cache[cache_key][value] = self.stats_cache[cache_key].get(value, 0) + 1
    
    def _write_section_header(self, f, title: str):
        """Write a standardized section header"""
        f.write(f"\n【{title}】\n")
        f.write("-" * 80 + "\n")
    
    def _write_bar_chart(self, f, data: dict, max_items: int = 20, bar_scale: int = 2):
        """Write a text-based bar chart"""
        sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)[:max_items]
        for item, count in sorted_items:
            percentage = count/len(self.data)*100
            bar = '█' * int(percentage/bar_scale)
            f.write(f"  {item:20} {bar:25} {count:5d} ({percentage:5.1f}%)\n")
    
    def _write_quality_overview(self, f):
        """Write data quality overview section"""
        self._write_section_header(f, "Data Quality Overview")
        
        quality_scores = self.stats_cache['quality_scores']
        if not quality_scores:
            f.write("No quality scores available.\n")
            return
        
        # Quality distribution
        quality_distribution = {
            'Excellent (>0.8)': sum(1 for s in quality_scores if s > 0.8),
            'Good (0.6-0.8)': sum(1 for s in quality_scores if 0.6 < s <= 0.8),
            'Medium (0.4-0.6)': sum(1 for s in quality_scores if 0.4 < s <= 0.6),
            'Poor (0.2-0.4)': sum(1 for s in quality_scores if 0.2 < s <= 0.4),
            'Very Poor (<0.2)': sum(1 for s in quality_scores if s <= 0.2)
        }
        
        f.write(f"Average Quality Score: {sum(quality_scores)/len(quality_scores):.3f}\n")
        f.write(f"Maximum Quality Score: {max(quality_scores):.3f}\n")
        f.write(f"Minimum Quality Score: {min(quality_scores):.3f}\n\n")
        
        f.write("Quality Distribution:\n")
        self._write_bar_chart(f, quality_distribution)
    
    def _write_lda_analysis(self, f):
        """Write LDA topic analysis"""
        self._write_section_header(f, "LDA Topic Analysis")
        
        topic_counter = {}
        items_with_topics = 0
        
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                lda_topics = item['DescriptiveMetadata'].get('lda_topics', [])
                if lda_topics:
                    items_with_topics += 1
                    for topic in lda_topics:
                        topic_id = topic.get('topic_id', -1)
                        topic_name = f"Topic{topic_id + 1}"
                        topic_counter[topic_name] = topic_counter.get(topic_name, 0) + 1
        
        f.write(f"Records with LDA topics: {items_with_topics} ({items_with_topics/len(self.data)*100:.2f}%)\n\n")
        
        if topic_counter:
            f.write("Topic Distribution:\n")
            for topic, count in sorted(topic_counter.items(), key=lambda x: x[1], reverse=True):
                f.write(f"  - {topic}: {count}\n")
    
    def _write_decoration_analysis(self, f):
        """Write decoration type distribution analysis"""
        self._write_section_header(f, "Decoration Type Distribution")
        
        # Group decorations by theme
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
        
        for dec, count in self.stats_cache['decorations'].items():
            if ':' in dec:
                theme, detail = dec.split(':', 1)
                if theme in decoration_themes:
                    decoration_themes[theme].append((detail, count))
                else:
                    decoration_themes['other'].append((dec, count))
            else:
                decoration_themes['other'].append((dec, count))
        
        # Print statistics for each theme
        for theme, details in decoration_themes.items():
            if details:
                total_count = sum(count for _, count in details)
                f.write(f"\n{theme.upper()} Theme (Total: {total_count} items):\n")
                sorted_details = sorted(details, key=lambda x: x[1], reverse=True)[:10]
                for detail, count in sorted_details:
                    f.write(f"  - {detail}: {count}\n")
    
    def _write_shape_analysis(self, f):
        """Write vessel shape distribution analysis"""
        self._write_section_header(f, "Vessel Shape Distribution")
        
        # Separate main shapes from specific descriptions
        main_shapes = ['bowl', 'vase', 'jar', 'plate', 'cup', 'pot', 'bottle', 'box', 'censer', 'ewer']
        shape_main = {}
        shape_specific = {}
        
        for shape, count in self.stats_cache['shapes'].items():
            if shape in main_shapes:
                shape_main[shape] = count
            else:
                shape_specific[shape] = count
        
        f.write("Main Shape Categories:\n")
        self._write_bar_chart(f, shape_main)
        
        if shape_specific:
            f.write("\nSpecific Shape Descriptions (Top 20):\n")
            for shape, count in sorted(shape_specific.items(), key=lambda x: x[1], reverse=True)[:20]:
                f.write(f"  - {shape}: {count}\n")
    
    def _write_function_analysis(self, f):
        """Write functional purpose distribution analysis"""
        self._write_section_header(f, "Functional Distribution")
        
        functions = self.stats_cache['functions']
        multi_function_count = sum(1 for item in self.data 
                                  if len(item.get('DescriptiveMetadata', {}).get('Function', [])) > 1)
        
        if functions:
            f.write(f"Multi-function items: {multi_function_count} ({multi_function_count/len(self.data)*100:.1f}%)\n\n")
            f.write("Function Category Distribution:\n")
            self._write_bar_chart(f, functions)
    
    def _write_glaze_analysis(self, f):
        """Write glaze technology distribution analysis"""
        self._write_section_header(f, "Glaze Technology Distribution")
        
        glazes = self.stats_cache['glazes']
        multi_glaze_count = sum(1 for item in self.data 
                               if len(item.get('DescriptiveMetadata', {}).get('Glaze', [])) > 1)
        
        if glazes:
            f.write(f"Multi-glaze items: {multi_glaze_count} ({multi_glaze_count/len(self.data)*100:.1f}%)\n\n")
            for glaze, count in sorted(glazes.items(), key=lambda x: x[1], reverse=True)[:20]:
                percentage = count/len(self.data)*100
                f.write(f"  - {glaze}: {count} ({percentage:.1f}%)\n")
    
    def _write_material_analysis(self, f):
        """Write material composition distribution analysis"""
        self._write_section_header(f, "Material Distribution")
        
        materials = self.stats_cache['materials']
        if materials:
            self._write_bar_chart(f, materials, bar_scale=1)
    
    def _write_production_analysis(self, f):
        """Write production location distribution analysis - simplified version"""
        self._write_section_header(f, "Production Location Distribution")
        
        # Define production location hierarchy
        place_hierarchy = {
            'china': 'China',
            'jingdezhen': 'China',
            'longquan': 'China',
            'dehua': 'China',
            'yixing': 'China',
            'netherlands': 'Netherlands',
            'delft': 'Netherlands',
            'belgium': 'Belgium',
            'brussels': 'Belgium',
            'germany': 'Germany',
            'meissen': 'Germany',
            'france': 'France',
            'sevres': 'France',
            'england': 'England',
            'worcester': 'England'
        }
        
        # Count by country
        country_counts = {}
        specific_places = {}
        
        for place, count in self.stats_cache['production_places'].items():
            place_lower = place.lower()
            country = place_hierarchy.get(place_lower, 'Unknown')
            country_counts[country] = country_counts.get(country, 0) + count
            specific_places[place] = count
        
        # Write country statistics
        f.write("【Statistics by Country】\n")
        for country, count in sorted(country_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = count / len(self.data) * 100
            f.write(f"  {country:20} {count:5d} ({percentage:5.1f}%)\n")
        
        # China vs Europe comparison
        china_count = country_counts.get('China', 0)
        european_count = sum(count for country, count in country_counts.items() 
                           if country in ['Netherlands', 'Belgium', 'Germany', 'France', 'England'])
        
        f.write("\n【China vs European Porcelain Comparison】\n")
        f.write(f"  Chinese Porcelain: {china_count} ({china_count/len(self.data)*100:.1f}%)\n")
        f.write(f"  European Porcelain: {european_count} ({european_count/len(self.data)*100:.1f}%)\n")
        
        # Specific production sites
        f.write("\n【Specific Production Site Distribution (Top 20)】\n")
        for place, count in sorted(specific_places.items(), key=lambda x: x[1], reverse=True)[:20]:
            percentage = count / len(self.data) * 100
            f.write(f"  {place:30} {count:4d} ({percentage:5.1f}%)\n")
    
    def _write_period_analysis(self, f):
        """Write historical period distribution analysis"""
        self._write_section_header(f, "Period Distribution")
        
        periods = self.stats_cache['periods']
        total_with_period = sum(periods.values()) if periods else 0
        
        f.write(f"Records with period info: {total_with_period} ({total_with_period/len(self.data)*100:.1f}%)\n")
        f.write(f"Records without period info: {len(self.data) - total_with_period} ({(len(self.data) - total_with_period)/len(self.data)*100:.1f}%)\n\n")
        
        if periods:
            # Define chronological order for Chinese dynasties
            dynasty_order = ['Tang', 'Song', 'Yuan', 'Ming', 'Qing', 'Republic', 'Modern']
            
            f.write("Dynasty Distribution:\n")
            for dynasty in dynasty_order:
                if dynasty in periods:
                    count = periods[dynasty]
                    percentage = count/len(self.data)*100
                    bar = '█' * int(percentage/2)
                    f.write(f"  {dynasty:10} {bar:40} {count:4d} ({percentage:5.1f}%)\n")
            
            # Other periods not in the standard order
            other_periods = {k: v for k, v in periods.items() if k not in dynasty_order}
            if other_periods:
                f.write("\nOther Periods:\n")
                for period, count in sorted(other_periods.items(), key=lambda x: x[1], reverse=True)[:10]:
                    f.write(f"  - {period}: {count}\n")
    
    def _write_institution_analysis(self, f):
        """Write contributing institution distribution analysis"""
        self._write_section_header(f, "Contributing Institution Distribution")
        
        institutions = self.stats_cache['institutions']
        
        if institutions:
            f.write(f"Total Different Institutions: {len(institutions)}\n\n")
            f.write("All Institutions (Top 20):\n")
            for institution, count in sorted(institutions.items(), key=lambda x: x[1], reverse=True)[:20]:
                f.write(f"  - {institution}: {count} ({count/len(self.data)*100:.2f}%)\n")
    
    def _write_color_analysis(self, f):
        """Write color distribution analysis"""
        self._write_section_header(f, "Color Distribution")
        
        colors = self.stats_cache['colors']
        
        if colors:
            f.write("Single Color Statistics:\n")
            self._write_bar_chart(f, colors)
    
    def _write_inscription_analysis(self, f):
        """Write inscription and mark information distribution"""
        self._write_section_header(f, "Inscription Information Distribution")
        
        inscriptions = self.stats_cache['inscriptions']
        has_inscription_count = sum(1 for item in self.data 
                                  if item.get('DescriptiveMetadata', {}).get('Inscriptions'))
        
        f.write(f"Records with inscriptions: {has_inscription_count} ({has_inscription_count/len(self.data)*100:.2f}%)\n")
        f.write(f"Records without inscriptions: {len(self.data) - has_inscription_count} ({(len(self.data) - has_inscription_count)/len(self.data)*100:.2f}%)\n\n")
        
        if inscriptions:
            # Group by inscription type
            inscription_types = {}
            for inscription, count in inscriptions.items():
                if ':' in inscription:
                    ins_type, detail = inscription.split(':', 1)
                    if ins_type not in inscription_types:
                        inscription_types[ins_type] = []
                    inscription_types[ins_type].append((detail, count))
                else:
                    if 'other' not in inscription_types:
                        inscription_types['other'] = []
                    inscription_types['other'].append((inscription, count))
            
            for ins_type, details in inscription_types.items():
                if details:
                    total = sum(c for _, c in details)
                    f.write(f"\n{ins_type.upper()} (Total: {total} items):\n")
                    sorted_details = sorted(details, key=lambda x: x[1], reverse=True)[:5]
                    for detail, count in sorted_details:
                        f.write(f"  - {detail}: {count}\n")
    
    def _write_completeness_analysis(self, f):
        """Write data completeness analysis"""
        self._write_section_header(f, "Data Completeness Analysis")
        
        # Calculate field coverage
        field_coverage = {
            'Description Info': sum(1 for item in self.data if item.get('DescriptiveMetadata', {}).get('Descriptions')),
            'Decoration Info': len([1 for _ in self.stats_cache['decorations']]),
            'Shape Info': len([1 for _ in self.stats_cache['shapes']]),
            'Function Info': len([1 for _ in self.stats_cache['functions']]),
            'Glaze Info': len([1 for _ in self.stats_cache['glazes']]),
            'Material Info': len([1 for _ in self.stats_cache['materials']]),
            'Production Info': len([1 for _ in self.stats_cache['production_places']]),
            'Color Info': len([1 for _ in self.stats_cache['colors']]),
            'Inscription Info': len([1 for _ in self.stats_cache['inscriptions']])
        }
        
        f.write("Field Coverage Rates:\n")
        for field, count in sorted(field_coverage.items(), key=lambda x: x[1], reverse=True):
            percentage = count/len(self.data)*100
            bar = '█' * int(percentage/5)
            f.write(f"  {field:20} {bar:20} {count:5d}/{len(self.data)} ({percentage:5.1f}%)\n")
    
    def _write_combination_analysis(self, f):
        """Write combination analysis"""
        self._write_section_header(f, "Combination Analysis")
        
        # Shape-Function combinations
        shape_function_combinations = {}
        main_shapes = ['bowl', 'vase', 'jar', 'plate', 'cup', 'pot', 'bottle', 'box', 'censer', 'ewer']
        
        for item in self.data:
            if 'DescriptiveMetadata' in item:
                shapes = item['DescriptiveMetadata'].get('Shape', [])
                functions = item['DescriptiveMetadata'].get('Function', [])
                
                # Get first main shape and first function
                main_shape = next((s for s in shapes if s in main_shapes), None)
                first_function = functions[0] if functions else None
                
                if main_shape and first_function:
                    combo = f"{main_shape} - {first_function}"
                    shape_function_combinations[combo] = shape_function_combinations.get(combo, 0) + 1
        
        if shape_function_combinations:
            f.write("Shape-Function Combinations (Top 20):\n")
            for combo, count in sorted(shape_function_combinations.items(), key=lambda x: x[1], reverse=True)[:20]:
                f.write(f"  - {combo}: {count}\n")
    
    def _write_summary(self, f):
        """Write comprehensive statistical summary"""
        self._write_section_header(f, "Comprehensive Statistical Summary")
        
        quality_scores = self.stats_cache['quality_scores']
        
        # Calculate average field fill rate
        field_counts = [
            len([1 for _ in self.stats_cache['decorations']]),
            len([1 for _ in self.stats_cache['shapes']]),
            len([1 for _ in self.stats_cache['functions']]),
            len([1 for _ in self.stats_cache['glazes']]),
            len([1 for _ in self.stats_cache['materials']]),
            len([1 for _ in self.stats_cache['production_places']]),
            len([1 for _ in self.stats_cache['colors']]),
            len([1 for _ in self.stats_cache['inscriptions']])
        ]
        avg_fields_per_item = sum(field_counts) / (len(self.data) * 8) if self.data else 0
        
        f.write(f"📊 Key Metrics:\n")
        f.write(f"  - Total Records: {len(self.data)}\n")
        f.write(f"  - Average Field Fill Rate: {avg_fields_per_item*100:.1f}%\n")
        
        if quality_scores:
            f.write(f"  - Average Quality Score: {sum(quality_scores)/len(quality_scores):.3f}\n")
            high_quality = sum(1 for s in quality_scores if s > 0.5)
            excellent = sum(1 for s in quality_scores if s > 0.8)
            f.write(f"  - High Quality Records (>0.5): {high_quality} ({high_quality/len(self.data)*100:.1f}%)\n")
            f.write(f"  - Excellent Records (>0.8): {excellent} ({excellent/len(self.data)*100:.1f}%)\n")
        
        f.write(f"\n💡 Data Quality Recommendations:\n")
        if avg_fields_per_item < 0.5:
            f.write(f"  - Low average field fill rate ({avg_fields_per_item*100:.1f}%), consider adding more descriptive information\n")
        
        # Check specific field coverage
        for field_name, cache_key in [('Function', 'functions'), ('Glaze', 'glazes')]:
            field_coverage = len([1 for _ in self.stats_cache[cache_key]]) / len(self.data)
            if field_coverage < 0.3:
                f.write(f"  - {field_name} info coverage only {field_coverage*100:.1f}%, consider adding {field_name.lower()} descriptions\n")
    
    def generate_summary_csv(self, output_file: str):
        """Generate CSV format statistical summary"""
        try:
            summary_data = []
            
            # Add quality score summary
            if self.stats_cache['quality_scores']:
                scores = self.stats_cache['quality_scores']
                summary_data.append({
                    'Category': 'QualityScore',
                    'Value': 'Average',
                    'Count': len(scores),
                    'Percentage': f"{sum(scores)/len(scores):.3f}"
                })
                summary_data.append({
                    'Category': 'QualityScore',
                    'Value': 'High Quality (>0.5)',
                    'Count': sum(1 for s in scores if s > 0.5),
                    'Percentage': f"{sum(1 for s in scores if s > 0.5)/len(scores)*100:.2f}%"
                })
            
            # Add all other categories
            for category, data in self.stats_cache.items():
                if category != 'quality_scores' and isinstance(data, dict):
                    for value, count in data.items():
                        summary_data.append({
                            'Category': category.replace('_', ' ').title(),
                            'Value': str(value)[:100],
                            'Count': count,
                            'Percentage': f"{count/len(self.data)*100:.2f}%"
                        })
            
            # Save to CSV
            df = pd.DataFrame(summary_data)
            df.sort_values(['Category', 'Count'], ascending=[True, False], inplace=True)
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"📊 Statistical summary CSV generated: {output_file}")
            
        except Exception as e:
            print(f"Failed to generate CSV summary: {e}")


# Main execution example
if __name__ == "__main__":
    """
    Example usage of the ReportGenerator class
    Run this script directly to generate a report from a JSON file
    """
    # Initialize the report generator
    generator = ReportGenerator()
    
    # Example: Generate report from a JSON file
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
