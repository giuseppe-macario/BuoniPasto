# BuoniPasto (macOS / Windows / Linux)

Applicazione che processa statini SIGE in PDF per generare automaticamente una tabella riepilogativa dei buoni pasto.  
Include:

- **GUI PyQt6**
- **Build locale per macOS**
- **Build automatica multipiattaforma tramite GitHub Actions**
- **Build Windows/macOS/Linux dagli artifact GitHub**

---

## Installazione ed esecuzione su macOS (da zero)

Questa sezione spiega come configurare il progetto su un Mac nuovo.

### 1. Scarica o posiziona i sorgenti

Metti questi file in una cartella, ad esempio:

```
~/Desktop/test/
  ├─ buoni_pasto_core.py
  └─ buoni_pasto_gui_qt.py
```

### 2. Apri il Terminale ed entra nella cartella

```bash
cd ~/Desktop/test
```

### 3. Crea un ambiente virtuale

```bash
python -m venv venv
```

### 4. Attiva il virtualenv

```bash
source venv/bin/activate
```

Vedrai il prompt diventare:

```
(venv) giuseppe@Mac test %
```

### 5. Installa le dipendenze

```bash
pip install pdfplumber PyQt6 pyinstaller
```

### 6. Avvia l'app GUI

```bash
python buoni_pasto_gui_qt.py
```

Se tutto è installato correttamente, si aprirà la finestra della GUI.

---

## Build locale per macOS (creare l’app cliccabile `.app`)

Dal virtualenv attivo:

```bash
python -m PyInstaller --windowed --name BuoniPasto buoni_pasto_gui_qt.py
```

Otterrai:

```
dist/
 └─ BuoniPasto.app
```

Avvia l'app con:

```bash
open dist
```

> Se macOS mostra l’avviso “sviluppatore non identificato”, apri con click destro → **Apri**.

### Ricompilazioni dopo ogni aggiornamento

Tutte le volte che aggiorni un sorgente `.py`, bisogna ripetere questi due comandi:

```bash
source venv/bin/activate
python -m PyInstaller --windowed --name BuoniPasto buoni_pasto_gui_qt.py
```

---

# Build multipiattaforma con GitHub Actions

Il repository contiene il workflow:

```
.github/workflows/build-all.yml
```

Questo workflow:

- Compila automaticamente l’app per **Windows**, **macOS**, **Linux**  
- Carica gli eseguibili come **artifacts** scaricabili

### Come eseguire il build via GitHub (da web)

1. Vai al repository BuoniPasto
2. Clicca sul tab **Actions**
3. Seleziona il workflow **Build desktop apps**
4. Clicca **Run workflow**
5. Attendere l'esecuzione dei task per qualche minuto, finché compare la spunta verde ✅

Clicca sul nome del workflow accanto alla spunta verde. Compariranno tre artifact:

- `BuoniPasto-windows`
- `BuoniPasto-macos`
- `BuoniPasto-linux`

Cliccando su ciascuno scarichi uno zip contenente:

- `.exe` per Windows  
- `.app` per macOS  
- binario eseguibile per Linux  

---

# Organizzazione del progetto

- **buoni_pasto_core.py** — contiene la logica di elaborazione (core)
- **buoni_pasto_gui_qt.py** — GUI PyQt6
- **.github/workflows/build-all.yml** — build multipiattaforma automatizzato

Inoltre, `buoni_pasto_cli.py` esegue il programma da linea di comando senza GUI, e `buoni_pasto.py` è un file unico che esegue tutto da linea di comando senza chiamare `buoni_pasto_core.py` (quindi può essere usato da solo).
