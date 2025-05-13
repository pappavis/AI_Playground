# AI chord generator  -- WORK in progress!!! 
Versie: 0.0.1

## Requirements
A frontend interface for a musical chord generator. Here’s a detailed breakdown of the tasks and requirements:
<br>
<img src="https://github.com/pappavis/AI_Playground/blob/main/ChordGeneratorFugroAI/img/Scaler3A_%20Chord_Generator_Clone.png?raw=true" width="30%" hight="30%" alt="AI Chord generator">
<br>


### User Interface

#### Sidebar
- **Dropdowns for:**
  - **Key:** Options include C, C#, D, ..., B.
  - **Scale:** Options include major, minor, pentatonic, etc.
  - **Chord Type:** Options include triad, seventh, augmented, etc.
- **Number input for progression length:** Range from 1 to 16 bars.
- **BPM input:** Default set to 85 BPM.
- **Time signature selection:** Options include 3/4, 4/4, etc.

#### Main Area
- **Canvas element for piano roll visualization.**
- **Playback controls:** Buttons for Play, Pause, and Stop.
- **Virtual piano:** Aligned vertically with MIDI notes on the left side of the piano roll view.
- **Buttons for:**
  - Record MIDI Notes (from external devices like BOSS GM-800).
  - Play MIDI Notes (to external devices like Arturia Minifreak).
  - Save MIDI Notes or settings to JSON file.
  - Load MIDI Notes or settings from JSON file.

### JavaScript Logic
- **Event listeners:** Attach to all inputs and buttons.
- **Mock function:** Generates dummy MIDI notes as if from an AI model.
- **Render generated chords:** Display on the piano roll canvas.
- **Web Audio API:** Play simple sine-wave tones when “Play” is clicked.
- **Metronome:** Start ticking at the set BPM when playback starts.

### Responsive Design
- **Layout:** Ensure it works well on both desktop and mobile devices.
- **CSS Flexbox or Grid:** Use for layout structure.

### File Structure
```
frontend/
│
├── index.html # Main HTML page
├── styles.css # Styling for the app
└── app.js # JavaScript logic
```

### Acceptance Criteria
- User can select key, scale, and chord type.
- User can set progression length (1–16 bars).
- Clicking "Generate Chords" triggers a function and displays output.
- Piano roll draws rectangles representing notes over time.
- Play/Pause/Stop buttons control audio playback of generated chords.
- No backend calls are made yet; all data is mocked.
- All code must run locally without external dependencies.

### Testing Plan
- **Manual testing:** Ensure UI responsiveness and interaction.
- **Edge cases:** Handle invalid input gracefully.
- **Cross-browser compatibility:** Test on Chrome, Firefox, and Safari.
- **Mobile view:** Ensure it works correctly.

### Tools & Technologies
- **VS Code:** IDE for development.
- **Live Server Extension:** For local testing.
- **Git:** Version control (commit early and often).
- **Browser DevTools:** Debugging JavaScript and layout issues.

### Deliverables
- Fully functional `index.html`, `styles.css`, and `app.js` files.
- Demo-ready build that runs locally.
- `README.md` explaining how to run and test the frontend.
- Optional: Unit tests for core functions (e.g., chord drawing logic).

This should give you a clear roadmap for developing the frontend interface for your musical chord generator.


#  Prompt  using <a herf="https://chat.qwen.ai/" target="_blank">https://chat.qwen.ai/</a>
As a web developer, your task is to build the frontend interface that allows users to:<br>

Select musical parameters (key, scale, chord type)<br>
Set progression length (number of bars)<br>
Generate chords using mock functionality<br>
View results in a piano roll canvas<br>
Play, pause, and stop playback using Web Audio API<br>

## 📋 Requirements
### User Interface
Create a responsive layout with two main sections:<br>
<br>
Sidebar<br>
Dropdowns for:<br>
Key (C, C#, D, ..., B)<br>
Scale (major, minor, pentatonic, etc.)<br>
Chord Type (triad, seventh, augmented, etc.)<br>
Number input for progression length (1–16 bars)<br>
BPM input (default: 85 BPM)<br>
Time signature selection (e.g., 3/4, 4/4)
<br><br>Main Area<br>
Canvas element for piano roll visualization<br>
Playback controls (Play, Pause, Stop)<br>
Virtual piano aligned vertically with MIDI notes on the left side of the piano roll view<br>
<br><br>Buttons for:<br>
Record MIDI Notes (from external devices like BOSS GM-800)<br>
Play MIDI Notes (to external devices like Arturia Minifreak)<br>
Save MIDI Notes or settings to JSON file<br>
Load MIDI Notes or settings from JSON file
JavaScript Logic
Attach event listeners to all inputs and buttons
Implement a mock function that generates dummy MIDI notes as if from an AI model
Render generated chords on the piano roll canvas
Use Web Audio API to play simple sine-wave tones when “Play” is clicked
Start a metronome ticking at the set BPM when playback starts
Responsive Design
Ensure the layout works well on desktop and mobile devices
Use CSS Flexbox or Grid for layout structure

##📁 File Structure

<br>****
frontend/<br>
│<br>
├── index.html      # Main HTML page<br>
├── styles.css      # Styling for the app<br>
└── app.js          # JavaScript logic<br>
<br>
✅ Acceptance Criteria<br>
User can select key (C, C#, D, ..., B)<br>
User can select scale (major, minor, pentatonic, etc.)<br>
User can select chord type (triad, seventh, augmented, etc.)<br>
User can set progression length (1–16 bars)<br>
Clicking "Generate Chords" triggers a function and displays output<br>
Piano roll draws rectangles representing notes over time<br>
Play/Pause/Stop buttons control audio playback of generated chords<br>
No backend calls are made yet; all data is mocked<br>
All code must run locally without external dependencies<br>

<br><br>🧪 Testing Plan<br>
Manual testing by QA or developer to ensure UI responsiveness and interaction<br>
Test edge cases like invalid input (ensure graceful handling)<br>
Check cross-browser compatibility (Chrome, Firefox, Safari)<br>
Ensure mobile view works correctly<br>
🔧 Tools & Technologies<br>
VS Code – IDE for development<br>
Live Server Extension – For local testing<br>
Git – Version control (commit early and often)<br>
Browser DevTools – Debugging JavaScript and layout issues<br>
<br>
<br><br>##📦 Deliverables
Fully functional index.html, styles.css, and app.js files<br>
Demo-ready build that runs locally<br>
README.md explaining how to run and test the frontend<br>
Optional: Unit tests for core functions (e.g., chord drawing logic)<br>

# AI Chord Generator Frontend (Sprint 1)

This is the frontend implementation for the AI Chord Generator, a web-based application for generating chord progressions. This is part of Sprint 1 and provides a basic user interface with mock chord generation and playback capabilities.

## How to Run

1.  **Save the Files:** Ensure you have `index.html`, `styles.css`, and `app.js` in the `frontend/` directory.
2.  **Use Live Server (VS Code Extension):**
    * If you have the Live Server extension installed in VS Code, open `index.html` and right-click.
    * Select "Open with Live Server". This will open the application in your default web browser.
3.  **Alternatively (Without Live Server):**
    * Open your web browser (Chrome, Firefox, Safari).
    * Navigate to the `frontend/index.html` file on your local file system.

## How to Test

1.  **UI Responsiveness:** Resize your browser window to check if the layout adapts well to different screen sizes (desktop and mobile).
2.  **Parameter Selection:** Use the dropdowns for Key, Scale, and Chord Type, and the number input for Length.
3.  **Generate Chords:** Click the "Generate Chords" button. You should see rectangles appearing on the piano roll canvas, representing the mocked chords.
4.  **Playback:**
    * Click the "Play" button. You should hear simple sine wave tones corresponding to the notes in the generated chords.
    * Click "Pause" to stop the currently playing audio.
    * Click "Stop" to halt playback and reset the current time.

## Known Limitations (Sprint 1)

* Chord generation is purely mock and does not involve any actual AI or sophisticated music theory.
* The piano roll visualization is basic and shows all notes of a chord at the same horizontal position within a bar.
* Playback uses simple sine waves; no actual instrument sounds are implemented.
* No backend communication is implemented.

## Deliverables

* `frontend/index.html`
* `frontend/styles.css`
* `frontend/app.js`
* `README.md`

## Optional: Unit Tests

No unit tests are included in this initial deliverable as the focus was on the basic UI and mock functionality. Unit tests for core logic (like the chord drawing function) can be added in subsequent sprints if needed.


<br>
<img src="https://github.com/pappavis/AI_Playground/blob/main/ChordGeneratorFugroAI/img/Scaler3A_%20Chord_Generator_Clone.png?raw=true" width="80%" hight="80%" alt="AI Chord generator">
<br><br>


by: Michiel.
