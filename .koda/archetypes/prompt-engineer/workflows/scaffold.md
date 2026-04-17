---
description: Create versioned prompt templates with testing, documentation, and enterprise governance (Prompt Engineer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Environment Setup

// turbo
Verify prompt engineering tools available:
- tiktoken for token counting
- jinja2 for templating

### 2. Load Configuration

- Read `prompt-engineer-constitution.md` for hard-stop rules
- Load template standards from env-config.yaml

### 3. Parse Input

Extract from $ARGUMENTS:
- **Prompt name**: Name for the prompt template
- **Purpose**: What the prompt accomplishes
- **Model target**: Target model(s) (gpt-4, claude-3, etc.)
- **Output format**: text | json | structured
- **Parameters**: Dynamic parameters needed

If incomplete, request:
```
Please provide:
1. Prompt Name: (e.g., "customer-response-generator")
2. Purpose: (what should this prompt accomplish?)
3. Target Model: gpt-4 | gpt-3.5-turbo | claude-3 | all
4. Output Format: text | json | structured
5. Parameters: (e.g., "customer_name, issue_type, context")
```

### 4. Generate Prompt Template

Create versioned prompt with metadata:

```markdown
---
name: {prompt_name}
version: 1.0.0
author: {author}
created: {date}
model_compatibility: [{models}]
token_estimate: {estimate}
parameters:
  - name: {param1}
    type: string
    required: true
    description: {desc}
---

## System Instructions

You are a {role} assistant. Your task is to {purpose}.

### Guidelines
- Be concise and accurate
- Follow the output format specified
- Do not hallucinate or make up information

### Constraints
- Maximum response length: {max_tokens} tokens
- Always cite sources when available
- Never provide {prohibited_content}

## Task Instructions

{task_description}

## Output Format

{output_schema}

## Examples

### Example 1
**Input:** {example_input_1}
**Output:** {example_output_1}

### Example 2
**Input:** {example_input_2}
**Output:** {example_output_2}
```

### 5. Generate Test Cases

Create test file for prompt validation:

```python
"""Tests for {prompt_name} prompt."""

import pytest
from prompt_templates import load_prompt, render_prompt

PROMPT_NAME = "{prompt_name}"

def test_prompt_renders():
    """Test prompt renders with valid parameters."""
    prompt = load_prompt(PROMPT_NAME)
    rendered = render_prompt(prompt, {
        "param1": "test_value",
        "param2": "test_value"
    })
    assert len(rendered) > 0

def test_prompt_token_count():
    """Test prompt stays within token limits."""
    prompt = load_prompt(PROMPT_NAME)
    rendered = render_prompt(prompt, TEST_PARAMS)
    token_count = count_tokens(rendered)
    assert token_count < prompt.metadata["token_estimate"] * 1.2

def test_prompt_output_format():
    """Test prompt produces expected output format."""
    # Integration test with actual model
    pass

GOLDEN_TESTS = [
    ({"param1": "value1"}, "expected output pattern"),
]

@pytest.mark.parametrize("params,expected_pattern", GOLDEN_TESTS)
def test_golden_outputs(params, expected_pattern):
    """Test against golden test cases."""
    pass
```

### 6. Generate Documentation

Create prompt documentation:

```markdown
# {prompt_name}

## Overview
{purpose}

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| {param1} | string | yes | {description} |

## Usage

\`\`\`python
from prompts import load_prompt

prompt = load_prompt("{prompt_name}")
rendered = prompt.render(param1="value")
\`\`\`

## Token Usage
- Base prompt: ~{base_tokens} tokens
- With typical parameters: ~{typical_tokens} tokens
- Maximum: {max_tokens} tokens

## Model Compatibility
- ✅ GPT-4 Turbo
- ✅ GPT-3.5 Turbo
- ✅ Claude 3

## Version History
- 1.0.0: Initial version
```

### 7. Validate and Report

// turbo
Validate prompt against constitution:
- [ ] Metadata header present
- [ ] No embedded PII/secrets
- [ ] Version specified
- [ ] Model compatibility documented
- [ ] Examples included
- [ ] Test cases created

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or incomplete | Stop. Prompt for prompt name, purpose, target model, output format, and parameters before generating files. |
| Unsupported target model | Stop. Ask the user to choose a supported target or broaden to `all` if cross-model output is intended. |
| Template rendering fails due to missing parameters | Report the missing parameter names, keep the prompt template unchanged, and regenerate only after placeholders are fully specified. |
| Token estimate exceeds configured ceiling | Warn, suggest trimming examples or constraints, and update the metadata before finalizing the prompt. |
| Generated prompt embeds secrets, PII, or policy-violating exemplars | Stop. Remove the unsafe content and rerun validation before writing the prompt artifacts. |

## Examples

**Example 1**: `/scaffold-prompt-engineer response-generator "Generate customer responses" gpt-4 json`

**Example 2**: `/scaffold-prompt-engineer data-extractor "Extract entities from text" all structured`
