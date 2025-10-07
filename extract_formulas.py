#!/usr/bin/env python3
"""
Script to extract all formulas from Sheet 1 of the Numerology Excel file.
This script extracts formulas as strings (not evaluated) for integration into the codebase.
"""

import openpyxl
from datetime import datetime
import os

def extract_formulas_from_excel(excel_path: str, sheet_name: str = None) -> dict:
    """
    Extract all formulas from the specified sheet of an Excel file.
    
    Args:
        excel_path: Path to the Excel file
        sheet_name: Name of the sheet (if None, uses the first sheet)
    
    Returns:
        Dictionary with cell addresses as keys and formula strings as values
    """
    formulas = {}
    
    try:
        # Open the workbook
        workbook = openpyxl.load_workbook(excel_path, data_only=False)
        
        # Get the sheet (first sheet if no specific name provided)
        if sheet_name:
            if sheet_name in workbook.sheetnames:
                sheet = workbook[sheet_name]
            else:
                print(f"Warning: Sheet '{sheet_name}' not found. Available sheets: {workbook.sheetnames}")
                sheet = workbook.active
        else:
            sheet = workbook.active
        
        print(f"Extracting formulas from sheet: {sheet.title}")
        print(f"Sheet dimensions: {sheet.max_row} rows x {sheet.max_column} columns")
        
        # Iterate through all cells in the used range
        for row in sheet.iter_rows(min_row=1, max_row=sheet.max_row, 
                                  min_col=1, max_col=sheet.max_column):
            for cell in row:
                if cell.value is not None and str(cell.value).startswith('='):
                    # This is a formula
                    cell_address = f"{cell.column_letter}{cell.row}"
                    formulas[cell_address] = str(cell.value)
        
        workbook.close()
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return {}
    
    return formulas

def create_formula_log(formulas: dict, excel_path: str) -> str:
    """
    Create a markdown log of extracted formulas.
    
    Args:
        formulas: Dictionary of cell addresses and formulas
        excel_path: Path to the Excel file
    
    Returns:
        Path to the created markdown log file
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_content = f"""# Excel Formula Extraction Log

**Timestamp:** {timestamp}
**Source File:** {os.path.basename(excel_path)}
**Total Formulas Extracted:** {len(formulas)}

## Extracted Formulas

"""
    
    if not formulas:
        log_content += "No formulas found in the specified sheet.\n"
    else:
        # Sort formulas by cell address for better organization
        sorted_formulas = sorted(formulas.items(), key=lambda x: (int(''.join(filter(str.isdigit, x[0]))), x[0]))
        
        for cell_address, formula in sorted_formulas:
            log_content += f"### Cell {cell_address}\n"
            log_content += f"```excel\n{formula}\n```\n\n"
    
    # Write to log file
    log_path = "formula_extraction_log.md"
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(log_content)
    
    return log_path

def main():
    """Main function to extract formulas and create log."""
    # Try both .xlsm and .xlsx files
    excel_files = [
        "Numerology Calculator savi's enhanced.xlsm",
        "Numerology Calculator savi's enhanced.xlsx"
    ]
    
    for excel_file in excel_files:
        if os.path.exists(excel_file):
            print(f"Processing: {excel_file}")
            
            # Extract formulas from Sheet 1 (or first sheet)
            formulas = extract_formulas_from_excel(excel_file)
            
            print(f"Found {len(formulas)} formulas")
            
            # Create log file
            log_path = create_formula_log(formulas, excel_file)
            print(f"Formula log created: {log_path}")
            
            # Display a few sample formulas
            if formulas:
                print("\nSample formulas:")
                for i, (cell, formula) in enumerate(list(formulas.items())[:5]):
                    print(f"  {cell}: {formula}")
                if len(formulas) > 5:
                    print(f"  ... and {len(formulas) - 5} more")
            
            break
    else:
        print("No Excel files found!")

if __name__ == "__main__":
    main()
