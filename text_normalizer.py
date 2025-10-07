"""
Natural Language Processing module for form normalization
Handles typos, natural language input, and text normalization for the numerology app
"""

import re
from typing import Dict, Optional, Tuple
from datetime import datetime
from dateutil.parser import parse as parse_date
from fuzzywuzzy import fuzz, process


class TextNormalizer:
    """Handles text normalization and typo correction for form inputs"""
    
    def __init__(self):
        # Common name corrections (typos -> correct)
        self.name_corrections = {
            'jhon': 'john',
            'micheal': 'michael',
            'catherina': 'catherine',
            'cristopher': 'christopher',
            'elizebeth': 'elizabeth',
            'willam': 'william',
            'robbert': 'robert',
            'stephany': 'stephanie',
            'brittney': 'brittany',
            'jeffery': 'jeffrey',
            'mathew': 'matthew',
            'nichole': 'nicole',
            'racheal': 'rachel',
            'rebeca': 'rebecca',
            'sephen': 'stephen',
            'tiffeny': 'tiffany',
        }
        
        # Common words to remove from names
        self.stopwords = {
            'mr', 'mrs', 'ms', 'dr', 'prof', 'sir', 'madam',
            'the', 'and', 'of', 'jr', 'sr', 'ii', 'iii', 'iv'
        }
        
        # Date format patterns
        self.date_patterns = [
            r'\b(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{4})\b',  # MM/DD/YYYY or DD/MM/YYYY
            r'\b(\d{4})[\/\-\.](\d{1,2})[\/\-\.](\d{1,2})\b',  # YYYY/MM/DD
            r'\b(\d{1,2})\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+(\d{4})\b',  # DD Month YYYY
            r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+(\d{1,2}),?\s+(\d{4})\b',  # Month DD, YYYY
        ]

    def normalize_name(self, raw_name: str) -> str:
        """
        Normalize a name by fixing typos and formatting
        
        Args:
            raw_name: Raw name input from user
            
        Returns:
            Normalized name
        """
        if not raw_name:
            return ""
        
        # Convert to lowercase for processing
        name = raw_name.lower().strip()
        
        # Remove extra spaces and special characters (except hyphens and apostrophes)
        name = re.sub(r'[^\w\s\'-]', '', name)
        name = re.sub(r'\s+', ' ', name)  # Multiple spaces to single space
        
        # Split into parts
        parts = name.split()
        normalized_parts = []
        
        for part in parts:
            # Skip stopwords
            if part in self.stopwords:
                continue
            
            # Apply corrections
            if part in self.name_corrections:
                part = self.name_corrections[part]
            
            # Capitalize properly
            if part:
                # Handle names with apostrophes (O'Connor, D'Angelo)
                if "'" in part:
                    subparts = part.split("'")
                    part = "'".join([sp.capitalize() for sp in subparts])
                # Handle hyphenated names (Mary-Jane)
                elif "-" in part:
                    subparts = part.split("-")
                    part = "-".join([sp.capitalize() for sp in subparts])
                else:
                    part = part.capitalize()
                
                normalized_parts.append(part)
        
        return " ".join(normalized_parts)

    def extract_date_from_text(self, text: str) -> Optional[datetime]:
        """
        Extract date from natural language text
        
        Args:
            text: Text that might contain a date
            
        Returns:
            Parsed datetime object or None
        """
        if not text:
            return None
        
        text = text.lower().strip()
        
        # Try dateutil parser first (handles many formats)
        try:
            # Clean common phrases
            text = re.sub(r'\b(born on|birth date|birthday|dob)\b', '', text)
            text = re.sub(r'\b(the|of)\b', '', text)
            text = text.strip()
            
            # Try parsing
            parsed_date = parse_date(text, fuzzy=True)
            
            # Validate reasonable birth date (between 1900 and current year)
            current_year = datetime.now().year
            if 1900 <= parsed_date.year <= current_year:
                return parsed_date
                
        except Exception:
            pass
        
        # Try regex patterns as fallback
        for pattern in self.date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    groups = match.groups()
                    if len(groups) == 3:
                        # Try different interpretations
                        for date_format in ["%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"]:
                            try:
                                date_str = "/".join(groups)
                                parsed_date = datetime.strptime(date_str, date_format)
                                if 1900 <= parsed_date.year <= datetime.now().year:
                                    return parsed_date
                            except ValueError:
                                continue
                except Exception:
                    continue
        
        return None

    def normalize_input(self, raw_input: str) -> Dict[str, Optional[str]]:
        """
        Attempt to extract both name and date from free-form input
        
        Args:
            raw_input: Free-form text input from user
            
        Returns:
            Dictionary with 'name' and 'date' keys
        """
        if not raw_input:
            return {"name": None, "date": None}
        
        # Try to extract date first
        extracted_date = self.extract_date_from_text(raw_input)
        
        # Remove date-like patterns from text to isolate name
        text_without_date = raw_input
        if extracted_date:
            # Remove the date portion
            for pattern in self.date_patterns:
                text_without_date = re.sub(pattern, '', text_without_date, flags=re.IGNORECASE)
        
        # Remove common date words
        date_words = ['born', 'birth', 'birthday', 'dob', 'date', 'on', 'the', 'of']
        for word in date_words:
            text_without_date = re.sub(r'\b' + word + r'\b', '', text_without_date, flags=re.IGNORECASE)
        
        # Extract and normalize name
        normalized_name = self.normalize_name(text_without_date)
        
        return {
            "name": normalized_name if normalized_name else None,
            "date": extracted_date.strftime("%Y-%m-%d") if extracted_date else None
        }

    def suggest_corrections(self, input_text: str, known_names: list = None) -> Dict[str, list]:
        """
        Suggest corrections for input text
        
        Args:
            input_text: User input text
            known_names: List of known names for fuzzy matching
            
        Returns:
            Dictionary with suggestions
        """
        suggestions = {
            "name_suggestions": [],
            "date_suggestions": [],
            "confidence": 0
        }
        
        if not input_text:
            return suggestions
        
        # Try to parse input
        parsed = self.normalize_input(input_text)
        
        # If we have known names, do fuzzy matching
        if known_names and parsed["name"]:
            matches = process.extract(parsed["name"], known_names, limit=3, scorer=fuzz.token_sort_ratio)
            suggestions["name_suggestions"] = [match[0] for match in matches if match[1] > 70]
        
        # Check for common name typos
        if parsed["name"]:
            name_parts = parsed["name"].lower().split()
            corrected_parts = []
            for part in name_parts:
                if part in self.name_corrections:
                    corrected_parts.append(self.name_corrections[part].capitalize())
                else:
                    corrected_parts.append(part.capitalize())
            
            corrected_name = " ".join(corrected_parts)
            if corrected_name != parsed["name"]:
                suggestions["name_suggestions"].insert(0, corrected_name)
        
        # Calculate confidence
        if parsed["name"] and parsed["date"]:
            suggestions["confidence"] = 90
        elif parsed["name"] or parsed["date"]:
            suggestions["confidence"] = 60
        else:
            suggestions["confidence"] = 20
        
        return suggestions


# Test function
def test_normalizer():
    """Test the text normalizer"""
    normalizer = TextNormalizer()
    
    test_cases = [
        "jhon smith born 15/03/1990",
        "micheal jordan 2/17/1963",
        "my name is elizebeth brown and i was born on march 5th 1985",
        "willam shakespear april 23 1564",
        "mr. robbert downey jr.",
        "dr. catherina martinez-jones",
    ]
    
    print("Testing Text Normalizer:")
    print("=" * 50)
    
    for test_input in test_cases:
        result = normalizer.normalize_input(test_input)
        suggestions = normalizer.suggest_corrections(test_input)
        
        print(f"Input: {test_input}")
        print(f"Name: {result['name']}")
        print(f"Date: {result['date']}")
        print(f"Confidence: {suggestions['confidence']}%")
        if suggestions['name_suggestions']:
            print(f"Name suggestions: {suggestions['name_suggestions']}")
        print("-" * 30)


if __name__ == "__main__":
    test_normalizer()
