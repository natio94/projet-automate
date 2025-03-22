from main import *
def est_standard(auto:Automate):
    ''' Vue que est_deterministe dit si l'automate a plusieurs entrée je le réutilise,
    et je demande en plus si il y a des transitions qui arrivent vers l'état initiale
    True si standar false si non
    '''
    if (est_deterministe(auto) and auto.etatsInitiaux[0].transiEntrante == []):
        return True
    return False


def standardisation(auto:Automate):
    '''
    d'abbord je test pour savoir si l'automate est pas déjà standar
    enssuite je crée un nouvelle état nomé "i" qui vas étre le nouveau
    état initiale
    la copie des etats initiale est pour pouvoir garder une trace
    je fait 2 boucles qui parcour la premiere les ellements initiaux de l'automate
    l'autre prend les transitions sortantes
    je crée enssuite les nouvelles transition et suprime après chaque ittération
    les ancien état initiaux de la liste etatsInitiaux pour mettre après le nouveau
    la fonction renvoie l'affichage de l'automate
    '''
    if (est_standard(auto) == True):
        return auto.affichage()
    else :
        c = Etat(1000)
        etatInit=deepcopy(auto.etatsInitiaux)
        for i in etatInit:
            for e in i.transiSortante:
                auto.transitions.append(Transition(c , e.symbole, e.arrivee))
            auto.etatsInitiaux.remove(i)
        c.final=any(etat.final for etat in etatInit)
        auto.etatsInitiaux.append(c)
        auto.etats.append(c)
    return auto.affichage()


def est_deterministe(auto:Automate):
    if auto.nbEtatsInitiaux!=1:
        return False
    etatSymb=[]
    for transi in auto.transitions:
        etatSymb.append(str(transi.depart)+str(transi.symbole))
    return len(etatSymb)==len(set(etatSymb))


def determinisation(auto:Automate):
    if est_deterministe(auto):
        print("L'automate est déjà déterministe")
        return auto
    if auto.nbEtatsInitiaux>1:
        etatsInit=auto.etatsInitiaux




t=Automate("automates/5")
print(est_standard(t))
print(standardisation(t))
print(est_deterministe(t))



