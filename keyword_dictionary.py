#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关键词字典模块 - 优化版
功能：管理瓷器相关的关键词字典，支持动态修改
增强：更好的产地识别（包括代尔夫特和比利时）
"""

from typing import Dict, List, Set
import json

class KeywordDictionary:
    """关键词字典管理器"""
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file
        self._init_keywords()
        
        # 如果提供了配置文件，尝试加载
        if config_file:
            self.load_from_file(config_file)
    
    def _init_keywords(self):
        """初始化默认关键词字典"""
        
        # 颜色关键词
        self.color_keywords = {
            'blue and white': ['blue', 'white', 'blue and white', 'underglaze blue', 'cobalt blue', 'qinghua', 'blue white', 'delft blue', 'delfts blauw'],
            'celadon': ['celadon', 'green glaze', 'greenish', 'longquan celadon', 'yue celadon', 'greenware', 'sea green'],
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
        
        # 装饰主题关键词
        self.decoration_themes = {
            'floral': ['flower', 'floral', 'peony', 'lotus', 'chrysanthemum', 
                      'prunus', 'bamboo', 'pine', 'plant', 'leaf', 'branch',
                      'bloom', 'blossom', 'orchid', 'camellia', 'magnolia', 
                      'plum blossom', 'rose', 'lily', 'iris', 'narcissus', 
                      'tree', 'foliage', 'vine', 'spray', 'flowers', 'petals', 
                      'stems', 'buds', 'willow', 'tulip'],  # 添加郁金香（荷兰特色）
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
                         'windmill', 'canal', 'dutch landscape'],  # 添加荷兰景观元素
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
                        'coat of arms', 'heraldic']  # 添加欧洲纹章元素
        }
        
        # 形状关键词
        self.shape_keywords = {
            'bowl': ['bowl', 'deep bowl', 'shallow bowl', 'tea bowl', 'rice bowl', 'lotus bowl'],
            'vase': ['vase', 'meiping', 'baluster vase', 'bottle vase', 'gu', 'hu', 'zun', 'tulip vase'],  # 添加郁金香花瓶
            'jar': ['jar', 'ginger jar', 'storage jar', 'covered jar', 'lidded jar', 'tobacco jar'],
            'plate': ['plate', 'dish', 'charger', 'saucer', 'platter'],
            'cup': ['cup', 'tea cup', 'wine cup', 'stem cup', 'beaker', 'teacup'],
            'pot': ['pot', 'teapot', 'wine pot', 'water pot', 'ewer', 'kettle', 'coffee pot'],
            'bottle': ['bottle', 'moon flask', 'double gourd', 'pilgrim flask', 'snuff bottle'],
            'box': ['box', 'covered box', 'seal box', 'cosmetic box', 'container'],
            'censer': ['censer', 'incense burner', 'tripod censer', 'brazier'],
            'ewer': ['ewer', 'wine ewer', 'water ewer', 'spouted vessel', 'pitcher'],
            'tile': ['tile', 'wall tile', 'floor tile', 'decorative tile']  # 添加瓷砖（代尔夫特特色）
        }
        
        # 功能关键词
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
            'pharmaceutical': ['pharmaceutical', 'apothecary', 'medicine', 'drug jar']  # 添加药用（代尔夫特特色）
        }
        
        # 材质关键词
        self.material_keywords = {
            'porcelain': ['porcelain', 'hard-paste', 'soft-paste', 'high-fired', 'paste porcelain', 'chinese porcelain'],
            'stoneware': ['stoneware', 'stone ware', 'proto-porcelain'],
            'earthenware': ['earthenware', 'pottery', 'terracotta', 'ceramics', 'faience', 'delftware'],
            'ceramic': ['ceramic', 'pottery']
        }
        
        # 釉色技术关键词
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
        
        # 生产地关键词 - 大幅扩展
        self.production_keywords = {
            # 中国产地
            'jingdezhen': ['jingdezhen', 'jiangxi', 'imperial kiln', 'porcelain capital', 'ching-te-chen'],
            'longquan': ['longquan', 'zhejiang', 'longquan kiln'],
            'dehua': ['dehua', 'fujian', 'blanc de chine', 'white porcelain', 'te-hua'],
            'yixing': ['yixing', 'jiangsu', 'purple clay', 'zisha'],
            'jun': ['jun', 'junzhou', 'henan', 'jun kiln', 'chun'],
            'ding': ['ding', 'dingzhou', 'hebei', 'ding kiln'],
            'cizhou': ['cizhou', 'hebei', 'cizhou kiln', 'tz\'u-chou'],
            'yaozhou': ['yaozhou', 'shaanxi', 'yaozhou kiln'],
            'china': ['china', 'chinese', 'middle kingdom', 'zhongguo', 'chine', 'cina', 'kina'],
            
            # 荷兰产地
            'delft': ['delft', 'delftware', 'delfts', 'delftse', 'hollants porceleyn', 'dutch delft', 
                     'de porceleyne fles', 'de grieksche a', 'de witte ster', 'royal delft',
                     'de delftse pauw', 'delft pottery', 'delfts blauw'],
            'amsterdam': ['amsterdam', 'amsterdamse'],
            'rotterdam': ['rotterdam', 'rotterdamse'],
            'haarlem': ['haarlem', 'haarlemse'],
            'makkum': ['makkum', 'tichelaar', 'friesland'],
            'netherlands': ['netherlands', 'dutch', 'holland', 'nederlandse', 'hollandse', 'nederland'],
            
            # 比利时产地
            'belgium': ['belgium', 'belgian', 'belgique', 'belgie', 'belgisch'],
            'brussels': ['brussels', 'bruxelles', 'brussel'],
            'antwerp': ['antwerp', 'antwerpen', 'anvers'],
            'tournai': ['tournai', 'doornik'],
            'ghent': ['ghent', 'gent', 'gand'],
            
            # 其他欧洲产地
            'meissen': ['meissen', 'dresden', 'saxony'],
            'sevres': ['sevres', 'vincennes'],
            'worcester': ['worcester', 'dr wall'],
            'staffordshire': ['staffordshire', 'stoke on trent'],
            
            # 出口和贸易相关
            'export': ['export', 'canton', 'guangzhou', 'trade port', 'chinese export', 'export porcelain'],

            # 在 production_keywords 中扩展 delft 相关关键词
            'delft': ['delft', 'delftware', 'delfts', 'delftse', 'hollants porceleyn', 'dutch delft', 
                    'de porceleyne fles', 'de grieksche a', 'de witte ster', 'royal delft',
                    'de delftse pauw', 'delft pottery', 'delfts blauw', 'delft blue',
                    'tin glaze', 'tin-glaze', 'tin glazed', 'tin-glazed',  # 锡釉相关
                    'faience', 'faïence', 'plateel',  # 欧洲锡釉陶
                    'galleyware', 'galliware',  # 英国称呼
                    'maiolica', 'majolica',  # 意大利锡釉陶
                    'dutch blue and white', 'dutch blue white',  # 荷兰蓝白瓷
                    'tin glazuur', 'tinglazuur'],  # 荷兰语锡釉
        }
        
        # 朝代/时期关键词 - 增加年份对应
        self.period_keywords = {
            'tang': ['tang', 'tang dynasty', '618-907', '7th century', '8th century', '9th century'],
            'song': ['song', 'northern song', 'southern song', 'song dynasty', '960-1279', '10th century', '11th century', '12th century', '13th century'],
            'yuan': ['yuan', 'mongol', 'yuan dynasty', '1279-1368', '13th century', '14th century'],
            'ming': ['ming', 'hongwu', 'yongle', 'xuande', 'chenghua', 'zhengde', 
                    'jiajing', 'wanli', 'tianqi', 'chongzhen', 'ming dynasty', '1368-1644',
                    '14th century', '15th century', '16th century', '17th century'],
            'qing': ['qing', 'shunzhi', 'kangxi', 'yongzheng', 'qianlong', 'jiaqing', 
                    'daoguang', 'xianfeng', 'tongzhi', 'guangxu', 'xuantong', 'qing dynasty',
                    '1644-1911', '17th century', '18th century', '19th century', '20th century'],
            'republic': ['republic', 'minguo', 'republic of china', '1912-1949'],
            'modern': ['modern', 'contemporary', '20th century', '21st century', '1900s', '2000s'],
            
            # 欧洲时期
            'delft_golden_age': ['1640-1740', 'dutch golden age', '17th century delft', '18th century delft'],
            'delft_revival': ['1870-1920', 'delft revival', 'new delft', 'art nouveau delft']
        }
        
       # 更新 place_normalization 字典，添加更多布鲁塞尔变体
        self.place_normalization = {
            # 中国变体
            'china': ['china', 'chine', 'cina', 'kina', 'kitajska', 'txina', 'kína', 'ķīna', 'kiina', 'hiina',
                    'čína', 'síne', 'xina', 'kinijos', 'chinese', 'chińska', 'ljudska republika kitajska',
                    'txinako herri errepublika', 'repubblika tal-poplu taċ-ċina', 'λαϊκή δημοκρατία της κίνας',
                    'daon-phoblacht na síne', 'república popular de la xina', 'kinijos liaudies respublika',
                    '中国', 'zhongguo', 'middle kingdom', 'китай'],
            
            # 维也纳变体（奥地利）- 注意：这可能是博物馆位置而非生产地
            'vienna': ['vienna', 'wien', 'viena', 'viin', 'viedeň', 'виена', 'bécs', 'vienne'],
            
            # 荷兰变体
            'netherlands': ['netherlands', 'nederland', 'holland', 'pays-bas', 'niederlande', 'olanda',
                        'países bajos', 'países baixos', 'paesi bassi', 'holandia', 'hollanda'],
            
            # 比利时变体
            'belgium': ['belgium', 'belgique', 'belgië', 'belgien', 'bélgica', 'belgio', 'belgia'],
            
            # 布鲁塞尔的所有变体
            'brussels': ['brussels', 'bruxelles', 'brussel', 'an bhruiséil', 'brisele', 'briseles',
                        'briuselio', 'briuselis', 'bruksela', 'brusel', 'brusela', 'brüssel'],
            
            # 英国变体
            'united_kingdom': ['united kingdom', 'uk', 'britain', 'great britain', 'england',
                            'an ríocht aontaithe', 'apvienotā karaliste', 'egyesült királyság',
                            'erresuma batua', 'regatul unit'],
            
            # 日本变体
            'japan': ['japan', 'nippon', 'an tseapáin', '日本']
        }
    
   # 在 keyword_dictionary.py 中更新 normalize_place 方法和添加新的映射

    def normalize_place(self, place: str) -> str:
        """标准化产地名称"""
        if not place:
            return place
            
        place_lower = place.lower().strip()
        
        # 过滤掉博物馆和机构名称
        museum_keywords = ['museum', 'gallery', 'collection', 'hallwyl', 'herstellung', 'manufacture']
        if any(keyword in place_lower for keyword in museum_keywords):
            return None
        
        # 检查是否匹配任何标准化映射
        for standard_name, variants in self.place_normalization.items():
            for variant in variants:
                if variant in place_lower:
                    return standard_name
        
        # 检查具体产地
        for place_type, keywords in self.production_keywords.items():
            for keyword in keywords:
                if keyword.lower() in place_lower:
                    return place_type
        
        # 如果都不匹配，返回原值（如果不是太长）
        if len(place) > 50:
            return None
            
        return place
        
    def get_dynasty_from_year(self, year: int) -> str:
        """根据年份返回对应的朝代"""
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
        """根据年份返回世纪"""
        century = (year - 1) // 100 + 1
        if century == 1:
            return "1st century"
        elif century == 2:
            return "2nd century"
        elif century == 3:
            return "3rd century"
        else:
            return f"{century}th century"
    
    def add_keyword(self, category: str, key: str, keywords: List[str]):
        """添加关键词到指定类别"""
        category_dict = getattr(self, f"{category}_keywords", None)
        if category_dict is not None:
            if key in category_dict:
                category_dict[key].extend(keywords)
                category_dict[key] = list(set(category_dict[key]))  # 去重
            else:
                category_dict[key] = keywords
    
    def remove_keyword(self, category: str, key: str, keywords: List[str]):
        """从指定类别移除关键词"""
        category_dict = getattr(self, f"{category}_keywords", None)
        if category_dict is not None and key in category_dict:
            category_dict[key] = [k for k in category_dict[key] if k not in keywords]
    
    def update_category(self, category: str, new_dict: Dict[str, List[str]]):
        """更新整个类别的关键词字典"""
        if hasattr(self, f"{category}_keywords"):
            setattr(self, f"{category}_keywords", new_dict)
    
    def get_all_keywords(self) -> Dict[str, Dict[str, List[str]]]:
        """获取所有关键词字典"""
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
        """保存关键词字典到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.get_all_keywords(), f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, filename: str):
        """从文件加载关键词字典"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.color_keywords = data.get('color', {})
            self.decoration_themes = data.get('decoration_themes', {})
            self.shape_keywords = data.get('shape', {})
            self.function_keywords = data.get('function', {})
            self.material_keywords = data.get('material', {})
            self.glaze_keywords = data.get('glaze', {})
            self.production_keywords = data.get('production', {})
            self.period_keywords = data.get('period', {})
            
            print(f"✅ 从 {filename} 加载关键词字典成功")
        except Exception as e:
            print(f"❌ 加载关键词字典失败: {e}")