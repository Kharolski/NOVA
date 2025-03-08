"""
Modul för grafiskt gränssnitt med tkinter för Nova chatbot.
"""

import tkinter as tk
from tkinter import messagebox
from voice import VoiceInterface
import threading
import time
import webbrowser
from utils.system_actions import SystemActions

class GraphicalInterface:
    """
    Ett grafiskt gränssnitt för Nova chatbot med tkinter.
    """
    
    def __init__(self, chatbot):
        """
        Initierar det grafiska gränssnittet.
        
        Args:
            chatbot: En instans av Nova chatbot
        """
        self.chatbot = chatbot
        self.root = tk.Tk()
        self.root.title(f"{self.chatbot.name} Chatbot")
        self.root.geometry("600x600")
        self.root.resizable(True, True)
        
        # För att hålla reda på "tänker"-meddelandet
        self.thinking_displayed = False
        
        # Lista för att hålla reda på meddelandewidgets
        self.message_widgets = []
        
        # Skapa röstgränssnitt
        self.voice_interface = VoiceInterface()
        self.system_actions = SystemActions()
        
        # ========== INIT UI COMPONENTS ==========
        self.create_menu()
        self.create_chat_frame()
        self.create_input_frame()
        # ========================================

        # Starta bakgrundslyssning efter nyckelord
        self.start_keyword_listening()
    
    # ---------------------------------------------------------------
    # Menu Functions
    # ---------------------------------------------------------------
    def create_menu(self):
        """
        Skapar menyn i det grafiska gränssnittet.
        """
        menubar = tk.Menu(self.root)
        
        # Skapa en File-meny
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Rensa chathistorik", command=self.clear_chat)
        file_menu.add_separator()
        file_menu.add_command(label="Avsluta", command=self.exit_application)
        
        # Skapa en Röst-meny
        voice_menu = tk.Menu(menubar, tearoff=0)
        voice_menu.add_command(label="Växla röststyrning", command=self.toggle_voice)
        voice_menu.add_command(label="Starta röstinmatning", command=self.activate_voice_input)
        
        # Skapa en Help-meny
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Hjälp", command=self.show_help)
        help_menu.add_command(label="Om NOVA", command=self.show_about)
        
        # Lägg till menyerna på menyraden
        menubar.add_cascade(label="Arkiv", menu=file_menu)
        menubar.add_cascade(label="Röst", menu=voice_menu)
        menubar.add_cascade(label="Hjälp", menu=help_menu)
        
        # Konfigurera root att använda menyn
        self.root.config(menu=menubar)
    
    def show_help(self):
        """
        Visar hjälpinformation.
        """
        help_text = self.chatbot.command_handler.get_help()
        messagebox.showinfo("Hjälp", help_text)

    def show_about(self):
        """
        Visar information om NOVA.
        """
        about_text = (
            f"{self.chatbot.name} är en enkel chatbot som kan hjälpa dig med "
            f"grundläggande uppgifter som att svara på frågor, visa tid och datum, "
            f"och söka information på webben.\n\n"
            f"Version: 1.0\n"
            f"Utvecklad som ett övningsprojekt i Python."
        )
        messagebox.showinfo("Om NOVA", about_text)

    def exit_application(self):
        """Avslutar applikationen"""
        print("Avslutar programmet...")
        # Stäng av röststyrning för att rensa temporära filer
        if self.voice_interface.voice_enabled:
            self.voice_interface.voice_enabled = False
            self.voice_interface.speaker.cleanup_temp_files()
        # Avsluta programmet
        self.root.quit()
        self.root.destroy()

    def clear_chat(self):
        """
        Rensar chatrutan och visar ett nytt välkomstmeddelande.
        """
        # Ta bort alla meddelanden
        for widget in self.message_widgets:
            widget.destroy()
        self.message_widgets = []
        
        # Visa välkomstmeddelande igen
        self.display_bot_message(f"Chathistoriken har rensats. Hur kan jag hjälpa dig?")

    # ---------------------------------------------------------------
    # Chat Display Functions
    # ---------------------------------------------------------------
    def create_chat_frame(self):
        """
        Skapar en modernare chatruta där användarmeddelanden visas på höger sida
        och botmeddelanden på vänster sida.
        """
        # Huvudramen för chatten
        chat_frame = tk.Frame(self.root)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas med scrollbar för att kunna rulla
        self.canvas = tk.Canvas(chat_frame, bg="#f0f0f0")
        scrollbar = tk.Scrollbar(chat_frame, orient="vertical", command=self.canvas.yview)
        
        # Konfigurera canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Skapa en frame inuti canvas för att hålla meddelandena
        self.messages_frame = tk.Frame(self.canvas, bg="#f0f0f0")
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.messages_frame, anchor="nw")
        
        # Konfigurera canvas att ändra storlek med fönstret
        self.messages_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
    
    def on_frame_configure(self, event):
        """Uppdaterar scrollregionen när den inre framen ändrar storlek."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """Ändrar storleken på den inre framen när canvas ändrar storlek."""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)
    
    def display_bot_message(self, message):
        """
        Visar botens meddelande i en bubbla på vänster sida.
        
        Args:
            message (str): Botens meddelande
        """
        # Skapa en frame för detta meddelande
        msg_frame = tk.Frame(self.messages_frame, bg="#f0f0f0")
        msg_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Skapa botens meddelandebubbla på vänster sida
        bubble = tk.Frame(msg_frame, bg="#E5E5EA", padx=10, pady=8)
        bubble.pack(side=tk.LEFT)
        
        # Lägg till texten i bubblan
        msg_label = tk.Label(
            bubble, 
            text=message, 
            bg="#E5E5EA", 
            fg="black", 
            font=("Arial", 11),
            justify="left",
            wraplength=300
        )
        msg_label.pack()
        
        # Lägg till en tom label på höger sida för balans
        tk.Label(msg_frame, bg="#f0f0f0", width=10).pack(side=tk.RIGHT)
        
        # Lägg till denna widget i listan och scrolla ner
        self.message_widgets.append(msg_frame)
        self.canvas.yview_moveto(1.0)

    def display_user_message(self, message):
        """
        Visar användarens meddelande i en bubbla på höger sida.
        
        Args:
            message (str): Användarens meddelande
        """
        # Skapa en frame för detta meddelande
        msg_frame = tk.Frame(self.messages_frame, bg="#f0f0f0")
        msg_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Skapa en tom label på vänster sida för att skjuta meddelandet åt höger
        tk.Label(msg_frame, bg="#f0f0f0", width=10).pack(side=tk.LEFT)
        
        # Skapa en frame som fungerar som meddelandebubbla
        bubble = tk.Frame(msg_frame, bg="#0084FF", padx=10, pady=8)
        bubble.pack(side=tk.RIGHT)
        
        # Lägg till texten i bubblan
        msg_label = tk.Label(
            bubble, 
            text=message, 
            bg="#0084FF", 
            fg="white", 
            font=("Arial", 11),
            justify="left",
            wraplength=200
        )
        msg_label.pack()
        
        # Lägg till denna widget i listan och scrolla ner
        self.message_widgets.append(msg_frame)
        self.canvas.yview_moveto(1.0)

    def display_thinking(self):
        """
        Visar ett "tänker"-meddelande i en bubbla på vänster sida.
        """
        # Skapa en frame för detta meddelande
        self.thinking_frame = tk.Frame(self.messages_frame, bg="#f0f0f0")
        self.thinking_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Skapa tänker-meddelandebubbla på vänster sida
        bubble = tk.Frame(self.thinking_frame, bg="#E5E5EA", padx=10, pady=8)
        bubble.pack(side=tk.LEFT)
        
        # Lägg till texten i bubblan
        msg_label = tk.Label(
            bubble, 
            text=f"{self.chatbot.name} tänker...", 
            bg="#E5E5EA", 
            fg="black", 
            font=("Arial", 11, "italic")
        )
        msg_label.pack()
        
        # Scrolla ner till botten
        self.canvas.yview_moveto(1.0)
        self.thinking_displayed = True

    def remove_thinking_and_display_response(self, response):
        """
        Tar bort "tänker"-meddelandet och visar chatbotens svar.
        
        Args:
            response (str): Chatbotens svar
        """
        # Ta bort "tänker"-frameen om den finns
        if self.thinking_displayed and hasattr(self, 'thinking_frame'):
            self.thinking_frame.destroy()
            self.thinking_displayed = False
        
        # Visa chatbotens svar
        self.display_bot_message(response)
        
        # Om röststyrning är aktiverad, läs upp svaret
        self.voice_interface.say_response(response)

    def run(self):
        """
        Startar det grafiska gränssnittet.
        """
        # Visa välkomstmeddelandet när programmet startar
        self.display_bot_message(f"Välkommen till {self.chatbot.name}! Hur kan jag hjälpa dig idag?")
        
        # Starta huvudloopen
        self.root.mainloop()

    # ---------------------------------------------------------------
    # Input Functions
    # ---------------------------------------------------------------
    def create_input_frame(self):
        """
        Skapar input-fältet och knapparna.
        """
        input_frame = tk.Frame(self.root, height=50)
        input_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)
        
        # Inmatningsfält
        self.user_input = tk.Entry(input_frame, font=("Arial", 11))
        self.user_input.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=(0, 10))
        
        # Bind Enter-tangenten till send_message
        self.user_input.bind("<Return>", lambda event: self.send_message())
        
        # Röstknapp
        self.voice_button = tk.Button(
            input_frame, 
            text="🎤 Av", 
            command=self.toggle_voice, 
            bg="#CCCCCC", 
            fg="black", 
            font=("Arial", 11, "bold"),
            width=6
        )
        self.voice_button.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Skicka-knapp
        send_button = tk.Button(
            input_frame, 
            text="Skicka", 
            command=self.send_message, 
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 11, "bold"),
            width=10
        )
        send_button.pack(side=tk.RIGHT)
        
        # Sätt fokus på input-fältet
        self.user_input.focus_set()
    
    def send_message(self):
        """
        Skickar användarens meddelande till chatboten och visar svaret.
        """
        user_message = self.user_input.get()
        
        if not user_message.strip():
            return
            
        # Visa användarens meddelande i chatten
        self.display_user_message(user_message)
        self.user_input.delete(0, tk.END)
        
        # Få ett svar från chatboten
        response = self.chatbot.get_response(user_message)
        
        # Kontrollera om exit_requested är satt
        if self.chatbot.exit_requested:
            # Visa meddelandet
            self.display_bot_message(response)
            # Om röststyrning är aktiverad, läs upp svaret
            if self.voice_interface.voice_enabled:
                self.voice_interface.say_response(response)
            # Vänta lite och avsluta
            self.root.after(2000, self.exit_application)
            return

        # Kontrollera om svaret är en sträng eller ett dictionary
        if isinstance(response, dict):
            # Om det är ett dictionary, kontrollera om det har en action
            if response.get("action"):
                # Skicka med extra_data om det finns
                extra_data = response.get("extra_data")
                self.handle_action(response["action"], response["text"], extra_data)
            else:
                # Visa chatbotens svar i chatten
                self.display_bot_message(response["text"])
                
                # Om röststyrning är aktiverad, läs upp svaret
                if self.voice_interface.voice_enabled:
                    self.voice_interface.say_response(response["text"])
        else:
            # Om det är en sträng, visa den direkt
            self.display_bot_message(response)
            
            # Om röststyrning är aktiverad, läs upp svaret
            if self.voice_interface.voice_enabled:
                self.voice_interface.say_response(response)

    # ---------------------------------------------------------------
    # Voice Interface Functions
    # ---------------------------------------------------------------
    def toggle_voice(self):
        """
        Växlar röststyrning på/av och uppdaterar knappens utseende.
        Om röststyrning aktiveras, börjar systemet lyssna direkt.
        """
        is_enabled = self.voice_interface.toggle_voice()
        
        if is_enabled:
            self.voice_button.config(text="🎤 På", bg="#FF6347")

            # Om röststyrning aktiveras via knapp, läs upp ett bekräftelsemeddelande
            self.voice_interface.say_response(f"Vad {self.chatbot.name} kan hjälpa dig medd ?")

            # Starta röstinmatning direkt efter en kort fördröjning
            self.root.after(400, self.activate_voice_input)  # Vänta 0.4 sekunder efter bekräftelsemeddelandet
        else:
            self.voice_button.config(text="🎤 Av", bg="#CCCCCC")

    def activate_voice_input(self):
        """
        Aktiverar röstinmatning för att lyssna efter ett kommando.
        """
        if not self.voice_interface.voice_enabled:
            return
            
        # Visa "lyssnar..." text
        self.display_bot_message("Lyssnar... Säg ditt meddelande.")
        
        # Starta en ny tråd för att lyssna efter röst (för att inte blockera GUI)
        threading.Thread(target=self.process_voice_input, daemon=True).start()

    def process_voice_input(self):
        """
        Processar röstinmatning i en separat tråd.
        """
        # Lyssna efter ett kommando
        text = self.voice_interface.listen_for_command()
        
        if text:
            # Kontrollera om det är ett systemkommando
            action, response, extra_data = self.voice_interface.check_for_command(text)
            
            if action:
                # Hantera specifika fall som kräver särskild hantering i röstläge
                if action == "deactivate_voice":
                    # Stäng av röststyrning
                    self.voice_interface.voice_enabled = False
                    self.voice_button.config(text="🎤 Av", bg="#CCCCCC")
                    self.voice_interface.say_response(response)
                    return
                elif action == "exit_app":
                    # Hantera avslutning (vi måste visa meddelande innan avslutning)
                    self.display_bot_message(response)
                    self.voice_interface.say_response(response)
                    self.root.after(2000, self.exit_application)
                    return
                
                # För andra kommandon, använd handle_action
                self.handle_action(action, response, extra_data)
                
                # För kommandon som inte avslutar röstlyssning
                if self.voice_interface.voice_enabled:
                    self.root.after(3000, self.activate_voice_input)
                return
                
            # Om det inte är ett systemkommando, behandla det som ett vanligt meddelande
            self.root.after(0, lambda: self.user_input.insert(0, text))
            self.root.after(100, self.send_message)
            
            # Om röststyrning fortfarande är aktiverad, lyssna igen efter en kort fördröjning
            if self.voice_interface.voice_enabled:
                self.root.after(3000, self.activate_voice_input)
        else:
            # Om inget text uppfattades, visa ett meddelande
            self.root.after(0, lambda: self.display_bot_message("Jag kunde inte förstå vad du sa."))
            
            # Om röststyrning fortfarande är aktiverad, lyssna igen efter en kort fördröjning
            if self.voice_interface.voice_enabled:
                self.root.after(1500, self.activate_voice_input)

    def start_keyword_listening(self):
        """
        Startar en bakgrundsprocess som lyssnar efter nyckelord.
        """
        def background_listener():
            while True:
                # Lyssna efter nyckelord om röststyrning är avstängd
                if not self.voice_interface.voice_enabled:
                    command_text = self.voice_interface.listen_for_activation()
                    if command_text:
                        # Kontrollera om det är ett kommando
                        action, response, extra_data = self.voice_interface.check_for_command(command_text)
                        
                        if action == "activate_voice":
                            # Aktivera röststyrning
                            self.voice_interface.voice_enabled = True
                            # Uppdatera UI
                            self.root.after(0, lambda: self.voice_button.config(text="🎤 På", bg="#FF6347"))
                            # Säg svaret
                            self.root.after(0, lambda r=response: self.voice_interface.say_response(r))
                            # Starta lyssning efter en kort fördröjning
                            self.root.after(1000, self.activate_voice_input)
                            print("Röststyrning är nu aktiverad")
        
        # Starta en separat tråd för bakgrundslyssning
        import threading
        threading.Thread(target=background_listener, daemon=True).start()

    def update_voice_button(self):
        """
        Uppdaterar röstknappens utseende baserat på röststyrningens status.
        """
        if self.voice_interface.voice_enabled:
            self.voice_button.config(text="🎤 På", bg="#FF6347")
        else:
            self.voice_button.config(text="🎤 Av", bg="#CCCCCC")

    # ---------------------------------------------------------------
    # Command Handling Functions
    # ---------------------------------------------------------------
    def handle_action(self, action, response_text, extra_data=None):
        """
        Hanterar en åtgärd baserat på kommandot från chatboten.
        
        Args:
            action (str): Åtgärden som ska utföras
            response_text (str): Svartexten att visa
            extra_data (dict, optional): Extra data för kommandot
        """
        # Visa svar i chatten
        self.display_bot_message(response_text)
        
        # Läs upp svaret om röststyrning är aktiverad
        if self.voice_interface.voice_enabled:
            self.voice_interface.say_response(response_text)
        
        # Utför åtgärden
        if action == "activate_voice":
            if not self.voice_interface.voice_enabled:
                self.toggle_voice()
        elif action == "deactivate_voice":
            if self.voice_interface.voice_enabled:
                self.toggle_voice()
        elif action == "clear_chat":
            self.clear_chat()
        elif action == "open_browser":
            self.system_actions.open_browser()
        elif action == "open_website" and extra_data and 'website' in extra_data:
            self.system_actions.open_website(extra_data['website'])
        elif action == "open_application" and extra_data and 'app_name' in extra_data:
            self.system_actions.open_application(extra_data['app_name'])
        elif action == "show_time":
            # Tiden visas redan i svaret, inget mer behövs
            pass
        elif action == "show_help":
            # Hjälpinformationen visas redan i svaret, inget mer behövs
            pass
        elif action == "exit_app":
            self.exit_application()

    # ---------------------------------------------------------------
    # Chatbot Response Functions
    # ---------------------------------------------------------------
    def get_bot_response(self, user_message):
        """
        Får svar från chatboten i en separat tråd.
        
        Args:
            user_message (str): Användarens meddelande
        """
        # Få svar från chatboten
        response = self.chatbot.get_response(user_message)
        print(f"Svar från get_bot_response: {response}")
        
        # Ta bort "tänker"-meddelandet och visa svaret
        self.root.after(0, lambda: self.remove_thinking_and_display_response(response))
        
        # Kontrollera om användaren vill avsluta
        if self.chatbot.exit_requested:
            self.root.after(1500, self.exit_program)
    
    # ---------------------------------------------------------------
    # Webbrowser Response Functions
    # ---------------------------------------------------------------
    


    

    

