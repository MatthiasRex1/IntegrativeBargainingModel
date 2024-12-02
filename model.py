import random
import pandas as pd
import copy
import time

'''
class GainsLosses:
    def __init__(self,country):
        self.gain=0
        self.loss=0
        self.country=country

    def gnlcreate(self,gains,losses):
        self.gain=gains
        self.loss=losses

'''

def vector_create(countries,resources):
        gainres=resources
        lossres=resources
        x=random.randint(0,len(countries)-1)
        xused=[]
        vector=[(countries[c],0,0) for c in range(len(countries)) ]
        for i in range (len(countries)):
            bl=True
            while  bl:
                x=random.randint(0,len(countries)-1)
                if not (x in xused):
                    bl=False

            xused.append(x)


            g=random.randint(0,gainres)
            gainres-=g
            l=random.randint(0,lossres)
            lossres-=l
            vector[x]=(vector[x][0],g,l)
            #vector[x][1]=g
            #vector[x][2]=l
        return vector
def whichcountry(country,vector):
        for i in range(len(vector)):
            #print(country,
            if country==vector[i][0]:
                return i
'''
class GNLvector:
    def __init__(self,count,resources):
        self.resources=resources
        self.countries=count
        self=[]

    def vectorcreate(self):
        self=vecc1_(self.resources,self,self.countries)
        

    def whichcountry(self,country):
        for i in range(len(self)):
            #print(country,
            if country==self[i][0]:
                return i
'''

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
                #if (dopvec[g][1]!=neg[i].negotiator.vector[g][1])or(dopvec[g][2]!=neg[i].negotiator.vector[g][2]):
                if ((dopvec[g][1]<(neg[i].negotiator.vector[g][1]-3))or(dopvec[g][1]>(neg[i].negotiator.vector[g][1]+3)))or((dopvec[g][2]<(neg[i].negotiator.vector[g][2]-3))or(dopvec[g][2]>(neg[i].negotiator.vector[g][2]+3))):
                    #print('aAAAAAAAA', i, g)
                    return False
        return True

def copyvec(vec):
    cop=[[vec[x][0],0,0] for x in range(len(vec)) ]
    for i in range (len(vec)):

        cop[i][1]=vec[i][1]
        cop[i][2]=vec[i][2]
    return cop

class Negotiator:
    def __init__(self,pos,vector):
        self.pos=pos
        self.vector=copyvec(vector)
        self.newg=[]
        self.newl=[]






    def ReplaceWithAverage(self):
        for i in range(len(self.vector)):
            self.vector[i]=(self.vector[i][0],int(self.newg[i]),int(self.newl[i]))
           # self.vector[i][1]=ng//(len(self.newg))
            #self.vector[i][2]=nl//(len(self.newl))
        #self.newg=[]
        #self.newl=[]

    def communicate(self,neg):
        new_vecg1=[]
        new_vecg2=[]
        new_vecl1=[]
        new_vecl2=[]

        if self.pos<neg.pos:
            posdiv=self.pos/neg.pos
        elif self.pos>neg.pos:
            posdiv=neg.pos/self.pos
        else:
            posdiv=0    


        k=0.5
        for i in range (len(self.vector)):
            diff=abs(self.vector[i][1]-neg.vector[i][1])
            if self.pos<neg.pos:
                diff1=diff+(diff*(1-posdiv)*k)
                diff2=diff-(diff*(1-posdiv)*k)
            if self.pos>neg.pos:
                diff1=diff-(diff*(1-posdiv)*k)
                diff2=diff+(diff*(1-posdiv)*k)
            if self.pos==neg.pos:
                diff1=diff2=diff
            if self.vector[i][1]<neg.vector[i][1]:
                diff1=-diff1
                diff2=-diff2


            new_vecg1.append(self.vector[i][1]-diff1//2)
            new_vecg2.append(neg.vector[i][1]+diff2//2)
            diff1=0
            diff2=0
            diff=0
       # for i in range(len(self.vector)):
            diff=abs(self.vector[i][2]-neg.vector[i][2])
            if self.pos<neg.pos:
                diff1=diff+(diff*(1-posdiv)*k)
                diff2=diff-(diff*(1-posdiv)*k)
            if self.pos>neg.pos:
                diff1=diff-(diff*(1-posdiv)*k)
                diff2=diff+(diff*(1-posdiv)*k)
            if self.pos==neg.pos:
                diff1=diff2=diff
            if self.vector[i][2]<neg.vector[i][2]:
                diff2=-diff2
                diff1=-diff1

            new_vecl1.append(self.vector[i][2]-diff1//2)
            new_vecl2.append(neg.vector[i][2]+diff2//2)
        return new_vecg1,new_vecg2,new_vecl1,new_vecl2




def vectdiff(vec1,vec2,cout):
    x=0
    y=0
    for i in range(len(vec1)):
        if i in cout:
            continue
        #x+=abs((vec1[i].gain-vec2[i].gain))
        x+=abs(vec1[i][1]-vec2[i][1])#**2
    x=x/(len(vec1)-len(cout))
    for i in range(len(vec1)):
        if i in cout:
            continue
        y+=abs(vec1[i][2]-vec2[i][2])#**2
    y=y/(len(vec1)-len(cout))
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


        for i in range(500):
            self.gnl.append(vector_create(count,res))
            #self.gnl[i]create()




    def sorted(self,country):


        for i in range(len(self.gnl)):

            #dopi=#vector_create(self.gnl[i].countries,self.gnl[i].resources)
            
            dopi=copyvec(self.gnl[i])
            #copyvec(self.gnl[i])
            #self.gnl[i]
            dopgnl=i
            for g in range(i,len(self.gnl)):
                if self.gnl[g][whichcountry(country,self.gnl[g])][1]-self.gnl[g][whichcountry(country,self.gnl[g])][2]>dopi[whichcountry(country,dopi)][1]-dopi[whichcountry(country,dopi)][2]:
                    #dopi=GNLvector(self.gnl[g].countries,self.gnl[g].resources)
                    dopi=copyvec(self.gnl[g])
                    dopgnl=g


            self.gnl[dopgnl]=copyvec(self.gnl[i])
            self.gnl[i]=copyvec(dopi)

    def zapis(self,d,sd):
        vv=[]
        gg=[]
        ll=[]
        for i in range(len(self.gnl)):
            for g in range(len(self.gnl[i])):
                vv.append(i)
                gg.append(self.gnl[i][g][1])
                ll.append(self.gnl[i][g][2])
        dic={'vector':vv,'gain':gg,'loss':ll}
        data=pd.DataFrame(dic)
        data.to_csv(str(sd)+'__'+str(d)+'.csv',index=False,sep=';')

    def initneg(self,vec):

        self.negotiator=0
        if self.isfirst:
            self.isfirst=False
            self.negotiator =Negotiator(self.pos,self.gnl[0])
            return
        self.negotiator=Negotiator(self.pos,self.gnl[vec])




    def decision(self,negagrgnl,country,cout,resor):
        listofvector=[]
        k=self.iner/100
        
        for i in range(len(self.gnl)):
            
            if self.gnl[i][whichcountry(country,self.gnl[i])][1]-self.gnl[i][whichcountry(country,self.gnl[i])][2]>0:
                v_diff=vectdiff(self.gnl[i],negagrgnl.vector,cout)        
                listofvector.append(((k)*((v_diff[0]+v_diff[1])/2))+((1-k)*i))



        for i in range(len(listofvector)):
            if listofvector[i]==min(listofvector):
                #print((vectdiff(self.gnl[i],negagrgnl,cout)[0]+vectdiff(self.gnl[i],negagrgnl,cout)[1])/2,(1.2*(resor/10)*(len(self.gnl[i])-len(cout))**0.5))
                
                v_diff=vectdiff(self.gnl[i],negagrgnl.vector,cout)
                if (v_diff[0]+v_diff[1])/2<(10*(len(self.gnl[i])-len(cout))):
                    self.isagreed=True
                if ((v_diff[0]+v_diff[1])/2)>resor//15: #(1.6*(resor/10)*(len(self.gnl[i])-len(cout))**0.5):
                    self.isout=True
                if (v_diff[0]+v_diff[1])/2<resor//13: # (1.5*(resor/10)*(len(self.gnl[i])-len(cout))**0.5):
                    self.isregime=True
                else:
                    self.isregime=False
                

                return i



    def communicate(self,count):
        #len_count=0
        #for i in range(len(count)):
              #  if count[i].isout:
                      #  continue
              #  else:
                       # len_count+=1
        
        for i in range(len(count)):
            if count[i].isout:
                continue
            newgnl=self.negotiator.communicate(count[i].negotiator)
           # newgnl=([int(c/(len_count))for c in newgnl[0]],[int(c/(len_count)) for c in newgnl[1]],[int(c/(len_count)) for c in newgnl[2]],[int(c/(len_count)) for c in newgnl[3]])
            #for d in range(len(newgnl[0])):
            #print('111111',  newgnl) 
            if len(self.negotiator.newg)==0:
                    self.negotiator.newg =[c for c in newgnl[0]]
                    self.negotiator.newl= [c for c in newgnl[2]]
            else:
                    for d in range(len(newgnl[0])):
                            self.negotiator.newg[d]=(newgnl[0][d]+self.negotiator.newg[d])/2
                            self.negotiator.newl[d]=(newgnl[2][d]+self.negotiator.newl[d])/2
            if len(count[i].negotiator.newg)==0:
                    count[i].negotiator.newg=[c for c in newgnl[1]]
                    count[i].negotiator.newl=[c for c in newgnl[3]]
            else:
                    for d in range(len(newgnl[1])):
                            count[i].negotiator.newg[d]=(newgnl[1][d]+count[i].negotiator.newg[d])/2
                            count[i].negotiator.newl[d]=(newgnl[3][d]+count[i].negotiator.newl[d])/2

                            




def cycle(countries,resor):
    
    countout=[]
    countoutn=[]
    for i in range(7):

        print(i)

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
        #print(i,' 1')
        while True:
            dd=random.randint(0,len(countries)-1)
            
            if not countries[dd].isout:
                break
        #print(i,' 2')
        for g in countries:

            if i!=0:
                negagrvec=g.decision(countries[dd].negotiator,g,countoutn,resor)
           # print('-----',negagrvec)
            g.negotiator=0
            g.initneg(negagrvec)
        #print(i,' 3')
        for g in range(len(countries)):
            if not countries[g] in countout:
                if countries[g].isout:
                    countout.append(countries[g])
                    countoutn.append(g)
        #print(i,' 4')



        for g in countries:
            if g.isout:
                    #print('isout')
                    continue
        print(i,' 5')
        while True:

            for g in range(len(countries)):
               # print(i, ' 5.5: ',g) 
                for d in range(g,len(countries)):   	
                    if d!=g and (not countries[d].isout) and (not countries[g].isout):
                        
                        countries[g].communicate(countries)            
            #print(i,' 5.5')
            g_i=0
            for g in countries:
                if (g.isout) |(len(g.negotiator.newg)==0)|(len(g.negotiator.newl)==0):
                    print('hohma')
                    continue
                g_i+=1
                #print(i, '6: ', g_i)
                g.negotiator.ReplaceWithAverage()
                g.negotiator.newg=[]
                g.negotiator.newl=[]
                print('----',[(c[1],c[2])for c in g.negotiator.vector])
        
            if isagreement(countries):
                break

        print(i,' 6')
    return False





data=pd.read_csv('data.csv',sep=';')
number=len(data['Country'].tolist())
vygody=[[]for c in range(number)]
izdershki=[[]for c in range(number)]
#ccc=['Canada','Sweden','Norway','USA','Iceland','Denmark','Finland','Russia']
ccc=data['Country'].tolist()
ss=2
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
