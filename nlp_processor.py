#!/usr/bin/env python3
"""
Natural Language Processing Module for Numerology Form Normalization

This module handles:
1. Text normalization (fixing typos, standardizing format)
2. Natural language input processing 
3. Name cleaning and standardization
4. Date parsing from natural language
"""

import re
import textdistance
from typing import Tuple, Optional, Dict
from datetime import datetime
from dateutil.parser import parse as parse_date
import logging

class NLPProcessor:
    """
    Natural Language Processor for numerology form inputs
    Handles typos, natural language, and text normalization
    """
    
    def __init__(self):
        """Initialize the NLP processor with common patterns and dictionaries."""
        
        # Common name patterns and corrections
        self.name_corrections = {
            # Common typos in names
            'jhon': 'john',
            'mike': 'michael',
            'bob': 'robert',
            'jim': 'james',
            'bill': 'william',
            'rick': 'richard',
            'dick': 'richard',
            'tom': 'thomas',
            'tony': 'anthony',
            'chris': 'christopher',
            'dave': 'david',
            'joe': 'joseph',
            'rob': 'robert',
            'steve': 'steven',
            'matt': 'matthew',
            'dan': 'daniel',
            'sam': 'samuel',
            'nick': 'nicholas',
            # Add more as needed
        }
        
        # Common words to remove from names
        self.stop_words = {
            'mr', 'mrs', 'ms', 'miss', 'dr', 'prof', 'professor', 
            'sir', 'madam', 'junior', 'jr', 'senior', 'sr', 'iii', 'ii'
        }
        
        # Date parsing patterns
        self.date_patterns = [
            r'(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{4})',  # MM/DD/YYYY
            r'(\d{4})[\/\-\.](\d{1,2})[\/\-\.](\d{1,2})',  # YYYY/MM/DD
            r'(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2})',  # MM/DD/YY
        ]
        
        # Month name mappings
        self.month_names = {
            'january': 1, 'jan': 1, 'february': 2, 'feb': 2, 'march': 3, 'mar': 3,
            'april': 4, 'apr': 4, 'may': 5, 'june': 6, 'jun': 6, 'july': 7, 'jul': 7,
            'august': 8, 'aug': 8, 'september': 9, 'sep': 9, 'sept': 9,
            'october': 10, 'oct': 10, 'november': 11, 'nov': 11, 'december': 12, 'dec': 12
        }
        
        # Natural language patterns
        self.birth_patterns = [
            r'born\s+(?:on\s+)?(.+)',
            r'birth\s+(?:date\s+)?(?:is\s+)?(.+)',
            r'birthday\s+(?:is\s+)?(.+)',
            r'dob\s+(?:is\s+)?(.+)',
            r'my\s+birthday\s+(?:is\s+)?(.+)',
            r'i\s+was\s+born\s+(?:on\s+)?(.+)',
        ]
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def normalize_name(self, name_input: str) -> str:
        """
        Normalize name input by fixing typos and standardizing format.
        
        Args:
            name_input: Raw name input from user
            
        Returns:
            Cleaned and normalized name
        """
        if not name_input or not isinstance(name_input, str):
            return ""
        
        # Convert to lowercase for processing
        name = name_input.lower().strip()
        
        # Remove extra whitespace and special characters
        name = re.sub(r'[^a-z\s]', '', name)
        name = re.sub(r'\s+', ' ', name)
        
        # Split into words
        words = name.split()
        normalized_words = []
        
        for word in words:
            # Skip stop words
            if word in self.stop_words:
                continue
            
            # Check for direct corrections
            if word in self.name_corrections:
                normalized_words.append(self.name_corrections[word])
            else:
                # Check for typos using text distance
                corrected = self._correct_typo(word)
                normalized_words.append(corrected)
        
        # Join and capitalize properly
        result = ' '.join(normalized_words)
        return self._capitalize_name(result)
    
    def _correct_typo(self, word: str) -> str:
        """
        Correct typos in a single word using fuzzy matching.
        
        Args:
            word: Word to check for typos
            
        Returns:
            Corrected word or original if no good match
        """
        if len(word) < 3:  # Don't correct very short words
            return word
        
        best_match = word
        best_score = 0.7  # Minimum similarity threshold
        
        # Check against known good names
        common_names = list(self.name_corrections.values()) + [
            'alexander', 'elizabeth', 'christopher', 'jennifer', 'michael', 'jessica',
            'william', 'ashley', 'david', 'sarah', 'richard', 'stephanie', 'joseph',
            'melissa', 'thomas', 'nicole', 'charles', 'patricia', 'john', 'kimberly',
            'daniel', 'deborah', 'matthew', 'rachel', 'anthony', 'carolyn', 'mark',
            'janet', 'donald', 'virginia', 'steven', 'maria', 'paul', 'catherine',
            'andrew', 'helen', 'joshua', 'frances', 'kenneth', 'ruth', 'kevin',
            'shirley', 'brian', 'barbara', 'george', 'amy', 'edward', 'kathleen',
            'ronald', 'dorothy', 'timothy', 'lisa', 'jason', 'nancy', 'jeffrey',
            'sandra', 'ryan', 'betty', 'jacob', 'anna', 'gary', 'cynthia',
        ]
        
        for name in common_names:
            # Use Jaro-Winkler similarity for better name matching
            similarity = textdistance.jaro_winkler(word, name)
            if similarity > best_score:
                best_score = similarity
                best_match = name
        
        return best_match
    
    def _capitalize_name(self, name: str) -> str:
        """
        Properly capitalize name(s).
        
        Args:
            name: Name to capitalize
            
        Returns:
            Properly capitalized name
        """
        if not name:
            return name
        
        # Handle special cases like O'Connor, McDonald, etc.
        words = []
        for word in name.split():
            if "'" in word:
                # Handle O'Connor, D'Angelo, etc.
                parts = word.split("'")
                word = "'".join([part.capitalize() for part in parts])
            elif word.startswith('mc'):
                # Handle McDonald, McKenzie, etc.
                word = 'Mc' + word[2:].capitalize()
            else:
                word = word.capitalize()
            words.append(word)
        
        return ' '.join(words)
    
    def parse_birth_date(self, date_input: str) -> Optional[datetime]:
        """
        Parse birth date from natural language input.
        
        Args:
            date_input: Date input in various formats
            
        Returns:
            Parsed datetime object or None if parsing fails
        """
        if not date_input or not isinstance(date_input, str):
            return None
        
        # Clean the input
        date_input = date_input.strip().lower()
        
        # Remove common prefixes
        for pattern in self.birth_patterns:
            match = re.search(pattern, date_input, re.IGNORECASE)
            if match:
                date_input = match.group(1).strip()
                break
        
        # Try different parsing approaches
        try:
            # First try dateutil parser (handles many formats)
            parsed_date = parse_date(date_input, fuzzy=True)
            
            # Validate the date makes sense for a birth date
            current_year = datetime.now().year
            if 1900 <= parsed_date.year <= current_year:
                return parsed_date
            elif parsed_date.year < 100:  # Handle 2-digit years
                # Assume years 00-30 are 2000s, 31-99 are 1900s
                if parsed_date.year <= 30:
                    parsed_date = parsed_date.replace(year=parsed_date.year + 2000)
                else:
                    parsed_date = parsed_date.replace(year=parsed_date.year + 1900)
                return parsed_date
        
        except Exception as e:
            self.logger.debug(f"Date parsing failed with dateutil: {e}")
        
        # Try manual parsing with regex patterns
        for pattern in self.date_patterns:
            match = re.search(pattern, date_input)
            if match:
                try:
                    groups = match.groups()
                    if len(groups) == 3:
                        # Determine if it's MM/DD/YYYY or YYYY/MM/DD format
                        if len(groups[0]) == 4:  # YYYY/MM/DD
                            year, month, day = int(groups[0]), int(groups[1]), int(groups[2])
                        else:  # MM/DD/YYYY or MM/DD/YY
                            month, day, year = int(groups[0]), int(groups[1]), int(groups[2])
                            if year < 100:
                                year = year + 2000 if year <= 30 else year + 1900
                        
                        return datetime(year, month, day)
                except (ValueError, TypeError):
                    continue
        
        self.logger.warning(f"Could not parse date: {date_input}")
        return None
    
    def extract_name_and_date(self, text_input: str) -> Tuple[str, Optional[datetime]]:
        """
        Extract both name and birth date from natural language input.
        
        Args:
            text_input: Natural language input containing name and/or date
            
        Returns:
            Tuple of (normalized_name, parsed_date)
        """
        if not text_input:
            return "", None
        
        text = text_input.strip()
        name = ""
        birth_date = None
        
        # Look for birth date patterns first
        for pattern in self.birth_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                date_part = match.group(1).strip()
                birth_date = self.parse_birth_date(date_part)
                # Remove the date part from text to extract name
                text = re.sub(pattern, '', text, flags=re.IGNORECASE).strip()
                break
        
        # Clean up remaining text as name
        if text:
            # Remove common prefixes like "my name is", "i am", etc.
            text = re.sub(r'^(?:my\s+name\s+is\s+|i\s+am\s+|call\s+me\s+)', '', text, flags=re.IGNORECASE)
            name = self.normalize_name(text)
        
        return name, birth_date
    
    def validate_input(self, name: str, birth_date: Optional[datetime]) -> Dict[str, str]:
        """
        Validate normalized inputs and provide feedback.
        
        Args:
            name: Normalized name
            birth_date: Parsed birth date
            
        Returns:
            Dictionary with validation results and suggestions
        """
        validation = {
            'name_valid': bool(name and len(name) > 1),
            'date_valid': birth_date is not None,
            'suggestions': [],
            'warnings': []
        }
        
        if not validation['name_valid']:
            validation['suggestions'].append("Please provide a valid name (at least 2 characters)")
        
        if not validation['date_valid']:
            validation['suggestions'].append("Please provide a valid birth date (e.g., '1990-01-15' or 'January 15, 1990')")
        
        if birth_date:
            current_year = datetime.now().year
            if birth_date.year > current_year:
                validation['warnings'].append("Birth date appears to be in the future")
            elif birth_date.year < 1900:
                validation['warnings'].append("Birth date appears to be very old")
        
        return validation

def test_nlp_processor():
    """Test the NLP processor with various inputs."""
    processor = NLPProcessor()
    
    test_cases = [
        "My name is Jhon Doe and I was born on 15/01/1990",
        "call me mike, birthday is january 15 1985",
        "i am dr. robert smith born 1980-03-20",
        "elizabeth born march 10th 1995",
        "name: Dave, DOB: 12-25-1987",
        "christopher o'connor, december 1st 1992"
    ]
    
    print("🧪 Testing NLP Processor")
    print("=" * 50)
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\\nTest {i}: '{test_input}'")
        name, birth_date = processor.extract_name_and_date(test_input)
        validation = processor.validate_input(name, birth_date)
        
        print(f"  Name: '{name}'")
        print(f"  Date: {birth_date.strftime('%Y-%m-%d') if birth_date else 'None'}")
        print(f"  Valid: Name={validation['name_valid']}, Date={validation['date_valid']}")
        
        if validation['suggestions']:
            print(f"  Suggestions: {', '.join(validation['suggestions'])}")
        if validation['warnings']:
            print(f"  Warnings: {', '.join(validation['warnings'])}")

if __name__ == "__main__":
    test_nlp_processor()
