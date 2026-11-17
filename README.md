# IdeaLab Experimentation Agent

## Purpose and status

A Python/Streamlit experimentation assistant for searching prior experiments, proposing ideas and drafting experiment intake material, with a telecom market-intelligence pipeline. The application lives in `experimentation-agent-app/`; this root README maps the repository. Generated predictions and recommendations are model output, not validated experiment results or an endorsement by any referenced organization.

## Repository map

- `experimentation-agent-app/app.py`: Streamlit chat interface.
- `experimentation-agent-app/agent_config.py`: context assembly and spreadsheet/Markdown loaders.
- `experimentation-agent-app/thinking_agent.py`: multi-stage reasoning orchestration.
- `experimentation-agent-app/telecom_intel/`: ingestion, classification, reasoning and pipeline modes.
- `experimentation-agent-app/requirements.txt`, `start.sh`: dependencies and startup.
- `experimentation-agent-app/test_integration.py`: integration-check script.
- `documents/`, `experimentation-agent-app/documents/`: source-document locations; do not duplicate their contents into public documentation.
- `UI/`: captured UI-reference artifacts, not an application frontend or verified reusable component library.

## Architecture and integrations

Streamlit handles the UI, OpenAI handles model generation, and pandas/openpyxl support spreadsheet loading. Telecom ingestion includes Apify website/Reddit adapters, while classification/reasoning can use model calls. The pipeline exposes live, cached, dry-run and disk-loaded web-search modes. A dry-run avoids Apify ingestion but does not by itself guarantee that all model calls are disabled; inspect the model setting before execution.

The nested README describes an Excel export and fixed experiment count. The configured workbook is tracked at `experimentation-agent-app/documents/XTrack_Chat_Bot_export_2025-07-28T07_28_00.xlsx`, with another tracked copy under root `documents/`. Its contents and experiment counts were not validated for this README. Current context assembly also loads a Markdown inventory when present; the UI's experiment count/field helpers only inspect Excel, so a zero count does not prove there is no Markdown context. Treat historical dataset counts and performance statements as unverified, not current ground truth.

## Setup and environments

The nested guide specifies Python 3.10+. For separately authorized development, work in `experimentation-agent-app/`, create an isolated Python environment and install the reviewed requirements. Supply private provider configuration through the intended local environment mechanism. Inspect actual files before following nested instructions to copy `.env.example`; template availability is not assumed.

Application configuration includes `OPENAI_API_KEY` and `OPENAI_MODEL`; the telecom configuration additionally reads `APIFY_API_TOKEN`, `APIFY_BASE_URL` and `CLASSIFICATION_MODEL`. Keep keys server-side and out of committed files. Model names in source describe defaults, not verified provider availability or pricing. Use only data approved for disclosure to the selected providers.

## Safe commands

Use `git status --short`, `git diff -- README.md` and `git diff --check` for documentation inspection. The application startup reference is `python3 -m streamlit run app.py` from the application directory. Do not execute it during README work.

`start.sh` may install dependencies automatically before launching Streamlit. Demo, integration-test and telecom pipeline scripts import application/provider modules and can write outputs or contact providers depending on configuration. Names such as “demo”, “test” and “dry_run” are not a blanket no-network/no-cost guarantee. No script was executed here.

## Testing and validation

The integration script checks imports/initialization and related wiring; it is not proof of model accuracy, production access controls or experiment validity. The repository has no root package/test command or verified CI gate. Future validation should use approved synthetic inputs, mocked providers where possible and explicit cost limits. No existing test result is claimed by this README.

## Deployment and rollback

No verified production deployment mapping or rollback procedure is established by the inspected root/application files. Local Streamlit defaults to port 8501 in the startup script. Public hosting requires a separate authentication, data-disclosure, credentials and resource review; do not assume a Streamlit interface provides access control.

For a future deployment, retain a known-good application/dependency revision and handle generated output/data separately. Reverting code does not undo provider calls or disclosure of submitted documents. This README branch remains local pending independent review.

## Risks and guardrails

This is a public repository. Do not add internal experiment results, personal data, proprietary intake details, account captures or credential values to the README. Existing document inclusion is not evidence of permission to redistribute it; this change does not modify or endorse those files. Do not scrape, run account-based acquisition, publish generated findings or send messages as part of documentation work. Human review is required before treating a proposed experiment or prediction as actionable evidence.

## Related documentation

- [Application README](experimentation-agent-app/README.md) — includes historical dataset/setup assumptions.
- [Quick start](experimentation-agent-app/QUICK_START.md)
- [Thinking-agent integration](experimentation-agent-app/THINKING_AGENT_INTEGRATION.md)
- [Knowledge-layer guide](experimentation-agent-app/KNOWLEDGE_LAYER_GUIDE.md)
- [Dependency manifest](experimentation-agent-app/requirements.txt)

No new license or third-party endorsement is asserted here.

This README update was checked statically only. No installs, application builds/tests, provider calls, database operations, skill installations or deployments were performed. Live hosting, external URLs and runtime behavior remain unverified.
