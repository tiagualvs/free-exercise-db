#!/usr/bin/env python3
"""Generate summary of translated exercises."""

import json

with open("dist/exercises-pt.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== RESUMO DA TRADUÇÃO ===")
print(f"Total de exercícios traduzidos: {len(data)}")

print(f"\nCategorias encontradas:")
cats = set(ex['category'] for ex in data if ex.get('category'))
for cat in sorted(cats):
    print(f'  - {cat}')

print(f"\nNíveis encontrados:")
levels = set(ex['level'] for ex in data if ex.get('level'))
for level in sorted(levels):
    print(f'  - {level}')

print(f"\nEquipamentos encontrados:")
equip = set(ex['equipment'] for ex in data if ex.get('equipment'))
for e in sorted(equip):
    print(f'  - {e}')

print(f"\nPrimeiros 5 exercícios:")
for i, ex in enumerate(data[:5], 1):
    print(f"{i}. {ex['name']} ({ex['category']}) - {ex['level']}")

print(f"\nÚltimos 5 exercícios:")
for i, ex in enumerate(data[-5:], len(data)-4):
    print(f"{i}. {ex['name']} ({ex['category']}) - {ex['level']}")

print(f"\nEstrutura do JSON (chaves):")
print(f"  {list(data[0].keys())}")
