#!/usr/bin/env python3
"""
Simple script to check if XML file can be read
"""

import os

def check_xml_file():
    """Check if XML file can be read"""
    print("Checking XML file access")
    print("=" * 30)
    
    # Current directory
    print(f"Current directory: {os.getcwd()}")
    
    # Check parent directory
    parent_dir = ".."
    print(f"Parent directory: {os.path.abspath(parent_dir)}")
    
    # List files in parent
    try:
        files = os.listdir(parent_dir)
        xml_files = [f for f in files if f.endswith('.xml')]
        print(f"XML files in parent: {xml_files}")
    except Exception as e:
        print(f"Error listing parent: {e}")
        return False
    
    # Try to read the file
    xml_path = "../modified_sms_v2.xml"
    print(f"\nTrying to read: {xml_path}")
    print(f"File exists: {os.path.exists(xml_path)}")
    
    if os.path.exists(xml_path):
        try:
            with open(xml_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"Successfully read file!")
            print(f"File size: {len(content)} characters")
            print(f"First 100 characters:")
            print(content[:100])
            return True
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
    else:
        print(f"File does not exist")
        return False

if __name__ == "__main__":
    check_xml_file()
