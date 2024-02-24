import xml.etree.ElementTree as ET
import json
import threading
import random
import time

class Supermarket(threading.Thread):

    Cassa1 = False
    Cassa2 = False
    Cassa3 = False
    carello = []
    filePath = r"F:\EnricoFioreInformtaica\python\5AI\Progetto_Supermercato\Magazzinov2.json"

    def __init__(self):
        threading.Thread.__init__(self)  # creo thread

    def Sleep(self,n):
        time.sleep(n)
        
    def Casse(self):
        spesa = self.EventiCasuali()
        if(self.Cassa1 == False):
            self.Cassa1 = True
            print("Cassa1 occupata\n")
            self.SalvaPagamento(spesa)  
            print("Cassa1 libera")
            self.Cassa1 = False 
        elif(self.Cassa2 == False):
            self.Cassa2 = True
            print("Cassa2 occupata\n")
            self.SalvaPagamento(spesa)
            print("Cassa2 libera")
            self.Cassa2 = False 
        elif(self.Cassa3 == False):
            self.Cassa3 = True
            print("Cassa3 occupata\n") 
            self.SalvaPagamento(spesa)
            print("Cassa3 libera")
            self.Cassa3 = False 


    def AggiungiProdottoAlCarello(self,data):
        print("sono in aggiungo prodotto\n")
        nome_prodotto = random.choice(list(data.keys()))# prendo un nome di un prodotto random nel file .json    
        # trovo il prodotto nel file .json e ne decremento la quantità
        print("nome prodotto: ",nome_prodotto)
        
        for prodotto in data:
            if prodotto == nome_prodotto:
                if(prodotto["quantità"]> 0):
                    self.carello.append(nome_prodotto)
                    prodotto["quantità"] -= 1
                    # salvo la quantità aggiornata
                    with open(self.filePath, "w") as file:
                        json.dump(data, file)
                    return prodotto["prezzo"] 
                else:
                    print("prodotto esaurito\n")
                    return None
        """if nome_prodotto in data:
            product = data[nome_prodotto]
            self.carello.append(product)#inserisco prodotto nel carello
            quantita = int(product['quantità'])
            if int(quantita) > 0:
                product["quantità"] -= 1
                prezzo = product["prezzo"]
                # salvo la quantità aggiornata
                with open("Magazzinov2.json", "w") as file:
                    json.dump(data, file)
                return prezzo
        return None # se non trova il prodotto nel file, ritorno il niente"""


    def PagamentoeScalata(self):
        data = self.ApriFileJson()     
        return self.AggiungiProdottoAlCarello(data)
       
    def ApriFileJson(self):
        with open(self.filePath, 'r') as f:
            data = json.load(f)
        return data
        
    def SalvaPagamento(self,prezzo):
        tree = ET.parse("SpeseTotali.xml") # Apro il file XML
        root = tree.getroot()
        
        # Trovo l'elemento "totale" nel file XML e aggiungo il prezzo
        totale = root.find("totale")
        totale.text = str(float(totale.text) + prezzo)
        
        tree.write("SpeseTotali.xml") # Salvo le modifiche al file XML
    
    def RipongoProdotto(self):
        if self.carello.count==0:  # Aggiunto controllo se il carello è vuoto
            prodotto_rimuovere = self.carello[-1]
            self.carello.pop()
            data = self.ApriFileJson()
            if prodotto_rimuovere in data:
                prodotto_rimuovere["quantità"] += 1
                prezzo = int(prodotto_rimuovere["prezzo"])
                with open("Magazzinov2.json", "w") as file:
                    json.dump(data, file)#aggiorno dati nel file json
                return prezzo
        return 0  # Ritorno 0 se il carello è vuoto



    def EventiCasuali(self):
        start_time = time.time()
        costo = 0
        while time.time() - start_time < 6:
            n_random = random.randint(1, 3)
            if n_random == 1:
                costo += self.PagamentoeScalata()
            elif n_random == 2:
                print("Dove si trova il latte?")
            elif n_random == 3:
                costo -= self.RipongoProdotto()
            time.sleep(0.5)  # Aggiunto ritardo di 0.5 secondi tra gli eventi
        return costo
  

    """def run(self):
        print("è entrato nel supermercato")
        self.Casse(self)"""


class Cliente(Supermarket):
    def __init__(self,nome,cognome):
        self.nome = nome
        self.cognome = cognome
        super().__init__()  
    
    def GetNome(self):
        return self.nome
    
    def GetCognome(self):
        return self.cognome
    
    def run(self):
        print("È entrato nel supermercato")
        self.Casse() #faccio partire il thread da qui


cliente1 = Cliente("Mario","Rossi")
cliente2 = Cliente("Luca","Bianchi")
cliente3 = Cliente("Giovanni","Verdi")
cliente4 = Cliente("Paolo","Neri")

clienti = [cliente1]

for i in clienti:
    i.start()#avvio i thread
    i.join()#attendo che finiscano i thread