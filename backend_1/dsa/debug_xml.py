#!/usr/bin/env python3
"""
Debug script to test XML file loading
"""

import os
import sys

def debug_file_paths():
    """Debug file path issues"""
    print("Debugging XML File Loading")
    print("=" * 40)
    
    # Current working directory
    print(f"Current working directory: {os.getcwd()}")
    
    # Check if we're in the right directory
    if not os.path.basename(os.getcwd()) == 'backend_1':
        print("Not in backend_1 directory!")
        return
    
    # Check parent directory
    parent_dir = ".."
    print(f"Parent directory: {os.path.abspath(parent_dir)}")
    
    # List files in parent directory
    try:
        parent_files = os.listdir(parent_dir)
        print(f"Files in parent directory:")
        xml_files = [f for f in parent_files if f.endswith('.xml')]
        for file in xml_files:
            print(f"   {file}")
        if not xml_files:
            print("   No XML files found")
    except Exception as e:
        print(f"Error listing parent directory: {e}")
    
    # Test different paths
    test_paths = [
        "../modified_sms_v2.xml",
        "modified_sms_v2.xml",
        os.path.join("..", "modified_sms_v2.xml")
    ]
    
    print(f"\nTesting file paths:")
    for path in test_paths:
        exists = os.path.exists(path)
        abs_path = os.path.abspath(path)
        print(f"   {'FOUND' if exists else 'NOT FOUND'} {path} -> {abs_path}")
    
    # Try to read the file
    xml_path = "../modified_sms_v2.xml"
    if os.path.exists(xml_path):
        try:
            with open(xml_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"\nSuccessfully read XML file!")
            print(f"File size: {len(content)} characters")
            print(f"First 200 characters:")
            print(content[:200])
        except Exception as e:
            print(f"Error reading file: {e}")
    else:
        print(f"\nXML file not found at {xml_path}")

if __name__ == "__main__":
    debug_file_paths()
