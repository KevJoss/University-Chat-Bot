import streamlit as st
from src.graph import app as graph_app

st.set_page_config(
    page_title="Yachay AI Assistant",
    page_icon="🎓",
    layout="centered"
)

st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Asistente Virtual Yachay")
st.markdown("Pregunta sobre servicios, ubicaciones y modalidades de la universidad.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Lógica del Chat ---
if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    # 1. Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generar respuesta usando el GRAFO
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("Procesando tu solicitud..."):
            try:
                # Preparamos el input para el grafo
                inputs = {"question": prompt}
                
                # Invocamos el grafo. 
                # Esto ejecutará: Router -> (Search -> Generate) O (Chat)
                result = graph_app.invoke(inputs)
                
                final_answer = result.get("answer", "Lo siento, no pude generar una respuesta.")
                
                # Mostramos la respuesta final
                message_placeholder.markdown(final_answer)
                
                # Opcional: Mostrar detalles de depuración (Categoría y Contexto)
                # Esto es útil para ver si el Router eligió SEARCH o CHAT
                category = result.get("category", "Desconocida")
                
                if "context" in result and result["context"]:
                    with st.expander(f"Fuentes consultadas (Modo: {category})"):
                        st.text(result["context"])
                else:
                    # Si es modo CHAT, no suele haber contexto de base de datos
                    with st.expander(f"Información del sistema (Modo: {category})"):
                        st.info("Respuesta generada en modo conversación general (sin búsqueda en BD).")

                # 3. Guardar respuesta en historial
                st.session_state.messages.append({"role": "assistant", "content": final_answer})

            except Exception as e:
                st.error(f"Ocurrió un error al procesar la solicitud: {e}")