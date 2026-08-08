import numpy as np
import time
from copy import deepcopy

class vertex_map():

    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.map = self.generate_vertex_map()
        self.count = [len(a) for a in self.map]

    def index(self, vertex: np.ndarray) -> int:
        return int(sum([max(x) for x in vertex.T])-1)

    def find(self, vertex: np.ndarray) -> (int, int, int):
        index = self.index(vertex)
        full = self.count[index]
        order = next((i for i, x in enumerate(self.map[index]) if np.all(x == vertex)), -1)

        return index, order, full

    def seed(self, i: int,j: int) -> np.ndarray:
        seed = np.zeros(shape=(self.k,self.n-1))
        for a in range(int(j), self.n-1):
            seed[i][a] = a+1
        for b in range(i+1, self.k):
            for a in range(self.n-1):
                seed[b][a] = a+1
        return seed
        

    def generate_vertex_map(self) -> list:
        vertex_map = [[] for _ in range(self.k*(self.n-1))]
    
        todo = [(np.zeros(shape=(self.n,self.k)), self.seed(0,0))]
        done = False
        
        while not done:
            vertex, remainder = todo.pop(0)
            
            for i in range(self.k):
                for j in remainder[i]:
                    if j==0:
                        continue
                        
                    new_vertices = self.increment(vertex, i, j)
                    for new_vertex in new_vertices:
                        vertex_map[self.index(new_vertex)].append(deepcopy(new_vertex))
                        todo.append((new_vertex, self.seed(i,j)))
                
            done = not todo

        return vertex_map

    def increment(self, vertex, k_0, n_count):

        new_eji_counts = deepcopy(vertex)
        
        count = n_count
        for i in range(self.n):
            if new_eji_counts[i, k_0] > 0:
                new_eji_counts[i, k_0]+= 1
                count -= 1
        
        line_to_edit = new_eji_counts[:,k_0]
        unique_indices = []
        for i in reversed(range(self.n)):
            if i == self.n-1 or not np.array_equal(new_eji_counts[i], new_eji_counts[i+1]):
                unique_indices.append(i)
        new_lines = self.binliner(line_to_edit, unique_indices, count)

        vertex_list = []
        for line in new_lines:
            new_eji_counts[:,k_0]=line
            vertex_list.append(deepcopy(new_eji_counts))
        return vertex_list

    def binliner(self, line_to_edit, unique_indices, count):
        new_lines = []
        bin_sizes = []
        for i in range(len(unique_indices)):
            index = unique_indices[i]
            if i == len(unique_indices)-1:
                prev_index = -1
            else:
                prev_index = unique_indices[i+1]
            size = 0
            for j in range(prev_index+1, index+1):
                if line_to_edit[j] == 0:
                    size +=1
            bin_sizes.append(size)
        combos = list(self.find_combinations(count, bin_sizes))
        for combo in combos:
            new_line = deepcopy(line_to_edit)
            for i in range(len(combo)):
                sub_count = combo[i]
                index = unique_indices[i]
                while sub_count > 0:
                    if new_line[index] == 0:
                        new_line[index] += 1
                        sub_count -= 1
                    index -= 1
            new_lines.append(new_line)
        return new_lines


    def find_combinations(self, max_count, max_values):
        combos = []
        todo = [(max_count, 0, [])]
        done = False

        while not done:
            count, index, current = todo.pop(0)
            if index == len(max_values):
                if count == 0: 
                    combos.append(current.copy())
            else:
                start = int(count-sum(max_values[index+1:]))
                end = int(np.round(min(max_values[index], count) + 1))
                for i in range(end):
                    current.append(i)
                    if i >= start: todo.append((count - i, index + 1, current.copy()))
                    current.pop()
            done = not todo

        return combos
                    
if __name__ == "__main__":
    n=int(input("n: "))
    k=int(input("k: "))
    #simplex_map = Simplex_Map(n,k)
    #key1 = simplex_map.vertex_key
    start=time.time()
    vmap = vertex_map(n,k)
    end=time.time()
    dur = end-start
    print(vmap.count)
    print(f"n={n}; k={k}; Runtime: {dur} seconds")                
                
    