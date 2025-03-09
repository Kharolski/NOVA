"""
Hjälpfunktioner för Nova chatbot.
Innehåller allmännyttiga funktioner som används på flera ställen i applikationen.
"""

import os
import json
import datetime
import re
import unicodedata
import random
import logging
from typing import Dict, List, Any, Optional, Union

# Konfigurera loggning
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'nova.log'), encoding='utf-8')
    ]
)

def get_logger(name: str) -> logging.Logger:
    """
    Skapar en loggare med det givna namnet.
    
    Args:
        name: Namnet på loggaren
        
    Returns:
        En konfigurerad logger-instans
    """
    return logging.getLogger(name)

# Logger för denna modul
logger = get_logger(__name__)

def load_json_file(file_path: str) -> Dict:
    """
    Laddar ett JSON-dokument från en fil.
    
    Args:
        file_path: Sökvägen till JSON-filen
        
    Returns:
        Innehållet i JSON-filen som ett dictionary
        
    Raises:
        FileNotFoundError: Om filen inte hittas
        json.JSONDecodeError: Om filen inte innehåller giltig JSON
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"Filen '{file_path}' kunde inte hittas.")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Filen '{file_path}' innehåller ogiltig JSON: {e}")
        raise

def save_json_file(file_path: str, data: Dict) -> bool:
    """
    Sparar data till en JSON-fil.
    
    Args:
        file_path: Sökvägen till JSON-filen
        data: Data att spara
        
    Returns:
        True om sparandet lyckades, annars False
    """
    try:
        # Skapa mappen om den inte finns
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"Kunde inte spara data till '{file_path}': {e}")
        return False

def get_current_time() -> str:
    """
    Returnerar den aktuella tiden i formatet 'HH:MM'.
    
    Returns:
        Aktuell tid som sträng
    """
    return datetime.datetime.now().strftime('%H:%M')

def get_current_date() -> str:
    """
    Returnerar det aktuella datumet i formatet 'YYYY-MM-DD'.
    
    Returns:
        Aktuellt datum som sträng
    """
    return datetime.datetime.now().strftime('%Y-%m-%d')

def get_formatted_datetime() -> str:
    """
    Returnerar aktuellt datum och tid i formatet 'YYYY-MM-DD HH:MM:SS'.
    
    Returns:
        Aktuellt datum och tid som sträng
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def normalize_text(text: str) -> str:
    """
    Normaliserar text genom att:
    1. Konvertera till gemener
    2. Ta bort accenttecken
    3. Ta bort specialtecken
    4. Ta bort överflödiga mellanslag
    
    Args:
        text: Texten som ska normaliseras
        
    Returns:
        Normaliserad text
    """
    if not text:
        return ""
        
    # Konvertera till gemener
    text = text.lower()
    
    # Ta bort accenttecken (t.ex. 'é' -> 'e')
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    
    # Ta bort specialtecken, behåll bokstäver, siffror och mellanslag
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    
    # Ta bort överflödiga mellanslag
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def select_random_response(responses: List[str]) -> str:
    """
    Väljer ett slumpmässigt svar från en lista.
    
    Args:
        responses: Lista med möjliga svar
        
    Returns:
        Ett slumpmässigt valt svar
    """
    if not responses:
        return ""
    
    return random.choice(responses)

def ensure_directory_exists(directory_path: str) -> bool:
    """
    Ser till att en mapp existerar, skapar den om den inte finns.
    
    Args:
        directory_path: Sökvägen till mappen
        
    Returns:
        True om mappen existerar eller skapades, annars False
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Kunde inte skapa mappen '{directory_path}': {e}")
        return False

def get_project_root() -> str:
    """
    Returnerar projektets rotmapp.
    
    Returns:
        Sökvägen till projektets rotmapp
    """
    # Detta antar att helpers.py är i utils/ under projektets rot
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def find_files_with_extension(directory: str, extension: str) -> List[str]:
    """
    Hittar alla filer med den angivna filändelsen i en mapp.
    
    Args:
        directory: Mappen att söka i
        extension: Filändelsen (t.ex. '.json')
        
    Returns:
        Lista med sökvägar till matchande filer
    """
    matching_files = []
    
    try:
        for file in os.listdir(directory):
            if file.endswith(extension):
                matching_files.append(os.path.join(directory, file))
    except Exception as e:
        logger.error(f"Fel vid sökning efter filer i '{directory}': {e}")
    
    return matching_files