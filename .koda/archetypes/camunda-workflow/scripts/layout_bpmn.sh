#!/bin/bash
#
# BPMN Auto-Layout Shell Wrapper
#
# This script provides an easy way to run the bpmn-auto-layout tool
# to fix overlapping flows and improve diagram visibility.
#
# Usage:
#   ./layout_bpmn.sh [options] [file.bpmn|directory]
#
# Options:
#   -a, --all       Process all BPMN files in the default bpmn directory
#   -i, --in-place  Overwrite original files (use with caution)
#   -h, --help      Show this help message
#
# Examples:
#   ./layout_bpmn.sh workflow.bpmn
#   ./layout_bpmn.sh --all
#   ./layout_bpmn.sh --all --in-place
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAYOUT_DIR="${SCRIPT_DIR}/layout"
BPMN_DIR="${SCRIPT_DIR}/../src/main/resources/bpmn"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_banner() {
  echo -e "${BLUE}"
  echo "╔══════════════════════════════════════════════════╗"
  echo "║         BPMN Auto-Layout Tool                    ║"
  echo "║   Fix overlapping flows & improve visibility     ║"
  echo "╚══════════════════════════════════════════════════╝"
  echo -e "${NC}"
}

print_help() {
  echo "Usage: $0 [options] [file.bpmn|directory]"
  echo ""
  echo "Options:"
  echo "  -a, --all       Process all BPMN files in src/main/resources/bpmn"
  echo "  -i, --in-place  Overwrite original files (use with caution)"
  echo "  -h, --help      Show this help message"
  echo ""
  echo "Examples:"
  echo "  $0 workflow.bpmn                    # Layout single file"
  echo "  $0 workflow.bpmn output.bpmn        # Layout to specific output"
  echo "  $0 --all                            # Layout all BPMN files"
  echo "  $0 --all --in-place                 # Layout all and overwrite"
  echo ""
}

check_dependencies() {
  if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Error: Node.js is not installed${NC}"
    echo "   Please install Node.js 16+ from https://nodejs.org"
    exit 1
  fi

  if [ ! -d "${LAYOUT_DIR}/node_modules" ]; then
    echo -e "${YELLOW}⚠️  Dependencies not installed. Installing...${NC}"
    cd "${LAYOUT_DIR}"
    npm install
    cd - > /dev/null
    echo -e "${GREEN}✅ Dependencies installed${NC}"
  fi
}

# Parse arguments
ALL_MODE=false
IN_PLACE=false
INPUT_FILE=""
OUTPUT_FILE=""

while [[ $# -gt 0 ]]; do
  case $1 in
    -a|--all)
      ALL_MODE=true
      shift
      ;;
    -i|--in-place)
      IN_PLACE=true
      shift
      ;;
    -h|--help)
      print_banner
      print_help
      exit 0
      ;;
    *)
      if [ -z "${INPUT_FILE}" ]; then
        INPUT_FILE="$1"
      else
        OUTPUT_FILE="$1"
      fi
      shift
      ;;
  esac
done

# Main execution
print_banner
check_dependencies

if [ "${ALL_MODE}" = true ]; then
  echo -e "${BLUE}📁 Processing all BPMN files in: ${BPMN_DIR}${NC}"
  
  IN_PLACE_ARG=""
  if [ "${IN_PLACE}" = true ]; then
    echo -e "${YELLOW}⚠️  WARNING: In-place mode - original files will be overwritten${NC}"
    read -p "   Continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      echo "Aborted."
      exit 0
    fi
    IN_PLACE_ARG="--in-place"
  fi
  
  cd "${LAYOUT_DIR}"
  node layout-all-bpmn.js "${BPMN_DIR}" ${IN_PLACE_ARG}
  
elif [ -n "${INPUT_FILE}" ]; then
  # Single file mode
  if [ ! -f "${INPUT_FILE}" ]; then
    # Try relative to BPMN directory
    if [ -f "${BPMN_DIR}/${INPUT_FILE}" ]; then
      INPUT_FILE="${BPMN_DIR}/${INPUT_FILE}"
    else
      echo -e "${RED}❌ Error: File not found: ${INPUT_FILE}${NC}"
      exit 1
    fi
  fi
  
  cd "${LAYOUT_DIR}"
  
  if [ -n "${OUTPUT_FILE}" ]; then
    node layout-bpmn.js "${INPUT_FILE}" "${OUTPUT_FILE}"
  else
    node layout-bpmn.js "${INPUT_FILE}"
  fi
  
else
  echo -e "${YELLOW}No input specified.${NC}"
  echo ""
  print_help
  exit 1
fi

echo ""
echo -e "${GREEN}✨ Done!${NC}"
