# Browser Fingerprinting Detection Experiment

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Status](https://img.shields.io/badge/status-Active-success)

Infrastructure expérimentale pour détecter et analyser les tentatives de fingerprinting des navigateurs sur des sites web réels.

**🔗 Associated Research Paper**: *Browser Fingerprinting Detection: A Comparative Analysis* (LNNS Springer, 2024)  
**👥 Authors**: Youness Ikkou, Mohamed Elboukhari, Ahmed Ouriarhi  
**🏛️ Institution**: MATSI Laboratory, Mohammed Premier University, Oujda, Morocco

## 📋 Description

Ce projet implémente un système complet de détection de fingerprinting basé sur:
- **Navigateurs**: Chromium et Firefox
- **Module de détection**: JavaScript custom qui intercepte les appels API
- **Automatisation**: Selenium WebDriver
- **Métriques**: Calcul de l'entropie de Shannon pour quantifier l'unicité des attributs
- **Protocole**: Tests longitudinaux sur 15 jours avec 2 visites par site/navigateur

## 🏗️ Architecture

```
fingerprinting_detector/
├── detector.js          # Module JavaScript de détection
├── main.py             # Script principal Selenium
├── config.json         # Configuration de l'expérience
├── websites.json       # Liste des 100 sites web à tester
├── requirements.txt    # Dépendances Python
├── results/           # Résultats des tests (créé automatiquement)
└── README.md          # Ce fichier
```

## 🔧 Installation

### Prérequis

1. **Python 3.8+**
   ```powershell
   python --version
   ```

2. **Navigateurs**
   - Google Chrome ou Chromium
   - Mozilla Firefox

3. **WebDrivers**

   **Option A: Installation automatique (Recommandée)**
   ```powershell
   pip install webdriver-manager
   ```

   **Option B: Installation manuelle**
   - ChromeDriver: https://chromedriver.chromium.org/
   - GeckoDriver (Firefox): https://github.com/mozilla/geckodriver/releases
   
   Placez les exécutables dans votre PATH ou dans le dossier du projet.

### Installation des dépendances

```powershell
# Créer un environnement virtuel (recommandé)
python -m venv venv
.\venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

## 🚀 Utilisation

### 1. Configuration

Modifiez `config.json` selon vos besoins:

```json
{
  "browsers": ["chrome", "firefox"],
  "session_duration": 45,
  "visits_per_browser": 2,
  "days_between_visits": 15,
  "results_dir": "results"
}
```

### 2. Personnaliser la liste de sites web

Modifiez `websites.json` pour ajouter/supprimer des sites:

```json
{
  "websites": [
    "https://www.example.com",
    "https://www.test.com"
  ]
}
```

### 3. Lancer l'expérience

**Première visite (Jour 1)**:
```powershell
python main.py
# Entrez "1" quand demandé
```

**Deuxième visite (Jour 15)**:
```powershell
python main.py
# Entrez "2" quand demandé
```

### 4. Mode test rapide

Pour tester rapidement sur quelques sites:

```python
# Créez un fichier test_websites.json
{
  "websites": [
    "https://www.google.com",
    "https://www.facebook.com",
    "https://www.amazon.com"
  ]
}
```

Modifiez `config.json`:
```json
{
  "websites_file": "test_websites.json",
  "session_duration": 20
}
```

## 📊 Résultats

Les résultats sont sauvegardés dans le dossier `results/`:

### Fichiers individuels
- Format: `{browser}_{website}_{visit}_{timestamp}.json`
- Contenu: Données brutes de fingerprinting + entropies calculées

Exemple:
```json
{
  "session_id": "chrome_www.example.com_1",
  "website": "https://www.example.com",
  "browser": "chrome",
  "visit_number": 1,
  "timestamp": "2025-11-02T10:30:45",
  "fingerprint_data": {
    "canvas": [...],
    "webgl": [...],
    "audio": [...]
  },
  "entropies": {
    "canvas": 5.23,
    "webgl": 4.87,
    "audio": 3.45,
    "total": 15.67
  },
  "success": true
}
```

### Rapports de synthèse
- Format: `experiment_report_visit{N}_{timestamp}.json`
- Contenu: Statistiques agrégées, moyennes d'entropie, taux de succès

## 🔍 Techniques de Fingerprinting Détectées

Le module `detector.js` intercepte:

| Catégorie | APIs surveillées |
|-----------|-----------------|
| **Canvas** | fillText, strokeText, toDataURL, toBlob |
| **WebGL** | getParameter, getExtension, getSupportedExtensions |
| **Audio** | createOscillator, createAnalyser, getFloatFrequencyData |
| **Fonts** | document.fonts.check |
| **Navigator** | userAgent, platform, languages, hardwareConcurrency |
| **Screen** | width, height, colorDepth, pixelDepth |
| **Storage** | localStorage, sessionStorage |
| **WebRTC** | RTCPeerConnection |
| **Battery** | getBattery |
| **Sensors** | Gyroscope, Accelerometer |
| **Plugins** | navigator.plugins |
| **Hardware** | hardwareConcurrency, deviceMemory |

## 📈 Calcul de l'Entropie de Shannon

L'entropie mesure l'unicité des attributs collectés:

**Formule**: H(X) = -Σ p(x) × log₂(p(x))

**Interprétation**:
- **0 bits**: Tous les sites collectent la même valeur (aucune unicité)
- **1 bit**: 2 valeurs possibles équiprobables
- **~5-10 bits**: Modérément unique
- **>15 bits**: Hautement unique (fort fingerprinting)

## ⚙️ Options Avancées

### Mode Headless

Pour exécuter sans interface graphique, modifiez `main.py`:

```python
# Chrome
options.add_argument('--headless=new')

# Firefox
options.add_argument('-headless')
```

### Parallélisation

Pour tester plusieurs sites simultanément, créez plusieurs instances:

```powershell
# Terminal 1
python main.py

# Terminal 2
python main.py
```

### Contourner la détection anti-automation

Le script inclut déjà des techniques pour éviter la détection:
- Désactivation de `navigator.webdriver`
- Préférences réalistes
- Simulation de comportement utilisateur
- Randomisation des actions

## 🐛 Résolution de problèmes

### WebDriver non trouvé

**Erreur**: `selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH`

**Solution**:
```powershell
pip install webdriver-manager
```

Ou téléchargez manuellement et ajoutez au PATH.

### Timeout sur certains sites

**Cause**: Sites lents ou protections anti-bot

**Solution**: Augmentez le timeout dans `config.json` ou `main.py`:
```python
self.driver.set_page_load_timeout(60)  # 60 secondes
```

### Navigateur détecté comme bot

**Solution**: Désactivez le mode headless et ajoutez des délais:
```json
{
  "experiment_settings": {
    "headless_mode": false
  }
}
```

### Erreur de certificat SSL

**Solution**: Ajoutez dans `main.py`:
```python
# Chrome
options.add_argument('--ignore-certificate-errors')

# Firefox
options.set_preference('accept_insecure_certs', True)
```

## 📊 Analyse des Résultats

### Script d'analyse simple

Créez `analyze_results.py`:

```python
import json
import os
from pathlib import Path

results_dir = Path('results')
all_results = []

for file in results_dir.glob('*.json'):
    if 'report' not in file.name:
        with open(file) as f:
            all_results.append(json.load(f))

# Statistiques
successful = [r for r in all_results if r.get('success')]
print(f"Taux de succès: {len(successful)}/{len(all_results)} ({len(successful)/len(all_results)*100:.1f}%)")

# Entropie moyenne
avg_entropy = sum(r['entropies']['total'] for r in successful) / len(successful)
print(f"Entropie moyenne: {avg_entropy:.2f} bits")

# Top 10 sites avec le plus de fingerprinting
by_entropy = sorted(successful, key=lambda x: x['entropies']['total'], reverse=True)
print("\nTop 10 sites avec le plus de fingerprinting:")
for i, r in enumerate(by_entropy[:10], 1):
    print(f"{i}. {r['website']}: {r['entropies']['total']:.2f} bits")
```

## 📝 Structure des Données Capturées

Chaque appel API capturé contient:

```json
{
  "timestamp": 1234,
  "method": "fillText",
  "value": "Sample text",
  "stackTrace": "Error\n    at ..."
}
```

Le `stackTrace` permet d'identifier les scripts tiers responsables.

## 🔒 Conformité GDPR

Pour analyser la conformité GDPR:

1. Vérifiez les sites européens dans `websites.json`
2. Cherchez les fingerprinting **avant** acceptation des cookies
3. Comparez avec **après** acceptation

## 📖 Références

- [1] Eckersley, P. (2010). "How Unique Is Your Web Browser?"
- [2] Laperdrix, P. et al. (2016). "Beauty and the Beast: Diverting modern web browsers to build unique browser fingerprints"
- [3] Englehardt, S. & Narayanan, A. (2016). "Online tracking: A 1-million-site measurement and analysis"

## 🤝 Contribution

Pour améliorer ce projet:

1. Ajoutez de nouvelles techniques de détection dans `detector.js`
2. Optimisez la simulation de comportement utilisateur
3. Ajoutez des visualisations dans les rapports
4. Créez des scripts d'analyse avancés

## 📊 Key Results from Our Research

Based on testing 100 websites across Chrome and Firefox:

- **67%** of sites use Canvas fingerprinting (17.23 bits entropy)
- **94.3%** re-identification success rate with Canvas
- **Firefox ETP** blocks 100% of Facebook trackers vs 0% for Chrome
- **Amazon** executes 259 API calls in 45 seconds
- **uBlock Origin** achieves only 28.4% reduction
- **98.7%** temporal persistence with combined techniques

See our published research paper for complete analysis and methodology.

## 🌟 Features

✅ **12 API Categories Monitored**: Canvas, WebGL, Audio, Fonts, Navigator, Screen, Storage, WebRTC, Battery, Sensors, Plugins, Hardware  
✅ **Multi-Browser Support**: Chrome, Chromium, Firefox (extensible to others)  
✅ **Real Behavioral Simulation**: Mouse movements, scrolling, realistic timing  
✅ **Shannon Entropy Calculation**: Quantifies uniqueness of fingerprinting attributes  
✅ **Longitudinal Protocol**: 15-day follow-up visits for temporal stability analysis  
✅ **Automated Detection Evasion**: Removes `navigator.webdriver` flag  
✅ **Complete JSON Export**: Full API call traces with stack traces  

## 📄 Licence

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This software is provided for academic and research purposes only.

## ⚠️ Avertissement

- Respectez les conditions d'utilisation des sites web testés
- Ne surchargez pas les serveurs (rate limiting)
- Utilisez uniquement pour la recherche académique
- Certains sites peuvent bloquer les requêtes automatisées

## 👥 Contributors

- **Youness Ikkou** - Lead Developer & Researcher
- **Mohamed Elboukhari** - Research Supervisor
- **Ahmed Ouriarhi** - Co-Researcher

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📖 Citation

If you use this tool in your research, please cite our paper:

```bibtex
@inproceedings{ikkou2024fingerprinting,
  title={Browser Fingerprinting Detection: A Comparative Analysis},
  author={Ikkou, Youness and Elboukhari, Mohamed and Ouriarhi, Ahmed},
  booktitle={Lecture Notes in Networks and Systems, Springer},
  year={2024},
  organization={MATSI Laboratory, Mohammed Premier University}
}
```

## 🔗 Related Links

- 📄 [Research Paper](https://github.com/younessikkou/fingerprinting-detector/paper)
- 🏛️ [MATSI Laboratory](https://www.ump.ac.ma/)
- 📧 Contact: ikkou557@gmail.com

## 📞 Support

Pour toute question ou problème:
- 🐛 [Open an Issue](https://github.com/younessikkou/fingerprinting-detector/issues)
- 📧 Email: ikkou557@gmail.com
- 📝 Consultez les logs: `fingerprinting_experiment.log`
- 🧪 Testez d'abord avec un petit nombre de sites

## ⭐ Star History

If you find this project useful, please consider giving it a star! It helps others discover the tool.

