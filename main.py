"""
Huvudfil för Nova chatbot.
"""

from nova.chatbot import Nova
from ui.interface import GraphicalInterface

def main():
    """
    Huvudfunktion som startar Nova chatbot.
    """
    # Skapa en instans av Nova chatbot
    nova = Nova()
    
    # Skapa och starta det grafiska gränssnittet
    interface = GraphicalInterface(nova)
    interface.run()

if __name__ == "__main__":
    main()