"""
Modul för att hantera kommandon i Nova chatbot.
"""

import datetime
import random
import json
import os
import re


class CommandHandler:
    """
    Hanterar kommandon som användaren kan ge till Nova.
    """
    
    def __init__(self, chatbot_name="NOVA"):
        """
        Initierar CommandHandler.
        
        Args:
            chatbot_name (str): Namn på chatboten, används för formatering av svar
        """
        self.chatbot_name = chatbot_name
        self.commands = {}
        self.load_commands()
        
        # Dictionary med kommandofunktioner
        self.command_functions = {
            "show_time": self.get_time,
            "show_date": self.get_date,
            "roll_dice": self.roll_dice,
            "show_help": self.get_help,
            "random_number": self.random_number,
            "exit_app": self.exit_command,
            "activate_voice": self.activate_voice,
            "deactivate_voice": self.deactivate_voice,
            "clear_chat": self.clear_chat
        }
    
    def load_commands(self):
        """
        Läser in kommandon från commands.json.
        """
        try:
            # Hitta den korrekta sökvägen till commands.json
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(script_dir, 'data', 'commands.json')
            
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.commands = data.get("commands", {})
                print(f"Laddade {len(self.commands)} kommandon från commands.json")
        except Exception as e:
            print(f"Kunde inte ladda kommandon från fil: {e}")
            self.commands = {}
    
    def handle_command(self, command_text):
        """
        Hanterar ett kommando och returnerar ett lämpligt svar.
        
        Args:
            command_text (str): Kommandot som ska hanteras
            
        Returns:
            str eller dict: Svaret på kommandot, kan vara text eller ett dictionary med action-info
        """
        # För bakåtkompatibilitet - anropa check_command och formatera svaret
        action, response, extra_data = self.check_command(command_text)
        
        if action:
            # Konvertera det nya formatet till det gamla för bakåtkompatibilitet
            
            # Om det är ett specialkommando som kräver ytterligare hantering
            if action in ["open_website", "open_application"]:
                return {
                    "action": action,
                    "text": response,
                    "extra_data": extra_data
                }
            
            # För exit-kommando, behåll textsvar för bakåtkompatibilitet
            if action == "exit_app":
                return response
            
            # För övriga kommandon, returnera bara texten
            return response
        
        return None
    
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
        text = text.lower().strip()
        
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
        
        # Gå igenom alla kommandon från JSON-filen
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
                        
                    # Anropa motsvarande funktion om den finns
                    if action in self.command_functions:
                        action_response = self.command_functions[action]()
                        if action_response:
                            return action, action_response, None
                    
                    # Om detta är exit-kommandot, skriv ut en extra notering
                    if action == "exit_app":
                        print("Exit-kommando identifierat - programmet kommer att avslutas")
                    
                    return action, response, None
        
        # Om inget matchade från JSON, kontrollera de gamla hårdkodade kommandona
        cmd_mapping = {
            "tid": ("show_time", self.get_time()),
            "datum": ("show_date", self.get_date()),
            "tärning": ("roll_dice", self.roll_dice()),
            "hjälp": ("show_help", self.get_help()),
            "slumpa tal": ("random_number", self.random_number()),
            "avsluta": ("exit_app", self.exit_command()),
            "rensa chatten": ("clear_chat", self.clear_chat()),
            "aktivera röst": ("activate_voice", self.activate_voice()),
            "avaktivera röst": ("deactivate_voice", self.deactivate_voice())
        }
        
        for cmd_keyword, (action, response) in cmd_mapping.items():
            if cmd_keyword in text:
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
    
    def get_time(self):
        """Returnerar aktuell tid."""
        current_time = datetime.datetime.now().strftime("%H:%M")
        return f"Klockan är {current_time}."
    
    def get_date(self):
        """Returnerar aktuellt datum."""
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        return f"Dagens datum är {current_date}."
    
    def roll_dice(self):
        """Simulerar ett tärningskast."""
        number = random.randint(1, 6)
        return f"Jag slog en tärning och fick: {number}"
    
    def random_number(self):
        """Genererar ett slumpmässigt tal mellan 1 och 100."""
        number = random.randint(1, 100)
        return f"Här är ett slumpmässigt tal: {number}"
    
    def get_help(self):
        """Returnerar hjälpinformation."""
        help_text = (
            "Här är några kommandon du kan använda:\n"
            "- 'tid' för att se aktuell tid\n"
            "- 'datum' för att se dagens datum\n"
            "- 'tärning' för att slå en tärning\n"
            "- 'slumpa tal' för att få ett slumpmässigt tal\n"
            "- 'öppna [webbsida]' för att öppna en webbplats\n"
            "- 'öppna [app]' för att starta en applikation\n"
            "- 'rensa chatten' för att rensa chathistoriken\n"
            "- 'aktivera röst'/'avaktivera röst' för att hantera röstläge\n"
            "- 'avsluta' för att avsluta programmet"
        )
        return help_text
    
    def exit_command(self):
        """Kommando för att avsluta chatboten."""
        return "Avslutar programmet. Hej då!"
    
    def activate_voice(self):
        """Aktiverar röststyrning."""
        return "Röststyrning aktiverad."
    
    def deactivate_voice(self):
        """Deaktiverar röststyrning."""
        return "Röststyrning deaktiverad."
    
    def clear_chat(self):
        """Rensar chatten."""
        return "Chatten har rensats."