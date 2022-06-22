#!/usr/bin/env python
# coding: utf-8

# In[48]:


import random


# In[115]:


class Route(list):
    route_number = 0
    def __init__(self, step, nodes=[]):
        self.step=step
        self.extend(nodes)
        self.success = False
        Route.route_number+=1
        self.route_number = Route.route_number
    
    def __repr__(self):
        s = "Route Number {}. Step={} ".format(self.route_number, self.step)
        s = s + super(type(self), self).__repr__()
        return s
    
    def __hash__(self):
        return self.route_number


# In[155]:


class Grid(list):
    def __init__(self, n, start, delivery):
        self.start = start
        self.delivery = delivery
        [self.append([0 for _ in range(n)]) for _ in range(n)] #10x10 grid
        self.obstacles = []
        
    
    def __repr__(self):
        s = ""
        for row in self:
#             print(row)
            row_string=[]
            for i in row:
                if i==-1:
                    row_string.append(" ")
                else:
                    row_string.append(str(i))
    
            s = s + " ".join(row_string) + "\n"
        
        return s
    
    

    def addObstacles(self, obstacles):  #i=column index, j = row index
        '''Add each obstacle one by one to grid
        Args:
            obstacles: Array of tuples- the coordinates of each obstacle
                        in the form (i, j) = (column index, row index)
        Returns:
            None
        '''
        for o in obstacles:
            self[o[1]][o[0]] = -1
            self.obstacles.append(o)
    
    def isValidPosition(self, step, x, y):
        '''Checks if moving to this position is viable. The position
        must be within the grid. The position must not be occupied
        by an obstacle. The position bust be a new position that has 
        not previously been visited.
        Args:
            pos (list): The grid co-ordinates being enquired about.
        Returns:
            valid (boolean): True if position is valid, false if not.
        '''
        #Grid positions with 1---obstacle
        #Grid positions with 2---Already visited
        valid = False
        #check if within grid
        if (0<=x<len(self))&(0<=y<len(self)):
            valid = True
            #check if no obstacle/ not already been
            value = self[y][x]
#             print(value)
            if (0<value <= step):
                valid = False
            if (value<0):
                valid=False
        return valid

    
    def move(self, step, all_routes):
        '''Find all most efficient paths to the end
        Args:
            step: step of recursion. corresponds to distance from start
            all_routes: list of all route instances.  
        '''
        bad_routes = []
        for route in (all_routes):
            if route.step>step:
                continue
            x, y = route[-1][0], route[-1][1]
            #try and append all surrounding blocks
            new_nodes = []
            a = [-1, 0, 1]
            curr = route[-1]
            for dx in a:
                for dy in a: 
                    if (self.isValidPosition(step, x+dx, y+dy))&((x+dx, y+dy)!=curr):
                        new_nodes.append((x+dx, y+dy))
                        self[y+dy][x+dx] += 1

            if len(new_nodes)==1:
                route.append(new_nodes[0])
                route.step+=1
            elif len(new_nodes)>1:
                for n in new_nodes[1:]:
                    r = route[:]
                    r.append(n)
                    new_route = Route(step+1, r)
                    
                    all_routes.append(new_route)
                route.append(new_nodes[0])
                route.step+=1
            else:
                bad_routes.append(route)
       
        i=0
        while i<len(all_routes):
            r = all_routes[i]
            if r in bad_routes:
                del all_routes[i]
            else:
                i+=1
        
#         print("\n\n")
        delivery=False
    
        for r in all_routes:
#             print(r)
            if r[-1]==self.delivery:
                delivery=True
                d = r
#         print(self)
#         print("\n\nNext Step\n")
        
        if (delivery==False):
#             if len(all_routes) == 0
            delivery_path = []
            success, delivery_path = self.move(step+1, all_routes)
            
        else:
            success=True
            delivery_path = d
            
        return success, delivery_path
    
    def findPath(self):
        self[start[1]][start[0]]+=1
#         print(self)
        route = Route(step=0, nodes=[self.start])
        all_routes = [route]
        s = self.move(0, all_routes)
        return s
    
    def addRandomObstacles(self, n):
        new_obstacles = 0
        while (new_obstacles)<=n:
            x = random.randint(0,len(self)-1)
            y = random.randint(0, len(self)-1)
            
            if ((x,y) not in self.obstacles) & ((x,y)!=self.start) & ((x,y)!=self.delivery):
                self.addObstacles([(x,y)])
                new_obstacles += 1
        
        pass


# In[156]:


g = Grid(n=10, start=(0,0), delivery=(9,9))

obstacles = [(9,7), (8,7), (6,7), (6,8)]
g.addObstacles(obstacles)

print(g, "\n")

#add 20 more randomly placed obstacles
g.addRandomObstacles(20)
print(g, "\n")
try:
    success, delivery_path=g.findPath()
    if success:
        print("Successful Delivery!!\nSuccessful path: " + str((delivery_path[:])))
except RecursionError:
    print("Delivery Not Possible")
# print(g)


# In[ ]:




