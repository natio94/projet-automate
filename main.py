class Automate:
    ''' Classe représentant un automate avec des etats et des transitions'''
    def __init__(self, nom):
        ''' Constructeur de la classe Automate
        :param nom: nom du fichier texte contenant la description de l'automate
        '''
        self.nom = nom
        print("Création de l'automate", nom)
        with open(nom+".txt", "r") as autoTxt:
            self.nbSymboles = autoTxt.readline()
            self.nbEtats = autoTxt.readline()
            self.etats=[]
            for i in range(int(self.nbEtats)):
                self.etats.append(Etat(i))
            txtEtatInitiaux = autoTxt.readline()
            self.nbEtatsInitiaux = txtEtatInitiaux.split()[0]
            self.etatsInitiaux = set(txtEtatInitiaux.split()[1:])
            for etat in self.etatsInitiaux:
                self.etats[int(etat)].initial=True
            txtEtatFinaux = autoTxt.readline()
            self.nbEtatsFinaux = txtEtatFinaux.split()[0]
            self.etatsFinaux = set(txtEtatFinaux.split()[1:])
            for etat in self.etatsFinaux:
                self.etats[int(etat)].final=True
            self.nbTransitions = autoTxt.readline()
            txtTransi=autoTxt.readlines()
            self.transitions=[]
            for transi in txtTransi:
                self.transitions.append(Transition(transi))

    def affichage(self):
        ''' Affichage de l''automate'''
        print("Lecture de l'automate", self.nom)
        print("Nombre de symboles:", self.nbSymboles)
        print("Nombre d'états:", self.nbEtats)
        print("Nombre d'états initiaux:", self.nbEtatsInitiaux)
        print("Liste des états initiaux:", self.etatsInitiaux)
        print("Nombre d'états finaux:", self.nbEtatsFinaux)
        print("Nombre de transitions:", self.nbTransitions)
        for transi in self.transitions:
            transi.affichage()


class Etat:
    ''' Classe représentant un état d'un automate'''
    def __init__(self, nom):
        '''
        Constructeur de la classe Etat
        :param nom: nom de l'état
        '''
        self.nom = nom
        self.initial = False
        self.final = False

    def __str__(self):
        '''Permet de convertir l'état en chaine de caractères implicitement'''
        return str(self.nom)

class Transition:
    ''' Classe représentant une transition d'un automate'''
    def __init__(self, texte):
        '''
        Constructeur de la classe Transition
        :param texte:texte de la forme "depart etiquette arrivee"
        '''
        self.txt = texte.replace("\n","")
        i=0
        depart=""
        car=self.txt[i]
        while car.isdigit() and i<=len(self.txt):
            depart+= car
            i += 1
            car = self.txt[i]
        self.depart = Etat(depart)
        etiquette=""
        while car.isalpha() and i<=len(self.txt):
            etiquette+= self.txt[i]
            i+=1
            car = self.txt[i]
        self.symbole = etiquette
        self.arrivee = Etat(self.txt[i:])

    def affichage(self):
        ''' Affichage de la transition'''
        print("Transition de", self.depart, "vers", self.arrivee, "avec l'étiquette", self.symbole,"\n")

    def __str__(self):
        '''Permet de convertir la transition en chaine de caractères implicitement'''
        return self.txt

t=Automate("test")
t.affichage()