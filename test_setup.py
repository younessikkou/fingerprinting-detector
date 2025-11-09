"""
Quick Setup Test Script
Vérifie que l'environnement est correctement configuré
"""

import sys
import os
from pathlib import Path

def test_python_version():
    """Test Python version"""
    print("🔍 Vérification de la version Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Version trop ancienne")
        print("      Installez Python 3.8 ou supérieur")
        return False

def test_selenium():
    """Test Selenium installation"""
    print("\n🔍 Vérification de Selenium...")
    try:
        import selenium
        print(f"   ✅ Selenium {selenium.__version__} installé")
        return True
    except ImportError:
        print("   ❌ Selenium non installé")
        print("      Exécutez: pip install selenium")
        return False

def test_chrome_driver():
    """Test Chrome/Chromium WebDriver"""
    print("\n🔍 Vérification de ChromeDriver...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--log-level=3')
        
        try:
            chromedriver_path = r"C:\Users\PC\Desktop\doctorat\chromedriver.exe"
            service = Service(executable_path=chromedriver_path)
            driver = webdriver.Chrome(service=service, options=options)
            driver.quit()
            print("   ✅ ChromeDriver fonctionne")
            print(f"      Chemin: {chromedriver_path}")
            return True
        except Exception as e:
            print(f"   ⚠️  ChromeDriver non accessible: {str(e)[:50]}")
            print(f"      Vérifiez que le fichier existe: C:\\Users\\PC\\Desktop\\doctorat\\chromedriver.exe")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_firefox_driver():
    """Test Firefox WebDriver"""
    print("\n🔍 Vérification de GeckoDriver (Firefox)...")
    try:
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options
        from selenium.webdriver.firefox.service import Service
        
        options = Options()
        options.add_argument('-headless')
        
        try:
            geckodriver_path = r"C:\Users\PC\Desktop\doctorat\geckodriver.exe"
            service = Service(executable_path=geckodriver_path)
            driver = webdriver.Firefox(service=service, options=options)
            driver.quit()
            print("   ✅ GeckoDriver fonctionne")
            print(f"      Chemin: {geckodriver_path}")
            return True
        except Exception as e:
            print(f"   ⚠️  GeckoDriver non accessible: {str(e)[:50]}")
            print(f"      Vérifiez que le fichier existe: C:\\Users\\PC\\Desktop\\doctorat\\geckodriver.exe")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_files():
    """Test required files"""
    print("\n🔍 Vérification des fichiers requis...")
    
    required_files = [
        'detector.js',
        'main.py',
        'config.json',
        'websites.json',
        'requirements.txt'
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - Fichier manquant!")
            all_ok = False
    
    return all_ok

def test_detector_script():
    """Test detector.js script"""
    print("\n🔍 Vérification du script de détection...")
    try:
        with open('detector.js', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'window.fingerprintData' in content and 'getFingerprintData' in content:
                print("   ✅ Script de détection valide")
                return True
            else:
                print("   ❌ Script de détection incomplet")
                return False
    except Exception as e:
        print(f"   ❌ Erreur de lecture: {e}")
        return False

def test_json_files():
    """Test JSON configuration files"""
    print("\n🔍 Vérification des fichiers de configuration...")
    try:
        import json
        
        # Test config.json
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            print(f"   ✅ config.json valide")
            print(f"      - Navigateurs: {config.get('browsers', [])}")
            print(f"      - Durée session: {config.get('session_duration', 0)}s")
        
        # Test websites.json
        with open('websites.json', 'r', encoding='utf-8') as f:
            websites = json.load(f)
            site_count = len([w for w in websites.get('websites', []) if not w.startswith('_')])
            print(f"   ✅ websites.json valide")
            print(f"      - Nombre de sites: {site_count}")
        
        return True
    except Exception as e:
        print(f"   ❌ Erreur JSON: {e}")
        return False

def run_quick_test():
    """Run a quick test of the entire system"""
    print("\n🔍 Test rapide du système complet...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        # Load detector script
        with open('detector.js', 'r', encoding='utf-8') as f:
            detector_script = f.read()
        
        # Start browser
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--log-level=3')
        
        print("   📦 Lancement du navigateur...")
        driver = webdriver.Chrome(options=options)
        
        # Visit a test page
        print("   🌐 Visite d'une page test...")
        driver.get('https://www.example.com')
        
        # Inject detector
        print("   💉 Injection du script de détection...")
        driver.execute_script(detector_script)
        
        # Get data
        print("   📊 Récupération des données...")
        data = driver.execute_script("return window.getFingerprintData();")
        stats = driver.execute_script("return window.getFingerprintStats();")
        
        driver.quit()
        
        print(f"   ✅ Test réussi!")
        print(f"      - API calls capturés: {stats.get('total', 0)}")
        print(f"      - Durée: {stats.get('duration', 0)}ms")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Échec du test: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 70)
    print("TEST DE CONFIGURATION - DÉTECTION DE FINGERPRINTING")
    print("=" * 70)
    print()
    
    results = []
    
    # Run all tests
    results.append(("Python Version", test_python_version()))
    results.append(("Selenium", test_selenium()))
    results.append(("Fichiers requis", test_files()))
    results.append(("Script de détection", test_detector_script()))
    results.append(("Fichiers JSON", test_json_files()))
    results.append(("ChromeDriver", test_chrome_driver()))
    results.append(("GeckoDriver", test_firefox_driver()))
    
    # Optional: Full system test
    print("\n" + "=" * 70)
    user_input = input("Voulez-vous exécuter un test complet du système? (o/n): ").strip().lower()
    if user_input in ['o', 'oui', 'y', 'yes']:
        results.append(("Test système complet", run_quick_test()))
    
    # Summary
    print("\n" + "=" * 70)
    print("RÉSUMÉ DES TESTS")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    print(f"Score: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 Félicitations! Votre environnement est prêt.")
        print("Vous pouvez maintenant lancer l'expérience avec: python main.py")
    elif passed >= total - 2:
        print("\n⚠️  Configuration presque complète.")
        print("Corrigez les erreurs ci-dessus avant de lancer l'expérience.")
    else:
        print("\n❌ Configuration incomplète.")
        print("Suivez le guide d'installation (GUIDE_INSTALLATION.md)")
    
    print()

if __name__ == "__main__":
    main()

