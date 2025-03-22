from copy import copy


class Automate:
    ''' Classe représentant un automate avec des etats et des transitions

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
    '''
    def __init__(self, nom,empty=0):
        ''' Constructeur de la classe Automate
        :param nom: nom du fichier texte contenant la description de l'automate
        :param empty: 1 si l'on veut creer un automate est vide rien sinon
        '''
        self.nom = nom
        print("Création de l'automate", nom)
        if not empty:
            with open(nom+".txt", "r") as autoTxt:
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
                        "le nombre d'états initiaux ou finaux donné ne correspond pas au nombre d'états initiaux ou finaux trouvés")
                self.nbTransitions = autoTxt.readline()
                txtTransi=autoTxt.readlines()
                self.transitions=[]
                for transi in txtTransi:
                    txt = transi.replace("\n", "")
                    i = 0
                    depart = ""
                    car = txt[i]
                    while car.isdigit() and i <= len(txt):
                        depart += car
                        i += 1
                        car = txt[i]
                    depart = self.etats[int(depart)]
                    etiquette = ""
                    while car.isalpha() and i <= len(txt):
                        etiquette += txt[i]
                        i += 1
                        car = txt[i]
                    arrivee = self.etats[int(txt[i:])]
                    self.transitions.append(Transition(depart,etiquette,arrivee))
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
    etatExistant = []
    ''' Classe représentant un état d'un automate'''

    def __init__(self, nom):
        '''
        Constructeur de la classe Etat
        :param nom: nom de l'état
        '''
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
        '''Permet de convertir l'état en chaine de caractères implicitement'''
        return str(self.nom)

    def __repr__(self):
        return str(self.nom)

    def __eq__(self, other):
        return self.nom==other.nom

    def __add__(self, other):
        if self==other:
            return copy(self)
        print(self.transiSortante,other.transiSortante)
        nouv=Etat(str(self.nom)+"-"+str(other.nom))
        if not nouv.doublon :
            print("fsdgzjinrg")
            nouv.transiEntrante=self.transiEntrante+other.transiEntrante
            nouv.transiSortante=self.transiSortante+other.transiSortante
            nouv.initial=self.initial or other.initial
            nouv.final=self.final or other.final
            tabTransi={}
            for transi in nouv.transiSortante:
                if transi.symbole not in tabTransi:
                    tabTransi[transi.symbole]=[]
                tabTransi[transi.symbole].append(transi)
            for transis in tabTransi.values():
                a=transis[0]
                for i in range(1,len(transis)):
                    a+=transis[i]
                nouv.transiSortante.append(a)
            return nouv

        return type(self).etatExistant[type(self).etatExistant.index(nouv)]

class Transition:
    ''' Classe représentant une transition d'un automate'''
    def __init__(self, depart, etiquette,arrivee):
        '''
        Constructeur de la classe Transition
        :param texte:texte de la forme "depart etiquette arrivee"
        '''
        self.depart = depart
        self.symbole = etiquette
        self.arrivee = arrivee
        self.txt = str(self.depart) + self.symbole + str(self.arrivee)
        print("\na",self,"\n")
        if self not in depart.transiSortante:
            print(self,depart.transiSortante)
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

    def affichage(self):
        """ Affichage de la transition"""
        print("Transition de", self.depart, "vers", self.arrivee, "avec l'étiquette", self.symbole,"\n")

    def __str__(self):
        """Permet de convertir la transition en chaine de caractères implicitement"""
        return self.txt

    def __repr__(self):
        return self.txt

    def __eq__(self, other):
        return self.txt==other.txt

    def __add__(self, other):
        if self==other:
            return copy(self)
        depart=self.depart+other.depart
        arrivee=self.arrivee+other.arrivee
        nouv=Transition(depart,self.symbole,arrivee)
        return nouv

if __name__ == "__main__":
    t=Automate("automateBase")
    t.affichage()