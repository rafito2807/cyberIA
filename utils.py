import pyttsx3
import tempfile
import os

def text_to_speech(text):
    try:
        engine = pyttsx3.init()
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, "output.mp3")
        engine.save_to_file(text, file_path)
        engine.runAndWait()
        # Aquí deberías subir el audio a un servidor público y retornar el enlace
        return None  # O reemplaza con el URL final si tienes hosting
    except Exception as e:
        print("Error generando audio:", e)
        return None
