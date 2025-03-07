"""
Modul för hantering av röstkommandon baserade på commands.json.
"""

import json
import os
import datetime

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
            tuple: (kommando-typ, svar) om en matchning hittades, annars (None, None)
        """
        if not text:
            return None, None
            
        # Konvertera till lower case för enklare jämförelse
        text = text.lower()
        
        print(f"Söker efter kommando i texten: '{text}'")
        
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
                    
                    return action, response
        
        # Inget kommando matchade
        print("  Inget kommando matchade")
        return None, None