import math

def calculate_distance(a:list[float],b:list[float]):
    distance = math.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)
    return distance
def valid(nodes,node):
    for el in nodes:
        if node == el[0]:
            return 0
    return 1 
def reverse_vector(vector:list):
    path = []
    i = len(vector)-1
    while i > -1:
        path.append(vector[i])
        i=i-1
    return path
def pathfinding(nodes,location,destination):
    
    def calc(x):
        return calculate_distance(x,destination)
    
    destination = repair_destination(nodes, destination)
    closest = nodes[0][0]
    for node in nodes:
        if calculate_distance(closest,location) > calculate_distance(node[0],location):
            closest = node[0]
    open = []
    open.append([closest,location])
    j = 0
    while open[len(open)-1][0] != destination:
        ok = False
        j=len(open)-1
        while ok == False and j > -1:
            element = open[j]
            j=j-1
            for node in nodes:
                if element[0] == node[0] :
                    #modificarea incepe d aci
                    '''
                    vector = nodes[1:]
                    
                    vector.sort(key=calc)
                    for el in vector:
                        if valid(open,el):
                            open.append([el,element[0]])
                            ok = True
                            break
                    '''
                    
                    for el in node[1:]:
                        if valid(open,el):
                            open.append([el,element[0]])
                            ok = True
                            break
                    
                if(ok == True):
                    break
    
    vector =[]
    step = open[len(open)-1]
    while step != open[0]:
        vector.append(step[0])
        for el in open:
            if el[0] == step[1]:
                step = el
    vector.append(open[0][0])

    vector = reverse_vector(vector)
    return vector
def repair_destination(nodes, destination):
    ok = 0
    for el in nodes:
        if destination == el[0]:
            ok = 1
    #if not add it in nodes
    if ok == 0:
        closest = nodes[0][0]
        for node in nodes:
            if calculate_distance(closest,destination) > calculate_distance(node[0],destination):
                closest = node[0]
        destination = closest
    return destination

