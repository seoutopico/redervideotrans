import streamlit as st
from moviepy.editor import VideoFileClip
import whisper
import tempfile
import os

st.set_page_config(
    page_title="Video Transcriber",
    page_icon="🎥",
    layout="centered"
)

# Configurar caché para el modelo
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

def extract_audio(video_path, output_path):
    """Extrae el audio de un video y lo guarda como archivo temporal"""
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(output_path, verbose=False, logger=None)
    video.close()
    audio.close()

def transcribe_audio(audio_path, model):
    """Transcribe el audio usando whisper"""
    result = model.transcribe(audio_path)
    return result["text"]

def main():
    st.title("📽️ Transcriptor de Videos")
    st.write("Sube un video para obtener su transcripción")
    
    # Cargar modelo al inicio
    model = load_whisper_model()
    
    # Configurar límite de tamaño (50MB)
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB en bytes
    
    # Widget para subir archivo
    video_file = st.file_uploader("Sube tu video (máximo 50MB)", type=['mp4', 'avi', 'mov'])
    
    if video_file:
        # Verificar tamaño del archivo
        if video_file.size > MAX_FILE_SIZE:
            st.error("El archivo es demasiado grande. Por favor, sube un video de menos de 50MB.")
            return
            
        try:
            # Crear directorio temporal para procesar archivos
            with tempfile.TemporaryDirectory() as temp_dir:
                # Guardar video subido
                video_path = os.path.join(temp_dir, "temp_video.mp4")
                with open(video_path, "wb") as f:
                    f.write(video_file.read())
                
                # Mostrar mensaje de procesamiento
                with st.spinner("Procesando video... Por favor espera."):
                    # Extraer y guardar audio
                    audio_path = os.path.join(temp_dir, "temp_audio.wav")
                    extract_audio(video_path, audio_path)
                    
                    # Transcribir audio
                    transcription = transcribe_audio(audio_path, model)
                
                # Mostrar resultados
                st.success("¡Transcripción completada!")
                st.write("### Transcripción:")
                st.write(transcription)
                
                # Opción para descargar transcripción
                st.download_button(
                    label="Descargar transcripción",
                    data=transcription,
                    file_name="transcripcion.txt",
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f"Error durante el procesamiento: {str(e)}")
            st.write("Por favor, intenta con un video más corto o en otro formato.")

if __name__ == "__main__":
    main()
