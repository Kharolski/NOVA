"""
Modul för röstigenkänning i Nova chatbot.
"""

import speech_recognition as sr

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
            print("Timeout - inget ljud uppfattades")
            return None
        except sr.UnknownValueError:
            # Kunde inte förstå ljudet
            print("Kunde inte förstå ljudet")
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
        # Ta bort den hårdkodade listan helt
        # Låt det vara None om inget skickas, vilket betyder att vi lyssnar efter alla ljud
        
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