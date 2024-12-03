import random
import pandas as pd
import copy
import time
import numpy as np

def vector_create(countries,resources):
        gainres=resources
        lossres=resources
        x=np.random.randint(0,len(countries))
        xused=[]
        vector=[(countries[c],0,0) for c in range(len(countries)) ]
        for i in range (len(countries)):
            bl=True
            while  bl:
                x=np.random.randint(0,len(countries))
                if not (x in xused):
                    bl=False

            xused.append(x)


            g=np.random.randint(0,gainres)
            gainres-=g
            l=np.random.randint(0,lossres)
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
                if ((dopvec[g][1]<(neg[i].negotiator.vector[g][1]-5))or(dopvec[g][1]>(neg[i].negotiator.vector[g][1]+5)))or((dopvec[g][2]<(neg[i].negotiator.vector[g][2]-5))or(dopvec[g][2]>(neg[i].negotiator.vector[g][2]+5))):
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
                diff1=diff
                diff2=diff
            if self.vector[i][1]<neg.vector[i][1]:
                diff1=-diff1
                diff2=-diff2

           # print(self.vector[i][1],neg.vector[i][1])
            new_vecg1.append(-diff1//2)
            new_vecg2.append(diff2//2)
            #print(new_vecg1,'\n ---\n',new_vecg2)
            diff1=0
            diff2=0
            diff=0
       
            diff=abs(self.vector[i][2]-neg.vector[i][2])
            if self.pos<neg.pos:
                diff1=diff+(diff*(1-posdiv)*k)
                diff2=diff-(diff*(1-posdiv)*k)
            if self.pos>neg.pos:
                diff1=diff-(diff*(1-posdiv)*k)
                diff2=diff+(diff*(1-posdiv)*k)
            if self.pos==neg.pos:
                diff1=diff
                diff2=diff
            if self.vector[i][2]<neg.vector[i][2]:
                diff2=-diff2
                diff1=-diff1

            new_vecl1.append(-diff1//2)
            new_vecl2.append(diff2//2)
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

def vectdiff_2(vec1,vec2,cout):
    x=0
    y=0
    for i in range(len(vec1)):
        if i in cout:
            continue
        #x+=abs((vec1[i].gain-vec2[i].gain))
        x+=(vec1[i][1]-vec2[i][1])**2
    x=x**0.5
    for i in range(len(vec1)):
        if i in cout:
            continue
        y+=(vec1[i][2]-vec2[i][2])**2
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
                listofvector.append(((k)*((v_diff[0]+v_diff[1])/2))+((1-k)*(i*(resor//100))))



        for i in range(len(listofvector)):
            if listofvector[i]==min(listofvector):
                #print((vectdiff(self.gnl[i],negagrgnl,cout)[0]+vectdiff(self.gnl[i],negagrgnl,cout)[1])/2,(1.2*(resor/10)*(len(self.gnl[i])-len(cout))**0.5))
                
                v_diff=vectdiff(self.gnl[i],negagrgnl.vector,cout)
                if (v_diff[0]+v_diff[1])/2<(10*(len(self.gnl[i])-len(cout))):
                    self.isagreed=True
                if ((v_diff[0]+v_diff[1])/2)>resor//3.7: #(1.6*(resor/10)*(len(self.gnl[i])-len(cout))**0.5):
                    self.isout=True
                if (v_diff[0]+v_diff[1])/2<resor//3.7: # (1.5*(resor/10)*(len(self.gnl[i])-len(cout))**0.5):
                    self.isregime=True
                else:
                    self.isregime=False
                

                return i



    def communicate(self,count):
        if len(self.negotiator.newg)==0:
                self.negotiator.newg =[c[1] for c in self.negotiator.vector]
                self.negotiator.newl= [c[2] for c in self.negotiator.vector]

        
        num_isout=0
        for i in count:
                if i.isout:
                        num_isout+=1
        for i in range(count.index(self),len(count)):
            if count[i].isout or self==count[i]:
                #print(self==count[i])
                continue
            if len(count[i].negotiator.newg)==0:
                count[i].negotiator.newg=[c[1] for c in count[i].negotiator.vector]
                count[i].negotiator.newl=[c[2] for c in count[i].negotiator.vector]
            newgnl=self.negotiator.communicate(count[i].negotiator)
            
            
            
            for d in range(len(newgnl[0])):
                        self.negotiator.newg[d]+=newgnl[0][d]/(len(count)-1-num_isout)#(newgnl[0][d]+self.negotiator.newg[d])/2#np.mean([newgnl[0][d],self.negotiator.newg[d]])
                        self.negotiator.newl[d]+=newgnl[2][d]/(len(count)-1-num_isout)#(newgnl[2][d]+self.negotiator.newl[d])/2#np.mean([newgnl[2][d],self.negotiator.newl[d]])
            for d in range(len(newgnl[1])):
                        count[i].negotiator.newg[d]+=newgnl[1][d]/(len(count)-1-num_isout)#(newgnl[1][d]+count[i].negotiator.newg[d])/2#np.mean([newgnl[1][d],count[i].negotiator.newg[d]])
                        count[i].negotiator.newl[d]+=newgnl[3][d]/(len(count)-1-num_isout)#(newgnl[3][d]+count[i].negotiator.newl[d])/2#np.mean([newgnl[3][d],count[i].negotiator.newl[d]])

                            




def cycle(countries,resor):
    
    countout=[]
    countoutn=[]
    for i in range(7):

        #print(i)

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
        #print(i,' 5')
        while True:
           # print([(round(sum([a[0] for a in c])/len([a[0] for a in c]),2),round(sum([a[1] for a in c])/len([a[1] for a in c]),2)) for c in list(map(list,zip(*[[(f[1],f[2]) for f in g] for g in [d.negotiator.vector for d in countries]])))] )
            
            for g in range(len(countries)):
               # print('----',[(c[1],c[2])for c in countries[g].negotiator.vector])
                if  (not countries[g].isout):
                        
                        countries[g].communicate(countries)            
            
            g_i=0
            for g in countries:
                if (g.isout) |(len(g.negotiator.newg)==0)|(len(g.negotiator.newl)==0):
                    
                    continue
                g_i+=1
                
                g.negotiator.ReplaceWithAverage()
                g.negotiator.newg=[]
                g.negotiator.newl=[]
                #print('----',[(c[1],c[2])for c in g.negotiator.vector])
            #print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            #print([round((sum(c[1])/len(c[1])-sum(c[2])/len(c[2])),2) for c in list(map(list,zip(*[[(f[1],f[2]) for f in g] for g in [d.negotiator.vector for d in countries]])))] )
            #print([(round(sum([a[0] for a in c])/len([a[0] for a in c]),2),round(sum([a[1] for a in c])/len([a[1] for a in c]),2)) for c in list(map(list,zip(*[[(f[1],f[2]) for f in g] for g in [d.negotiator.vector for d in countries]])))] )
            if isagreement(countries):
                break
            #assert False
        #print(i,' 6')
    return False



