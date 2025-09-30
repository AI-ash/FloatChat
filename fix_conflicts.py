#!/usr/bin/env python3
"""
Fix all Git merge conflicts by removing conflict markers
"""

import os
import re
import glob

def fix_merge_conflicts_in_file(filepath):
    """Fix merge conflicts in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has merge conflicts
        if '<<<<<<< HEAD' not in content:
            return False
        
        print(f"Fixing conflicts in: {filepath}")
        
        # Remove merge conflict markers and keep the HEAD version
        # Pattern: <<<<<<< HEAD ... ======= ... >>>>>>> commit
        pattern = r'<<<<<<< HEAD\n(.*?)\n=======\n.*?\n>>>>>>> [^\n]+\n'
        
        # Replace with just the HEAD content
        fixed_content = re.sub(pattern, r'\1\n', content, flags=re.DOTALL)
        
        # Write back the fixed content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        return True
        
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    """Fix all merge conflicts in the project"""
    print("🔧 Fixing Git merge conflicts...")
    
    # Find all Python and text files
    file_patterns = [
        '*.py',
        '*.md', 
        '*.txt',
        '*.yml',
        '*.yaml',
        '*.json'
    ]
    
    files_fixed = 0
    
    for pattern in file_patterns:
        for filepath in glob.glob(pattern, recursive=True):
            if fix_merge_conflicts_in_file(filepath):
                files_fixed += 1
        
        # Also check subdirectories
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith(pattern.replace('*', '')):
                    full_path = os.path.join(root, file)
                    if fix_merge_conflicts_in_file(full_path):
                        files_fixed += 1
    
    print(f"✅ Fixed merge conflicts in {files_fixed} files")

if __name__ == "__main__":
    main()