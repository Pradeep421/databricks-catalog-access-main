#!/usr/bin/env python3
"""
Catalog Validation Script
Validates catalog naming conventions and checks for duplicates
"""

import re
import sys
import json
from typing import Dict, List, Tuple


class CatalogValidator:
    """Validates Databricks catalog configurations"""
    
    # Naming convention: lowercase letters, numbers, underscores
    CATALOG_NAME_PATTERN = re.compile(r'^[a-z0-9_]+$')
    
    # Minimum and maximum catalog name length
    MIN_NAME_LENGTH = 3
    MAX_NAME_LENGTH = 64
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate_catalog_name(self, name: str) -> bool:
        """Validate catalog name format and length"""
        if not name:
            self.errors.append("Catalog name is required")
            return False
        
        if len(name) < self.MIN_NAME_LENGTH:
            self.errors.append(f"Catalog name must be at least {self.MIN_NAME_LENGTH} characters long")
            return False
        
        if len(name) > self.MAX_NAME_LENGTH:
            self.errors.append(f"Catalog name must not exceed {self.MAX_NAME_LENGTH} characters")
            return False
        
        if not self.CATALOG_NAME_PATTERN.match(name):
            self.errors.append(
                f"Catalog name '{name}' is invalid. "
                "Must contain only lowercase letters, numbers, and underscores."
            )
            return False
        
        return True
    
    def validate_owner(self, owner: str) -> bool:
        """Validate catalog owner"""
        if not owner:
            self.errors.append("Catalog owner is required")
            return False
        
        if len(owner.strip()) == 0:
            self.errors.append("Catalog owner cannot be empty")
            return False
        
        return True
    
    def validate_tag(self, tag: str) -> bool:
        """Validate environment tag"""
        valid_tags = ['dev', 'staging', 'prod', 'development', 'production']
        
        if not tag:
            self.errors.append("Environment tag is required")
            return False
        
        if tag.lower() not in valid_tags:
            self.warnings.append(
                f"Tag '{tag}' is not in standard list: {', '.join(valid_tags)}. "
                "Consider using a standard tag."
            )
        
        return True
    
    def validate_reader_groups(self, groups: List[str]) -> bool:
        """Validate reader groups (mandatory)"""
        if not groups or len(groups) == 0:
            self.errors.append("At least one reader group is required")
            return False
        
        for group in groups:
            if not group or not group.strip():
                self.errors.append("Reader group cannot be empty")
                return False
        
        return True
    
    def validate_groups(self, groups: List[str], group_type: str = 'group') -> bool:
        """Validate group list format"""
        if not groups:
            return True  # Optional groups
        
        for group in groups:
            if not group or not group.strip():
                self.errors.append(f"{group_type} cannot be empty")
                return False
        
        return True
    
    def validate_catalog_config(self, catalog_config: Dict) -> bool:
        """Validate complete catalog configuration"""
        self.errors.clear()
        self.warnings.clear()
        
        # Validate required fields
        if 'catalog_name' not in catalog_config:
            self.errors.append("Missing 'catalog_name' field")
            return False
        
        catalog_name = catalog_config['catalog_name']
        
        if 'owner' not in catalog_config:
            self.errors.append("Missing 'owner' field")
            return False
        
        owner = catalog_config['owner']
        
        if 'tag' not in catalog_config:
            self.errors.append("Missing 'tag' field")
            return False
        
        tag = catalog_config['tag']
        
        # Validate catalog name
        if not self.validate_catalog_name(catalog_name):
            return False
        
        # Validate owner
        if not self.validate_owner(owner):
            return False
        
        # Validate tag
        if not self.validate_tag(tag):
            return False
        
        # Validate reader groups (mandatory)
        reader_groups = catalog_config.get('reader_groups', [])
        if not self.validate_reader_groups(reader_groups):
            return False
        
        # Validate optional groups
        editor_groups = catalog_config.get('editor_groups', [])
        if not self.validate_groups(editor_groups, 'Editor group'):
            return False
        
        spn_readers = catalog_config.get('spn_readers', [])
        if not self.validate_groups(spn_readers, 'SPN reader'):
            return False
        
        spn_editors = catalog_config.get('spn_editors', [])
        if not self.validate_groups(spn_editors, 'SPN editor'):
            return False
        
        return len(self.errors) == 0
    
    def check_duplicate(self, catalog_name: str, existing_catalogs: List[str]) -> bool:
        """Check if catalog already exists"""
        if catalog_name in existing_catalogs:
            self.errors.append(f"Catalog '{catalog_name}' already exists")
            return False
        return True
    
    def get_errors(self) -> List[str]:
        """Get list of validation errors"""
        return self.errors
    
    def get_warnings(self) -> List[str]:
        """Get list of validation warnings"""
        return self.warnings
    
    def get_report(self) -> Dict:
        """Get validation report"""
        return {
            'valid': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings
        }


def main():
    """Main function for CLI usage"""
    if len(sys.argv) < 2:
        print("Usage: python validate_catalog.py <config_json>")
        sys.exit(1)
    
    try:
        config = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON config: {e}")
        sys.exit(1)
    
    validator = CatalogValidator()
    
    # Check for duplicates if provided
    if 'existing_catalogs' in config:
        existing = config['existing_catalogs']
        if not validator.check_duplicate(config['catalog_name'], existing):
            print(json.dumps(validator.get_report()))
            sys.exit(1)
    
    # Validate configuration
    if validator.validate_catalog_config(config):
        print(json.dumps(validator.get_report()))
        sys.exit(0)
    else:
        print(json.dumps(validator.get_report()))
        sys.exit(1)


if __name__ == '__main__':
    main()
