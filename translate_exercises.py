#!/usr/bin/env python3
"""
Script to translate exercises.json from English to Brazilian Portuguese (pt-BR)
Uses Google Translate via deep-translator for quality translations.
Saves progress incrementally to avoid losing data.
"""

import json
import time
import os
from deep_translator import GoogleTranslator

# Field name mappings
FIELD_MAPPINGS = {
    "name": "nome",
    "force": "forca",
    "level": "nivel",
    "mechanic": "mecanica",
    "equipment": "equipamento",
    "primaryMuscles": "musculosPrimarios",
    "secondaryMuscles": "musculosSecundarios",
    "instructions": "instrucoes",
    "category": "categoria",
    "images": "imagens",
    "id": "id",
}

# Initialize translator
translator = GoogleTranslator(source='en', target='pt')

# Cache for translations to avoid repeated API calls
translation_cache = {}
cache_file = "translation_cache.json"

# Load existing cache if exists
if os.path.exists(cache_file):
    with open(cache_file, "r", encoding="utf-8") as f:
        translation_cache = json.load(f)
    print(f"Cache carregado com {len(translation_cache)} entradas.")


def save_cache():
    """Save translation cache to file."""
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(translation_cache, f, ensure_ascii=False, indent=2)


def translate_text(text):
    """Translate text from English to pt with caching."""
    if not text or not isinstance(text, str):
        return text
    
    if text in translation_cache:
        return translation_cache[text]
    
    try:
        translated = translator.translate(text)
        translation_cache[text] = translated
        return translated
    except Exception as e:
        print(f"Erro na tradução: {e}")
        return text


def translate_exercise(exercise):
    """Translate a complete exercise object to pt-BR."""
    translated = {}
    
    # Map field names
    for eng_key, pt_key in FIELD_MAPPINGS.items():
        value = exercise.get(eng_key)
        
        # Keep images and id as-is
        if eng_key in ["images", "id"]:
            translated[pt_key] = value
            continue
        
        # Translate strings
        if isinstance(value, str):
            translated[pt_key] = translate_text(value)
        # Translate lists of strings (muscles, instructions)
        elif isinstance(value, list):
            if eng_key == "instructions":
                # Translate each instruction
                translated[pt_key] = [translate_text(inst) for inst in value]
            else:
                # Translate muscle names
                translated[pt_key] = [translate_text(muscle) for muscle in value]
        elif value is None:
            translated[pt_key] = None
    
    return translated


def save_progress(translated_exercises, filename="dist/exercises-pt.json"):
    """Save current progress to file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(translated_exercises, f, ensure_ascii=False, indent=2)


def main():
    """Main translation function."""
    print("Lendo arquivo exercises.json...")
    
    with open("dist/exercises.json", "r", encoding="utf-8") as f:
        exercises = json.load(f)
    
    print(f"Encontrados {len(exercises)} exercícios para traduzir...")
    print("Iniciando tradução com Google Translate...")
    
    translated_exercises = []
    start_time = time.time()
    
    for i, exercise in enumerate(exercises, 1):
        translated_exercises.append(translate_exercise(exercise))
        
        # Print progress and save every 10 exercises
        if i % 10 == 0:
            elapsed = time.time() - start_time
            rate = i / elapsed if elapsed > 0 else 0
            remaining = (len(exercises) - i) / rate if rate > 0 else 0
            
            print(f"Progresso: {i}/{len(exercises)} ({i*100//len(exercises)}%) - "
                  f"Tempo decorrido: {elapsed:.0f}s - "
                  f"Tempo restante estimado: {remaining:.0f}s")
            
            # Save progress
            save_progress(translated_exercises)
            save_cache()
        
        # Small delay to avoid rate limiting
        if i % 3 == 0:
            time.sleep(0.2)
    
    # Final save
    output_file = "dist/exercises-pt.json"
    print(f"\nSalvando tradução final em {output_file}...")
    
    save_progress(translated_exercises)
    save_cache()
    
    total_time = time.time() - start_time
    print(f"Tradução concluída! {len(translated_exercises)} exercícios traduzidos.")
    print(f"Tempo total: {total_time:.0f} segundos ({total_time/60:.1f} minutos)")
    print(f"Arquivo salvo: {output_file}")


if __name__ == "__main__":
    main()
