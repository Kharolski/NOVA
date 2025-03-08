import os
import subprocess
import webbrowser
import platform

class SystemActions:
    """Klass för att hantera systemåtgärder som att öppna applikationer och webbplatser."""
    
    def __init__(self):
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
                'safari': 'Safari.app'
            },
            'linux': {
                'kalkylator': 'gnome-calculator',
                'kalkylatorn': 'gnome-calculator',
                'anteckningar': 'gedit',
                'utforskaren': 'nautilus'
            }
        }
    
    def open_browser(self):
        """Öppnar standardwebbläsaren."""
        try:
            webbrowser.open("https://www.google.com")
            return True
        except Exception as e:
            print(f"Kunde inte öppna webbläsaren: {e}")
            return False
    
    def open_website(self, website):
        """
        Öppnar den angivna webbplatsen i standardwebbläsaren.
        
        Args:
            website (str): URL:en att öppna
        
        Returns:
            bool: True om operationen lyckas, annars False
        """
        if not website.startswith(('http://', 'https://')):
            # Om ingen protokollprefix, lägg till https://
            if not website.startswith('www.'):
                website = 'www.' + website
            website = 'https://' + website.replace('www.', '', 1) if website.startswith('www.') else 'https://' + website
        
        try:
            webbrowser.open(website)
            return True
        except Exception as e:
            print(f"Kunde inte öppna webbplatsen {website}: {e}")
            return False
    
    def open_application(self, app_name):
        """
        Öppnar den angivna applikationen.
        
        Args:
            app_name (str): Namnet på applikationen att öppna
        
        Returns:
            bool: True om operationen lyckas, annars False
        """
        app_name = app_name.lower()
        system_key = self.system.lower()
        
        if system_key not in self.common_apps:
            print(f"Operativsystemet {self.system} stöds inte.")
            return False
        
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
                return True
            except Exception as e:
                print(f"Kunde inte öppna applikationen {app_name}: {e}")
                return False
        else:
            print(f"Applikationen '{app_name}' finns inte i listan över kända applikationer.")
            # Försök att köra appnamnet direkt
            try:
                subprocess.Popen(app_name, shell=True)
                return True
            except Exception as e:
                print(f"Kunde inte öppna applikationen {app_name} direkt: {e}")
                return False