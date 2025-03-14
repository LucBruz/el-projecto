import numpy as np
from collections import deque

class Instance:
    def __init__(self, fichier):
        self.N, self.H, self.D, self.Td, self.distances, self.scores = self.lire_instance(fichier)
    
    def lire_instance(self, fichier):
        with open(fichier, 'r') as f:
            lignes = [ligne.strip() for ligne in f.readlines() if ligne.strip()]  # Supprime les lignes vides
        
        # Lecture des paramètres
        N, H, D = map(int, lignes[0].split())  # Nombre total de sites, hôtels intermédiaires, jours
        
        # Lecture des distances maximales Td (format unique maintenant)
        Td = list(map(float, lignes[1].split()))
        del lignes[1]  # Supprime cette ligne de Td après extraction
        
        # Lecture des coordonnées et scores
        sites = []
        scores = []
        for ligne in lignes[1:]:  # Reprise après la ligne supprimée
            valeurs = ligne.split()
            if len(valeurs) == 3:  # Vérification standard
                x, y, score = map(float, valeurs)
                sites.append((x, y))  # Stocke uniquement les coordonnées temporairement pour le calcul des distances
                scores.append(int(score))  # Stocke uniquement les scores
        
        # Calculer la matrice des distances et supprimer les coordonnées après usage
        distances = self.calculer_matrice_distances(sites)
        del sites  # On ne garde plus les coordonnées
        
        return N, H, D, Td, distances, scores
    
    def calculer_matrice_distances(self, sites):
        n = len(sites)
        distances = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    distances[i][j] = np.sqrt((sites[i][0] - sites[j][0])**2 + (sites[i][1] - sites[j][1])**2)
        return distances

class PlusProcheVoisinTabou:
    def __init__(self, instance, tabu_size=10, max_iter=100):
        self.instance = instance
        self.tabu_size = tabu_size
        self.max_iter = max_iter
        self.tabu_list = deque(maxlen=tabu_size)
        self.solution = [[] for _ in range(instance.D)]
        self.score_total = 0
    
    def trouver_tournee(self):
        visite = set()
        for jour in range(self.instance.D):
            distance_restante = self.instance.Td[jour]
            position_actuelle = 0  # Hôtel de départ (index 0)
            journee = [position_actuelle]
            
            while distance_restante > 0:
                prochain_site = self.choisir_prochain_site(position_actuelle, distance_restante, visite)
                if prochain_site is None:
                    break  # Plus de site visitable dans la limite de distance
                
                distance_restante -= self.instance.distances[position_actuelle][prochain_site]
                position_actuelle = prochain_site
                journee.append(prochain_site)
                visite.add(prochain_site)
                self.score_total += self.instance.scores[prochain_site]  # Ajout du score du site visité
            
            journee.append(1)  # Retourner à l'hôtel d'arrivée (index 1)
            self.solution[jour] = journee
        
        self.appliquer_recherche_tabou()
        return self.solution
    
    def choisir_prochain_site(self, position_actuelle, distance_restante, visite):
        candidats = [(i, self.instance.distances[position_actuelle][i]) for i in range(2 + self.instance.H, self.instance.N)
                     if i not in visite and self.instance.distances[position_actuelle][i] <= distance_restante]
        
        if not candidats:
            return None
        
        return min(candidats, key=lambda x: x[1])[0]  # Prend le site le plus proche
    
    def appliquer_recherche_tabou(self):
        for _ in range(self.max_iter):
            meilleur_delta = 0
            meilleur_echange = None
            
            for jour in range(self.instance.D):
                for i in range(1, len(self.solution[jour]) - 2):
                    for j in range(i + 1, len(self.solution[jour]) - 1):
                        if (self.solution[jour][i], self.solution[jour][j]) in self.tabu_list:
                            continue  # Ignorer si dans la liste tabou
                        
                        nouvelle_tournee = self.solution[jour][:]
                        nouvelle_tournee[i], nouvelle_tournee[j] = nouvelle_tournee[j], nouvelle_tournee[i]
                        
                        delta = self.calculer_gain(nouvelle_tournee, jour) - self.calculer_gain(self.solution[jour], jour)
                        
                        if delta > meilleur_delta:
                            meilleur_delta = delta
                            meilleur_echange = (jour, i, j)
            
            if meilleur_echange:
                jour, i, j = meilleur_echange
                self.solution[jour][i], self.solution[jour][j] = self.solution[jour][j], self.solution[jour][i]
                self.tabu_list.append((self.solution[jour][i], self.solution[jour][j]))
    
    def calculer_gain(self, tournee, jour):
        return sum(self.instance.scores[site] for site in tournee if site not in [0, 1])

# Charger l'instance
fichier_instance = "instances/instance1.txt"  # Remplace par ton fichier
instance = Instance(fichier_instance)

# Exécuter l'algorithme du Plus Proche Voisin avec Recherche Tabou
algo_ppv_tabou = PlusProcheVoisinTabou(instance)
solution = algo_ppv_tabou.trouver_tournee()

# Afficher la solution
print("--- Solution Heuristique du Plus Proche Voisin (Optimisée avec Recherche Tabou) ---")
for jour, trajet in enumerate(solution):
    print(f"Jour {jour + 1} : {' -> '.join(map(str, trajet))}")

# Afficher le score total obtenu
print(f"\n🔹 Score total obtenu après Recherche Tabou : {algo_ppv_tabou.score_total}")