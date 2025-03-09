"""
Modul för att hantera systemspecifika åtgärder som att öppna webbläsare, 
webbplatser och applikationer.
"""

import os
import subprocess
import webbrowser
import platform


class SystemActions:
    """
    Hanterar systemåtgärder som att öppna applikationer och webbplatser.
    
    Stödjer flera operativsystem: Windows, macOS (Darwin) och Linux.
    """
    
    def __init__(self):
        """
        Initierar SystemActions med operativsystemsdetektering och 
        en mappning av vanliga applikationer.
        """
        self.system = platform.system()  # 'Windows', 'Darwin' (macOS), 'Linux'
        
        # Mappa vanliga applikationsnamn till deras faktiska körbara filer på olika plattformar
        self.common_apps = {
            'windows': {
                'kalkylator': 'calc.exe',
                'kalkylatorn': 'calc.exe',
                'notepad': 'notepad.exe',
                'anteckningar': 'notepad.exe',
                'filutforskaren': 'explorer.exe',
                'utforskaren': 'explorer.exe',
                'paint': 'mspaint.exe',
                'ritprogrammet': 'mspaint.exe',
                'word': 'winword.exe',
                'excel': 'excel.exe',
                'powerpoint': 'powerpnt.exe',
                'outlook': 'outlook.exe'
            },
            'darwin': {  # macOS
                'kalkylator': 'Calculator.app',
                'kalkylatorn': 'Calculator.app',
                'anteckningar': 'Notes.app',
                'utforskaren': 'Finder.app',
                'safari': 'Safari.app',
                'terminalen': 'Terminal.app',
                'inställningar': 'System Preferences.app'
            },
            'linux': {
                'kalkylator': 'gnome-calculator',
                'kalkylatorn': 'gnome-calculator',
                'anteckningar': 'gedit',
                'utforskaren': 'nautilus',
                'terminal': 'gnome-terminal',
                'inställningar': 'gnome-control-center'
            }
        }
    
    def open_browser(self):
        """
        Öppnar standardwebbläsaren med Googles startsida.
        
        Returns:
            dict: Resultat med status och meddelande
        """
        try:
            webbrowser.open("https://www.google.com")
            return {"success": True, "message": "Webbläsaren öppnades framgångsrikt."}
        except Exception as e:
            error_msg = f"Kunde inte öppna webbläsaren: {e}"
            print(error_msg)
            return {"success": False, "message": error_msg}
    
    def open_website(self, website):
        """
        Öppnar den angivna webbplatsen i standardwebbläsaren.
        
        Args:
            website (str): URL:en att öppna
        
        Returns:
            dict: Resultat med status och meddelande
        """
        # Hantera tomma eller None-värden
        if not website:
            return {"success": False, "message": "Ingen webbplats angiven."}
            
        # Säkerställ att URL:en är korrekt formaterad
        if not website.startswith(('http://', 'https://')):
            # Om ingen protokollprefix, lägg till https://
            if not website.startswith('www.'):
                website = 'www.' + website
            website = 'https://' + website.replace('www.', '', 1) if website.startswith('www.') else 'https://' + website
        
        try:
            webbrowser.open(website)
            return {"success": True, "message": f"Öppnade {website} framgångsrikt."}
        except Exception as e:
            error_msg = f"Kunde inte öppna webbplatsen {website}: {e}"
            print(error_msg)
            return {"success": False, "message": error_msg}
    
    def open_application(self, app_name):
        """
        Öppnar den angivna applikationen.
        
        Args:
            app_name (str): Namnet på applikationen att öppna
        
        Returns:
            dict: Resultat med status och meddelande
        """
        # Hantera tomma eller None-värden
        if not app_name:
            return {"success": False, "message": "Ingen applikation angiven."}
            
        app_name = app_name.lower()
        system_key = self.system.lower()
        
        if system_key not in self.common_apps:
            error_msg = f"Operativsystemet {self.system} stöds inte."
            print(error_msg)
            return {"success": False, "message": error_msg}
        
        # Kontrollera om applikationen finns i listan över kända applikationer
        if app_name in self.common_apps[system_key]:
            app_executable = self.common_apps[system_key][app_name]
            
            try:
                if system_key == 'windows':
                    subprocess.Popen(app_executable, shell=True)
                elif system_key == 'darwin':  # macOS
                    subprocess.Popen(['open', '-a', app_executable])
                else:  # Linux
                    subprocess.Popen(app_executable, shell=True)
                return {"success": True, "message": f"Applikationen {app_name} öppnades framgångsrikt."}
            except Exception as e:
                error_msg = f"Kunde inte öppna applikationen {app_name}: {e}"
                print(error_msg)
                return {"success": False, "message": error_msg}
        else:
            print(f"Applikationen '{app_name}' finns inte i listan över kända applikationer. Provar direkt...")
            # Försök att köra appnamnet direkt
            try:
                subprocess.Popen(app_name, shell=True)
                return {"success": True, "message": f"Applikationen {app_name} öppnades direkt."}
            except Exception as e:
                error_msg = f"Kunde inte öppna applikationen {app_name} direkt: {e}"
                print(error_msg)
                return {"success": False, "message": error_msg}
                
    def exit_application(self):
        """
        Förbereder för att avsluta applikationen.
        
        Returns:
            dict: Statusinformation
        """
        return {"success": True, "message": "Förbereder för att avsluta programmet."}