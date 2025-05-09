# pip install opencv-python streamlit

import streamlit as st
import cv2
import numpy as np
import tempfile
import os
from datetime import datetime


def detect_face(scale_factor, min_neighbors, rect_color):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)

    frame_placeholder = st.empty()

    st.write("Appuyez sur 'q' dans la fenêtre caméra pour quitter la détection.")

    while True:
        ret, frame = cap.read()

        if not ret:
            st.error('Échec de la détection.')
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Détection des visages
        faces = face_cascade.detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=min_neighbors)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), rect_color, 2)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame_placeholder.image(frame_rgb, channels='RGB', use_container_width=True)

        # Attente clavier pour sortir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Sauvegarde image avec visages
            save_path = os.path.join(tempfile.gettempdir(), f"detected_faces_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
            cv2.imwrite(save_path, frame)
            st.success(f"L'image a été sauvegardée ici : {save_path}")
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    st.title('🧠 Face Recognition App')

    st.markdown("""
    ### Instructions :
    1. Cliquez sur **'Détecter les visages'** pour activer la webcam.
    2. Ajustez les paramètres `scaleFactor` et `minNeighbors` pour affiner la détection.
    3. Choisissez la couleur du rectangle autour des visages.
    4. Appuyez sur **'q'** dans la fenêtre de la webcam pour arrêter et enregistrer l'image.
    """)

    # Paramètres utilisateurs
    scale_factor = st.slider('Ajuster scaleFactor (plus bas = plus sensible)', 1.05, 1.5, 1.1, step=0.01)
    min_neighbors = st.slider('Ajuster minNeighbors (plus haut = moins de détections)', 1, 10, 5)

    # Choix couleur
    color_hex = st.color_picker("Choisissez la couleur du rectangle", "#00FF00")
    rect_color = tuple(int(color_hex.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))  # hex to BGR tuple

    if st.button('Détecter les visages'):
        detect_face(scale_factor, min_neighbors, rect_color)


if __name__ == "__main__":
    main()
