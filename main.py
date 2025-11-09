"""
Browser Fingerprinting Detection Experiment
Main automation script using Selenium WebDriver
Supports Chromium and Firefox browsers on Windows 10
"""

import os
import json
import time
import random
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import math

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fingerprinting_experiment.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class EntropyCalculator:
    """Calculate Shannon entropy for browser attributes"""
    
    @staticmethod
    def calculate_shannon_entropy(data: List[str]) -> float:
        """
        Calculate Shannon entropy for a list of values
        H(X) = -Σ p(x) * log2(p(x))
        
        Args:
            data: List of attribute values
            
        Returns:
            Shannon entropy value in bits
        """
        if not data:
            return 0.0
        
        # Count frequencies
        freq_dict = {}
        for item in data:
            item_str = str(item)
            freq_dict[item_str] = freq_dict.get(item_str, 0) + 1
        
        # Calculate probabilities and entropy
        entropy = 0.0
        total = len(data)
        
        for count in freq_dict.values():
            probability = count / total
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    @staticmethod
    def calculate_attribute_entropies(fingerprint_data: Dict) -> Dict[str, float]:
        """
        Calculate entropy for each category of fingerprinting attributes
        
        Args:
            fingerprint_data: Dictionary containing captured fingerprint data
            
        Returns:
            Dictionary mapping category names to entropy values
        """
        entropies = {}
        
        for category, calls in fingerprint_data.items():
            if isinstance(calls, list) and calls:
                # Extract values from API calls
                values = [str(call.get('value', '')) for call in calls if 'value' in call]
                if values:
                    entropies[category] = EntropyCalculator.calculate_shannon_entropy(values)
                else:
                    entropies[category] = 0.0
            else:
                entropies[category] = 0.0
        
        # Calculate total entropy
        all_values = []
        for calls in fingerprint_data.values():
            if isinstance(calls, list):
                all_values.extend([str(call.get('value', '')) for call in calls if 'value' in call])
        
        entropies['total'] = EntropyCalculator.calculate_shannon_entropy(all_values)
        
        return entropies


class BrowserSession:
    """Manages a browser session for fingerprinting detection"""
    
    def __init__(self, browser_type: str, detector_script_path: str):
        """
        Initialize browser session
        
        Args:
            browser_type: Either 'chrome' or 'firefox'
            detector_script_path: Path to the detector.js file
        """
        self.browser_type = browser_type
        self.driver = None
        self.detector_script = self._load_detector_script(detector_script_path)
        
    def _load_detector_script(self, script_path: str) -> str:
        """Load the JavaScript detection module"""
        with open(script_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def start(self):
        """Start the browser session"""
        try:
            if self.browser_type == 'chrome':
                self._start_chrome()
            elif self.browser_type == 'firefox':
                self._start_firefox()
            else:
                raise ValueError(f"Unsupported browser type: {self.browser_type}")
            
            logger.info(f"Started {self.browser_type} browser session")
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise
    
    def _start_chrome(self):
        """Start Chrome/Chromium browser"""
        options = ChromeOptions()
        
        # Disable automation detection
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Add realistic user preferences
        prefs = {
            "profile.default_content_setting_values": {
                "notifications": 2  # Block notifications
            },
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        options.add_experimental_option("prefs", prefs)
        
        # Headless mode (invisible browser)
        options.add_argument('--headless=new')
        
        # Disable logging
        options.add_argument('--log-level=3')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Use temporary user data directory to avoid conflicts with open Chrome instances
        import tempfile
        import os
        import time
        import random
        temp_dir = os.path.join(tempfile.gettempdir(), f'chrome_selenium_{int(time.time())}_{os.getpid()}_{random.randint(1000,9999)}')
        os.makedirs(temp_dir, exist_ok=True)
        options.add_argument(f'--user-data-dir={temp_dir}')
        
        # Additional arguments to ensure complete isolation
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-background-networking')
        options.add_argument('--disable-sync')
        options.add_argument('--disable-translate')
        options.add_argument('--disable-features=TranslateUI')
        options.add_argument('--disable-features=Translate')
        options.add_argument('--metrics-recording-only')
        options.add_argument('--no-first-run')
        options.add_argument('--safebrowsing-disable-auto-update')
        options.add_argument('--disable-client-side-phishing-detection')
        options.add_argument('--disable-component-update')
        options.add_argument('--disable-hang-monitor')
        options.add_argument('--disable-prompt-on-repost')
        options.add_argument('--disable-domain-reliability')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-ipc-flooding-protection')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        
        # Use specific ChromeDriver path
        chromedriver_path = r"C:\Users\PC\Desktop\doctorat\chromedriver.exe"
        service = ChromeService(executable_path=chromedriver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        
        # Remove webdriver property
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            '''
        })
    
    def _start_firefox(self):
        """Start Firefox browser"""
        options = FirefoxOptions()
        
        # Headless mode (invisible browser)
        options.add_argument('-headless')
        
        # Set preferences to appear more realistic
        options.set_preference('dom.webdriver.enabled', False)
        options.set_preference('useAutomationExtension', False)
        options.set_preference('dom.webnotifications.enabled', False)
        
        # Use specific GeckoDriver path
        geckodriver_path = r"C:\Users\PC\Desktop\doctorat\geckodriver.exe"
        service = FirefoxService(executable_path=geckodriver_path)
        self.driver = webdriver.Firefox(service=service, options=options)
    
    def visit_website(self, url: str, duration: int = 45) -> Optional[Dict]:
        """
        Visit a website and capture fingerprinting attempts
        
        Args:
            url: Website URL to visit
            duration: Session duration in seconds (default: 45)
            
        Returns:
            Dictionary containing fingerprinting data or None on failure
        """
        try:
            logger.info(f"Visiting {url}")
            
            # Navigate to the website
            self.driver.set_page_load_timeout(30)
            self.driver.get(url)
            
            # Inject the detection script immediately
            self.driver.execute_script(self.detector_script)
            
            # Simulate realistic user behavior
            self._simulate_user_behavior(duration)
            
            # Wait a bit more to ensure all scripts have executed
            time.sleep(2)
            
            # Retrieve collected data
            fingerprint_data = self.driver.execute_script("return window.getFingerprintData();")
            stats = self.driver.execute_script("return window.getFingerprintStats();")
            
            logger.info(f"Captured {stats.get('total', 0)} fingerprinting API calls from {url}")
            
            return fingerprint_data
            
        except TimeoutException:
            logger.warning(f"Timeout loading {url}")
            return None
        except WebDriverException as e:
            logger.error(f"WebDriver error visiting {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error visiting {url}: {e}")
            return None
    
    def _simulate_user_behavior(self, duration: int):
        """
        Simulate realistic user behavior during the session
        
        Args:
            duration: Duration in seconds
        """
        start_time = time.time()
        actions_performed = 0
        
        while time.time() - start_time < duration:
            try:
                # Random actions to trigger scripts
                action = random.choice(['scroll', 'mouse_move', 'wait'])
                
                if action == 'scroll':
                    # Random scroll
                    scroll_amount = random.randint(100, 500)
                    self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    time.sleep(random.uniform(0.5, 2))
                    
                elif action == 'mouse_move':
                    # Move mouse to random element
                    self.driver.execute_script("""
                        var event = new MouseEvent('mousemove', {
                            'view': window,
                            'bubbles': true,
                            'cancelable': true,
                            'clientX': Math.random() * window.innerWidth,
                            'clientY': Math.random() * window.innerHeight
                        });
                        document.dispatchEvent(event);
                    """)
                    time.sleep(random.uniform(0.3, 1))
                    
                else:  # wait
                    time.sleep(random.uniform(1, 3))
                
                actions_performed += 1
                
            except Exception as e:
                logger.debug(f"Minor error during simulation: {e}")
                time.sleep(1)
        
        logger.debug(f"Performed {actions_performed} user actions during {duration}s session")
    
    def close(self):
        """Close the browser session"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info(f"Closed {self.browser_type} browser session")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")


class ExperimentManager:
    """Manages the entire fingerprinting detection experiment"""
    
    def __init__(self, config_path: str = 'config.json'):
        """
        Initialize experiment manager
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.results_dir = Path(self.config.get('results_dir', 'results'))
        self.results_dir.mkdir(exist_ok=True)
        
        self.websites = self._load_websites()
        self.browsers = self.config.get('browsers', ['chrome', 'firefox'])
        self.session_duration = self.config.get('session_duration', 45)
        self.visits_per_browser = self.config.get('visits_per_browser', 2)
        self.days_between_visits = self.config.get('days_between_visits', 15)
        
    def _load_config(self, config_path: str) -> Dict:
        """Load experiment configuration"""
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            logger.warning(f"Config file not found: {config_path}. Using defaults.")
            return {}
    
    def _load_websites(self) -> List[str]:
        """Load list of websites to test"""
        websites_file = self.config.get('websites_file', 'websites.json')
        
        if os.path.exists(websites_file):
            with open(websites_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('websites', [])
        else:
            logger.warning(f"Websites file not found: {websites_file}. Using sample list.")
            # Sample websites for testing
            return [
                'https://www.google.com',
                'https://www.facebook.com',
                'https://www.amazon.com',
                'https://www.youtube.com',
                'https://www.wikipedia.org'
            ]
    
    def run_single_session(self, website: str, browser: str, visit_number: int) -> Dict:
        """
        Run a single test session
        
        Args:
            website: Website URL
            browser: Browser type
            visit_number: Visit number (1 or 2)
            
        Returns:
            Session results dictionary
        """
        session_id = f"{browser}_{website.replace('https://', '').replace('/', '_')}_{visit_number}"
        logger.info(f"Starting session: {session_id}")
        
        session = BrowserSession(browser, 'detector.js')
        
        try:
            session.start()
            fingerprint_data = session.visit_website(website, self.session_duration)
            
            if fingerprint_data:
                # Calculate entropy
                entropy_calculator = EntropyCalculator()
                entropies = entropy_calculator.calculate_attribute_entropies(
                    fingerprint_data.get('data', {})
                )
                
                # Prepare results
                results = {
                    'session_id': session_id,
                    'website': website,
                    'browser': browser,
                    'visit_number': visit_number,
                    'timestamp': datetime.now().isoformat(),
                    'fingerprint_data': fingerprint_data,
                    'entropies': entropies,
                    'success': True
                }
                
                logger.info(f"Session completed. Total entropy: {entropies.get('total', 0):.2f} bits")
                
                return results
            else:
                return {
                    'session_id': session_id,
                    'website': website,
                    'browser': browser,
                    'visit_number': visit_number,
                    'timestamp': datetime.now().isoformat(),
                    'success': False,
                    'error': 'Failed to capture data'
                }
                
        except Exception as e:
            logger.error(f"Session failed: {e}")
            return {
                'session_id': session_id,
                'website': website,
                'browser': browser,
                'visit_number': visit_number,
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'error': str(e)
            }
        finally:
            session.close()
    
    def run_experiment(self, visit_number: int = 1):
        """
        Run the complete experiment for all websites and browsers
        
        Args:
            visit_number: Visit number (1 or 2 for the 15-day protocol)
        """
        logger.info(f"Starting experiment - Visit {visit_number}")
        logger.info(f"Testing {len(self.websites)} websites across {len(self.browsers)} browsers")
        
        all_results = []
        successful_sessions = 0
        failed_sessions = 0
        
        for website in self.websites:
            for browser in self.browsers:
                try:
                    result = self.run_single_session(website, browser, visit_number)
                    all_results.append(result)
                    
                    if result.get('success'):
                        successful_sessions += 1
                    else:
                        failed_sessions += 1
                    
                    # Save individual result
                    self._save_result(result)
                    
                    # Brief pause between sessions
                    time.sleep(random.uniform(2, 5))
                    
                except KeyboardInterrupt:
                    logger.info("Experiment interrupted by user")
                    break
                except Exception as e:
                    logger.error(f"Unexpected error in experiment loop: {e}")
                    failed_sessions += 1
        
        # Generate summary report
        self._generate_summary_report(all_results, visit_number)
        
        logger.info(f"Experiment completed. Successful: {successful_sessions}, Failed: {failed_sessions}")
    
    def _save_result(self, result: Dict):
        """Save individual session result"""
        filename = f"{result['session_id']}_{result['timestamp'].replace(':', '-')}.json"
        filepath = self.results_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
    
    def _generate_summary_report(self, results: List[Dict], visit_number: int):
        """Generate summary report of the experiment"""
        report = {
            'experiment_timestamp': datetime.now().isoformat(),
            'visit_number': visit_number,
            'total_sessions': len(results),
            'successful_sessions': sum(1 for r in results if r.get('success')),
            'failed_sessions': sum(1 for r in results if not r.get('success')),
            'browsers_tested': self.browsers,
            'websites_count': len(self.websites),
            'session_duration': self.session_duration,
            'results_summary': []
        }
        
        # Aggregate statistics
        for result in results:
            if result.get('success'):
                summary_entry = {
                    'website': result['website'],
                    'browser': result['browser'],
                    'total_api_calls': result.get('fingerprint_data', {}).get('data', {}),
                    'entropies': result.get('entropies', {}),
                    'timestamp': result['timestamp']
                }
                report['results_summary'].append(summary_entry)
        
        # Calculate average entropies
        if report['successful_sessions'] > 0:
            all_entropies = [r.get('entropies', {}) for r in results if r.get('success')]
            avg_entropies = {}
            
            if all_entropies:
                categories = all_entropies[0].keys()
                for category in categories:
                    values = [e.get(category, 0) for e in all_entropies if category in e]
                    if values:
                        avg_entropies[category] = sum(values) / len(values)
            
            report['average_entropies'] = avg_entropies
        
        # Save report
        report_filename = f"experiment_report_visit{visit_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = self.results_dir / report_filename
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Summary report saved: {report_path}")


def main():
    """Main entry point"""
    print("=" * 70)
    print("Browser Fingerprinting Detection Experiment")
    print("=" * 70)
    print()
    
    # Initialize experiment
    manager = ExperimentManager()
    
    print(f"Configuration:")
    print(f"  - Browsers: {', '.join(manager.browsers)}")
    print(f"  - Websites: {len(manager.websites)}")
    print(f"  - Session duration: {manager.session_duration}s")
    print(f"  - Visits per browser: {manager.visits_per_browser}")
    print()
    
    # Ask for visit number
    try:
        visit_number = int(input("Enter visit number (1 or 2): ").strip())
        if visit_number not in [1, 2]:
            print("Invalid visit number. Using 1.")
            visit_number = 1
    except ValueError:
        print("Invalid input. Using visit number 1.")
        visit_number = 1
    
    print()
    print("Starting experiment...")
    print()
    
    # Run experiment
    try:
        manager.run_experiment(visit_number)
        print()
        print("Experiment completed successfully!")
        print(f"Results saved in: {manager.results_dir}")
    except KeyboardInterrupt:
        print("\n\nExperiment interrupted by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\n\nExperiment failed: {e}")


if __name__ == "__main__":
    main()

