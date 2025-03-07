"""
Modul för att hantera specifika kommandon i Nova chatbot.
"""

import datetime
import random
import json
import os

class CommandHandler:
    """
    Hanterar kommandon som användaren kan ge till Nova.
    """
    
    def __init__(self, chatbot_name="NOVA"):
        """
        Initierar CommandHandler.
        """
        self.chatbot_name = chatbot_name
        # Ladda kommandon från JSON-fil
        self.commands_json = self._load_commands()
        
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
    
    def _load_commands(self):
        """
        Laddar kommandon från commands.json-filen.
        
        Returns:
            dict: Ett lexikon med kommandon
        """
        try:
            # Hitta den korrekta sökvägen till commands.json
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(script_dir, 'data', 'commands.json')
            
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get("commands", {})
        except Exception as e:
            print(f"Kunde inte ladda kommandon från fil: {e}")
            # Returnera tom dict om filen inte kunde laddas
            return {}
    
    def handle_command(self, command_text):
        """
        Hanterar ett kommando och returnerar ett lämpligt svar.
        
        Args:
            command_text (str): Kommandot som ska hanteras
            
        Returns:
            str: Svaret på kommandot eller None om kommandot inte känns igen
        """
        command_text = command_text.lower().strip()
        
        # Försök att matcha mot kommandon från JSON-filen först
        for command_key, command_data in self.commands_json.items():
            phrases = command_data.get("phrases", [])
            for phrase in phrases:
                if phrase in command_text:
                    action = command_data.get("action", "")
                    response = command_data.get("response", "")
                    
                    # Ersätt eventuella variabler i svaret
                    response = response.replace("{name}", self.chatbot_name)
                    if "{time}" in response:
                        current_time = datetime.datetime.now().strftime("%H:%M")
                        response = response.replace("{time}", current_time)
                    
                    # Anropa motsvarande funktion om den finns
                    if action in self.command_functions:
                        action_response = self.command_functions[action]()
                        if action_response:
                            return action_response
                    
                    return response
        
        # Om inget matchade från JSON, kontrollera de gamla hårdkodade kommandona
        for cmd_keyword, cmd_function in {
            "tid": self.get_time,
            "datum": self.get_date,
            "tärning": self.roll_dice,
            "hjälp": self.get_help,
            "slumpa tal": self.random_number,
            "avsluta": self.exit_command
        }.items():
            if cmd_keyword in command_text:
                return cmd_function()
        
        # Om vi inte känner igen kommandot
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
            "- 'sök på [ämne]' för att söka information\n"
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