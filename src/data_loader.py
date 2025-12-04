import os
import pandas as pd
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "Grid Public.csv")
PERSIST_DIRECTORY = os.path.join(BASE_DIR, "..", "chroma_db")

def get_vector_store():
    embedding_function = OllamaEmbeddings(model="nomic-embed-text")

    if os.path.exists(PERSIST_DIRECTORY) and os.listdir(PERSIST_DIRECTORY):
        print("Cargando base de datos existente...")
        return Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embedding_function)

    print("Creando base de datos vectorial desde cero...")
    
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"No se encuentra el archivo CSV en: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    documents = []

    for _, row in df.iterrows():
        servicio = row['Servicio'] if pd.notna(row['Servicio']) else "Servicio General"
        ubicacion = row['Centro de Atención'] if pd.notna(row['Centro de Atención']) else "No especificada"
        modalidad = row['Modalidad'] if pd.notna(row['Modalidad']) else "Presencial/Virtual"
        link = row['Link'] if pd.notna(row['Link']) else "No disponible"

        page_content = f"Servicio: {servicio}. Ubicación: {ubicacion}. Modalidad: {modalidad}."
        
        metadata = {
            "servicio": servicio,
            "ubicacion": ubicacion,
            "modalidad": modalidad,
            "link": link
        }
        documents.append(Document(page_content=page_content, metadata=metadata))

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_function,
        persist_directory=PERSIST_DIRECTORY
    )
    print("Base de datos guardada exitosamente.")
    return vector_store

def retrieve_info(query: str):
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query, k=3)
    
    context_text = ""
    for doc in results:
        context_text += f"- Servicio: {doc.metadata['servicio']}\n"
        context_text += f"  Ubicación: {doc.metadata['ubicacion']}\n"
        context_text += f"  Link: {doc.metadata['link']}\n\n"
    
    return context_text

if __name__ == "__main__":
    print("Probando el Data Loader...")
    pregunta = "Donde puedo consultar sobre las residencias universitarias?"
    respuesta = retrieve_info(pregunta)
    print(f"\nPregunta: {pregunta}")
    print(f"Resultados encontrados:\n{respuesta}")