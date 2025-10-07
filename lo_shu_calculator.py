"""
Lo-Shu Grid Calculator for North Indian Chaldean Numerology
Based on traditional 3x3 magic square with Raj Yog analysis
"""

from typing import Dict, List, Any
from datetime import datetime
from dataclasses import dataclass


@dataclass
class LoShuGridResult:
    """Result container for Lo-Shu Grid analysis"""
    grid: List[List[int]]
    missing_numbers: List[int]
    repeated_numbers: Dict[int, int]
    planes: Dict[str, Dict[str, Any]]
    raj_yog: List[Dict[str, Any]]
    recommendations: List[str]
    strength_score: float


class LoShuGridCalculator:
    """Calculator for Lo-Shu Grid numerological analysis"""
    
    def __init__(self):
        # Traditional Lo-Shu Grid template (3x3 magic square)
        self.base_grid = [
            [4, 9, 2],
            [3, 5, 7],
            [8, 1, 6]
        ]
        
        # Plane definitions
        self.planes = {
            'intellectual': {
                'positions': [(0, 0), (0, 1), (0, 2)],  # Top row: 4, 9, 2
                'numbers': [4, 9, 2],
                'description': 'Mental abilities, thinking patterns, learning'
            },
            'emotional': {
                'positions': [(1, 0), (1, 1), (1, 2)],  # Middle row: 3, 5, 7
                'numbers': [3, 5, 7],
                'description': 'Feelings, intuition, emotional responses'
            },
            'practical': {
                'positions': [(2, 0), (2, 1), (2, 2)],  # Bottom row: 8, 1, 6
                'numbers': [8, 1, 6],
                'description': 'Physical actions, material world, execution'
            }
        }
        
        # Raj Yog (auspicious) combinations
        self.raj_yog_patterns = [
            # Horizontal lines
            {'pattern': [4, 9, 2], 'type': 'horizontal', 'name': 'Intellectual Raj Yog'},
            {'pattern': [3, 5, 7], 'type': 'horizontal', 'name': 'Emotional Raj Yog'},
            {'pattern': [8, 1, 6], 'type': 'horizontal', 'name': 'Practical Raj Yog'},
            # Vertical lines
            {'pattern': [4, 3, 8], 'type': 'vertical', 'name': 'Left Raj Yog'},
            {'pattern': [9, 5, 1], 'type': 'vertical', 'name': 'Center Raj Yog'},
            {'pattern': [2, 7, 6], 'type': 'vertical', 'name': 'Right Raj Yog'},
            # Diagonal lines
            {'pattern': [4, 5, 6], 'type': 'diagonal', 'name': 'Main Diagonal Raj Yog'},
            {'pattern': [2, 5, 8], 'type': 'diagonal', 'name': 'Anti-Diagonal Raj Yog'}
        ]
    
    def calculate_from_birth_date(self, birth_date: str) -> LoShuGridResult:
        """Calculate Lo-Shu Grid from birth date (DD-MM-YYYY format)"""
        try:
            # Parse birth date
            date_obj = datetime.strptime(birth_date, "%d-%m-%Y")
            day = date_obj.day
            month = date_obj.month
            year = date_obj.year
            
            # Extract all digits from birth date
            digits = []
            digits.extend([int(d) for d in str(day).zfill(2)])
            digits.extend([int(d) for d in str(month).zfill(2)])
            digits.extend([int(d) for d in str(year)])
            
            # Remove zeros and count digit frequency
            digit_counts = {}
            for digit in digits:
                if digit != 0:  # Ignore zeros in numerology
                    digit_counts[digit] = digit_counts.get(digit, 0) + 1
            
            return self._analyze_grid(digit_counts, birth_date)
            
        except ValueError as e:
            raise ValueError(f"Invalid birth date format. Use DD-MM-YYYY: {e}")
    
    def calculate_from_digits(self, digits: List[int]) -> LoShuGridResult:
        """Calculate Lo-Shu Grid from list of digits"""
        # Count digit frequency
        digit_counts = {}
        for digit in digits:
            if 1 <= digit <= 9:  # Only count valid numerology digits
                digit_counts[digit] = digit_counts.get(digit, 0) + 1
        
        return self._analyze_grid(digit_counts)
    
    def _analyze_grid(self, digit_counts: Dict[int, int], birth_date: str = "") -> LoShuGridResult:
        """Analyze the Lo-Shu Grid based on digit counts"""
        
        # Create grid with counts
        grid = [[0 for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                number = self.base_grid[i][j]
                grid[i][j] = digit_counts.get(number, 0)
        
        # Find missing and repeated numbers
        missing_numbers = [i for i in range(1, 10) if i not in digit_counts]
        repeated_numbers = {k: v for k, v in digit_counts.items() if v > 1}
        
        # Analyze planes
        planes_analysis = self._analyze_planes(digit_counts)
        
        # Check for Raj Yog
        raj_yog = self._check_raj_yog(digit_counts)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            missing_numbers, repeated_numbers, planes_analysis, raj_yog
        )
        
        # Calculate strength score
        strength_score = self._calculate_strength_score(
            missing_numbers, repeated_numbers, raj_yog
        )
        
        return LoShuGridResult(
            grid=grid,
            missing_numbers=missing_numbers,
            repeated_numbers=repeated_numbers,
            planes=planes_analysis,
            raj_yog=raj_yog,
            recommendations=recommendations,
            strength_score=strength_score
        )
    
    def _analyze_planes(self, digit_counts: Dict[int, int]) -> Dict[str, Dict[str, Any]]:
        """Analyze the three planes of consciousness"""
        planes_analysis = {}
        
        for plane_name, plane_info in self.planes.items():
            numbers = plane_info['numbers']
            present_count = sum(1 for num in numbers if num in digit_counts)
            total_occurrences = sum(digit_counts.get(num, 0) for num in numbers)
            
            # Determine plane strength
            if present_count == 3:
                strength = "Strong"
            elif present_count == 2:
                strength = "Moderate"
            elif present_count == 1:
                strength = "Weak"
            else:
                strength = "Empty"
            
            planes_analysis[plane_name] = {
                'strength': strength,
                'present_numbers': [num for num in numbers if num in digit_counts],
                'missing_numbers': [num for num in numbers if num not in digit_counts],
                'total_occurrences': total_occurrences,
                'description': plane_info['description'],
                'advice': self._get_plane_advice(plane_name, strength, present_count)
            }
        
        return planes_analysis
    
    def _check_raj_yog(self, digit_counts: Dict[int, int]) -> List[Dict[str, Any]]:
        """Check for Raj Yog (auspicious) combinations"""
        raj_yog_found = []
        
        for pattern_info in self.raj_yog_patterns:
            pattern = pattern_info['pattern']
            if all(num in digit_counts for num in pattern):
                raj_yog_found.append({
                    'name': pattern_info['name'],
                    'type': pattern_info['type'],
                    'pattern': pattern,
                    'strength': self._calculate_raj_yog_strength(pattern, digit_counts),
                    'benefits': self._get_raj_yog_benefits(pattern_info['name'])
                })
        
        return raj_yog_found
    
    def _calculate_raj_yog_strength(self, pattern: List[int], digit_counts: Dict[int, int]) -> str:
        """Calculate strength of a Raj Yog pattern"""
        total_occurrences = sum(digit_counts.get(num, 0) for num in pattern)
        
        if total_occurrences >= 6:
            return "Very Strong"
        elif total_occurrences >= 4:
            return "Strong"
        elif total_occurrences >= 3:
            return "Moderate"
        else:
            return "Weak"
    
    def _get_raj_yog_benefits(self, raj_yog_name: str) -> List[str]:
        """Get benefits for specific Raj Yog patterns"""
        benefits_map = {
            'Intellectual Raj Yog': [
                "Enhanced mental abilities and learning capacity",
                "Success in academic and intellectual pursuits",
                "Good decision-making and analytical skills"
            ],
            'Emotional Raj Yog': [
                "Strong emotional intelligence and intuition",
                "Harmonious relationships and social connections",
                "Artistic and creative abilities"
            ],
            'Practical Raj Yog': [
                "Excellent execution and implementation skills",
                "Material success and financial stability",
                "Strong physical health and stamina"
            ],
            'Center Raj Yog': [
                "Balanced personality and centered approach",
                "Leadership qualities and influence",
                "Spiritual growth and inner wisdom"
            ]
        }
        
        return benefits_map.get(raj_yog_name, ["General auspicious influences"])
    
    def _get_plane_advice(self, plane_name: str, strength: str, present_count: int) -> str:
        """Get advice based on plane analysis"""
        advice_map = {
            'intellectual': {
                'Strong': "Excellent mental faculties. Use your analytical abilities for leadership roles.",
                'Moderate': "Good thinking abilities. Focus on developing decision-making skills.",
                'Weak': "Enhance mental development through reading, learning, and strategic thinking.",
                'Empty': "Important to develop intellectual abilities. Engage in educational activities."
            },
            'emotional': {
                'Strong': "Strong emotional intelligence. Great for counseling and people-oriented careers.",
                'Moderate': "Good emotional balance. Work on expressing feelings constructively.",
                'Weak': "Develop emotional awareness through meditation and introspection.",
                'Empty': "Focus on emotional development and building meaningful relationships."
            },
            'practical': {
                'Strong': "Excellent at implementation and material success. Great for business ventures.",
                'Moderate': "Good practical skills. Focus on consistent action and follow-through.",
                'Weak': "Improve practical skills through hands-on activities and physical exercise.",
                'Empty': "Essential to develop practical abilities for material success."
            }
        }
        
        return advice_map.get(plane_name, {}).get(strength, "General development needed")
    
    def _generate_recommendations(self, missing_numbers: List[int], repeated_numbers: Dict[int, int], 
                                planes_analysis: Dict[str, Dict[str, Any]], raj_yog: List[Dict[str, Any]]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Missing numbers recommendations
        if missing_numbers:
            recommendations.append(f"Missing Numbers ({', '.join(map(str, missing_numbers))}): " +
                                 "Consider incorporating these numbers in important decisions, dates, or personal items.")
        
        # Repeated numbers insights
        if repeated_numbers:
            for num, count in repeated_numbers.items():
                recommendations.append(f"Number {num} appears {count} times: This indicates strong {self._get_number_meaning(num)} energy.")
        
        # Plane-specific recommendations
        weak_planes = [plane for plane, analysis in planes_analysis.items() if analysis['strength'] in ['Weak', 'Empty']]
        if weak_planes:
            recommendations.append(f"Focus on developing {', '.join(weak_planes)} plane(s) for balanced growth.")
        
        # Raj Yog benefits
        if raj_yog:
            recommendations.append(f"You have {len(raj_yog)} active Raj Yog pattern(s) - this indicates natural auspicious influences.")
        else:
            recommendations.append("Work on creating more balanced number combinations for enhanced fortune.")
        
        return recommendations
    
    def _get_number_meaning(self, number: int) -> str:
        """Get meaning of individual numbers"""
        meanings = {
            1: "leadership and independence",
            2: "cooperation and sensitivity", 
            3: "creativity and communication",
            4: "stability and hard work",
            5: "freedom and adventure",
            6: "nurturing and responsibility",
            7: "spirituality and analysis",
            8: "material success and authority",
            9: "humanitarianism and completion"
        }
        return meanings.get(number, "unknown")
    
    def _calculate_strength_score(self, missing_numbers: List[int], repeated_numbers: Dict[int, int], 
                                raj_yog: List[Dict[str, Any]]) -> float:
        """Calculate overall grid strength score (0-100)"""
        score = 50.0  # Base score
        
        # Deduct for missing numbers
        score -= len(missing_numbers) * 5
        
        # Add for balanced repetitions
        for count in repeated_numbers.values():
            if count == 2:
                score += 5
            elif count == 3:
                score += 8
            elif count > 3:
                score += 10
        
        # Add for Raj Yog patterns
        score += len(raj_yog) * 10
        
        # Ensure score is within bounds
        return max(0.0, min(100.0, score))
    
    def format_grid_display(self, result: LoShuGridResult) -> str:
        """Format grid for display"""
        grid_str = "Lo-Shu Grid Analysis:\n"
        grid_str += "┌─────┬─────┬─────┐\n"
        
        for i in range(3):
            grid_str += "│"
            for j in range(3):
                base_num = self.base_grid[i][j]
                count = result.grid[i][j]
                if count == 0:
                    grid_str += f"  {base_num}  │"
                else:
                    grid_str += f" {base_num}({count})│"
            grid_str += "\n"
            if i < 2:
                grid_str += "├─────┼─────┼─────┤\n"
        
        grid_str += "└─────┴─────┴─────┘\n"
        return grid_str


if __name__ == "__main__":
    # Test the Lo-Shu Grid calculator
    calculator = LoShuGridCalculator()
    
    # Test with sample birth date
    result = calculator.calculate_from_birth_date("29-01-1979")
    
    print(calculator.format_grid_display(result))
    print(f"\nStrength Score: {result.strength_score:.1f}/100")
    print(f"Missing Numbers: {result.missing_numbers}")
    print(f"Repeated Numbers: {result.repeated_numbers}")
    print(f"Raj Yog Patterns: {len(result.raj_yog)}")
    
    for recommendation in result.recommendations:
        print(f"• {recommendation}")
