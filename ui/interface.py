"""
Modul för grafiskt gränssnitt med tkinter för Nova chatbot.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import time

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
        self.thinking_position = None
        
        # Skapa meny
        self.create_menu()
        
        # Skapa huvudramen för chatten
        self.create_chat_frame()
        
        # Skapa inmatningsramen
        self.create_input_frame()
        
        # Visa ett välkomstmeddelande
        self.display_bot_message(f"Välkommen till {self.chatbot.name}! Hur kan jag hjälpa dig idag?")
    
    def create_menu(self):
        """
        Skapar menyn i det grafiska gränssnittet.
        """
        menubar = tk.Menu(self.root)
        
        # Skapa en File-meny
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Rensa chathistorik", command=self.clear_chat)
        file_menu.add_separator()
        file_menu.add_command(label="Avsluta", command=self.exit_program)
        
        # Skapa en Help-meny
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Hjälp", command=self.show_help)
        help_menu.add_command(label="Om NOVA", command=self.show_about)
        
        # Lägg till menyerna på menyraden
        menubar.add_cascade(label="Arkiv", menu=file_menu)
        menubar.add_cascade(label="Hjälp", menu=help_menu)
        
        # Konfigurera root att använda menyn
        self.root.config(menu=menubar)
    
    def create_chat_frame(self):
        """
        Skapar chatrutan där meddelanden visas.
        """
        chat_frame = tk.Frame(self.root)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Skapa chattruta med rullningslist
        self.chat_area = scrolledtext.ScrolledText(
            chat_frame, 
            wrap=tk.WORD, 
            bg="#f0f0f0", 
            font=("Arial", 11)
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)  # Gör textrutan read-only
    
    def create_input_frame(self):
        """
        Skapar input-fältet och skicka-knappen.
        """
        input_frame = tk.Frame(self.root, height=50)
        input_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)
        
        # Inmatningsfält
        self.user_input = tk.Entry(input_frame, font=("Arial", 11))
        self.user_input.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=(0, 10))
        
        # Bind Enter-tangenten till send_message
        self.user_input.bind("<Return>", lambda event: self.send_message())
        
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
        Hanterar skickandet av användarens meddelande och visar svaret från chatboten.
        """
        user_message = self.user_input.get().strip()
        
        # Om användaren inte har skrivit något, gör ingenting
        if not user_message:
            return
        
        # Visa användarens meddelande i chattrutan
        self.display_user_message(user_message)
        
        # Rensa input-fältet
        self.user_input.delete(0, tk.END)
        
        # Visa "tänker"-meddelande
        self.display_thinking()
        
        # Skapa en tråd för att få svar från chatboten (för att undvika frysning av GUI)
        threading.Thread(target=self.get_bot_response, args=(user_message,), daemon=True).start()
    
    def get_bot_response(self, user_message):
        """
        Får svar från chatboten i en separat tråd.
        
        Args:
            user_message (str): Användarens meddelande
        """
        # Få svar från chatboten
        response = self.chatbot.get_response(user_message)
        
        # Ta bort "tänker"-meddelandet och visa svaret
        self.root.after(0, lambda: self.remove_thinking_and_display_response(response))
        
        # Kontrollera om användaren vill avsluta
        if self.chatbot.exit_requested:
            self.root.after(1500, self.exit_program)
    
    def remove_thinking_and_display_response(self, response):
        """
        Tar bort "tänker"-meddelandet och visar chatbotens svar.
        
        Args:
            response (str): Chatbotens svar
        """
        # Ta bort "tänker"-meddelandet om det visas
        if self.thinking_displayed and self.thinking_position:
            self.chat_area.config(state=tk.NORMAL)
            # Ta bort från start av "tänker"-meddelandet till slutet av texten
            self.chat_area.delete(self.thinking_position, tk.END)
            self.chat_area.config(state=tk.DISABLED)
            self.thinking_displayed = False
        
        # Visa chatbotens svar
        self.display_bot_message(response)
    
    def display_thinking(self):
        """
        Visar ett "tänker"-meddelande medan chatboten processar frågan.
        """
        self.chat_area.config(state=tk.NORMAL)
        # Spara positionen innan vi lägger till "tänker"-meddelandet
        self.thinking_position = self.chat_area.index(tk.END)
        self.chat_area.insert(tk.END, f"\n{self.chatbot.name} tänker...")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
        self.thinking_displayed = True
    
    def display_user_message(self, message):
        """
        Visar användarens meddelande justerat till höger i chattrutan.
        
        Args:
            message (str): Användarens meddelande
        """
        self.chat_area.config(state=tk.NORMAL)
        
        # Sätt in en tom rad
        self.chat_area.insert(tk.END, "\n")
        
        # Skapa en tagg för att sätta användarens text till höger
        self.chat_area.tag_config("right", justify="right")
        
        # Sätt in "Du: " som prefix och meddelandet, allt justerat till höger
        self.chat_area.insert(tk.END, "Du: ", "user_prefix")
        self.chat_area.insert(tk.END, message, "right")
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def display_bot_message(self, message):
        """
        Visar chatbotens meddelande i chattrutan.
        
        Args:
            message (str): Chatbotens meddelande
        """
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"\n{self.chatbot.name}: ", "bot_prefix")
        self.chat_area.insert(tk.END, message)
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def clear_chat(self):
        """
        Rensar chatrutan och visar ett nytt välkomstmeddelande.
        """
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete(1.0, tk.END)
        self.chat_area.config(state=tk.DISABLED)
        self.display_bot_message(f"Chathistoriken har rensats. Hur kan jag hjälpa dig?")
    
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
    
    def exit_program(self):
        """
        Avslutar programmet.
        """
        self.root.destroy()
    
    def run(self):
        """
        Startar det grafiska gränssnittet.
        """
        # Konfigurera några taggar för formatting av text
        self.chat_area.tag_configure("user_prefix", foreground="blue", font=("Arial", 11, "bold"))
        self.chat_area.tag_configure("bot_prefix", foreground="green", font=("Arial", 11, "bold"))
        
        # Starta huvudloopen
        self.root.mainloop()