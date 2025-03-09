# **NOVA: Neural Operating Virtual Assistant**

NOVA är en enkel chatbot och virtuell assistent byggd i Python som kombinerar textbaserad och röststyrd interaktion.

## Beskrivning

NOVA är en Enkel Chatbot i Python en virtuell assistent utformad för att hjälpa användare med olika uppgifter genom både text- och röstkommandon. Projektet ska utvecklas vidare från en enkel till en mer avancerad textbaserad chatbot till en mer avancerad assistent med röstaktivering och fler funktioner.

## Nuvarande Funktioner

- **Dual Interface**: Både text- och röstbaserad interaktion
- **Röstaktivering**: Starta röstläge genom röstkommandon
- **Röststyrning**: Diktera meddelanden och ge kommandon via tal
- **Visuell Feedback**: Indikator som visar när NOVA lyssnar
- **Tärningsslag**: Simulera tärningsslag med olika antal sidor
- **Webbsökning**: Hämta information från nätet vid specifika frågor
- **Minnesfunktion**: Kommer ihåg konversationer inom en session
- **Systemkommandon**: Starta program, utföra beräkningar, m.m.

## Teknisk Stack

- **Språk**: Python 3.x
- **Bibliotek**:
  - `speech_recognition` för röstinmatning
  - `pyttsx3` för text-till-tal
  - `tkinter` för grafiskt gränssnitt
  - `threading` för parallella operationer
  - `nltk` för enkel textbehandling
  - `requests` för webbsökningar

## Användning

När du har startat NOVA, kan du interagera med assistenten genom:

1. **Text**: Skriv ditt meddelande i inmatningsfältet
2. **Röst**: Aktivera röstläge med knappen eller genom att säga "Hej Nova"

### Exempel på kommandon:
- "Hej" för en hälsning
- "Vad kan du göra?" för att se tillgängliga funktioner
- "Slå en tärning" för att simulera ett tärningsslag
- "Sök på [ämne]" för att göra en webbsökning
- "Öppna [program]" för att starta ett program
- "Avsluta" för att stänga programmet

## Visuell Feedback
- **Rund indikator**: Visar när NOVA lyssnar (röd), väntar på nyckelord (blå) eller är redo (grå)
- **Statustext**: Visar assistentens aktuella tillstånd

## Framtida Utveckling

- **Utökad NLP**: Bättre förståelse av naturligt språk
- **Personalisering**: Anpassa assistenten efter användarens behov
- **API-integration**: Koppla till fler tjänster och plattformar
- **Mer avancerad AI**: Implementera modernare språkmodeller
- **Kalenderhantering**: Lägga till och påminna om händelser

## Bidra

Bidrag till projektet är välkomna! För att bidra:
- Forka repositoryt
- Skapa en feature branch
- Gör dina ändringar
- Skicka en pull request

## Licens

Detta projekt är licensierat under MIT-licensen.

---

NOVA - Din personliga virtuella assistent med röst och text