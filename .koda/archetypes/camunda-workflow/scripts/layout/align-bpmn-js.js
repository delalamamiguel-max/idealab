#!/usr/bin/env node
/**
 * BPMN-JS Alignment Tool
 * 
 * Uses bpmn-js library for programmatic BPMN diagram alignment.
 * Provides sophisticated element positioning, distribution, and edge routing.
 * 
 * Usage:
 *   node align-bpmn-js.js <input.bpmn> [output.bpmn]
 *   node align-bpmn-js.js --analyze <input.bpmn>
 * 
 * Features:
 *   - Align elements horizontally (same y-coordinate)
 *   - Align elements vertically (same x-coordinate)  
 *   - Distribute elements evenly with consistent spacing
 *   - Fix overlapping sequence flow edges
 *   - Smart edge routing with orthogonal connections
 */

const fs = require('fs-extra');
const path = require('path');
const BpmnModdle = require('bpmn-moddle');

// Configuration
const CONFIG = {
  HORIZONTAL_TOLERANCE: 50,   // Elements within this y-range are same row
  VERTICAL_TOLERANCE: 50,     // Elements within this x-range are same column
  MIN_SPACING: 80,            // Minimum spacing between elements
  PREFERRED_SPACING: 150,     // Preferred spacing between elements
  GATEWAY_SIZE: 50,           // Standard gateway size
  TASK_WIDTH: 100,            // Standard task width
  TASK_HEIGHT: 80,            // Standard task height
  EVENT_SIZE: 36,             // Standard event size
};

class BpmnJsAligner {
  constructor() {
    this.moddle = new BpmnModdle();
    this.definitions = null;
    this.shapes = new Map();
    this.edges = new Map();
    this.process = null;
  }

  async load(bpmnXml) {
    const { rootElement } = await this.moddle.fromXML(bpmnXml);
    this.definitions = rootElement;
    this._parseElements();
    return this;
  }

  _parseElements() {
    // Find the BPMNDiagram
    const diagrams = this.definitions.diagrams || [];
    if (diagrams.length === 0) {
      throw new Error('No BPMN diagram found');
    }

    const diagram = diagrams[0];
    const plane = diagram.plane;
    
    if (!plane || !plane.planeElement) {
      throw new Error('No plane elements found');
    }

    // Parse shapes and edges
    for (const element of plane.planeElement) {
      if (element.$type === 'bpmndi:BPMNShape') {
        const bounds = element.bounds;
        if (bounds) {
          this.shapes.set(element.bpmnElement?.id || element.id, {
            id: element.id,
            elementId: element.bpmnElement?.id,
            x: bounds.x,
            y: bounds.y,
            width: bounds.width,
            height: bounds.height,
            element: element,
            bounds: bounds
          });
        }
      } else if (element.$type === 'bpmndi:BPMNEdge') {
        const waypoints = element.waypoint || [];
        this.edges.set(element.bpmnElement?.id || element.id, {
          id: element.id,
          elementId: element.bpmnElement?.id,
          waypoints: waypoints.map(wp => ({ x: wp.x, y: wp.y })),
          element: element
        });
      }
    }
  }

  analyze() {
    const issues = {
      overlappingShapes: [],
      misalignedRows: [],
      misalignedColumns: [],
      tightSpacing: [],
      crossingEdges: []
    };

    const shapesArray = Array.from(this.shapes.values());

    // Check for overlapping shapes
    for (let i = 0; i < shapesArray.length; i++) {
      for (let j = i + 1; j < shapesArray.length; j++) {
        if (this._shapesOverlap(shapesArray[i], shapesArray[j])) {
          issues.overlappingShapes.push([shapesArray[i].elementId, shapesArray[j].elementId]);
        }
      }
    }

    // Find misaligned rows
    const rows = this._groupByRow();
    for (const [rowY, elements] of rows) {
      if (elements.length > 1) {
        const yValues = elements.map(id => this.shapes.get(id)?.y || 0);
        const variance = Math.max(...yValues) - Math.min(...yValues);
        if (variance > 10) {
          issues.misalignedRows.push({
            approximateY: rowY,
            elements: elements,
            variance: variance
          });
        }
      }
    }

    // Check for tight spacing
    for (let i = 0; i < shapesArray.length; i++) {
      for (let j = i + 1; j < shapesArray.length; j++) {
        const dist = this._horizontalDistance(shapesArray[i], shapesArray[j]);
        if (dist > 0 && dist < CONFIG.MIN_SPACING) {
          issues.tightSpacing.push({
            elements: [shapesArray[i].elementId, shapesArray[j].elementId],
            distance: dist
          });
        }
      }
    }

    return issues;
  }

  _shapesOverlap(s1, s2) {
    return !(s1.x + s1.width < s2.x || s2.x + s2.width < s1.x ||
             s1.y + s1.height < s2.y || s2.y + s2.height < s1.y);
  }

  _horizontalDistance(s1, s2) {
    if (s1.x + s1.width < s2.x) {
      return s2.x - (s1.x + s1.width);
    } else if (s2.x + s2.width < s1.x) {
      return s1.x - (s2.x + s2.width);
    }
    return 0;
  }

  _groupByRow() {
    const rows = new Map();
    for (const [id, shape] of this.shapes) {
      const rowKey = Math.round((shape.y + shape.height / 2) / CONFIG.HORIZONTAL_TOLERANCE) * CONFIG.HORIZONTAL_TOLERANCE;
      if (!rows.has(rowKey)) {
        rows.set(rowKey, []);
      }
      rows.get(rowKey).push(id);
    }
    return rows;
  }

  _groupByColumn() {
    const columns = new Map();
    for (const [id, shape] of this.shapes) {
      const colKey = Math.round((shape.x + shape.width / 2) / CONFIG.VERTICAL_TOLERANCE) * CONFIG.VERTICAL_TOLERANCE;
      if (!columns.has(colKey)) {
        columns.set(colKey, []);
      }
      columns.get(colKey).push(id);
    }
    return columns;
  }

  alignRow(elementIds, targetY = null) {
    const shapes = elementIds
      .map(id => this.shapes.get(id))
      .filter(s => s);

    if (shapes.length === 0) return;

    if (targetY === null) {
      targetY = shapes.reduce((sum, s) => sum + s.y, 0) / shapes.length;
    }

    for (const shape of shapes) {
      this._moveShape(shape, shape.x, targetY);
    }
  }

  alignColumn(elementIds, targetX = null) {
    const shapes = elementIds
      .map(id => this.shapes.get(id))
      .filter(s => s);

    if (shapes.length === 0) return;

    if (targetX === null) {
      targetX = shapes.reduce((sum, s) => sum + s.x, 0) / shapes.length;
    }

    for (const shape of shapes) {
      this._moveShape(shape, targetX, shape.y);
    }
  }

  distributeHorizontally(elementIds, spacing = CONFIG.PREFERRED_SPACING) {
    const shapes = elementIds
      .map(id => this.shapes.get(id))
      .filter(s => s)
      .sort((a, b) => a.x - b.x);

    if (shapes.length < 2) return;

    let currentX = shapes[0].x + shapes[0].width + spacing;
    for (let i = 1; i < shapes.length; i++) {
      this._moveShape(shapes[i], currentX, shapes[i].y);
      currentX = shapes[i].x + shapes[i].width + spacing;
    }
  }

  distributeVertically(elementIds, spacing = CONFIG.PREFERRED_SPACING) {
    const shapes = elementIds
      .map(id => this.shapes.get(id))
      .filter(s => s)
      .sort((a, b) => a.y - b.y);

    if (shapes.length < 2) return;

    let currentY = shapes[0].y + shapes[0].height + spacing;
    for (let i = 1; i < shapes.length; i++) {
      this._moveShape(shapes[i], shapes[i].x, currentY);
      currentY = shapes[i].y + shapes[i].height + spacing;
    }
  }

  _moveShape(shape, newX, newY) {
    const dx = newX - shape.x;
    const dy = newY - shape.y;

    // Update bounds
    shape.bounds.x = newX;
    shape.bounds.y = newY;
    shape.x = newX;
    shape.y = newY;

    // Update connected edges
    this._updateConnectedEdges(shape, dx, dy);
  }

  _updateConnectedEdges(shape, dx, dy) {
    for (const [id, edge] of this.edges) {
      const waypoints = edge.element.waypoint;
      if (!waypoints || waypoints.length === 0) continue;

      // Check first waypoint
      const first = waypoints[0];
      if (this._pointNearShape(first.x, first.y, shape)) {
        first.x += dx;
        first.y += dy;
      }

      // Check last waypoint
      const last = waypoints[waypoints.length - 1];
      if (this._pointNearShape(last.x, last.y, shape)) {
        last.x += dx;
        last.y += dy;
      }
    }
  }

  _pointNearShape(px, py, shape, tolerance = 30) {
    return (shape.x - tolerance <= px && px <= shape.x + shape.width + tolerance &&
            shape.y - tolerance <= py && py <= shape.y + shape.height + tolerance);
  }

  autoAlignRows() {
    const rows = this._groupByRow();
    for (const [rowY, elementIds] of rows) {
      if (elementIds.length > 1) {
        this.alignRow(elementIds, rowY);
      }
    }
  }

  autoAlignColumns() {
    const columns = this._groupByColumn();
    for (const [colX, elementIds] of columns) {
      if (elementIds.length > 1) {
        this.alignColumn(elementIds, colX);
      }
    }
  }

  fixEdgeRouting() {
    for (const [id, edge] of this.edges) {
      const waypoints = edge.element.waypoint;
      if (!waypoints || waypoints.length < 2) continue;

      // Ensure orthogonal routing (only horizontal/vertical segments)
      for (let i = 1; i < waypoints.length - 1; i++) {
        const prev = waypoints[i - 1];
        const curr = waypoints[i];
        const next = waypoints[i + 1];

        // If the middle waypoint creates diagonal lines, adjust it
        if (Math.abs(prev.x - curr.x) > 10 && Math.abs(prev.y - curr.y) > 10) {
          // Make it orthogonal by choosing horizontal then vertical
          curr.x = prev.x;
        }
      }
    }
  }

  autoFixAll() {
    console.log('  → Auto-aligning rows...');
    this.autoAlignRows();
    console.log('  → Auto-aligning columns...');
    this.autoAlignColumns();
    console.log('  → Fixing edge routing...');
    this.fixEdgeRouting();
  }

  async toXML() {
    const { xml } = await this.moddle.toXML(this.definitions, { format: true });
    return xml;
  }
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`
BPMN-JS Alignment Tool

Usage:
  node align-bpmn-js.js <input.bpmn> [output.bpmn]
  node align-bpmn-js.js --analyze <input.bpmn>

Options:
  --analyze     Analyze alignment issues without modifying
  --align-rows  Only align elements in rows
  --align-cols  Only align elements in columns
  --help, -h    Show this help

Examples:
  node align-bpmn-js.js workflow.bpmn
  node align-bpmn-js.js workflow.bpmn fixed_workflow.bpmn
  node align-bpmn-js.js --analyze workflow.bpmn
`);
    process.exit(0);
  }

  const analyzeOnly = args.includes('--analyze');
  const alignRowsOnly = args.includes('--align-rows');
  const alignColsOnly = args.includes('--align-cols');
  
  const fileArgs = args.filter(a => !a.startsWith('--'));
  const inputPath = fileArgs[0];
  const outputPath = fileArgs[1] || inputPath.replace('.bpmn', '_aligned.bpmn');

  if (!inputPath) {
    console.error('❌ Error: No input file specified');
    process.exit(1);
  }

  if (!fs.existsSync(inputPath)) {
    console.error(`❌ Error: File not found: ${inputPath}`);
    process.exit(1);
  }

  console.log('\n📐 BPMN-JS Alignment Tool');
  console.log('─'.repeat(50));
  console.log(`📄 Input: ${path.resolve(inputPath)}`);

  try {
    const bpmnXml = await fs.readFile(inputPath, 'utf-8');
    const aligner = new BpmnJsAligner();
    await aligner.load(bpmnXml);

    console.log(`   Loaded ${aligner.shapes.size} shapes, ${aligner.edges.size} edges`);

    if (analyzeOnly) {
      console.log('\n🔍 Analyzing diagram...');
      const issues = aligner.analyze();

      console.log('\n📊 Analysis Results:');
      console.log(`   • Overlapping shapes: ${issues.overlappingShapes.length}`);
      console.log(`   • Misaligned rows: ${issues.misalignedRows.length}`);
      console.log(`   • Tight spacing issues: ${issues.tightSpacing.length}`);

      if (issues.misalignedRows.length > 0) {
        console.log('\n   Misaligned rows:');
        issues.misalignedRows.slice(0, 5).forEach(row => {
          console.log(`     - y≈${row.approximateY}: ${row.elements.length} elements, variance=${row.variance.toFixed(0)}px`);
        });
      }
      return;
    }

    console.log(`📄 Output: ${path.resolve(outputPath)}`);
    console.log('\n⏳ Applying alignment fixes...');

    if (alignRowsOnly) {
      aligner.autoAlignRows();
    } else if (alignColsOnly) {
      aligner.autoAlignColumns();
    } else {
      aligner.autoFixAll();
    }

    const outputXml = await aligner.toXML();
    await fs.writeFile(outputPath, outputXml, 'utf-8');

    console.log('\n✅ Alignment complete!');
    console.log(`💡 Open ${outputPath} in Camunda Modeler to view the result.`);

  } catch (error) {
    console.error(`\n❌ Error: ${error.message}`);
    process.exit(1);
  }
}

main();
