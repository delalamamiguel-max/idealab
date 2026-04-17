#!/usr/bin/env python3
"""
Archetype Quality Analysis Script

Analyzes archetypes against archetype-architect best practices for structural
validation, workflow quality, discovery performance, and platform compatibility.

Usage:
    python analyze-archetypes.py [--output DIR] [--archetype SLUG] [--verbose] [--json]

Examples:
    # Analyze all archetypes
    python analyze-archetypes.py

    # Analyze specific archetype with verbose output
    python analyze-archetypes.py --archetype sql-query-crafter --verbose

    # Output JSON for programmatic use
    python analyze-archetypes.py --archetype model-architect --json

Cross-Platform: Works on Windows, Mac, and Linux.
"""

import argparse
import csv
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)


# ============================================================================
# Configuration - Archetype Architect Standards
# ============================================================================

REQUIRED_WORKFLOWS = ['scaffold', 'debug', 'refactor', 'test', 'compare', 'document']
MIN_HARD_STOP_RULES = 3
MIN_MANDATORY_PATTERNS = 5
MIN_PREFERRED_PATTERNS = 2
MIN_KEYWORDS = 5

WORKFLOW_REQUIRED_SECTIONS = [
    'Execution Steps',
    'Error Handling',
    'Examples',
]

SKIP_DIRECTORIES = [
    '.git',
    '__pycache__',
    'node_modules',
    '.venv',
    'venv',
]


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class ManifestValidation:
    exists: bool = False
    valid_yaml: bool = False
    has_name: bool = False
    has_display_name: bool = False
    has_description: bool = False
    has_keywords: bool = False
    keyword_count: int = 0
    has_workflows: bool = False
    workflow_count: int = 0
    issues: List[str] = field(default_factory=list)


@dataclass
class ConstitutionValidation:
    exists: bool = False
    valid_structure: bool = False
    hard_stop_count: int = 0
    mandatory_count: int = 0
    preferred_count: int = 0
    has_hard_stop_section: bool = False
    has_mandatory_section: bool = False
    has_preferred_section: bool = False
    issues: List[str] = field(default_factory=list)


@dataclass
class WorkflowValidation:
    name: str = ""
    exists: bool = False
    has_frontmatter: bool = False
    has_description: bool = False
    has_arguments: bool = False
    has_execution_steps: bool = False
    has_error_handling: bool = False
    has_examples: bool = False
    has_references: bool = False
    issues: List[str] = field(default_factory=list)


@dataclass
class PlatformValidation:
    bash_only_scripts: List[str] = field(default_factory=list)
    hardcoded_paths: List[str] = field(default_factory=list)
    platform_issues: List[str] = field(default_factory=list)
    is_compatible: bool = True


@dataclass
class ArchetypeAnalysis:
    slug: str
    path: str
    timestamp: str = ""
    manifest: ManifestValidation = field(default_factory=ManifestValidation)
    constitution: ConstitutionValidation = field(default_factory=ConstitutionValidation)
    workflows: Dict[str, WorkflowValidation] = field(default_factory=dict)
    platform: PlatformValidation = field(default_factory=PlatformValidation)
    overall_score: str = "UNKNOWN"
    priority: str = "P3"
    issues_summary: List[str] = field(default_factory=list)


# ============================================================================
# Path Utilities (Cross-Platform)
# ============================================================================

def find_archetypes_basedir() -> Optional[Path]:
    """Find the archetypes-aggregation directory (cross-platform)."""
    current = Path(__file__).resolve().parent
    
    # Search up to find archetypes-aggregation
    for _ in range(10):
        # Check if we're in archetypes-aggregation
        if (current / "00-core-orchestration").exists():
            return current
        
        # Check if archetypes-aggregation is a sibling
        candidate = current / "archetypes-aggregation"
        if candidate.exists() and (candidate / "00-core-orchestration").exists():
            return candidate
        
        # Move up one level
        parent = current.parent
        if parent == current:
            break
        current = parent
    
    return None


# ============================================================================
# Analysis Functions
# ============================================================================

def analyze_manifest(archetype_path: Path) -> ManifestValidation:
    """Analyze manifest.yaml for required fields."""
    result = ManifestValidation()
    manifest_path = archetype_path / "manifest.yaml"
    
    if not manifest_path.exists():
        result.issues.append("manifest.yaml not found")
        return result
    
    result.exists = True
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        result.valid_yaml = True
    except yaml.YAMLError as e:
        result.issues.append(f"Invalid YAML: {e}")
        return result
    
    if not data or 'archetype' not in data:
        result.issues.append("Missing 'archetype' root key")
        return result
    
    arch = data['archetype']
    
    # Check required fields
    if arch.get('name'):
        result.has_name = True
    else:
        result.issues.append("Missing 'name' field")
    
    if arch.get('display_name'):
        result.has_display_name = True
    else:
        result.issues.append("Missing 'display_name' field")
    
    if arch.get('description'):
        result.has_description = True
    else:
        result.issues.append("Missing 'description' field")
    
    # Check keywords
    if isinstance(arch.get('keywords'), list):
        result.has_keywords = True
        result.keyword_count = len(arch['keywords'])
        if result.keyword_count < MIN_KEYWORDS:
            result.issues.append(f"Only {result.keyword_count} keywords (minimum {MIN_KEYWORDS})")
    else:
        result.issues.append("Missing 'keywords' field")
    
    # Check workflows
    if isinstance(arch.get('workflows'), dict):
        result.has_workflows = True
        result.workflow_count = len(arch['workflows'])
        
        for wf in REQUIRED_WORKFLOWS:
            if wf not in arch['workflows']:
                result.issues.append(f"Missing workflow mapping for '{wf}'")
    else:
        result.issues.append("Missing 'workflows' field")
    
    return result


def analyze_constitution(archetype_path: Path, slug: str) -> ConstitutionValidation:
    """Analyze constitution file for required structure and content."""
    result = ConstitutionValidation()
    
    # Try different constitution file patterns
    patterns = [
        archetype_path / f"{slug}-constitution.md",
        archetype_path / "constitution.md",
    ]
    
    constitution_path = None
    for pattern in patterns:
        if pattern.exists():
            constitution_path = pattern
            break
    
    if not constitution_path:
        result.issues.append("Constitution file not found")
        return result
    
    result.exists = True
    
    try:
        with open(constitution_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        result.issues.append(f"Could not read constitution: {e}")
        return result
    
    # Check for required sections
    if re.search(r'#+\s*(I\.|Hard-Stop|Non-Negotiable)', content, re.IGNORECASE):
        result.has_hard_stop_section = True
    else:
        result.issues.append("Missing Hard-Stop Rules section")
    
    if re.search(r'#+\s*(II\.|Mandatory|Must Apply)', content, re.IGNORECASE):
        result.has_mandatory_section = True
    else:
        result.issues.append("Missing Mandatory Patterns section")
    
    if re.search(r'#+\s*(III\.|Preferred|Recommended)', content, re.IGNORECASE):
        result.has_preferred_section = True
    else:
        result.issues.append("Missing Preferred Patterns section")
    
    # Count rules/patterns using Unicode markers
    # Hard-stop: ✘ or ✗ or × or "No "
    hard_stop_matches = re.findall(r'[-✘✗×]\s*\*?\*?No\s|[-✘✗×]\s*\*?\*?\w+', content)
    result.hard_stop_count = len([m for m in hard_stop_matches if '✘' in m or '✗' in m or '×' in m or 'No ' in m])
    
    # Mandatory: ✔ or ✓
    mandatory_matches = re.findall(r'[-✔✓]\s*\*?\*?\w+', content)
    result.mandatory_count = len([m for m in mandatory_matches if '✔' in m or '✓' in m])
    
    # Preferred: ➜ or →
    preferred_matches = re.findall(r'[-➜→]\s*\*?\*?\w+', content)
    result.preferred_count = len([m for m in preferred_matches if '➜' in m or '→' in m])
    
    # Validate minimums
    if result.hard_stop_count < MIN_HARD_STOP_RULES:
        result.issues.append(f"Only {result.hard_stop_count} hard-stop rules (minimum {MIN_HARD_STOP_RULES})")
    
    if result.mandatory_count < MIN_MANDATORY_PATTERNS:
        result.issues.append(f"Only {result.mandatory_count} mandatory patterns (minimum {MIN_MANDATORY_PATTERNS})")
    
    if result.preferred_count < MIN_PREFERRED_PATTERNS:
        result.issues.append(f"Only {result.preferred_count} preferred patterns (minimum {MIN_PREFERRED_PATTERNS})")
    
    result.valid_structure = (
        result.has_hard_stop_section and 
        result.has_mandatory_section and 
        result.has_preferred_section
    )
    
    return result


def analyze_workflow(workflow_path: Path, workflow_name: str) -> WorkflowValidation:
    """Analyze a workflow file for required structure."""
    result = WorkflowValidation(name=workflow_name)
    
    if not workflow_path.exists():
        result.issues.append(f"Workflow file not found: {workflow_path.name}")
        return result
    
    result.exists = True
    
    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        result.issues.append(f"Could not read workflow: {e}")
        return result
    
    # Check YAML frontmatter
    if content.startswith('---'):
        frontmatter_end = content.find('---', 3)
        if frontmatter_end > 0:
            result.has_frontmatter = True
            frontmatter = content[3:frontmatter_end]
            if 'description:' in frontmatter:
                result.has_description = True
            else:
                result.issues.append("Frontmatter missing 'description' field")
        else:
            result.issues.append("Invalid frontmatter format")
    else:
        result.issues.append("Missing YAML frontmatter")
    
    # Check for $ARGUMENTS
    if '$ARGUMENTS' in content:
        result.has_arguments = True
    else:
        result.issues.append("Missing $ARGUMENTS placeholder")
    
    # Check required sections
    if re.search(r'#+\s*Execution\s+Steps', content, re.IGNORECASE):
        result.has_execution_steps = True
    else:
        result.issues.append("Missing 'Execution Steps' section")
    
    if re.search(r'#+\s*Error\s+Handling', content, re.IGNORECASE):
        result.has_error_handling = True
    else:
        result.issues.append("Missing 'Error Handling' section")
    
    if re.search(r'#+\s*Examples?', content, re.IGNORECASE):
        result.has_examples = True
    else:
        result.issues.append("Missing 'Examples' section")
    
    if re.search(r'#+\s*References?', content, re.IGNORECASE):
        result.has_references = True
    # References is recommended but not strictly required
    
    return result


def analyze_workflows(archetype_path: Path, slug: str) -> Dict[str, WorkflowValidation]:
    """Analyze all required workflow files."""
    results = {}
    
    workflows_dir = archetype_path / ".windsurf" / "workflows"
    
    for wf_type in REQUIRED_WORKFLOWS:
        wf_filename = f"{wf_type}-{slug}.md"
        wf_path = workflows_dir / wf_filename
        results[wf_type] = analyze_workflow(wf_path, wf_type)
    
    return results


def analyze_platform_compatibility(archetype_path: Path) -> PlatformValidation:
    """Check for platform-specific code patterns."""
    result = PlatformValidation()
    
    # Scan workflow files for platform issues
    workflows_dir = archetype_path / ".windsurf" / "workflows"
    
    if not workflows_dir.exists():
        return result
    
    for wf_file in workflows_dir.glob("*.md"):
        try:
            with open(wf_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue
        
        # Check for bash-only script references
        bash_refs = re.findall(r'[\s"`\']([^`\'"]*\.sh)[\s"`\']', content)
        for ref in bash_refs:
            if '/python/' not in ref.lower():
                result.bash_only_scripts.append(f"{wf_file.name}: {ref}")
    
    result.is_compatible = len(result.bash_only_scripts) == 0
    
    if result.bash_only_scripts:
        result.platform_issues.append(f"Found {len(result.bash_only_scripts)} bash-only script references")
    
    return result


def calculate_priority(analysis: ArchetypeAnalysis) -> str:
    """Calculate priority based on issues found (P0=Critical to P3=Low)."""
    critical_issues = 0
    high_issues = 0
    medium_issues = 0
    
    # Critical: Missing required files
    if not analysis.manifest.exists:
        critical_issues += 1
    if not analysis.constitution.exists:
        critical_issues += 1
    
    missing_workflows = sum(1 for wf in analysis.workflows.values() if not wf.exists)
    if missing_workflows > 0:
        critical_issues += 1
    
    # High: Constitution below minimums
    if analysis.constitution.exists:
        if analysis.constitution.hard_stop_count < MIN_HARD_STOP_RULES:
            high_issues += 1
        if analysis.constitution.mandatory_count < MIN_MANDATORY_PATTERNS:
            high_issues += 1
    
    # High: Workflow missing required sections
    for wf in analysis.workflows.values():
        if wf.exists:
            if not wf.has_execution_steps:
                high_issues += 1
            if not wf.has_error_handling:
                high_issues += 1
    
    # Medium: Platform compatibility
    if not analysis.platform.is_compatible:
        medium_issues += 1
    
    # Medium: Low keyword count
    if analysis.manifest.keyword_count < MIN_KEYWORDS:
        medium_issues += 1
    
    if critical_issues > 0:
        return "P0"
    elif high_issues > 0:
        return "P1"
    elif medium_issues > 0:
        return "P2"
    else:
        return "P3"


def calculate_score(analysis: ArchetypeAnalysis) -> str:
    """Calculate overall score (EXCELLENT to CRITICAL)."""
    total_checks = 0
    passed_checks = 0
    
    # Manifest checks
    manifest_checks = [
        analysis.manifest.exists,
        analysis.manifest.valid_yaml,
        analysis.manifest.has_name,
        analysis.manifest.has_display_name,
        analysis.manifest.has_description,
        analysis.manifest.has_keywords and analysis.manifest.keyword_count >= MIN_KEYWORDS,
        analysis.manifest.has_workflows,
    ]
    total_checks += len(manifest_checks)
    passed_checks += sum(manifest_checks)
    
    # Constitution checks
    const_checks = [
        analysis.constitution.exists,
        analysis.constitution.has_hard_stop_section,
        analysis.constitution.has_mandatory_section,
        analysis.constitution.has_preferred_section,
        analysis.constitution.hard_stop_count >= MIN_HARD_STOP_RULES,
        analysis.constitution.mandatory_count >= MIN_MANDATORY_PATTERNS,
        analysis.constitution.preferred_count >= MIN_PREFERRED_PATTERNS,
    ]
    total_checks += len(const_checks)
    passed_checks += sum(const_checks)
    
    # Workflow checks (per workflow)
    for wf in analysis.workflows.values():
        wf_checks = [
            wf.exists,
            wf.has_frontmatter,
            wf.has_description,
            wf.has_arguments,
            wf.has_execution_steps,
            wf.has_error_handling,
            wf.has_examples,
        ]
        total_checks += len(wf_checks)
        passed_checks += sum(wf_checks)
    
    # Platform check
    total_checks += 1
    passed_checks += 1 if analysis.platform.is_compatible else 0
    
    percentage = (passed_checks / total_checks * 100) if total_checks > 0 else 0
    
    if percentage >= 95:
        return "EXCELLENT"
    elif percentage >= 85:
        return "GOOD"
    elif percentage >= 70:
        return "FAIR"
    elif percentage >= 50:
        return "NEEDS_WORK"
    else:
        return "CRITICAL"


def analyze_archetype(archetype_path: Path, verbose: bool = False) -> ArchetypeAnalysis:
    """Perform full analysis of an archetype."""
    slug = archetype_path.name
    
    if verbose:
        print(f"  Analyzing {slug}...")
    
    analysis = ArchetypeAnalysis(
        slug=slug,
        path=str(archetype_path),
        timestamp=datetime.now().isoformat()
    )
    
    # Run all analyses
    analysis.manifest = analyze_manifest(archetype_path)
    analysis.constitution = analyze_constitution(archetype_path, slug)
    analysis.workflows = analyze_workflows(archetype_path, slug)
    analysis.platform = analyze_platform_compatibility(archetype_path)
    
    # Calculate priority and score
    analysis.priority = calculate_priority(analysis)
    analysis.overall_score = calculate_score(analysis)
    
    # Summarize issues
    all_issues = []
    all_issues.extend(analysis.manifest.issues)
    all_issues.extend(analysis.constitution.issues)
    for wf in analysis.workflows.values():
        all_issues.extend(wf.issues)
    all_issues.extend(analysis.platform.platform_issues)
    analysis.issues_summary = all_issues
    
    return analysis


# ============================================================================
# Output Functions
# ============================================================================

def to_dict(obj: Any) -> Any:
    """Convert dataclass to dictionary recursively."""
    if hasattr(obj, '__dict__'):
        return {k: to_dict(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_dict(v) for v in obj]
    elif isinstance(obj, Path):
        return str(obj)
    else:
        return obj


def print_analysis_report(analysis: ArchetypeAnalysis, verbose: bool = False):
    """Print human-readable analysis report."""
    print()
    print("=" * 60)
    print(f"ARCHETYPE QUALITY REPORT: {analysis.slug}")
    print("=" * 60)
    print()
    print(f"Priority: {analysis.priority}")
    print(f"Score: {analysis.overall_score}")
    print(f"Total Issues: {len(analysis.issues_summary)}")
    print()
    
    # Manifest
    m = analysis.manifest
    manifest_status = "✅" if m.exists and m.valid_yaml else "❌"
    print(f"MANIFEST: {manifest_status}")
    if m.exists:
        print(f"  Keywords: {m.keyword_count} (min {MIN_KEYWORDS})")
        print(f"  Workflows: {m.workflow_count}")
    if m.issues:
        for issue in m.issues:
            print(f"  ⚠️  {issue}")
    print()
    
    # Constitution
    c = analysis.constitution
    const_status = "✅" if c.exists and c.valid_structure else "❌"
    print(f"CONSTITUTION: {const_status}")
    if c.exists:
        print(f"  Hard-Stop Rules: {c.hard_stop_count} (min {MIN_HARD_STOP_RULES})")
        print(f"  Mandatory Patterns: {c.mandatory_count} (min {MIN_MANDATORY_PATTERNS})")
        print(f"  Preferred Patterns: {c.preferred_count} (min {MIN_PREFERRED_PATTERNS})")
    if c.issues:
        for issue in c.issues:
            print(f"  ⚠️  {issue}")
    print()
    
    # Workflows
    print("WORKFLOWS:")
    for wf_name, wf in analysis.workflows.items():
        wf_status = "✅" if wf.exists and wf.has_execution_steps and wf.has_error_handling else "❌" if not wf.exists else "⚠️"
        print(f"  {wf_name}: {wf_status}")
        if verbose and wf.issues:
            for issue in wf.issues:
                print(f"    - {issue}")
    print()
    
    # Platform
    p = analysis.platform
    platform_status = "✅" if p.is_compatible else "⚠️"
    print(f"PLATFORM COMPATIBILITY: {platform_status}")
    if p.platform_issues:
        for issue in p.platform_issues:
            print(f"  ⚠️  {issue}")
    print()
    
    # Quality Gates
    print("QUALITY GATES:")
    print(f"  1. Structural Pass: {'✅' if m.exists and c.exists else '❌'} All required files exist")
    print(f"  2. Constitution Pass: {'✅' if c.hard_stop_count >= MIN_HARD_STOP_RULES and c.mandatory_count >= MIN_MANDATORY_PATTERNS and c.preferred_count >= MIN_PREFERRED_PATTERNS else '❌'} Meets minimum rule counts (3/5/2)")
    workflows_pass = all(wf.exists and wf.has_execution_steps and wf.has_error_handling and wf.has_examples for wf in analysis.workflows.values())
    print(f"  3. Workflow Pass: {'✅' if workflows_pass else '❌'} All required sections present")
    print(f"  4. Discovery Pass: ⏳ Run discover-archetype.py to verify score ≥30")
    print(f"  5. Analysis Pass: {'✅' if analysis.priority == 'P3' else '❌'} Priority is P3")
    print()


def print_summary(analyses: List[ArchetypeAnalysis]):
    """Print summary of all analyses."""
    print()
    print("=" * 60)
    print("ANALYSIS SUMMARY")
    print("=" * 60)
    
    priority_counts = {'P0': 0, 'P1': 0, 'P2': 0, 'P3': 0}
    for a in analyses:
        priority_counts[a.priority] = priority_counts.get(a.priority, 0) + 1
    
    print(f"Total archetypes: {len(analyses)}")
    print(f"  P0 (Critical):  {priority_counts['P0']}")
    print(f"  P1 (High):      {priority_counts['P1']}")
    print(f"  P2 (Medium):    {priority_counts['P2']}")
    print(f"  P3 (Low):       {priority_counts['P3']}")
    print()
    
    if priority_counts['P0'] > 0:
        print("⚠️  CRITICAL ISSUES FOUND - Immediate attention required")
        print("   P0 archetypes:")
        for a in analyses:
            if a.priority == 'P0':
                print(f"   - {a.slug}")
        print()


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Analyze archetypes for quality compliance against archetype-architect standards',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze-archetypes.py                           # Analyze all archetypes
  python analyze-archetypes.py -a sql-query-crafter -v   # Analyze specific archetype, verbose
  python analyze-archetypes.py -a model-architect --json # Output as JSON
        """
    )
    parser.add_argument('--output', '-o', type=str, default='results',
                       help='Output directory for reports (default: results)')
    parser.add_argument('--archetype', '-a', type=str,
                       help='Analyze specific archetype only')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    parser.add_argument('--json', action='store_true',
                       help='Output as JSON (single archetype only)')
    args = parser.parse_args()
    
    # Find archetypes directory
    basedir = find_archetypes_basedir()
    if not basedir:
        print("ERROR: Could not find archetypes-aggregation directory")
        print("Run this script from within the archetypes project")
        sys.exit(1)
    
    if not args.json:
        print(f"Found archetypes at: {basedir}")
    
    # Find all archetypes
    archetypes = []
    for item in sorted(basedir.iterdir()):
        if not item.is_dir():
            continue
        if item.name in SKIP_DIRECTORIES:
            continue
        if item.name.startswith('.'):
            continue
        
        # Check if it has a manifest.yaml (indicates it's an archetype)
        if (item / "manifest.yaml").exists():
            archetypes.append(item)
    
    if args.archetype:
        archetypes = [a for a in archetypes if a.name == args.archetype]
        if not archetypes:
            print(f"ERROR: Archetype '{args.archetype}' not found")
            sys.exit(1)
    
    if not args.json:
        print(f"Found {len(archetypes)} archetypes to analyze")
    
    # Analyze each archetype
    analyses = []
    for archetype_path in archetypes:
        analysis = analyze_archetype(archetype_path, verbose=args.verbose)
        analyses.append(analysis)
    
    # Output
    if args.json and len(analyses) == 1:
        # JSON output for single archetype
        result = to_dict(analyses[0])
        print(json.dumps(result, indent=2))
    elif args.archetype and len(analyses) == 1:
        # Detailed report for single archetype
        print_analysis_report(analyses[0], verbose=args.verbose)
    else:
        # Summary for multiple archetypes
        print_summary(analyses)
        
        # Create output directory and generate reports
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # CSV summary
        csv_path = output_dir / "structural-scan-summary.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Archetype', 'Priority', 'Score', 'Manifest', 'Constitution',
                'Workflows (6)', 'Platform', 'Total Issues', 'Key Issues'
            ])
            
            for a in analyses:
                workflows_ok = sum(1 for wf in a.workflows.values() if wf.exists)
                key_issues = '; '.join(a.issues_summary[:3]) if a.issues_summary else 'None'
                
                writer.writerow([
                    a.slug,
                    a.priority,
                    a.overall_score,
                    '✅' if a.manifest.exists and a.manifest.valid_yaml else '❌',
                    '✅' if a.constitution.exists and a.constitution.valid_structure else '❌',
                    f"{workflows_ok}/6",
                    '✅' if a.platform.is_compatible else '⚠️',
                    len(a.issues_summary),
                    key_issues[:100]
                ])
        
        print(f"Reports saved to: {output_dir}")


if __name__ == '__main__':
    main()
