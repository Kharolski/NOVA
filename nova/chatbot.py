import json
import os
import random
from nova.commands import CommandHandler
from nova.search import WebSearch

class Nova:
    """
    Nova är en enkel chatbot som kan svara på grundläggande frågor
    och utföra enkla kommandon.
    """
    
    def __init__(self):
        """
        Initierar Nova chatbot.
        """
        self.name = "NOVA"
        self.responses = self._load_responses()
        self.command_handler = CommandHandler()
        self.web_search = WebSearch()
        self.exit_requested = False
    
    def _load_responses(self):
        """
        Laddar fördefinierade svar från JSON-filen.
        
        Returns:
            dict: Ett lexikon med svarsmönster
        """
        try:
            # Hitta den korrekta sökvägen till responses.json
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(script_dir, 'data', 'responses.json')
            
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Kunde inte ladda svar från fil: {e}")
            # Returnera ett enkelt standardsvar om filen inte kunde laddas
            return {
                "greetings": {"hej": "Hej!"},
                "fallback": ["Jag förstår inte."]
            }
    
    def get_response(self, user_input):
        """
        Genererar ett svar baserat på användarens input.
        
        Args:
            user_input (str): Användarens meddelande
            
        Returns:
            str: Novas svar
        """
        # Konvertera input till gemener för bättre matchning
        user_input = user_input.lower().strip()
        
        # Först, kontrollera om input är ett kommando
        command_response = self.command_handler.handle_command(user_input)
        if command_response:
            # Om kommandot är för att avsluta, markera detta
            if "avslutar programmet" in command_response.lower():
                self.exit_requested = True
            return command_response
        
        # Kontrollera om användaren ber om en webbsökning
        if user_input.startswith("sök på "):
            query = user_input[7:]  # Ta bort "sök på " från början
            return self.web_search.search(query)
        
        # Kontrollera om det är en fråga (börjar med "vad", "vem", "hur", etc.)
        question_starters = ["vad", "vem", "hur", "varför", "när", "var"]
        if any(user_input.startswith(starter) for starter in question_starters):
            # Detta verkar vara en fråga, prova att söka på webben
            return self.web_search.search(user_input)
        
        # Om inte ett kommando eller en sökning, fortsätt med vanlig svarshantering
        # Gå igenom varje kategori av svar
        for category in self.responses:
            # Undanta fallback-kategorin som hanteras separat
            if category == "fallback":
                continue
                
            # Kontrollera om input matchar något nyckelord i denna kategori
            for keyword, response in self.responses[category].items():
                if keyword in user_input:
                    return response
        
        # Om inget matchade, välj ett slumpmässigt fallback-svar
        return random.choice(self.responses["fallback"])