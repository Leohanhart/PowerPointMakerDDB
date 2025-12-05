# 🚀 PowerPoint Maker DDB - Datadriven Business Hackathon

<div align="center">

### ✨ Transformeer PDF's naar PowerPoint presentaties met AI-powered embeddings! ✨

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📖 Over dit Project

Welkom bij **PowerPoint Maker DDB**! 🎉 Dit project is ontwikkeld voor de **Datadriven Business Hackathon** en combineert de kracht van OpenAI's geavanceerde embedding technologie met automatische PowerPoint generatie.

### 🎯 Wat doet dit project?

Dit project maakt het mogelijk om:
- 📄 **PDF's automatisch te verwerken** - Gooi je PDF's in de folder en laat de magic beginnen!
- 🧠 **Tekst te embedden met AI** - Gebruikt OpenAI's state-of-the-art embedding modellen
- 📊 **PowerPoint presentaties te genereren** - Creëert automatisch professionele slides
- 💾 **Lokale vector opslag** - Slaat embeddings lokaal op voor snelle toegang

---

## 🛠️ Technologie Stack

| Technologie | Beschrijving | Emoji |
|------------|-------------|-------|
| **Python 3.8+** | De programmeertaal | 🐍 |
| **OpenAI API** | Voor tekst embedding en AI-magic | 🤖 |
| **python-pptx** | PowerPoint bestanden maken en bewerken | 📊 |
| **PyPDF2** | PDF tekst extractie | 📄 |
| **NumPy** | Vector manipulatie en opslag | 🔢 |
| **python-dotenv** | Environment variabelen beheer | 🔐 |

---

## 🚀 Quick Start

### Stap 1: Clone & Setup 📥

```bash
git clone <repository-url>
cd PowerPointMakerDDB
```

### Stap 2: Installeer Dependencies 📦

```bash
pip install -e .
```

Of als je pip direct wilt gebruiken:
```bash
pip install openai python-pptx PyPDF2 numpy python-dotenv requests
```

### Stap 3: Configureer OpenAI API Key 🔑

1. Kopieer het voorbeeld bestand:
```bash
cp example.env .env
```

2. Open `.env` en voeg je OpenAI API key toe:
```env
OPENAI_API_KEY=sk-jouw-super-geheime-api-key-hier
```

> 💡 **Tip**: Je kunt je API key krijgen op [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

---

## 🎮 Gebruik

### Basis Workflow

1. **📁 Plaats je PDF's**
   - Stop alle PDF bestanden die je wilt verwerken in de `src/pdf/` folder

2. **▶️ Run de applicatie**
   ```bash
   python -m src.main
   ```
   
   Of gebruik de command-line tool:
   ```bash
   powerpoint-maker
   ```

3. **✨ Geniet van de magic!**
   - De service verwerkt automatisch alle PDF's
   - Tekst wordt geëxtraheerd en gechunkt
   - Embeddings worden gemaakt met OpenAI
   - Alles wordt opgeslagen in `src/service/vectors.pkl`

### 📊 Wat gebeurt er precies?

```
📄 PDF Bestanden
    ↓
🔍 Tekst Extractie (PyPDF2)
    ↓
✂️ Chunking (1000 karakters, 200 overlap)
    ↓
🧠 OpenAI Embeddings (text-embedding-3-small)
    ↓
💾 Lokale Vector Opslag (vectors.pkl)
    ↓
🎉 Klaar voor gebruik!
```

---

## 📁 Project Structuur

```
PowerPointMakerDDB/
├── 📂 src/                    # Source code
│   ├── 🐍 main.py            # Hoofdapplicatie entry point
│   ├── 📂 pdf/               # 📄 PDF input folder (plaats hier je PDF's!)
│   ├── 📂 powerpoint/        # 📊 PowerPoint output folder
│   └── 📂 service/           # 🔧 Service layer
│       ├── pdf_service.py    # PDF processing & embedding service
│       └── vectors.pkl       # 💾 Lokaal vector bestand (auto-generated)
├── ⚙️ pyproject.toml          # Project dependencies en configuratie
├── 📖 README.md               # Deze awesome documentatie!
├── 📝 example.env             # Voorbeeld environment variabelen
└── 🔒 .env                    # Jouw environment variabelen (niet in git!)
```

---

## 🔧 PDF Processing Details

### Hoe werkt de PDF Service? 🤔

De `PDFService` class doet het volgende:

1. **📄 PDF Extractie**
   - Leest alle `.pdf` bestanden uit de `src/pdf/` folder
   - Extraheert tekst van alle pagina's

2. **✂️ Intelligent Chunking**
   - Splitst tekst in overlappende chunks (standaard: 1000 karakters)
   - Overlap van 200 karakters voor context behoud
   - Probeert te breken bij zinsgrenzen voor betere kwaliteit

3. **🧠 AI Embeddings**
   - Gebruikt OpenAI's `text-embedding-3-small` model
   - Creëert vector representaties van elke chunk
   - Batch processing voor efficiëntie

4. **💾 Vector Opslag**
   - Slaat alle embeddings lokaal op in `vectors.pkl`
   - **Vervangt** het bestaande bestand (geen append!)
   - Bevat chunks, embeddings en metadata

### ⚙️ Configuratie Opties

Je kunt de service aanpassen in `src/service/pdf_service.py`:

```python
pdf_service = PDFService(
    pdf_folder="src/pdf",                    # PDF input folder
    vector_file="src/service/vectors.pkl"    # Vector opslag locatie
)

# Chunking parameters (in chunk_text methode):
chunk_size=1000    # Maximale chunk grootte
overlap=200        # Overlap tussen chunks
```

---

## 📚 Dependencies Overzicht

| Package | Versie | Doel |
|---------|--------|------|
| `openai` | ≥1.0.0 | 🤖 OpenAI API interactie voor embeddings |
| `python-pptx` | ≥0.6.21 | 📊 PowerPoint bestanden maken/bewerken |
| `PyPDF2` | ≥3.0.0 | 📄 PDF tekst extractie |
| `numpy` | ≥1.24.0 | 🔢 Vector manipulatie en opslag |
| `python-dotenv` | ≥1.0.0 | 🔐 Environment variabelen beheer |
| `requests` | ≥2.31.0 | 🌐 HTTP requests (voor API calls) |

---

## 🎯 Features

- ✅ **Automatische PDF verwerking** - Gooi erin en het werkt!
- ✅ **Intelligent chunking** - Slimme tekst splitsing met overlap
- ✅ **OpenAI embeddings** - State-of-the-art AI technologie
- ✅ **Lokale vector opslag** - Snel en efficiënt
- ✅ **Metadata tracking** - Houdt bij welke chunk van welk bestand komt
- ✅ **Error handling** - Robuuste foutafhandeling
- ✅ **Clean code** - Goed gestructureerd en onderhoudbaar

---

## 🐛 Troubleshooting

### ❌ "OPENAI_API_KEY not found"
**Oplossing**: Zorg dat je een `.env` bestand hebt met je API key. Kopieer `example.env` naar `.env` en vul je key in.

### ❌ "No PDF files found"
**Oplossing**: Plaats PDF bestanden in de `src/pdf/` folder.

### ❌ "PyPDF2 is required"
**Oplossing**: Installeer dependencies met `pip install -e .`

### ❌ Import errors
**Oplossing**: Zorg dat je in de root directory van het project bent en dat alle dependencies geïnstalleerd zijn.

---

## 🚧 Roadmap

- [ ] PowerPoint generatie functionaliteit
- [ ] Vector similarity search
- [ ] Multi-language support
- [ ] Web interface
- [ ] Batch processing opties
- [ ] Custom chunking strategieën

---

## 🤝 Contributing

Dit project is ontwikkeld voor de **Datadriven Business Hackathon**. 

Wil je bijdragen? 🎉
1. Fork het project
2. Maak een feature branch
3. Commit je changes
4. Push naar de branch
5. Open een Pull Request

---

## 📝 Licentie

[Voeg licentie informatie toe indien van toepassing]

---

## 👥 Auteurs

Ontwikkeld met ❤️ voor de **Datadriven Business Hackathon**

---

## 🎉 Hackathon Info

Dit project is speciaal ontwikkeld voor de **Datadriven Business Hackathon** en combineert:
- 🤖 AI/ML technologie (OpenAI embeddings)
- 📊 Business intelligence (PowerPoint generatie)
- 💡 Innovatieve oplossingen (Automatische document processing)

---

<div align="center">

### ⭐ Star dit project als je het cool vindt! ⭐

**Made with ❤️ and ☕ for the Datadriven Business Hackathon**

</div>
