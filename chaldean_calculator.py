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
    
    # Chaldean letter-to-number mapping (corrected as per PDF)
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
    
    # Vowels and Consonants classification
    VOWELS = {'A', 'E', 'I', 'O', 'U'}
    CONSONANTS = {'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z'}

    # If the PDF specifies special handling for Y/W, vowels, or other letters, add logic here
    # For example, if Y is only counted as a vowel in certain positions, add that logic in calculation
    
    # Number meanings and interpretations (enhanced as per PDF)
    NUMBER_MEANINGS = {
        1: {
            "traits": "Independence, leadership, originality, pioneering spirit, initiative",
            "description": "Number 1 represents the beginning, the source of all creation. People with this number are natural born leaders who possess strong willpower, determination, and the ability to inspire others. They are innovative, self-reliant, and have a powerful drive to succeed. They prefer to lead rather than follow and are often pioneers in their chosen fields.",
            "challenges": "Can be overly aggressive, dominating, impatient, or self-centered. May struggle with accepting help from others or working in teams.",
            "strengths": "Strong leadership abilities, independence, creativity, initiative, confidence, and the ability to start new ventures.",
            "career": "Excellent in executive positions, entrepreneurship, politics, military, sales, and any field requiring leadership and initiative.",
            "relationships": "Needs a partner who respects their independence and supports their ambitions. Can be loyal but may struggle with compromise.",
            "health": "Generally strong constitution but may suffer from stress-related issues due to their driven nature. Should watch blood pressure and heart conditions."
        },
        2: {
            "traits": "Cooperation, diplomacy, sensitivity, partnership, peace-making",
            "description": "Number 2 represents duality, balance, and cooperation. These individuals are natural peacemakers who excel in partnerships and collaborative efforts. They are empathetic, gentle, and skilled at bringing harmony to situations. They have strong intuition and emotional intelligence, making them excellent mediators and counselors.",
            "challenges": "May be overly sensitive, indecisive, dependent on others, or prone to mood swings. Can lack confidence in their own abilities.",
            "strengths": "Cooperation, mediation skills, emotional intelligence, diplomacy, teamwork, and the ability to work well with others.",
            "career": "Excel in counseling, diplomacy, teaching, nursing, social work, customer service, and any field requiring teamwork and interpersonal skills.",
            "relationships": "Natural partners who thrive in loving, supportive relationships. They are caring, loyal, and devoted to their loved ones.",
            "health": "May be prone to nervous disorders, digestive issues, and stress-related ailments. Need emotional stability for good health."
        },
        3: {
            "traits": "Creativity, communication, expression, optimism, artistic talent",
            "description": "Number 3 represents creativity, self-expression, and joy. These individuals are natural entertainers and communicators with strong creative talents. They are optimistic, inspiring, and have a gift for self-expression through words, art, or performance. They bring joy and inspiration to others through their enthusiasm and creativity.",
            "challenges": "Can be scattered, superficial, overly talkative, or prone to exaggeration. May lack focus and discipline in pursuing goals.",
            "strengths": "Artistic talent, communication skills, optimism, creativity, inspiration, and the ability to motivate others.",
            "career": "Excel in arts, entertainment, writing, speaking, teaching, advertising, and any field requiring creativity and communication.",
            "relationships": "Charming and sociable partners who bring joy and excitement to relationships. Need partners who appreciate their creative nature.",
            "health": "Generally healthy but may suffer from throat, respiratory issues, or nervous exhaustion from overactivity."
        },
        4: {
            "traits": "Stability, practicality, hard work, organization, reliability",
            "description": "Number 4 represents stability, order, and hard work. These individuals are natural builders who value security, structure, and systematic approaches. They are reliable, methodical, and excellent at creating solid foundations for themselves and others. They have strong work ethics and prefer practical, tangible results.",
            "challenges": "May be too rigid, stubborn, resistant to change, or overly focused on material security. Can be seen as boring or inflexible.",
            "strengths": "Reliability, organization, perseverance, practical skills, loyalty, and the ability to build lasting structures.",
            "career": "Excel in construction, engineering, accounting, banking, real estate, administration, and any field requiring attention to detail and systematic work.",
            "relationships": "Loyal and dependable partners who provide stability and security. May need to work on expressing emotions and being more flexible.",
            "health": "Generally robust health but may suffer from issues related to bones, joints, or digestive system. Should maintain regular routines."
        },
        5: {
            "traits": "Freedom, adventure, versatility, curiosity, progressive thinking",
            "description": "Number 5 represents freedom, change, and adventure. These individuals are natural explorers who crave variety and new experiences. They are versatile, progressive, and excellent at adapting to change. They have strong communication skills and are drawn to travel, learning, and experiencing all that life has to offer.",
            "challenges": "Can be restless, irresponsible, inconsistent, or lack focus. May have difficulty with commitment and routine.",
            "strengths": "Adaptability, versatility, progressive thinking, communication skills, and the ability to inspire change in others.",
            "career": "Excel in travel, sales, journalism, marketing, entertainment, consulting, and any field requiring flexibility and communication.",
            "relationships": "Need freedom and variety in relationships. Exciting partners but may struggle with long-term commitment without understanding.",
            "health": "Generally healthy but may suffer from nervous disorders, addiction issues, or accidents due to their adventurous nature."
        },
        6: {
            "traits": "Responsibility, nurturing, service, harmony, family-oriented",
            "description": "Number 6 represents love, responsibility, and service to others. These individuals are natural caregivers who are drawn to helping others and creating harmony. They are compassionate, responsible, and family-oriented. They have strong healing abilities and are often found in service professions.",
            "challenges": "May be overly self-sacrificing, interfering, perfectionist, or prone to worry. Can become overwhelmed by others' problems.",
            "strengths": "Compassion, responsibility, healing abilities, artistic sense, and the ability to create harmony and beauty.",
            "career": "Excel in healthcare, counseling, teaching, social work, interior design, and any field involving service to others.",
            "relationships": "Devoted and caring partners who prioritize family and home. May need to balance giving with receiving in relationships.",
            "health": "May suffer from stress-related issues due to taking on others' burdens. Should focus on self-care and emotional balance."
        },
        7: {
            "traits": "Spirituality, analysis, intuition, mystery, wisdom",
            "description": "Number 7 represents spirituality, introspection, and the search for truth. These individuals are natural seekers with strong intuitive and analytical abilities. They are spiritual, mysterious, and drawn to deeper meanings and hidden truths. They often have psychic abilities and strong connection to the spiritual realm.",
            "challenges": "Can be too aloof, secretive, pessimistic, or isolated. May struggle with practical matters and emotional expression.",
            "strengths": "Intuition, analytical skills, spiritual insight, research abilities, and the capacity for deep understanding.",
            "career": "Excel in research, spirituality, psychology, science, writing, and any field requiring deep analysis and intuitive insight.",
            "relationships": "Need partners who understand their need for solitude and spiritual growth. Can be deeply loyal but may struggle with emotional intimacy.",
            "health": "May suffer from nervous disorders, digestive issues, or mental health challenges. Need quiet time and spiritual practices for wellness."
        },
        8: {
            "traits": "Material success, power, ambition, authority, business acumen",
            "description": "Number 8 represents material success, power, and achievement in the physical world. These individuals are natural executives with strong business acumen and leadership abilities. They are ambitious, efficient, and skilled at managing resources and people. They have strong drive for material success and recognition.",
            "challenges": "May be too materialistic, demanding, workaholic, or ruthless in pursuit of success. Can neglect relationships and spiritual growth.",
            "strengths": "Business skills, leadership, efficiency, material success, and the ability to organize and manage large enterprises.",
            "career": "Excel in business, finance, real estate, politics, law, and any field requiring executive ability and material focus.",
            "relationships": "May struggle to balance career and relationships. Need partners who understand their ambitions and support their goals.",
            "health": "May suffer from stress-related issues, heart problems, or high blood pressure due to intense focus on achievement."
        },
        9: {
            "traits": "Universal love, compassion, completion, wisdom, humanitarian spirit",
            "description": "Number 9 represents completion, universal love, and service to humanity. These individuals are natural humanitarians with a broad perspective and deep compassion. They are wise, generous, and drawn to serving the greater good. They have strong artistic abilities and often work for causes larger than themselves.",
            "challenges": "Can be too emotional, impractical, self-sacrificing, or disappointed when others don't share their idealism.",
            "strengths": "Compassion, wisdom, artistic abilities, humanitarian spirit, and the ability to inspire others toward higher purposes.",
            "career": "Excel in humanitarian work, arts, teaching, healing, philanthropy, and any field serving the greater good of humanity.",
            "relationships": "Loving and generous partners who care deeply about others. May need partners who share their humanitarian values.",
            "health": "May suffer from emotional stress due to caring too much about world problems. Need to balance giving with self-care."
        }
    }
    
    # Compound number meanings (expanded as per PDF)
    COMPOUND_MEANINGS = {
        10: "The Wheel of Fortune - Completion of a cycle, new beginnings, rise and fall of fortune. Represents honor, faith, and rise in life with potential for great success.",
        11: "The Clenched Fist - Master number of intuition and spiritual insight. Illumination through trial and error. Represents hidden trials, treachery, and the need for faith.",
        12: "The Hanged Man - Sacrifice, trials, spiritual testing and growth. Represents anxiety, suffering, and sacrifice for others. Often indicates a life of service and spiritual development.",
        13: "Death and Rebirth - Transformation through upheaval, death and rebirth. Often considered unlucky but represents necessary change and regeneration. Power of reconstruction.",
        14: "Temperance - Movement, change, freedom from limitations. Represents risk, danger, and the need for caution. Often involves speculation and uncertain ventures.",
        15: "The Devil - Material success, love of luxury, magnetic personality. Represents eloquence, commerce, and material gain. Strong influence over others but potential for misuse of power.",
        16: "The Tower - Destruction of the old, spiritual awakening, tower of destruction. Represents sudden and unexpected events, accidents, and the fall of previously secure positions.",
        17: "The Star - Immortality, spiritual strength, the eight-pointed star of Venus. Represents love, peace, and hope. Often called the 'Star of the Magi' - highly spiritual number.",
        18: "The Moon - Materialism vs spirituality, deception, quarrels with family. Represents illusion, deception, and hidden enemies. Warns against treachery and false friends.",
        19: "The Sun - Success, happiness, fulfillment, the sun of achievement. Represents victory, success, and honor. One of the most fortunate numbers indicating happiness and success.",
        20: "Judgment - Awakening, spiritual calling, the judgment of rebirth. Represents new judgment, renewal, and spiritual awakening. Often indicates a calling to serve others.",
        21: "The Crown of the Magi - Success, advancement, the crown of achievement. Represents advancement, honors, and general success. Victory through personal effort and merit.",
        22: "The Fool - Master number of submission, suffering, warning of illusion and false hopes. Represents blind folly, errors in judgment, and the need for caution.",
        23: "The Royal Star of the Lion - Protection, help from superiors, the royal star of the lion. Represents success, help from others, and protection from those in authority.",
        24: "Venus Love - Love, marriage, assistance from others. Represents love, money, and help from those of the opposite sex. Favorable for artistic and creative pursuits.",
        25: "Wisdom Gained Through Experience - Learning through experience, strength gained through struggle. Represents learning through trial and error, strength through adversity.",
        26: "Partnerships - Partnership, cooperation, material success through others. Represents teamwork, cooperation, and success through joint efforts with others.",
        27: "The Sceptre - Courage, mental strength, scepter of command. Represents strength, courage, and the power to command others. Leadership through mental superiority.",
        28: "The Trusting Fool - Written agreements, legal matters, partnerships. Represents trust in others that may be misplaced. Caution needed in partnerships and legal matters.",
        29: "The Grave of Anxiety - Uncertainty, treachery, deception from others. Represents grave dangers, deception, and the potential for great difficulties.",
        30: "The Loner - Contemplation, retreat, thoughtful consideration. Represents loneliness, isolation, and the need for independent thought and action.",
        31: "The Void - Isolation, withdrawal, misunderstood genius. Represents someone ahead of their time, often misunderstood by others. Potential for great achievement if perseverance is maintained.",
        32: "Communication - Communication, networking, helpful connections. Represents the power of words, good counsel, and beneficial connections with others.",
        33: "The Master Teacher - Master number representing the teacher of teachers. Highest level of spiritual development and service to humanity.",
        34: "The Broken Wing - Represents struggles and limitations, but with potential for overcoming through persistence.",
        35: "The Beautiful Garden - Represents beauty, harmony, and the fruits of labor. Success through creative efforts.",
        36: "The Warrior - Represents strength, courage, and the ability to overcome obstacles through determination.",
        37: "The Wanderer - Represents search for truth, spiritual journey, and the quest for higher knowledge.",
        38: "The Healer - Represents healing abilities, service to others, and the power to restore and regenerate.",
        39: "The Peacemaker - Represents diplomacy, mediation, and the ability to bring harmony to difficult situations.",
        40: "The Foundation - Represents solid foundations, practical achievements, and lasting success through hard work.",
        41: "The Reformer - Represents the drive to improve and reform existing systems and structures.",
        42: "The Visionary - Represents foresight, planning, and the ability to see future possibilities.",
        43: "The Messenger - Represents communication, teaching, and the spreading of important information.",
        44: "The Master Builder - Master number representing the ability to build lasting structures and institutions.",
        45: "The Explorer - Represents adventure, discovery, and the courage to venture into unknown territories.",
        46: "The Nurturer - Represents caring, healing, and the ability to provide comfort and support to others.",
        47: "The Mystic - Represents spiritual insight, intuition, and connection to higher realms of consciousness.",
        48: "The Organizer - Represents efficiency, management, and the ability to bring order out of chaos."
    }
    
    def calculate_name_number(self, name: str) -> Tuple[int, int, List[int]]:
        """
        Calculate the name number using Chaldean numerology (enhanced PDF rules)
        - Only letters A-Z are counted
        - Each letter has specific vibrational value
        - Compound number is the sum before reduction
        - Reduced number is the final single digit (preserving master numbers 11, 22, 33)
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
        
        compound_number = total
        # Use authentic Chaldean reduction method from Excel formulas
        reduced_number = self.chaldean_reduce(total)
        
        return compound_number, reduced_number, letter_values
    
    def calculate_vowel_number(self, name: str) -> Tuple[int, int]:
        """
        Calculate the vowel number (Soul/Heart's Desire number)
        Represents inner desires, motivations, and what the soul craves
        """
        clean_name = re.sub(r'[^A-Za-z]', '', name.upper())
        vowel_total = 0
        
        for letter in clean_name:
            if letter in self.VOWELS and letter in self.CHALDEAN_CHART:
                vowel_total += self.CHALDEAN_CHART[letter]
        
        compound_vowel = vowel_total
        reduced_vowel = self.chaldean_reduce(vowel_total)
        
        return compound_vowel, reduced_vowel
    
    def calculate_consonant_number(self, name: str) -> Tuple[int, int]:
        """
        Calculate the consonant number (Personality number)
        Represents outer personality, how others see you
        """
        clean_name = re.sub(r'[^A-Za-z]', '', name.upper())
        consonant_total = 0
        
        for letter in clean_name:
            if letter in self.CONSONANTS and letter in self.CHALDEAN_CHART:
                consonant_total += self.CHALDEAN_CHART[letter]
        
        compound_consonant = consonant_total
        reduced_consonant = self.chaldean_reduce(consonant_total)
        
        return compound_consonant, reduced_consonant
    
    def calculate_birth_number(self, birth_date: datetime) -> int:
        """
        Calculate the birth number (day of birth)
        In Chaldean numerology, this represents natural talents and abilities
        """
        day = birth_date.day
        if day > 9:
            return self.chaldean_reduce(day)
        return day
    
    def calculate_destiny_number(self, birth_date: datetime) -> Tuple[int, int]:
        """
        Calculate the destiny number from full birth date (enhanced PDF rules)
        Add all digits of day, month, and year together, then reduce
        Example: 24-07-1985: 2+4+0+7+1+9+8+5 = 36 -> 3+6 = 9
        This represents life path and ultimate purpose
        """
        date_string = birth_date.strftime('%d%m%Y')
        digits = [int(d) for d in date_string]
        total = sum(digits)
        
        compound_destiny = total
        reduced_destiny = self.chaldean_reduce(total)
        
        return compound_destiny, reduced_destiny
    
    def calculate_life_stage_numbers(self, birth_date: datetime) -> Dict:
        """
        Calculate the three life stage numbers based on birth date
        These represent different periods of life and their influences
        """
        month = birth_date.month
        day = birth_date.day
        year = birth_date.year
        
        # First Life Stage (0-28/35 years) - based on month
        first_stage = self.chaldean_reduce(month)
        
        # Second Life Stage (28/35-56 years) - based on day
        second_stage = self.chaldean_reduce(day)
        
        # Third Life Stage (56+ years) - based on year
        year_sum = sum(int(digit) for digit in str(year))
        third_stage = self.chaldean_reduce(year_sum)
        
        return {
            "first_stage": first_stage,
            "second_stage": second_stage,
            "third_stage": third_stage
        }
    
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
    
    def chaldean_reduce(self, number: int) -> int:
        """
        Chaldean-specific number reduction using MOD operation
        Based on Excel formula: =MOD(number-1,9)+1
        This ensures the result is always 1-9, never 0
        
        This is the authentic Chaldean method extracted from the Excel file.
        Different from traditional digit summing.
        
        Args:
            number: The number to reduce
            
        Returns:
            Single digit 1-9 using Chaldean MOD method
        """
        if number <= 0:
            return 1
        
        # Handle master numbers first (preserve them as-is)
        if number in [11, 22, 33]:
            return number
        
        # Chaldean reduction: MOD(number-1, 9) + 1
        # This is the authentic Chaldean method from the Excel
        return ((number - 1) % 9) + 1
    
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
    
    def calculate_personal_year(self, birth_date: datetime, year: int = None) -> int:
        """
        Calculate the personal year number for a specific year
        This indicates the general theme and opportunities for that year
        """
        if year is None:
            year = datetime.now().year
        
        month = birth_date.month
        day = birth_date.day
        
        # Add birth month + birth day + current year
        total = month + day + year
        return self.chaldean_reduce(total)
    
    def calculate_karmic_debt_numbers(self, birth_date: datetime, name: str) -> List[int]:
        """
        Identify karmic debt numbers (13, 14, 16, 19) in the person's chart
        These represent lessons to be learned in this lifetime
        """
        karmic_numbers = []
        
        # Check destiny number
        destiny_compound, _ = self.calculate_destiny_number(birth_date)
        if destiny_compound in [13, 14, 16, 19]:
            karmic_numbers.append(destiny_compound)
        
        # Check name number
        name_compound, _, _ = self.calculate_name_number(name)
        if name_compound in [13, 14, 16, 19]:
            karmic_numbers.append(name_compound)
        
        # Check birth number
        birth_day = birth_date.day
        if birth_day in [13, 14, 16, 19]:
            karmic_numbers.append(birth_day)
        
        return list(set(karmic_numbers))  # Remove duplicates
    
    def calculate_master_numbers(self, birth_date: datetime, name: str) -> List[int]:
        """
        Identify master numbers (11, 22, 33) in the person's chart
        These represent special spiritual missions and heightened potential
        """
        master_numbers = []
        
        # Check destiny number
        destiny_compound, _ = self.calculate_destiny_number(birth_date)
        if destiny_compound in [11, 22, 33]:
            master_numbers.append(destiny_compound)
        
        # Check name number
        name_compound, _, _ = self.calculate_name_number(name)
        if name_compound in [11, 22, 33]:
            master_numbers.append(name_compound)
        
        return list(set(master_numbers))
    
    def get_lucky_numbers(self, birth_date: datetime, name: str) -> List[int]:
        """
        Calculate lucky numbers based on name and birth date
        These numbers are considered favorable for the person
        """
        name_compound, name_reduced, _ = self.calculate_name_number(name)
        destiny_compound, destiny_reduced = self.calculate_destiny_number(birth_date)
        birth_number = self.calculate_birth_number(birth_date)
        
        lucky_numbers = [name_reduced, destiny_reduced, birth_number]
        
        # Add friendly numbers based on core numbers
        friendly_numbers = {
            1: [1, 2, 4, 7], 2: [1, 2, 7, 8], 3: [3, 6, 9], 
            4: [1, 2, 4, 8], 5: [5, 6, 9], 6: [3, 5, 6, 9],
            7: [1, 2, 7], 8: [2, 4, 8], 9: [3, 5, 6, 9]
        }
        
        for core_number in [name_reduced, destiny_reduced, birth_number]:
            lucky_numbers.extend(friendly_numbers.get(core_number, []))
        
        return sorted(list(set(lucky_numbers)))
    
    def get_challenging_numbers(self, birth_date: datetime, name: str) -> List[int]:
        """
        Calculate challenging numbers that may present difficulties
        """
        name_reduced = self.calculate_name_number(name)[1]
        destiny_reduced = self.calculate_destiny_number(birth_date)[1]
        birth_number = self.calculate_birth_number(birth_date)
        
        challenging_numbers = []
        
        # Numbers that conflict with core numbers
        challenging_map = {
            1: [6, 8, 9], 2: [3, 5, 9], 3: [1, 4, 5, 8],
            4: [3, 5, 7, 9], 5: [2, 4, 7, 8], 6: [1, 5, 7],
            7: [3, 4, 5, 6, 8, 9], 8: [1, 3, 5, 7, 9], 9: [1, 2, 4, 7, 8]
        }
        
        for core_number in [name_reduced, destiny_reduced, birth_number]:
            challenging_numbers.extend(challenging_map.get(core_number, []))
        
        return sorted(list(set(challenging_numbers)))
    
    def generate_full_report(self, name: str, birth_date: datetime) -> Dict:
        """
        Generate a comprehensive Chaldean numerology report (enhanced with PDF depth)
        
        Args:
            name: The person's name
            birth_date: The person's birth date
            
        Returns:
            Complete numerology report dictionary with all calculations
        """
        # Calculate all core numbers
        name_compound, name_reduced, letter_values = self.calculate_name_number(name)
        vowel_compound, vowel_reduced = self.calculate_vowel_number(name)
        consonant_compound, consonant_reduced = self.calculate_consonant_number(name)
        birth_number = self.calculate_birth_number(birth_date)
        destiny_compound, destiny_reduced = self.calculate_destiny_number(birth_date)
        life_stages = self.calculate_life_stage_numbers(birth_date)
        current_year = datetime.now().year
        personal_year = self.calculate_personal_year(birth_date, current_year)
        
        # Calculate special numbers
        karmic_debt = self.calculate_karmic_debt_numbers(birth_date, name)
        master_numbers = self.calculate_master_numbers(birth_date, name)
        lucky_numbers = self.get_lucky_numbers(birth_date, name)
        challenging_numbers = self.get_challenging_numbers(birth_date, name)
        
        # Get interpretations
        name_interpretation = self.get_number_interpretation(name_reduced)
        vowel_interpretation = self.get_number_interpretation(vowel_reduced)
        consonant_interpretation = self.get_number_interpretation(consonant_reduced)
        birth_interpretation = self.get_number_interpretation(birth_number)
        destiny_interpretation = self.get_number_interpretation(destiny_reduced)
        personal_year_interpretation = self.get_number_interpretation(personal_year)
        
        # Calculate compatibility between key numbers
        name_birth_compatibility = self.calculate_compatibility(name_reduced, birth_number)
        name_destiny_compatibility = self.calculate_compatibility(name_reduced, destiny_reduced)
        birth_destiny_compatibility = self.calculate_compatibility(birth_number, destiny_reduced)
        
        report = {
            "personal_info": {
                "name": name,
                "birth_date": birth_date.strftime("%B %d, %Y"),
                "calculation_date": datetime.now().strftime("%B %d, %Y"),
                "current_age": (datetime.now() - birth_date).days // 365
            },
            "core_numbers": {
                "name_number": {
                    "compound": name_compound,
                    "reduced": name_reduced,
                    "letter_breakdown": list(zip(list(re.sub(r'[^A-Za-z]', '', name.upper())), letter_values)),
                    "interpretation": name_interpretation,
                    "compound_meaning": self.get_compound_interpretation(name_compound) if name_compound > 9 else None,
                    "description": "Represents your full personality and how you express yourself in the world"
                },
                "vowel_number": {
                    "compound": vowel_compound,
                    "reduced": vowel_reduced,
                    "interpretation": vowel_interpretation,
                    "compound_meaning": self.get_compound_interpretation(vowel_compound) if vowel_compound > 9 else None,
                    "description": "Your Soul/Heart's Desire - represents inner motivations and what your soul craves"
                },
                "consonant_number": {
                    "compound": consonant_compound,
                    "reduced": consonant_reduced,
                    "interpretation": consonant_interpretation,
                    "compound_meaning": self.get_compound_interpretation(consonant_compound) if consonant_compound > 9 else None,
                    "description": "Your Personality Number - how others see you and your outer expression"
                },
                "birth_number": {
                    "number": birth_number,
                    "interpretation": birth_interpretation,
                    "description": "Your natural talents, abilities, and the gifts you were born with"
                },
                "destiny_number": {
                    "compound": destiny_compound,
                    "reduced": destiny_reduced,
                    "interpretation": destiny_interpretation,
                    "compound_meaning": self.get_compound_interpretation(destiny_compound) if destiny_compound > 9 else None,
                    "description": "Your Life Path - the purpose and lessons you're here to learn and fulfill"
                }
            },
            "temporal_influences": {
                "personal_year": {
                    "year": current_year,
                    "number": personal_year,
                    "interpretation": personal_year_interpretation,
                    "description": f"The overriding theme and opportunities for {current_year}"
                },
                "life_stages": {
                    "first_stage": {
                        "number": life_stages["first_stage"],
                        "period": "Ages 0-35 (approximately)",
                        "interpretation": self.get_number_interpretation(life_stages["first_stage"]),
                        "description": "Foundation years - learning basic life lessons"
                    },
                    "second_stage": {
                        "number": life_stages["second_stage"],
                        "period": "Ages 35-56 (approximately)",
                        "interpretation": self.get_number_interpretation(life_stages["second_stage"]),
                        "description": "Productive years - applying learned lessons to achieve goals"
                    },
                    "third_stage": {
                        "number": life_stages["third_stage"],
                        "period": "Ages 56+ (approximately)",
                        "interpretation": self.get_number_interpretation(life_stages["third_stage"]),
                        "description": "Wisdom years - sharing knowledge and spiritual development"
                    }
                }
            },
            "special_numbers": {
                "karmic_debt": {
                    "numbers": karmic_debt,
                    "meanings": [self.get_compound_interpretation(num) for num in karmic_debt],
                    "description": "Karmic lessons to be learned in this lifetime"
                },
                "master_numbers": {
                    "numbers": master_numbers,
                    "meanings": [self.get_compound_interpretation(num) for num in master_numbers],
                    "description": "Special spiritual missions and heightened potential"
                },
                "lucky_numbers": {
                    "numbers": lucky_numbers,
                    "description": "Numbers that bring favorable energy and opportunities"
                },
                "challenging_numbers": {
                    "numbers": challenging_numbers,
                    "description": "Numbers that may present obstacles or require extra attention"
                }
            },
            "compatibility": {
                "name_birth": name_birth_compatibility,
                "name_destiny": name_destiny_compatibility,
                "birth_destiny": birth_destiny_compatibility,
                "internal_harmony": {
                    "rating": "High" if all([
                        name_birth_compatibility["compatible"],
                        name_destiny_compatibility["compatible"],
                        birth_destiny_compatibility["compatible"]
                    ]) else "Moderate" if any([
                        name_birth_compatibility["compatible"],
                        name_destiny_compatibility["compatible"],
                        birth_destiny_compatibility["compatible"]
                    ]) else "Challenging",
                    "description": "Overall harmony between your core numbers"
                }
            },
            "life_guidance": {
                "strengths": [
                    name_interpretation["strengths"],
                    birth_interpretation["strengths"],
                    destiny_interpretation["strengths"]
                ],
                "challenges": [
                    name_interpretation["challenges"],
                    birth_interpretation["challenges"],
                    destiny_interpretation["challenges"]
                ],
                "career_guidance": [
                    name_interpretation.get("career", "Leadership and initiative-based roles"),
                    birth_interpretation.get("career", "Roles utilizing natural talents"),
                    destiny_interpretation.get("career", "Purpose-driven career paths")
                ],
                "relationship_guidance": [
                    name_interpretation.get("relationships", "Authentic self-expression in relationships"),
                    birth_interpretation.get("relationships", "Natural relationship style"),
                    destiny_interpretation.get("relationships", "Relationship lessons and growth")
                ],
                "health_guidance": [
                    name_interpretation.get("health", "General wellness considerations"),
                    birth_interpretation.get("health", "Constitutional health tendencies"),
                    destiny_interpretation.get("health", "Life path health considerations")
                ]
            },
            "summary": {
                "life_path_theme": destiny_interpretation["description"],
                "personality_core": name_interpretation["description"],
                "inner_motivation": vowel_interpretation["description"],
                "outer_expression": consonant_interpretation["description"],
                "natural_gifts": birth_interpretation["strengths"],
                "key_challenges": name_interpretation["challenges"],
                "current_year_focus": personal_year_interpretation["description"]
            }
        }
        
        return report
    
    def generate_comprehensive_report(self, name: str, birth_date: datetime) -> Dict:
        """
        Generate a comprehensive numerology report for a person
        
        Args:
            name: Full name of the person
            birth_date: Birth date
            
        Returns:
            Dictionary containing complete numerology analysis
        """
        # Calculate all core numbers
        name_compound, name_reduced, name_letters = self.calculate_name_number(name)
        vowel_compound, vowel_reduced = self.calculate_vowel_number(name)
        consonant_compound, consonant_reduced = self.calculate_consonant_number(name)
        birth_number = self.calculate_birth_number(birth_date)
        destiny_compound, destiny_reduced = self.calculate_destiny_number(birth_date)
        life_stages = self.calculate_life_stages(birth_date)
        personal_year = self.calculate_personal_year(birth_date)
        
        # Calculate special numbers
        karmic_debt = self.calculate_karmic_debt_numbers(birth_date, name)
        master_numbers = self.identify_master_numbers(birth_date, name)
        lucky_numbers = self.calculate_lucky_numbers(birth_date, name)
        challenging_numbers = self.calculate_challenging_numbers(birth_date, name)
        
        # Get interpretations
        name_interpretation = self.get_number_interpretation(name_reduced)
        vowel_interpretation = self.get_number_interpretation(vowel_reduced)
        consonant_interpretation = self.get_number_interpretation(consonant_reduced)
        birth_interpretation = self.get_number_interpretation(birth_number)
        destiny_interpretation = self.get_number_interpretation(destiny_reduced)
        personal_year_interpretation = self.get_number_interpretation(personal_year)
        
        # Calculate compatibility
        name_birth_compatibility = self.calculate_compatibility(name_reduced, birth_number)
        name_destiny_compatibility = self.calculate_compatibility(name_reduced, destiny_reduced)
        birth_destiny_compatibility = self.calculate_compatibility(birth_number, destiny_reduced)
        
        # Compile comprehensive report
        report = {
            "personal_info": {
                "name": name,
                "birth_date": birth_date.strftime("%Y-%m-%d"),
                "age": (datetime.now() - birth_date).days // 365
            },
            "core_numbers": {
                "name_number": {
                    "compound": name_compound,
                    "reduced": name_reduced,
                    "letter_values": name_letters,
                    "interpretation": name_interpretation,
                    "description": "Your outer personality and how others see you"
                },
                "vowel_number": {
                    "compound": vowel_compound,
                    "reduced": vowel_reduced,
                    "interpretation": vowel_interpretation,
                    "description": "Your inner desires and what your soul craves"
                },
                "consonant_number": {
                    "compound": consonant_compound,
                    "reduced": consonant_reduced,
                    "interpretation": consonant_interpretation,
                    "description": "Your outer expression and first impression"
                },
                "birth_number": {
                    "value": birth_number,
                    "interpretation": birth_interpretation,
                    "description": "Your natural talents and abilities"
                },
                "destiny_number": {
                    "compound": destiny_compound,
                    "reduced": destiny_reduced,
                    "interpretation": destiny_interpretation,
                    "description": "Your life purpose and spiritual mission"
                },
                "personal_year": {
                    "value": personal_year,
                    "interpretation": personal_year_interpretation,
                    "description": f"The theme and energy for your current year ({datetime.now().year})"
                }
            },
            "life_stages": {
                "first_stage": {
                    "number": life_stages["first_stage"],
                    "period": "0-28 years",
                    "interpretation": self.get_number_interpretation(life_stages["first_stage"]),
                    "description": "Foundation building and early development"
                },
                "second_stage": {
                    "number": life_stages["second_stage"],
                    "period": "28-56 years",
                    "interpretation": self.get_number_interpretation(life_stages["second_stage"]),
                    "description": "Prime productive years and major achievements"
                },
                "third_stage": {
                    "number": life_stages["third_stage"],
                    "period": "56+ years",
                    "interpretation": self.get_number_interpretation(life_stages["third_stage"]),
                    "description": "Wisdom years and spiritual fulfillment"
                }
            },
            "special_numbers": {
                "karmic_debt": {
                    "numbers": karmic_debt,
                    "meanings": [self.get_compound_interpretation(num) for num in karmic_debt],
                    "description": "Karmic lessons to be learned in this lifetime"
                },
                "master_numbers": {
                    "numbers": master_numbers,
                    "meanings": [self.get_compound_interpretation(num) for num in master_numbers],
                    "description": "Special spiritual missions and heightened potential"
                },
                "lucky_numbers": {
                    "numbers": lucky_numbers,
                    "description": "Numbers that bring favorable energy and opportunities"
                },
                "challenging_numbers": {
                    "numbers": challenging_numbers,
                    "description": "Numbers that may present obstacles or require extra attention"
                }
            },
            "compatibility": {
                "name_birth": name_birth_compatibility,
                "name_destiny": name_destiny_compatibility,
                "birth_destiny": birth_destiny_compatibility,
                "internal_harmony": {
                    "rating": "High" if all([
                        name_birth_compatibility["compatible"],
                        name_destiny_compatibility["compatible"],
                        birth_destiny_compatibility["compatible"]
                    ]) else "Moderate" if any([
                        name_birth_compatibility["compatible"],
                        name_destiny_compatibility["compatible"],
                        birth_destiny_compatibility["compatible"]
                    ]) else "Challenging",
                    "description": "Overall harmony between your core numbers"
                }
            },
            "life_guidance": {
                "strengths": [
                    name_interpretation["strengths"],
                    birth_interpretation["strengths"],
                    destiny_interpretation["strengths"]
                ],
                "challenges": [
                    name_interpretation["challenges"],
                    birth_interpretation["challenges"],
                    destiny_interpretation["challenges"]
                ],
                "career_guidance": [
                    name_interpretation.get("career", "Leadership and initiative-based roles"),
                    birth_interpretation.get("career", "Roles utilizing natural talents"),
                    destiny_interpretation.get("career", "Purpose-driven career paths")
                ],
                "relationship_guidance": [
                    name_interpretation.get("relationships", "Authentic self-expression in relationships"),
                    birth_interpretation.get("relationships", "Natural relationship style"),
                    destiny_interpretation.get("relationships", "Relationship lessons and growth")
                ],
                "health_guidance": [
                    name_interpretation.get("health", "General wellness considerations"),
                    birth_interpretation.get("health", "Constitutional health tendencies"),
                    destiny_interpretation.get("health", "Life path health considerations")
                ]
            },
            "summary": {
                "life_path_theme": destiny_interpretation["description"],
                "personality_core": name_interpretation["description"],
                "inner_motivation": vowel_interpretation["description"],
                "outer_expression": consonant_interpretation["description"],
                "natural_gifts": birth_interpretation["strengths"],
                "key_challenges": name_interpretation["challenges"],
                "current_year_focus": personal_year_interpretation["description"]
            }
        }
        
        return report
