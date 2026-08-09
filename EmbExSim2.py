import numpy as np
from EncDec import *
from MultisetEmbedder import MultisetEmbedder
from vertex_map_generator import *

from itertools import permutations

from typing import Any

from copy import deepcopy

import time

class EmbExSim2(MultisetEmbedder):

    def __init__(self, n, k, v_map=None):
        self.n = n
        self.k = k
        self.vertex_map = v_map if v_map else vertex_map(self.n, self.k)
        
    def polar(self, mlc: MonoLinComb) -> np.ndarray:
        value = np.zeros(2*self.n*self.k-self.k)
        
        vertex = np.array(mlc.basis_vec)
        
        index, order, full = self.vertex_map.find(vertex) 

        assert order != -1
        
        theta = order*2*np.pi/full

        value[self.k+2*index] = mlc.coeff*np.cos(theta)
        value[self.k+2*index+1] = mlc.coeff*np.sin(theta)

        return value  

    def size_from_n_k_generic(self, n, k):
        return 2*n*k-k

    def embed_kOne(self, data: np.ndarray, debug = False) -> (np.ndarray, Any):
        return np.sort(data)
                

    def embed_generic(self, data: np.ndarray, debug=False) -> (np.ndarray, Any):

        metadata = None
        
        embedding = np.zeros(2*self.n*self.k-self.k)
        
        assert MultisetEmbedder.is_generic_data(data) # Precondition
        if debug:
            print(f"data is {data}")
    
        n,k = data.shape
        assert self.n == n and self.k == k
        
        lin_comb, offsets = simplex_2_preprocess_steps(data, preserve_scale_in_step_2=False, canonicalise = True)
        i = 0
        for mlc in offsets.mlcs():
            embedding[i] = mlc.coeff
            i += 1
        for mlc in lin_comb.mlcs():
            embedding += self.polar(mlc)

        return embedding, metadata

    def extract(self, data: np.ndarray, debug=False) -> LinComb:

        n = self.n
        k = self.k
        ans = np.zeros(shape = (n,k))
        for i in range(n):
            ans[i] += data[:k]
        data = data[k:]
        
        deltas, ejis = self.extract_data(data)
        raw_lin_comb = zip(deltas, ejis)
        lin_comb = self.fix_lin_comb(raw_lin_comb)
        for i in range(len(lin_comb)):
            ans += lin_comb[i][0]*lin_comb[i][1]
        return array_to_lin_comb(ans)

        

    def fix_lin_comb(self, unfixed_lin_comb):
        lin_comb = sorted(unfixed_lin_comb, key = lambda x: sum(x[1].flatten()))
        for i in range(len(lin_comb)):
            lin_comb[i] = list(lin_comb[i])
        n = len(lin_comb[0][1])
        k = len(lin_comb[0][1][0])
        new_lin_comb = []
        indices =[]
        for i in range(0, (n-1)*k):
            if lin_comb[i][0] != 0:
                new_lin_comb.append(lin_comb[i])
                indices.append(i)
        for i in range(1, len(new_lin_comb)):
            benchmark = new_lin_comb[i-1][1]
            fixed_array = np.zeros(shape=(n, k))
            perms = list(permutations(new_lin_comb[i][1]))
            arrays = [np.stack(p).astype(np.int16) for p in perms]
            diffs = [np.linalg.norm(array-benchmark) for array in arrays]
            min_diff = diffs.index(min(diffs))
            fixed_array = arrays[min_diff]
            new_lin_comb[i][1] = fixed_array
            #the command below normalises the lin_comb - this is needed if in the embedder preserve_scale_in_step_2 is set to True
            #new_lin_comb[i][0] /= (indices[i]+1)
        
        return new_lin_comb    

    def extract_data(self, data):
        n = self.n
        k = self.k
        deltas = []
        ejis= []
        for i in range((n-1)*k):
            deltas.append(np.hypot(data[2*i], data[2*i+1]))
            temp = self.vertex_map.map[i]
            full = len(temp)
            order = int(np.round((np.arctan2(data[2*i+1], data[2*i]))*full/2/np.pi))
            if order < 0:
                order += full
            ejis.append(temp[order])
        return deltas, ejis


if __name__ == "__main__":
    some_input = np.asarray([[1,2,4], [4,3,5], [2,8,3], [9,7,1]])
    n = len(some_input)
    k = len(some_input[0])
    embedder = EmbExSim2(n, k)
    output = embedder.embed(some_input, debug = True)

    print("Embedding:")
    print(f"{some_input}")
    print("leads to:")
    print(f"{output[0]}")

    decoded_input = embedder.extract(output[0])
    print(f"Decoded: {decoded_input.to_numpy_array()}")

    
        
        
        
        

    

        

