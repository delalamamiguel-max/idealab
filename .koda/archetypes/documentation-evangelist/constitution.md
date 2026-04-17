# documentation evangelist Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the documentation evangelist archetype.

**Source**: Converted from `vibe_cdo/documentation_evangelist/.rules` and `governance_prompt.md`

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** if these rules are violated:

- ✘ **Line length limit**: Do not exceed 100 characters per line
- ✘ **Metadata required**: Do not omit metadata block (version, author, last updated)
- ✘ **Valid diagrams**: Do not use non-Mermaid diagram syntax or invalid Mermaid code
- ✘ **No hard-coded links**: Do not hard-code external links or references; parameterize them
- ✘ **Required sections**: Do not skip any required sections: Overview, Data Flow, Schema Definitions, Metrics Glossary
- ✘ **CSV formatting violations**: When generating CSV files, wrap all text fields in double quotes to prevent comma parsing errors; use proper CSV escaping (double-quote internal quotes); validate CSV output against RFC 4180 standard; use Python `csv.QUOTE_ALL` or `pandas.to_csv(quoting=csv.QUOTE_ALL)`

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

- ✔ **Metadata header**: Include metadata header (YAML frontmatter or company template) with title, author, date, version
- ✔ **Diagram validation**: Validate Mermaid diagrams for syntax correctness
- ✔ **Template compliance**: Follow company doc template for headers, footers, and section ordering
- ✔ **Parameterized references**: Parameterize all external references (links to code, schemas, dashboards)

## III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

- ➜ **Section order**: Keep section order: Overview → Data Flow → Schema Definitions → Metrics Glossary
- ➜ **Tables for schemas**: Use Markdown tables for schema definitions and examples
- ➜ **Annotated diagrams**: Annotate diagrams with clear labels, step descriptions, and notes
- ➜ **Example queries**: Provide example queries or sample data snippets where relevant
- ➜ **Concise prose**: Limit prose paragraphs to 3–4 sentences before breaking into lists or tables

## IV. HTML Report Generation Strategies

**Template Reference**: 📄 `.cdo-aifc/templates/09-documentation-requirements/documentation-evangelist/html-report-generation-pattern.py`

Databricks Jobs API does **not** capture cell outputs, requiring alternative strategies for HTML report generation.

### Hard-Stop Rules
- ✘ **Never** rely on Jobs API for cell output capture
- ✘ **Never** assume `display()` or charts will be in job results
- ✘ **Do NOT** skip accessibility compliance (alt text, WCAG)
- ✘ **Never** hard-code sensitive data (credentials, PII) in HTML reports

### Mandatory Patterns
- ✔ **Include report metadata**: Date, analyst, data source, notebook name
- ✔ **Provide data source documentation**: Clear source table and freshness info
- ✔ **Accessibility compliance**: Alt text for images, WCAG color contrast
- ✔ **Document generation method**: Indicate which method was used and why
- ✔ **Version control**: Store HTML templates in git
- ✔ **Test rendering**: Validate in multiple browsers

### HTML Report Generation Methods

#### Method 1: Export Executed Notebook (Recommended for Ad-Hoc)
**Best for**: One-time analysis reports, exploratory findings, audit documentation

**Process**:
1. Run notebook interactively in Databricks UI
2. Wait for all cells to complete with outputs
3. File → Export → HTML
4. Download HTML file with all outputs embedded

**Pros**: ✅ Complete outputs, ✅ Professional appearance, ✅ Easy  
**Cons**: ⚠️ Manual step required

#### Method 2: Programmatic HTML from Structured Data (For Automation)
**Best for**: Scheduled recurring reports, automated pipelines

**Process**:
1. Analysis notebook writes results to Unity Catalog table
2. Reporting script reads results and generates HTML
3. HTML saved to Volume or distributed via email

**Pros**: ✅ Fully automated, ✅ Customizable styling  
**Cons**: ⚠️ Doesn't include interactive charts

#### Method 3: Embedded Visualizations with Base64
**Best for**: Reports requiring charts without external dependencies

**Process**:
1. Create matplotlib/plotly charts
2. Convert to base64-encoded images
3. Embed directly in HTML `<img>` tags

**Pros**: ✅ Self-contained HTML, ✅ No external files  
**Cons**: ⚠️ Larger file sizes

#### Method 4: Jinja2 Templates for Complex Reports
**Best for**: Complex layouts with multiple sections and data sources

**Process**:
1. Define Jinja2 template with placeholders
2. Render with data from analysis results
3. Generate styled HTML with loops and conditionals

**Pros**: ✅ Very flexible, ✅ Reusable templates  
**Cons**: ⚠️ Requires Jinja2 library

#### Method 5: Interactive Notebook as Living Document
**Best for**: Collaborative analysis, recurring reviews, stakeholder engagement

**Process**:
1. Share Databricks notebook URL directly
2. Stakeholders run "Run All" to refresh data
3. No HTML generation needed

**Pros**: ✅ Always latest data, ✅ Interactive filters  
**Cons**: ⚠️ Requires Databricks workspace access

### Decision Matrix

| Use Case | Method | Why |
|----------|--------|-----|
| Ad-hoc analysis report | Export executed notebook | Complete, professional |
| Scheduled report | Programmatic HTML | Automated |
| Executive dashboard | Lakeview Dashboard | Interactive, self-service |
| Audit documentation | Export executed notebook | Includes all outputs |
| Recurring review | Interactive notebook URL | Always fresh data |

### HTML Template Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Analysis Report</title>
    <style>
        /* Professional styling */
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; }
        .header { background: #667eea; color: white; padding: 20px; }
        .metric-card { background: #f5f5f5; padding: 15px; margin: 10px 0; }
        /* WCAG compliant colors */
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Data Analysis Report</h1>
        <p><strong>Date:</strong> 2025-11-23 | <strong>Analyst:</strong> Data Team</p>
    </div>
    <!-- Content sections -->
</body>
</html>
```

### Accessibility Requirements (WCAG)
- ✔ **Color contrast**: ≥ 4.5:1 ratio for text
- ✔ **Alt text**: All images must have descriptive alt attributes
- ✔ **Semantic HTML**: Use proper heading hierarchy (h1 → h2 → h3)
- ✔ **Font size**: ≥ 12pt for body text
- ✔ **Keyboard navigation**: All interactive elements accessible via keyboard

### Template Features
The HTML report generation template provides:
1. Complete HTML generation function with professional styling
2. Embedded visualization patterns (matplotlib to base64)
3. Jinja2 template examples for complex layouts
4. Decision tree for choosing the right method
5. Accessibility compliance checklist
6. Testing and validation patterns
7. Troubleshooting guide for common issues

---

**Version**: 1.2.0  
**Last Updated**: 2025-11-23  
**Changelog**:
- 1.2.0 (2025-11-23): Added comprehensive HTML report generation strategies
- 1.1.0 (2025-11-15): Added CSV formatting hard-stop rule for proper text field quoting
- 1.0.0: Initial release

**Source**: `/Users/md464h/projects/aifc_projects/eaifc_windsurf/../vibe_cdo/documentation_evangelist/.rules`
