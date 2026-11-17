import os
import pygame
import asyncio
import tempfile
import edge_tts

VOICE = "en-IN-PrabhatNeural"

def _play_audio(file_path):
    """Play an MP3 file using pygame and clean up afterwards."""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        pygame.mixer.quit()
        try:
            os.remove(file_path)
        except OSError:
            pass

async def _generate_speech(text, output_path):
    """Generate speech audio file from text using Edge TTS."""
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_path)

def speak(text):
    """Convert text to speech using Edge TTS (Indian voice) and play it aloud.
    
    This function is synchronous and blocks until the speech finishes playing.
    Safe to call from any thread.
    """
    if not text or not text.strip():
        return
    try:
        fd, temp_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)
        # asyncio.run() creates a fresh event loop each time — safe from any thread
        asyncio.run(_generate_speech(text, temp_path))
        _play_audio(temp_path)
    except Exception as e:
        print(f"[VoiceTTS] Error: {e}")

if __name__ == "__main__":
    speak("Hello, this is a test of the Indian Edge TTS module.")
