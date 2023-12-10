import matplotlib.pyplot as plt
import numpy

def MyDBSCAN(D, eps, MinPts):
   	# D(veri kümesi), eps(yaricap), MinPts(minimum komsu sayisi) 
    # -1(noise, gurultu)
    labels = [0]*len(D) # 0(unvisited, baslangicta her deger 0 ile etiketlenir) 

    C = 0 # mevcut kume
    
    # yeni kume olusturmak icin secilen P noktasi bir veri noktasinin indeksidir
    for P in range(0, len(D)):
        if not (labels[P] == 0): # eger nokta visited ise siradaki noktadan devam edilir
           continue
        
        NeighborPts = regionQuery(D, P, eps) # secilen noktanin komsulari bulunur
        
        if len(NeighborPts) < MinPts:	# komsu sayisi MinPts'den kucukse gurultudur
            labels[P] = -1
        else: 							# en azindan yakinlarda MinPts varsa..
           C += 1
           growCluster(D, labels, P, NeighborPts, C, eps, MinPts) # ..kume genisler
    
    return labels # tum veri kumelendi


def growCluster(D, labels, P, NeighborPts, C, eps, MinPts): # kumeyi genisletme fonksiyonu
    
    # P esas noktasindan yeni bir kume olusturulur. Kumeye ait tum noktalar bulunur
    labels[P] = C 	# kume etiketi esas noktaya atanir
    
    # komsu noktalar icin queue yapisi kullanilir. kume dallanarak buyur
    i = 0
    while i < len(NeighborPts): # P noktasinin tum komsulari icin..    
        
        P0 = NeighborPts[i] # siradaki nokta alinir
       
        if labels[P0] == -1:	# P0 gurultu olarak etiketlendiyse, C kumesine yaprak olarak eklenir
            labels[P0] = C 		
        elif labels[P0] == 0:	# P0 unvisited ise, C kumesine ait varsayilir
            labels[P0] = C            
            P0NeighborPts = regionQuery(D, P0, eps) # P0'in tum komsulari bulunur
            if len(P0NeighborPts) >= MinPts: # komsu sayisi MinPts'den buyukse dallanma noktasidir
                NeighborPts += P0NeighborPts # tum komsular queue'ya eklenir
            # yeterli sayida komsu yoksa yaprak noktalardir, siradaki noktaya gecilir
        i += 1        


def regionQuery(D, P, eps): # komsu bulma fonksiyonu
    	# P noktasi baz alinarak eps yaricapli cember cizilir
    	# cember icinde kalan noktalar(komsular) bulunur
    neighbors = []

    for P0 in range(0, len(D)): # veri kumesindeki tum noktalar icin..
        if numpy.linalg.norm(D[P] - D[P0]) < eps: # mesafe yaricaptan kucukse, komsudur
           neighbors.append(P0)		
            
    return neighbors

#___________________________________________________________plot
f = open('data.txt', 'r')
date = []; time = []; code = []; value = [];
for line in f:
    columns = line.split()
    date.append(columns[0])
    time.append(columns[1])
    code.append(int(columns[2]))
    value.append(columns[3])
f.close()
Data = numpy.array(code)
#print(Data)
test = MyDBSCAN(Data, 1, 5)

#print(test)

arr = []    
for i in range(10) : 
    arr.append(0)

for i in test : 
    arr[i]+=1	
print(arr)
   
plt.hist(test, bins = 10)
plt.show();
