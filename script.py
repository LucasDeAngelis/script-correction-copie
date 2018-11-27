# On importe la bibliothèque csv dont on aura besoin pour lire et écrire des csv
import csv

# Ces deux variables sont les entrées et sorties du script
objet_formate = []
resultats = []

# On a besoin de ces deux variables pour faire des boucles correctes
nb_questions = 0
nb_eleves = 0
# On avancera dans les réponses de chaque élève en même temps que dans cette liste de bonnes réponses pour les comparer
bonne_reponses = []


# Cette fonction prends en paramètre les résultats du google form reformattés par la fonction de lecture, et renvoie l'objet résultat prêt à être écrit dans le resultats.csv
def fonction_traitement(input):
    # On initialise la valeur retour de la fonction
    output = []

    # On parcours chaque tuples, avec un tuple par élève
    for x in range(nb_eleves):
        # partieEnt est le tuple correspondant à l'input de l'élève actuel
        partieEnt = input[x]
        # partieSor est le tuple correspondant à l'output de l'élève actuel
        partieSor = []
        # La notre qu'on attribuera à l'élève
        note = 0

        # On met le nom de l'élève en premier dans partieSor
        partieSor.append(partieEnt[-1])

        # On parcours ensuite toutes les réponses de l'élève, sauf son nom, d'où le "nb_questions-1"
        for y in range(nb_questions-1):
            # Si la réponse est bonne, on ajoute 1 à la note
            # Possibilité de remplacer celà par note = note + valeurReponse[y] si les questions ont des valeurs différentes
            if(partieEnt[y] == bonne_reponses[y][0]):
                note += bonne_reponses[y][1]
            else:
                note += bonne_reponses[y][2]


        # On ajoute la note pour créer des couples sortie [nomEleve, note]
        partieSor.append(note)

        # On ajoute ces tuples sortie dans l'objet renvoyé
        output.append(partieSor)

    return output


# On demande le nombre de questions et le nombre d'élèves ayant répondu au questionnaire, pour faire tourner les boucles correctement
nb_questions = int(input("Combien y a-t-il de questions dans le questionnaire en comptant le nom à la fin ? "))
nb_eleves = int(input("Combien d'élèves ont rendu ce questionnaire ? "))


# Ici on demande les bonnes réponses aux questions, avec nb_questions-1 car on ne compte pas le nom de l'élève
for i in range(nb_questions-1):
    reponse = ["", 1, 0]
    reponse[0] = input("Bonne réponse de la question n°" + str(i+1) + " : ")
    reponse[1] = input("Points si bonne réponse à la question n°" + str(i + 1) + " (1 par défaut) : ")
    if reponse[1] == '':
        reponse[1] = 1
    reponse[2] = input("Points si mauvaise réponse à la question n°" + str(i + 1) + " (0 par défaut) : ")
    if reponse[2] == '':
        reponse[2] = 0
    reponse[1] = int(reponse[1])
    reponse[2] = int(reponse[2])
    print(reponse)
    bonne_reponses.append(reponse)


# On utilise "with" pour ouvrir et fermer facilement le fichier csv
with open('csv.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    # on se sert de line_count car on va ignorer la première ligne
    line_count = 0

    nb_questions += 1

    # On ignore la première ligne, comopsée uniquement des tags des colonnes
    for row in csv_reader:

        if line_count == 0:

            line_count += 1

        else:

            eleve = []

            for i in range(1, nb_questions):
                if i != nb_questions-1:
                    eleve.append(row[i])
                else:
                    eleve.append((row[i]))

            objet_formate.append(eleve)

    nb_questions -= 1


# On met les résultats dans l'objet correspondant
resultats = fonction_traitement(objet_formate)


# On ouvre le fichier output et on écrit dedans
with open('resultats.csv', mode='w', newline="") as resultats_file:
    resultats_writer = csv.writer(resultats_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for i in range(nb_eleves):

        resultats_writer.writerow(resultats[i])
