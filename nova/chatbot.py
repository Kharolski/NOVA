"""
Huvudmodul för Nova chatbot.
"""

import json
import os
import random
from nova.commands import CommandHandler
from nova.responses import ResponseHandler


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
        self.command_handler = CommandHandler(chatbot_name=self.name)
        self.response_handler = ResponseHandler(chatbot_name=self.name)
        self.exit_requested = False
    
    def get_response(self, user_input):
        """
        Genererar ett svar baserat på användarens input.
        
        Args:
            user_input (str): Användarens meddelande
            
        Returns:
            str eller dict: Novas svar, antingen som sträng eller som dictionary med action-info
        """
        # Konvertera input till gemener för bättre matchning
        user_input = user_input.lower().strip()
        
        # Kontrollera om input är ett kommando
        action, response, extra_data = self.command_handler.check_command(user_input)
        
        if action:
            # Om vi har en action, formatera svaret korrekt
            command_result = {
                "action": action,
                "text": response,
                "extra_data": extra_data
            }
            
            # Om kommandot är för att avsluta, markera detta
            if action == "exit_app":
                self.exit_requested = True
                
            return command_result
        
        # Om inte ett kommando, delegera till response_handler
        return self.response_handler.get_response(user_input)