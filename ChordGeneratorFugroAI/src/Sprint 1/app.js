const AudioContext = window.AudioContext || window.webkitAudioContext;
const audioCtx = new AudioContext();

let currentNotes = [];
let oscillators = [];
let metronomeOscillator = null;
let bpm = 85;
let intervalId = null;
let currentStep = 0;
let isPlaying = false;
let recordedEvents = [];
let midiAccess = null;
let activeMidiOut = null;

const midiInputSelect = document.getElementById("midiInput");
const midiOutputSelect = document.getElementById("midiOutput");

// Initialize MIDI access
if (navigator.requestMIDIAccess) {
  navigator.requestMIDIAccess().then(success, failure);
} else {
  alert("Web MIDI not supported in this browser.");
}

function success(midi) {
  midiAccess = midi;
  updateMIDIDevices();
}

function failure() {
  console.log("Could not access your MIDI devices.");
}

function updateMIDIDevices() {
  midiInputSelect.innerHTML = "<option value=''>None</option>";
  midiOutputSelect.innerHTML = "<option value=''>None</option>";

  for (let input of midiAccess.inputs.values()) {
    let option = document.createElement("option");
    option.value = input.id;
    option.text = input.name || "Unknown MIDI Input";
    midiInputSelect.appendChild(option);
  }

  for (let output of midiAccess.outputs.values()) {
    let option = document.createElement("option");
    option.value = output.id;
    option.text = output.name || "Unknown MIDI Output";
    midiOutputSelect.appendChild(option);
  }
}

midiInputSelect.addEventListener("change", () => {
  const inputId = midiInputSelect.value;
  if (!inputId) return;
  const input = [...midiAccess.inputs.values()].find(i => i.id === inputId);
  if (input) {
    input.onmidimessage = handleMIDIMessage;
  }
});

function handleMIDIMessage(message) {
  const [status, note, velocity] = message.data;
  if ((status & 0xf0) === 0x90 && velocity > 0) {
    recordedEvents.push({ note, startTime: audioCtx.currentTime });
  } else if ((status & 0xf0) === 0x80 || ((status & 0xf0) === 0x90 && velocity === 0)) {
    const match = recordedEvents.find(e => e.note === note && !e.endTime);
    if (match) match.endTime = audioCtx.currentTime;
  }
}

function recordMIDINotes() {
  recordedEvents = [];
  alert("Recording started. Play your MIDI notes...");
}

function playMIDINotes() {
  if (!recordedEvents.length) {
    alert("No MIDI notes recorded yet.");
    return;
  }

  const sorted = recordedEvents.sort((a, b) => a.startTime - b.startTime);
  const firstTime = sorted[0].startTime;
  let now = audioCtx.currentTime;

  sorted.forEach(event => {
    const delay = event.startTime - firstTime;
    sendMIDINote(event.note, true, now + delay);
    if (event.endTime) {
      sendMIDINote(event.note, false, now + event.endTime - firstTime);
    }
  });
}

function sendMIDINote(note, on, time) {
  const outputId = midiOutputSelect.value;
  if (!outputId) return;
  const output = [...midiAccess.outputs.values()].find(o => o.id === outputId);
  if (!output) return;
  const cmd = on ? 0x90 : 0x80;
  output.send([cmd, note, on ? 127 : 0], time * 1000);
}

function startMetronomeTick() {
  if (metronomeOscillator) metronomeOscillator.stop();
  const interval = 60 / bpm;
  let tickCount = 0;

  metronomeOscillator = audioCtx.createOscillator();
  metronomeOscillator.type = "square";
  metronomeOscillator.frequency.value = 1000;
  metronomeOscillator.connect(audioCtx.destination);

  metronomeOscillator.start();

  intervalId = setInterval(() => {
    metronomeOscillator.frequency.setValueAtTime(1000, audioCtx.currentTime);
    metronomeOscillator.frequency.exponentialRampToValueAtTime(1, audioCtx.currentTime + 0.05);
    tickCount++;
  }, interval * 1000);
}

function startPlayback() {
  if (!currentNotes.length) return;
  stopPlayback();
  currentStep = 0;
  startMetronomeTick();

  intervalId = setInterval(() => {
    if (currentStep >= currentNotes.length) {
      stopPlayback();
      return;
    }
    playChord(currentNotes[currentStep]);
    currentStep++;
  }, (60 / bpm) * 1000);
}

function pausePlayback() {
  clearInterval(intervalId);
}

function stopPlayback() {
  clearInterval(intervalId);
  stopChord();
  currentStep = 0;
  if (metronomeOscillator) metronomeOscillator.stop();
}

function noteToFrequency(noteNumber) {
  return 440 * Math.pow(2, (noteNumber - 69) / 12);
}

function playChord(notes) {
  stopChord(); // Stop previous notes

  oscillators = notes.map((note) => {
    const osc = audioCtx.createOscillator();
    osc.type = "sine";
    osc.frequency.setValueAtTime(noteToFrequency(note), audioCtx.currentTime);
    osc.connect(audioCtx.destination);
    osc.start();
    return osc;
  });

  setTimeout(() => {
    stopChord();
  }, (60 / bpm) * 1000); // Duration based on BPM
}

function stopChord() {
  if (oscillators.length > 0) {
    oscillators.forEach((osc) => osc.stop());
    oscillators = [];
  }
}

function drawPianoRoll(chords) {
  const canvas = document.getElementById("pianoRollCanvas");
  const ctx = canvas.getContext("2d");

  canvas.width = canvas.clientWidth;
  canvas.height = canvas.clientHeight;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const lowestNote = 24; // C1
  const highestNote = 108; // C7
  const totalNotes = highestNote - lowestNote;
  const noteHeight = canvas.height / totalNotes;
  const barWidth = (canvas.width - 60) / chords.length;

  // Draw vertical piano
  for (let i = 0; i <= totalNotes; i++) {
    const note = highestNote - i;
    const y = i * noteHeight;
    ctx.fillStyle = (note % 12 === 0) ? "#333" : "#555";
    ctx.fillRect(0, y, 60, noteHeight);
    if (note % 12 === 0) {
      ctx.fillStyle = "#fff";
      ctx.font = "10px sans-serif";
      ctx.fillText(`C${Math.floor((note - 12) / 12)}`, 5, y + noteHeight - 5);
    }
  }

  // Draw chords
  chords.forEach((chord, index) => {
    chord.forEach((note) => {
      const y = (highestNote - note) * noteHeight;
      ctx.fillStyle = "#00ffcc";
      ctx.fillRect(60 + index * barWidth, y, barWidth, noteHeight);
    });
  });
}

function generateMockChords(key, scale, chordType, length) {
  const baseMidi = {
    C: 60,
    "C#": 61,
    D: 62,
    "D#": 63,
    E: 64,
    F: 65,
    "F#": 66,
    G: 67,
    "G#": 68,
    A: 69,
    "A#": 70,
    B: 71,
  };

  const root = baseMidi[key] || 60;

  const progressions = {
    major: [root, root + 2, root + 4, root + 5, root + 7, root + 9, root + 11],
    minor: [root, root + 2, root + 3, root + 5, root + 7, root + 8, root + 10],
    pentatonic: [root, root + 2, root + 4, root + 7, root + 9],
    harmonicMinor: [root, root + 2, root + 3, root + 5, root + 7, root + 8, root + 11],
    melodicMinor: [root, root + 2, root + 3, root + 5, root + 7, root + 9, root + 11],
  };

  const scaleNotes = progressions[scale] || progressions["major"];
  const chords = [];

  for (let i = 0; i < length; i++) {
    const randomRootIndex = Math.floor(Math.random() * scaleNotes.length);
    const chordRoot = scaleNotes[randomRootIndex];
    let chordNotes = [chordRoot];

    switch (chordType) {
      case "seventh":
        chordNotes.push(chordRoot + 4, chordRoot + 7, chordRoot + 10);
        break;
      case "augmented":
        chordNotes.push(chordRoot + 4, chordRoot + 8);
        break;
      case "diminished":
        chordNotes.push(chordRoot + 3, chordRoot + 6);
        break;
      case "suspended":
        chordNotes.push(chordRoot + 5, chordRoot + 7);
        break;
      default:
        chordNotes.push(chordRoot + 4, chordRoot + 7);
    }

    chords.push(chordNotes);
  }

  return chords;
}

function generateChords() {
  const key = document.getElementById("key").value;
  const scale = document.getElementById("scale").value;
  const chordType = document.getElementById("chordType").value;
  const length = parseInt(document.getElementById("length").value);
  bpm = parseInt(document.getElementById("bpm").value);

  const chords = generateMockChords(key, scale, chordType, length);
  currentNotes = chords;

  drawPianoRoll(chords);
}

function saveToFile() {
  const projectData = {
    bpm,
    key: document.getElementById("key").value,
    scale: document.getElementById("scale").value,
    chordType: document.getElementById("chordType").value,
    length: parseInt(document.getElementById("length").value),
    notes: currentNotes,
    recordedEvents
  };
  const blob = new Blob([JSON.stringify(projectData, null, 2)], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "project.json";
  link.click();
}

function loadFromFile() {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = ".json";
  input.onchange = async () => {
    const file = input.files[0];
    const reader = new FileReader();
    reader.onload = () => {
      const data = JSON.parse(reader.result);
      document.getElementById("key").value = data.key;
      document.getElementById("scale").value = data.scale;
      document.getElementById("chordType").value = data.chordType;
      document.getElementById("length").value = data.length;
      document.getElementById("bpm").value = data.bpm;
      currentNotes = data.notes;
      recordedEvents = data.recordedEvents || [];
      drawPianoRoll(data.notes);
    };
    reader.readAsText(file);
  };
  input.click();
}