import copy
import time
from graph_tool.all import *

#################################
##### Reading Functions ######
#################################


def Edge(uv):
    """uv is a string that have to be spleat in two int"""
    edge=list(uv)
    u=""
    v=""
    i=0
    while edge[i]!=";":
        u=u+edge[i]
        i=i+1
    i=i+1
    while i<len(edge):
        v=v+edge[i]
        i=i+1

    return int(u), int(v)


def List_to_graph(line_tab):
    """At index 0 there is the number of vertices and then all edges. 
    Warning, not all lists have the same length."""

    #Create a graph with the right number of vertices
    n=int(line_tab[0])
    g=Graph(directed=False)
    g.add_vertex(n)
    #Add the right number of edges
    for i in range(1,len(line_tab)):
        u,v=Edge(line_tab[i])
        g.add_edge(u,v)

    return g


def File_to_graphs(file_name):
    """Output the list of graphs read in the file """
    #Dont output the size of the graphs 
    tab=[]
    f=open(file_name,"r")
    for line in f:
        #From all line take the graph and put it in the list
        line_to_list=line.split()
        g=List_to_graph(line_to_list)
        tab.append(g)
    f.close()
    return tab


def Read_Graph(n):
    """n is the order of the graph"""
    #Look if the file exists
    if Look_in_sommaire(n):
        #Generate the name of the falie  
        nb=str(n)
        name="grapheofsize"
        name=name+nb+".txt"
        tab=File_to_graphs(name)
        return tab
    else :
        return None


def Look_in_sommaire(n):
    """Look if the file already exists"""
    f=open("sommaire_graphs.txt")
    text=f.readlines()
    f.close()
    if str(n)+"\n" in text:
        return True 
    else: 
        return False

################################
#### Writting functions ###
################################

def New_file(n):
    #generate new file
    nb=str(n) 
    name="grapheofsize"+nb+".txt"
    f=open(name,"w")
    f.close()
    Add_to_Sommaire(n)


def Graph_to_liste(g,n):
    """Add a graph to a list in the rigth format. 
    n is the order of g """
    t=[]
    t.append(n)
    for v in g.vertices():
        for w in v.out_neighbors():
            if w>v:
                edge=str(w)+";"+str(v)
                t.append(edge)
    return t 

def List_to_File(l,file_name): 
    f=open(file_name,"r")
    text=f.read()
    f.close()
    f=open(file_name,"w")
    f.write(text) 
    graph_line=""
    for i in range (len(l)):
        graph_line=graph_line+str(l[i])+" "
    graph_line=graph_line+"\n"
    f.write(graph_line)
    f.close()


def Graph_in_file(g,n):
    """Add g in the right file"""
    if Look_in_sommaire(n)==False:
        New_file(n)
    t=Graph_to_liste(g,n)
    nb=str(n)
    name="grapheofsize"+nb+".txt"
    List_to_File(t,name)


def Add_to_Sommaire(n):
    """Add files to the list of already created files."""
    if Look_in_sommaire(n)==False:
        f=open("sommaire_graphs.txt")
        text=f.read()
        f.close()
        w=open("sommaire_graphs.txt","w")
        w.write(text) 
        w.write(str(n)+"\n")
        w.close()
