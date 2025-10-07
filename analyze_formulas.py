#!/usr/bin/env python3
"""
Formula Analysis Script for Numerology Excel Integration
Analyzes extracted formulas and categorizes them for integration into the Python codebase.
"""

import re
from collections import defaultdict
from datetime import datetime

def load_extracted_formulas(log_file: str = "formula_extraction_log.md") -> dict:
    """Load formulas from the extraction log file."""
    formulas = {}
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract formulas using regex
        pattern = r'### Cell ([A-Z]+\d+)\n```excel\n(.*?)\n```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for cell, formula in matches:
            formulas[cell] = formula.strip()
    
    except Exception as e:
        print(f"Error loading formulas: {e}")
    
    return formulas

def analyze_formula_patterns(formulas: dict) -> dict:
    """Analyze formulas and categorize them by function types."""
    categories = defaultdict(list)
    
    # Define function patterns
    patterns = {
        'text_extraction': [r'MID\(', r'LEFT\(', r'RIGHT\(', r'LEN\('],
        'lookup_functions': [r'INDEX\(', r'MATCH\(', r'VLOOKUP\(', r'HLOOKUP\('],
        'mathematical': [r'MOD\(', r'SUM\(', r'ABS\(', r'ROUND\(', r'INT\('],
        'conditional': [r'IF\(', r'IFERROR\(', r'IFNA\('],
        'text_functions': [r'CONCATENATE\(', r'TRIM\(', r'UPPER\(', r'LOWER\('],
        'date_functions': [r'DATE\(', r'YEAR\(', r'MONTH\(', r'DAY\('],
        'logical': [r'AND\(', r'OR\(', r'NOT\('],
        'counting': [r'COUNT\(', r'COUNTA\(', r'COUNTIF\('],
        'simple_arithmetic': [r'\+', r'\-', r'\*', r'\/']
    }
    
    for cell, formula in formulas.items():
        formula_upper = formula.upper()
        
        # Check each category
        for category, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, formula_upper):
                    categories[category].append({
                        'cell': cell,
                        'formula': formula,
                        'pattern': pattern
                    })
                    break  # Only categorize once per formula
    
    return categories

def identify_numerology_patterns(formulas: dict) -> dict:
    """Identify specific numerology calculation patterns."""
    numerology_patterns = {
        'name_parsing': [],
        'number_reduction': [],
        'chaldean_mapping': [],
        'date_calculations': [],
        'compatibility': [],
        'interpretations': []
    }
    
    for cell, formula in formulas.items():
        formula_upper = formula.upper()
        
        # Name parsing patterns (extracting characters)
        if re.search(r'MID\([A-Z]\d+,\d+,1\)', formula_upper):
            numerology_patterns['name_parsing'].append({
                'cell': cell,
                'formula': formula,
                'type': 'character_extraction'
            })
        
        # Number reduction patterns (MOD operations for reducing to single digits)
        if re.search(r'MOD\(.*,9\)', formula_upper):
            numerology_patterns['number_reduction'].append({
                'cell': cell,
                'formula': formula,
                'type': 'digit_reduction'
            })
        
        # Lookup patterns (likely for Chaldean mappings and interpretations)
        if re.search(r'INDEX\(.*MATCH\(', formula_upper):
            if 'AH' in formula_upper or 'AI' in formula_upper:  # Common lookup table ranges
                numerology_patterns['chaldean_mapping'].append({
                    'cell': cell,
                    'formula': formula,
                    'type': 'chaldean_lookup'
                })
            else:
                numerology_patterns['interpretations'].append({
                    'cell': cell,
                    'formula': formula,
                    'type': 'interpretation_lookup'
                })
        
        # Date-related calculations
        if re.search(r'(YEAR|MONTH|DAY)\(', formula_upper):
            numerology_patterns['date_calculations'].append({
                'cell': cell,
                'formula': formula,
                'type': 'date_processing'
            })
    
    return numerology_patterns

def generate_analysis_report(categories: dict, numerology_patterns: dict, formulas: dict) -> str:
    """Generate a comprehensive analysis report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# Formula Analysis Report

**Generated:** {timestamp}
**Total Formulas Analyzed:** {len(formulas)}

## Executive Summary

This analysis categorizes the {len(formulas)} extracted Excel formulas to guide their integration into the Python numerology application.

## General Function Categories

"""
    
    # General categories
    for category, items in sorted(categories.items()):
        report += f"### {category.replace('_', ' ').title()} ({len(items)} formulas)\n\n"
        
        if items:
            # Show top 3 examples
            for i, item in enumerate(items[:3]):
                report += f"**Example {i+1}:** Cell {item['cell']}\n"
                report += f"```excel\n{item['formula']}\n```\n\n"
            
            if len(items) > 3:
                report += f"*...and {len(items) - 3} more similar formulas*\n\n"
    
    # Numerology-specific patterns
    report += "## Numerology-Specific Patterns\n\n"
    
    for pattern_type, items in numerology_patterns.items():
        if items:
            report += f"### {pattern_type.replace('_', ' ').title()} ({len(items)} formulas)\n\n"
            
            # Show examples
            for i, item in enumerate(items[:2]):
                report += f"**Cell {item['cell']}:** {item['type']}\n"
                report += f"```excel\n{item['formula']}\n```\n\n"
            
            if len(items) > 2:
                report += f"*...and {len(items) - 2} more*\n\n"
    
    # Integration recommendations
    report += """## Integration Recommendations

### Priority 1: Core Calculations
1. **Number Reduction Formulas** - Integrate MOD operations for proper Chaldean digit reduction
2. **Name Parsing** - Extract character-by-character parsing logic
3. **Chaldean Mapping** - Implement lookup table logic for letter-to-number conversion

### Priority 2: Enhanced Features
1. **Date Calculations** - Add any missing birth date processing
2. **Interpretation Lookups** - Integrate comprehensive interpretation tables
3. **Compatibility Logic** - Add relationship compatibility calculations

### Priority 3: Advanced Features
1. **Conditional Logic** - Implement complex decision trees from IF statements
2. **Text Processing** - Add advanced name processing capabilities
3. **Counting Functions** - Implement statistical analysis features

## Next Steps

1. **Manual Review** - Examine specific formulas for unique calculation methods
2. **Mapping Exercise** - Map Excel formulas to existing Python methods
3. **Gap Analysis** - Identify missing functionality in current implementation
4. **Implementation Plan** - Create detailed integration roadmap
5. **Testing Strategy** - Develop validation tests against Excel results

## Key Insights

- Heavy use of character extraction suggests sophisticated name analysis
- MOD operations indicate proper numerological digit reduction
- Complex INDEX/MATCH patterns suggest rich interpretation databases
- Date functions may reveal advanced birth date analysis methods

---

*This analysis provides the foundation for systematic integration of Excel formulas into the Python numerology application.*
"""
    
    return report

def main():
    """Main analysis function."""
    print("Loading extracted formulas...")
    formulas = load_extracted_formulas()
    
    if not formulas:
        print("No formulas found. Make sure formula_extraction_log.md exists.")
        return
    
    print(f"Analyzing {len(formulas)} formulas...")
    
    # Categorize formulas
    categories = analyze_formula_patterns(formulas)
    
    # Identify numerology patterns
    numerology_patterns = identify_numerology_patterns(formulas)
    
    # Generate report
    report = generate_analysis_report(categories, numerology_patterns, formulas)
    
    # Save report
    report_file = "formula_analysis_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Analysis complete! Report saved to: {report_file}")
    
    # Print summary
    print("\nAnalysis Summary:")
    print("================")
    for category, items in sorted(categories.items()):
        print(f"{category.replace('_', ' ').title()}: {len(items)} formulas")
    
    print("\nNumerology Patterns:")
    print("===================")
    for pattern, items in numerology_patterns.items():
        if items:
            print(f"{pattern.replace('_', ' ').title()}: {len(items)} formulas")

if __name__ == "__main__":
    main()
