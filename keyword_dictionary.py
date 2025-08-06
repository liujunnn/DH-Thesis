#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Keyword Dictionary Module for Cultural Heritage Metadata Extraction

This module provides a comprehensive keyword dictionary system for identifying
and normalizing cultural heritage terminology across multiple languages and
cultures. It supports extraction of attributes from ceramic and pottery
descriptions with a focus on both Eastern (Chinese) and Western (European,
particularly Dutch/Delft) traditions.

Key Features:
- Multi-language keyword mappings for colors, shapes, decorations, etc.
- Historical period and dynasty recognition
- Production location normalization across language variants
- Configurable keyword management with file persistence
- Support for both Chinese imperial ceramics and European pottery traditions

Author: [Your Name]
Date: [Current Date]
Version: 1.0
"""

from typing import Dict, List, Set
import json

class KeywordDictionary:
    """
    Keyword Dictionary Manager for cultural heritage metadata extraction
    
    This class maintains comprehensive keyword mappings for extracting
    structured information from unstructured text descriptions of ceramics,
    pottery, and porcelain items. It includes specialized vocabulary for:
    - Chinese imperial ceramics (Ming, Qing dynasties)
    - European pottery (Delftware, Meissen, Sèvres)
    - Cross-cultural export porcelain
    
    Attributes:
        config_file: Optional path to JSON configuration file
        color_keywords: Color terminology mappings
        decoration_themes: Decorative motif categorizations
        shape_keywords: Vessel form classifications
        function_keywords: Functional use categories
        material_keywords: Material composition terms
        glaze_keywords: Glaze technique terminology
        production_keywords: Production center identifications
        period_keywords: Historical period mappings
        place_normalization: Multi-language place name standardization
    """
    
    def __init__(self, config_file: str = None):
        """
        Initialize the KeywordDictionary with default or custom keywords
        
        Args:
            config_file: Optional path to JSON file containing custom keyword mappings
        """
        self.config_file = config_file
        self._init_keywords()
        
        # Load custom keywords from file if provided
        if config_file:
            self.load_from_file(config_file)
    
    def _init_keywords(self):
        """
        Initialize default keyword dictionaries with comprehensive terminology
        
        This method sets up the default keyword mappings covering:
        - Traditional Chinese ceramic terminology
        - European pottery terminology (especially Dutch/Delft)
        - Modern classification systems
        - Multi-language variations
        """
        
        # Color keywords including traditional glaze colors and modern descriptions
        self.color_keywords = {
            'blue and white': ['blue', 'white', 'blue and white', 'underglaze blue', 'cobalt blue', 
                              'qinghua', 'blue white', 'delft blue', 'delfts blauw'],
            'celadon': ['celadon', 'green glaze', 'greenish', 'longquan celadon', 'yue celadon', 
                       'greenware', 'sea green'],
            'famille rose': ['famille rose', 'pink', 'rose', 'fencai', 'yangcai', 'enamel pink'],
            'famille verte': ['famille verte', 'green family', 'kangxi palette', 'wucai'],
            'red': ['red', 'copper red', 'iron red', 'sang de boeuf', 'oxblood', 'jihong', 'crimson'],
            'yellow': ['yellow', 'imperial yellow', 'egg yolk', 'lemon yellow', 'mustard'],
            'black': ['black', 'mirror black', 'tenmoku', 'jian ware'],
            'brown': ['brown', 'cafe-au-lait', 'chocolate', 'tea dust', 'coffee'],
            'purple': ['purple', 'aubergine', 'violet', 'lavender', 'plum'],
            'green': ['green', 'apple green', 'cucumber green', 'emerald', 'jade'],
            'gold': ['gold', 'gilt', 'gilded', 'golden', 'gilding'],
            'multicolor': ['polychrome', 'multicolor', 'wucai', 'doucai', 'contrasting colors', 'five color']
        }
        
        # Decoration theme keywords covering Eastern and Western motifs
        self.decoration_themes = {
            'floral': ['flower', 'floral', 'peony', 'lotus', 'chrysanthemum', 
                      'prunus', 'bamboo', 'pine', 'plant', 'leaf', 'branch',
                      'bloom', 'blossom', 'orchid', 'camellia', 'magnolia', 
                      'plum blossom', 'rose', 'lily', 'iris', 'narcissus', 
                      'tree', 'foliage', 'vine', 'spray', 'flowers', 'petals', 
                      'stems', 'buds', 'willow', 'tulip'],  # Added tulip (Dutch characteristic)
            
            'figural': ['figure', 'people', 'scholar', 'lady', 'child', 'immortal',
                       'deity', 'warrior', 'official', 'sage', 'goddess', 
                       'emperor', 'court', 'attendant', 'maiden', 'monk', 
                       'buddha', 'bodhisattva', 'luohan', 'guanyin', 'figures', 
                       'person', 'man', 'woman', 'boy', 'dutch figure', 'european figure'],
            
            'animal': ['dragon', 'phoenix', 'bird', 'crane', 'fish', 'deer', 
                      'lion', 'tiger', 'horse', 'butterfly', 'qilin', 'foo dog', 
                      'bat', 'magpie', 'peacock', 'eagle', 'carp', 'goldfish', 
                      'mandarin duck', 'rooster', 'rabbit', 'birds', 'animals'],
            
            'landscape': ['landscape', 'mountain', 'river', 'pavilion', 'garden',
                         'rock', 'tree', 'cloud', 'moon', 'scenery', 'waterfall', 
                         'bridge', 'pagoda', 'temple', 'island', 'boat', 'shore', 
                         'cliff', 'wave', 'mist', 'mountains', 'hills', 'valley', 'lake',
                         'windmill', 'canal', 'dutch landscape'],  # Added Dutch landscape elements
            
            'geometric': ['geometric', 'pattern', 'band', 'border', 'scroll',
                         'lattice', 'diaper', 'key-fret', 'meander', 'lozenge', 
                         'checkerboard', 'zigzag', 'diamond', 'hexagon', 'octagon', 
                         'circle', 'square', 'triangle', 'stripes', 'dots', 'lines'],
            
            'calligraphy': ['character', 'inscription', 'poem', 'text', 'writing',
                           'calligraphy', 'seal script', 'kaishu', 'poetry', 
                           'verse', 'couplet', 'mark', 'characters', 'script'],
            
            'symbolic': ['ruyi', 'shou', 'fu', 'lu', 'xi', 'bagua', 'taiji',
                        'yin yang', 'endless knot', 'auspicious', 'symbol',
                        'eight treasures', 'buddhist emblems', 'daoist emblems',
                        'coat of arms', 'heraldic']  # Added European heraldic elements
        }
        
        # Shape keywords for vessel forms
        self.shape_keywords = {
            'bowl': ['bowl', 'deep bowl', 'shallow bowl', 'tea bowl', 'rice bowl', 'lotus bowl'],
            'vase': ['vase', 'meiping', 'baluster vase', 'bottle vase', 'gu', 'hu', 'zun', 
                    'tulip vase'],  # Added tulip vase (Dutch specialty)
            'jar': ['jar', 'ginger jar', 'storage jar', 'covered jar', 'lidded jar', 'tobacco jar'],
            'plate': ['plate', 'dish', 'charger', 'saucer', 'platter'],
            'cup': ['cup', 'tea cup', 'wine cup', 'stem cup', 'beaker', 'teacup'],
            'pot': ['pot', 'teapot', 'wine pot', 'water pot', 'ewer', 'kettle', 'coffee pot'],
            'bottle': ['bottle', 'moon flask', 'double gourd', 'pilgrim flask', 'snuff bottle'],
            'box': ['box', 'covered box', 'seal box', 'cosmetic box', 'container'],
            'censer': ['censer', 'incense burner', 'tripod censer', 'brazier'],
            'ewer': ['ewer', 'wine ewer', 'water ewer', 'spouted vessel', 'pitcher'],
            'tile': ['tile', 'wall tile', 'floor tile', 'decorative tile']  # Added tile (Delft characteristic)
        }
        
        # Function keywords for usage categories
        self.function_keywords = {
            'tea': ['tea', 'tea bowl', 'teapot', 'tea cup', 'tea ceremony', 'tea service'],
            'wine': ['wine', 'wine cup', 'wine pot', 'wine vessel', 'drinking'],
            'dining': ['dining', 'eating', 'food', 'serving', 'table', 'banquet', 'tableware'],
            'ceremonial': ['ceremonial', 'ritual', 'religious', 'altar', 'offering', 'sacrifice', 'temple'],
            'storage': ['storage', 'container', 'jar', 'keeping', 'preservation', 'vessel', 'tobacco'],
            'decorative': ['decorative', 'display', 'ornamental', 'aesthetic', 'ornament'],
            'scholarly': ['scholar', 'study', 'desk', 'brush', 'ink', 'literati', 'studio', 'writing'],
            'cosmetic': ['cosmetic', 'powder', 'rouge', 'mirror', 'toiletry', 'makeup'],
            'export': ['export', 'trade', 'commercial', 'overseas', 'maritime', 'shipping', 'canton'],
            'pharmaceutical': ['pharmaceutical', 'apothecary', 'medicine', 'drug jar']  # Added pharmaceutical (Delft specialty)
        }
        
        # Material keywords for composition
        self.material_keywords = {
            'porcelain': ['porcelain', 'hard-paste', 'soft-paste', 'high-fired', 'paste porcelain', 
                         'chinese porcelain'],
            'stoneware': ['stoneware', 'stone ware', 'proto-porcelain'],
            'earthenware': ['earthenware', 'pottery', 'terracotta', 'ceramics', 'faience', 'delftware'],
            'ceramic': ['ceramic', 'pottery']
        }
        
        # Glaze technique keywords
        self.glaze_keywords = {
            'celadon': ['celadon', 'longquan', 'guan', 'ge', 'greenware', 'yue ware', 'ru ware'],
            'blue_white': ['blue and white', 'underglaze blue', 'cobalt', 'qinghua', 'ming blue', 'delft blue'],
            'famille_rose': ['famille rose', 'fencai', 'overglaze enamel', 'yangcai', 'rose enamel'],
            'famille_verte': ['famille verte', 'wucai', 'five color', 'kangxi colors'],
            'monochrome': ['monochrome', 'single color', 'solid glaze', 'plain'],
            'crackle': ['crackle', 'crazing', 'ice crackle', 'ge glaze', 'craquelure'],
            'flambe': ['flambe', 'transmutation', 'jun glaze', 'copper splash'],
            'sancai': ['sancai', 'three color', 'tang sancai', 'tricolor'],
            'underglaze': ['underglaze', 'underglaze red', 'underglaze copper', 'underglaze painting'],
            'overglaze': ['overglaze', 'enamel', 'enameled', 'overglaze enamel'],
            'transfer': ['transfer', 'transfer printed', 'transfer print', 'printed'],
            'tin_glaze': ['tin glaze', 'tin-glazed', 'tin glazed', 'tin-glaze', 'maiolica', 'majolica',
                        'faience', 'faïence', 'émail stannifère', 'tinglazuur', 'plateel',
                        'fayence', 'zinnglasur', 'galleyware', 'galliware', 'delftware']
        }
        
        # Production location keywords - Extensively expanded for global coverage
        self.production_keywords = {
            # Chinese production centers
            'jingdezhen': ['jingdezhen', 'jiangxi', 'imperial kiln', 'porcelain capital', 'ching-te-chen'],
            'longquan': ['longquan', 'zhejiang', 'longquan kiln'],
            'dehua': ['dehua', 'fujian', 'blanc de chine', 'white porcelain', 'te-hua'],
            'yixing': ['yixing', 'jiangsu', 'purple clay', 'zisha'],
            'jun': ['jun', 'junzhou', 'henan', 'jun kiln', 'chun'],
            'ding': ['ding', 'dingzhou', 'hebei', 'ding kiln'],
            'cizhou': ['cizhou', 'hebei', 'cizhou kiln', 'tz\'u-chou'],
            'yaozhou': ['yaozhou', 'shaanxi', 'yaozhou kiln'],
            'china': ['china', 'chinese', 'middle kingdom', 'zhongguo', 'chine', 'cina', 'kina'],
            
            # Dutch production centers (extensive Delft coverage)
            'delft': ['delft', 'delftware', 'delfts', 'delftse', 'hollants porceleyn', 'dutch delft', 
                     'de porceleyne fles', 'de grieksche a', 'de witte ster', 'royal delft',
                     'de delftse pauw', 'delft pottery', 'delfts blauw', 'delft blue',
                     'tin glaze', 'tin-glaze', 'tin glazed', 'tin-glazed',  # Tin glaze related
                     'faience', 'faïence', 'plateel',  # European tin-glazed pottery
                     'galleyware', 'galliware',  # British terminology
                     'maiolica', 'majolica',  # Italian tin-glazed pottery
                     'dutch blue and white', 'dutch blue white',  # Dutch blue and white
                     'tin glazuur', 'tinglazuur'],  # Dutch tin glaze terms
            'amsterdam': ['amsterdam', 'amsterdamse'],
            'rotterdam': ['rotterdam', 'rotterdamse'],
            'haarlem': ['haarlem', 'haarlemse'],
            'makkum': ['makkum', 'tichelaar', 'friesland'],
            'netherlands': ['netherlands', 'dutch', 'holland', 'nederlandse', 'hollandse', 'nederland'],
            
            # Belgian production centers
            'belgium': ['belgium', 'belgian', 'belgique', 'belgie', 'belgisch'],
            'brussels': ['brussels', 'bruxelles', 'brussel'],
            'antwerp': ['antwerp', 'antwerpen', 'anvers'],
            'tournai': ['tournai', 'doornik'],
            'ghent': ['ghent', 'gent', 'gand'],
            
            # Other European production centers
            'meissen': ['meissen', 'dresden', 'saxony'],
            'sevres': ['sevres', 'vincennes'],
            'worcester': ['worcester', 'dr wall'],
            'staffordshire': ['staffordshire', 'stoke on trent'],
            
            # Export and trade related
            'export': ['export', 'canton', 'guangzhou', 'trade port', 'chinese export', 'export porcelain'],
        }
        
        # Historical period/dynasty keywords with year mappings
        self.period_keywords = {
            # Chinese dynasties with reign periods
            'tang': ['tang', 'tang dynasty', '618-907', '7th century', '8th century', '9th century'],
            'song': ['song', 'northern song', 'southern song', 'song dynasty', '960-1279', 
                    '10th century', '11th century', '12th century', '13th century'],
            'yuan': ['yuan', 'mongol', 'yuan dynasty', '1279-1368', '13th century', '14th century'],
            'ming': ['ming', 'hongwu', 'yongle', 'xuande', 'chenghua', 'zhengde', 
                    'jiajing', 'wanli', 'tianqi', 'chongzhen', 'ming dynasty', '1368-1644',
                    '14th century', '15th century', '16th century', '17th century'],
            'qing': ['qing', 'shunzhi', 'kangxi', 'yongzheng', 'qianlong', 'jiaqing', 
                    'daoguang', 'xianfeng', 'tongzhi', 'guangxu', 'xuantong', 'qing dynasty',
                    '1644-1911', '17th century', '18th century', '19th century', '20th century'],
            'republic': ['republic', 'minguo', 'republic of china', '1912-1949'],
            'modern': ['modern', 'contemporary', '20th century', '21st century', '1900s', '2000s'],
            
            # European periods specific to pottery
            'delft_golden_age': ['1640-1740', 'dutch golden age', '17th century delft', '18th century delft'],
            'delft_revival': ['1870-1920', 'delft revival', 'new delft', 'art nouveau delft']
        }
        
        # Place name normalization dictionary for multi-language support
        # Maps standard names to all known language variants
        self.place_normalization = {
            # China variants across languages
            'china': ['china', 'chine', 'cina', 'kina', 'kitajska', 'txina', 'kína', 'ķīna', 'kiina', 'hiina',
                    'čína', 'síne', 'xina', 'kinijos', 'chinese', 'chińska', 'ljudska republika kitajska',
                    'txinako herri errepublika', 'repubblika tal-poplu taċ-ċina', 'λαϊκή δημοκρατία της κίνας',
                    'daon-phoblacht na síne', 'república popular de la xina', 'kinijos liaudies respublika',
                    '中国', 'zhongguo', 'middle kingdom', 'китай'],
            
            # Vienna variants (Austria) - Note: Often a museum location rather than production site
            'vienna': ['vienna', 'wien', 'viena', 'viin', 'viedeň', 'виена', 'bécs', 'vienne'],
            
            # Netherlands variants
            'netherlands': ['netherlands', 'nederland', 'holland', 'pays-bas', 'niederlande', 'olanda',
                        'países bajos', 'países baixos', 'paesi bassi', 'holandia', 'hollanda'],
            
            # Belgium variants
            'belgium': ['belgium', 'belgique', 'belgië', 'belgien', 'bélgica', 'belgio', 'belgia'],
            
            # Brussels variants (all linguistic variations)
            'brussels': ['brussels', 'bruxelles', 'brussel', 'an bhruiséil', 'brisele', 'briseles',
                        'briuselio', 'briuselis', 'bruksela', 'brusel', 'brusela', 'brüssel'],
            
            # United Kingdom variants
            'united_kingdom': ['united kingdom', 'uk', 'britain', 'great britain', 'england',
                            'an ríocht aontaithe', 'apvienotā karaliste', 'egyesült királyság',
                            'erresuma batua', 'regatul unit'],
            
            # Japan variants
            'japan': ['japan', 'nippon', 'an tseapáin', '日本']
        }
    
    def normalize_place(self, place: str) -> str:
        """
        Normalize place names across different languages and variations
        
        This method handles:
        - Multi-language place name variations
        - Museum location filtering (not production places)
        - Standardization to consistent naming conventions
        - Length validation to filter out invalid entries
        
        Args:
            place: Raw place name string in any language
            
        Returns:
            Normalized place name or None if invalid/museum location
            
        Example:
            >>> dict.normalize_place("Bruxelles")
            'brussels'
            >>> dict.normalize_place("Museum of Vienna")
            None  # Filtered as museum location
        """
        if not place:
            return place
            
        place_lower = place.lower().strip()
        
        # Filter out museum and institution names (not production locations)
        museum_keywords = ['museum', 'gallery', 'collection', 'hallwyl', 'herstellung', 'manufacture']
        if any(keyword in place_lower for keyword in museum_keywords):
            return None
        
        # Check against standardized place name mappings
        for standard_name, variants in self.place_normalization.items():
            for variant in variants:
                if variant in place_lower:
                    return standard_name
        
        # Check against specific production location keywords
        for place_type, keywords in self.production_keywords.items():
            for keyword in keywords:
                if keyword.lower() in place_lower:
                    return place_type
        
        # Filter out overly long strings (likely not valid place names)
        if len(place) > 50:
            return None
            
        return place
        
    def get_dynasty_from_year(self, year: int) -> str:
        """
        Convert a year to its corresponding Chinese dynasty
        
        Args:
            year: Year as integer (e.g., 1500)
            
        Returns:
            Dynasty name as string (e.g., 'Ming')
            
        Example:
            >>> dict.get_dynasty_from_year(1500)
            'Ming'
            >>> dict.get_dynasty_from_year(1700)
            'Qing'
        """
        if 618 <= year <= 907:
            return 'Tang'
        elif 960 <= year <= 1279:
            return 'Song'
        elif 1279 <= year <= 1368:
            return 'Yuan'
        elif 1368 <= year <= 1644:
            return 'Ming'
        elif 1644 <= year <= 1911:
            return 'Qing'
        elif 1912 <= year <= 1949:
            return 'Republic'
        elif year >= 1950:
            return 'Modern'
        else:
            return 'Unknown'
    
    def get_century_from_year(self, year: int) -> str:
        """
        Convert a year to its century in ordinal format
        
        Args:
            year: Year as integer
            
        Returns:
            Century as string with ordinal suffix (e.g., '16th century')
            
        Example:
            >>> dict.get_century_from_year(1650)
            '17th century'
        """
        century = (year - 1) // 100 + 1
        
        # Handle ordinal suffixes correctly
        if century == 1:
            return "1st century"
        elif century == 2:
            return "2nd century"
        elif century == 3:
            return "3rd century"
        else:
            return f"{century}th century"
    
    def add_keyword(self, category: str, key: str, keywords: List[str]):
        """
        Add keywords to a specified category
        
        Args:
            category: Category name (e.g., 'color', 'shape', 'material')
            key: Subcategory key (e.g., 'blue and white', 'vase')
            keywords: List of new keywords to add
            
        Example:
            >>> dict.add_keyword('color', 'blue and white', ['kraak', 'transitional'])
        """
        category_dict = getattr(self, f"{category}_keywords", None)
        if category_dict is not None:
            if key in category_dict:
                category_dict[key].extend(keywords)
                # Remove duplicates while preserving order
                category_dict[key] = list(set(category_dict[key]))
            else:
                category_dict[key] = keywords
    
    def remove_keyword(self, category: str, key: str, keywords: List[str]):
        """
        Remove keywords from a specified category
        
        Args:
            category: Category name
            key: Subcategory key
            keywords: List of keywords to remove
        """
        category_dict = getattr(self, f"{category}_keywords", None)
        if category_dict is not None and key in category_dict:
            category_dict[key] = [k for k in category_dict[key] if k not in keywords]
    
    def update_category(self, category: str, new_dict: Dict[str, List[str]]):
        """
        Replace entire category dictionary with new mappings
        
        Args:
            category: Category name to update
            new_dict: New dictionary of keyword mappings
        """
        if hasattr(self, f"{category}_keywords"):
            setattr(self, f"{category}_keywords", new_dict)
    
    def get_all_keywords(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Get all keyword dictionaries as a single structure
        
        Returns:
            Dictionary containing all keyword categories and their mappings
        """
        return {
            'color': self.color_keywords,
            'decoration_themes': self.decoration_themes,
            'shape': self.shape_keywords,
            'function': self.function_keywords,
            'material': self.material_keywords,
            'glaze': self.glaze_keywords,
            'production': self.production_keywords,
            'period': self.period_keywords
        }
    
    def save_to_file(self, filename: str):
        """
        Save keyword dictionaries to JSON file
        
        Args:
            filename: Path to output JSON file
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.get_all_keywords(), f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, filename: str):
        """
        Load keyword dictionaries from JSON file
        
        Args:
            filename: Path to input JSON file
            
        Note:
            File should contain a JSON object with keys matching category names
            (color, decoration_themes, shape, etc.) and values as dictionaries
            of keyword mappings.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Load each category from the JSON data
            self.color_keywords = data.get('color', {})
            self.decoration_themes = data.get('decoration_themes', {})
            self.shape_keywords = data.get('shape', {})
            self.function_keywords = data.get('function', {})
            self.material_keywords = data.get('material', {})
            self.glaze_keywords = data.get('glaze', {})
            self.production_keywords = data.get('production', {})
            self.period_keywords = data.get('period', {})
            
            print(f"✅ Successfully loaded keyword dictionary from {filename}")
        except Exception as e:
            print(f"❌ Failed to load keyword dictionary: {e}")
