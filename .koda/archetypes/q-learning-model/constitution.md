# Q-learning Model Constitution

## Purpose

This constitution sets the foundational guardrails for the Q-learning model archetype, ensuring safe, reproducible, and auditable reinforcement learning workflows.

## I. Hard-Stop Rules (Non-Negotiable)

- ✘ **No unbounded training loops**: Do not run Q-learning without config-defined `max_episodes` and `max_steps_per_episode`; abort when either value is missing or non-positive.
- ✘ **No invalid hyperparameters**: Do not accept `learning_rate` ≤ 0 or > 1, `discount_factor` < 0 or ≥ 1, or exploration rates outside [0, 1]; validate configs before training.
- ✘ **No unsafe environment contracts**: Do not interact with environments lacking deterministic `observation_space` and `action_space` metadata or support for `reset(seed=...)`; refuse training if interface checks fail.
- ✘ **No silent numeric instability**: Do not continue once Q-values become `NaN`, `Inf`, or exceed configurable saturation thresholds; fail the job and emit diagnostics.
- ✘ **No unsecured policy artifacts**: Do not persist Q-tables, metrics, or checkpoints outside approved storage paths from configuration or without required encryption.

## II. Mandatory Patterns (Must Apply)

- ✔ **Config-first initialization**: Source all hyperparameters, exploration schedules, reward clipping ranges, and persistence paths from external YAML/JSON config; forbid inline literals.
- ✔ **Deterministic seeding**: Seed RNGs for Python, NumPy, and the environment using config-provided values before collecting experience; log the seeds.
- ✔ **Exploration governance**: Implement epsilon (or softmax temperature) schedules defined in config, log per-episode exploration rates, and enforce final minimum values.
- ✔ **Training telemetry**: After each episode, log cumulative reward, episode length, epsilon/temperature, max |ΔQ|, and rolling averages to structured logs or metrics sinks.
- ✔ **Policy validation**: Run deterministic evaluation rollouts at configurable intervals and fail training when average return or success-rate thresholds are not met.
- ✔ **Checkpoint discipline**: Persist versioned Q-table snapshots and optimizer state (if applicable) after each improvement cycle using idempotent writes with overwrite protection.

## III. Preferred Patterns (Recommended)

- ➜ **Vectorized updates**: Use NumPy or framework tensor ops to batch state-action updates where possible; fall back to scalar loops only when the state space is sparse.
- ➜ **Adaptive exploration**: Prefer piecewise or exponential decay schedules with floor enforcement over linear decay for stable convergence.
- ➜ **Reward normalization**: Clip or normalize rewards via config-driven transforms before Q-updates to improve stability.
- ➜ **Experience replay hygiene**: When using replay buffers, cap buffer length, stratify sampling, and purge stale transitions tied to deprecated policies.
- ➜ **Evaluation environments**: Maintain separate evaluation environments seeded differently from training to prevent overfitting to reset conditions.
- ➜ **Telemetry integration**: Emit metrics to centralized observability stacks (Prometheus, Datadog, etc.) with lineage identifiers for audit trails.

---

**Version**: 1.0.0
**Last Updated**: 2025-10-23
**Source**: Derived from Q-learning practices within `vibe_cdo/rl_models/.rules`
