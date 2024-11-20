import random
import pandas as pd
import copy
import time


class GainsLosses:
    def __init__(self,country):
        self.gain=0
        self.loss=0
        self.country=country

    def gnlcreate(self,gains,losses):
        self.gain=gains
        self.loss=losses




class GNLvector:
    def __init__(self,count,resources):
        self.resources=resources
        self.countries=count
        self.vector=[]

    def vectorcreate(self):
        gainres=self.resources
        lossres=self.resources
        x=random.randint(0,len(self.countries)-1)
        xused=[]
        self.vector=[GainsLosses(self.countries[c]) for c in range(len(self.countries)) ]
        for i in range (len(self.countries)):
            bl=True
            while  bl:
                x=random.randint(0,len(self.countries)-1)
                if not (x in xused):
                    bl=False

            xused.append(x)


            g=random.randint(0,gainres)
            gainres-=g
            l=random.randint(0,lossres)
            lossres-=l
            self.vector[x].gnlcreate(g,l)

    def whichcountry(self,country):
        for i in range(len(self.vector)):
            if country==self.vector[i].country:
                return i


def isagreement(neg):
        d=0
        for i in range(len(neg)):
            if not neg[i].isout:
                d=i
        dopvec=neg[d].negotiator.vector
        for i in range(len(neg)):
            if neg[i].isout:
                continue
            for g in range(len(neg[i].negotiator.vector)):
                if (dopvec[g].gain!=neg[i].negotiator.vector[g].gain)or(dopvec[g].loss!=neg[i].negotiator.vector[g].loss):
                    return False
        return True

def copyvec(vec):
    cop=[GainsLosses(vec[x].country) for x in range(len(vec)) ]
    for i in range (len(vec)):

        cop[i].gain=vec[i].gain
        cop[i].loss=vec[i].loss
    return cop

class Negotiator:
    def __init__(self,pos,vector):
        self.pos=pos
        self.vector=copyvec(vector)
        self.newg=[]
        self.newl=[]






    def ReplaceWithAverage(self):
        for i in range(len(self.vector)):
            ng=0
            nl=0
            for g in range(len(self.newg)):
                ng+=self.newg[g][i]
                nl+=self.newl[g][i]
            self.vector[i].gain=ng//(len(self.newg))
            self.vector[i].loss=nl//(len(self.newl))

    def communicate(self,neg):
        new_vecg1=[]
        new_vecg2=[]
        new_vecl1=[]
        new_vecl2=[]

        if self.pos<neg.pos:
            posdiv=self.pos/neg.pos
        if self.pos>neg.pos:
            posdiv=neg.pos/self.pos


        k=0.5
        for i in range (len(self.vector)):
            diff=abs(self.vector[i].gain-neg.vector[i].gain)
            if self.pos<neg.pos:
                diff1=diff+(diff*(1-posdiv)*k)
                diff2=diff-(diff*(1-posdiv)*k)
            if self.pos>neg.pos:
                diff1=diff-(diff*(1-posdiv)*k)
                diff2=diff+(diff*(1-posdiv)*k)
            if self.pos==neg.pos:
                diff1=diff2=diff
            if self.vector[i].gain<neg.vector[i].gain:
                diff1=-diff1
                diff2=-diff2


            new_vecg1.append(self.vector[i].gain-diff1//2)
            new_vecg2.append(neg.vector[i].gain+diff2//2)

        for i in range(len(self.vector)):
            diff=abs(self.vector[i].loss-neg.vector[i].loss)
            if self.pos<neg.pos:
                diff1=diff+(diff*(1-posdiv)*k)
                diff2=diff-(diff*(1-posdiv)*k)
            if self.pos>neg.pos:
                diff1=diff-(diff*(1-posdiv)*k)
                diff2=diff+(diff*(1-posdiv)*k)
            if self.pos==neg.pos:
                diff1=diff2=diff
            if self.vector[i].loss<neg.vector[i].loss:
                diff2=-diff2
                diff1=-diff1

            new_vecl1.append(self.vector[i].loss-diff1//2)
            new_vecl2.append(neg.vector[i].loss+diff2//2)
        return new_vecg1,new_vecg2,new_vecl1,new_vecl2




def vectdiff(vec1,vec2,cout):
    x=0
    y=0
    for i in range(len(vec1)):
        if i in cout:
            continue
        #x+=abs((vec1[i].gain-vec2[i].gain))
        x+=(vec1[i].gain-vec2[i].gain)**2
    x=x**0.5
    for i in range(len(vec1)):
        if i in cout:
            continue
        y+=(vec1[i].loss-vec2[i].loss)**2
    y=y**0.5
    return x,y




class Country:
    def __init__(self,pos,inter):
        self.gnl=[]
        self.pos=pos
        self.iner=inter
        self.isfirst=True
        self.negotiator=0
        self.isagreed=False
        self.isout=False
        self.isregime=False



    def GNLvi(self,count,res):


        for i in range(100):
            self.gnl.append(GNLvector(count,res))
            self.gnl[i].vectorcreate()




    def sorted(self,country):


        for i in range(len(self.gnl)):

            dopi=GNLvector(self.gnl[i].countries,self.gnl[i].resources)
            dopi.vector=copyvec(self.gnl[i].vector)
            #copyvec(self.gnl[i].vector)
            #self.gnl[i]
            dopgnl=i
            for g in range(i,len(self.gnl)):
                if self.gnl[g].vector[self.gnl[g].whichcountry(country)].gain-self.gnl[g].vector[self.gnl[g].whichcountry(country)].loss>dopi.vector[dopi.whichcountry(country)].gain-dopi.vector[dopi.whichcountry(country)].loss:
                    dopi=GNLvector(self.gnl[g].countries,self.gnl[g].resources)
                    dopi.vector=copyvec(self.gnl[g].vector)
                    dopgnl=g


            self.gnl[dopgnl].vector=copyvec(self.gnl[i].vector)
            self.gnl[i].vector=copyvec(dopi.vector)

    def zapis(self,d,sd):
        vv=[]
        gg=[]
        ll=[]
        for i in range(len(self.gnl)):
            for g in range(len(self.gnl[i].vector)):
                vv.append(i)
                gg.append(self.gnl[i].vector[g].gain)
                ll.append(self.gnl[i].vector[g].loss)
        dic={'vector':vv,'gain':gg,'loss':ll}
        data=pd.DataFrame(dic)
        data.to_csv(str(sd)+'__'+str(d)+'.csv',index=False,sep=';')

    def initneg(self,vec):

        self.negotiator=0
        if self.isfirst:
            self.isfirst=False
            self.negotiator =Negotiator(self.pos,self.gnl[0].vector)
            return
        self.negotiator=Negotiator(self.pos,self.gnl[vec].vector)




    def decision(self,negagrgnl,country,cout,resor):
        listofvector=[]
        k=self.iner/100
        for i in range(len(self.gnl)):
            if self.gnl[i].vector[self.gnl[i].whichcountry(country)].gain-self.gnl[i].vector[self.gnl[i].whichcountry(country)].loss>0:
                listofvector.append((k*((vectdiff(self.gnl[i].vector,negagrgnl,cout)[0]+vectdiff(self.gnl[i].vector,negagrgnl,cout)[1])/2))+((1-k)*i))



        for i in range(len(listofvector)):
            if listofvector[i]==min(listofvector):
                #print((vectdiff(self.gnl[i].vector,negagrgnl,cout)[0]+vectdiff(self.gnl[i].vector,negagrgnl,cout)[1])/2,(1.2*(resor/10)*(len(self.gnl[i].vector)-len(cout))**0.5))

                if (vectdiff(self.gnl[i].vector,negagrgnl,cout)[0]+vectdiff(self.gnl[i].vector,negagrgnl,cout)[1])/2<(10*(len(self.gnl[i].vector)-len(cout))):
                    self.isagreed=True
                if ((vectdiff(self.gnl[i].vector,negagrgnl,cout)[0]+vectdiff(self.gnl[i].vector,negagrgnl,cout)[1])/2)>(1.6*(resor/10)*(len(self.gnl[i].vector)-len(cout))**0.5):
                                                                                                                        #(resor/(len(self.gnl[i].vector)-len(cout)))):
                    #-len(cout)
                    self.isout=True
                if (vectdiff(self.gnl[i].vector,negagrgnl,cout)[0]+vectdiff(self.gnl[i].vector,negagrgnl,cout)[1])/2<(1.5*(resor/10)*(len(self.gnl[i].vector)-len(cout))**0.5):
                    self.isregime=True
                else:
                    self.isregime=False
                

                return i



    def communicate(self,count):
        for i in range(len(count)):
            if count[i].isout:
                continue
            newgnl=self.negotiator.communicate(count[i].negotiator)

            self.negotiator.newg.append(newgnl[0])
            self.negotiator.newl.append(newgnl[2])
            count[i].negotiator.newg.append(newgnl[1])
            count[i].negotiator.newl.append(newgnl[3])




def cycle(countries,resor):

    countout=[]
    countoutn=[]
    for i in range(7):



        negagrvec=0


        bl=True
        for g in countries:
            if g.isout:
                continue
            if not g.isregime:
                bl=False
        if bl:

            return True
            break

        while True:
            dd=random.randint(0,len(countries)-1)
            
            if not countries[dd].isout:
                break
        
        for g in countries:

            if i!=0:
                negagrvec=g.decision(countries[dd].negotiator.vector,g,countoutn,resor)
            g.negotiator=0
            g.initneg(negagrvec)
        for g in range(len(countries)):
            if not countries[g] in countout:
                if countries[g].isout:
                    countout.append(countries[g])
                    countoutn.append(g)



        for g in countries:
            if g.isout:
                    #print('isout')
                    continue

        while True:

            for g in range(len(countries)):
                for d in range(len(countries)):
                    if d!=g and (not countries[d].isout) and (not countries[g].isout):
                        countries[g].communicate(countries)


            for g in countries:
                if (g.isout) |(len(g.negotiator.newg)==0)|(len(g.negotiator.newl)==0):
                    continue
                g.negotiator.ReplaceWithAverage()
                g.negotiator.newg=[]
                g.negotiator.newl=[]
            if isagreement(countries):
                break


    return False





data=pd.read_csv('data.csv',sep=';')
number=len(data['Country'].tolist())
vygody=[[]for c in range(number)]
izdershki=[[]for c in range(number)]
#ccc=['Canada','Sweden','Norway','USA','Iceland','Denmark','Finland','Russia']
ccc=data['Country'].tolist()
ss=150
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
        i.GNLvi(countries,200)
        i.sorted(i)
    bl=False
    bl=cycle(countries,200)
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
    for i in range(len(countries[resi].negotiator.vector)):
        if countries[i].isout:
            print(i,'isout','isout')
            continue
        print(ccc[i],'Выгоды:',countries[resi].negotiator.vector[i].gain,'Издержки:',countries[resi].negotiator.vector[i].loss)
        vygody[i].append(countries[resi].negotiator.vector[i].gain)
        izdershki[i].append(countries[resi].negotiator.vector[i].loss)
        suofiz+=izdershki[i][len(izdershki[i])-1]
    sumofizderzhki.append(suofiz)
    #for i in range (len(countries[resi].negotiator.vector)):
        

    print('==================')
    #time.sleep(3)
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