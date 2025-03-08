"""
Modul för röstutmatning (text-till-tal) i Nova chatbot.
Använder Google's Text-to-Speech API för bättre kvalitet.
"""

from gtts import gTTS
import os
import pygame
import time
import re

class VoiceSpeaker:
    """
    Klass för att hantera röstutmatning (text-till-tal) med Google TTS.
    """
    
    def __init__(self):
        """
        Initierar en ny instans av VoiceSpeaker.
        """
        # Initialisera pygame mixer för ljuduppspelning
        pygame.mixer.init()
        
        # Ställ in språk (sv för svenska)
        self.language = "sv"
        
        # Flagga för om en uppläsning pågår
        self.is_speaking = False
        
        # Skapa en dedikerad mapp för Nova's temporära filer
        self.nova_temp_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp", "Nova")
        if not os.path.exists(self.nova_temp_dir):
            os.makedirs(self.nova_temp_dir)
            
        # Rensa gamla filer vid start
        self.cleanup_temp_files()
    
    def improve_speech_text(self, text):
        """
        Förbättrar text för att ge mer naturlig röstuppläsning.
        
        Args:
            text (str): Originaltexten som ska förbättras
            
        Returns:
            str: Förbättrad text för mer naturligt tal
        """
        # Ord som uttalas konstigt - ersätt med bättre fonetiska versioner
        replacements = {
            "AI": "A I",
            "chatbot": "chatt bått",
            "Nova": "Nåva",  # Om uttalsproblem finns
            "URL": "U R L",
            "HTTP": "H T T P",
            "HTML": "H T M L",
            "www": "w w w",
            ".com": "dått cåmm",
            "plugin": "plugg in",
            "UI": "U I",
            "GUI": "G U I",
            "API": "A P I",
        }
        
        # Tillämpa ersättningar
        for word, replacement in replacements.items():
            # Använd regex för att se till att vi bara ersätter hela ord
            text = re.sub(r'\b' + re.escape(word) + r'\b', replacement, text)
        
        # Lägg till pauser för mer naturligt tal genom att modifiera punktuation
        text = text.replace(". ", "... ")     # Längre paus efter meningar
        text = text.replace("? ", "?... ")    # Längre paus efter frågor
        text = text.replace("! ", "!... ")    # Längre paus efter utrop
        text = text.replace(", ", ",.. ")     # Kort paus vid kommatecken
        text = text.replace(": ", ":.. ")     # Kort paus vid kolon
        
        # Dela upp långa siffror för bättre uppläsning
        # T.ex. ändra "12345" till "1 2 3 4 5"
        def space_digits(match):
            digits = match.group(0)
            return " ".join(digits)
            
        text = re.sub(r'\b\d{4,}\b', space_digits, text)
        
        return text
    
    def cleanup_temp_files(self):
        """
        Rensar alla temporära MP3-filer i Nova-mappen.
        """
        try:
            count = 0
            for filename in os.listdir(self.nova_temp_dir):
                if filename.endswith(".mp3"):
                    file_path = os.path.join(self.nova_temp_dir, filename)
                    try:
                        os.remove(file_path)
                        count += 1
                    except Exception as e:
                        print(f"Kunde inte radera {file_path}: {e}")
            print(f"Rensade {count} gamla temporära ljudfiler från Nova-mappen.")
        except Exception as e:
            print(f"Ett fel uppstod vid rensning av temporära filer: {e}")
    
    def speak(self, text):
        """
        Konverterar text till tal och läser upp det med Google TTS.
        
        Args:
            text (str): Texten som ska läsas upp
        """
        try:
            print(f"Läser upp: {text}")
            self.is_speaking = True
            
            # Förbättra texten för mer naturligt tal
            improved_text = self.improve_speech_text(text)
            
            # Skapa ett unikt filnamn i Nova-mappen
            timestamp = int(time.time())
            temp_filename = os.path.join(self.nova_temp_dir, f"nova_speech_{timestamp}.mp3")
            
            # Använd Google TTS för att konvertera text till tal
            tts = gTTS(text=improved_text, lang=self.language, slow=False)
            tts.save(temp_filename)
            
            # Spela upp ljudfilen
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            
            # Vänta tills ljudet är färdigspelat
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Vi försöker inte radera filen direkt - den rensas vid nästa start
            
        except Exception as e:
            print(f"Ett fel uppstod vid uppläsning: {e}")
        finally:
            self.is_speaking = False