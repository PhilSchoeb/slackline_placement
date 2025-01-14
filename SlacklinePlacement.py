import csv
import math
import sys

# Matricules des étudiants : 20190448 et 20228889

# Classe Arbre représente un arbre dans le problème présent
class Arbre:
    number = None  # Numéro identificateur de l'arbre
    x = None
    y = None

    # Constructeur d'un arbre
    def __init__(self, number, x, y):
        self.number = int(number)
        self.x = float(x)
        self.y = float(y)

    # Méthodes d'affichage
    def print(self):
        print("(" + str(self.number) + ", " + str(self.x) + ", " + str(self.y) + ")")

    def toString(self):
        return "(" + str(self.number) + ", " + str(self.x) + ", " + str(self.y) + ")"

# Classe Slackline représente une slackline dans le problème présent
class Slackline:
    arbre1 = None
    arbre2 = None
    distance = None

    # Constructeur d'une slackline
    def __init__(self, arbre1, arbre2, distance):
        self.arbre1 = arbre1
        self.arbre2 = arbre2
        self.distance = float(distance)

    # Méthodes d'affichage
    def print(self):
        print("Slackline de " + str(self.arbre1.number) + " et " + str(self.arbre2.number) + " avec distance : "
              + str(self.distance))

    def toString(self):
        return "Slackline de " + str(self.arbre1.number) + " et " + str(self.arbre2.number) + " avec distance : " \
            + str(self.distance)


# Set up pour l'ouverture du fichier à lire
with open('instance_lionais.csv', 'r') as file:

    reader = csv.reader(file)

    header = next(reader)

    listeArbres = []
    num = 1  # Le numéro associé à l'arbre
    for row in reader:
        if float(row[14]) >= 25:  # Seulement considérer les arbres de diamètre supérieur ou égal à 25
            newArbre = Arbre(0, 0, 0)
            newArbre.number = num
            newArbre.x = float(row[8])
            newArbre.y = float(row[9])
            listeArbres.append(newArbre)
        num += 1

# Création de toutes slacklines possibles
listeSL = []
for i in range(len(listeArbres) - 1):
    arbre1 = listeArbres[i]
    for j in range(i+1, len(listeArbres)):
        arbre2 = listeArbres[j]
        distance = math.sqrt((arbre2.x - arbre1.x)**2 + (arbre2.y - arbre1.y)**2)
        if 5 <= distance <= 30:
            slackline = Slackline(arbre1, arbre2, distance)
            listeSL.append(slackline)

# Fonction qui tri une liste de slacklines en ordre décroissant de leur longueur (attribut distance)
# avec la méthode du tri fusion.
def triFusionDistance(tab):
    # Cas de base
    if len(tab) == 1:
        return tab
    # Cas récursif
    tab1 = tab[0:math.floor(len(tab)/2)]
    tab2 = tab[math.floor(len(tab)/2):len(tab)]
    tabTri1 = triFusionDistance(tab1)
    tabTri2 = triFusionDistance(tab2)
    tabTri = []
    i = 0
    j = 0
    while i < len(tabTri1) or j < len(tabTri2):
        # Si tabTri1 a été vidé
        if i == len(tabTri1):
            tabTri.append(tabTri2[j])
            j += 1
        # Si tabTri2 a été vidé
        elif j == len(tabTri2):
            tabTri.append(tabTri1[i])
            i += 1
        # Comparaison de la slackline de tabTri1 à celle de tabTri2
        elif tabTri1[i].distance > tabTri2[j].distance:
            tabTri.append(tabTri1[i])
            i += 1
        else:
            tabTri.append(tabTri2[j])
            j += 1
    return tabTri

# Fonction qui enlève les slacklines qui croisent celle sélectionnée (sl) dans la liste des slacklines (tabSL)
# La méthode suivie ne provient pas d'une source extérieure
def update(tabSL, sl):
    tabRemoveSL = []  # Tableau qui contient les slacklines à enlever
    # Regarder d'abord si la droite caractéristique de sl est caractérisée par x = k ou k est une constante
    if (sl.arbre2.x - sl.arbre1.x) == 0:
        # On doit s'occuper de ce cas, car lorsque la droite caractéristique de sl n'est pas une fonction,
        # cela change notre approche.
        separationX = sl.arbre1.x
        for slLeft in tabSL:  # Itération sur toutes les slacklines restantes
            # Trouver les coordonnées des arbres 1 et 2 de slLeft
            x1 = slLeft.arbre1.x
            y1 = slLeft.arbre1.y
            x2 = slLeft.arbre2.x
            y2 = slLeft.arbre2.y
            if (x1 < separationX and x2 < separationX) or (x1 > separationX and x2 > separationX):
                # Pas de croisement, car les deux arbres sont dans le même demi plan
                # (on sépare le plan avec l'équation de sl)
                continue
            else:
                # Regarder d'abord si slLeft est parallèle à sl (de la forme x = k)
                if x2 - x1 == 0:
                    # La droite caractéristique de slLeft est la même que celle de sl car on s'est occupé des cas
                    # quand les deux points sont dans le même demi plan.
                    # Regarder si elles se croisent.
                    # avant est true si slLeft est avant sl (contient des y plus petits)
                    avant = y1 <= sl.arbre1.y and y1 <= sl.arbre2.y and y2 <= sl.arbre1.y and y2 <= sl.arbre2.y
                    # apres est true si slLeft est apres sl (contient des y plus grands)
                    apres = y1 >= sl.arbre1.y and y1 >= sl.arbre2.y and y2 >= sl.arbre1.y and y2 >= sl.arbre2.y
                    if avant or apres:
                        # Pas de croisement
                        continue
                    else:
                        # sl et slLeft se croisent
                        tabRemoveSL.append(slLeft)
                        continue

                # slLeft n'est pas parallèle à sl
                # Trouver la droite de la slackline slLeft
                tauxSLLeft = (y2 - y1) / (x2 - x1)
                ordSLLeft = y1 - (tauxSLLeft * x1)

                # On sait que sl et slLeft ne sont pas parallèles donc si slLeft part d'un des arbres
                # de sl, il n'y a pas de croisement.
                if slLeft.arbre1 == sl.arbre1 or slLeft.arbre1 == sl.arbre2 or slLeft.arbre2 == sl.arbre1 \
                        or slLeft.arbre2 == sl.arbre2:
                    continue

                # Trouver l'intersection entre la droite de sl et la droite de slLeft
                yInter = (tauxSLLeft * separationX) + ordSLLeft
                # Ce critère fonctionne, car on travaille avec des droites
                if (yInter < sl.arbre1.y and yInter < sl.arbre2.y) or \
                        (yInter > sl.arbre1.y and yInter > sl.arbre2.y):
                    # Dans ce cas, l'intersection n'est pas sur la slackline sl
                    continue
                else:
                    # Dans ce cas, slLeft et sl se croisent
                    tabRemoveSL.append(slLeft)
                    continue

    # Ici la droite caractéristique de sl est une fonction
    else:
        # Calcul l'équation de la droite de sl
        taux = (sl.arbre2.y - sl.arbre1.y)/(sl.arbre2.x - sl.arbre1.x)
        ord = sl.arbre1.y - (taux * sl.arbre1.x)

        for slLeft in tabSL:
            # Trouver les coordonnées des arbres 1 et 2 de slLeft
            x1 = slLeft.arbre1.x
            y1 = slLeft.arbre1.y
            x2 = slLeft.arbre2.x
            y2 = slLeft.arbre2.y
            if (y1 > taux * x1 + ord and y2 > taux * x2 + ord) or (y1 < taux * x1 + ord and y2 < taux * x2 + ord):
                # Pas de croisement, car les deux arbres sont dans le même demi plan
                # (on sépare le plan avec l'équation de sl)
                continue
            else:
                # Regarder d'abord si slLeft est caractérisée par x = k ou k est une constante
                if x2 - x1 == 0:
                    # La droite caractéristique de slLeft n'est pas une fonction
                    xSLLeft = x1  # L'équation de slLeft est : x = xSLLeft

                    # Si sl et slLeft ont un arbre en commun, elles ne se croisent pas
                    if slLeft.arbre1 == sl.arbre1 or slLeft.arbre1 == sl.arbre2 or slLeft.arbre2 == sl.arbre1 \
                            or slLeft.arbre2 == sl.arbre2:
                        # Pas de croisement
                        continue

                    if (xSLLeft < sl.arbre1.x and xSLLeft < sl.arbre2.x) or \
                            (xSLLeft > sl.arbre1.x and xSLLeft > sl.arbre2.x):
                        # slLeft est complètement avant ou après sl
                        continue
                    else:
                        # Trouver le y du point d'intersection
                        yInter = (taux * xSLLeft) + ord
                        if (yInter < y1 and yInter < y2) or (yInter > y1 and yInter > y2):
                            # Pas de croisement
                            continue
                        else:
                            # Il y a croisement
                            tabRemoveSL.append(slLeft)
                            continue

                # slLeft est caractérisée par une fonction
                # Trouver la droite de la slackline slLeft
                tauxSLLeft = (y2 - y1)/(x2 - x1)
                ordSLLeft = y1 - (tauxSLLeft * x1)

                # Si sl et slLeft sont parallèles
                if taux == tauxSLLeft:
                    # Si leur ordonnée à l'origine est différent
                    if ord != ordSLLeft:
                        # Pas de croisement
                        continue
                    else:
                        # avant est true si slLeft est avant sl en coordonnées x
                        avant = x1 <= sl.arbre1.x and x1 <= sl.arbre2.x and x2 <= sl.arbre1.x and x2 <= sl.arbre2.x
                        # apres est true si slLeft est apres sl en coordonnées x
                        apres = x1 >= sl.arbre1.x and x1 >= sl.arbre2.x and x2 >= sl.arbre1.x and x2 >= sl.arbre2.x
                        if avant or apres:
                            # Pas de croisement
                            continue
                        else:
                            # slLeft et sl se croisent
                            tabRemoveSL.append(slLeft)
                            continue

                # On sait que sl et slLeft ne sont pas parallèles donc si slLeft part d'un des arbres
                # de sl, il n'y a pas de croisement
                if slLeft.arbre1 == sl.arbre1 or slLeft.arbre1 == sl.arbre2 or slLeft.arbre2 == sl.arbre1 \
                        or slLeft.arbre2 == sl.arbre2:
                    continue

                # Trouver le x de l'intersection entre la droite de sl et la droite de slLeft
                xInter = (ordSLLeft - ord) / (taux - tauxSLLeft)

                # Ce critère fonctionne, car on travaille avec des droites
                if (xInter < sl.arbre1.x and xInter < sl.arbre2.x) or \
                        (xInter > sl.arbre1.x and xInter > sl.arbre2.x):
                    # Dans ce cas, l'intersection n'est pas sur la slackline sl
                    continue
                else:
                    # Dans ce cas, slLeft et sl se croisent
                    tabRemoveSL.append(slLeft)

    # Suppression des slacklines croisées avec sl
    for slRemove in tabRemoveSL:
        tabSL.remove(slRemove)

    return tabSL


# Algorithme vorace
listeSLTri = triFusionDistance(listeSL)
listeSelectedSL = []  # Tableau contenant les slacklines sélectionnées
# Tant qu'il reste des slacklines possibles
while len(listeSLTri) != 0:
    # Prendre la plus grande
    selectedSL = listeSLTri.pop(0)
    listeSelectedSL.append(selectedSL)
    listeSLTri = update(listeSLTri, selectedSL)  # Update la liste de slacklines possibles


# Création du texte contenu dans le csv écrit
text = ""
for sl in listeSelectedSL:
    text += str(sl.arbre1.number) + "," + str(sl.arbre2.number) + "\n"

# Set up pour l'écriture du csv qui contient le résultat
nomFile = "resultat_parc_ex.csv"
with open(nomFile, 'w') as file2:
    file2.write(text)

