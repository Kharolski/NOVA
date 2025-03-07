"""
Modul för röstutmatning (text-till-tal) i Nova chatbot.
Använder Google's Text-to-Speech API för bättre kvalitet.
"""

from gtts import gTTS
import os
import pygame
import time

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
            
            # Skapa ett unikt filnamn i Nova-mappen
            timestamp = int(time.time())
            temp_filename = os.path.join(self.nova_temp_dir, f"nova_speech_{timestamp}.mp3")
            
            # Använd Google TTS för att konvertera text till tal
            tts = gTTS(text=text, lang=self.language, slow=False)
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