import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_core.tools import tool
from src.data_loader import retrieve_info

@tool
def search_university_services(query: str) -> str:
    """
    Useful for finding information about university services, office locations,
    procedures, scholarships, medical and psychological care, and sports at the Yachay Tech university.
    
    Args:
        query (str): The user's question or search term (ej: "dónde queda bienestar estudiantil").
    """
    return retrieve_info(query)


tools = [search_university_services]

if __name__ == "__main__":
    # Simulamos que el agente decide usar la herramienta
    tool = tools[0]
    print(f"Nombre de la herramienta: {tool.name}")
    print(f"Descripción: {tool.description}")
    
    # Probamos la ejecución
    resultado = tool.invoke("Dónde puedo consultar sobre becas?")
    print("\nResultado de la prueba:")
    print(resultado)