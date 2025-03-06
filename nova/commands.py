"""
Modul för att hantera specifika kommandon i Nova chatbot.
"""

import datetime
import random

class CommandHandler:
    """
    Hanterar kommandon som användaren kan ge till Nova.
    """
    
    def __init__(self):
        """
        Initierar CommandHandler.
        """
        # Dictionary med kommandofunktioner
        self.commands = {
            "tid": self.get_time,
            "datum": self.get_date,
            "tärning": self.roll_dice,
            "hjälp": self.get_help,
            "slumpa tal": self.random_number,
            "avsluta": self.exit_command
        }
    
    def handle_command(self, command):
        """
        Hanterar ett kommando och returnerar ett lämpligt svar.
        
        Args:
            command (str): Kommandot som ska hanteras
            
        Returns:
            str: Svaret på kommandot eller None om kommandot inte känns igen
        """
        command = command.lower().strip()
        
        # Kontrollera om kommandot finns i vår dictionary
        for cmd_keyword, cmd_function in self.commands.items():
            if cmd_keyword in command:
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