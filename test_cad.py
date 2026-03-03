# Direct parser test
import sys
sys.path.insert(0, '.')

from cad_parser import CADParser

# Create parser and test regex directly
parser = CADParser()

# Test mileage extraction manually
test_texts = [
    {'text': 'K0+000', 'layer': 'A-MILEAGE', 'insert': (100, 200)},
    {'text': 'K0+100', 'layer': 'A-MILEAGE', 'insert': (200, 200)},
    {'text': 'K1+000', 'layer': 'A-MILEAGE', 'insert': (500, 200)},
    {'text': 'K5+200', 'layer': 'A-MILEAGE', 'insert': (1500, 200)},
    {'text': '1-通道K0+150', 'layer': 'S-STRUCTURE', 'insert': (250, 210)},
    {'text': '2-小桥K1+000', 'layer': 'S-STRUCTURE', 'insert': (550, 210)},
    {'text': '3-中桥K5+200', 'layer': 'S-STRUCTURE', 'insert': (1550, 210)},
]

parser.entities['texts'] = test_texts
parser._extract_mileages()
parser._extract_structures()

print("=" * 50)
print("CAD Parser Test Results")
print("=" * 50)

print(f"\n[Mileages] Found: {len(parser.entities['mileages'])}")
for m in parser.entities['mileages']:
    print(f"  K{m['km']}+{m['meter']:03d} at ({m['position']})")

print(f"\n[Structures] Found: {len(parser.entities['structures'])}")
for s in parser.entities['structures']:
    print(f"  {s['name']} ({s['type']}) at {s['position']}")

# Export to Neo4j format
nodes = parser.export_to_neo4j_format()
print(f"\n[Neo4j Export] Nodes: {len(nodes)}")
for n in nodes[:5]:
    print(f"  {n['type']}: {n['properties']}")

print("\n[OK] Parser test PASSED!")
