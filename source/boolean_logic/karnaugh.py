import matplotlib.pyplot as plt
import numpy as np

class KarnaughMap:
    def __init__(self, boolean_function):
        self.boolean_function = boolean_function
        self.variables = boolean_function.variables
        self.num_vars = len(self.variables)
        if self.num_vars < 2 or self.num_vars > 4:
            raise ValueError("Karnaugh maps are only supported for 2 to 4 variables.")
        self.truth_table = boolean_function.get_truth_table()

    def generate_map(self):
        if self.num_vars == 2:
            return self._generate_map_2vars()
        elif self.num_vars == 3:
            return self._generate_map_3vars()
        elif self.num_vars == 4:
            return self._generate_map_4vars()

    def _generate_map_2vars(self):
        vars_order = self.variables
        mapping = {
            (0,0):0,  
            (0,1):1,  
            (1,0):2,  
            (1,1):3   
        }
        kmap = ['']*4
        for values, result in self.truth_table:
            pos = mapping[values]
            kmap[pos] = str(result)
        kmap = np.array(kmap).reshape((2,2))
        return kmap, vars_order

    def _generate_map_3vars(self):
        vars_order = self.variables
        mapping = {
            (0,0,0):0, (0,0,1):1,
            (0,1,0):2, (0,1,1):3,
            (1,0,0):4, (1,0,1):5,
            (1,1,0):6, (1,1,1):7
        }
        kmap = ['']*8
        for values, result in self.truth_table:
            pos = mapping[values]
            kmap[pos] = str(result)
        kmap = np.array(kmap).reshape((2,4))
        return kmap, vars_order

    def _generate_map_4vars(self):
        vars_order = self.variables
        mapping = {
            (0,0,0,0):0,  (0,0,0,1):1,  (0,0,1,0):2,  (0,0,1,1):3,
            (0,1,0,0):4,  (0,1,0,1):5,  (0,1,1,0):6,  (0,1,1,1):7,
            (1,0,0,0):8,  (1,0,0,1):9,  (1,0,1,0):10, (1,0,1,1):11,
            (1,1,0,0):12, (1,1,0,1):13, (1,1,1,0):14, (1,1,1,1):15
        }
        kmap = ['']*16
        for values, result in self.truth_table:
            pos = mapping[values]
            kmap[pos] = str(result)
        kmap = np.array(kmap).reshape((4,4))
        return kmap, vars_order

    def plot_map(self):
        kmap, vars_order = self.generate_map()
        num_rows, num_cols = kmap.shape

        fig, ax = plt.subplots()
        ax.axis("off")
        ax.axis("tight")

        if self.num_vars == 2:
            row_vars = [f"{vars_order[0]}=0", f"{vars_order[0]}=1"]
            col_vars = [f"{vars_order[1]}=0", f"{vars_order[1]}=1"]
        elif self.num_vars == 3:
            row_vars = [f"{vars_order[0]}=0", f"{vars_order[0]}=1"]
            col_vars = [f"{vars_order[1]}{vars_order[2]}=00", f"{vars_order[1]}{vars_order[2]}=01",
                        f"{vars_order[1]}{vars_order[2]}=10", f"{vars_order[1]}{vars_order[2]}=11"]
        elif self.num_vars == 4:
            row_vars = [f"{vars_order[0]}{vars_order[1]}=00", f"{vars_order[0]}{vars_order[1]}=01",
                        f"{vars_order[0]}{vars_order[1]}=10", f"{vars_order[0]}{vars_order[1]}=11"]
            col_vars = [f"{vars_order[2]}{vars_order[3]}=00", f"{vars_order[2]}{vars_order[3]}=01",
                        f"{vars_order[2]}{vars_order[3]}=10", f"{vars_order[2]}{vars_order[3]}=11"]

        table = plt.table(cellText=kmap,
                          rowLabels=row_vars,
                          colLabels=col_vars,
                          loc="center",
                          cellLoc="center")

        table.scale(1, 2)
        plt.title("Karnaugh map")
        plt.show()