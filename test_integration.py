#!/usr/bin/env python3
"""
Test script to validate Chaldean reduction method against Excel formulas
This ensures our Python implementation matches the Excel calculations exactly.
"""

from chaldean_calculator import ChaldeanNumerology

def test_chaldean_reduction():
    """Test the new Chaldean reduction method against known Excel results."""
    calc = ChaldeanNumerology()
    
    print("Testing Chaldean Reduction Method")
    print("=" * 40)
    
    # Test cases based on Excel MOD formula: =MOD(number-1,9)+1
    test_cases = [
        # (input_number, expected_result)
        (1, 1),    # MOD(1-1,9)+1 = MOD(0,9)+1 = 0+1 = 1
        (9, 9),    # MOD(9-1,9)+1 = MOD(8,9)+1 = 8+1 = 9
        (10, 1),   # MOD(10-1,9)+1 = MOD(9,9)+1 = 0+1 = 1
        (18, 9),   # MOD(18-1,9)+1 = MOD(17,9)+1 = 8+1 = 9
        (19, 1),   # MOD(19-1,9)+1 = MOD(18,9)+1 = 0+1 = 1
        (27, 9),   # MOD(27-1,9)+1 = MOD(26,9)+1 = 8+1 = 9
        (28, 1),   # MOD(28-1,9)+1 = MOD(27,9)+1 = 0+1 = 1
        (45, 9),   # MOD(45-1,9)+1 = MOD(44,9)+1 = 8+1 = 9
        (100, 1),  # MOD(100-1,9)+1 = MOD(99,9)+1 = 0+1 = 1
    ]
    
    # Test master numbers (should be preserved)
    master_cases = [
        (11, 11),
        (22, 22),
        (33, 33),
    ]
    
    all_passed = True
    
    print("Regular Numbers:")
    for input_num, expected in test_cases:
        result = calc.chaldean_reduce(input_num)
        passed = result == expected
        all_passed = all_passed and passed
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {input_num:3d} -> {result} (expected {expected}) {status}")
    
    print("\\nMaster Numbers:")
    for input_num, expected in master_cases:
        result = calc.chaldean_reduce(input_num)
        passed = result == expected
        all_passed = all_passed and passed
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {input_num:3d} -> {result} (expected {expected}) {status}")
    
    print("\\n" + "=" * 40)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Chaldean reduction is working correctly.")
    else:
        print("⚠️  SOME TESTS FAILED! Please check the implementation.")
    
    return all_passed

def test_name_calculation():
    """Test name calculation with the new method."""
    calc = ChaldeanNumerology()
    
    print("\\nTesting Name Calculations")
    print("=" * 40)
    
    # Test a simple name
    test_name = "JOHN"
    compound, reduced, letter_values = calc.calculate_name_number(test_name)
    
    print(f"Name: {test_name}")
    print(f"Letter values: {letter_values}")
    print(f"Sum (compound): {compound}")
    print(f"Reduced (Chaldean): {reduced}")
    
    # Manual calculation for verification
    # J=1, O=7, H=5, N=5
    # Total = 1 + 7 + 5 + 5 = 18
    # Chaldean reduction: MOD(18-1,9)+1 = MOD(17,9)+1 = 8+1 = 9
    expected_total = 18
    expected_reduced = 9
    
    total_correct = compound == expected_total
    reduced_correct = reduced == expected_reduced
    
    print(f"Expected compound: {expected_total} (got {compound}) {'✅' if total_correct else '❌'}")
    print(f"Expected reduced: {expected_reduced} (got {reduced}) {'✅' if reduced_correct else '❌'}")
    
    return total_correct and reduced_correct

def compare_methods():
    """Compare old vs new reduction methods."""
    calc = ChaldeanNumerology()
    
    print("\\nComparing Reduction Methods")
    print("=" * 40)
    
    test_numbers = [10, 18, 19, 27, 28, 36, 45, 54, 63]
    
    print("Number | Old Method | New Chaldean | Difference")
    print("-------|------------|--------------|----------")
    
    for num in test_numbers:
        old_result = calc.reduce_to_single_digit(num)
        new_result = calc.chaldean_reduce(num)
        different = old_result != new_result
        diff_mark = " ⚠️ " if different else "   "
        print(f"  {num:2d}   |     {old_result}      |      {new_result}       |{diff_mark}")

def main():
    """Run all tests."""
    print("🧪 CHALDEAN FORMULA VALIDATION TESTS")
    print("🔍 Verifying Excel formula integration")
    print("📊 Testing against MOD-based reduction")
    print()
    
    # Test the core reduction method
    reduction_passed = test_chaldean_reduction()
    
    # Test name calculation
    name_passed = test_name_calculation()
    
    # Compare methods
    compare_methods()
    
    print("\\n" + "=" * 50)
    if reduction_passed and name_passed:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("✅ Excel formula integration successful")
        print("✅ Chaldean calculations are now authentic")
    else:
        print("⚠️  VALIDATION ISSUES DETECTED")
        print("❌ Please review the implementation")
    
    print("\\n📝 Integration complete! Check the web app for updated calculations.")

if __name__ == "__main__":
    main()
