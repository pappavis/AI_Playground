# Dit script genereert een MIDI-bestand met een vingerpatroon op basis van een opgegeven akkoordprogressie.
# Het maakt gebruik van de music21-bibliotheek om akkoorden en noten te verwerken.
# Het script accepteert command-line argumenten voor de akkoordprogressie, maatsoort, tempo en uitvoermap.
# Het genereert een vingerpatroon en slaat het resultaat op als een MIDI-bestand in de opgegeven uitvoermap.
# Het script toont ook een tabel met het vingerpatroon en de bijbehorende noten in de melodie.
# CHANGELOG: 
# 0.1.0 - Eerste versie van het script

# Ontwikkelaar: MIchiel Erasmus

import tabulate
import music21
from uuid import uuid4
import os
import sys

# Standaardwaarden
default_chord_progression = 'D3 A3 B3 F3 G3'
akkoord_uuid = str(uuid4()).replace("-", "")  # UUID zonder streepjes
default_out_dir = f'/Volumes/data1/AI_Gerelateerd/github/AI_Playground/speelplek/Muziek_Genereer/out/akkoord_spelen/{akkoord_uuid}'

# Functie om help-informatie te tonen
def print_help():
    print("Gebruik:")
    print("  python muziekgen_akkoord_spelen.py [opties]")
    print("\nOpties:")
    print("  --chord_progression   Specificeer een akkoordprogressie (bijv. 'D3 A3 Bmin F3 G3').")
    print("  --time_signature      default bijvb '4/4'")
    print("  --bpm                 default bijvb 106")
    print("  --out_dir             Specificeer de uitvoermap.")
    print("  --help                Toon deze help-informatie.")
    exit(0)

# Verwerk command-line argumenten
chord_progression = default_chord_progression
out_dir = default_out_dir
time_signature_ts = '4/4'  # Standaard maatsoort
tempo_bpm = 60


for i, arg in enumerate(sys.argv):
    if arg == "--help":
        print_help()
    elif arg == "--chord_progression" and i + 1 < len(sys.argv):
        chord_progression = sys.argv[i + 1]
    elif arg == "--out_dir" and i + 1 < len(sys.argv):
        out_dir = sys.argv[i + 1]
    elif arg == "--time_signature" and i + 1 < len(sys.argv):
        time_signature_ts = sys.argv[i + 1]
    elif arg == "--bpm" and i + 1 < len(sys.argv):
        tempo_bpm = sys.argv[i + 1]

# Parse the chord progression into a list of Chord objects
try:
    chords = [music21.chord.Chord(chord) for chord in chord_progression.split()]
except Exception as e:
    print(f"Fout bij het parsen van de akkoordprogressie: {e}")
    exit(1)

# Bereken de vingerpatroon op basis van de maatsoort (4/4) en tempo (60 bpm)
time_signature = music21.meter.TimeSignature(time_signature_ts)

# Maak een MetronomeMark-object aan voor visualisatie
metronome = music21.tempo.MetronomeMark(number=tempo_bpm)

# Initialiseer een lege lijst om de noten in de melodie op te slaan
melody_notes = []

# Itereer door elke beat in het lied en bepaal welke noten moeten worden toegevoegd op basis van de akkoordprogressie
for i in range(len(chords) * 4):
    # Bereken de huidige maat en beat op basis van de loopindex
    measure = int(i / 4) + 1
    beat = (i % 4) + 1

    # Haal het huidige akkoord op
    current_chord = chords[(measure - 1) % len(chords)]

    # Voeg een noot uit het huidige akkoord toe aan de melodie
    if beat == 1 or beat == 3:  # Voorbeeld vingerpatroon
        melody_notes.append(music21.note.Note(current_chord.root(), quarterLength=1))

# Maak een Stream-object aan om het hele lied op te slaan
song = music21.stream.Stream()

# Voeg de maatsoort, metronoommarkering en melodienoten toe aan de stream
song.append(time_signature)
song.append(metronome)
for note in melody_notes:
    song.append(note)

# Controleer of de uitvoermap bestaat, anders maak deze aan
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# Sla het lied op als een MIDI-bestand
output_file = f'{out_dir}/fingerpicking_pattern.mid'
song.write('midi', fp=output_file)
print(f"\n/{akkoord_uuid} Song opgeslagen in {output_file}")

# Print een tabel met het vingerpatroon en de bijbehorende noten in de melodie
print(tabulate.tabulate([['Beat', 'Fingerpicking', 'Guitar Note']] +
                        [[i + 1, 'x' if (i % 4) in [0, 2] else '', str(chords[i // 4 % len(chords)].root())]
                         for i in range(len(chords) * 4)],
                        headers='firstrow', tablefmt="grid"))
