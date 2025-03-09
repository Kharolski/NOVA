"""
Modul för röstinteraktion i Nova chatbot.
Hanterar både tal-till-text och text-till-tal.
"""

import os
import time
import re
import pygame
import speech_recognition as sr
from gtts import gTTS

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


class VoiceRecognizer:
    """
    Klass för att hantera röstigenkänning.
    """
    
    def __init__(self):
        """
        Initierar en ny instans av VoiceRecognizer.
        """
        # Skapa en recognizer-instans från speech_recognition
        self.recognizer = sr.Recognizer()
        
        # Ange språket för igenkänning (svenska)
        self.language = "sv-SE"
    
    def listen(self):
        """
        Lyssnar efter tal och omvandlar det till text.
        
        Returns:
            str: Den uppfattade texten, eller None om inget tal uppfattades
        """
        try:
            # Skriv bara en gång att vi lyssnar
            print("Lyssnar...")
            
            # Använd mikrofonen som ljudkälla
            with sr.Microphone() as source:
                # Justera för bakgrundsljud
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Lyssna efter ljud från mikrofonen
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                # Försök känna igen talet
                text = self.recognizer.recognize_google(audio, language=self.language)
                print(f"Uppfattade: '{text}'")
                return text
                    
        except sr.WaitTimeoutError:
            # Timeout - inget ljud hördes
            # print("Timeout - inget ljud uppfattades")
            return None
        except sr.UnknownValueError:
            # Kunde inte förstå ljudet
            # print("Kunde inte förstå ljudet")
            return None
        except sr.RequestError:
            # Kunde inte ansluta till Google's API
            print("Kunde inte ansluta till Google's API")
            return None
        except Exception as e:
            print(f"Ett fel uppstod vid taligenkänning: {e}")
            return None      

    def listen_for_keyword(self, keywords=None):
        """
        Lyssnar efter specifika nyckelord.
        
        Args:
            keywords (list): Lista med nyckelord att lyssna efter. 
                            Om None, lyssnar efter alla ord.
        
        Returns:
            str: Den uppfattade texten om ett nyckelord identifieras, annars None
        """
        try:
            print("Lyssnar efter nyckelord...")
            
            # Använd mikrofonen som ljudkälla
            with sr.Microphone() as source:
                # Justera för bakgrundsljud
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Lyssna efter ljud från mikrofonen med kortare timeout
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Försök känna igen talet
                text = self.recognizer.recognize_google(audio, language=self.language).lower()
                
                # Om vi har specifika nyckelord, kontrollera om texten matchar
                if keywords:
                    for keyword in keywords:
                        if keyword.lower() in text:
                            print(f"Nyckelord identifierat: '{text}'")
                            return text
                    # Inget nyckelord hittades
                    return None
                else:
                    # Om inga specifika nyckelord, returnera all text
                    print(f"Uppfattade: '{text}'")
                    return text
                    
        except sr.WaitTimeoutError:
            # Timeout - inget ljud hördes
            return None
        except sr.UnknownValueError:
            # Kunde inte förstå ljudet
            return None
        except sr.RequestError:
            # Kunde inte ansluta till Google's API
            return None
        except Exception as e:
            print(f"Ett fel uppstod vid lyssning efter nyckelord: {e}")
            return None


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
        
        # Importera CommandHandler här istället för på toppnivån för att undvika cirkulära beroenden
        from nova.commands import CommandHandler
        
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
            activation_phrases = ["nova är du här", "nova är du här", "nova lyssna", "hej nova", "aktivera röststyrning"]
            
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
        Kontrollerar om texten innehåller ett kommando.
        
        Args:
            text (str): Texten att kontrollera
        
        Returns:
            tuple: (action, response, extra_data) eller (None, None, None)
        """
        if self.command_handler:
            return self.command_handler.check_command(text)
        return None, None, None