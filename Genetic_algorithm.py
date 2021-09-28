# -*- coding: utf-8 -*-
# Function approximation using genetic algorithm

# %% ## I- Initialisation
# Basics import
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd

# Performance
import time

#%%
def upload(name):
  temp = pd.read_csv(name,sep=";")
  temp.rename(columns={"#i": "i"}, inplace=True)
  return temp

temp = upload("C:\\Users\\flavi\\OneDrive\\Documents\\ESILV\\A3\\S2\\Datascience et IA\\TD\\Rendu algorithme Génétique\\temperature_sample.csv")
temp.head(3)

# %% ## II- Méthodes

### Fonctions d'aide

def convert2binary(nb, max = 20):
  nb = bin(nb).split("b")[1]
  while len(nb) < len(bin(max).split("b")[1]):
    nb = "0" + nb
  return nb

def t(i,a,b,c):
  return [np.sum([np.cos((np.pi)*k*(b**n))*(float(a)**n) for n in range(c)]) for k in i]

def accuracy_method(a,b,c):
  return sum(np.abs(t(temp["i"],a,b,c) - temp["t"]))/sum(np.abs(temp["i"]))*100

"""### Individu"""

class individu:
  def __init__(self, a=None, b=None, c=None, bin=None): # Val => liste contenant a,b,c
    self.bin = None

    if a != None and b != None and c != None:
      self.a, self.b, self.c = a, b, c
    elif a != None and bin != None and len(bin) == 10:
      self.a, self.bin = a, bin
      self.b, self.c = int(bin[:5],2), int(bin[5:],2)
    else:
      self.a, self.b, self.c = random.uniform(0,1), random.randint(1, 21), random.randint(1, 21)      

    if self.bin == None:
      self.bin = convert2binary(self.b) + convert2binary(self.c)
    self.accuracy = self.fitness()
      
  def __str__(self):
    return f"[{self.a} {self.b} {self.c}]"

  def __eq__(self, autreIndividu):
    return self.a == autreIndividu.a and self.b == autreIndividu.b and self.c == autreIndividu.c
  
  def fitness(self):
    self.accuracy = np.linalg.norm(t(np.array(temp["i"]), self.a, self.b, self.c) - temp["t"])
    return self.accuracy

  def display_individu(self):
    plt.figure(figsize=(10, 5))
    i = np.arange(0, 4.7, 0.0005)
    plt.grid()
    plt.plot(i, t(i,self.a, self.b, self.c), c="b", linewidth=0.5)
    plt.scatter(temp["i"], temp["t"], c='r',s=10)

"""### Sélection, mutations et croisements"""

def mutation_binaire(parent,nb=4):
  pm = random.uniform(0,1)
  um = random.uniform(0,1)
  if um < pm:
    rank = []
    while len(rank) < nb:
      val = random.randint(0,len(parent))
      while val in rank:
        val = np.random.randint(0,len(parent))
      rank.append(val)
    parent_modified = ""
    for i in range(len(parent)):
      if i in rank:
        parent_modified += "0" if parent[i] == "1" else "1"
      else:
        parent_modified += parent[i]
    return parent_modified
  return parent

def mutation_reel(parent):
  mutation_prob=random.randint(0,10)
  if mutation_prob < 3:
    vary = 1 + random.uniform(-0.05, 0.05)
    rem = parent*vary
    if abs(rem) <= 10:
      parent = rem
  return parent

def croisement_binaire(parent1,parent2):
  p1 = random.randint(0, 10)
  p2 = random.randint(0, 10)
  while p2 == p1:
    p2 = random.randint(0, 10)
  p1,p2 = min(p1,p2),max(p1,p2)
  enfant1 = parent1[0:p1]+parent2[p1:p2+1]+parent1[p2+1:10]
  enfant2 = parent2[0:p1]+parent1[p1:p2+1]+parent2[p2+1:10]
  return enfant1, enfant2

def croisement_real(parent1,parent2,eta=2): #eta entre 2 et 5: (2 => plus de variations entre les parents, 5 => moins de variations)
  u = random.uniform(0,1)
  beta = (2*u)**(1/(eta+1)) if u<=0.5 else (1/(2*(1-u)))**(1/(eta+1))
  enfant1 = 0.5*((1+beta)*parent1 + (1-beta)*parent2)
  enfant2 = 0.5*((1-beta)*parent1 + (1+beta)*parent2)
  return enfant1, enfant2

def generer_pop(count):
  return [individu() for i in range(count)]

def evaluate(pop):
  return sorted(pop, key=individu.fitness)

def selection(pop, hcount, lcount):
  return pop[:hcount] + pop[-lcount:]

def croisement(parent1, parent2):
  e1_a, e2_a = croisement_real(parent1.a, parent2.a)  
  e1_binaire, e2_binaire = croisement_binaire(parent1.bin, parent2.bin)
  return [individu(a = e1_a, bin = e1_binaire), individu(a = e2_a, bin = e2_binaire)]

def mutation(parent):
  return individu(a = mutation_reel(parent.a), bin = mutation_binaire(parent.bin))

# %% ## III- Algorithme

def algoloopSimple(SEUIL, TAILLE_POP, REPARTITION=[10/30,4/30]):
  pop = generer_pop(TAILLE_POP)
  nbriteration=0
  history = []
  solution_trouvee = False
  while not solution_trouvee:
    nbriteration+=1

    evaluation = evaluate(pop)
    history.append(evaluation[0].accuracy)

    if evaluation[0].accuracy < SEUIL:
      solution_trouvee = True

    #print("iteration numéro :", nbriteration, "- Fitness:", evaluation[0].accuracy)

    select = selection(evaluation, int(REPARTITION[0] * TAILLE_POP), int(REPARTITION[1] * TAILLE_POP))
    croises = []
    for i in range(0, len(select)//2):
      croises += croisement(random.choice(select),random.choice(select))
    mutes = []
    for i in range(len(select)):
      mutes.append(mutation(select[i]))
    newalea = generer_pop(TAILLE_POP - int(REPARTITION[0]*TAILLE_POP) - int(REPARTITION[1]*TAILLE_POP))

    pop=select[:]+croises[:]+mutes[:]+newalea[:]

  evaluation = evaluate(pop)
  best_ind = evaluation[0]
  return history, best_ind, nbriteration

# %% ## IV- Résultats

debut = time.process_time()
history, best_ind, nb_iter= algoloopSimple(0.1813,100)
diff = time.process_time()-debut

print(f"{round(diff,5)} seconds - {nb_iter} itérations")
print(best_ind.a, best_ind.b, best_ind.c, best_ind.accuracy)
print(accuracy_method(best_ind.a, best_ind.b, best_ind.c))

plt.plot(history)

# %%
val = []
for i in range(30):
  debut = time.process_time()
  history, best_ind, nb_iter= algoloopSimple(0.1813,30)
  diff = time.process_time()-debut

  print(f"{round(diff,5)} seconds - {nb_iter} itérations")
  print(best_ind.a, best_ind.b, best_ind.c, best_ind.accuracy)
  print(accuracy_method(best_ind.a, best_ind.b, best_ind.c))
  val.append(diff)
print(val)
print(np.mean(val))
plt.boxplot(val)



# %% ## V- Téléchargement des données

def generate_download_file(a,b,c):
  with open("flavien_deseure--charron.txt","w") as file:
    file.write(f"{a};{b};{c}")

generate_download_file(best_ind.a, best_ind.b, best_ind.c)