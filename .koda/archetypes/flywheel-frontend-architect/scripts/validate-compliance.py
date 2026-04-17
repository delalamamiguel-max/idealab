#!/usr/bin/env python3
"""
Flywheel Frontend Architect — Compliance Validator

Validates a project against Flywheel Frontend Architect constitution rules.
Cross-platform: works on Windows, Mac, and Linux.

Usage:
    python validate-compliance.py [project_root]
    python validate-compliance.py              # uses current directory
"""

import os
import sys
import json
import re
from pathlib import Path


def find_project_root(start_path: str) -> Path:
    """Find the project root by looking for package.json."""
    path = Path(start_path).resolve()
    while path != path.parent:
        if (path / "package.json").exists():
            return path
        path = path.parent
    return Path(start_path).resolve()


def scan_files(root: Path, extensions: tuple, exclude_dirs: tuple) -> list:
    """Recursively find files with given extensions, excluding certain dirs."""
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        for f in filenames:
            if f.endswith(extensions):
                results.append(Path(dirpath) / f)
    return results


def check_prohibited_imports(src_dir: Path) -> list:
    """Rule 1.1: Check for prohibited icon library imports."""
    issues = []
    prohibited = [
        (r"from\s+['\"]lucide-react", "lucide-react (legally prohibited)"),
        (r"from\s+['\"]react-icons", "react-icons"),
        (r"from\s+['\"]@heroicons", "@heroicons"),
        (r"from\s+['\"]phosphor-react", "phosphor-react"),
        (r"from\s+['\"]@radix-ui/react-icons", "@radix-ui/react-icons"),
    ]

    files = scan_files(src_dir, (".ts", ".tsx", ".js", ".jsx"), ("node_modules", ".git", "dist"))
    for filepath in files:
        try:
            content = filepath.read_text(encoding="utf-8")
            for pattern, lib_name in prohibited:
                for match in re.finditer(pattern, content):
                    line_num = content[:match.start()].count("\n") + 1
                    rel_path = filepath.relative_to(src_dir.parent)
                    issues.append(f"  {rel_path}:{line_num} — prohibited import: {lib_name}")
        except (OSError, UnicodeDecodeError):
            continue
    return issues


def check_hardcoded_colors(components_dir: Path) -> list:
    """Rule 1.4: Check for hardcoded Tailwind palette colors in components."""
    issues = []
    palette_pattern = re.compile(
        r"(?:text|bg|border|ring|outline|fill|stroke)-"
        r"(?:blue|red|green|yellow|purple|pink|orange|slate|gray|zinc|neutral|stone)-\d+"
    )
    hex_pattern = re.compile(r"#[0-9a-fA-F]{3,8}")
    inline_color_pattern = re.compile(r"(?:color|backgroundColor|borderColor)\s*:\s*['\"]#")

    if not components_dir.exists():
        return []

    files = scan_files(components_dir, (".ts", ".tsx", ".js", ".jsx"), ("node_modules",))
    for filepath in files:
        try:
            content = filepath.read_text(encoding="utf-8")
            rel_path = filepath.relative_to(components_dir.parent.parent)

            for match in palette_pattern.finditer(content):
                line_num = content[:match.start()].count("\n") + 1
                issues.append(f"  {rel_path}:{line_num} — palette class: {match.group()}")

            for match in hex_pattern.finditer(content):
                line_num = content[:match.start()].count("\n") + 1
                issues.append(f"  {rel_path}:{line_num} — hex literal: {match.group()}")

            for match in inline_color_pattern.finditer(content):
                line_num = content[:match.start()].count("\n") + 1
                issues.append(f"  {rel_path}:{line_num} — inline style color")
        except (OSError, UnicodeDecodeError):
            continue
    return issues


def check_registry_config(root: Path) -> list:
    """Rule 1.2: Verify components.json has Forge registry."""
    issues = []
    components_json = root / "components.json"

    if not components_json.exists():
        issues.append("  components.json not found")
        return issues

    try:
        data = json.loads(components_json.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        issues.append(f"  components.json parse error: {e}")
        return issues

    registries = data.get("registries", {})
    forge_reg = registries.get("@forge", {})
    if not forge_reg.get("url", ""):
        issues.append("  @forge registry not configured in components.json")

    if "forge.dev.att.com" not in forge_reg.get("url", ""):
        issues.append("  @forge registry URL does not point to forge.dev.att.com")

    if data.get("style") != "flywheel":
        issues.append(f"  style is '{data.get('style', 'missing')}', expected 'flywheel'")

    if data.get("iconLibrary") == "lucide":
        issues.append("  iconLibrary is set to 'lucide' — must be 'none'")

    return issues


def check_token_setup(root: Path) -> list:
    """Rule 1.3: Verify @forge/ui-tokens setup."""
    issues = []

    # Check package.json
    pkg_json = root / "package.json"
    if pkg_json.exists():
        try:
            pkg = json.loads(pkg_json.read_text(encoding="utf-8"))
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "@forge/ui-tokens" not in deps:
                issues.append("  @forge/ui-tokens not in package.json dependencies")
            if "@flywheel/react-icons" not in deps:
                issues.append("  @flywheel/react-icons not in package.json dependencies")
        except (json.JSONDecodeError, OSError):
            issues.append("  Could not parse package.json")

    # Check globals.css
    globals_candidates = [
        root / "src" / "styles" / "globals.css",
        root / "src" / "index.css",
        root / "src" / "globals.css",
    ]
    globals_found = False
    for css_path in globals_candidates:
        if css_path.exists():
            globals_found = True
            content = css_path.read_text(encoding="utf-8")
            if "@forge/ui-tokens" not in content:
                issues.append(f"  {css_path.name} does not import @forge/ui-tokens")
            if "color-background" not in content:
                issues.append(f"  {css_path.name} missing @theme inline color mappings")
            break

    if not globals_found:
        issues.append("  No globals.css found (checked src/styles/, src/)")

    return issues


def check_typescript_strict(root: Path) -> list:
    """Rule 1.6: Verify TypeScript strict mode."""
    issues = []
    tsconfig = root / "tsconfig.json"
    if not tsconfig.exists():
        issues.append("  tsconfig.json not found")
        return issues

    try:
        content = tsconfig.read_text(encoding="utf-8")
        # Simple check — tsconfig may have comments so full JSON parse may fail
        if '"strict": true' not in content and '"strict":true' not in content:
            issues.append("  strict mode not enabled in tsconfig.json")
    except OSError:
        issues.append("  Could not read tsconfig.json")

    return issues


def check_any_types(src_dir: Path) -> list:
    """Rule 1.6: Scan for explicit 'any' types."""
    issues = []
    any_pattern = re.compile(r":\s*any\b|as\s+any\b")

    files = scan_files(src_dir, (".ts", ".tsx"), ("node_modules", ".git", "dist"))
    for filepath in files:
        if filepath.name.endswith(".d.ts"):
            continue
        try:
            content = filepath.read_text(encoding="utf-8")
            for match in any_pattern.finditer(content):
                line_num = content[:match.start()].count("\n") + 1
                rel_path = filepath.relative_to(src_dir.parent)
                issues.append(f"  {rel_path}:{line_num} — explicit 'any' type")
        except (OSError, UnicodeDecodeError):
            continue
    return issues


def check_architecture(root: Path) -> list:
    """Verify directory structure follows constitution Section 2.3."""
    issues = []
    required = [
        root / "src" / "components" / "ui",
        root / "src" / "lib" / "utils.ts",
        root / "src" / "main.tsx",
    ]
    for path in required:
        if not path.exists():
            issues.append(f"  Missing: {path.relative_to(root)}")

    # Check cn() utility
    utils_file = root / "src" / "lib" / "utils.ts"
    if utils_file.exists():
        content = utils_file.read_text(encoding="utf-8")
        if "twMerge" not in content:
            issues.append("  src/lib/utils.ts does not use tailwind-merge")

    return issues


def main():
    project_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    project_root = find_project_root(str(project_root))
    src_dir = project_root / "src"

    print(f"Flywheel Compliance Validator")
    print(f"Project: {project_root}")
    print("=" * 60)

    total_issues = 0
    categories = {}

    # Rule 1.1: Prohibited imports
    issues = check_prohibited_imports(src_dir) if src_dir.exists() else ["  src/ directory not found"]
    categories["Icons (Rule 1.1)"] = issues
    total_issues += len(issues)

    # Rule 1.2: Registry config
    issues = check_registry_config(project_root)
    categories["Registry (Rule 1.2)"] = issues
    total_issues += len(issues)

    # Rule 1.3: Token setup
    issues = check_token_setup(project_root)
    categories["Tokens (Rule 1.3)"] = issues
    total_issues += len(issues)

    # Rule 1.4: Hardcoded colors
    components_dir = src_dir / "components"
    issues = check_hardcoded_colors(components_dir)
    categories["Colors (Rule 1.4)"] = issues
    total_issues += len(issues)

    # Rule 1.6: TypeScript
    issues = check_typescript_strict(project_root)
    ts_any = check_any_types(src_dir) if src_dir.exists() else []
    issues.extend(ts_any)
    categories["TypeScript (Rule 1.6)"] = issues
    total_issues += len(issues)

    # Architecture
    issues = check_architecture(project_root)
    categories["Architecture (Section 2.3)"] = issues
    total_issues += len(issues)

    # Print results
    for category, issues in categories.items():
        status = "PASS" if not issues else "FAIL"
        print(f"\n[{status}] {category}")
        for issue in issues:
            print(issue)

    print("\n" + "=" * 60)
    if total_issues == 0:
        print("RESULT: PASS — All checks passed")
    else:
        print(f"RESULT: FAIL — {total_issues} issue(s) found")

    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
