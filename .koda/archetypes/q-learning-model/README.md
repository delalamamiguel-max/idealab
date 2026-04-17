# Q-learning Model Archetype

## Overview
This archetype sets the foundational guardrails for safe and reproducible Q-learning workflows.

## Core Principles
The following hard-stop rules must be strictly followed:
- **No unbounded training loops**: Define max_episodes and max_steps_per_episode.
- **No invalid hyperparameters**: Validate learning rates, discount factors, and exploration rates.
- **No unsafe environment contracts**: Require deterministic observation/action space metadata and seeded resets.
- **No silent numeric instability**: Fail jobs on NaN/Inf/saturation.
- **No unsecured policy artifacts**: Persist to approved, encrypted paths.

## Standard Pattern
Implementations must demonstrate:
- **Config-first initialization**: Source all params from config.
- **Deterministic seeding**: Seed Python/NumPy/env RNGs.
- **Exploration governance**: Enforce defined epsilon/temperature schedules.
- **Training telemetry**: Log rewards and metrics each episode.
- **Policy validation**: Run deterministic evaluation rollouts.
- **Checkpoint discipline**: Persist versioned Q-tables and optimizer state.
