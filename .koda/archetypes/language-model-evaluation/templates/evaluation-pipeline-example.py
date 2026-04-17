"""
Complete LLM Evaluation Pipeline Example

This script demonstrates how to build an end-to-end LLM evaluation pipeline
using the grader library and YAML configuration.

Last Updated: 2025-12-01
Constitution: .cdo-aifc/memory/archetypes/02-ml-operations-lifecycle/language-model-evaluation-constitution.md
"""

import asyncio
import pandas as pd
import yaml
import os
from typing import List, Dict, Any
from grader_library import (
    EvaluationInput,
    GradeResult,
    BaseGrader,
    Heuristic,
    LLMJudge,
    Evaluator,
    LengthCheckGrader,
    FormatValidatorGrader,
    KeywordPresenceGrader
)


# ============================================================================
# Configuration Loading
# ============================================================================

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load YAML configuration file.
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


# ============================================================================
# Data Loading
# ============================================================================

def load_data_from_file(data_config: Dict[str, Any]) -> List[EvaluationInput]:
    """
    Load evaluation data from file sources (CSV, JSONL, Parquet).
    """
    file_format = data_config['format']
    location = data_config['location']
    columns = data_config.get('columns', {})
    
    # Load data based on format
    if file_format == 'csv':
        df = pd.read_csv(location)
    elif file_format == 'jsonl':
        df = pd.read_json(location, lines=True)
    elif file_format == 'parquet':
        df = pd.read_parquet(location)
    else:
        raise ValueError(f"Unsupported format: {file_format}")
    
    # Map columns to EvaluationInput fields
    prompt_col = columns.get('prompt', 'prompt')
    response_col = columns.get('response', 'response')
    system_prompt_col = columns.get('system_prompt')
    context_cols = columns.get('context', [])
    
    # Validate required columns
    if response_col not in df.columns:
        raise ValueError(f"Required column '{response_col}' not found in data")
    
    # Create EvaluationInput objects
    inputs = []
    for _, row in df.iterrows():
        context = {col: row[col] for col in context_cols if col in df.columns}
        
        inputs.append(EvaluationInput(
            response=str(row[response_col]),
            prompt=str(row[prompt_col]) if prompt_col in df.columns else None,
            system_prompt=str(row[system_prompt_col]) if system_prompt_col and system_prompt_col in df.columns else None,
            context=context
        ))
    
    return inputs


# ============================================================================
# Grader Creation
# ============================================================================

def create_heuristic_grader(grader_config: Dict[str, Any]) -> Heuristic:
    """
    Factory function to create heuristic graders from config.
    """
    name = grader_config['name']
    
    if name == 'length_check':
        # Extract length parameters from logic description
        return LengthCheckGrader(min_length=50, max_length=500)
    
    elif name == 'format_validator':
        return FormatValidatorGrader(required_fields=['answer', 'confidence'])
    
    else:
        raise ValueError(f"Unknown heuristic grader: {name}")


async def create_llm_judge_grader(grader_config: Dict[str, Any]) -> LLMJudge:
    """
    Factory function to create LLM judge graders from config.
    """
    name = grader_config['name']
    template = grader_config['judge_prompt_template']
    llm_config = grader_config.get('llm_config', {})
    
    # Create LLM callable (mock implementation for example)
    # In production, this would call actual LLM API
    async def mock_llm_callable(prompt: str) -> str:
        """
        Mock LLM callable for demonstration.
        Replace with actual API call in production.
        """
        # Simulate async API call
        await asyncio.sleep(0.1)
        
        # Return mock response based on grader type
        if 'correctness' in name.lower():
            return "Score: 8.5\n\nThe response is mostly correct with minor inaccuracies."
        elif 'safety' in name.lower():
            return "Score: 1.0\n\nThe response is completely safe with no harmful content."
        else:
            return "Score: 7.0\n\nGeneric evaluation result."
    
    return LLMJudge(
        name=name,
        judge_prompt_template=template,
        llm_callable=mock_llm_callable
    )


async def create_graders_from_config(graders_config: List[Dict[str, Any]]) -> List[BaseGrader]:
    """
    Create all graders from configuration.
    """
    graders = []
    
    for grader_config in graders_config:
        grader_type = grader_config['type']
        
        if grader_type == 'heuristic':
            grader = create_heuristic_grader(grader_config)
            graders.append(grader)
        
        elif grader_type == 'llm_judge':
            grader = await create_llm_judge_grader(grader_config)
            graders.append(grader)
        
        else:
            raise ValueError(f"Unknown grader type: {grader_type}")
    
    return graders


# ============================================================================
# Results Analysis
# ============================================================================

def aggregate_results(results_df: pd.DataFrame, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute aggregated metrics from evaluation results.
    """
    aggregation_config = config['output'].get('aggregation', {})
    metrics_to_compute = aggregation_config.get('metrics', ['mean', 'median'])
    group_by_cols = aggregation_config.get('group_by', [])
    
    # Get score columns
    score_cols = [col for col in results_df.columns if col.endswith('_score')]
    
    # Compute aggregated metrics
    aggregated = {}
    
    for score_col in score_cols:
        grader_name = score_col.replace('_score', '')
        grader_metrics = {}
        
        if 'mean' in metrics_to_compute:
            grader_metrics['mean'] = results_df[score_col].mean()
        if 'median' in metrics_to_compute:
            grader_metrics['median'] = results_df[score_col].median()
        if 'std' in metrics_to_compute:
            grader_metrics['std'] = results_df[score_col].std()
        if 'pass_rate' in metrics_to_compute:
            # Assume pass if score >= 0.7
            grader_metrics['pass_rate'] = (results_df[score_col] >= 0.7).mean()
        
        aggregated[grader_name] = grader_metrics
    
    return aggregated


def check_decision_criteria(results_df: pd.DataFrame, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check if evaluation results meet decision criteria.
    """
    decision_config = config.get('decision_criteria', {})
    hard_stops = decision_config.get('hard_stops', {})
    targets = decision_config.get('targets', {})
    
    decision_result = {
        'pass': True,
        'hard_stop_violations': [],
        'target_misses': []
    }
    
    # Check hard stops
    for grader_name, threshold in hard_stops.items():
        score_col = f"{grader_name}_score"
        if score_col in results_df.columns:
            mean_score = results_df[score_col].mean()
            if mean_score < threshold:
                decision_result['pass'] = False
                decision_result['hard_stop_violations'].append({
                    'grader': grader_name,
                    'threshold': threshold,
                    'actual': mean_score
                })
    
    # Check targets (warnings only)
    for grader_name, threshold in targets.items():
        score_col = f"{grader_name}_score"
        if score_col in results_df.columns:
            mean_score = results_df[score_col].mean()
            if mean_score < threshold:
                decision_result['target_misses'].append({
                    'grader': grader_name,
                    'threshold': threshold,
                    'actual': mean_score
                })
    
    return decision_result


def generate_prose_report(results_df: pd.DataFrame, aggregated: Dict[str, Any], 
                         decision: Dict[str, Any], config: Dict[str, Any]) -> str:
    """
    Generate human-readable evaluation report in Markdown.
    """
    evaluation_name = config['evaluation_name']
    
    report = f"# {evaluation_name} - Evaluation Report\n\n"
    
    # Executive Summary
    report += "## Executive Summary\n\n"
    report += f"- Total samples evaluated: {len(results_df)}\n"
    report += f"- Number of graders: {len(aggregated)}\n"
    report += f"- Overall decision: {'**PASS**' if decision['pass'] else '**FAIL**'}\n\n"
    
    # Per-Grader Analysis
    report += "## Per-Grader Analysis\n\n"
    for grader_name, metrics in aggregated.items():
        report += f"### {grader_name}\n\n"
        for metric_name, value in metrics.items():
            report += f"- {metric_name}: {value:.3f}\n"
        report += "\n"
    
    # Failure Highlights
    if decision['hard_stop_violations']:
        report += "## 🚫 Hard-Stop Violations\n\n"
        for violation in decision['hard_stop_violations']:
            report += f"- **{violation['grader']}**: Required {violation['threshold']:.2f}, got {violation['actual']:.2f}\n"
        report += "\n"
    
    if decision['target_misses']:
        report += "## ⚠️ Target Misses (Warnings)\n\n"
        for miss in decision['target_misses']:
            report += f"- **{miss['grader']}**: Target {miss['threshold']:.2f}, got {miss['actual']:.2f}\n"
        report += "\n"
    
    # Recommendations
    report += "## Recommendations\n\n"
    if decision['pass']:
        report += "- ✅ Evaluation passed all hard-stop criteria\n"
        report += "- Consider deploying model to production\n"
        if decision['target_misses']:
            report += "- Monitor target metrics that missed thresholds\n"
    else:
        report += "- ❌ Evaluation failed hard-stop criteria\n"
        report += "- Do NOT deploy to production\n"
        report += "- Address hard-stop violations before retrying\n"
    
    return report


# ============================================================================
# Main Pipeline
# ============================================================================

async def run_evaluation_pipeline(config_path: str):
    """
    Execute complete evaluation pipeline.
    """
    print(f"Loading configuration from {config_path}...")
    config = load_config(config_path)
    
    print(f"Evaluation: {config['evaluation_name']}")
    print(f"Description: {config['description']}\n")
    
    # Load data
    print("Loading evaluation data...")
    data_config = config['data_source']
    inputs = load_data_from_file(data_config)
    print(f"Loaded {len(inputs)} samples\n")
    
    # Create graders
    print("Creating graders...")
    graders = await create_graders_from_config(config['graders'])
    print(f"Created {len(graders)} graders\n")
    
    # Create evaluator
    settings = config['settings']
    evaluator = Evaluator(
        graders=graders,
        max_concurrency=settings['max_concurrency']
    )
    
    # Run evaluation
    print("Running evaluation...")
    results_df = await evaluator.evaluate_batch(inputs)
    print(f"Evaluation complete!\n")
    
    # Save raw results
    output_config = config['output']
    if output_config.get('structured'):
        structured_config = output_config['structured']
        results_path = structured_config['path']
        os.makedirs(os.path.dirname(results_path), exist_ok=True)
        results_df.to_csv(results_path, index=False)
        print(f"Saved raw results to {results_path}")
    
    # Aggregate results
    print("\nAggregating results...")
    aggregated = aggregate_results(results_df, config)
    
    # Check decision criteria
    print("Checking decision criteria...")
    decision = check_decision_criteria(results_df, config)
    
    # Generate prose report
    if output_config.get('prose_report', {}).get('enabled'):
        print("\nGenerating prose report...")
        report = generate_prose_report(results_df, aggregated, decision, config)
        
        report_config = output_config['prose_report']
        report_path = report_config['path']
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"Saved report to {report_path}")
    
    # Print summary
    print("\n" + "="*80)
    print("EVALUATION SUMMARY")
    print("="*80)
    print(f"\nDecision: {'PASS' if decision['pass'] else 'FAIL'}")
    
    if decision['hard_stop_violations']:
        print("\nHard-Stop Violations:")
        for v in decision['hard_stop_violations']:
            print(f"  - {v['grader']}: {v['actual']:.3f} < {v['threshold']:.3f}")
    
    print("\nAggregated Metrics:")
    for grader_name, metrics in aggregated.items():
        print(f"  {grader_name}: mean={metrics.get('mean', 0):.3f}")
    
    print("\n" + "="*80)
    
    return results_df, aggregated, decision


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    # Example: run with config file
    config_file = "language-model-evaluation.yaml"
    
    # Run pipeline
    results, aggregated, decision = asyncio.run(run_evaluation_pipeline(config_file))
