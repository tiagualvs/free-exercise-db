#!/usr/bin/env python3
"""
Post-processing script to fix specific translation issues in exercises-pt.json
"""

import json

# Common translation fixes for fitness terminology
TRANSLATION_FIXES = {
    "bezerros": "panturrilhas",
    "corpo apenas": "somente o corpo",
    "força": "força",
    "novato": "iniciante",
}

def fix_translations(data):
    """Fix common translation errors in the translated data."""
    fixed_count = 0
    
    for exercise in data:
        for key, value in exercise.items():
            if isinstance(value, str):
                for wrong, correct in TRANSLATION_FIXES.items():
                    if value.lower() == wrong.lower():
                        exercise[key] = correct
                        fixed_count += 1
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, str):
                        for wrong, correct in TRANSLATION_FIXES.items():
                            if item.lower() == wrong.lower():
                                value[i] = correct
                                fixed_count += 1
    
    return data, fixed_count

def main():
    print("Lendo arquivo exercises-pt.json...")
    
    with open("dist/exercises-pt.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"Corrigindo traduções...")
    fixed_data, fixed_count = fix_translations(data)
    
    output_file = "dist/exercises-pt.json"
    print(f"Salvando correções em {output_file}...")
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(fixed_data, f, ensure_ascii=False, indent=2)
    
    print(f"Correções aplicadas: {fixed_count}")
    print(f"Arquivo final salvo: {output_file}")

if __name__ == "__main__":
    main()
