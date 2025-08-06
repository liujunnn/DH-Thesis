#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from typing import Dict, List, Any, Union, Tuple  # Import Tuple for type hints
from datetime import datetime
import json

class DataMapper:
    """Data mapper for extracting and mapping metadata from cultural heritage items"""
    
    def __init__(self, keyword_dict):
        """
        Initialize the DataMapper with a keyword dictionary
        
        Args:
            keyword_dict: Dictionary containing keyword mappings for various attributes
        """
        self.keyword_dict = keyword_dict
    
    def _flatten_list(self, lst: Union[List, Any]) -> List[str]:
        """
        Recursively flatten nested lists into a single-level list of strings
        
        Args:
            lst: Input list or value to flatten
            
        Returns:
            List of strings with all nested elements flattened
        """
        result = []
        if isinstance(lst, list):
            for item in lst:
                if isinstance(item, list):
                    # Recursively flatten nested lists
                    result.extend(self._flatten_list(item))
                elif item is not None:
                    result.append(str(item))
        elif lst is not None:
            result.append(str(lst))
        return result
    
    def extract_colored_drawing(self, text: str) -> List[str]:
        """
        Extract color information from text using keyword matching
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of unique color names found in the text
        """
        if not text:
            return []
            
        text_lower = text.lower()
        colors_found = []
        
        # Search for color keywords in the text
        for color_name, keywords in self.keyword_dict.color_keywords.items():
            for keyword in keywords:
                # Use word boundaries to ensure exact matches
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    colors_found.append(color_name)
                    break
        
        # Return unique color names
        return list(set(colors_found))
    
    def extract_decorations(self, text: str) -> List[str]:
        """
        Extract decoration information including themes, patterns, and motifs
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of decoration descriptions (limited to 15 items)
        """
        if not text:
            return []
            
        text_lower = text.lower()
        decorations = []
        
        # Extract decoration themes from keyword dictionary
        for theme, keywords in self.keyword_dict.decoration_themes.items():
            theme_decorations = []
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    theme_decorations.append(keyword)
            
            # Limit to 3 keywords per theme to avoid redundancy
            for keyword in theme_decorations[:3]:
                decorations.append(f"{theme}:{keyword}")
        
        # Include colors as part of decoration metadata
        colors = self.extract_colored_drawing(text)
        decorations.extend([f"color:{c}" for c in colors])
        
        # Use regex patterns to extract specific decoration descriptions
        decoration_patterns = [
            (r'decorated with ([\w\s,]+?)(?:\.|,|;|and)', 'decorated'),
            (r'depicting ([\w\s,]+?)(?:\.|,|;|and)', 'depicting'),
            (r'painted with ([\w\s,]+?)(?:\.|,|;|and)', 'painted'),
            (r'design of ([\w\s,]+?)(?:\.|,|;|and)', 'design'),
            (r'motif of ([\w\s,]+?)(?:\.|,|;|and)', 'motif'),
            (r'pattern of ([\w\s,]+?)(?:\.|,|;|and)', 'pattern')
        ]
        
        # Extract decoration patterns from text
        for pattern, prefix in decoration_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches[:2]:  # Limit to 2 matches per pattern
                if len(match) < 50:  # Filter out overly long descriptions
                    decorations.append(f"{prefix}:{match.strip()}")
        
        # Remove duplicates while preserving order
        unique_decorations = []
        seen = set()
        for dec in decorations:
            dec_lower = dec.lower()
            if dec_lower not in seen:
                unique_decorations.append(dec)
                seen.add(dec_lower)
        
        # Return up to 15 unique decorations
        return unique_decorations[:15]
    
    def extract_shape(self, text: str) -> List[str]:
        """
        Extract shape information from text
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of shape descriptions (limited to 5 items)
        """
        if not text:
            return []
            
        text_lower = text.lower()
        shapes_found = []
        shape_details = []
        
        # Match shape keywords from dictionary
        for shape_type, keywords in self.keyword_dict.shape_keywords.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    shapes_found.append(shape_type)
                    # Capture specific shape details if different from main type
                    if keyword != shape_type:
                        shape_details.append(keyword)
        
        # Combine and deduplicate results
        result = list(set(shapes_found))
        result.extend([d for d in set(shape_details) if d not in result])
        
        # Return up to 5 shape descriptors
        return result[:5]
    
    def extract_function(self, text: str) -> List[str]:
        """
        Extract functional information about the item
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of unique function types
        """
        if not text:
            return []
            
        text_lower = text.lower()
        functions_found = []
        
        # Match function keywords from dictionary
        for function_type, keywords in self.keyword_dict.function_keywords.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    functions_found.append(function_type)
                    break  # Only need one match per function type
        
        return list(set(functions_found))
    
    def extract_material(self, text: str) -> List[str]:
        """
        Extract material composition information
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of unique material types
        """
        if not text:
            return []
            
        text_lower = text.lower()
        materials_found = []
        
        # Match material keywords from dictionary
        for material_type, keywords in self.keyword_dict.material_keywords.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    materials_found.append(material_type)
        
        # Apply default material inference if no explicit materials found
        if not materials_found:
            if any(word in text_lower for word in ['ceramic', 'pottery', 'clay']):
                materials_found.append('ceramic')
            elif any(word in text_lower for word in ['porcelain', 'china']):
                materials_found.append('porcelain')
        
        return list(set(materials_found))
    
    def extract_glaze(self, text: str) -> List[str]:
        """
        Extract glaze type and color information
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of glaze types (limited to 5 items)
        """
        if not text:
            return []
            
        text_lower = text.lower()
        glazes_found = []
        
        # Match glaze keywords from dictionary
        for glaze_type, keywords in self.keyword_dict.glaze_keywords.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    # Normalize underscores to spaces in glaze type names
                    normalized_type = glaze_type.replace('_', ' ')
                    glazes_found.append(normalized_type)
                    # Include specific keyword if different from normalized type
                    if keyword != glaze_type and keyword != normalized_type:
                        glazes_found.append(keyword)
        
        # Return up to 5 unique glaze types
        return list(set(glazes_found))[:5]
    
    def extract_production_place(self, item: Dict[str, Any], text: str) -> List[str]:
        """
        Extract production place information from item metadata and text
        
        Args:
            item: Dictionary containing item metadata
            text: Description text to analyze
            
        Returns:
            List of production places (limited to 10 items)
        """
        places = []
        normalized_places = set()
        
        # 1. Extract from dedicated place fields in metadata
        place_fields = ['edmPlaceLabel', 'placeLabel', 'place', 'origin', 'provenance', 'production']
        for field in place_fields:
            if field in item:
                place_data = item[field]
                if isinstance(place_data, list):
                    for p in self._flatten_list(place_data):
                        if p and isinstance(p, str):
                            # Handle dictionary format like {'def': 'place_name'}
                            if p.startswith('{') and 'def' in p:
                                try:
                                    p_dict = json.loads(p.replace("'", '"'))
                                    if 'def' in p_dict:
                                        p = p_dict['def']
                                except:
                                    pass
                            
                            # Normalize place names using keyword dictionary
                            normalized = self.keyword_dict.normalize_place(p)
                            if normalized and len(normalized) < 50:
                                normalized_places.add(normalized)
                                
                elif isinstance(place_data, str) and place_data:
                    normalized = self.keyword_dict.normalize_place(place_data)
                    if normalized and len(normalized) < 50:
                        normalized_places.add(normalized)
                        
                elif isinstance(place_data, dict) and 'def' in place_data:
                    # Handle direct dictionary format
                    p = place_data['def']
                    normalized = self.keyword_dict.normalize_place(p)
                    if normalized and len(normalized) < 50:
                        normalized_places.add(normalized)
        
        # 2. Extract production place from text content
        if text:
            text_lower = text.lower()
            
            # Check production place keywords
            for place_type, keywords in self.keyword_dict.production_keywords.items():
                for keyword in keywords:
                    if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                        normalized_places.add(place_type)
                        break
            
            # Special pattern recognition for Delftware
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
                    # Avoid double counting by not automatically adding netherlands
                    break
            
            # Belgian pottery patterns
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
        
        # 3. Clean up results
        # Remove potential museum locations (not production places)
        museum_locations = ['vienna', 'stockholm', 'london', 'paris', 'new york']
        normalized_places = {p for p in normalized_places if p not in museum_locations}
        
        # Merge Brussels variants to Belgium
        if 'brussels' in normalized_places:
            normalized_places.add('belgium')
            normalized_places.remove('brussels')
        
        # 4. Priority-based sorting
        final_places = []
        
        # Define priority order for production places
        priority_order = [
            'jingdezhen', 'delft', 'longquan', 'dehua', 'yixing', 'jun', 'ding', 'cizhou',
            'amsterdam', 'rotterdam', 'haarlem', 'makkum',
            'antwerp', 'tournai', 'ghent',
            'china', 'netherlands', 'belgium',
            'meissen', 'sevres', 'worcester',
            'export'
        ]
        
        # Add high-priority places first
        for place in priority_order:
            if place in normalized_places:
                final_places.append(place)
                normalized_places.remove(place)
        
        # Add remaining places in alphabetical order
        final_places.extend(sorted(normalized_places))
        
        # Return up to 10 production places
        return final_places[:10]
    
    def extract_period_info(self, item: Dict[str, Any]) -> Tuple[List[str], List[int], Dict[str, Any]]:
        """
        Extract period, dynasty, and dating information from item metadata
        
        Args:
            item: Dictionary containing item metadata
            
        Returns:
            Tuple containing:
                - List of period/dynasty names
                - List of years
                - Dictionary with comprehensive period information
        """
        periods = []
        years = []
        dynasty_info = {}
        
        # 1. Extract from Period field
        period_data = item.get('Metadata_for_Management', {}).get('Period', '')
        if not period_data and 'edmTimespanLabel' in item:
            period_data = item['edmTimespanLabel']
        
        # Process period data into strings
        period_strings = []
        if isinstance(period_data, list):
            for p in period_data:
                if isinstance(p, str) and p.strip():
                    # Filter out URLs and other non-period information
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
        
        # 2. Parse period strings for years and dynasties
        for period_str in period_strings:
            # Extract 4-digit years
            year_matches = re.findall(r'\b(1[0-9]{3}|20[0-2][0-9])\b', period_str)
            for year_str in year_matches:
                year = int(year_str)
                if 1000 <= year <= 2025:
                    years.append(year)
            
            # Extract centuries and convert to years (using mid-century as representative)
            century_patterns = [
                (r'\b(\d{1,2})(?:st|nd|rd|th)\s+century\b', 'en'),  # English
                (r'\b(\d{1,2})[èe]me\s+siècle\b', 'fr'),           # French
                (r'\b(\d{1,2})\.\s+Jahrhundert\b', 'de'),          # German
                (r'\b(\d{1,2})[º°]\s+século\b', 'pt'),             # Portuguese
                (r'\b(\d{1,2})\s+век\b', 'ru'),                    # Russian
                (r'\b(\d{1,2})-luku\b', 'fi'),                     # Finnish
                (r'\b(\d{1,2})\.\s+gadsimts\b', 'lv'),            # Latvian
                (r'\b(\d{1,2})\s+amžius\b', 'lt'),                # Lithuanian
            ]
            
            for pattern, lang in century_patterns:
                matches = re.findall(pattern, period_str, re.IGNORECASE)
                for match in matches:
                    century = int(match)
                    if 1 <= century <= 21:
                        # Use mid-century year as representative
                        year = (century - 1) * 100 + 50
                        years.append(year)
                        periods.append(f"{century}th century")
            
            # Extract dynasty information
            period_lower = period_str.lower()
            for dynasty, keywords in self.keyword_dict.period_keywords.items():
                for keyword in keywords:
                    if keyword in period_lower:
                        periods.append(dynasty.capitalize())
                        break
        
        # 3. Infer dynasty from years
        for year in years:
            dynasty = self.keyword_dict.get_dynasty_from_year(year)
            if dynasty != 'Unknown':
                dynasty_info[year] = dynasty
                if dynasty not in periods:
                    periods.append(dynasty)
        
        # 4. Clean and deduplicate results
        # Remove duplicate and invalid years
        unique_years = []
        for year in years:
            if 1000 <= year <= 2025 and year not in unique_years:
                unique_years.append(year)
        
        # Remove duplicate periods
        unique_periods = []
        seen = set()
        for period in periods:
            if period and period not in seen and len(period) < 50:
                unique_periods.append(period)
                seen.add(period.lower())
        
        # 5. Generate comprehensive period summary
        period_summary = {
            'periods': unique_periods[:5],
            'years': sorted(unique_years)[:10],
            'dynasty_mapping': dynasty_info,
            'century': self.keyword_dict.get_century_from_year(unique_years[0]) if unique_years else None,
            'date_range': f"{min(unique_years)}-{max(unique_years)}" if len(unique_years) > 1 else str(unique_years[0]) if unique_years else None
        }
        
        return unique_periods, unique_years, period_summary
    
    def extract_inscriptions(self, text: str) -> List[str]:
        """
        Extract inscription and mark information from text
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of inscription descriptions (limited to 5 items)
        """
        if not text:
            return []
            
        text_lower = text.lower()
        inscriptions = []
        
        # Keywords related to inscriptions and marks
        inscription_keywords = [
            'mark', 'marked', 'inscription', 'inscribed', 'character',
            'seal', 'signature', 'signed', 'reign mark', 'nianzhi',
            'nianzhao', 'tang', 'zhi', 'zao', 'six character', 
            'four character', 'seal mark', 'reign title', 'base mark'
        ]
        
        # Find relevant keywords in text
        found_keywords = []
        for keyword in inscription_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        # Add up to 3 found keywords
        inscriptions.extend(found_keywords[:3])
        
        # Extract specific inscription content using patterns
        inscription_patterns = [
            (r'mark(?:ed)?\s+(?:of|with|reading)\s+([\w\s]+?)(?:\.|,|;)', 'mark'),
            (r'inscription\s+(?:of|reading)\s+([\w\s]+?)(?:\.|,|;)', 'inscription'),
            (r'(?:six|four|two)\s+character\s+mark\s+(?:of|reading)?\s*([\w\s]+?)(?:\.|,|;)', 'character mark'),
            (r'reign\s+mark\s+of\s+([\w\s]+?)(?:\.|,|;)', 'reign mark'),
            (r'signed\s+([\w\s]+?)(?:\.|,|;)', 'signature')
        ]
        
        # Extract inscription patterns from text
        for pattern, prefix in inscription_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches[:2]:  # Limit to 2 matches per pattern
                if len(match) < 30:  # Filter out overly long descriptions
                    inscriptions.append(f"{prefix}:{match.strip()}")
        
        # Check for dynasty-related marks
        for period, keywords in self.keyword_dict.period_keywords.items():
            for keyword in keywords:
                if keyword in text_lower and 'mark' in text_lower:
                    inscriptions.append(f"period mark:{period}")
                    break
        
        # Return up to 5 unique inscriptions
        return list(set(inscriptions))[:5]
    
    def map_to_descriptive_metadata(self, item: Dict[str, Any], text: str, 
                                  lda_topics: List[Dict] = None) -> Dict[str, Any]:
        """
        Map item data to descriptive metadata structure
        
        Args:
            item: Dictionary containing item metadata
            text: Combined text for analysis
            lda_topics: Optional LDA topic analysis results
            
        Returns:
            Dictionary with descriptive metadata
        """
        # Safely extract descriptions
        descriptions = []
        if 'dcDescription' in item:
            desc_data = item['dcDescription']
            descriptions = self._flatten_list(desc_data)
        
        # Build descriptive metadata structure
        descriptive_metadata = {
            'Descriptions': descriptions[:3],  # Limit to 3 descriptions
            'ColoredDrawing': self.extract_colored_drawing(text),
            'Decorations': self.extract_decorations(text),
            'Shape': self.extract_shape(text),
            'ShapeDescription': [],  # Additional shape details can be added here
            'Function': self.extract_function(text),
            'FunctionCategory': [],  # Higher-level function categories can be added
            'Paste': self.extract_material(text),
            'PasteMaterial': self.extract_material(text),  # Same as Paste for now
            'Glaze': self.extract_glaze(text),
            'ProductionPlace': self.extract_production_place(item, text),
            'ProductionPlaceLocation': self.extract_production_place(item, text),  # Same as ProductionPlace
            'Inscriptions': self.extract_inscriptions(text)
        }
        
        # Add LDA topic information if available
        if lda_topics:
            descriptive_metadata['lda_topics'] = lda_topics
        
        # Calculate extraction quality metrics
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
        
        # Add quality metrics to metadata
        descriptive_metadata['extraction_quality'] = extraction_quality
        descriptive_metadata['quality_score'] = sum(extraction_quality.values()) / len(extraction_quality)
        
        return descriptive_metadata
    
    def map_to_management_metadata(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map item data to management metadata structure
        
        Args:
            item: Dictionary containing item metadata
            
        Returns:
            Dictionary with management metadata
        """
        # Safely extract title information
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
        
        # Extract comprehensive period information
        periods, years, period_summary = self.extract_period_info(item)
        
        # Build management metadata structure
        management_metadata = {
            'Title': title_value,
            'Used_Titles': [],  # Alternative titles
            'Identifier': item.get('id', ''),
            'Period': periods,  # Cleaned period list
            'Years': years,  # Extracted years
            'PeriodSummary': period_summary,  # Comprehensive period information
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
        
        # Process title variants
        all_titles = []
        
        if 'dcTitle' in item:
            dc_titles = self._flatten_list(item['dcTitle'])
            all_titles.extend(dc_titles)
        
        if 'title' in item:
            titles = self._flatten_list(item['title'])
            all_titles.extend(titles)
        
        # Deduplicate titles
        unique_titles = []
        seen = set()
        for title in all_titles:
            if isinstance(title, str) and title and title not in seen:
                unique_titles.append(title)
                seen.add(title)
        
        management_metadata['Used_Titles'] = unique_titles
        
        return management_metadata
    
    def map_to_extended_metadata(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map item data to extended metadata structure
        
        Args:
            item: Dictionary containing item metadata
            
        Returns:
            Dictionary with extended metadata
        """
        # Build extended metadata structure
        extended_metadata = {
            'RelatedPeople': [],  # Creators, contributors, etc.
            'RelatedCollections': [],  # Collection names
            'Digitalization': {
                'edmIsShownAt': item.get('edmIsShownAt', ''),  # Web page URL
                'edmIsShownBy': item.get('edmIsShownBy', ''),  # Direct media URL
                'edmPreview': item.get('edmPreview', '')  # Preview image URL
            },
            'DocumentationsAPI': item.get('link', ''),  # API endpoint
            'OriginalData': {
                'guid': item.get('guid', ''),
                'europeanaCollectionName': item.get('europeanaCollectionName', ''),
                'provider': item.get('provider', ''),
                'type': item.get('type', ''),
                'language': item.get('language', [])
            }
        }
        
        # Extract related people (creators, contributors)
        if 'dcCreator' in item:
            creators = self._flatten_list(item['dcCreator'])
            extended_metadata['RelatedPeople'].extend(creators)
        
        # Extract related collections
        if 'europeanaCollectionName' in item:
            collections = self._flatten_list(item['europeanaCollectionName'])
            extended_metadata['RelatedCollections'].extend(collections)
        
        return extended_metadata
    
    def process_item(self, item: Dict[str, Any], text: str, 
                    lda_topics: List[Dict] = None) -> Dict[str, Any]:
        """
        Process a single data item to generate complete mapped structure
        
        Args:
            item: Dictionary containing item metadata
            text: Combined text for analysis
            lda_topics: Optional LDA topic analysis results
            
        Returns:
            Dictionary with complete mapped metadata structure
        """
        try:
            # Build complete result structure
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
            # Handle processing errors gracefully
            print(f"Error processing item {item.get('id', 'unknown')}: {e}")
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
