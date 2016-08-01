#!/usr/bin/python3

from qrcodeoutils import *

annulateur=285#0x11d#0b100011101

@memorise
class F256():
  def __init__(self,s):
    if isinstance(s,str) or hasattr(s,'__iter__') or hasattr(s,'iter'):
      self.val=bin2dec(s)
    elif type(s) is F256:
      self.val=s.val
    else:
      self.val=s
    while True:
      ch=bin(self.val)[2:]
      if len(ch)<=8:
        break
      self.val^=annulateur*2**(9-len(ch))
    self.corps=F256
  def __str__(self):
#    nb=bin(self.val)[2:]
#    nb="0"*(8-len(nb))+nb
#    nb2=""
#    for c in nb:
#      nb2=nb2+c+"\u0305"
    nb=hex(self.val)[2:]
    return nb
  def __repr__(self):
    return str(self)
  def __add__(self,n):
    return F256(self.val^n.val)
  def __sub__(self,n):
    return self+n
  def __neg__(self):
    return self
  def __mul__(self,n):
    if self.val==0 or n.val==0:
      return F256(0)
    else:
      return F256(F256.exp((self.log()+n.log())))
  def __truediv__(self,n):
    if n.val==0:
      raise ZeroDivisionError
    if self.val==0:
      return F256(0)
    return F256(F256.exp((self.log()-n.log())))
  def __pow__(self,e):
    if self.val==0:
      if e<0:
        raise ZeroDivisionError
      elif e==0:
        return F256(1)
      else:
        return F256(0)
    return F256(F256.exp((e*self.log())))
  def log(self):
    if self.val==0:
      raise ZeroDivisionError
    return F256.log[self.val]

F256.log=dict()
exp=[]
nb=1
for i in range(255):
  F256.log[nb]=i
  exp.append(nb)
  nb*=2
  if nb>=256:
    nb^=annulateur
F256.exp=lambda i:exp[i%255]
#F256.exp.append(1)
#F256.exp*=2
F256.__name__="𝔽_2⁸"

@memorise
class Polynome(ElementAnneau):

  def __init__(self,c):
    if type(c) is Polynome:
      self.coefficients=tuple(c.coefficients)
    elif type(c) is Polynome.corps:
      self.coefficients=(c,)
    elif not hasattr(c,'__iter__') and not hasattr(c,'iter'):
      self.coefficients=(Polynome.corps(c),)
    else:
      self.coefficients=tuple(c)
    try:
      while self.coefficients[0]==Polynome.corps(0):
        self.coefficients=self.coefficients[1:]
    except IndexError:
      pass

  def estzero(self):
    return self.coefficients==tuple()

  def __str__(self):
    if self.estzero():
      return "0"
    expo={"0":"⁰","1":"¹","2":"²","3":"³","4":"⁴","5":"⁵","6":"⁶","7":"⁷","8":"⁸","9":"⁹"}
    return "+".join([str(self.coefficients[i])+"X"+"".join(expo[j] for j in str(self.degre()-i)) for i in range(len(self)) if self.coefficients[i]!=Polynome.corps(0)])

  def __repr__(self):
    return str(self)

  def __call__(self,val):
    res=Polynome(tuple())
    if type(val) is type(self):
      va=val
    else:
      va=Polynome(tuple([val]))
    for c in self:
      res*=va
      res+=Polynome(tuple([c]))
    if type(val) is type(self):
      return res
    if res.coefficients:
      return res[0]
    return Polynome.corps(0)
  def __abs__(self):
    return len(self.coefficients)
  def __len__(self):
    return len(self.coefficients)
  def __iter__(self):
    return iter(self.coefficients)
  def iter(self):
    return self.__iter__()
  def __getitem__(self,i):
    return self.coefficients[self.degre()-i]
  def __setitem__(self,i,x):
    coef=list(self.coefficients)
    coef[self.degre()-i]=x
    self.coefficients=tuple(coef)
  def coefficientdominant(self):
    return self.coefficients[0]
  def degre(self):
    return abs(self)-1
  def __eq__(self,autre):
    return self.coefficients==autre.coefficients#all([x==y for (x,y) in zip(self,autre)])
  def __add__(self,autre):
    somme=[Polynome.corps(0)]*(max(len(self),len(autre))-len(self))+list(self.coefficients)
    for i in range(len(autre)):
      somme[-i-1]+=autre[i]
    return Polynome(tuple(somme))
  def __xor__(self,autre):
    return self+autre
  def __neg__(self):
    return Polynome(tuple((-a for a in self)))
  def __sub__(self,autre):
    return self+(-autre)
  def __mul__(self,autre):
    if self.estzero() or autre.estzero():
      return Polynome(tuple())
    prod=[Polynome.corps(0) for _ in range(len(self)+len(autre)-1)]
    for i in range(len(self)):
      for j in range(len(autre)):
        prod[-i-j-1]+=autre[j]*self[i]
    return Polynome(tuple(prod))
  def __pow__(self,exp):
    if exp>0:
      prod=Polynome(tuple([Polynome.corps(1)]))
      x=Polynome(self.coefficients)
      while exp>1:
        if exp%2:
          prod*=x
        x*=x
        exp//=2
      return prod*x
    elif exp==0:
      return Polynome(tuple([Polynome.corps(1)]))

  def __divmod__(self,diviseur):
    quotient,reste=Polynome(tuple()),self
    degdiviseur=diviseur.degre()
    coefdom=diviseur.coefficientdominant()
    while reste.degre()>=degdiviseur:
      monomediviseur=Polynome(tuple([reste.coefficientdominant()/coefdom]+[Polynome.corps(0)]*(reste.degre()-degdiviseur)))#)+zeros)
      quotient+=monomediviseur
      reste-=monomediviseur*diviseur
#      print(":",quotient,reste)
    return quotient,reste

  def __floordiv__(self,div):
    q,_=divmod(self,div)
    return q
  def __mod__(self,div):
    _,r=divmod(self,div)
    return r

  def bezoutpoly(self,p2):
    r,u,v,rr,uu,vv=p2,Polynome.construction([1]),Polynome.construction([0]),self,Polynome.construction([0]),Polynome.construction([1])
    while not rr.estzero():
#    while rr.degre()>=len(p2)/2:
      q=r//rr
      r,u,v,rr,uu,vv=rr,uu,vv,r-q*rr,u-q*uu,v-q*vv
    return v,u,r

  def der(self):
#    l=self.degre()
    derive=[Polynome.corps(0) for _ in self]
    for i in range(len(self)):
      if i%2==1:
        derive[-i-1]=self[i]
#        print(i,self[i])
#    print(derive)
    return Polynome(tuple(derive[:-1]))

Polynome.corps=F256
Polynome.__name__="(%s)[x]"%F256.__name__
Polynome.construction=lambda L: Polynome(tuple(F256(x) for x in L))

def message2poly(message):
  poly=[]
#  print(len(message))
  for i in range(len(message)//8):
    poly.append(F256(bin2dec(message[8*i:8*i+8])))
#  print(poly)
  return Polynome(tuple(poly))

def poly2message(poly):
  mess=poly.coefficients
  liste=[]
  for c in mess:
    b=[int(i) for i in bin(c.val)[2:]]
    liste=liste+[0]*(8-len(b))+b
  return liste

#def bezoutpoly(p1,p2):
#  r,u,v,rr,uu,vv=p2,Polynome.construction([1]),Polynome.construction([0]),p1,Polynome.construction([0]),Polynome.construction([1])
#  while not rr.estzero():
#    q=r//rr
#    r,u,v,rr,uu,vv=rr,uu,vv,r-q*rr,u-q*uu,v-q*vv
#  return u,v,r

if __name__=="__main__":
  a=F256(140)
  print(a)
  b=F256("101")
  print(b)
#  b=F256((1,0,1))
#  print(b)
  print(a.log())
  print(b+a)
  print(a*a*a*a*a*a)
  print(a**6)
#  print([F256(i) for i in F256.exp[:15]])
  erreurs=[]
  for i in range(256):
    if F256.log[F256.exp(i)]!=i:
      erreurs.append([i,F256.log[F256.exp(i)]])
  if not erreurs:
    print("log et exp OK.")
  else:
    print(erreurs)
  print(F256.log[128])
  print(Polynome.__name__)
  poly=Polynome.construction
  p=poly((15,1,12))
  q=poly(("11","10110","0"))
  print(p,q)
  print(p+q)
#  print(a*p)
  print(p%q)
  print(divmod(p,q))
  print(p//q*q+p%q)
  print(p^q)
  print(p*p)
  print(p**2)
  print(p(F256(1)))
  print(p(q))
  print(p(q).der())
#  p*=q
#  p=poly([0x12,0x34,0x56,0,0,0,0])
#  q=poly([1,0xf,0x36,0x78,0x40])
#  print(divmod(p,q))
  message="4254c6973657a20474e552f4c696e7578206d6167617a696e65204672616e63652e20f09f98830ec11ec11ec11ec11ec11ec11ec11ec11"
  correction="0b1622eb6e2c152a08d34a2dd8c788"

#  message="40d2754776173206272696c6c69670ec"
#  correction="bc2a90136bafeffd4be0"

  polynome=[]
  for i in range(len(message)//2):
    polynome=polynome+[eval("0x"+message[2*i:2*i+2])]
  polynome=poly(polynome+[0]*(len(correction)//2))
#  print(len(polynome))
#  print(polynome)
  modulo=poly([1])
  for i in range(len(correction)//2):
    modulo*=poly([1,F256.exp(i)])
#  print(modulo)
  reste=polynome%modulo
  ch=""
  for i in reste.coefficients:
    s=str(i)
    ch=ch+"0"*(2-len(s))+s
  print(ch)
  print(correction)
#  print(''.join(str(i) for i in (polynome%modulo).coefficients))
#  for i in range(len(F256.exp)):
#    print(i,bin(F256.exp[i])[2:])
#  for i in range(1,256):
#    print(i,F256.log[i])
#  print(len(F256.exp),len(F256.log))
