import streamlit as st
import pandas as pd
from openai import OpenAI

# Configuración de la página
st.set_page_config(page_title="Chatbot de Matemáticas Financieras", page_icon="💬")

st.title("💬 Chatbot de Matemáticas Financieras")
st.markdown("Consulta sobre anualidades, valor presente, tasa de interés, etc. y evalúa la respuesta del bot.")

# Inicializar historial y feedback
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Clave API desde .streamlit/secrets.toml
openai_api_key = st.secrets["api_key"]
client = OpenAI(api_key=openai_api_key)

# Entrada del usuario
prompt = st.chat_input("Escribe tu duda de matemáticas financieras...")

if prompt:
    # Mostrar entrada del usuario
    with st.chat_message("user", avatar="🦖"):
        st.markdown(prompt)

    # Mensaje del sistema
    system_message = {
        "role": "system",
        "content": (
            "Eres un profesor universitario experto en Matemáticas Financieras. "
            "Especialista en anualidades ordinarias, valor presente, valor futuro, número de periodos y tasa de interés. "
            "Explica paso a paso y responde dudas como si hablaras con estudiantes."
        )
    }

    try:
        # Solicitud al modelo
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[system_message, {"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.3
        )
        respuesta = response.choices[0].message.content

        # Mostrar respuesta del bot
        with st.chat_message("assistant", avatar="🧑‍🏫"):
            st.markdown(respuesta)

        # Agregar entrada temporal al historial (feedback vacío inicialmente)
        st.session_state.chat_history.append({
            "Pregunta": prompt,
            "Respuesta": respuesta,
            "¿Fue útil?": ""
        })

    except Exception as e:
        st.error(f"Error en la respuesta del modelo: {e}")

# Mostrar tabla de historial + evaluación
if st.session_state.chat_history:
    st.markdown("### 🗃️ Historial de Preguntas y Evaluaciones")

    for i, row in enumerate(st.session_state.chat_history):
        with st.expander(f"📝 Pregunta {i + 1}"):
            st.markdown(f"**Pregunta:** {row['Pregunta']}")
            st.markdown(f"**Respuesta:** {row['Respuesta']}")
            if row["¿Fue útil?"] == "":
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ Sí (útil)", key=f"yes_{i}"):
                        st.session_state.chat_history[i]["¿Fue útil?"] = "Sí"
                with col2:
                    if st.button(f"❌ No (no fue útil)", key=f"no_{i}"):
                        st.session_state.chat_history[i]["¿Fue útil?"] = "No"
            else:
                st.markdown(f"**¿La respuesta fue útil?** {row['¿Fue útil?']}")

    # Convertir a DataFrame y mostrar como tabla
    df = pd.DataFrame(st.session_state.chat_history)
    st.dataframe(df, use_container_width=True)
