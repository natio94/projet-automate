from main import *
def litMot(automate:Automate,mot:str):
    #if not est_deterministe(automate):
    #    automate=determinisation(automate)
    etatCourant=automate.etatsInitiaux[0]
    for lettre in mot:
        for transi in etatCourant.transiSortante:
            if transi.symbole==lettre:
                etatCourant=transi.arrivee
                avance=True
                break
        if avance!=True:
            return False
        avance=False
    return etatCourant.final
auto=Automate("automates/12")
print(litMot(auto,"acbbd"))