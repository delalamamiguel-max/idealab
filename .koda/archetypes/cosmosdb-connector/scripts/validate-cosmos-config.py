#!/usr/bin/env python3
"""
Validation script for Cosmos DB Connector configuration.
Validates configuration properties and connection settings.
"""

import argparse
import json
import sys
import re
from typing import Dict, List, Tuple


def validate_hostname(hostname: str) -> Tuple[bool, str]:
    """Validate Cosmos DB hostname format."""
    pattern = r'^https://[a-zA-Z0-9\-]+\.documents\.azure\.com:443/$'
    if not re.match(pattern, hostname):
        return False, f"Invalid hostname format. Expected: https://{{account}}.documents.azure.com:443/"
    return True, "Valid hostname"


def validate_consistency_level(level: str) -> Tuple[bool, str]:
    """Validate consistency level."""
    valid_levels = ["STRONG", "BOUNDED_STALENESS", "SESSION", "CONSISTENT_PREFIX", "EVENTUAL"]
    if level.upper() not in valid_levels:
        return False, f"Invalid consistency level. Must be one of: {', '.join(valid_levels)}"
    return True, "Valid consistency level"


def validate_connection_pool(pool_size: int) -> Tuple[bool, str]:
    """Validate connection pool size."""
    if pool_size < 1 or pool_size > 1000:
        return False, "Connection pool size must be between 1 and 1000"
    return True, "Valid connection pool size"


def validate_timeout(timeout: int) -> Tuple[bool, str]:
    """Validate timeout value."""
    if timeout < 100 or timeout > 60000:
        return False, "Timeout must be between 100ms and 60000ms"
    return True, "Valid timeout"


def validate_retry_config(retry_count: int, retry_wait: int) -> Tuple[bool, str]:
    """Validate retry configuration."""
    if retry_count < 0 or retry_count > 10:
        return False, "Retry count must be between 0 and 10"
    if retry_wait < 10 or retry_wait > 5000:
        return False, "Retry wait time must be between 10ms and 5000ms"
    return True, "Valid retry configuration"


def check_hardcoded_secrets(config: Dict) -> List[str]:
    """Check for hardcoded secrets in configuration."""
    violations = []
    
    for key, db_config in config.items():
        if isinstance(db_config, dict):
            secret_key = db_config.get('secretKey', '')
            
            # Check if secret key looks hardcoded (not a reference)
            if secret_key and not secret_key.startswith('${'):
                if len(secret_key) > 20:  # Likely an actual key
                    violations.append(
                        f"Database '{key}': Hardcoded secret detected. "
                        f"Use environment variable: ${{COSMOS_SECRET_KEY}}"
                    )
    
    return violations


def validate_database_config(db_key: str, db_config: Dict) -> List[str]:
    """Validate a single database configuration."""
    errors = []
    
    # Required fields
    required_fields = ['hostName', 'secretKey', 'databaseName']
    for field in required_fields:
        if field not in db_config or not db_config[field]:
            errors.append(f"Database '{db_key}': Missing required field '{field}'")
    
    # Validate hostname
    if 'hostName' in db_config:
        valid, msg = validate_hostname(db_config['hostName'])
        if not valid:
            errors.append(f"Database '{db_key}': {msg}")
    
    # Validate consistency level
    if 'consistencyLevel' in db_config:
        valid, msg = validate_consistency_level(db_config['consistencyLevel'])
        if not valid:
            errors.append(f"Database '{db_key}': {msg}")
    
    # Validate connection pool
    if 'maxConnectionPool' in db_config:
        try:
            pool_size = int(db_config['maxConnectionPool'])
            valid, msg = validate_connection_pool(pool_size)
            if not valid:
                errors.append(f"Database '{db_key}': {msg}")
        except ValueError:
            errors.append(f"Database '{db_key}': maxConnectionPool must be an integer")
    
    # Validate timeout
    if 'idleConnectionTimeout' in db_config:
        try:
            timeout = int(db_config['idleConnectionTimeout'])
            valid, msg = validate_timeout(timeout)
            if not valid:
                errors.append(f"Database '{db_key}': {msg}")
        except ValueError:
            errors.append(f"Database '{db_key}': idleConnectionTimeout must be an integer")
    
    return errors


def validate_config(config_file: str, json_output: bool = False) -> int:
    """Main validation function."""
    try:
        # Load configuration
        with open(config_file, 'r') as f:
            if config_file.endswith('.json'):
                config = json.load(f)
            else:
                # Parse properties file
                config = parse_properties_file(f)
        
        errors = []
        warnings = []
        
        # Check for hardcoded secrets
        secret_violations = check_hardcoded_secrets(config.get('cosmos.config', {}))
        if secret_violations:
            errors.extend(secret_violations)
        
        # Validate each database configuration
        for db_key, db_config in config.get('cosmos.config', {}).items():
            db_errors = validate_database_config(db_key, db_config)
            errors.extend(db_errors)
        
        # Validate retry configuration
        retry_enabled = config.get('cosmos.retry.enabled', 'false').lower() == 'true'
        if retry_enabled:
            retry_count = int(config.get('cosmos.retry.count', 3))
            retry_wait = int(config.get('cosmos.retry.sleep.time', 100))
            valid, msg = validate_retry_config(retry_count, retry_wait)
            if not valid:
                errors.append(f"Retry configuration: {msg}")
        
        # Generate report
        if json_output:
            result = {
                "valid": len(errors) == 0,
                "errors": errors,
                "warnings": warnings,
                "databases_validated": len(config.get('cosmos.config', {}))
            }
            print(json.dumps(result, indent=2))
        else:
            print("=" * 60)
            print("Cosmos DB Configuration Validation Report")
            print("=" * 60)
            print(f"\nDatabases validated: {len(config.get('cosmos.config', {}))}")
            
            if errors:
                print(f"\n❌ Errors found: {len(errors)}")
                for error in errors:
                    print(f"  - {error}")
            else:
                print("\n✅ No errors found")
            
            if warnings:
                print(f"\n⚠️  Warnings: {len(warnings)}")
                for warning in warnings:
                    print(f"  - {warning}")
            
            print("\n" + "=" * 60)
        
        return 0 if len(errors) == 0 else 1
        
    except Exception as e:
        if json_output:
            print(json.dumps({"valid": False, "error": str(e)}))
        else:
            print(f"Error validating configuration: {e}", file=sys.stderr)
        return 1


def parse_properties_file(file_handle) -> Dict:
    """Parse Java properties file into nested dictionary."""
    config = {'cosmos.config': {}}
    
    for line in file_handle:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            # Parse cosmos.config.{db}.{property} format
            if key.startswith('cosmos.config.'):
                parts = key.split('.')
                if len(parts) >= 4:
                    db_key = parts[2]
                    # Use only the immediate property name, not joined parts
                    prop_key = parts[3]
                    
                    if db_key not in config['cosmos.config']:
                        config['cosmos.config'][db_key] = {}
                    
                    config['cosmos.config'][db_key][prop_key] = value
            else:
                config[key] = value
    
    return config


def main():
    parser = argparse.ArgumentParser(
        description='Validate Cosmos DB Connector configuration'
    )
    parser.add_argument(
        '--config',
        required=True,
        help='Path to configuration file (properties or JSON)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    
    args = parser.parse_args()
    
    exit_code = validate_config(args.config, args.json)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
