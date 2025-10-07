"""
Personal Year/Month/Day Calculator for North Indian Chaldean Numerology
Calculates temporal numerology cycles and predictions
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, date
from dataclasses import dataclass


@dataclass
class PersonalCycleResult:
    """Result container for Personal Year/Month/Day analysis"""
    personal_year: int
    personal_month: int
    personal_day: int
    cycle_analysis: Dict[str, Any]
    predictions: Dict[str, List[str]]
    recommendations: List[str]
    lucky_dates: List[date]
    challenging_dates: List[date]


class PersonalCycleCalculator:
    """Calculator for Personal Year, Month, and Day cycles"""
    
    def __init__(self):
        # Personal Year meanings and themes
        self.personal_year_themes = {
            1: {
                'theme': 'New Beginnings and Leadership',
                'keywords': ['Start', 'Initiative', 'Independence', 'Innovation'],
                'opportunities': ['New career', 'Starting business', 'Leadership roles', 'Personal projects'],
                'challenges': ['Impatience', 'Selfishness', 'Rushed decisions'],
                'advice': 'Take initiative and start new ventures. Focus on self-development.',
                'lucky_months': [1, 10, 11],
                'challenging_months': [4, 7, 8]
            },
            2: {
                'theme': 'Cooperation and Relationships',
                'keywords': ['Partnership', 'Diplomacy', 'Patience', 'Teamwork'],
                'opportunities': ['Marriage', 'Business partnerships', 'Collaborative projects', 'Mediation'],
                'challenges': ['Indecision', 'Over-sensitivity', 'Dependency'],
                'advice': 'Focus on relationships and cooperative endeavors. Practice patience.',
                'lucky_months': [2, 6, 9],
                'challenging_months': [1, 5, 8]
            },
            3: {
                'theme': 'Creative Expression and Communication',
                'keywords': ['Creativity', 'Communication', 'Joy', 'Social'],
                'opportunities': ['Artistic pursuits', 'Public speaking', 'Social events', 'Creative projects'],
                'challenges': ['Scattered energy', 'Superficiality', 'Gossip'],
                'advice': 'Express creativity and improve communication skills. Enjoy social activities.',
                'lucky_months': [3, 6, 12],
                'challenging_months': [4, 7, 9]
            },
            4: {
                'theme': 'Foundation Building and Hard Work',
                'keywords': ['Stability', 'Organization', 'Hard work', 'Practical'],
                'opportunities': ['Career advancement', 'Property investment', 'Skill development', 'System building'],
                'challenges': ['Rigidity', 'Overwork', 'Stubbornness'],
                'advice': 'Build solid foundations through systematic work. Focus on practical matters.',
                'lucky_months': [4, 8, 10],
                'challenging_months': [3, 5, 9]
            },
            5: {
                'theme': 'Freedom and Adventure',
                'keywords': ['Change', 'Freedom', 'Adventure', 'Progress'],
                'opportunities': ['Travel', 'Career change', 'Learning new skills', 'Networking'],
                'challenges': ['Restlessness', 'Impulsiveness', 'Lack of focus'],
                'advice': 'Embrace change and seek new experiences. Avoid major commitments.',
                'lucky_months': [5, 7, 11],
                'challenging_months': [2, 4, 6]
            },
            6: {
                'theme': 'Responsibility and Service',
                'keywords': ['Family', 'Service', 'Responsibility', 'Healing'],
                'opportunities': ['Family matters', 'Community service', 'Healing work', 'Home improvement'],
                'challenges': ['Over-responsibility', 'Worry', 'Interference'],
                'advice': 'Focus on family and service to others. Take on responsibilities willingly.',
                'lucky_months': [6, 9, 12],
                'challenging_months': [1, 5, 8]
            },
            7: {
                'theme': 'Spiritual Growth and Analysis',
                'keywords': ['Spirituality', 'Study', 'Analysis', 'Introspection'],
                'opportunities': ['Spiritual study', 'Research', 'Meditation', 'Higher education'],
                'challenges': ['Isolation', 'Pessimism', 'Over-analysis'],
                'advice': 'Focus on spiritual and intellectual development. Spend time in contemplation.',
                'lucky_months': [7, 11, 12],
                'challenging_months': [3, 5, 8]
            },
            8: {
                'theme': 'Material Achievement and Recognition',
                'keywords': ['Success', 'Recognition', 'Authority', 'Material'],
                'opportunities': ['Business success', 'Financial gain', 'Recognition', 'Leadership positions'],
                'challenges': ['Materialism', 'Workaholism', 'Ruthlessness'],
                'advice': 'Focus on business and financial matters. Seek recognition for achievements.',
                'lucky_months': [8, 10, 11],
                'challenging_months': [2, 7, 9]
            },
            9: {
                'theme': 'Completion and Humanitarian Service',
                'keywords': ['Completion', 'Service', 'Wisdom', 'Transformation'],
                'opportunities': ['Completing projects', 'Humanitarian work', 'Teaching', 'Global activities'],
                'challenges': ['Emotional intensity', 'Letting go', 'Drama'],
                'advice': 'Complete unfinished business and serve humanity. Prepare for new cycles.',
                'lucky_months': [9, 12, 3],
                'challenging_months': [1, 4, 8]
            }
        }
        
        # Personal Month additional influences
        self.month_influences = {
            1: 'Leadership and new starts',
            2: 'Cooperation and relationships',
            3: 'Creative expression',
            4: 'Hard work and foundation',
            5: 'Change and freedom',
            6: 'Family and responsibility',
            7: 'Spirituality and study',
            8: 'Business and achievement',
            9: 'Completion and service',
            10: 'New cycles (1 energy)',
            11: 'Intuition and inspiration',
            12: 'Creative completion (3 energy)'
        }
    
    def calculate_personal_cycles(self, birth_date: str, target_date: Optional[str] = None) -> PersonalCycleResult:
        """Calculate Personal Year, Month, and Day for given dates"""
        try:
            # Parse birth date
            birth_obj = datetime.strptime(birth_date, "%d-%m-%Y").date()
            
            # Use current date if target_date not provided
            if target_date:
                target_obj = datetime.strptime(target_date, "%d-%m-%Y").date()
            else:
                target_obj = date.today()
            
            # Calculate Personal Year
            personal_year = self._calculate_personal_year(birth_obj, target_obj)
            
            # Calculate Personal Month
            personal_month = self._calculate_personal_month(personal_year, target_obj.month)
            
            # Calculate Personal Day
            personal_day = self._calculate_personal_day(personal_month, target_obj.day)
            
            # Generate cycle analysis
            cycle_analysis = self._analyze_cycles(personal_year, personal_month, personal_day, target_obj)
            
            # Generate predictions
            predictions = self._generate_predictions(personal_year, personal_month, personal_day, target_obj)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(personal_year, personal_month, personal_day)
            
            # Calculate lucky and challenging dates
            lucky_dates, challenging_dates = self._calculate_significant_dates(
                birth_obj, target_obj, personal_year
            )
            
            return PersonalCycleResult(
                personal_year=personal_year,
                personal_month=personal_month,
                personal_day=personal_day,
                cycle_analysis=cycle_analysis,
                predictions=predictions,
                recommendations=recommendations,
                lucky_dates=lucky_dates,
                challenging_dates=challenging_dates
            )
            
        except ValueError as e:
            raise ValueError(f"Invalid date format. Use DD-MM-YYYY: {e}")
    
    def _calculate_personal_year(self, birth_date: date, target_date: date) -> int:
        """Calculate Personal Year number"""
        # Personal Year = Birth day + Birth month + Target year
        birth_day = self._reduce_to_single_digit(birth_date.day)
        birth_month = self._reduce_to_single_digit(birth_date.month)
        target_year = self._reduce_to_single_digit(target_date.year)
        
        personal_year = birth_day + birth_month + target_year
        return self._reduce_to_single_digit(personal_year)
    
    def _calculate_personal_month(self, personal_year: int, target_month: int) -> int:
        """Calculate Personal Month number"""
        # Personal Month = Personal Year + Target month
        month_reduced = self._reduce_to_single_digit(target_month)
        personal_month = personal_year + month_reduced
        return self._reduce_to_single_digit(personal_month)
    
    def _calculate_personal_day(self, personal_month: int, target_day: int) -> int:
        """Calculate Personal Day number"""
        # Personal Day = Personal Month + Target day
        day_reduced = self._reduce_to_single_digit(target_day)
        personal_day = personal_month + day_reduced
        return self._reduce_to_single_digit(personal_day)
    
    def _reduce_to_single_digit(self, number: int) -> int:
        """Reduce number to single digit (1-9)"""
        while number > 9:
            number = sum(int(digit) for digit in str(number))
        return number
    
    def _analyze_cycles(self, personal_year: int, personal_month: int, 
                       personal_day: int, target_date: date) -> Dict[str, Any]:
        """Analyze the interaction of all cycles"""
        analysis = {
            'dominant_influence': self._determine_dominant_influence(personal_year, personal_month, personal_day),
            'cycle_harmony': self._calculate_cycle_harmony(personal_year, personal_month, personal_day),
            'energy_level': self._calculate_energy_level(personal_year, personal_month, personal_day),
            'life_phase': self._determine_life_phase(personal_year),
            'monthly_focus': self._get_monthly_focus(personal_month),
            'daily_energy': self._get_daily_energy(personal_day),
            'overall_vibration': self._calculate_overall_vibration(personal_year, personal_month, personal_day)
        }
        
        return analysis
    
    def _determine_dominant_influence(self, py: int, pm: int, pd: int) -> str:
        """Determine which cycle has the strongest influence"""
        # Personal Year has strongest influence, followed by Month, then Day
        if py in [1, 8, 9]:  # Strong leadership/achievement/completion years
            return f"Personal Year {py} (Strong yearly influence)"
        elif pm in [1, 8, 9]:
            return f"Personal Month {pm} (Strong monthly influence)"
        elif pd in [1, 8, 9]:
            return f"Personal Day {pd} (Strong daily influence)"
        else:
            return "Balanced influence across all cycles"
    
    def _calculate_cycle_harmony(self, py: int, pm: int, pd: int) -> str:
        """Calculate harmony between cycles"""
        # Check for complementary numbers
        cycles = [py, pm, pd]
        
        # Perfect harmony: same number or complementary pairs
        if len(set(cycles)) == 1:
            return "Perfect Harmony - All cycles aligned"
        elif py == pm or py == pd or pm == pd:
            return "Good Harmony - Two cycles aligned"
        elif self._are_complementary(py, pm) or self._are_complementary(py, pd) or self._are_complementary(pm, pd):
            return "Moderate Harmony - Complementary energies"
        else:
            return "Dynamic Tension - Conflicting but growth-oriented"
    
    def _are_complementary(self, num1: int, num2: int) -> bool:
        """Check if two numbers are complementary"""
        complementary_pairs = [(1, 2), (3, 6), (4, 8), (5, 7), (9, 3)]
        pair = tuple(sorted([num1, num2]))
        return pair in complementary_pairs or pair[::-1] in complementary_pairs
    
    def _calculate_energy_level(self, py: int, pm: int, pd: int) -> str:
        """Calculate overall energy level"""
        total = py + pm + pd
        if total >= 21:
            return "Very High Energy"
        elif total >= 15:
            return "High Energy"
        elif total >= 12:
            return "Moderate Energy"
        else:
            return "Calm Energy"
    
    def _determine_life_phase(self, personal_year: int) -> str:
        """Determine current life phase based on Personal Year"""
        phase_map = {
            1: "Initiation Phase - New beginnings",
            2: "Development Phase - Building relationships",
            3: "Expression Phase - Creative output",
            4: "Foundation Phase - Establishing stability",
            5: "Expansion Phase - Exploring possibilities",
            6: "Responsibility Phase - Service and family",
            7: "Reflection Phase - Inner development",
            8: "Achievement Phase - Material success",
            9: "Completion Phase - Ending cycles"
        }
        return phase_map.get(personal_year, "Transition Phase")
    
    def _get_monthly_focus(self, personal_month: int) -> str:
        """Get focus for current Personal Month"""
        return self.month_influences.get(personal_month, "General development")
    
    def _get_daily_energy(self, personal_day: int) -> str:
        """Get energy description for Personal Day"""
        day_energies = {
            1: "Leadership and initiative",
            2: "Cooperation and patience",
            3: "Communication and creativity",
            4: "Organization and hard work",
            5: "Freedom and adventure",
            6: "Service and responsibility",
            7: "Study and reflection",
            8: "Business and achievement",
            9: "Completion and service"
        }
        return day_energies.get(personal_day, "Balanced energy")
    
    def _calculate_overall_vibration(self, py: int, pm: int, pd: int) -> int:
        """Calculate overall vibrational number"""
        total = py + pm + pd
        return self._reduce_to_single_digit(total)
    
    def _generate_predictions(self, py: int, pm: int, pd: int, target_date: date) -> Dict[str, List[str]]:
        """Generate predictions for different life areas"""
        predictions = {
            'career': [],
            'relationships': [],
            'health': [],
            'finances': [],
            'spiritual': []
        }
        
        # Career predictions based on Personal Year
        if py == 1:
            predictions['career'].extend([
                "Excellent time for starting new career ventures",
                "Leadership opportunities will present themselves",
                "Independence in work matters is favored"
            ])
        elif py == 8:
            predictions['career'].extend([
                "Recognition and advancement are likely",
                "Business ventures show strong potential",
                "Financial rewards for past efforts"
            ])
        elif py == 4:
            predictions['career'].extend([
                "Focus on building stable career foundations",
                "Hard work will pay off in the long term",
                "Systematic approach to goals is essential"
            ])
        
        # Relationship predictions
        if py == 2:
            predictions['relationships'].extend([
                "Excellent year for partnerships and marriage",
                "Cooperation in relationships brings harmony",
                "Focus on diplomatic communication"
            ])
        elif py == 6:
            predictions['relationships'].extend([
                "Family relationships take center stage",
                "Responsibilities towards loved ones increase",
                "Home and family harmony is emphasized"
            ])
        
        # Add general predictions based on monthly and daily influences
        predictions['general'] = [
            f"Monthly focus on {self._get_monthly_focus(pm)}",
            f"Daily energy supports {self._get_daily_energy(pd)}",
            f"Overall vibration promotes {self._get_vibration_meaning(self._calculate_overall_vibration(py, pm, pd))}"
        ]
        
        return predictions
    
    def _get_vibration_meaning(self, vibration: int) -> str:
        """Get meaning for overall vibration number"""
        meanings = {
            1: "leadership and new initiatives",
            2: "cooperation and relationship building",
            3: "creative expression and communication",
            4: "practical work and foundation building",
            5: "freedom and progressive thinking",
            6: "service and family responsibilities",
            7: "spiritual development and study",
            8: "material achievement and recognition",
            9: "completion and humanitarian service"
        }
        return meanings.get(vibration, "balanced development")
    
    def _generate_recommendations(self, py: int, pm: int, pd: int) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Year-based recommendations
        if py in self.personal_year_themes:
            theme = self.personal_year_themes[py]
            recommendations.append(f"Year Theme: {theme['advice']}")
            recommendations.extend([f"Opportunity: {opp}" for opp in theme['opportunities'][:2]])
            recommendations.append(f"Be aware of: {', '.join(theme['challenges'])}")
        
        # Month-based recommendations
        recommendations.append(f"This month, focus on {self._get_monthly_focus(pm)}")
        
        # Day-based recommendations
        recommendations.append(f"Today's energy supports {self._get_daily_energy(pd)}")
        
        # Harmony recommendations
        harmony = self._calculate_cycle_harmony(py, pm, pd)
        if "tension" in harmony.lower():
            recommendations.append("Navigate conflicting energies by staying flexible and open to growth")
        elif "harmony" in harmony.lower():
            recommendations.append("Take advantage of aligned energies for maximum progress")
        
        return recommendations
    
    def _calculate_significant_dates(self, birth_date: date, target_date: date, 
                                   personal_year: int) -> tuple[List[date], List[date]]:
        """Calculate lucky and challenging dates for the current month"""
        lucky_dates = []
        challenging_dates = []
        
        # Get lucky and challenging months for this Personal Year
        year_info = self.personal_year_themes.get(personal_year, {})
        lucky_months = year_info.get('lucky_months', [])
        challenging_months = year_info.get('challenging_months', [])
        
        # Generate dates for current month
        current_month = target_date.month
        current_year = target_date.year
        
        # Lucky dates: days that reduce to Personal Year number or lucky numbers
        for day in range(1, 32):
            try:
                check_date = date(current_year, current_month, day)
                day_reduced = self._reduce_to_single_digit(day)
                
                if (day_reduced == personal_year or 
                    day_reduced in [1, 6, 9] or  # Generally lucky numbers
                    current_month in lucky_months):
                    lucky_dates.append(check_date)
                elif (day_reduced in [4, 7, 8] or  # Potentially challenging numbers
                      current_month in challenging_months):
                    challenging_dates.append(check_date)
                    
            except ValueError:
                continue  # Invalid date (e.g., Feb 30)
        
        return lucky_dates[:10], challenging_dates[:10]  # Limit to 10 each
    
    def format_cycle_report(self, result: PersonalCycleResult, target_date: Optional[date] = None) -> str:
        """Format comprehensive cycle analysis report"""
        if not target_date:
            target_date = date.today()
            
        report = []
        report.append("=== PERSONAL CYCLE ANALYSIS ===\n")
        
        # Current Cycles
        report.append(f"📅 Analysis for: {target_date.strftime('%d-%m-%Y')}")
        report.append("-" * 50)
        report.append(f"Personal Year: {result.personal_year}")
        report.append(f"Personal Month: {result.personal_month}")
        report.append(f"Personal Day: {result.personal_day}")
        report.append("")
        
        # Year Theme
        if result.personal_year in self.personal_year_themes:
            theme = self.personal_year_themes[result.personal_year]
            report.append(f"🎯 YEAR THEME: {theme['theme']}")
            report.append(f"Keywords: {', '.join(theme['keywords'])}")
            report.append(f"Advice: {theme['advice']}")
            report.append("")
        
        # Cycle Analysis
        analysis = result.cycle_analysis
        report.append("🔄 CYCLE ANALYSIS")
        report.append("-" * 30)
        report.append(f"Dominant Influence: {analysis['dominant_influence']}")
        report.append(f"Cycle Harmony: {analysis['cycle_harmony']}")
        report.append(f"Energy Level: {analysis['energy_level']}")
        report.append(f"Life Phase: {analysis['life_phase']}")
        report.append("")
        
        # Predictions
        if 'general' in result.predictions:
            report.append("🔮 CURRENT INFLUENCES")
            report.append("-" * 30)
            for prediction in result.predictions['general']:
                report.append(f"• {prediction}")
            report.append("")
        
        # Recommendations
        if result.recommendations:
            report.append("💡 RECOMMENDATIONS")
            report.append("-" * 30)
            for rec in result.recommendations:
                report.append(f"• {rec}")
            report.append("")
        
        # Lucky Dates
        if result.lucky_dates:
            report.append("🍀 FAVORABLE DATES (Current Month)")
            report.append("-" * 30)
            date_strings = [d.strftime('%d-%m') for d in result.lucky_dates[:5]]
            report.append(f"Best days: {', '.join(date_strings)}")
            report.append("")
        
        return "\n".join(report)


if __name__ == "__main__":
    # Test the Personal Cycle calculator
    calculator = PersonalCycleCalculator()
    
    # Test with sample birth date
    result = calculator.calculate_personal_cycles("29-01-1979", "20-08-2025")
    
    print(calculator.format_cycle_report(result, date(2025, 8, 20)))
