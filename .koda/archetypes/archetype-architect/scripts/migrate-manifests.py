#!/usr/bin/env python3
"""
Manifest Migration Script

Updates all archetype manifests to the new schema:
- Adds constitution field if missing
- Adds dependencies field if missing
- Removes deprecated version field
- Validates manifest structure

Usage:
    python migrate-manifests.py --dry-run    # Preview changes
    python migrate-manifests.py --apply      # Apply changes
    python migrate-manifests.py --validate   # Validate only
"""
import os
import sys
import yaml
import argparse
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# archetype-architect/scripts -> archetypes base (up 2 levels)
DEFAULT_BASEDIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', '..'))


def get_basedir():
    """Get the archetypes base directory."""
    return os.environ.get('ARCHETYPES_BASEDIR', DEFAULT_BASEDIR)


def find_all_manifests(basedir):
    """Find all manifest.yaml files in archetype directories."""
    manifests = []
    for entry in os.listdir(basedir):
        if entry.startswith('.') or entry == '00-core-orchestration':
            continue
        manifest_path = os.path.join(basedir, entry, 'manifest.yaml')
        if os.path.exists(manifest_path):
            manifests.append((entry, manifest_path))
    return sorted(manifests)


def analyze_manifest(archetype_name, manifest_path):
    """Analyze a manifest and determine required changes."""
    changes = []
    issues = []
    
    try:
        with open(manifest_path, 'r') as f:
            content = f.read()
            manifest = yaml.safe_load(content)
    except Exception as e:
        return None, [], [f"Could not parse manifest: {e}"]
    
    if not manifest or 'archetype' not in manifest:
        return None, [], ["Invalid manifest structure: missing 'archetype' key"]
    
    archetype = manifest.get('archetype', {})
    
    # Check for deprecated version field at root level
    if 'version' in manifest:
        changes.append("Remove deprecated 'version' field from root")
    
    # Check for constitution field
    if 'constitution' not in archetype:
        constitution_file = f"{archetype_name}-constitution.md"
        changes.append(f"Add constitution reference: {constitution_file}")
    
    # Check for dependencies field
    if 'dependencies' not in archetype:
        changes.append("Add empty dependencies field")
    
    # Validate required fields
    required_fields = ['name', 'display_name', 'description', 'keywords', 'workflows']
    for field in required_fields:
        if field not in archetype:
            issues.append(f"Missing required field: archetype.{field}")
    
    return manifest, changes, issues


def migrate_manifest(archetype_name, manifest_path, dry_run=False):
    """Migrate a single manifest to the new schema."""
    manifest, changes, issues = analyze_manifest(archetype_name, manifest_path)
    
    if manifest is None:
        return {'status': 'error', 'issues': issues, 'changes': []}
    
    if not changes:
        return {'status': 'unchanged', 'issues': issues, 'changes': []}
    
    if dry_run:
        return {'status': 'would_change', 'issues': issues, 'changes': changes}
    
    # Apply changes
    archetype = manifest.get('archetype', {})
    
    # Remove version from root
    if 'version' in manifest:
        del manifest['version']
    
    # Add constitution if missing
    if 'constitution' not in archetype:
        constitution_file = f"{archetype_name}-constitution.md"
        archetype['constitution'] = {'path': constitution_file}
    
    # Add dependencies if missing
    if 'dependencies' not in archetype:
        archetype['dependencies'] = []
    
    # Reorder fields for consistency
    ordered_archetype = {}
    field_order = ['name', 'display_name', 'description', 'keywords', 'constitution', 'dependencies', 'workflows']
    
    for field in field_order:
        if field in archetype:
            ordered_archetype[field] = archetype[field]
    
    # Add any remaining fields
    for field, value in archetype.items():
        if field not in ordered_archetype:
            ordered_archetype[field] = value
    
    manifest['archetype'] = ordered_archetype
    
    # Write updated manifest
    try:
        with open(manifest_path, 'w') as f:
            yaml.dump(manifest, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        return {'status': 'updated', 'issues': issues, 'changes': changes}
    except Exception as e:
        return {'status': 'error', 'issues': [f"Could not write manifest: {e}"], 'changes': changes}


def main():
    parser = argparse.ArgumentParser(description="Migrate archetype manifests to new schema")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    parser.add_argument("--apply", action="store_true", help="Apply changes")
    parser.add_argument("--validate", action="store_true", help="Validate manifests only")
    parser.add_argument("--basedir", help="Override ARCHETYPES_BASEDIR")
    
    args = parser.parse_args()
    
    if not args.dry_run and not args.apply and not args.validate:
        parser.error("Specify --dry-run, --apply, or --validate")
    
    basedir = args.basedir or get_basedir()
    manifests = find_all_manifests(basedir)
    
    print(f"Found {len(manifests)} archetype manifests in {basedir}\n")
    
    stats = {'updated': 0, 'unchanged': 0, 'would_change': 0, 'error': 0}
    all_issues = []
    
    for archetype_name, manifest_path in manifests:
        if args.validate:
            manifest, changes, issues = analyze_manifest(archetype_name, manifest_path)
            if issues:
                print(f"❌ {archetype_name}: {len(issues)} issue(s)")
                for issue in issues:
                    print(f"   - {issue}")
                all_issues.extend(issues)
                stats['error'] += 1
            elif changes:
                print(f"⚠️  {archetype_name}: {len(changes)} change(s) needed")
                for change in changes:
                    print(f"   - {change}")
                stats['would_change'] += 1
            else:
                print(f"✓ {archetype_name}: valid")
                stats['unchanged'] += 1
        else:
            result = migrate_manifest(archetype_name, manifest_path, dry_run=args.dry_run)
            status = result['status']
            stats[status] += 1
            
            if status == 'error':
                print(f"❌ {archetype_name}: ERROR")
                for issue in result['issues']:
                    print(f"   - {issue}")
            elif status == 'would_change':
                print(f"⚠️  {archetype_name}: would change")
                for change in result['changes']:
                    print(f"   - {change}")
            elif status == 'updated':
                print(f"✓ {archetype_name}: updated")
                for change in result['changes']:
                    print(f"   - {change}")
            else:
                print(f"○ {archetype_name}: unchanged")
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    if args.validate:
        print(f"Valid:        {stats['unchanged']}")
        print(f"Need changes: {stats['would_change']}")
        print(f"Errors:       {stats['error']}")
    elif args.dry_run:
        print(f"Would update: {stats['would_change']}")
        print(f"Unchanged:    {stats['unchanged']}")
        print(f"Errors:       {stats['error']}")
        print("\nRun with --apply to apply changes")
    else:
        print(f"Updated:      {stats['updated']}")
        print(f"Unchanged:    {stats['unchanged']}")
        print(f"Errors:       {stats['error']}")
    
    return 0 if stats['error'] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
