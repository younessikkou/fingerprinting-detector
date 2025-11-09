"""
Script de téléchargement automatique des drivers
Télécharge et installe automatiquement ChromeDriver et GeckoDriver
"""
import os
import shutil
from pathlib import Path

def download_chromedriver():
    """Télécharge automatiquement ChromeDriver compatible"""
    try:
        print("📥 Téléchargement de ChromeDriver...")
        print("   (Cela peut prendre quelques secondes...)")
        
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        # Télécharger via webdriver-manager
        driver_path = ChromeDriverManager().install()
        print(f"✅ Téléchargé: {driver_path}")
        
        # Copier vers le dossier doctorat
        dest = r"C:\Users\PC\Desktop\doctorat\chromedriver.exe"
        
        # Créer le dossier s'il n'existe pas
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        
        shutil.copy2(driver_path, dest)
        print(f"✅ Copié vers: {dest}")
        
        # Vérifier la version
        import subprocess
        try:
            result = subprocess.run([dest, "--version"], capture_output=True, text=True)
            version = result.stdout.strip()
            print(f"   Version: {version}")
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("\nSolution alternative:")
        print("1. Allez sur: https://googlechromelabs.github.io/chrome-for-testing/")
        print("2. Téléchargez ChromeDriver pour votre version de Chrome")
        print("3. Extrayez et copiez chromedriver.exe vers C:\\Users\\PC\\Desktop\\doctorat\\")
        return False

def download_geckodriver():
    """Télécharge automatiquement GeckoDriver"""
    try:
        print("📥 Téléchargement de GeckoDriver...")
        print("   (Cela peut prendre quelques secondes...)")
        
        from selenium import webdriver
        from selenium.webdriver.firefox.service import Service
        from webdriver_manager.firefox import GeckoDriverManager
        
        # Télécharger via webdriver-manager
        driver_path = GeckoDriverManager().install()
        print(f"✅ Téléchargé: {driver_path}")
        
        # Copier vers le dossier doctorat
        dest = r"C:\Users\PC\Desktop\doctorat\geckodriver.exe"
        
        # Créer le dossier s'il n'existe pas
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        
        shutil.copy2(driver_path, dest)
        print(f"✅ Copié vers: {dest}")
        
        # Vérifier la version
        import subprocess
        try:
            result = subprocess.run([dest, "--version"], capture_output=True, text=True)
            version = result.stdout.split('\n')[0]
            print(f"   Version: {version}")
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("\nSolution alternative:")
        print("1. Allez sur: https://github.com/mozilla/geckodriver/releases")
        print("2. Téléchargez geckodriver-vX.X.X-win64.zip")
        print("3. Extrayez et copiez geckodriver.exe vers C:\\Users\\PC\\Desktop\\doctorat\\")
        return False

def main():
    """Point d'entrée principal"""
    print("=" * 70)
    print("TÉLÉCHARGEMENT AUTOMATIQUE DES DRIVERS")
    print("=" * 70)
    print()
    print("Ce script va télécharger et installer automatiquement:")
    print("  - ChromeDriver (compatible avec votre version de Chrome)")
    print("  - GeckoDriver (pour Firefox)")
    print()
    print("Destination: C:\\Users\\PC\\Desktop\\doctorat\\")
    print()
    
    input("Appuyez sur Entrée pour continuer...")
    print()
    
    # Télécharger ChromeDriver
    print("-" * 70)
    print("1. CHROMEDRIVER")
    print("-" * 70)
    chrome_ok = download_chromedriver()
    print()
    
    # Télécharger GeckoDriver
    print("-" * 70)
    print("2. GECKODRIVER")
    print("-" * 70)
    firefox_ok = download_geckodriver()
    print()
    
    # Résumé
    print("=" * 70)
    print("RÉSUMÉ")
    print("=" * 70)
    
    if chrome_ok:
        print("✅ ChromeDriver installé avec succès")
    else:
        print("❌ ChromeDriver: échec du téléchargement")
    
    if firefox_ok:
        print("✅ GeckoDriver installé avec succès")
    else:
        print("❌ GeckoDriver: échec du téléchargement")
    
    print()
    
    if chrome_ok and firefox_ok:
        print("🎉 Tous les drivers ont été installés!")
        print()
        print("Prochaines étapes:")
        print("  1. Relancez: python test_setup.py")
        print("  2. Tous les tests devraient passer maintenant")
        print("  3. Lancez l'expérience: python main.py")
    elif chrome_ok or firefox_ok:
        print("⚠️ Certains téléchargements ont échoué.")
        print("Consultez TELECHARGER_DRIVERS.md pour les instructions manuelles.")
    else:
        print("❌ Les téléchargements ont échoué.")
        print("Consultez TELECHARGER_DRIVERS.md pour les instructions manuelles.")
    
    print("=" * 70)
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrompu par l'utilisateur.")
    except Exception as e:
        print(f"\n\nErreur inattendue: {e}")
        print("\nConsultez TELECHARGER_DRIVERS.md pour les instructions manuelles.")




