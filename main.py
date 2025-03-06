"""
Huvudfil för Nova chatbot.
"""

import argparse
from nova.chatbot import Nova
from ui.text_interface import TextInterface
from ui.interface import GraphicalInterface

def main():
    """
    Huvudfunktion som startar Nova chatbot.
    """
    # Skapa en kommandoradsparser
    parser = argparse.ArgumentParser(description='NOVA Chatbot')
    parser.add_argument('--text', action='store_true', help='Använd textbaserat gränssnitt istället för GUI')
    args = parser.parse_args()
    
    # Skapa en instans av Nova chatbot
    nova = Nova()
    
    # Välj gränssnitt baserat på kommandoradsargument
    if args.text:
        # Använd textgränssnitt
        interface = TextInterface(nova)
    else:
        # Använd grafiskt gränssnitt
        interface = GraphicalInterface(nova)
    
    # Starta valt gränssnitt
    interface.run()

if __name__ == "__main__":
    main()