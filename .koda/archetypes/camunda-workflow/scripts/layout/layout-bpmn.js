#!/usr/bin/env node
/**
 * BPMN Auto-Layout Tool
 * 
 * Automatically layouts BPMN diagrams to fix overlapping flows and improve visibility.
 * Uses bpmn-auto-layout library for optimal element positioning.
 * 
 * Usage:
 *   node layout-bpmn.js <input.bpmn> [output.bpmn]
 *   
 * If output is not specified, creates <input>_layouted.bpmn
 */

const fs = require('fs-extra');
const path = require('path');
const { layoutProcess } = require('bpmn-auto-layout');

const LAYOUT_OPTIONS = {
  // Horizontal spacing between elements
  horizontalSpacing: 150,
  // Vertical spacing between elements  
  verticalSpacing: 100,
  // Edge routing style: 'orthogonal' or 'bezier'
  edgeRouting: 'orthogonal'
};

async function layoutBpmn(inputPath, outputPath) {
  console.log(`\n📐 BPMN Auto-Layout Tool`);
  console.log(`${'─'.repeat(50)}`);
  
  // Validate input file
  if (!fs.existsSync(inputPath)) {
    console.error(`❌ Error: Input file not found: ${inputPath}`);
    process.exit(1);
  }

  const absoluteInput = path.resolve(inputPath);
  const absoluteOutput = outputPath 
    ? path.resolve(outputPath)
    : absoluteInput.replace('.bpmn', '_layouted.bpmn');

  console.log(`📄 Input:  ${absoluteInput}`);
  console.log(`📄 Output: ${absoluteOutput}`);

  try {
    // Read the BPMN file
    const bpmnXml = await fs.readFile(absoluteInput, 'utf-8');
    console.log(`\n⏳ Applying auto-layout...`);

    // Apply auto-layout
    const layoutedXml = await layoutProcess(bpmnXml);

    // Write the layouted BPMN
    await fs.writeFile(absoluteOutput, layoutedXml, 'utf-8');
    
    console.log(`✅ Layout complete!`);
    console.log(`\n📊 Statistics:`);
    
    // Count elements for statistics
    const elementCount = (bpmnXml.match(/<bpmn:(task|serviceTask|callActivity|exclusiveGateway|inclusiveGateway|startEvent|endEvent)/g) || []).length;
    const flowCount = (bpmnXml.match(/<bpmn:sequenceFlow/g) || []).length;
    
    console.log(`   • Elements repositioned: ${elementCount}`);
    console.log(`   • Sequence flows routed: ${flowCount}`);
    console.log(`\n💡 Open in Camunda Modeler to view the result.`);
    
    return absoluteOutput;
  } catch (error) {
    console.error(`\n❌ Layout failed: ${error.message}`);
    
    if (error.message.includes('no diagram to layout')) {
      console.error(`   The BPMN file may be missing diagram information (bpmndi:BPMNDiagram).`);
    }
    
    process.exit(1);
  }
}

// CLI execution
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(`
Usage: node layout-bpmn.js <input.bpmn> [output.bpmn]

Arguments:
  input.bpmn   - Path to the BPMN file to layout
  output.bpmn  - Optional output path (default: <input>_layouted.bpmn)

Examples:
  node layout-bpmn.js workflow.bpmn
  node layout-bpmn.js workflow.bpmn workflow_clean.bpmn
`);
    process.exit(0);
  }

  const inputPath = args[0];
  const outputPath = args[1];

  layoutBpmn(inputPath, outputPath);
}

module.exports = { layoutBpmn };
