"""
Modul för textbaserat gränssnitt för Nova chatbot.
"""

class TextInterface:
    """
    Ett enkelt textbaserat gränssnitt för Nova chatbot.
    """
    
    def __init__(self, chatbot):
        """
        Initierar det textbaserade gränssnittet.
        
        Args:
            chatbot: En instans av Nova chatbot
        """
        self.chatbot = chatbot
    
    def display_welcome(self):
        """
        Visar ett välkomstmeddelande.
        """
        print("="*50)
        print(f"Välkommen till {self.chatbot.name} - Din personliga chatbot")
        print("="*50)
        print("Skriv 'hjälp' för att se tillgängliga kommandon.")
        print("Skriv 'avsluta' för att avsluta programmet.")
        print("="*50)
    
    def display_response(self, response):
        """
        Visar chatbotens svar på ett snyggt sätt.
        
        Args:
            response (str): Chatbotens svar
        """
        print(f"\n{self.chatbot.name}: {response}\n")
    
    def get_user_input(self):
        """
        Hämtar användarens input från konsolen.
        
        Returns:
            str: Användarens input
        """
        return input("Du: ")
    
    def run(self):
        """
        Startar det interaktiva chatbot-gränssnittet.
        """
        self.display_welcome()
        
        while True:
            user_input = self.get_user_input()
            
            # Avsluta om användaren skriver "avsluta" direkt
            if user_input.lower().strip() == "avsluta":
                print("\nAvslutar programmet. Hej då!")
                break
            
            # Få svar från chatboten
            response = self.chatbot.get_response(user_input)
            self.display_response(response)
            
            # Avsluta om chatboten säger att det är dags (t.ex. från exit_command)
            if self.chatbot.exit_requested:
                break