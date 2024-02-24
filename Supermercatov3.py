import xml.etree.ElementTree as ET
import json
import threading
import random
import time
import multiprocessing


#inizializzo i semafori
sem1=multiprocessing.Semaphore(1) #cassa1
sem2=multiprocessing.Semaphore(1) #cassa2
sem3=multiprocessing.Semaphore(1) #cassa3

class Supermarket(threading.Thread):

    negozio = []
    prodotti_nome = []
    filePathJson = r"E:\EnricoFioreInformtaica\python\5AI\Progetto_Supermercato\Magazzinov2.json"
    filePathXml = r"E:\EnricoFioreInformtaica\python\5AI\Progetto_Supermercato\SpesaTotale.xml"

    def __init__(self):
        threading.Thread.__init__(self)  # creo thread


    def Sleep(self,n):
        time.sleep(n)
        
    def Casse(self):
        #self.AzzeraFileXml()
        #self.ImportaDatiFileJson()
        spesa = self.EventiCasuali(Cliente.GetCosto(self))#faccio fare gli eventi per 6 secondi prima di entare alla cassa
        Cliente.SetCosto(self,spesa) # lo inserisco nella classe cliente
        while True:
            if(sem1.acquire(block=False)):#se il semaforo è libero
                print("Cassa1 occupata\n")
                #self.SalvaPagamento(Cliente.GetCosto(self))
                print("carrello: ", Cliente.GetCarrello(self))
                print(Cliente.GetNome(self)," ", Cliente.GetCognome(self)," ha pagato: ",Cliente.GetCosto(self))  
                time.sleep(5) #simulare attesa in cassa
                sem1.release()
                print("Cassa1 libera")
                break
                    
            elif(sem2.acquire(block=False)):#se il semaforo è libero
                print("Cassa2 occupata\n")
                #self.SalvaPagamento(Cliente.GetCosto(self))
                print("carrello: ",Cliente.GetCarrello(self))
                print(Cliente.GetNome(self)," ", Cliente.GetCognome(self)," ha pagato: ",Cliente.GetCosto(self)) 
                time.sleep(5) #simulare attesa in cassa
                sem2.release()
                print("Cassa2 libera")
                break
                    
            elif(sem3.acquire(block=False)):#se il semaforo è libero
                print("Cassa3 occupata\n") 
                #self.SalvaPagamento(Cliente.GetCosto(self))
                print("carrello: ", Cliente.GetCarrello(self))
                print(Cliente.GetNome(self)," ", Cliente.GetCognome(self)," ha pagato: ",Cliente.GetCosto(self))   
                time.sleep(5) #simulare attesa in cassa
                sem3.release()
                print("Cassa3 libera")
                break
                


    def AggiungiProdottoAlcarrello(self):
        print("sono in aggiungo prodotto\n")
        for prodotto in self.negozio:
            self.prodotti_nome.append(prodotto["nome"]) #salvo i nomi dei prodotti nella list
        nome_prodotto = random.choice(self.prodotti_nome) #prendo un prodotto random tra quelli salvati nella list
        for prodotto in self.negozio:
            if nome_prodotto == prodotto["nome"]: #se il prodotto corissponde a quello scelto
                if(prodotto["quantita"]> 0): # e non è finito
                   prodotto["quantita"] -= 1 # decremento
                   print(Cliente.GetNome(self), " " , Cliente.GetCognome(self)," ha inserito nel carrello: ", nome_prodotto)
                   Cliente.GetCarrello(self).append(nome_prodotto) # lo salvo nel carrello
                   return prodotto["costo"]# ritorno il prezzo
                else:
                    print("prodotto esaurito\n")
                    return 0
        

       
    def ImportaDatiFileJson(self):
        with open(self.filePathJson, 'r') as f:
            data = json.load(f)
        for prodotto in data:
            self.negozio.append(prodotto)
        
    def SalvaPagamento(self, prezzo):
        tree = ET.parse(self.filePathXml)  # Apro il file XML
        root = tree.getroot()

        # Trovo l'elemento "totale" nel file XML e aggiungo il prezzo
        totale = root.find("./totali/totale")
        if totale is not None:
            totale.text = str("{:.2f}".format(float(totale.text) + prezzo))
        else:
            print("Elemento 'totale' non trovato.")

        tree.write(self.filePathXml)  # Salvo le modifiche al file XML


    def AzzeraFileXml(self):
        tree = ET.parse(self.filePathXml)
        root = tree.getroot()
        totale = root.find("./totali/totale")
        totale.text = "0.0"
        tree.write(self.filePathXml)
    
    def RipongoProdotto(self,spesa_costo):
        print("ripongo prodotto\n")
        if(spesa_costo > 0 and Cliente.GetCarrello(self) != []) : # se ho prodotti nel carrello
            nome_prodotto = random.choice(Cliente.GetCarrello(self)) # prendo un prodotto a caso dal carrello
            for prodotto in self.negozio: # controllo dove il prodotto è presente nel negozio
                if nome_prodotto == prodotto["nome"]:
                        prodotto["quantita"] += 1 # incremento la quantità
                        print("ho riposto: ", nome_prodotto)
                        Cliente.GetCarrello(self).remove(nome_prodotto)#rimuovo il prodotto dal carrello
                        return prodotto["costo"] # ritorno il prezzo per decrementarlo dal totale
        else:
            print(Cliente.GetNome(self), " " , Cliente.GetCognome(self), " non ha prodotti nel carrello\n")
            return 0



    def EventiCasuali(self,costo):
        start_time = time.time()
        while time.time() - start_time < 6:
            n_random = random.randint(1, 3)
            if n_random == 1:
                costo += self.AggiungiProdottoAlcarrello()
            elif n_random == 2:
                print(Cliente.GetNome(self), Cliente.GetCognome(self), " chiede dove si trova il latte?")
            elif n_random == 3:
                costo -= self.RipongoProdotto(costo)
            time.sleep(2)  # ogni 2 secondi parte evento 
        return costo 
    
  

    """def run(self):
        print("è entrato nel supermercato")
        self.Casse(self)"""


class Cliente(Supermarket):
    def __init__(self,nome,cognome):
        self.nome = nome
        self.cognome = cognome
        self.carrello = []
        self.costo = 0
        super().__init__()  
    
    def GetNome(self):
        return self.nome
    
    def GetCognome(self):
        return self.cognome
    
    def GetCarrello(self):
        return self.carrello
    
    def GetCosto(self):
       return float("{:.2f}".format(self.costo)) # formula per arrotondare fino a 0.00
    
    def SetCosto(self,costo):
        self.costo = costo
    
    def run(self):
        print("È entrato nel supermercato")
        self.Casse() #faccio partire il thread da qui

carrello  = []
cliente1 = Cliente("Mario","Rossi")
cliente2 = Cliente("Luca","Bianchi")
cliente3 = Cliente("Giovanni","Verdi")
cliente4 = Cliente("Paolo","Neri")
cliente5 = Cliente("Enrico","Fiore")
cliente6 = Cliente("Giovanni","Virile")
clinete7 = Cliente("Marco","Pela")
cliente7 = Cliente("Gianmarco","Roberti")
cliente8 = Cliente("John Paul","Magsino")
cliente9 = Cliente("Nicolo","Isotti")
cliente10 = Cliente("Even","Bellucci") 
cliente11 = Cliente("Lorenzo","Bottegoni")
cliente12 = Cliente("Kunal","Sharma")
cliente13 = Cliente("Daniele","Riccardo")
cliente14 = Cliente("Nicolo","Vero")
cliente15 = Cliente("Davide","Renzi")
cliente16 = Cliente("Gianmarco","Belardinelli")
cliente17 = Cliente("Alessio","Pesaresi")
cliente18 = Cliente("Alessandro","Roccetti")
cliente19 = Cliente("Mattia","Di Lorenzo")
cliente20 = Cliente("Lorenzo","Bastianelli")
cliente21 = Cliente("Samuele","Tomori")
cliente22 = Cliente("Francesco","Massimo")
cliente23 = Cliente("Michela","Giampietro")
cliente24 = Cliente("Riccardo","Cotani")
cliente25 = Cliente("Leonardo","Papa")

clienti = [cliente1,cliente2,cliente3,cliente4,cliente5,cliente6,clinete7,cliente7,cliente8,cliente9,cliente10,cliente11,cliente12,cliente13,cliente14,cliente15,cliente16,cliente17,cliente18,cliente19,cliente20,cliente21,cliente22,cliente23,cliente24,cliente25]

supermercato1 = Supermarket()

supermercato1.AzzeraFileXml() #azzero il file prima di eseguire i thread
supermercato1.ImportaDatiFileJson() #importo i dati dal file json

for i in clienti:
    i.start()#avvio i thread

for i in clienti:
    i.join()#attendo che finiscano i thread
    supermercato1.SalvaPagamento(i.GetCosto())

    