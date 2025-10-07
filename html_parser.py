"""
HTML Parser for North Indian Chaldean Numerology Excel Export
Extracts calculation formulas, structures, and data from Excel HTML files
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any
from bs4 import BeautifulSoup


class NumerologyHTMLParser:
    """Parser for extracting numerology data from Excel HTML exports"""
    
    def __init__(self, base_path: str = "src/Numerology Calculator savi's enhanced_files"):
        self.base_path = Path(base_path)
        self.parsed_data = {}
        self.sheets = {
            'sheet001.htm': 'Instructions_Glossary',
            'sheet002.htm': 'Master_Calculator', 
            'sheet003.htm': 'Lo_Shu_Grid',
            'sheet004.htm': 'Personal_Year_Month_Day',
            'sheet005.htm': 'Mobile_Vehicle_House_Bank_CoNam',
            'sheet006.htm': 'Past_Future_PY_PM_PD',
            'sheet007.htm': 'Output'
        }
        
    def parse_all_sheets(self) -> Dict[str, Any]:
        """Parse all Excel sheets and extract numerology data"""
        for sheet_file, sheet_name in self.sheets.items():
            sheet_path = self.base_path / sheet_file
            if sheet_path.exists():
                print(f"Parsing {sheet_name}...")
                self.parsed_data[sheet_name] = self.parse_sheet(sheet_path)
            else:
                print(f"Warning: {sheet_file} not found")
                
        return self.parsed_data
    
    def parse_sheet(self, file_path: Path) -> Dict[str, Any]:
        """Parse individual sheet and extract relevant data"""
        # Try different encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252', 'windows-1252']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        else:
            print(f"Warning: Could not decode {file_path}")
            return {}
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract table data
        tables = soup.find_all('table')
        sheet_data = {
            'title': file_path.stem,
            'tables': [],
            'formulas': [],
            'abbreviations': {},
            'sample_data': {},
            'structures': []
        }
        
        # Parse tables for data
        for i, table in enumerate(tables):
            table_data = self.parse_table(table)
            if table_data:
                sheet_data['tables'].append({
                    'index': i,
                    'data': table_data
                })
        
        # Extract specific numerology patterns
        sheet_data.update(self.extract_numerology_patterns(content))
        
        return sheet_data
    
    def parse_table(self, table) -> List[List[str]]:
        """Extract table data as 2D array"""
        rows = []
        for tr in table.find_all('tr'):
            row = []
            for td in tr.find_all(['td', 'th']):
                # Clean text content
                text = td.get_text(strip=True)
                # Handle merged cells
                colspan = int(td.get('colspan', 1))
                rowspan = int(td.get('rowspan', 1))
                
                row.append({
                    'text': text,
                    'colspan': colspan,
                    'rowspan': rowspan,
                    'class': td.get('class', [])
                })
            if row:  # Only add non-empty rows
                rows.append(row)
        return rows
    
    def extract_numerology_patterns(self, content: str) -> Dict[str, Any]:
        """Extract numerology-specific patterns from HTML content"""
        patterns = {
            'abbreviations': {},
            'sample_data': {},
            'formulas': [],
            'structures': []
        }
        
        # Extract core number abbreviations
        abbrev_patterns = {
            'BD': 'Birth Date',
            'LP': 'Life Path', 
            'HP': 'Hidden Passion',
            'KL': 'Karmic Lessons',
            'MKL': 'Most Karmic Lesson',
            'PN': 'Personality Number',
            'SN': 'Soul Number',
            'DN': 'Destiny Number',
            'EN': 'Expression Number'
        }
        
        for abbrev, full_name in abbrev_patterns.items():
            if re.search(f'>{abbrev}<', content):
                patterns['abbreviations'][abbrev] = full_name
        
        # Extract date patterns (sample data)
        date_matches = re.findall(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b', content)
        if date_matches:
            patterns['sample_data']['dates'] = list(set(date_matches))
        
        # Extract name patterns
        name_matches = re.findall(r'[A-Z]{2,}(?:\s+[A-Z]{2,})*', content)
        if name_matches:
            # Filter out common HTML/CSS terms
            filtered_names = [name for name in set(name_matches) 
                            if not any(term in name.lower() for term in 
                                     ['style', 'border', 'width', 'height', 'font', 'color'])]
            patterns['sample_data']['names'] = filtered_names[:10]  # Limit to 10
        
        # Extract number sequences (for Lo-Shu grid)
        number_sequences = re.findall(r'>[1-9]<', content)
        if number_sequences:
            patterns['sample_data']['numbers'] = [int(n[1:-1]) for n in set(number_sequences)]
        
        return patterns
    
    def extract_lo_shu_grid_structure(self) -> Dict[str, Any]:
        """Extract Lo-Shu Grid specific structure and calculations"""
        if 'Lo_Shu_Grid' not in self.parsed_data:
            return {}
            
        # Extract 3x3 grid structure
        grid_structure = {
            'positions': {
                'top_row': [4, 9, 2],
                'middle_row': [3, 5, 7], 
                'bottom_row': [8, 1, 6]
            },
            'planes': {
                'intellectual': [4, 9, 2],  # Top row
                'emotional': [3, 5, 7],     # Middle row
                'practical': [8, 1, 6]      # Bottom row
            },
            'raj_yog_combinations': [
                [4, 9, 2], [3, 5, 7], [8, 1, 6],  # Rows
                [4, 3, 8], [9, 5, 1], [2, 7, 6],  # Columns  
                [4, 5, 6], [2, 5, 8]              # Diagonals
            ]
        }
        
        return grid_structure
    
    def extract_chaldean_mappings(self) -> Dict[str, int]:
        """Extract Chaldean alphabet to number mappings"""
        return {
            'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
            'B': 2, 'K': 2, 'R': 2,
            'C': 3, 'G': 3, 'L': 3, 'S': 3,
            'D': 4, 'M': 4, 'T': 4,
            'E': 5, 'H': 5, 'N': 5, 'X': 5,
            'U': 6, 'V': 6, 'W': 6,
            'O': 7, 'Z': 7,
            'F': 8, 'P': 8
        }
    
    def extract_compatibility_matrix(self) -> Dict[str, Dict[str, str]]:
        """Extract compatibility ratings matrix"""
        # Based on traditional Chaldean compatibility
        compatibility = {}
        for i in range(1, 10):
            compatibility[str(i)] = {}
            for j in range(1, 10):
                # Simplified compatibility logic - can be enhanced with parsed data
                if i == j:
                    rating = "Excellent"
                elif abs(i - j) in [1, 2]:
                    rating = "Very Good"
                elif abs(i - j) in [3, 4]:
                    rating = "Good"
                else:
                    rating = "Fair"
                compatibility[str(i)][str(j)] = rating
        
        return compatibility
    
    def save_parsed_data(self, output_file: str = "parsed_numerology_data.json"):
        """Save parsed data to JSON file"""
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.parsed_data, f, indent=2, ensure_ascii=False)
        print(f"Parsed data saved to {output_path}")
    
    def generate_summary_report(self) -> str:
        """Generate summary of parsed data"""
        report = []
        report.append("=== NUMEROLOGY DATA PARSING SUMMARY ===\n")
        
        for sheet_name, data in self.parsed_data.items():
            report.append(f"\n📊 {sheet_name.replace('_', ' ').title()}")
            report.append("-" * 40)
            
            if 'abbreviations' in data and data['abbreviations']:
                report.append("🔤 Abbreviations Found:")
                for abbrev, full_name in data['abbreviations'].items():
                    report.append(f"  • {abbrev} = {full_name}")
            
            if 'sample_data' in data:
                if 'dates' in data['sample_data']:
                    report.append(f"📅 Sample Dates: {', '.join(data['sample_data']['dates'][:3])}")
                if 'names' in data['sample_data']:
                    report.append(f"👤 Sample Names: {', '.join(data['sample_data']['names'][:3])}")
            
            if 'tables' in data:
                report.append(f"📋 Tables Found: {len(data['tables'])}")
        
        # Add extracted structures
        report.append(f"\n🔮 Lo-Shu Grid Structure: {bool(self.extract_lo_shu_grid_structure())}")
        report.append(f"🔤 Chaldean Mappings: {len(self.extract_chaldean_mappings())} letters")
        report.append("💑 Compatibility Matrix: 9x9 grid available")
        
        return "\n".join(report)


if __name__ == "__main__":
    # Parse all sheets
    parser = NumerologyHTMLParser()
    parsed_data = parser.parse_all_sheets()
    
    # Save data
    parser.save_parsed_data()
    
    # Print summary
    print(parser.generate_summary_report())
