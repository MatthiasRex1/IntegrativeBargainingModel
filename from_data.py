import pandas as pd
from model import Country,cycle


data=pd.read_csv('data.csv',sep=';')
number=len(data['Country'].tolist())
vygody=[[]for c in range(number)]
izdershki=[[]for c in range(number)]
#ccc=['Canada','Sweden','Norway','USA','Iceland','Denmark','Finland','Russia']
ccc=data['Country'].tolist()
ss=20
for s in range(ss):
    print('Список стран:')
    countries=[]
    interes=data['Interest'].tolist()
    posit=data['Position'].tolist()
    #interes=[49,18,22,27,100,50,39,32]
    #interes=[random.randint(0,100) for c in range(10)]
    #posit=[random.randint(0,100) for c in range(10)]
    
    for i in range (number):

        countries.append(Country(posit[i],interes[i]))
        print(ccc[i],'Интерес:',countries[i].iner,'Позиция:',countries[i].pos)
    d=0
    for i in countries:
        d+=1
        i.GNLvi(countries,len(countries)*100)
        i.sorted(i)
    bl=False
    bl=cycle(countries,len(countries)*100)
    gainres=[]
    lossres=[]
    resi=0
    if bl:
        print('Режим был создан')
    else:
        print('Режим не был создан')
        print('==================')
        continue
    for i in range(len(countries)):
        if not countries[i].isout:
            resi=i
            break
    print('Результат:')
    sumofizderzhki=[]
    suofiz=0
   # print(countries[resi].negotiator.vector)
    #for i in countries:
        #    print('!!!!!!!!!!!',[(c[1],c[2]) for c in i.negotiator.vector])
    for i in range(len(countries[resi].negotiator.vector)):
        if countries[i].isout:
            print(i,'isout','isout')
            continue
        print(ccc[i],'Выгоды:',countries[resi].negotiator.vector[i][1],'Издержки:',countries[resi].negotiator.vector[i][2])
        
        vygody[i].append(countries[resi].negotiator.vector[i][1])
        izdershki[i].append(countries[resi].negotiator.vector[i][2])
        suofiz+=izdershki[i][len(izdershki[i])-1]
    sumofizderzhki.append(suofiz)
    #for i in range (len(countries[resi].negotiator)):
        

    print('==================')
    #time.sleep(3)
#print(vygody)
#print(izdershki)
for i in range (number):
    print(ccc[i],'Интерес:',countries[i].iner,'Позиция:',countries[i].pos)
   # print(len(vygody[i]))
outc=[]
vyvod=[[]for c in range(7)]
for i in range(len(vygody)):
    print(ccc[i],(ss-len(vygody[i]))/ss)
    outc.append((ss-len(vygody[i]))/ss)
for i in range(len(vygody)):
    print(ccc[i],'min gain:',min(vygody[i]),'max gain:',max(vygody[i]),'avg gain:',sum(vygody[i])/len(vygody[i]),'||| min loss:',min(izdershki[i]),'max loss:',max(izdershki[i]),'avg loss:',sum(izdershki[i])/len(izdershki[i]),'diffference gains and loss',sum(vygody[i])/len(vygody[i])-sum(izdershki[i])/len(izdershki[i]))
    vyvod[0].append(min(vygody[i]))
    vyvod[1].append(max(vygody[i]))
    vyvod[2].append(sum(vygody[i])/len(vygody[i]))
    vyvod[3].append(min(izdershki[i]))
    vyvod[4].append(max(izdershki[i]))
    vyvod[5].append(sum(izdershki[i])/len(izdershki[i]))
    vyvod[6].append(sum(vygody[i])/len(vygody[i])-sum(izdershki[i])/len(izdershki[i]))
print(sum(sumofizderzhki)/len(sumofizderzhki))
dic={'country':ccc,'share of outs':outc,'min gain':vyvod[0],'max gain':vyvod[1],'avg gain':vyvod[2],'min loss':vyvod[3],'max loss':vyvod[4],'avg loss':vyvod[5],'diff gains and losses':vyvod[6]}
datares=pd.DataFrame(dic)
datares.to_csv('Results.csv',sep=';',index=False,encoding='utf-16le')
