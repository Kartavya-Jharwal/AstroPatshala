from typing import Dict, List, Tuple
from datetime import datetime
import re

class ChaldeanNumerology:
    """
    Chaldean Numerology Calculator
    
    Based on the ancient Babylonian system that assigns specific vibrational
    energies to numbers and letters. Uses the traditional Chaldean chart
    where number 9 is considered sacred and excluded from letter assignments.
    """
    
    # Chaldean letter-to-number mapping
    CHALDEAN_CHART = {
        'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
        'B': 2, 'K': 2, 'R': 2,
        'C': 3, 'G': 3, 'L': 3, 'S': 3,
        'D': 4, 'M': 4, 'T': 4,
        'E': 5, 'H': 5, 'N': 5,
        'U': 6, 'V': 6, 'W': 6, 'X': 6,
        'O': 7, 'Z': 7,
        'F': 8, 'P': 8
    }
    
    # Number meanings and interpretations
    NUMBER_MEANINGS = {
        1: {
            "traits": "Leadership, independence, pioneering spirit, originality",
            "description": "Natural leaders with strong willpower and determination. They are innovative, self-reliant, and have the ability to inspire others.",
            "challenges": "Can be too dominating, impatient, or self-centered",
            "strengths": "Initiative, confidence, creativity, leadership abilities"
        },
        2: {
            "traits": "Sensitivity, cooperation, diplomacy, intuition",
            "description": "Natural peacemakers who excel in partnerships and collaborative efforts. They are empathetic, gentle, and skilled at bringing harmony.",
            "challenges": "May be too sensitive, indecisive, or dependent on others",
            "strengths": "Cooperation, mediation, emotional intelligence, teamwork"
        },
        3: {
            "traits": "Creativity, expression, communication, artistic abilities",
            "description": "Natural entertainers and communicators with strong creative talents. They are optimistic, inspiring, and have a gift for self-expression.",
            "challenges": "Can be scattered, superficial, or overly talkative",
            "strengths": "Artistic talent, communication skills, optimism, inspiration"
        },
        4: {
            "traits": "Stability, practicality, hard work, organization",
            "description": "Natural builders who value security, order, and systematic approaches. They are reliable, methodical, and excellent at creating solid foundations.",
            "challenges": "May be too rigid, stubborn, or resistant to change",
            "strengths": "Reliability, organization, perseverance, practical skills"
        },
        5: {
            "traits": "Freedom, adaptability, adventure, curiosity",
            "description": "Natural explorers who crave variety and new experiences. They are versatile, progressive, and excellent at adapting to change.",
            "challenges": "Can be restless, irresponsible, or lack focus",
            "strengths": "Adaptability, versatility, progressive thinking, communication"
        },
        6: {
            "traits": "Harmony, responsibility, nurturing, service",
            "description": "Natural caregivers who are drawn to helping others and creating harmony. They are compassionate, responsible, and family-oriented.",
            "challenges": "May be too self-sacrificing, interfering, or perfectionist",
            "strengths": "Compassion, responsibility, healing abilities, artistic sense"
        },
        7: {
            "traits": "Intuition, spirituality, analysis, mystery",
            "description": "Natural seekers of truth with strong intuitive and analytical abilities. They are spiritual, introspective, and drawn to deeper meanings.",
            "challenges": "Can be too aloof, secretive, or pessimistic",
            "strengths": "Intuition, analytical skills, spiritual insight, research abilities"
        },
        8: {
            "traits": "Power, material success, ambition, authority",
            "description": "Natural executives with strong business acumen and leadership abilities. They are ambitious, efficient, and skilled at managing resources.",
            "challenges": "May be too materialistic, demanding, or workaholic",
            "strengths": "Business skills, leadership, efficiency, material success"
        },
        9: {
            "traits": "Universal love, compassion, completion, wisdom",
            "description": "Natural humanitarians with a broad perspective and deep compassion. They are wise, generous, and drawn to serving humanity.",
            "challenges": "Can be too emotional, impractical, or self-sacrificing",
            "strengths": "Compassion, wisdom, artistic abilities, humanitarian spirit"
        }
    }
    
    # Compound number meanings (11-99)
    COMPOUND_MEANINGS = {
        10: "Completion of a cycle, new beginnings, potential for leadership",
        11: "Intuition, spiritual insight, master number of illumination",
        12: "Sacrifice, trials, spiritual testing and growth",
        13: "Transformation through upheaval, death and rebirth",
        14: "Movement, change, freedom from limitations",
        15: "Material success, love of luxury, magnetic personality",
        16: "Destruction of the old, spiritual awakening, tower of destruction",
        17: "Immortality, spiritual strength, the eight-pointed star of Venus",
        18: "Materialism vs spirituality, deception, quarrels with family",
        19: "Success, happiness, fulfillment, the sun of achievement",
        20: "Awakening, spiritual calling, the judgment of rebirth",
        21: "Success, advancement, the crown of achievement",
        22: "Submission, suffering, warning of illusion and false hopes",
        23: "Protection, help from superiors, the royal star of the lion",
        24: "Love, marriage, assistance from others, Venus love",
        25: "Learning through experience, strength gained through struggle",
        26: "Partnership, cooperation, material success through others",
        27: "Courage, mental strength, scepter of command",
        28: "Written agreements, legal matters, partnerships",
        29: "Uncertainty, treachery, deception from others",
        30: "Contemplation, retreat, thoughtful consideration",
        31: "Isolation, withdrawal, misunderstood genius",
        32: "Communication, networking, helpful connections"
    }
    
    def calculate_name_number(self, name: str) -> Tuple[int, int, List[int]]:
        """
        Calculate the name number using Chaldean numerology
        
        Args:
            name: The name to calculate (cleaned of special characters)
            
        Returns:
            Tuple of (compound_number, reduced_number, letter_values)
        """
        # Clean the name - remove spaces and special characters, convert to uppercase
        clean_name = re.sub(r'[^A-Za-z]', '', name.upper())
        
        letter_values = []
        total = 0
        
        for letter in clean_name:
            if letter in self.CHALDEAN_CHART:
                value = self.CHALDEAN_CHART[letter]
                letter_values.append(value)
                total += value
        
        # Reduce to single digit unless it's a master number or significant compound
        compound_number = total
        reduced_number = self.reduce_to_single_digit(total)
        
        return compound_number, reduced_number, letter_values
    
    def calculate_birth_number(self, birth_date: datetime) -> int:
        """
        Calculate the birth number (day of birth)
        
        Args:
            birth_date: The birth date
            
        Returns:
            The birth day as the birth number
        """
        return birth_date.day
    
    def calculate_destiny_number(self, birth_date: datetime) -> Tuple[int, int]:
        """
        Calculate the destiny number from full birth date
        
        Args:
            birth_date: The birth date
            
        Returns:
            Tuple of (compound_destiny, reduced_destiny)
        """
        day = birth_date.day
        month = birth_date.month
        year = birth_date.year
        
        total = day + month + year
        compound_destiny = total
        reduced_destiny = self.reduce_to_single_digit(total)
        
        return compound_destiny, reduced_destiny
    
    def reduce_to_single_digit(self, number: int) -> int:
        """
        Reduce a number to single digit (1-9)
        Special handling for master numbers 11, 22, 33
        """
        while number > 9:
            if number in [11, 22, 33]:  # Master numbers
                break
            number = sum(int(digit) for digit in str(number))
        return number
    
    def get_number_interpretation(self, number: int) -> Dict:
        """
        Get the interpretation for a given number
        
        Args:
            number: The number to interpret (1-9)
            
        Returns:
            Dictionary with traits, description, challenges, and strengths
        """
        return self.NUMBER_MEANINGS.get(number, {
            "traits": "Unknown number",
            "description": "No interpretation available",
            "challenges": "Unknown",
            "strengths": "Unknown"
        })
    
    def get_compound_interpretation(self, number: int) -> str:
        """
        Get interpretation for compound numbers
        
        Args:
            number: The compound number
            
        Returns:
            String interpretation of the compound number
        """
        return self.COMPOUND_MEANINGS.get(number, "Special compound number with unique energy")
    
    def calculate_compatibility(self, number1: int, number2: int) -> Dict:
        """
        Calculate basic compatibility between two numbers
        
        Args:
            number1: First number
            number2: Second number
            
        Returns:
            Dictionary with compatibility information
        """
        # Simplistic compatibility matrix based on traditional numerology
        compatible_pairs = {
            1: [1, 5, 7], 2: [2, 4, 8], 3: [3, 6, 9],
            4: [2, 4, 8], 5: [1, 5, 7], 6: [3, 6, 9],
            7: [1, 5, 7], 8: [2, 4, 8], 9: [3, 6, 9]
        }
        
        is_compatible = number2 in compatible_pairs.get(number1, [])
        
        compatibility_descriptions = {
            (1, 1): "Two leaders - can work well together but may clash over control",
            (1, 5): "Great combination - leadership with freedom and adventure",
            (1, 7): "Good balance - leadership with spiritual insight",
            (2, 2): "Harmonious pair - mutual understanding and cooperation",
            (2, 4): "Stable partnership - sensitivity with practical foundation",
            (2, 8): "Powerful combination - diplomacy with business acumen",
            (3, 3): "Creative explosion - inspiring but may lack focus",
            (3, 6): "Artistic harmony - creativity with nurturing support",
            (3, 9): "Humanitarian creativity - expression serving higher purpose",
            (4, 4): "Solid foundation - practical and reliable partnership",
            (5, 5): "Adventure together - exciting but may lack stability",
            (6, 6): "Caring and harmonious - deeply nurturing relationship",
            (7, 7): "Spiritual connection - deep understanding but may be isolated",
            (8, 8): "Power couple - material success but may compete",
            (9, 9): "Humanitarian mission - serving the world together"
        }
        
        key = (min(number1, number2), max(number1, number2))
        description = compatibility_descriptions.get(key, "Unique combination with its own special energy")
        
        return {
            "compatible": is_compatible,
            "description": description,
            "rating": "High" if is_compatible else "Moderate"
        }
    
    def generate_full_report(self, name: str, birth_date: datetime) -> Dict:
        """
        Generate a comprehensive Chaldean numerology report
        
        Args:
            name: The person's name
            birth_date: The person's birth date
            
        Returns:
            Complete numerology report dictionary
        """
        # Calculate all numbers
        name_compound, name_reduced, letter_values = self.calculate_name_number(name)
        birth_number = self.calculate_birth_number(birth_date)
        destiny_compound, destiny_reduced = self.calculate_destiny_number(birth_date)
        
        # Get interpretations
        name_interpretation = self.get_number_interpretation(name_reduced)
        birth_interpretation = self.get_number_interpretation(birth_number)
        destiny_interpretation = self.get_number_interpretation(destiny_reduced)
        
        # Calculate compatibility between key numbers
        name_birth_compatibility = self.calculate_compatibility(name_reduced, birth_number)
        name_destiny_compatibility = self.calculate_compatibility(name_reduced, destiny_reduced)
        
        report = {
            "personal_info": {
                "name": name,
                "birth_date": birth_date.strftime("%B %d, %Y"),
                "calculation_date": datetime.now().strftime("%B %d, %Y")
            },
            "name_number": {
                "compound": name_compound,
                "reduced": name_reduced,
                "letter_breakdown": list(zip(list(re.sub(r'[^A-Za-z]', '', name.upper())), letter_values)),
                "interpretation": name_interpretation,
                "compound_meaning": self.get_compound_interpretation(name_compound) if name_compound > 9 else None
            },
            "birth_number": {
                "number": birth_number,
                "interpretation": birth_interpretation
            },
            "destiny_number": {
                "compound": destiny_compound,
                "reduced": destiny_reduced,
                "interpretation": destiny_interpretation,
                "compound_meaning": self.get_compound_interpretation(destiny_compound) if destiny_compound > 9 else None
            },
            "compatibility": {
                "name_birth": name_birth_compatibility,
                "name_destiny": name_destiny_compatibility
            },
            "summary": {
                "life_path_theme": destiny_interpretation["description"],
                "personality_core": name_interpretation["description"],
                "natural_gifts": birth_interpretation["strengths"],
                "key_challenges": name_interpretation["challenges"]
            }
        }
        
        return report
