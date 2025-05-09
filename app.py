

import streamlit as st
import speech_recognition as sr
import os
from datetime import datetime

# Fonction de transcription vocale
def transcribe_speech(api_choice, language, is_paused):
    if is_paused:
        return "⏸️ Reconnaissance en pause."

    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        st.info("🎙️ Parlez maintenant...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)

            if api_choice == "Google":
                text = recognizer.recognize_google(audio, language=language)
            elif api_choice == "Sphinx":
                text = recognizer.recognize_sphinx(audio, language=language)
            else:
                return "❌ API non prise en charge."

            return text

        except sr.WaitTimeoutError:
            return "⏰ Délai dépassé. Aucun son détecté."
        except sr.UnknownValueError:
            return "❓ Impossible de comprendre l'audio."
        except sr.RequestError as e:
            return f"⚠️ Erreur de l'API : {e}"
        except Exception as e:
            return f"❌ Erreur inattendue : {str(e)}"

# Fonction de sauvegarde
def save_transcription(text):
    filename = f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(os.getcwd(), filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    return filepath

# Interface utilisateur Streamlit
def main():
    st.title("🗣️ Amélioration de l'App de Reconnaissance Vocale")

    st.markdown("""
    ### Instructions :
    - Choisissez une API de reconnaissance vocale.
    - Sélectionnez votre langue.
    - Cliquez sur "Écouter".
    - Optionnel : Sauvegardez le texte transcrit.
    """)

    api_choice = st.selectbox("Sélectionnez l'API", ["Google", "Sphinx"])
    language = st.text_input("Langue (ex: 'fr-FR' pour français, 'en-US' pour anglais)", "fr-FR")

    pause = st.checkbox("⏸️ Mettre en pause la reconnaissance")

    if st.button("🎧 Écouter"):
        result = transcribe_speech(api_choice, language, pause)
        st.text_area("📝 Transcription :", result, height=100)

        if result and "Impossible" not in result and "Erreur" not in result:
            if st.button("💾 Sauvegarder la transcription"):
                path = save_transcription(result)
                st.success(f"✅ Transcription sauvegardée : {path}")

if __name__ == "__main__":
    main()
