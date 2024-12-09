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
           
        return vector
def whichcountry(country,vector):
        for i in range(len(vector)):
           
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
                if ((dopvec[g][1]<(neg[i].negotiator.vector[g][1]-1))or(dopvec[g][1]>(neg[i].negotiator.vector[g][1]+1)))or((dopvec[g][2]<(neg[i].negotiator.vector[g][2]-1))or(dopvec[g][2]>(neg[i].negotiator.vector[g][2]+1))):
                    
                    return False
        return True

def copyvec(vec):
    cop=[(vec[x][0],vec[x][1],vec[x][2]) for x in range(len(vec))]
    
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

           
            new_vecg1.append(-diff1//2)
            new_vecg2.append(diff2//2)
            
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
        
        x+=abs(vec1[i][1]-vec2[i][1])
    x=x/(len(vec1)-len(cout))
    for i in range(len(vec1)):
        if i in cout:
            continue
        y+=abs(vec1[i][2]-vec2[i][2])
    y=y/(len(vec1)-len(cout))
    return x,y

def vectdiff_2(vec1,vec2,cout):
    x=0
    y=0
    for i in range(len(vec1)):
        if i in cout:
            continue
        
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
        self.willbeout=False



    def GNLvi(self,count,res):


        for i in range(1000):
            self.gnl.append(vector_create(count,res))
            




    def sorted(self,gnl):
        if len(gnl)<=1:
                return gnl
        else:

            q=random.choice(gnl)
            q_self_index=whichcountry(self,q)
            L=[]
            M=[]
            R=[]
            for elem in gnl:
                    self_index=whichcountry(self,elem)
                    
                    if elem[self_index][1]-elem[self_index][2]>q[q_self_index][1]-q[q_self_index][2]:
                            L.append(elem)
                    elif elem[self_index][1]-elem[self_index][2]<q[q_self_index][1]-q[q_self_index][2]:
                            R.append(elem)
                    else:
                            M.append(elem)
            return self.sorted(L)+M+self.sorted(R)  
            

      
        

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
        num_countries=resor//100-len(cout) 
        for i in range(len(self.gnl)):
            
            if self.gnl[i][whichcountry(country,self.gnl[i])][1]-self.gnl[i][whichcountry(country,self.gnl[i])][2]>0:
                v_diff=vectdiff(self.gnl[i],negagrgnl.vector,cout)        
                listofvector.append(((k)*((v_diff[0]+v_diff[1])/2))+((1-k)*(i)))
            else:
                listofvector.append(resor)



        
        i = listofvector.index(min(listofvector))
        v_diff=vectdiff(self.gnl[i],negagrgnl.vector,cout)
        if ((v_diff[0]+v_diff[1])/2)>153-(200)/num_countries:
                self.willbeout=True
        if (v_diff[0]+v_diff[1])/2<150-(200)/num_countries:
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
                
                continue
            if len(count[i].negotiator.newg)==0:
                count[i].negotiator.newg=[c[1] for c in count[i].negotiator.vector]
                count[i].negotiator.newl=[c[2] for c in count[i].negotiator.vector]
            newgnl=self.negotiator.communicate(count[i].negotiator)
            
            
            
            for d in range(len(newgnl[0])):
                        self.negotiator.newg[d]+=newgnl[0][d]/(len(count)-1-num_isout)
                        self.negotiator.newl[d]+=newgnl[2][d]/(len(count)-1-num_isout)
            for d in range(len(newgnl[1])):
                        count[i].negotiator.newg[d]+=newgnl[1][d]/(len(count)-1-num_isout)
                        count[i].negotiator.newl[d]+=newgnl[3][d]/(len(count)-1-num_isout)

                            




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
                negagrvec=g.decision(countries[dd].negotiator,g,countoutn,resor)
           
            g.negotiator=0
            g.initneg(negagrvec)
        
        for g in countries:
                if g.willbeout:
                        g.isout=True
                        
                
                        
        
        for g in range(len(countries)):
            if not countries[g] in countout:
                if countries[g].isout:
                    countout.append(countries[g])
                    countoutn.append(g)
      
        while True:
           
            for g in range(len(countries)):
              
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
               
            
            if isagreement(countries):
                break
            
    return False



