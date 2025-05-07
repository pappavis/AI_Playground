from transformers import AutoTokenizer, MusicgenForConditionalGeneration
import torch
import numpy as np
from scipy.io.wavfile import write
from uuid import uuid4
from pydub import AudioSegment  # Voor MP3-conversie
import os
import sys  # Voor het verwerken van command-line argumenten
import json

# Dit script genereert muziek met behulp van het MusicGen-model van Facebook.
# Het maakt gebruik van de transformers-bibliotheek om het model te laden en audio te genereren.
# Het script accepteert een prompt via command-line argumenten en genereert een audiofragment op basis van die prompt.
# Het script slaat de gegenereerde audio op als een WAV-bestand en converteert het naar MP3.
# Het script maakt ook gebruik van de simpleaudio-bibliotheek om de audio af te spelen.
# Ontwikkelaar: Michiel Erasmus

# CHANGELOG:
# 0.1.0 - Eerste versie van het script


class muziekgenMichiel:
    def __init__(self, initModel=True):
        self.liedje_uuid = str(uuid4()).replace("-", "")  # UUID zonder streepjes
        self.liedje_lengte = 10  # Lengte van het liedje in seconden
        self.liedje_fadeout_start = 8  # Starttijd van de fade-out in seconden
        self.default_prompt = f'A light and cheerly campfire acoustic guitar radio jingle, with gentle cajon beats 8beat3, Chord progression C G C Am C Am F G, fingerpicking acoustic guitar, and strong emotions bpm: 66, song length {self.liedje_lengte} seconds, quick fade out after {self.liedje_fadeout_start} seconds'
        self.tokenizer = None
        self.modelArr = ['facebook/musicgen-small', 'Xenova/musicgen-small']
        self.modelName = self.modelArr[0]  # Kies het model dat je wilt gebruiken
        self.model = None
        self.out_dir = f'/Volumes/data1/AI_Gerelateerd/github/AI_Playground/speelplek/Muziek_Genereer/out/liedje_gen/{self.liedje_uuid }'

        if(initModel):
            self.init_model()


    def init_model(self):
        # Forceer het downloaden van het model
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.modelName, force_download=False)
            self.model = MusicgenForConditionalGeneration.from_pretrained(self.modelName, torch_dtype=torch.float32, force_download=False)
        except OSError as e:
            print(f"Fout bij het laden van het model: {e}")
            exit(1)


    def run(self):
        # Controleer of er een command-line argument '--prompt' is meegegeven
        liedje_prompt = self.default_prompt  # Standaard prompt
        for i, arg in enumerate(sys.argv):
            if arg == "--prompt" and i + 1 < len(sys.argv):
                liedje_prompt = sys.argv[i + 1]  # Gebruik de waarde na '--prompt'
                print(f"Command-line prompt gedetecteerd: {liedje_prompt}")
                break
        else:
            print(f"Geen '--prompt' argument gedetecteerd. Standaard prompt wordt gebruikt: {liedje_prompt}")


        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

        # Schrijf de prompt naar een tekstbestand
        outPromptLoggerFile = f'{self.out_dir}/musicgenMichiel_{self.liedje_uuid}.json'
        try:
            liedje_promptJSON =  {
                "prompt": liedje_prompt,
                "length": self.liedje_lengte,
                "fadeout_start": self.liedje_fadeout_start,
                "sampling_rate": self.model.config.audio_encoder.sampling_rate,
                "model": "facebook/musicgen-small",
                "model_type": "MusicgenForConditionalGeneration",
                "model_config": self.model.config.to_dict(),
                "out_dir": self.out_dir,
                "outPromptLoggerFile": outPromptLoggerFile,
                "outUUID": self.liedje_uuid,
                "outFile": f'{self.out_dir}/musicgenMichiel_{self.liedje_uuid}.wav',
                "mp3File": f'{self.out_dir}/musicgenMichiel_{self.liedje_uuid}.mp3',
                "audio_channels": self.model.config.audio_encoder.audio_channels
            }
            # Controleer of het bestand al bestaat
            with open(outPromptLoggerFile, 'w') as f:                    
                json.dump(liedje_promptJSON, f, indent=4)
                f.close()
        except Exception as e:  
            print(f"Fout bij het opslaan van de prompt: {e}")
            exit(1)
    
        print(f"Prompt succesvol opgeslagen in '{outPromptLoggerFile}'")
        # Print de prompt
        print(f"Prompt: {liedje_prompt}")
        # Tokenizer invoer voorbereiden
        inputs = self.tokenizer(liedje_prompt, return_tensors="pt")
        print("")
        # Genereren van audio
        audio_values = self.model.generate(
            **inputs,
            max_new_tokens=500,
            do_sample=True,
            guidance_scale=3,
        )

        # Sampling rate ophalen uit de modelconfiguratie
        sampling_rate = self.model.config.audio_encoder.sampling_rate

        # Audio opslaan als een WAV-bestand
        outUUID = self.liedje_uuid
        audio_array = audio_values.cpu().numpy()
        audio_array = np.int16(audio_array / np.max(np.abs(audio_array)) * 32767)  # Normaliseren naar 16-bit PCM

        # Pad voor het WAV-bestand
        outFile = f'{self.out_dir}/musicgenMichiel_{outUUID}.wav'

        # Audio opslaan als WAV-bestand
        try:
            write(outFile, sampling_rate, audio_array)
        except Exception as e:
            print(f"Fout bij het opslaan van audio: {e}")
            exit(1)
        print(f"Audio succesvol gegenereerd en opgeslagen als '{outFile}'")

        # Converteer WAV naar MP3
        try:
            mp3File = f'{self.out_dir}/musicgenMichiel_{outUUID}.mp3'
            audio = AudioSegment.from_wav(outFile)
            audio.export(mp3File, format="mp3")
            print(f"Audio succesvol geconverteerd naar MP3 en opgeslagen als '{mp3File}'")
        except Exception as e:
            print(f"Fout bij het converteren naar MP3: {e}")

        print("")
        # Audio afspelen
        try:
            import simpleaudio as sa
            
            # Get audio parameters from model config
            num_channels = 1  # From model config audio_channels
            bytes_per_sample = 2  # For 16-bit audio
            
            # Convert NumPy array to bytes in the correct format for simpleaudio
            # Ensure it's in the right shape (samples, channels)
            if len(audio_array.shape) == 1:
                # If mono, reshape to (samples, 1)
                audio_data = audio_array.reshape(-1, 1)
            else:
                audio_data = audio_array
                
            # Make sure data is in int16 format and convert to bytes
            audio_bytes = audio_data.astype(np.int16).tobytes()
            
            # Play the audio
            print(f"Audio wordt afgespeeld...")
            play_obj = sa.play_buffer(audio_bytes, num_channels, bytes_per_sample, sampling_rate)
            
            # Wait for playback to finish
            play_obj.wait_done()
            
            print("Audio is succesvol afgespeeld.")
            print("")
            print("Audio is succesvol opgeslagen en afgespeeld.")
        except ImportError:
            print("simpleaudio is niet geïnstalleerd. Audio kan niet worden afgespeeld.")
        except Exception as e:
            print(f"Fout bij het afspelen van audio: {e}")

if __name__ == "__main__":
    # Maak een instantie van de muziekgenMichiel klasse
    muziekgen = muziekgenMichiel(initModel=True)

    # Start het genereren van muziek
    print("Muziekgeneratie gestart...")
    muziekgen.run()

    # Einde van de muziekgeneratie
    print("Muziekgeneratie voltooid.")
    # Einde van de klasse

    # Einde van het script
    print("Einde van het script.")

