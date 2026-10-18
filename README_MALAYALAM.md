# Personal CMA & CA Office AI Agent — Setup Guide (Windows + VS Code)

ഈ project PDF / Word / Excel ഫയലുകളിൽ നിന്ന് text എടുക്കാനും, local AI ഉപയോഗിച്ച് summary, analysis, CMA study notes, CA office working-paper draft, action points എന്നിവ തയ്യാറാക്കാനും സഹായിക്കും. ഫലം Word, PDF, Excel, Markdown/TXT ആയി export ചെയ്യാം.

## 1. ആവശ്യമായവ
- Windows കമ്പ്യൂട്ടർ
- Python 3.11 അല്ലെങ്കിൽ 3.12
- VS Code
- Ollama (local AI പ്രവർത്തിപ്പിക്കാൻ)
- കുറഞ്ഞത് 8 GB RAM-ൽ ചെറിയ model മാത്രം ഉപയോഗിക്കുക. വലിയ ഫയലുകൾക്ക് സമയം എടുക്കാം.

## 2. Python പരിശോധിക്കുക
VS Code തുറക്കുക → Terminal → New Terminal. തുടർന്ന്:

```powershell
python --version
```

Python കാണുന്നില്ലെങ്കിൽ Python ഇൻസ്റ്റാൾ ചെയ്ത് installation സമയത്ത് **Add Python to PATH** തിരഞ്ഞെടുക്കുക.

## 3. Ollama ഇൻസ്റ്റാൾ ചെയ്യുക
1. https://ollama.com എന്ന ഔദ്യോഗിക സൈറ്റിൽ നിന്ന് Ollama ഇൻസ്റ്റാൾ ചെയ്യുക.
2. VS Code Terminal-ൽ:

```powershell
ollama pull qwen2.5:3b
```

3. പരിശോധിക്കാൻ:

```powershell
ollama run qwen2.5:3b
```

ചാറ്റ് പരിശോധിച്ച ശേഷം ` /bye ` നൽകി പുറത്തുകടക്കാം. Ollama പശ്ചാത്തലത്തിൽ പ്രവർത്തിക്കണം.

## 4. Project തുറക്കുക
ZIP extract ചെയ്യുക. VS Code → File → Open Folder → `Personal_CMA_AI_Agent` തിരഞ്ഞെടുക്കുക.

## 5. App പ്രവർത്തിപ്പിക്കുക
ഏറ്റവും എളുപ്പം: `run_app.bat` double-click ചെയ്യുക.

അല്ലെങ്കിൽ VS Code Terminal-ൽ project folder തുറന്നിരിക്കെ:

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

Browser-ൽ local app തുറക്കും. തുറന്നില്ലെങ്കിൽ terminal-ൽ കാണിക്കുന്ന `http://localhost:8501` വിലാസം തുറക്കുക.

## 6. ഉപയോഗിക്കുന്നത്
1. **Tax & accounts chat** tab-ൽ ഇന്ത്യൻ Income Tax, GST, Tally, Zoho Books, accounting, commercial law വിഷയങ്ങളിൽ ചോദിക്കുക. മറുപടികൾ local Ollama model-ൽ നിന്നാണ്; നിലവിലെ നിയമം/നിരക്ക്/തീയതി ഔദ്യോഗിക ഉറവിടങ്ങളിൽ പരിശോധിക്കുക.
2. **Document assistant** tab-ൽ PDF / DOCX / XLSX / TXT / CSV upload ചെയ്യുക.
3. Sidebar-ൽ Summarise, Analyse, Study notes, CA office review, Action points എന്നിവ തിരഞ്ഞെടുക്കുക.
4. **Run AI task** അമർത്തുക.
5. Result പരിശോധിച്ച് Word / PDF / Excel / Markdown ആയി download ചെയ്യുക.
6. **Convert / extract** tab-ൽ ഫയലിൽ നിന്ന് text എടുത്ത് മറ്റൊരു format-ൽ export ചെയ്യാം.

## പ്രധാന പരിമിതികൾ
- Scanned PDF-ൽ selectable text ഇല്ലെങ്കിൽ ഈ version-ന് text കിട്ടണമെന്നില്ല. OCR വേറെ ഇൻസ്റ്റാൾ ചെയ്ത് ചേർക്കണം.
- പഴയ `.doc` / `.xls` ഫയലുകൾ ആദ്യം `.docx` / `.xlsx` ആയി save ചെയ്യുക.
- PDF-ലുള്ള complex tables, layout, charts, formulas എന്നിവയുടെ കൃത്യമായ conversion ഉറപ്പില്ല.
- Excel export ഇപ്പോൾ AI output-നെ വരികളാക്കി നൽകുന്നു; യഥാർത്ഥ accounting workbook-ന്റെ layout/formulas പൂർണ്ണമായി പുനർനിർമ്മിക്കില്ല.
- Local AI തെറ്റായ സംഗ്രഹം, നിയമവകുപ്പ്, tax conclusion, calculation എന്നിവ നൽകാം. CA firm-ന്റെ client data ഉപയോഗിക്കുന്നതിന് മുമ്പ് firm policy/permission പാലിക്കുക. എല്ലാ statutory figures, reconciliations, audit/tax conclusions എന്നിവ മനുഷ്യൻ verify ചെയ്യണം.
- ഈ app free/local-first ആണ്; model download ചെയ്യാൻ disk space വേണം. Model ഉപയോഗിക്കുന്ന സമയത്ത് RAM/CPU ഉപയോഗിക്കും.

## പ്രശ്നപരിഹാരം
**`ollama` is not recognized**: Ollama ഇൻസ്റ്റാൾ ചെയ്തിട്ടുണ്ടോ എന്ന് പരിശോധിക്കുക; പുതിയ Terminal തുറക്കുക.

**Ollama connection error**: Ollama തുറന്നിരിക്കണം. `ollama list` ഉപയോഗിച്ച് model ഉണ്ടോ എന്ന് പരിശോധിക്കുക.

**Streamlit not found**: `.venv` activate ചെയ്ത് `pip install -r requirements.txt` വീണ്ടും നടത്തുക.

**കമ്പ്യൂട്ടർ slow**: `qwen2.5:3b` പോലുള്ള ചെറിയ model ഉപയോഗിക്കുക, വളരെ വലിയ PDF ഭാഗങ്ങളായി upload ചെയ്യുക, മറ്റ് apps അടയ്ക്കുക.

**Confidential files**: ഈ app text AI-ക്ക് local Ollama വഴി അയയ്ക്കുന്നു. എങ്കിലും കമ്പനി/CA firm policy പാലിക്കുക; client data ഉപയോഗിക്കാൻ മുൻകൂർ അനുമതി ഉറപ്പാക്കുക.
