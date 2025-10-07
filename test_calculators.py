#!/usr/bin/env python3
"""Test script for advanced calculators"""

from lo_shu_calculator import LoShuGridCalculator
from karmic_calculator import KarmicAnalysisCalculator  
from personal_cycle_calculator import PersonalCycleCalculator

print('Testing calculators...')

# Test Lo-Shu Grid
lo_shu = LoShuGridCalculator()
result = lo_shu.calculate_from_birth_date('29-01-1979')
print(f'Lo-Shu Grid: {result.strength_score:.1f}/100')

# Test Karmic Analysis
karmic = KarmicAnalysisCalculator()
result = karmic.analyze_name('JOHN SMITH')
print(f'Karmic Analysis: {result.analysis["overall_profile"]["personality_type"]}')

# Test Personal Cycles
cycles = PersonalCycleCalculator()
result = cycles.calculate_personal_cycles('29-01-1979')
print(f'Personal Year: {result.personal_year}')

print('All calculators working!')
