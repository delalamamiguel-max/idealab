#!/bin/bash
# Validate BPMN files against Camunda Orchestration constitution rules
# Usage: ./validate_bpmn.sh <bpmn_directory>

set -euo pipefail

BPMN_DIR="${1:-src/main/resources/bpmn}"
EXIT_CODE=0

echo "=== Camunda BPMN Constitution Validator ==="
echo "Scanning directory: ${BPMN_DIR}"
echo ""

if [ ! -d "${BPMN_DIR}" ]; then
  echo "ERROR: Directory ${BPMN_DIR} does not exist."
  exit 1
fi

BPMN_FILES=$(find "${BPMN_DIR}" -name "*.bpmn" -type f 2>/dev/null)

if [ -z "${BPMN_FILES}" ]; then
  echo "WARNING: No .bpmn files found in ${BPMN_DIR}"
  exit 0
fi

for FILE in ${BPMN_FILES}; do
  echo "--- Checking: ${FILE} ---"

  # Rule: isExecutable must be true
  if ! grep -q 'isExecutable="true"' "${FILE}"; then
    echo "  FAIL: Process not marked isExecutable=\"true\""
    EXIT_CODE=1
  fi

  # Rule: historyTimeToLive must be set
  if ! grep -q 'camunda:historyTimeToLive' "${FILE}"; then
    echo "  FAIL: Missing camunda:historyTimeToLive"
    EXIT_CODE=1
  fi

  # Rule: Check for exclusive gateways without default flows
  GATEWAY_COUNT=$(grep -c 'exclusiveGateway' "${FILE}" 2>/dev/null || echo "0")
  DEFAULT_COUNT=$(grep -c 'default=' "${FILE}" 2>/dev/null || echo "0")
  if [ "${GATEWAY_COUNT}" -gt 0 ] && [ "${DEFAULT_COUNT}" -lt "${GATEWAY_COUNT}" ]; then
    echo "  WARN: ${GATEWAY_COUNT} exclusive gateways found but only ${DEFAULT_COUNT} have default flows"
  fi

  # Rule: Check for external tasks with error boundary events
  EXTERNAL_TASK_COUNT=$(grep -c 'camunda:type="external"' "${FILE}" 2>/dev/null || echo "0")
  BOUNDARY_ERROR_COUNT=$(grep -c 'boundaryEvent.*errorEventDefinition\|errorEventDefinition.*boundaryEvent' "${FILE}" 2>/dev/null || echo "0")
  if [ "${EXTERNAL_TASK_COUNT}" -gt 0 ] && [ "${BOUNDARY_ERROR_COUNT}" -lt "${EXTERNAL_TASK_COUNT}" ]; then
    echo "  WARN: ${EXTERNAL_TASK_COUNT} external tasks but only ${BOUNDARY_ERROR_COUNT} error boundary events"
  fi

  # Rule: Check for snake_case process ID
  PROCESS_ID=$(grep -oP 'bpmn:process id="\K[^"]+' "${FILE}" 2>/dev/null || echo "")
  if [ -n "${PROCESS_ID}" ]; then
    if echo "${PROCESS_ID}" | grep -qP '[A-Z]'; then
      echo "  FAIL: Process ID '${PROCESS_ID}' is not snake_case"
      EXIT_CODE=1
    fi
  fi

  echo "  Done."
  echo ""
done

if [ ${EXIT_CODE} -eq 0 ]; then
  echo "=== All checks passed ==="
else
  echo "=== Some checks FAILED — review violations above ==="
fi

exit ${EXIT_CODE}
