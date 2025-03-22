from copy import copy, deepcopy


class Automate:
    """ Classe représentant un automate avec des etats et des transitions

    Attributs :
        - nbSymboles int : nombre de symboles de l'automate
        - nbEtats int : nombre d'états de l'automate
        - etats list : liste des états de l'automate
        - nbEtatsInitiaux int : nombre d'états initiaux de l'automate
        - etatsInitiaux set : ensemble des états initiaux de l'automate
        - nbEtatsFinaux int : nombre d'états finaux de l'automate
        - etatsFinaux set : ensemble des états finaux de l'automate
        - nbTransitions int : nombre de transitions de l'automate
        - transitions list : liste des transitions de l'automate
    """
    def __init__(self, nom,empty=0):
        """ Constructeur de la classe Automate
        :param nom: nom du fichier texte contenant la description de l'automate
        :param empty: 1 si l'on veut creer un automate est vide rien sinon
        """
        self.nom =nom
        if not empty:
            with open('automates/'+nom+".txt", "r") as autoTxt:
                self.nbSymboles = autoTxt.readline()
                self.nbEtats = autoTxt.readline()
                self.etats=[]
                self.etatsInitiaux = []
                txtEtatInitiaux = autoTxt.readline()
                self.nbEtatsInitiaux = int(txtEtatInitiaux.split()[0])
                txtEtatFinaux = autoTxt.readline()
                self.nbEtatsFinaux = int(txtEtatFinaux.split()[0])
                self.etatsFinaux = []
                for i in range(int(self.nbEtats)):
                    etat = Etat(str(i))
                    self.etats.append(etat)
                    if str(i) in txtEtatInitiaux.split()[1:]:
                        etat.initial = True
                        self.etatsInitiaux.append(etat)
                    if str(i) in txtEtatFinaux.split()[1:]:
                        etat.final = True
                        self.etatsFinaux.append(etat)
                if self.nbEtatsInitiaux != len(self.etatsInitiaux) or self.nbEtatsFinaux != len(self.etatsFinaux):
                    raise ValueError(
                        "le nombre d'états initiaux ou finaux donné ne correspond pas au nombre d'états initiaux ou finaux trouvés : ", self.nbEtatsInitiaux, len(self.etatsInitiaux), self.nbEtatsFinaux, len(self.etatsFinaux))
                self.nbTransitions = autoTxt.readline()
                txtTransi=autoTxt.readlines()
                self.transitions=[]
                for transi in txtTransi:
                    txt = transi.replace("\n", "")
                    if "-"in txt:
                        depart, etiquette, arrivee = txt.split("-")
                        arrivee=self.etats[int(arrivee)]
                    else:
                        i = 0
                        depart = ""
                        car = txt[i]
                        while car.isdigit() and i <= len(txt):
                            depart += car
                            i += 1
                            car = txt[i]
                        etiquette = ""
                        while car.isalpha() and i <= len(txt):
                            etiquette += txt[i]
                            i += 1
                            car = txt[i]
                        arrivee = self.etats[int(txt[i:])]
                    depart = self.etats[int(depart)]


                    self.transitions.append(Transition(depart,etiquette,arrivee))
            self.alphabet = self.getAlphabet()
            if 'E' in self.alphabet:
                self.asynchrone = True
        else:
            self.nbSymboles=0
            self.nbEtats=0
            self.etats=[]
            self.nbEtatsInitiaux=0
            self.etatsInitiaux=[]
            self.nbEtatsFinaux=0
            self.etatsFinaux=[]
            self.nbTransitions=0
            self.transitions=[]
            self.alphabet =[]
            self.asynchrone = False

    def getAlphabet(self):
        '''Recupere l'alphabet de l'automate
        return: l'alphabet de l'automate
        '''
        alphabet = set()
        for transition in self.transitions:
            alphabet.add(transition.symbole)
        return alphabet

    def est_standard(self):
        ''' Verifie si l'automate est standard
        return: True si l'automate est standard, False sinon
        '''
        return (self.est_deterministe() and self.etatsInitiaux[0].transiEntrante == [])

    def standardiser(self):
        '''
        Standardisation de l'automate
        :return: L'automate standardisé
        '''
        auto = deepcopy(self)
        if auto.est_standard():
            return auto
        if not self.est_deterministe():
            auto = self.determiniser()
        if auto.est_standard():
            return auto
        nouvEtat = Etat("i")
        etatInit = auto.etatsInitiaux
        """On parcourt tous les états initiaux de l'automate ainsi que leurs transitions sortantes pour les copier avec le nouvel état initial en depart
        On supprime également les autres etats initiaux de la liste de l'automate
        """
        for etat in etatInit:
            for transi in etat.transiSortante:
                auto.transitions.append(Transition(nouvEtat, transi.symbole, transi.arrivee))
            etat.initial=False
        #On ajoute le nouvel état initial à la liste des états initiaux de l'automate et on le met final s'il y a un état final parmi les états initiaux
        nouvEtat.final = any(etat.final for etat in etatInit)
        if nouvEtat.final:
            auto.etatsFinaux.append(nouvEtat)
        nouvEtat.initial = True
        auto.etatsInitiaux=[nouvEtat]
        auto.etats.append(nouvEtat)
        return auto

    def determiniser(self):
        """Determinisation de l'automate
        :return: Le nouvel automate déterminisé
        """
        if self.est_deterministe():
            return deepcopy(self)
        setEtatInital = frozenset(self.etatsInitiaux)
        etatsNouvAuto = {}
        transiNouvAuto = []
        queue = []
        departNouvAuto = Etat(self.changerNomEtat(setEtatInital))
        departNouvAuto.initial = True
        etatsNouvAuto[setEtatInital] = departNouvAuto
        queue.append(setEtatInital)

        # On parcourt les états de l'automate
        while queue:
            setEtatCourant = queue.pop(0)
            etatCourant = etatsNouvAuto[setEtatCourant]
            etatCourant.final = any(state.final for state in setEtatCourant)
            # On ajoute les etats des transitions sortantes du premier etat fusionne a une liste pour être sur de tous les traiter
            for symbole in self.alphabet:
                prochainSetEtat = set()
                for etatAuto in setEtatCourant:
                    for transition in etatAuto.transiSortante:
                        if transition.symbole == symbole:
                            prochainSetEtat.add(transition.arrivee)
                if not prochainSetEtat:
                    continue
                prochainSetEtat = frozenset(prochainSetEtat)
                # on fusionne les etats non traites
                if prochainSetEtat not in etatsNouvAuto:
                    nouvEtat = Etat(self.changerNomEtat(prochainSetEtat))
                    etatsNouvAuto[prochainSetEtat] = nouvEtat
                    queue.append(prochainSetEtat)
                # on redefinit la transition avec les nouveaux etats fusionnes
                transiNouvAuto.append(Transition(etatCourant, symbole, etatsNouvAuto[prochainSetEtat]))

        # On finit par tout ajouter au nouvel automate
        nouvAuto = Automate(self.nom, 1)
        nouvAuto.etats = list(etatsNouvAuto.values())
        nouvAuto.etatsInitiaux = [departNouvAuto]
        nouvAuto.etatsFinaux = [state for state in etatsNouvAuto.values() if state.final]
        nouvAuto.transitions = transiNouvAuto
        nouvAuto.nbEtats = len(nouvAuto.etats)
        nouvAuto.nbEtatsInitiaux = 1
        nouvAuto.nbEtatsFinaux = len(nouvAuto.etatsFinaux)
        nouvAuto.nbTransitions = len(nouvAuto.transitions)
        nouvAuto.nbSymboles = self.nbSymboles
        nouvAuto.alphabet = self.alphabet
        return nouvAuto

    def est_deterministe(self):
        """Vérifie si l'automate est déterministe
        :return: True si l'automate est déterministe, False sinon"""
        if self.nbEtatsInitiaux != 1:
            return False
        etatSymb = []
        for transi in self.transitions:
            if transi.symbole=="E":
                continue
            etatSymb.append(str(transi.depart) + str(transi.symbole))
        return len(etatSymb) == len(set(etatSymb))

    def changerNomEtat(self, setEtat):
        """Une methode qui permet de changer le nom d'un etat fusionne
        :param setEtat: ensemble des etats fusionnes
        :return: le nouveau nom de l'etat fusionne"""
        return "-".join(sorted(etat.nom for etat in setEtat))

    def complémentaire(self):
        """Calcul du complémentaire de l'automate
        :return: L'automate complémentaire"""
        if not self.est_deterministe():
           automate=self.determiniser()
        else:
            automate=deepcopy(self)
        automate.etatsFinaux = set()
        automate.nbEtatsFinaux = 0
        for etat in automate.etats:
            if etat.final == True:
                etat.final = False
            else:
                etat.final = True
                automate.etatsFinaux.add(etat)
                automate.nbEtatsFinaux += 1
        return automate

    def litMot(self, mot: str):
        """Lecture d'un mot par l'automate
        :param mot: mot à lire
        :return: True si le mot est accepté, False sinon"""
        if not self.est_deterministe():
           automate=self.determiniser()
        else:
            automate=self
        etatCourant = automate.etatsInitiaux[0]
        #On parcourt l'automate en fonction des lettres du mot
        for lettre in mot:
            for transi in etatCourant.transiSortante:
                if transi.symbole == lettre:
                    etatCourant = transi.arrivee
                    avance = True
                    break
            if avance != True:
                return False
            avance = False
        #On verifie si l'etat courant est bien final
        return etatCourant.final

    def affichage(self):
        """ Affichage de l'automate"""
        print("Lecture de l'automate", self.nom)
        print("Nombre de symboles:", self.nbSymboles)
        print("Nombre d'états:", self.nbEtats)
        print("Nombre d'états initiaux:", self.nbEtatsInitiaux)
        print("Liste des états initiaux:", self.etatsInitiaux)
        print("Nombre d'états finaux:", self.nbEtatsFinaux)
        print("Nombre de transitions:", self.nbTransitions)
        print("Transitions:",self.transitions)

    def affichageTable(self, file=''):
        """Affiche la table de transition de l'automate"""
        symboles = list(self.alphabet)

        #On cree le haut du tableau
        header = ["Etat"] + sorted(symboles) + ["E/S"]
        table = [] 

        #On cree un ligne pour chaque etat
        for etat in self.etats:
            ligne = [str(etat)]
            for symbole in sorted(symboles):
                #On cherche toutes les transitions sortantes de l'etat pour chaque symbole
                destinations = set()
                for transition in etat.transiSortante:
                    if transition.symbole == symbole:
                        destinations.add(str(transition.arrivee))
                if destinations:
                    ligne.append(", ".join(sorted(destinations)))
                else:
                    ligne.append("-")
            #On termine par afficher si l'etat est initial ou final
            ligne.append("E-S" if etat.initial and etat.final else"S" if etat.final else "E" if etat.initial else  "")
            table.append(ligne)

        #On calcule la largeur de chaque colonne
        largColonnes = [max(len(str(item)) for item in col) for col in zip(header, *table)]

        
        def afficheLigne(ligne):
            """Fonction permettant d'afficher une ligne du tableau"""
            return " | ".join(f"{obj:<{larg}}" for obj, larg in zip(ligne, largColonnes))

        if file!='':
            print('Automate',self.nom, file=open(file, 'a'))
            print(afficheLigne(header), file=open(file, 'a'))
            print("-" * (sum(largColonnes) + 3 * (len(largColonnes) - 1)), file=open(file, 'a'))
            for ligne in table:
                print(afficheLigne(ligne), file=open(file, 'a'))
            print('', file=open(file, 'a'))

        print('Automate',self.nom)
        print(afficheLigne(header))
        print("-" * (sum(largColonnes) + 3 * (len(largColonnes) - 1)))
        for ligne in table:
            print(afficheLigne(ligne))
        print()

class Etat:
    etatExistant = []
    ''' Classe représentant un état d'un automate'''

    def __init__(self, nom):
        """
        Constructeur de la classe Etat
        :param nom: nom de l'état
        """
        self.nom = nom
        self.initial = False
        self.final = False
        self.transiSortante=[]
        self.transiEntrante=[]
        self.doublon=False
        if self not in type(self).etatExistant:
            type(self).etatExistant.append(self)
        else:
            self.doublon=True

    def __str__(self):
        """Permet de convertir l'état en chaine de caractères implicitement"""
        return str(self.nom)

    def __repr__(self):
        return str(self.nom)

    def __eq__(self, other):
        return self.nom==other.nom

    def __hash__(self):
        return hash(self.nom)

class Transition:
    """ Classe représentant une transition d'un automate"""
    def __init__(self, depart, etiquette,arrivee):
        """
        Constructeur de la classe Transition
        :param texte:texte de la forme "depart etiquette arrivee"
        """
        self.depart = depart
        self.symbole = etiquette
        self.arrivee = arrivee
        self.txt = str(self.depart) + self.symbole + str(self.arrivee)
        if self not in depart.transiSortante:
            depart.transiSortante.append(self)
        if self not in arrivee.transiEntrante:
            arrivee.transiEntrante.append(self)

    def check(self, val, pos):
        if pos=="d":
            return self.depart.nom==val
        elif pos=="a":
            return self.arrivee.nom==val
        elif pos=="s":
            return self.symbole==val


    def __str__(self):
        """Permet de convertir la transition en chaine de caractères implicitement"""
        return self.txt

    def __repr__(self):
        return self.txt

    def __eq__(self, other):
        return self.txt==other.txt

    def __hash__(self):
        return hash(self.txt)

if __name__ == "__main__":
    rep=input("Voulez-vous afficher les executions de tous les automates? (o/n)")
    if rep=="o":
        for i in range(1,45):
            fichier = 'traceAuto/' +str(i) + '.txt'
            print('Debut du programme avec l\'automate ',i,file=open(fichier,'w'))
            a=Automate(str(i))
            a.affichageTable(fichier)
            print("Determinisation",file=open(fichier,'a'))
            print(a.est_deterministe())
            e=a.determiniser()
            e.affichageTable(fichier)
            print("Standardisation",file=open(fichier,'a'))
            s=a.standardiser()
            s.affichageTable(fichier)
            print("Complementaire",file=open(fichier,'a'))
            c=a.complémentaire()
            c.affichageTable(fichier)

    else:
        rep=input("Quel automate voulez-vous executer ?\n")
        boucle=1
        while boucle:
            print('Debut du programme avec l\'automate '+rep)
            a = Automate(rep)
            a.affichageTable()
            print("Determinisation")
            print(a.est_deterministe())
            e = a.determiniser()
            e.affichageTable()
            print("Standardisation")
            s = a.standardiser()
            s.affichageTable()
            print("Complementaire")
            c = a.complémentaire()
            c.affichageTable()
            mot=1
            rep = input("Voulez-vous lire un mot avec cet automate ? (o/n)\n")
            if rep=='n':
                mot=0
            while mot:
                if rep=="o":
                    mot=input("Veuillez entrer un mot : ")
                    print("Lecture du mot ",mot)
                    print('Avec l\'automate standard')
                    print("Mot reconnu" if a.litMot(mot) else "Mot non reconnu")
                    print('Avec l\'automate determinise')
                    print("Mot reconnu" if e.litMot(mot) else "Mot non reconnu")
                    print('Avec l\'automate standardise')
                    print("Mot reconnu" if s.litMot(mot) else "Mot non reconnu")
                    print('Avec l\'automate complementaire')
                    print("Mot reconnu" if c.litMot(mot) else "Mot non reconnu")
                rep=input("Voulez-vous lire un autre mot ? (o/n)\n")
                if rep=="n":
                    mot=0
                else:
                    rep="o"
            rep=input("Voulez-vous continuer avec d'autres automates ? (o/n)\n")
            if rep=="n":
                boucle=0
            else:
                rep=input("Quel automate voulez-vous executer ? ")



