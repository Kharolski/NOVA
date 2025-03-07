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
                data = json.load(file)
                return data.get("responses", {})
        except Exception as e:
            print(f"Kunde inte ladda svar från fil: {e}")
            # Returnera ett enkelt standardsvar om filen inte kunde laddas
            return {
                "greetings": {
                    "phrases": ["hej"],
                    "responses": ["Hej!"]
                },
                "fallback": {
                    "phrases": [],
                    "responses": ["Jag förstår inte."]
                }
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
        # Gå igenom varje kategori av svar med den nya strukturen
        for category, content in self.responses.items():
            # Undanta fallback-kategorin som hanteras separat
            if category == "fallback":
                continue
                
            # Kontrollera om input matchar någon fras i denna kategori
            phrases = content.get("phrases", [])
            for phrase in phrases:
                if phrase in user_input:
                    # Välj ett slumpmässigt svar från denna kategori
                    responses_list = content.get("responses", [])
                    if responses_list:
                        return random.choice(responses_list)
        
        # Om inget matchade, välj ett slumpmässigt fallback-svar
        if "fallback" in self.responses:
            fallback_responses = self.responses["fallback"].get("responses", [])
            if fallback_responses:
                return random.choice(fallback_responses)
            
        # Om ingen fallback-kategori finns, använd ett standardsvar
        return "Jag förstår inte riktigt. Kan du förklara på ett annat sätt?"