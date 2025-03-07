"""
Modul för röstinteraktion i Nova chatbot.
Hanterar både tal-till-text och text-till-tal.
"""

from .recognition import VoiceRecognizer
from .speech import VoiceSpeaker
from utils.command_handler import CommandHandler

class VoiceInterface:
    """
    Klass för att hantera röstinteraktion med användaren.
    Kombinerar taligenkänning och tal.
    """
    
    def __init__(self, chatbot_name="Nova"):
        """
        Initierar en ny instans av VoiceInterface.
        
        Args:
            chatbot_name (str): Namn på chatboten
        """
        # Skapa komponenter för taligenkänning och tal
        self.recognizer = VoiceRecognizer()
        self.speaker = VoiceSpeaker()
        
        # Initiera kommandohanterare
        self.command_handler = CommandHandler(chatbot_name)
        
        # Flagga för om röststyrning är aktiverad
        self.voice_enabled = False
        
    def toggle_voice(self):
        """
        Växlar mellan aktivering och deaktivering av röststyrning.
        
        Returns:
            bool: Den nya statusen för röststyrning (True = aktiverad)
        """
        self.voice_enabled = not self.voice_enabled
        status = "aktiverad" if self.voice_enabled else "deaktiverad"
        print(f"Röststyrning är nu {status}")
        
        # Om röststyrning stängs av, rensa gamla temporära filer
        if not self.voice_enabled:
            self.speaker.cleanup_temp_files()
            
        return self.voice_enabled
        
    def say_response(self, text):
        """
        Läser upp ett svar med röst.
        
        Args:
            text (str): Texten som ska läsas upp
        """
        if self.voice_enabled:
            self.speaker.speak(text)
    
    def listen_for_activation(self):
        """
        Lyssnar efter aktiveringskommandon, även när röststyrning är avstängd.
        
        Returns:
            str: Kommandot som identifierades, eller None
        """
        # Hämta aktiveringsfraserna från commands.json
        activation_phrases = []
        for cmd_type, cmd_data in self.command_handler.commands.items():
            if cmd_data.get("action") == "activate_voice":
                activation_phrases.extend(cmd_data.get("phrases", []))
        
        # Om vi inte hittade några fraser, använd några standardfraser
        if not activation_phrases:
            activation_phrases = ["nova är du här", "hej nova", "aktivera röststyrning"]
            
        print("Väntar på kommando...")
        
        # Lyssna efter nyckelord med de specifika fraserna
        text = self.recognizer.listen_for_keyword(activation_phrases)
        
        # Om vi fick text, kontrollera om det är ett kommando
        if text:
            return text
        
        return None
        
    def listen_for_command(self):
        """
        Lyssnar efter ett kommando från användaren.
        
        Returns:
            str: Det uppfattade kommandot, eller None om inget uppfattades
        """
        # Lyssna efter användarinput
        return self.recognizer.listen()
        
    def check_for_command(self, text):
        """
        Kontrollerar om texten innehåller ett systemkommando.
        
        Args:
            text (str): Texten att kontrollera
            
        Returns:
            tuple: (action, response) om kommando hittades, annars (None, None)
        """
        # Använd CommandHandler för att kontrollera efter kommandon
        return self.command_handler.check_command(text)