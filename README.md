# slackline_placement
Résolution algorithmique d'un problème de placement de slacklines - Introduction à l'algorithmique (IFT2125).

Utilisation d'un algorithme glouton afin de trouver l'ensemble des slacklines qui maximise la longueur totale de slacklines dans un parc sans que ces dernières se croisent. Le fichier "instance_lionais.csv" est un exemple d'input.

### Discussion

D'abord il faut savoir que nous avons mis dans une liste toutes les slacklines possibles entre 5 et 30 mètres et attachées à des arbres de diamètre d'au moins 25 cm. De plus, nous avons trier la liste en ordre décroissant par rapport à la longueur des slacklines. La stratégie vorace utilisée est de sélectionner la première slackline (la plus longue), l'enlever de la liste, puis on enlève toute slackline qui croise cette dernière dans la liste contenant le reste. Ensuite, on sélectionne la première slackline encore et on fait les mêmes opérations jusqu'à ce que la liste soit vide.

Pour la complexité théorique, considérons le pire cas d'une entrée de n arbres qui ont tous un diamètre supérieur ou égal à 25 cm. Au début, l'opération de créer une slackline entre chaque arbres est dans $O(n^2)$. La fonction de triFusion est dans $O(nlog(n))$. La fonction update (qui dans le pire cas prend un tableau de slacklines dont  la taille est dans $O(n^2)$ en paramètre) est dans $O(n^2)$. Pour ce qui est de l'algorithme vorace, il va être effectué un nombre de fois dans $O(n)$ car le nombre d'arêtes maximum qu'on peut prendre sans qu'elles se croisent est en $O(n)$. À chaque itération, le triFusion et l'update sont appelés donc on en conclue que tout l'algorithme est dans $O(n^3)$.

Finalement, parlons de la complexité empirique, soit du temps d'exécution en fonction de l'entrée. En prennant la plus grosse entrée : instance\_jarry, qui contient 2407 arbres, le temps pris est d'environ 0,95 seconde. Alors qu'avec le plus petit : insance\_lionais, qui contient 20 arbres, seulement 5 de bons diamètres, le temps pris est d'environ 0,001 seconde.

02/2023
