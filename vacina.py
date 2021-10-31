import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
#pip install openpyxl

df = pd.read_csv("https://s3-sa-east-1.amazonaws.com/ckan.saude.gov.br/PNI/vacina/uf/2021-04-05/uf%3DAC/part-00000-00cdbe61-e0aa-4158-aa8d-3057bbea561d.c000.csv",header=0, sep=";")

######################DOSES POR DIA###################

data = df['vacina_dataAplicacao']
dy = pd.DataFrame(np.zeros(len(data)))
dy.columns=['DA']

for i in range(len(data)):
    dy['DA'][i]=data[i][:10 or None]


##############VACINA UTILIZADA############################
    
vacina_nome = df['vacina_nome']
sinovac = np.zeros(len(vacina_nome))
covishield = np.zeros(len(vacina_nome))
janssen = np.zeros(len(vacina_nome))

for i in range(len(vacina_nome)):
    if "Sinovac" in vacina_nome[i]: 
       sinovac[i]=1
    elif "Covishield" in vacina_nome[i]:
       covishield[i]=1
    elif "Janssen" in vacina_nome[i]:
       janssen[i]=1


###########################QUAL A DOSE###############################
       
dose_semfiltro = df['vacina_descricao_dose']
primeira_dose = np.zeros(len(dose_semfiltro))
segunda_dose = np.zeros(len(dose_semfiltro))

for i in range(len(dose_semfiltro)):
    if "1ª Dose" in dose_semfiltro[i]: 
       primeira_dose[i]=1
    elif "2ª Dose" in dose_semfiltro[i]:
       segunda_dose[i]=1
    elif "Janssen" in vacina_nome[i]:
       primeira_dose[i]=1


##########################Quantas doses por dia#####################################
       
x = np.stack([sinovac, covishield, janssen, primeira_dose, segunda_dose], axis=1)
v = pd.DataFrame(x)
m = pd.concat([pd.DataFrame(dy), v], axis = 1)
m.columns=['Data de Aplicação','Sinovac', 'Covishield', 'Janssen', 'Primeira Dose', 'Segunda Dose']
n = m.groupby(['Data de Aplicação']).sum()

writer = pd.ExcelWriter('vacinacao.xlsx')
n.to_excel(writer)
writer.save()

################################# Nome ############################################

dates = n.index
x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
y = n['Sinovac']
z = n['Janssen']
w = n['Covishield']

fig, ax2 = plt.subplots()

plt.title('Nomes')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=6))
ax2.plot(x, y, label='Sinovac')
ax2.plot(x, z, label = 'Janssen')
ax2.plot(x, w, label = 'Covishield')
plt.legend()
plt.gcf().autofmt_xdate()


plt.savefig('nome.png')

################################ Dose #################################################

x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
p = n['Primeira Dose']
s = n['Segunda Dose']

fig, ax1 = plt.subplots()
plt.title('Doses')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=6))
ax1.plot(x,p, label = 'Primeira Dose')
ax1.plot(x,s, label = 'Segunda Dose')
plt.legend()
plt.gcf().autofmt_xdate()

plt.savefig('dose.png')

###############################Excel###############################

writer = pd.ExcelWriter('vacinacao.xlsx', engine = 'xlsxwriter')
n.to_excel(writer, sheet_name='Sheet1')
worksheet = writer.sheets['Sheet1']
worksheet.insert_image('G12','nome.png')
worksheet.insert_image('G1','dose.png')
writer.save()

