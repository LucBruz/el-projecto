def load_from_file(fichier):
    with open(fichier, 'r') as f:
        lignes = f.readlines()

    # Lecture des paramètres
    N, H, D = map(int, lignes[0].split())  # Nombre total de sites, hôtels intermédiaires, jours
    Td = list(map(float, lignes[1].split()))  # Distances maximales par jour

    # Lecture des coordonnées et scores
    sites = []
    for ligne in lignes[2:]:
        x = list(map(float, ligne.split()))
        y = list(map(float, ligne.split()))
        si = list(map(float, ligne.split()))
        sites.append((x, y, si))


    return N, H, D, Td, sites



if __name__ == '__main__':
    filename = "./instances/instance1.txt"
    N, H, D, td, sites = load_from_file(filename)
    print("N", N)
    print("H", H)
    print("D", D)
    print("td", td)
    print("sites",sites)

