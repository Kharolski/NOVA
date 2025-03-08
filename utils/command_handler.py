"""
Modul för hantering av röstkommandon baserade på commands.json.
"""

import json
import os
import datetime
import re

class CommandHandler:
    """
    Klass för att hantera systemkommandon från commands.json.
    """
    
    def __init__(self, chatbot_name="Nova"):
        """
        Initierar en CommandHandler och läser in commands.json.
        
        Args:
            chatbot_name (str): Namn på chatboten, används för formatering av svar
        """
        self.chatbot_name = chatbot_name
        self.commands = {}
        self.load_commands()
        
    def load_commands(self):
        """
        Läser in kommandon från commands.json.
        """
        try:
            # Hämta sökvägen till commands.json
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            commands_path = os.path.join(script_dir, "data", "commands.json")
            
            # Läs in JSON-filen
            with open(commands_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            # Spara kommandona
            self.commands = data.get("commands", {})
            print(f"Laddade {len(self.commands)} kommandon från commands.json")
        except Exception as e:
            print(f"Fel vid inläsning av commands.json: {e}")
            self.commands = {}
            
    def check_command(self, text):
        """
        Kontrollerar om texten matchar något kommando.
        
        Args:
            text (str): Texten att kontrollera
        
        Returns:
            tuple: (kommando-typ, svar, extra_data) om en matchning hittades, 
                annars (None, None, None)
        """
        if not text:
            return None, None, None
            
        # Konvertera till lower case för enklare jämförelse
        text = text.lower()
        
        print(f"Söker efter kommando i texten: '{text}'")
        
        # Kontrollera om detta är ett webbplatskommando
        if any(phrase in text for phrase in self.commands.get('open_website', {}).get('phrases', [])):
            website = self.extract_website(text)
            if website:
                response = self.commands['open_website']['response'].replace("{website}", website)
                response = response.replace("{name}", self.chatbot_name)
                return "open_website", response, {"website": website}
        
        # Kontrollera om detta är ett applikationskommando
        if any(phrase in text for phrase in self.commands.get('open_application', {}).get('phrases', [])):
            app_name = self.extract_application(text)
            if app_name:
                response = self.commands['open_application']['response'].replace("{app}", app_name)
                response = response.replace("{name}", self.chatbot_name)
                return "open_application", response, {"app_name": app_name}
        
        # Gå igenom alla kommandon
        for command_type, command_data in self.commands.items():
            # Kontrollera om texten matchar någon av fraserna
            for phrase in command_data.get("phrases", []):
                if phrase.lower() in text:
                    # Formatera svaret
                    response = command_data.get("response", "")
                    action = command_data.get("action", "")
                    
                    # Ersätt {name} med chatbotens namn
                    response = response.replace("{name}", self.chatbot_name)
                    
                    # Specialhantering för tidskommando
                    if "{time}" in response:
                        current_time = datetime.datetime.now().strftime("%H:%M")
                        response = response.replace("{time}", current_time)
                    
                    # Om detta är exit-kommandot, skriv ut en extra notering
                    if action == "exit_app":
                        print("Exit-kommando identifierat - programmet kommer att avslutas")
                    
                    return action, response, None
        
        # Inget kommando matchade
        print("  Inget kommando matchade")
        return None, None, None
    
    def extract_website(self, text):
        """
        Extraherar webbadress från användarens text.
        
        Args:
            text (str): Användarens text
        
        Returns:
            str: Extraherad webbadress eller None
        """
        # Leta efter ord efter "gå till", "öppna sidan", etc.
        patterns = [
            r'(?:gå till|öppna sidan|besök hemsidan|öppna webbplatsen) ([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            r'(?:gå till|öppna sidan|besök hemsidan|öppna webbplatsen) ([a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/\S*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1)
        
        return None

    def extract_application(self, text):
        """
        Extraherar applikationsnamn från användarens text.
        
        Args:
            text (str): Användarens text
        
        Returns:
            str: Extraherad applikation eller None
        """
        patterns = [
            r'(?:öppna|starta) ([a-zåäöA-ZÅÄÖ]+)',
            r'(?:starta|kör) ([a-zåäöA-ZÅÄÖ]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1)
        
        return None