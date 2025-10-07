"""
Hidden Passion and Karmic Lessons Calculator for North Indian Chaldean Numerology
Analyzes letter frequency for dominant and missing energies
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from collections import Counter


@dataclass
class KarmicAnalysisResult:
    """Result container for Karmic analysis"""
    hidden_passion: List[int]
    karmic_lessons: List[int]
    most_karmic_lesson: int
    letter_frequency: Dict[str, int]
    number_frequency: Dict[int, int]
    analysis: Dict[str, Any]
    recommendations: List[str]


class KarmicAnalysisCalculator:
    """Calculator for Hidden Passion and Karmic Lessons analysis"""
    
    def __init__(self):
        # Chaldean alphabet to number mapping
        self.chaldean_map = {
            'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
            'B': 2, 'K': 2, 'R': 2,
            'C': 3, 'G': 3, 'L': 3, 'S': 3,
            'D': 4, 'M': 4, 'T': 4,
            'E': 5, 'H': 5, 'N': 5, 'X': 5,
            'U': 6, 'V': 6, 'W': 6,
            'O': 7, 'Z': 7,
            'F': 8, 'P': 8
            # Note: No 9 in Chaldean system
        }
        
        # Number meanings for analysis
        self.number_meanings = {
            1: {
                'energy': 'Leadership and Independence',
                'qualities': ['Initiative', 'Originality', 'Ambition', 'Self-reliance'],
                'challenges': ['Selfishness', 'Domination', 'Impatience'],
                'career_fields': ['Management', 'Entrepreneurship', 'Politics', 'Innovation']
            },
            2: {
                'energy': 'Cooperation and Sensitivity',
                'qualities': ['Diplomacy', 'Partnership', 'Patience', 'Intuition'],
                'challenges': ['Indecision', 'Over-sensitivity', 'Dependency'],
                'career_fields': ['Counseling', 'Healthcare', 'Education', 'Social Work']
            },
            3: {
                'energy': 'Creativity and Communication',
                'qualities': ['Artistic ability', 'Eloquence', 'Optimism', 'Social skills'],
                'challenges': ['Scattered energy', 'Superficiality', 'Gossip'],
                'career_fields': ['Arts', 'Media', 'Entertainment', 'Writing']
            },
            4: {
                'energy': 'Stability and Hard Work',
                'qualities': ['Practicality', 'Organization', 'Reliability', 'Persistence'],
                'challenges': ['Rigidity', 'Narrow-mindedness', 'Stubbornness'],
                'career_fields': ['Engineering', 'Architecture', 'Accounting', 'Administration']
            },
            5: {
                'energy': 'Freedom and Adventure',
                'qualities': ['Versatility', 'Curiosity', 'Progressive thinking', 'Adaptability'],
                'challenges': ['Restlessness', 'Irresponsibility', 'Impulsiveness'],
                'career_fields': ['Travel', 'Sales', 'Marketing', 'Technology']
            },
            6: {
                'energy': 'Nurturing and Responsibility',
                'qualities': ['Compassion', 'Healing', 'Family focus', 'Service'],
                'challenges': ['Interference', 'Worry', 'Self-sacrifice'],
                'career_fields': ['Healthcare', 'Teaching', 'Hospitality', 'Community Service']
            },
            7: {
                'energy': 'Spirituality and Analysis',
                'qualities': ['Intuition', 'Research', 'Contemplation', 'Wisdom'],
                'challenges': ['Isolation', 'Skepticism', 'Moodiness'],
                'career_fields': ['Research', 'Spirituality', 'Analysis', 'Investigation']
            },
            8: {
                'energy': 'Material Success and Authority',
                'qualities': ['Business acumen', 'Organization', 'Achievement', 'Recognition'],
                'challenges': ['Materialism', 'Workaholism', 'Ruthlessness'],
                'career_fields': ['Business', 'Finance', 'Real Estate', 'Corporate Leadership']
            }
        }
    
    def analyze_name(self, full_name: str) -> KarmicAnalysisResult:
        """Analyze full name for Hidden Passion and Karmic Lessons"""
        # Clean and prepare name
        clean_name = ''.join(c.upper() for c in full_name if c.isalpha())
        
        if not clean_name:
            raise ValueError("Name must contain at least one letter")
        
        # Count letter frequency
        letter_frequency = Counter(clean_name)
        
        # Convert to number frequency using Chaldean system
        number_frequency = {}
        for letter, count in letter_frequency.items():
            if letter in self.chaldean_map:
                number = self.chaldean_map[letter]
                number_frequency[number] = number_frequency.get(number, 0) + count
        
        # Calculate Hidden Passion (most frequent numbers)
        max_frequency = max(number_frequency.values()) if number_frequency else 0
        hidden_passion = [num for num, freq in number_frequency.items() if freq == max_frequency]
        
        # Calculate Karmic Lessons (missing numbers)
        all_numbers = set(range(1, 9))  # 1-8 in Chaldean system
        present_numbers = set(number_frequency.keys())
        karmic_lessons = sorted(list(all_numbers - present_numbers))
        
        # Determine Most Karmic Lesson (lowest frequency or most impactful missing)
        most_karmic_lesson = self._determine_most_karmic_lesson(karmic_lessons, number_frequency)
        
        # Generate detailed analysis
        analysis = self._generate_analysis(hidden_passion, karmic_lessons, number_frequency)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(hidden_passion, karmic_lessons, most_karmic_lesson)
        
        return KarmicAnalysisResult(
            hidden_passion=hidden_passion,
            karmic_lessons=karmic_lessons,
            most_karmic_lesson=most_karmic_lesson,
            letter_frequency=dict(letter_frequency),
            number_frequency=number_frequency,
            analysis=analysis,
            recommendations=recommendations
        )
    
    def _determine_most_karmic_lesson(self, karmic_lessons: List[int], number_frequency: Dict[int, int]) -> int:
        """Determine the most significant karmic lesson"""
        if not karmic_lessons:
            return 0
        
        # Priority order for karmic impact (based on traditional numerology)
        priority_order = [1, 4, 7, 8, 2, 5, 3, 6]
        
        # Find the first missing number in priority order
        for num in priority_order:
            if num in karmic_lessons:
                return num
        
        # If none found in priority, return the first karmic lesson
        return karmic_lessons[0] if karmic_lessons else 0
    
    def _generate_analysis(self, hidden_passion: List[int], karmic_lessons: List[int], 
                          number_frequency: Dict[int, int]) -> Dict[str, Any]:
        """Generate detailed analysis of the karmic profile"""
        analysis = {
            'hidden_passion_analysis': {},
            'karmic_lessons_analysis': {},
            'overall_profile': {},
            'strengths': [],
            'challenges': [],
            'life_themes': []
        }
        
        # Hidden Passion Analysis
        for num in hidden_passion:
            if num in self.number_meanings:
                meaning = self.number_meanings[num]
                analysis['hidden_passion_analysis'][num] = {
                    'frequency': number_frequency[num],
                    'energy': meaning['energy'],
                    'dominant_qualities': meaning['qualities'],
                    'potential_challenges': meaning['challenges'],
                    'career_alignment': meaning['career_fields']
                }
                analysis['strengths'].extend(meaning['qualities'])
        
        # Karmic Lessons Analysis
        for num in karmic_lessons:
            if num in self.number_meanings:
                meaning = self.number_meanings[num]
                analysis['karmic_lessons_analysis'][num] = {
                    'missing_energy': meaning['energy'],
                    'areas_to_develop': meaning['qualities'],
                    'life_challenges': meaning['challenges'],
                    'growth_opportunities': meaning['career_fields']
                }
                analysis['challenges'].extend([f"Develop {quality.lower()}" for quality in meaning['qualities']])
        
        # Overall Profile
        analysis['overall_profile'] = {
            'dominant_energies': len(hidden_passion),
            'missing_energies': len(karmic_lessons),
            'balance_score': self._calculate_balance_score(number_frequency, karmic_lessons),
            'personality_type': self._determine_personality_type(hidden_passion, karmic_lessons)
        }
        
        # Life Themes
        analysis['life_themes'] = self._extract_life_themes(hidden_passion, karmic_lessons)
        
        return analysis
    
    def _calculate_balance_score(self, number_frequency: Dict[int, int], karmic_lessons: List[int]) -> float:
        """Calculate overall numerological balance score (0-100)"""
        # Base score
        score = 50.0
        
        # Add points for number diversity
        present_numbers = len(number_frequency)
        score += (present_numbers * 6.25)  # Max 50 points for all 8 numbers
        
        # Deduct for missing numbers
        score -= (len(karmic_lessons) * 6.25)
        
        # Add points for balanced frequency (avoid extremes)
        if number_frequency:
            frequencies = list(number_frequency.values())
            avg_freq = sum(frequencies) / len(frequencies)
            variance = sum((f - avg_freq) ** 2 for f in frequencies) / len(frequencies)
            # Lower variance = more balanced = higher score
            balance_bonus = max(0, 25 - variance)
            score += balance_bonus
        
        return max(0.0, min(100.0, score))
    
    def _determine_personality_type(self, hidden_passion: List[int], karmic_lessons: List[int]) -> str:
        """Determine overall personality type based on dominant and missing energies"""
        if not hidden_passion:
            return "Balanced Explorer"
        
        primary_passion = hidden_passion[0]
        
        type_mapping = {
            1: "Natural Leader",
            2: "Collaborative Diplomat", 
            3: "Creative Communicator",
            4: "Practical Builder",
            5: "Dynamic Adventurer",
            6: "Caring Nurturer",
            7: "Wise Seeker",
            8: "Ambitious Achiever"
        }
        
        base_type = type_mapping.get(primary_passion, "Unique Individual")
        
        # Modify based on karmic lessons
        if len(karmic_lessons) > 4:
            return f"Developing {base_type}"
        elif len(karmic_lessons) <= 2:
            return f"Well-Rounded {base_type}"
        else:
            return base_type
    
    def _extract_life_themes(self, hidden_passion: List[int], karmic_lessons: List[int]) -> List[str]:
        """Extract major life themes based on karmic profile"""
        themes = []
        
        # Themes from Hidden Passion
        if 1 in hidden_passion:
            themes.append("Leadership and Self-Discovery")
        if 2 in hidden_passion:
            themes.append("Partnership and Cooperation")
        if 3 in hidden_passion:
            themes.append("Creative Expression")
        if 4 in hidden_passion:
            themes.append("Building and Stability")
        if 5 in hidden_passion:
            themes.append("Freedom and Change")
        if 6 in hidden_passion:
            themes.append("Service and Responsibility")
        if 7 in hidden_passion:
            themes.append("Spiritual Growth")
        if 8 in hidden_passion:
            themes.append("Material Achievement")
        
        # Themes from Karmic Lessons
        if 1 in karmic_lessons:
            themes.append("Developing Independence")
        if 4 in karmic_lessons:
            themes.append("Learning Discipline")
        if 7 in karmic_lessons:
            themes.append("Cultivating Inner Wisdom")
        if 8 in karmic_lessons:
            themes.append("Building Material Security")
        
        return themes[:5]  # Return top 5 themes
    
    def _generate_recommendations(self, hidden_passion: List[int], karmic_lessons: List[int], 
                                most_karmic_lesson: int) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Hidden Passion recommendations
        if hidden_passion:
            passion_energies = [self.number_meanings[num]['energy'] for num in hidden_passion 
                              if num in self.number_meanings]
            recommendations.append(
                f"Your Hidden Passion ({', '.join(map(str, hidden_passion))}): "
                f"Embrace your natural {', '.join(passion_energies).lower()} abilities."
            )
        
        # Karmic Lessons recommendations
        if karmic_lessons:
            recommendations.append(
                f"Karmic Lessons ({', '.join(map(str, karmic_lessons))}): "
                f"Focus on developing these missing energies for balanced growth."
            )
        
        # Most Karmic Lesson specific advice
        if most_karmic_lesson and most_karmic_lesson in self.number_meanings:
            meaning = self.number_meanings[most_karmic_lesson]
            recommendations.append(
                f"Most Important Karmic Lesson ({most_karmic_lesson}): "
                f"Prioritize developing {meaning['energy'].lower()} in your life."
            )
        
        # General development recommendations
        if len(karmic_lessons) > 4:
            recommendations.append(
                "With many karmic lessons, focus on gradual development rather than trying to change everything at once."
            )
        elif len(karmic_lessons) <= 2:
            recommendations.append(
                "You have a well-balanced karmic profile. Focus on refining your existing strengths."
            )
        
        # Color therapy recommendations (traditional numerology)
        color_recommendations = self._get_color_recommendations(hidden_passion, karmic_lessons)
        if color_recommendations:
            recommendations.extend(color_recommendations)
        
        return recommendations
    
    def _get_color_recommendations(self, hidden_passion: List[int], karmic_lessons: List[int]) -> List[str]:
        """Get color therapy recommendations based on numerological profile"""
        color_map = {
            1: "Red (energy, leadership)",
            2: "Orange (cooperation, creativity)", 
            3: "Yellow (communication, joy)",
            4: "Green (stability, growth)",
            5: "Blue (freedom, truth)",
            6: "Indigo (responsibility, intuition)",
            7: "Violet (spirituality, wisdom)",
            8: "Pink (material success, love)"
        }
        
        recommendations = []
        
        # Colors to enhance (based on hidden passion)
        if hidden_passion:
            enhance_colors = [color_map[num] for num in hidden_passion if num in color_map]
            if enhance_colors:
                recommendations.append(f"Enhance with colors: {', '.join(enhance_colors)}")
        
        # Colors to develop (based on karmic lessons)
        if karmic_lessons:
            develop_colors = [color_map[num] for num in karmic_lessons[:3] if num in color_map]  # Top 3
            if develop_colors:
                recommendations.append(f"Develop with colors: {', '.join(develop_colors)}")
        
        return recommendations
    
    def format_analysis_report(self, result: KarmicAnalysisResult) -> str:
        """Format comprehensive analysis report"""
        report = []
        report.append("=== KARMIC ANALYSIS REPORT ===\n")
        
        # Hidden Passion Section
        if result.hidden_passion:
            report.append("🔥 HIDDEN PASSION (Dominant Energies)")
            report.append("-" * 40)
            for num in result.hidden_passion:
                if num in result.analysis['hidden_passion_analysis']:
                    analysis = result.analysis['hidden_passion_analysis'][num]
                    report.append(f"Number {num}: {analysis['energy']} (appears {analysis['frequency']} times)")
                    report.append(f"  Qualities: {', '.join(analysis['dominant_qualities'])}")
                    report.append(f"  Career Fields: {', '.join(analysis['career_alignment'])}")
            report.append("")
        
        # Karmic Lessons Section
        if result.karmic_lessons:
            report.append("⚖️ KARMIC LESSONS (Missing Energies)")
            report.append("-" * 40)
            for num in result.karmic_lessons:
                if num in result.analysis['karmic_lessons_analysis']:
                    analysis = result.analysis['karmic_lessons_analysis'][num]
                    report.append(f"Number {num}: {analysis['missing_energy']}")
                    report.append(f"  Areas to Develop: {', '.join(analysis['areas_to_develop'])}")
            
            if result.most_karmic_lesson:
                report.append(f"\n🎯 Most Important Karmic Lesson: {result.most_karmic_lesson}")
            report.append("")
        
        # Overall Profile
        profile = result.analysis['overall_profile']
        report.append("📊 OVERALL PROFILE")
        report.append("-" * 40)
        report.append(f"Personality Type: {profile['personality_type']}")
        report.append(f"Balance Score: {profile['balance_score']:.1f}/100")
        report.append(f"Dominant Energies: {profile['dominant_energies']}")
        report.append(f"Missing Energies: {profile['missing_energies']}")
        report.append("")
        
        # Life Themes
        if result.analysis['life_themes']:
            report.append("🌟 LIFE THEMES")
            report.append("-" * 40)
            for theme in result.analysis['life_themes']:
                report.append(f"• {theme}")
            report.append("")
        
        # Recommendations
        if result.recommendations:
            report.append("💡 RECOMMENDATIONS")
            report.append("-" * 40)
            for rec in result.recommendations:
                report.append(f"• {rec}")
        
        return "\n".join(report)


if __name__ == "__main__":
    # Test the Karmic Analysis calculator
    calculator = KarmicAnalysisCalculator()
    
    # Test with sample name
    result = calculator.analyze_name("JOHN SMITH")
    
    print(calculator.format_analysis_report(result))
    print(f"\nNumber Frequency: {result.number_frequency}")
    print(f"Letter Frequency: {result.letter_frequency}")
