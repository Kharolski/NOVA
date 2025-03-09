"""
Modul för att hantera konversationsmönster och svar i Nova chatbot.
"""

import json
import os
import random


class ResponseHandler:
    """
    Hanterar matchning av användarinput mot fördefinierade fraser och genererar lämpliga svar.
    """
    
    def __init__(self, chatbot_name="NOVA"):
        """
        Initierar ResponseHandler.
        
        Args:
            chatbot_name (str): Namn på chatboten, används för formatering av svar
        """
        self.chatbot_name = chatbot_name
        self.responses = self._load_responses()
        
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
                responses = data.get("responses", {})
                print(f"Laddade {len(responses)} svarskategorier från responses.json")
                return responses
                
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
        Matchar användarinput mot fördefinierade fraser och genererar ett svar.
        
        Args:
            user_input (str): Användarens input, förväntas vara förbehandlad (lowercase, strip, etc.)
            
        Returns:
            str: Ett lämpligt svar baserat på input
        """
        # Gå igenom varje kategori av svar
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
                        response = random.choice(responses_list)
                        # Ersätt eventuella variabler i svaret
                        response = response.replace("{name}", self.chatbot_name)
                        return response
        
        # Om inget matchade, välj ett slumpmässigt fallback-svar
        if "fallback" in self.responses:
            fallback_responses = self.responses["fallback"].get("responses", [])
            if fallback_responses:
                response = random.choice(fallback_responses)
                response = response.replace("{name}", self.chatbot_name)
                return response
            
        # Om ingen fallback-kategori finns, använd ett standardsvar
        return f"Jag förstår inte riktigt. Kan du förklara på ett annat sätt?"