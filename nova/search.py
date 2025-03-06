"""
Modul för webbsökningsfunktioner i Nova chatbot.
"""

import requests
from urllib.parse import quote_plus
import re

class WebSearch:
    """
    Hanterar webbsökningar för Nova chatbot.
    """
    
    def __init__(self):
        """
        Initierar WebSearch.
        """
        self.search_url = "https://www.google.com/search?q="
        self.user_agent = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
    
    def search(self, query):
        """
        Utför en webbsökning och returnerar ett enkelt resultat.
        
        Args:
            query (str): Sökfrågan
            
        Returns:
            str: Sökresultatet eller ett felmeddelande
        """
        try:
            # Formatera söksträngen och skapa URL
            search_term = quote_plus(query)
            url = f"{self.search_url}{search_term}"
            
            # Skicka HTTP-förfrågan
            response = requests.get(url, headers=self.user_agent, timeout=5)
            
            # Kontrollera om förfrågan lyckades
            if response.status_code == 200:
                # Extrahera resultat (en enkel version)
                result = self._extract_search_result(response.text)
                
                if result:
                    return f"Här är vad jag hittade om '{query}':\n\n{result}"
                else:
                    return f"Jag sökte på '{query}' men kunde inte hitta ett tydligt svar."
            else:
                return "Tyvärr, jag kunde inte genomföra sökningen just nu."
                
        except Exception as e:
            print(f"Sökfel: {e}")
            return "Jag kunde inte genomföra sökningen på grund av ett fel."
    
    def _extract_search_result(self, html_content):
        """
        Extraherar det första relevanta resultatet från HTML-innehållet.
        Detta är en enkel implementation som kan behöva förbättras.
        
        Args:
            html_content (str): HTML-innehållet från sökningen
            
        Returns:
            str: Extraherad information eller tom sträng om inget hittades
        """
        # Enkel metod för att extrahera "featured snippet" från Google
        # Obs: Detta är en enkel implementation som kan behöva justeras
        try:
            # Försök hitta en "featured snippet" eller annan resultatruta
            pattern = r'<div class="[^"]*BNeawe[^"]*">(.*?)</div>'
            matches = re.findall(pattern, html_content)
            
            if matches:
                # Ta de första 2-3 resultaten och rensa från HTML-taggar
                results = [re.sub(r'<[^>]+>', '', match) for match in matches[:3]]
                
                # Filtrera bort tomma eller för korta resultat
                filtered_results = [r for r in results if len(r) > 20]
                
                if filtered_results:
                    # Returnera det längsta resultatet (troligen mest informativt)
                    return max(filtered_results, key=len)
            
            return ""
        except Exception as e:
            print(f"Extraktionsfel: {e}")
            return ""