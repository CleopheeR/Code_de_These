import copy
import time
from graph_tool.all import *
from Gestion_Fichiers import *


def FreeC4O4(g,v1):
    """Return true if v1 is not in a C4 or a 4K1"""
    for v2 in v1.out_neighbors():
        if v2!=v1:
            for v3 in v1.out_neighbors():
                if v3!=v1 and v3!=v2 and not(v3 in v2.out_neighbors()):
                    for v4 in v2.out_neighbors() :
                        if v4!=v1 and v4!=v2 and v4!=v3 and v4 in v3.out_neighbors() and not(v4 in v1.out_neighbors()):
                            return False
    for v2 in g.vertices():
        if not (v2 in v1.out_neighbors()) and v2!=v1:
            for v3 in g.vertices():
                if v3!=v1 and v3!=v2 and not(v3 in v1.out_neighbors())  and not(v3 in v2.out_neighbors()):
                    for v4 in g.vertices():
                        if v4!=v1 and v4!=v2 and v4!=v3 and not(v4 in v1.out_neighbors()) and not(v4 in v2.out_neighbors()) and (not v4 in v3.out_neighbors()):
                            return False                                                                                                          
    return True


def HaveTwin(g,v):
    """ v in g, return true iif v has a twin in g """
    for w in v.out_neighbors():
        #look if v and w are twin
        twin=True
        for x in w.out_neighbors():
            # see if N(v) subset of N(w)
            if x!=v and not(x in v.out_neighbors()):
                twin=False
                break 
        if twin : 
            for x in v.out_neighbors():
                # see if N(w) subset of N(v)
                if x!=w and not(x in w.out_neighbors()):
                    twin=False 
                    break 
        if twin:
            return True 
            #as soon I find a twin I stop
    return False 


def subset_nonord_k(k, n):
    """Return all non ordered subset of size k with integer from 1 to n"""
    L=[]
    k=int(k)
    n=int(n)
    sublist=list(range(1,k+1))
    i=k-1
    end=1
    if k!=0 and k<=n:
        while end!=0:
            i=k-1
            #Last sub list
            ToAdd=copy.copy(sublist)
            L.append(ToAdd)
            while sublist[i]==n-k+i+1 and i!=-1:
                i=i-1
            if i==-1:
                end=0
            else:
                sublist[i]=sublist[i]+1
                for z in range(i+1,k):
                    sublist[z]=sublist[z-1]+1
    return L


def Attach_with_m_edges(g,m):
    """ Test if we can add a vertex v of degree m to g.
    If the resulting graph is not in Free(C4;O4) or if v has a twin of i
    v is complete return True"""
    if m==0:
        G=copy.copy(g)
        v=G.add_vertex()
        if FreeC4O4(G,v)==True :
            if HaveTwin(G,v)==False:
                return False
        return True 
    else:
        #Take the order of g
        n=0
        for v in g.vertices(): 
            n=n+1
        #For all ordered set of m integer from 1 to n  P
        LP=subset_nonord_k(m,n)
        for P in LP :
            G=copy.copy(g)
            v=G.add_vertex()
            #Add all edges from v to the vertices corresponding to the indec of P
            for i in P :
                w = G.vertex(i-1)
                G.add_edge(v,w)
            #Test G 
            if FreeC4O4(G,v)==True :
                if HaveTwin(G,v)==False:
                    for w in g.vertices():
                        if not(w in v.out_neighbors()):
                            return False
        return True 


def Is_Fixer(g):
    """test if every graph containing g is a fixer of g"""
    #Take the order of g
    n=0
    for v in g.vertices():
        n=n+1
    #test for all possible degree 
    k=0
    G=copy.copy(g)
    while k<n+1:
        if Attach_with_m_edges(G,k)== False:
            return False
        k=k+1
    return True 


def Is_Fixer_without_generate(n):
    """Take all graphs from the files, teste them and remove them"""
    if Look_in_sommaire(n):
            L=Read_Graph(n)
    else :
            L=All_Graphs_By_File(n)
    LFinal=[]
    print( len(L), "graphs have to be tested")

    while len(L)!=0:
        if len(L)%100==0:
            print( len(L),"still have to be tested")
        Gtested=copy.copy(L[0])
        if Is_Fixer(L[0]):
            LFinal.append(Gtested)
        del L[0]
        
    return LFinal


###########################
# FONCTIONS FOR GENERATING #
###########################

def ListDegree(g):
    """Return a tupple of all degree in g in increasing order"""
    List=[]
    for v in g.vertices():
        List.append(v.out_degree())
    List=sorted(List)
    return tuple(List)


def All_Graphs(n):
    """Return the list of all graph of order n in Free(C4,4K1)"""
    L=[]
    #Start with graphs of order n-1
    if n==1:
        g=Graph(directed=False)
        g.add_vertex()
        L.append(g)
    elif n==2:
        NonAdjacent=Graph(directed=False)
        v1=NonAdjacent.add_vertex()
        v2=NonAdjacent.add_vertex()
        L.append(NonAdjacent)
        Adjacent=Graph(directed=False)
        v1A=Adjacent.add_vertex()
        v2A=Adjacent.add_vertex()
        Adjacent.add_edge(v2A,v1A)
        L.append(Adjacent)      
    else  : 
        lminusone=All_Graphs(n-1)
        print("I generate all graphs of order ", n-1)
        L=[]
        Dic = {}
        #Generate all ordered subset of integer from 1 to n of size m P, there are the vertex to attach
        LP=[]
        for m in range(1,n):
            LP=LP+subset_nonord_k(m,n-1)
        print("I have to add a vertex to ", len(lminusone), 'graphs')
        for i in range(len(lminusone)):
            if i%10==0:
                print("We are on the ",i+1,"th graph under", len(lminusone), "graphs")
            g=copy.copy(lminusone[i])
            #First without aditional edges
            GNotConnected=copy.copy(g)
            q=GNotConnected.add_vertex()
            if FreeC4O4(GNotConnected,q)==True:
                Dic[ListDegree(GNotConnected)]=[GNotConnected]
            #Attach the vertices
            for P in LP :
                G=copy.copy(g)
                v=G.add_vertex()
                #Add all edges between v and the vertex corresponding to index in P
                for i in P :
                    w = G.vertex(i-1)
                    G.add_edge(v,w)
                #Test if g in Free(C4,4K1) and isomorph to one already created
                if FreeC4O4(G,v)==True:
                    LD=ListDegree(G)
                    IsInDic=False
                    #If the key exists, look for isomorphism 
                    if (LD in Dic)==True:
                        ToCheck=Dic.get(LDG)
                        for g2 in ToCheck:
                             if graph_tool.topology.isomorphism(G,g2)==True:
                                IsInDic=True
                                break
                        if IsInDic==False:
                            Dic[LD].append(G)
                    #Otherwise create the key 
                    else: 
                        Dic[LD]=[G]
        #Create final list
        for key in Dic:
            L=L+Dic.get(key)
    return L  


def All_Graphs_By_File(n):
    """Return a liste of graph of order n in Free(C4,4K1)"""
    #Look if graphs of order n-1 are already created 
    L=[]
    if n==1:
        g=Graph(directed=False)
        g.add_vertex()
        L.append(g) 
    elif n==2:
        NonAdjacent=Graph(directed=False)
        v1=NonAdjacent.add_vertex()
        v2=NonAdjacent.add_vertex()
        L.append(NonAdjacent)
        Adjacent=Graph(directed=False)
        v1A=Adjacent.add_vertex()
        v2A=Adjacent.add_vertex()
        Adjacent.add_edge(v2A,v1A)
        L.append(Adjacent)     
    else  : 
        if Look_in_sommaire(n-1):
            lminusone=Read_Graph(n-1)
        else :
            lminusone=All_Graphs(n-1)
        print("I generate all graphs of order", n-1)
        L=[]
        Dic = {}
        #Generate all ordered subset of integer from 1 to n of size m P, there are the vertex to attach 
        LP=[]
        for m in range(1,n):
            LP=LP+subset_nonord_k(m,n-1)
        print("I need to add a vertex to ", len(lminusone), 'graphs')
        for i in range(len(lminusone)):
            if i%10==0:
                print("We are on the ",i+1,"th graph under", len(lminusone), "graphs")
            g=copy.copy(lminusone[i])
            GNotConnected=copy.copy(g)
            q=GNotConnected.add_vertex()
            if FreeC4O4(GNotConnected,q)==True:
                Dic[ListDegree(GNotConnected)]=[GNotConnected]         
            for P in LP :
                G=copy.copy(g)
                v=G.add_vertex()
                #Add all edges between v and the vertex corresponding to index in P
                for i in P :
                    w = G.vertex(i-1)
                    G.add_edge(v,w)
                #Test if g in Free(C4,4K1) and isomorph to one already created
                if FreeC4O4(G,v)==True:
                    LD=ListDegree(G)
                    IsInDic=False
                    #If the key exists, look for isomorphism
                    if (LD in Dic)==True:
                        ToCheck=Dic.get(LD)
                        for g2 in ToCheck:
                             if graph_tool.topology.isomorphism(G,g2)==True:
                                IsInDic=True
                                break
                        if IsInDic==False:
                            Dic[LD].append(G)
                    #Otherwise create the key 
                    else: 
                        Dic[LD]=[G]
        #Create final list
        for key in Dic:
            L=L+Dic.get(key)
    #Put all in a file 
    for i in range(len(L)):
        Graph_in_file(L[i],n)
    return L  




def main():
    n=int(input("Enter the number of vertices :"))
    GenerOrTest=input("Do you want to generate graphs (G) or to test graphs(T) :")
    if GenerOrTest == "G":
        L=All_Graphs_By_File(n)
        print("There are ",len (L)," graphs de of order ",n)
        SeeGraph=input("Do you want to see them ? (Y or N)")
        if SeeGraph=="Y" : 
            for i in range(len(L)) :
                print(L[i])
                for e in L[i].edges():
                    print(e) 
    else : 
        L=Is_Fixer_without_generate(n)
        if len(L)==0:
            print("No fixer")
        else:
            for i in range(len(L)):
                print(L[i])
                for e in L[i].edges():
                    print(e)


if __name__=="__main__":
    main()
