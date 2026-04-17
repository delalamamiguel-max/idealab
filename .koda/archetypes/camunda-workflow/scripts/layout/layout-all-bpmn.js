#!/usr/bin/env node
/**
 * Batch BPMN Auto-Layout Tool
 * 
 * Processes all BPMN files in a directory and applies auto-layout.
 * Useful for post-processing archetype-generated workflows.
 * 
 * Usage:
 *   node layout-all-bpmn.js [bpmn-directory] [--in-place]
 *   
 * Options:
 *   --in-place    Overwrite original files instead of creating _layouted versions
 */

const fs = require('fs-extra');
const path = require('path');
const { glob } = require('glob');
const { layoutProcess } = require('bpmn-auto-layout');

const DEFAULT_BPMN_DIR = '../../src/main/resources/bpmn';

async function layoutAllBpmn(bpmnDir, inPlace = false) {
  console.log(`\n📐 Batch BPMN Auto-Layout Tool`);
  console.log(`${'═'.repeat(50)}`);
  
  const absoluteDir = path.resolve(__dirname, bpmnDir);
  
  if (!fs.existsSync(absoluteDir)) {
    console.error(`❌ Error: Directory not found: ${absoluteDir}`);
    process.exit(1);
  }

  console.log(`📁 Directory: ${absoluteDir}`);
  console.log(`📝 Mode: ${inPlace ? 'In-place (overwrite)' : 'Create _layouted copies'}`);

  // Find all BPMN files
  const bpmnFiles = await glob('**/*.bpmn', { 
    cwd: absoluteDir,
    ignore: ['**/*_layouted.bpmn']
  });

  if (bpmnFiles.length === 0) {
    console.log(`\n⚠️  No BPMN files found in ${absoluteDir}`);
    process.exit(0);
  }

  console.log(`\n📄 Found ${bpmnFiles.length} BPMN file(s):\n`);

  let successCount = 0;
  let failCount = 0;
  const results = [];

  for (const file of bpmnFiles) {
    const inputPath = path.join(absoluteDir, file);
    const outputPath = inPlace 
      ? inputPath 
      : inputPath.replace('.bpmn', '_layouted.bpmn');

    console.log(`  ⏳ Processing: ${file}`);

    try {
      const bpmnXml = await fs.readFile(inputPath, 'utf-8');
      const layoutedXml = await layoutProcess(bpmnXml);
      await fs.writeFile(outputPath, layoutedXml, 'utf-8');
      
      console.log(`     ✅ Success → ${path.basename(outputPath)}`);
      successCount++;
      results.push({ file, status: 'success', output: outputPath });
    } catch (error) {
      console.log(`     ❌ Failed: ${error.message}`);
      failCount++;
      results.push({ file, status: 'failed', error: error.message });
    }
  }

  // Summary
  console.log(`\n${'═'.repeat(50)}`);
  console.log(`📊 Summary:`);
  console.log(`   ✅ Successful: ${successCount}`);
  console.log(`   ❌ Failed: ${failCount}`);
  console.log(`   📁 Total: ${bpmnFiles.length}`);

  if (failCount > 0) {
    console.log(`\n⚠️  Some files failed to layout. Review errors above.`);
    process.exit(1);
  }

  console.log(`\n✨ All BPMN files layouted successfully!`);
  return results;
}

// CLI execution
if (require.main === module) {
  const args = process.argv.slice(2);
  
  const inPlace = args.includes('--in-place');
  const dirArg = args.find(arg => !arg.startsWith('--'));
  const bpmnDir = dirArg || DEFAULT_BPMN_DIR;

  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
Usage: node layout-all-bpmn.js [bpmn-directory] [--in-place]

Arguments:
  bpmn-directory  Path to directory containing BPMN files
                  (default: ../../src/main/resources/bpmn)

Options:
  --in-place      Overwrite original files instead of creating copies
  --help, -h      Show this help message

Examples:
  node layout-all-bpmn.js
  node layout-all-bpmn.js ./my-bpmn-files
  node layout-all-bpmn.js --in-place
`);
    process.exit(0);
  }

  layoutAllBpmn(bpmnDir, inPlace);
}

module.exports = { layoutAllBpmn };
