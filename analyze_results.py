"""
Results Analysis Script for Fingerprinting Detection Experiment
Generates comprehensive analysis and visualizations of collected data
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from collections import defaultdict, Counter


class ResultsAnalyzer:
    """Analyze fingerprinting detection results"""
    
    def __init__(self, results_dir: str = 'results'):
        self.results_dir = Path(results_dir)
        self.results = self._load_results()
    
    def _load_results(self) -> List[Dict]:
        """Load all result files"""
        results = []
        
        if not self.results_dir.exists():
            print(f"Results directory not found: {self.results_dir}")
            return results
        
        for file in self.results_dir.glob('*.json'):
            # Skip report files
            if 'report' in file.name:
                continue
            
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    results.append(data)
            except Exception as e:
                print(f"Error loading {file}: {e}")
        
        return results
    
    def print_overall_statistics(self):
        """Print overall experiment statistics"""
        print("\n" + "=" * 70)
        print("STATISTIQUES GÉNÉRALES")
        print("=" * 70)
        
        total = len(self.results)
        successful = [r for r in self.results if r.get('success')]
        failed = [r for r in self.results if not r.get('success')]
        
        print(f"\nNombre total de sessions: {total}")
        print(f"  ✓ Réussies: {len(successful)} ({len(successful)/total*100:.1f}%)")
        print(f"  ✗ Échouées: {len(failed)} ({len(failed)/total*100:.1f}%)")
        
        # Browser statistics
        browsers = Counter(r.get('browser') for r in self.results)
        print(f"\nRépartition par navigateur:")
        for browser, count in browsers.items():
            print(f"  - {browser}: {count} sessions")
        
        # Visit statistics
        visits = Counter(r.get('visit_number') for r in self.results)
        print(f"\nRépartition par visite:")
        for visit, count in visits.items():
            print(f"  - Visite {visit}: {count} sessions")
        
        return len(successful), len(failed)
    
    def print_entropy_analysis(self):
        """Analyze and print entropy statistics"""
        print("\n" + "=" * 70)
        print("ANALYSE DE L'ENTROPIE (Shannon)")
        print("=" * 70)
        
        successful = [r for r in self.results if r.get('success') and 'entropies' in r]
        
        if not successful:
            print("\nAucune donnée d'entropie disponible.")
            return
        
        # Calculate average entropies by category
        categories = set()
        for r in successful:
            categories.update(r['entropies'].keys())
        
        category_entropies = defaultdict(list)
        for r in successful:
            for cat, val in r['entropies'].items():
                category_entropies[cat].append(val)
        
        # Print averages
        print("\nEntropie moyenne par catégorie:")
        print(f"{'Catégorie':<25} {'Moyenne (bits)':<15} {'Min':<10} {'Max':<10}")
        print("-" * 70)
        
        # Sort by average entropy (descending)
        sorted_cats = sorted(
            category_entropies.items(),
            key=lambda x: sum(x[1]) / len(x[1]) if x[1] else 0,
            reverse=True
        )
        
        for cat, values in sorted_cats:
            if values:
                avg = sum(values) / len(values)
                min_val = min(values)
                max_val = max(values)
                print(f"{cat:<25} {avg:>10.2f}     {min_val:>7.2f}    {max_val:>7.2f}")
        
        # Overall entropy distribution
        if 'total' in category_entropies:
            total_entropies = category_entropies['total']
            avg_total = sum(total_entropies) / len(total_entropies)
            print(f"\n{'TOTAL':<25} {avg_total:>10.2f}     {min(total_entropies):>7.2f}    {max(total_entropies):>7.2f}")
    
    def print_top_fingerprinting_sites(self, top_n: int = 20):
        """Print sites with highest fingerprinting activity"""
        print("\n" + "=" * 70)
        print(f"TOP {top_n} SITES AVEC LE PLUS DE FINGERPRINTING")
        print("=" * 70)
        
        successful = [r for r in self.results if r.get('success') and 'entropies' in r]
        
        if not successful:
            print("\nAucune donnée disponible.")
            return
        
        # Sort by total entropy
        sorted_results = sorted(
            successful,
            key=lambda x: x['entropies'].get('total', 0),
            reverse=True
        )
        
        print(f"\n{'#':<4} {'Site':<45} {'Entropie':<12} {'Navigateur':<10}")
        print("-" * 70)
        
        for i, result in enumerate(sorted_results[:top_n], 1):
            website = result['website'][:43] + '...' if len(result['website']) > 45 else result['website']
            entropy = result['entropies'].get('total', 0)
            browser = result['browser']
            print(f"{i:<4} {website:<45} {entropy:>8.2f}     {browser:<10}")
    
    def print_fingerprinting_techniques(self):
        """Analyze which fingerprinting techniques are most common"""
        print("\n" + "=" * 70)
        print("TECHNIQUES DE FINGERPRINTING DÉTECTÉES")
        print("=" * 70)
        
        successful = [r for r in self.results if r.get('success') and 'fingerprint_data' in r]
        
        if not successful:
            print("\nAucune donnée disponible.")
            return
        
        # Count API calls by category
        technique_counts = defaultdict(int)
        technique_sites = defaultdict(set)
        
        for result in successful:
            website = result['website']
            fp_data = result['fingerprint_data'].get('data', {})
            
            for category, calls in fp_data.items():
                if isinstance(calls, list) and calls:
                    technique_counts[category] += len(calls)
                    technique_sites[category].add(website)
        
        # Sort by number of API calls
        sorted_techniques = sorted(
            technique_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        print(f"\n{'Technique':<20} {'API Calls':<12} {'Sites':<12} {'Prévalence':<15}")
        print("-" * 70)
        
        total_sites = len(set(r['website'] for r in successful))
        
        for technique, count in sorted_techniques:
            if count > 0:
                sites_count = len(technique_sites[technique])
                prevalence = sites_count / total_sites * 100
                print(f"{technique:<20} {count:>10}   {sites_count:>10}   {prevalence:>10.1f}%")
    
    def print_browser_comparison(self):
        """Compare fingerprinting between browsers"""
        print("\n" + "=" * 70)
        print("COMPARAISON ENTRE NAVIGATEURS")
        print("=" * 70)
        
        successful = [r for r in self.results if r.get('success') and 'entropies' in r]
        
        if not successful:
            print("\nAucune donnée disponible.")
            return
        
        # Group by browser
        by_browser = defaultdict(list)
        for r in successful:
            by_browser[r['browser']].append(r['entropies'].get('total', 0))
        
        print(f"\n{'Navigateur':<15} {'Sessions':<12} {'Entropie moy.':<15} {'Min':<10} {'Max':<10}")
        print("-" * 70)
        
        for browser, entropies in sorted(by_browser.items()):
            avg = sum(entropies) / len(entropies)
            min_val = min(entropies)
            max_val = max(entropies)
            print(f"{browser:<15} {len(entropies):>10}   {avg:>12.2f}    {min_val:>7.2f}    {max_val:>7.2f}")
    
    def print_temporal_analysis(self):
        """Analyze changes between first and second visits"""
        print("\n" + "=" * 70)
        print("ANALYSE TEMPORELLE (Visite 1 vs Visite 2)")
        print("=" * 70)
        
        successful = [r for r in self.results if r.get('success') and 'entropies' in r]
        
        # Group by visit number
        by_visit = defaultdict(list)
        for r in successful:
            by_visit[r['visit_number']].append(r['entropies'].get('total', 0))
        
        if 1 in by_visit and 2 in by_visit:
            visit1_avg = sum(by_visit[1]) / len(by_visit[1])
            visit2_avg = sum(by_visit[2]) / len(by_visit[2])
            
            print(f"\nVisite 1: {len(by_visit[1])} sessions, entropie moyenne = {visit1_avg:.2f} bits")
            print(f"Visite 2: {len(by_visit[2])} sessions, entropie moyenne = {visit2_avg:.2f} bits")
            
            diff = visit2_avg - visit1_avg
            diff_pct = (diff / visit1_avg * 100) if visit1_avg > 0 else 0
            
            print(f"\nDifférence: {diff:+.2f} bits ({diff_pct:+.1f}%)")
            
            if abs(diff) < 0.5:
                print("→ Stabilité temporelle: ÉLEVÉE (peu de changement)")
            elif abs(diff) < 2:
                print("→ Stabilité temporelle: MOYENNE")
            else:
                print("→ Stabilité temporelle: FAIBLE (changement important)")
        else:
            print("\nDonnées insuffisantes pour l'analyse temporelle.")
            print(f"Visites disponibles: {list(by_visit.keys())}")
    
    def print_geographic_analysis(self):
        """Analyze by geographic region"""
        print("\n" + "=" * 70)
        print("ANALYSE GÉOGRAPHIQUE")
        print("=" * 70)
        
        # Simple geographic classification based on domain
        europe_domains = ['.de', '.fr', '.uk', '.es', '.it', '.nl', '.be', '.ch', '.at']
        asia_domains = ['.cn', '.jp', '.kr', '.in', '.sg']
        
        successful = [r for r in self.results if r.get('success') and 'entropies' in r]
        
        regions = {
            'Europe': [],
            'Amérique du Nord': [],
            'Asie': [],
            'Autre': []
        }
        
        for r in successful:
            website = r['website']
            entropy = r['entropies'].get('total', 0)
            
            if any(domain in website for domain in europe_domains):
                regions['Europe'].append(entropy)
            elif any(domain in website for domain in asia_domains):
                regions['Asie'].append(entropy)
            elif '.com' in website or '.org' in website:
                regions['Amérique du Nord'].append(entropy)
            else:
                regions['Autre'].append(entropy)
        
        print(f"\n{'Région':<20} {'Sites':<12} {'Entropie moy.':<15}")
        print("-" * 50)
        
        for region, entropies in regions.items():
            if entropies:
                avg = sum(entropies) / len(entropies)
                print(f"{region:<20} {len(entropies):>10}   {avg:>12.2f}")
    
    def export_csv_summary(self, output_file: str = 'results_summary.csv'):
        """Export results summary to CSV"""
        import csv
        
        output_path = self.results_dir / output_file
        
        successful = [r for r in self.results if r.get('success')]
        
        if not successful:
            print("Aucune donnée à exporter.")
            return
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Website', 'Browser', 'Visit', 'Timestamp', 
                'Total_Entropy', 'Canvas_Entropy', 'WebGL_Entropy', 
                'Audio_Entropy', 'Navigator_Entropy', 'Success'
            ])
            
            # Data
            for r in successful:
                entropies = r.get('entropies', {})
                writer.writerow([
                    r.get('website', ''),
                    r.get('browser', ''),
                    r.get('visit_number', ''),
                    r.get('timestamp', ''),
                    entropies.get('total', 0),
                    entropies.get('canvas', 0),
                    entropies.get('webgl', 0),
                    entropies.get('audio', 0),
                    entropies.get('navigator', 0),
                    r.get('success', False)
                ])
        
        print(f"\n✓ Résumé exporté: {output_path}")
    
    def generate_complete_report(self):
        """Generate complete analysis report"""
        print("\n" + "=" * 70)
        print("RAPPORT COMPLET D'ANALYSE - DÉTECTION DE FINGERPRINTING")
        print("=" * 70)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Dossier des résultats: {self.results_dir}")
        
        if not self.results:
            print("\n⚠ Aucun résultat trouvé.")
            print("Assurez-vous que l'expérience a été exécutée et que les fichiers sont dans le dossier 'results/'.")
            return
        
        # All sections
        self.print_overall_statistics()
        self.print_entropy_analysis()
        self.print_top_fingerprinting_sites()
        self.print_fingerprinting_techniques()
        self.print_browser_comparison()
        self.print_temporal_analysis()
        self.print_geographic_analysis()
        
        # Export CSV
        print("\n" + "=" * 70)
        print("EXPORT DES DONNÉES")
        print("=" * 70)
        self.export_csv_summary()
        
        print("\n" + "=" * 70)
        print("FIN DU RAPPORT")
        print("=" * 70)
        print()


def main():
    """Main entry point"""
    print("\n" + "=" * 70)
    print("ANALYSEUR DE RÉSULTATS - DÉTECTION DE FINGERPRINTING")
    print("=" * 70)
    
    analyzer = ResultsAnalyzer()
    analyzer.generate_complete_report()


if __name__ == "__main__":
    main()

