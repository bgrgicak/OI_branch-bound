from __future__ import division
from drvo import *
from simplex_lib import *
nep=None
njed=None
def search(tree,z0,val):
	try:
		for a in tree.getNodeValue():
			if(a==val):
				return True
	except:
		pass
	try:
		if(tree.left.getNodeValue()<>'halt' and not isinstance(racunajZ(racunaj(z0,tree.left.getNodeValue())),int)):
			search(tree.left,z0,val)		
		if(tree.right.getNodeValue()<>'halt' and not isinstance(racunajZ(racunaj(z0,tree.right.getNodeValue())),int)):
			search(tree.right,z0,val)
	except:
		pass
def racunaj(z,x):
	b=Tableau(z)
	for xi in x:
		b.add_constraint(xi[0],xi[1])
	b.solve()
	return b.Dmatrix[len(b.Dmatrix)-1]
def racunajX(t,z0,rez):
	x=[]
	for i in range(1,(nep+1)):
		for red in rez:	
			if red.item(i)==1:
				x.append(round(red.item(red.shape[1]-1),3))
	con=x[0]
	conInd=0
	for i in range(1,nep):
		if(not isinstance(x[i],int) and fabs(0.5-round(modf(x[i])[0],3))<fabs(0.5-round(modf(con)[0],3))):
			con=x[i]
			conInd=i
	pom1=[]
	pom2=[]
	for i in range(0,nep):
		if i<>conInd:
			pom1.append(0)
			pom2.append(0)
		else:
			pom1.append(1)
			pom2.append(-1)
	pom1i=[pom1[1],pom1[0]]
	pom2i=[pom2[1],pom2[0]]
	if(search(t,z0,[pom1,modf(con)[1]])<>None or search(t,z0,[pom1i,modf(con)[1]])<>None):
		pom1='halt'
	elif (search(t,z0,[pom2,-(modf(con)[1]+1)])<>None or search(t,z0,[pom2i,-(modf(con)[1]+1)])<>None):
		pom2='halt'	
	return [pom1,modf(con)[1],pom2,-(modf(con)[1]+1)]
def racunajZ(rez):
	return rez[rez.shape[0]-1].item(rez.shape[1]-1)
def getPrev(tree,node):
	if(tree.left<>None):
		if(tree.left.getNodeValue==node.getNodeValue):
			return tree
		else:
			getPrev(tree.left,node)
	if(tree.right<>None):
		if(tree.right.getNodeValue==node.getNodeValue):
			return tree
		else:
			getPrev(tree.right,node)
def kraj(z0,root,node):
	if(node.getNodeValue is not root.getNodeValue):
		if(getPrev(root,node).left is not None and getPrev(root,node).right is not None):
			kraj(z0,root,getPrev(root,node))
		elif(getPrev(root,node).left is None):
			Xu=racunajX(root,z0,racunaj(z0,getPrev(root,node).left.getNodeValue()))
			getPrev(root,node).left.insertLeft(x0+[[Xu[0],Xu[1]]])
			getPrev(root,node).left.insertRight(x0+[[Xu[2],Xu[3]]])
			return getPrev(root,node)
		elif(getPrev(root,node).right is None):
			Xu=racunajX(root,z0,racunaj(z0,getPrev(root,node).right.getNodeValue()))
			getPrev(root,node).right.insertLeft(x0+[[Xu[0],Xu[1]]])
			getPrev(root,node).right.insertRight(x0+[[Xu[2],Xu[3]]])
			return getPrev(root,node)
	else:
		return True
		
if __name__=='__main__':
	z0=[-3,-4]#z=3x1+4x2->max
	x0=[[[2,1],6],[[2,3],9]]#2x1+x2=6, 2x1+3x2=9
	nep=len(z0)
	njed=len(x0)
	n=nep+njed+1
	t=BinaryTree(x0)
	rez=racunaj(z0,t.getNodeValue())
	Xu=racunajX(t,z0,rez)
	t.insertLeft(x0+[[Xu[0],Xu[1]]])
	t.insertRight(x0+[[Xu[2],Xu[3]]])
	tL=t.left
	tR=t.right
	tPrev=t
	while 1==1:
		rezL=racunaj(z0,tL.getNodeValue())
		rezR=racunaj(z0,tR.getNodeValue())
		ZL=racunajZ(rezL)
		ZR=racunajZ(rezR)
		if(modf(ZR)[0]==0 and modf(ZL)[0]==0):
			if(ZR>=ZL): 
				tPrev=tR
				print 'gotovo',ZR
				break
			else:
				tPrev=tL
				print 'gotovo',ZL
				break
		elif (modf(ZR)[0]==0): 
			tPrev=tR
			print 'gotovo',ZR
			break
		elif (modf(ZL)[0]==0):
			tPrev=tL
			print 'gotovo',ZL
			break
		else:
			Xu=racunajX(tPrev,z0,rezR)
			if((ZR>=ZL or Xu[0] is 'halt') and Xu[2]<>'halt'):
				print 'R',tR.getNodeValue()
				tR.insertLeft(tR.getNodeValue()+[[Xu[0],Xu[1]]])
				tR.insertRight(tR.getNodeValue()+[[Xu[2],Xu[3]]])
				tPrev=tR
				tL=tR.left
				tR=tR.right
				print ('ZR',ZR)
			elif Xu[0]<>'halt':
				Xu=racunajX(tPrev,z0,rezL)
				print 'L',tL.getNodeValue()
				tL.insertLeft(tL.getNodeValue()+[[Xu[0],Xu[1]]])
				tL.insertRight(tL.getNodeValue()+[[Xu[2],Xu[3]]])
				tPrev=tL
				tR=tL.right
				tL=tL.left
				print ('ZL',ZL)
			else:
				print 'gotovo',racunajZ(racunaj(tPrev))
				break
	print racunaj(z0,tPrev.getNodeValue())
