#!/usr/bin/env python3
"""
BPMN Alignment Tool

Programmatically aligns BPMN diagram elements to fix overlapping flows
and improve diagram visibility. Works directly on BPMN XML files.

Usage:
    python align_bpmn.py <input.bpmn> [output.bpmn]
    python align_bpmn.py --analyze <input.bpmn>

Features:
    - Align elements horizontally (same row)
    - Align elements vertically (same column)
    - Distribute elements evenly
    - Fix overlapping sequence flows
    - Detect and report alignment issues
"""

import xml.etree.ElementTree as ET
import argparse
import sys
import os
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

# XML namespaces used in BPMN files
NAMESPACES = {
    'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
    'bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
    'dc': 'http://www.omg.org/spec/DD/20100524/DC',
    'di': 'http://www.omg.org/spec/DD/20100524/DI',
    'camunda': 'http://camunda.org/schema/1.0/bpmn',
}

# Register namespaces to preserve them in output
for prefix, uri in NAMESPACES.items():
    ET.register_namespace(prefix, uri)


@dataclass
class BPMNShape:
    """Represents a BPMN shape with its position and dimensions."""
    id: str
    element_id: str
    x: float
    y: float
    width: float
    height: float
    element: ET.Element
    
    @property
    def center_x(self) -> float:
        return self.x + self.width / 2
    
    @property
    def center_y(self) -> float:
        return self.y + self.height / 2
    
    @property
    def right(self) -> float:
        return self.x + self.width
    
    @property
    def bottom(self) -> float:
        return self.y + self.height


@dataclass
class BPMNEdge:
    """Represents a BPMN edge (sequence flow) with waypoints."""
    id: str
    element_id: str
    waypoints: List[Tuple[float, float]]
    element: ET.Element


class BPMNAligner:
    """Aligns BPMN diagram elements programmatically."""
    
    # Alignment thresholds
    HORIZONTAL_TOLERANCE = 50  # Elements within this y-range are considered same row
    VERTICAL_TOLERANCE = 50    # Elements within this x-range are considered same column
    MIN_SPACING = 80           # Minimum spacing between elements
    PREFERRED_SPACING = 150    # Preferred spacing between elements
    
    def __init__(self, bpmn_path: str):
        self.bpmn_path = bpmn_path
        self.tree = ET.parse(bpmn_path)
        self.root = self.tree.getroot()
        self.shapes: Dict[str, BPMNShape] = {}
        self.edges: Dict[str, BPMNEdge] = {}
        self._parse_diagram()
    
    def _parse_diagram(self):
        """Parse all shapes and edges from the BPMN diagram."""
        # Find BPMNDiagram element
        diagram = self.root.find('.//bpmndi:BPMNDiagram', NAMESPACES)
        if diagram is None:
            raise ValueError("No BPMNDiagram found in file")
        
        plane = diagram.find('bpmndi:BPMNPlane', NAMESPACES)
        if plane is None:
            raise ValueError("No BPMNPlane found in diagram")
        
        # Parse shapes
        for shape in plane.findall('bpmndi:BPMNShape', NAMESPACES):
            bounds = shape.find('dc:Bounds', NAMESPACES)
            if bounds is not None:
                shape_obj = BPMNShape(
                    id=shape.get('id'),
                    element_id=shape.get('bpmnElement'),
                    x=float(bounds.get('x')),
                    y=float(bounds.get('y')),
                    width=float(bounds.get('width')),
                    height=float(bounds.get('height')),
                    element=shape
                )
                self.shapes[shape_obj.element_id] = shape_obj
        
        # Parse edges
        for edge in plane.findall('bpmndi:BPMNEdge', NAMESPACES):
            waypoints = []
            for wp in edge.findall('di:waypoint', NAMESPACES):
                waypoints.append((float(wp.get('x')), float(wp.get('y'))))
            
            edge_obj = BPMNEdge(
                id=edge.get('id'),
                element_id=edge.get('bpmnElement'),
                waypoints=waypoints,
                element=edge
            )
            self.edges[edge_obj.element_id] = edge_obj
    
    def analyze(self) -> Dict:
        """Analyze the diagram and report alignment issues."""
        issues = {
            'overlapping_shapes': [],
            'misaligned_rows': [],
            'misaligned_columns': [],
            'crossing_edges': [],
            'tight_spacing': [],
        }
        
        shapes_list = list(self.shapes.values())
        
        # Check for overlapping shapes
        for i, s1 in enumerate(shapes_list):
            for s2 in shapes_list[i+1:]:
                if self._shapes_overlap(s1, s2):
                    issues['overlapping_shapes'].append((s1.element_id, s2.element_id))
        
        # Find rows and check alignment
        rows = self._find_rows()
        for row_y, elements in rows.items():
            if len(elements) > 1:
                y_values = [self.shapes[eid].y for eid in elements]
                if max(y_values) - min(y_values) > 10:
                    issues['misaligned_rows'].append({
                        'approximate_y': row_y,
                        'elements': elements,
                        'y_variance': max(y_values) - min(y_values)
                    })
        
        # Check for tight spacing
        for i, s1 in enumerate(shapes_list):
            for s2 in shapes_list[i+1:]:
                dist = self._horizontal_distance(s1, s2)
                if 0 < dist < self.MIN_SPACING:
                    issues['tight_spacing'].append({
                        'elements': (s1.element_id, s2.element_id),
                        'distance': dist
                    })
        
        return issues
    
    def _shapes_overlap(self, s1: BPMNShape, s2: BPMNShape) -> bool:
        """Check if two shapes overlap."""
        return not (s1.right < s2.x or s2.right < s1.x or 
                   s1.bottom < s2.y or s2.bottom < s1.y)
    
    def _horizontal_distance(self, s1: BPMNShape, s2: BPMNShape) -> float:
        """Calculate horizontal distance between two shapes."""
        if s1.right < s2.x:
            return s2.x - s1.right
        elif s2.right < s1.x:
            return s1.x - s2.right
        return 0  # Overlapping
    
    def _find_rows(self) -> Dict[int, List[str]]:
        """Group elements into approximate rows based on y-coordinate."""
        rows = defaultdict(list)
        for shape in self.shapes.values():
            # Round y to nearest HORIZONTAL_TOLERANCE to group nearby elements
            row_key = round(shape.center_y / self.HORIZONTAL_TOLERANCE) * self.HORIZONTAL_TOLERANCE
            rows[row_key].append(shape.element_id)
        return dict(rows)
    
    def _find_columns(self) -> Dict[int, List[str]]:
        """Group elements into approximate columns based on x-coordinate."""
        columns = defaultdict(list)
        for shape in self.shapes.values():
            col_key = round(shape.center_x / self.VERTICAL_TOLERANCE) * self.VERTICAL_TOLERANCE
            columns[col_key].append(shape.element_id)
        return dict(columns)
    
    def align_row(self, element_ids: List[str], target_y: Optional[float] = None):
        """Align multiple elements to the same y-coordinate (horizontal row)."""
        if not element_ids:
            return
        
        shapes = [self.shapes[eid] for eid in element_ids if eid in self.shapes]
        if not shapes:
            return
        
        # Use average y if no target specified
        if target_y is None:
            target_y = sum(s.y for s in shapes) / len(shapes)
        
        for shape in shapes:
            self._update_shape_position(shape, shape.x, target_y)
    
    def align_column(self, element_ids: List[str], target_x: Optional[float] = None):
        """Align multiple elements to the same x-coordinate (vertical column)."""
        if not element_ids:
            return
        
        shapes = [self.shapes[eid] for eid in element_ids if eid in self.shapes]
        if not shapes:
            return
        
        # Use average x if no target specified
        if target_x is None:
            target_x = sum(s.x for s in shapes) / len(shapes)
        
        for shape in shapes:
            self._update_shape_position(shape, target_x, shape.y)
    
    def distribute_horizontally(self, element_ids: List[str], spacing: Optional[float] = None):
        """Distribute elements evenly along x-axis."""
        if len(element_ids) < 2:
            return
        
        shapes = [self.shapes[eid] for eid in element_ids if eid in self.shapes]
        if len(shapes) < 2:
            return
        
        # Sort by current x position
        shapes.sort(key=lambda s: s.x)
        
        if spacing is None:
            spacing = self.PREFERRED_SPACING
        
        # Keep first element fixed, distribute rest
        start_x = shapes[0].right + spacing
        for shape in shapes[1:]:
            self._update_shape_position(shape, start_x, shape.y)
            start_x = shape.right + spacing
    
    def distribute_vertically(self, element_ids: List[str], spacing: Optional[float] = None):
        """Distribute elements evenly along y-axis."""
        if len(element_ids) < 2:
            return
        
        shapes = [self.shapes[eid] for eid in element_ids if eid in self.shapes]
        if len(shapes) < 2:
            return
        
        # Sort by current y position
        shapes.sort(key=lambda s: s.y)
        
        if spacing is None:
            spacing = self.PREFERRED_SPACING
        
        # Keep first element fixed, distribute rest
        start_y = shapes[0].bottom + spacing
        for shape in shapes[1:]:
            self._update_shape_position(shape, shape.x, start_y)
            start_y = shape.bottom + spacing
    
    def _update_shape_position(self, shape: BPMNShape, new_x: float, new_y: float):
        """Update shape position in the XML tree."""
        bounds = shape.element.find('dc:Bounds', NAMESPACES)
        if bounds is not None:
            old_x, old_y = shape.x, shape.y
            bounds.set('x', str(int(new_x)))
            bounds.set('y', str(int(new_y)))
            shape.x = new_x
            shape.y = new_y
            
            # Update connected edges
            self._update_connected_edges(shape.element_id, old_x, old_y, new_x, new_y)
    
    def _update_connected_edges(self, element_id: str, old_x: float, old_y: float, 
                                 new_x: float, new_y: float):
        """Update waypoints of edges connected to a moved shape."""
        shape = self.shapes.get(element_id)
        if not shape:
            return
        
        dx = new_x - old_x
        dy = new_y - old_y
        
        # Find edges connected to this element
        for edge in self.edges.values():
            waypoints = edge.element.findall('di:waypoint', NAMESPACES)
            if not waypoints:
                continue
            
            # Check if first or last waypoint is near the old shape position
            first_wp = waypoints[0]
            last_wp = waypoints[-1]
            
            # Update first waypoint if it was connected to this shape
            fx, fy = float(first_wp.get('x')), float(first_wp.get('y'))
            if self._point_near_shape(fx, fy, old_x, old_y, shape.width, shape.height):
                first_wp.set('x', str(int(fx + dx)))
                first_wp.set('y', str(int(fy + dy)))
            
            # Update last waypoint if it was connected to this shape
            lx, ly = float(last_wp.get('x')), float(last_wp.get('y'))
            if self._point_near_shape(lx, ly, old_x, old_y, shape.width, shape.height):
                last_wp.set('x', str(int(lx + dx)))
                last_wp.set('y', str(int(ly + dy)))
    
    def _point_near_shape(self, px: float, py: float, sx: float, sy: float, 
                          sw: float, sh: float, tolerance: float = 20) -> bool:
        """Check if a point is near a shape boundary."""
        return (sx - tolerance <= px <= sx + sw + tolerance and
                sy - tolerance <= py <= sy + sh + tolerance)
    
    def auto_align_rows(self):
        """Automatically align all detected rows."""
        rows = self._find_rows()
        for row_y, element_ids in rows.items():
            if len(element_ids) > 1:
                self.align_row(element_ids, target_y=row_y)
    
    def auto_align_columns(self):
        """Automatically align all detected columns."""
        columns = self._find_columns()
        for col_x, element_ids in columns.items():
            if len(element_ids) > 1:
                self.align_column(element_ids, target_x=col_x)
    
    def auto_fix_all(self):
        """Apply all automatic fixes."""
        print("  → Auto-aligning rows...")
        self.auto_align_rows()
        print("  → Auto-aligning columns...")
        self.auto_align_columns()
    
    def save(self, output_path: str):
        """Save the modified BPMN to a file."""
        self.tree.write(output_path, encoding='utf-8', xml_declaration=True)
        # Fix namespace declarations (ElementTree doesn't handle this well)
        self._fix_namespaces(output_path)
    
    def _fix_namespaces(self, path: str):
        """Fix namespace declarations in the output file."""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ensure proper namespace prefixes
        content = content.replace('ns0:', 'bpmn:').replace('ns1:', 'bpmndi:')
        content = content.replace('ns2:', 'dc:').replace('ns3:', 'di:')
        content = content.replace(':ns0=', ':bpmn=').replace(':ns1=', ':bpmndi=')
        content = content.replace(':ns2=', ':dc=').replace(':ns3=', ':di=')
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)


def main():
    parser = argparse.ArgumentParser(
        description='BPMN Alignment Tool - Fix overlapping flows and align elements'
    )
    parser.add_argument('input', help='Input BPMN file')
    parser.add_argument('output', nargs='?', help='Output BPMN file (default: <input>_aligned.bpmn)')
    parser.add_argument('--analyze', action='store_true', help='Only analyze, do not modify')
    parser.add_argument('--align-rows', action='store_true', help='Align elements in rows')
    parser.add_argument('--align-columns', action='store_true', help='Align elements in columns')
    parser.add_argument('--auto', action='store_true', help='Apply all automatic fixes')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"❌ Error: File not found: {args.input}")
        sys.exit(1)
    
    print("\n📐 BPMN Alignment Tool (Python)")
    print("─" * 50)
    print(f"📄 Input: {args.input}")
    
    try:
        aligner = BPMNAligner(args.input)
        print(f"   Loaded {len(aligner.shapes)} shapes, {len(aligner.edges)} edges")
        
        if args.analyze:
            print("\n🔍 Analyzing diagram...")
            issues = aligner.analyze()
            
            print(f"\n📊 Analysis Results:")
            print(f"   • Overlapping shapes: {len(issues['overlapping_shapes'])}")
            print(f"   • Misaligned rows: {len(issues['misaligned_rows'])}")
            print(f"   • Tight spacing issues: {len(issues['tight_spacing'])}")
            
            if issues['misaligned_rows']:
                print("\n   Misaligned rows:")
                for row in issues['misaligned_rows'][:5]:
                    print(f"     - y≈{row['approximate_y']}: {len(row['elements'])} elements, variance={row['y_variance']:.0f}px")
            
            return
        
        # Apply fixes
        output = args.output or args.input.replace('.bpmn', '_aligned.bpmn')
        print(f"📄 Output: {output}")
        print("\n⏳ Applying alignment fixes...")
        
        if args.auto or (not args.align_rows and not args.align_columns):
            aligner.auto_fix_all()
        else:
            if args.align_rows:
                aligner.auto_align_rows()
            if args.align_columns:
                aligner.auto_align_columns()
        
        aligner.save(output)
        print(f"\n✅ Alignment complete!")
        print(f"💡 Open {output} in Camunda Modeler to view the result.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
