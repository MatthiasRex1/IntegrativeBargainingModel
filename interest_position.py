from model import cycle,Country
import pandas as pd
import matplotlib.pyplot as plt

dic={'interest':[],'gains_1':[],'gains_2':[],'losses_1':[],'losses_2':[],'outs_1':[],'outs_2':[]}
for i in range(0,101,5):
    gains=[0,0]
    losses=[0,0]
    outs=[0,0]
    num_of_iter=50
    for d in range(num_of_iter):
        print(i,d)
        #print(
        countries=[Country(50,i),Country(50,i)]
        for g in range(len(countries)):
            #d+=1
            countries[g].GNLvi(countries,len(countries)*100)
            countries[g].sorted(countries[g])
        cycle(countries,200)
        resi=0
        for g in range(len(countries)):
           if not countries[g].isout:
                resi=g
                continue
           outs[g]+=1
        for g in range(len(countries[resi].negotiator.vector)):
            if countries[g].isout:               
                continue
            gains[g]+=countries[resi].negotiator.vector[g][1]
            losses[g]+=countries[resi].negotiator.vector[g][2]
            #print(g,countries[resi].negotiator.vector[g][1],countries[resi].negotiator.vector[g][2])
    dic['interest'].append(i)
    if outs[0]==num_of_iter:
        dic['gains_1'].append(0)
        dic['losses_1'].append(0)
    else:
        dic['losses_1'].append(losses[0]/(num_of_iter-outs[0]))
        dic['gains_1'].append(gains[0]/(num_of_iter-outs[0]))
    if outs[1]==num_of_iter:
        dic['gains_2'].append(0)
        dic['losses_2'].append(0)
    else:
        
        dic['gains_2'].append(gains[1]/(num_of_iter-outs[1]))
    
        dic['losses_2'].append(losses[1]/(num_of_iter-outs[1]))
    dic['outs_1'].append(outs[0]/num_of_iter)
    dic['outs_2'].append(outs[1]/num_of_iter)

#print
pd.DataFrame(dic).to_csv('interest_dynamics.csv',sep=';',index=False)
fil=open('interest_dynamics.csv','r')
st=fil.read().replace('.',',')
fil.close()
fil=open('interest_dynamics.csv','w')#.write(st).close()
fil.write(st)
fil.close()
plt.plot([c for c in range(0,101,5)],dic['gains_1'])
plt.plot([c for c in range(0,101,5)],dic['gains_2'])
plt.show()    
            
            
        
        
