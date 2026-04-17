import argparse
import os
import sys


def _is_nonempty_file(p: str) -> bool:
    try:
        return os.path.isfile(p) and os.path.getsize(p) > 0
    except OSError:
        return False


def _read_text(p: str) -> str:
    try:
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def _extract_headings(md: str) -> set[str]:
    headings: set[str] = set()
    for raw in md.splitlines():
        line = raw.strip()
        if not line.startswith("#"):
            continue
        text = line.lstrip("#").strip()
        if text:
            headings.add(text)
    return headings


def _has_required_headings(
    md_path: str, required_headings: list[str]
) -> tuple[bool, list[str]]:
    md = _read_text(md_path)
    headings = _extract_headings(md)
    missing = [h for h in required_headings if h not in headings]
    return (len(missing) == 0, missing)


def _check_ci_security_baseline(repo_root: str, errors: list[str]) -> None:
    workflow_path = os.path.join(repo_root, ".github", "workflows", "security.yml")
    if not _is_nonempty_file(workflow_path):
        errors.append("missing_security_workflow: expected .github/workflows/security.yml")
        return

    content = _read_text(workflow_path)
    lowered = content.lower()

    required_markers = {
        "missing_dependency_audit_gate": "npm audit",
        "missing_secret_scan_gate": "trufflehog",
        "missing_container_scan_gate": "trivy",
        "missing_sbom_gate": "sbom",
    }

    for code, marker in required_markers.items():
        if marker not in lowered:
            errors.append(f"{code}: expected '{marker}' in .github/workflows/security.yml")

    if "continue-on-error: true" in lowered:
        errors.append(
            "fail_open_security_gate: remove continue-on-error: true from security workflow"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default=".")
    parser.add_argument(
        "--strict-headings",
        dest="strict_headings",
        action="store_true",
        default=True,
        help="Fail if required headings are missing from evidence markdown files.",
    )
    parser.add_argument(
        "--no-strict-headings",
        dest="strict_headings",
        action="store_false",
        help="Skip required-heading checks (not recommended).",
    )
    args = parser.parse_args()

    repo_root = os.path.abspath(args.path)
    evidence_dir = os.path.join(repo_root, "security", "evidence")

    required = [
        "security-requirements.md",
        "risk-profile.md",
        "threat-model.md",
        "secure-by-default-checklist.md",
        "security-test-matrix.md",
        "vulnerability-management.md",
        "security-metrics.md",
    ]

    required_headings_by_file: dict[str, list[str]] = {
        "security-requirements.md": [
            "Security Requirements",
            "System",
            "Verification target",
            "Requirements (minimum)",
            "Exceptions",
        ],
        "risk-profile.md": [
            "Risk Profile",
            "System summary",
            "Risk rating",
            "Verification target",
            "Exceptions and compensating controls",
        ],
        "threat-model.md": [
            "Threat Model",
            "Overview",
            "Data flows",
            "Assets",
            "Threat enumeration",
            "Top risks summary",
            "Decision log",
        ],
        "secure-by-default-checklist.md": [
            "Secure-by-Default Checklist",
            "Identity and access",
            "Secrets",
            "Data protection",
            "Network exposure",
            "Logging and telemetry",
            "Supply chain",
            "Infrastructure and CI/CD",
        ],
        "security-test-matrix.md": [
            "Security Test Matrix",
            "Scope",
            "Test categories",
            "Evidence",
        ],
        "vulnerability-management.md": [
            "Vulnerability Management",
            "Intake",
            "Severity model",
            "SLAs",
            "Workflow",
            "Exception handling",
            "Reporting",
        ],
        "security-metrics.md": [
            "Security Metrics",
            "Goals",
            "Metrics",
            "Reporting cadence",
        ],
    }

    errors: list[str] = []

    if not os.path.isdir(evidence_dir):
        errors.append(f"missing_dir: {os.path.relpath(evidence_dir, repo_root)}")
    else:
        for fname in required:
            p = os.path.join(evidence_dir, fname)
            if not _is_nonempty_file(p):
                errors.append(f"missing_or_empty: {os.path.relpath(p, repo_root)}")
                continue

            required_headings = required_headings_by_file.get(fname)
            if args.strict_headings and required_headings:
                ok, missing = _has_required_headings(p, required_headings)
                if not ok:
                    missing_str = ", ".join([f"'{h}'" for h in missing])
                    errors.append(
                        f"missing_headings: {os.path.relpath(p, repo_root)} missing {missing_str}"
                    )

    sbom_dirs = [
        os.path.join(repo_root, "security", "sbom"),
        os.path.join(repo_root, "sbom"),
    ]

    sbom_found = False
    for d in sbom_dirs:
        if not os.path.isdir(d):
            continue
        for root, _, files in os.walk(d):
            for f in files:
                lf = f.lower()
                if (
                    lf.endswith(".json")
                    or lf.endswith(".xml")
                    or lf.endswith(".spdx")
                    or lf.endswith(".spdx.json")
                ):
                    sbom_found = True
                    break
            if sbom_found:
                break
        if sbom_found:
            break

    if not sbom_found:
        errors.append("missing_sbom: expected under security/sbom/ or sbom/")

    _check_ci_security_baseline(repo_root, errors)

    if errors:
        for e in errors:
            print(f"FAIL {e}")
        return 1

    print("OK security-guardian")
    return 0


if __name__ == "__main__":
    sys.exit(main())
