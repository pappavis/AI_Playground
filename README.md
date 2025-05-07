# AI_Playground
Experimenteren met AI

# setup instructies
1. Installeer python in ~/venv
2. Creeer een virtualenv
3. uitvoeren
  
```bash
source ~/venv/bin/activate
pip install -r ./requirements
```

## muziekgen_small_uitprobeer.py
Dit script genereert muziek met behulp van het MusicGen-model van Facebook.
Het maakt gebruik van de transformers-bibliotheek om het model te laden en audio te genereren.
Het script accepteert een prompt via command-line argumenten en genereert een audiofragment op basis van die prompt.
Het script slaat de gegenereerde audio op als een WAV-bestand en converteert het naar MP3.
Het script maakt ook gebruik van de simpleaudio-bibliotheek om de audio af te spelen.
Ontwikkelaar: Michiel Erasmus

```bash
muziekgen_small_uitprobeer.py --help
```


## muziekgen_akkoord_spelen.py:
Dit script genereert een MIDI-bestand met een vingerpatroon op basis van een opgegeven akkoordprogressie.
 Het maakt gebruik van de music21-bibliotheek om akkoorden en noten te verwerken.
 Het script accepteert command-line argumenten voor de akkoordprogressie, maatsoort, tempo en uitvoermap.
 Het genereert een vingerpatroon en slaat het resultaat op als een MIDI-bestand in de opgegeven uitvoermap.
 Het script toont ook een tabel met het vingerpatroon en de bijbehorende noten in de melodie.


```bash
muziekgen_akkoord_spelen.py --help
```


# Nuttige dingen
## Zelf afbeeldingen renderen met teskt-naar-afbeelding
<img src="https://github.com/pappavis/AI_Playground/blob/main/COmfyUI_clip_vision_g.safetensors_sdxl_revision_zero_positive.png?raw=true" width="40%" height="40%"><br>
<a href="https://www.comfy.org">ComfyUI</a>

# AI Agents
<img src="https://github.com/pappavis/AI_Playground/blob/main/n8n_AIAgent.png?raw=true" width="80%" height="80%"><br>


# CHANGELOG: 
# 0.1.0 - Eerste versie van het script

 Ontwikkelaar: MIchiel Erasmus
 
