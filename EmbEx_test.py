from EmbExSim2 import *
import numpy as np
from copy import deepcopy
from tools import sort_np_array_rows_lexicographically as canon

class UI():

    def __init__(self, n ,k):
        self.n = n
        self.k = k
        self.codec = EmbExSim2(n,k)

    def menu(self):
        input_dict = {1: (self.specific_array, "specific array"), 2: (self.random_arrays, "random arrays")}
        last = max(list(input_dict.keys()))
        close = False
        while not close:
            print(f"Codec for n={self.n}, k={self.k}")
            print("0: Exit")
            for key in input_dict.keys():
                print(f"{key}: Test {input_dict[key][1]}")
            request = input("Enter mode: ")
            valid_input = False
            mode = None
            while not valid_input:
                try:
                    mode = int(request)
                    assert mode >= 0 and mode <= last
                    valid_input = True
                except:
                    print(f"Invalid mode. Mode must be an integer between 0 and {last}")
                    request = input("Enter mode: ")
            if mode == 0:
                close = True
            else:
                input_dict[mode][0]()

    def run_codec(self, data, output=False):
        encoded, dim, meta = self.codec.embed(data)
        decoded = self.codec.extract(encoded).to_numpy_array()

        error = np.linalg.norm(canon(data)-canon(decoded))

        if output:
            print("Embedding:")
            print(f"{data}")
            print("leads to:")
            print(f"{output}")
            print("Decoded:")
            print(f"{decoded}")

        return error, encoded, decoded
        
    def specific_array(self):
        print("Input array in form [[a,b,c...],[..],[..]]:")
        array = np.zeros(shape=(self.n, self.k))
        array_str = list(input())
        valid = False
        while not valid:
            try:
                assert array_str.pop(0) == '['
                assert array_str.pop() == ']'
                for i in range(n):
                    assert array_str.pop(0) == '['
                
                    for j in range(k):
                        delim = ']' if j == k-1 else ','
                        end = array_str.index(delim)
                        array[i,j] = int(''.join(array_str[0:end]))
                        array_str = array_str[end+1:]
                    
                    if i==n-1:
                        assert not array_str
                    else: 
                        assert array_str.pop(0) == ','
                valid = True

            except AssertionError:
                print("Invalid format - missing delimiter or array too large")
                print("Input array in form [[a,b,c...],[..],[..]]:")
                array_str = input()
                
            #except ValueError:
                #print("Invalid format - number could not be parsed to array")
                #print("Input array in form [[a,b,c...],[..],[..]]:")
                #array_str = input()

        self.run_codec(array, output=True)            

    def random_arrays(self):
        low_bound = float(input("Min value of array elements: "))
        high_bound = float(input("Max value of array elements: "))
        num = int(input("Number of arrays: "))

        rng=np.random.default_rng()

        arrays = [((high_bound-low_bound)*rng.random(size=(self.n, self.k))+low_bound) for i in range(num)]
        results = [(data, self.run_codec(data)) for data in arrays]

        errors = [res[1][0] for res in results]

        max_i = errors.index(max(errors))
        min_i = errors.index(min(errors))
        avr_error = sum(errors)/num

        print("Average error: ", avr_error)
        print("Smallest error: ", errors[min_i])
        print("Data :", results[min_i][0])
        print("Decoded: ", results[min_i][1][2])
        print("Largest error: ", errors[max_i])
        print("Data :", results[max_i][0])
        print("Decoded: ", results[max_i][1][2])
        print("\n ===== \n")

        if input("Print all error data? (y/n): ") == 'y':
            for result in results:
                print("Error: ", result[1][0], "\nData:\n", result[0], "\n")

        print("\n ===== \n")
        

if __name__ == "__main__":
    n = int(input("n: "))
    k = int(input("k: "))
    ui = UI(n,k)
    ui.menu()

        

        
            
        
        
                    
        