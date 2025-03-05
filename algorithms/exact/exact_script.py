
import os
import sys

import gurobipy as gp
from gurobipy import GRB

import re

sys.path.append(os.path.abspath("../../util"))
from data_utils import *
from plot_utils import *


file, data = read_data_from_file("../../data/BicyclesRelocationData.xlsx")


# Decision Vars
categories = list(data.columns)

s = {cat: int(data.loc[0, cat]) for cat in categories} # surplus
c = {cat: float(data.loc[1, cat]) for cat in categories} # space

# Capacity
T = 80 

sheets       = [sheet for sheet in file.sheet_names if sheet.startswith("ExpectedProfitsArea")]
destinations = [] 
profit_dict  = {}    


for sheet in sheets:
    area_idx = re.search(r"ExpectedProfitsArea(\d+)", sheet)
    if area_idx:
        area = f"Area{area_idx.group(1)}"
        destinations.append(area)
        profits_data = pd.read_excel(file, sheet_name=sheet, header=0)
        for cat in categories:
            profits = profits_data[cat].dropna().tolist()
            profit_dict[(cat, area)] = profits


def get_profits(i, j, s_i):
    """ fill missing elements with zeros
    Args:
        i ([type]): categories
        j ([type]): destination areas
        s_i ([type]): surplus

    Returns:
        [type]: This function ensures that for every (i,j) the list of profits has exactly s[i] elements. 
    """
    profits = profit_dict.get((i, j), [])
    if len(profits) < s_i:
        profits = profits + [0]*(s_i - len(profits))
        
    return profits


model = gp.Model("bicycles_relocation_opt")
model.setParam("OutputFlag", 0)  # Turns off the log

# Variável binária y[i,j,k] para indicar se a k-ésima bicicleta da categoria i é alocada para a área j.
y = {}

for i in categories:
    for j in destinations:
        for k in range(1, s[i] + 1):
            y[i, j, k] = model.addVar(vtype=GRB.BINARY, name=f"y_{i}_{j}_{k}")

model.update()

# Constraint 1: Sequência dos lucros
for i in categories:
    for j in destinations:
        for k in range(2, s[i] + 1):
            model.addConstr(y[i, j, k] <= y[i, j, k - 1], name=f"seq_{i}_{j}_{k}")

# Constraint 2: Excedente disponível por categoria
for i in categories:
    model.addConstr(
        gp.quicksum(y[i, j, k] for j in destinations for k in range(1, s[i] + 1)) <= s[i],
        name=f"surplus_{i}"
    )

# Constaint 3: Capacidade do caminhão
model.addConstr(
    gp.quicksum(c[i] * y[i, j, k] for i in categories for j in destinations for k in range(1, s[i] + 1)) <= T,
    name="capacity"
)

model.setObjective(
    gp.quicksum(
        get_profits(i, j, s[i])[k - 1] * y[i, j, k]
        for i in categories for j in destinations for k in range(1, s[i] + 1)
    ),
    GRB.MAXIMIZE
)

model.optimize()

model.write("../../models/bike_relocation.lp")  

# %%
if model.status == GRB.OPTIMAL:
    print("=========================")
    print("Optimal Solution Found:")
    print("=========================")
    for i in categories:
        for j in destinations:
            settled = sum(y[i, j, k].x for k in range(1, s[i] + 1))
            print(f"{i} -> {j}: {settled} bicycle")
    print("-----------------------------")
    print(f"Total profit: {model.objVal}")
else:
    print("Optimal solution not found.")


capacities = list(range(100, 4001, 100))
results = []

best_capacity = None
best_objVal = -float("inf")
best_solution_values = None

for T in capacities:

    model = gp.Model("bicycles_relocation_opt")
    model.setParam('OutputFlag', 0) 

    y = {}

    for i in categories:
        for j in destinations:
            for k in range(1, s[i] + 1):
                y[i, j, k] = model.addVar(vtype=GRB.BINARY, name=f"y_{i}_{j}_{k}")

    model.update()

    for i in categories:
        for j in destinations:
            for k in range(2, s[i] + 1):
                model.addConstr(y[i, j, k] <= y[i, j, k - 1], name=f"seq_{i}_{j}_{k}")

    for i in categories:
        model.addConstr(
            gp.quicksum(y[i, j, k] for j in destinations for k in range(1, s[i] + 1)) <= s[i],
            name=f"excedente_{i}"
        )

    model.addConstr(
        gp.quicksum(c[i] * y[i, j, k] for i in categories for j in destinations for k in range(1, s[i] + 1)) <= T,
        name="capacidade"
    )

    model.setObjective(
        gp.quicksum(
            get_profits(i, j, s[i])[k - 1] * y[i, j, k]
            for i in categories for j in destinations for k in range(1, s[i] + 1)
        ),
        GRB.MAXIMIZE
    )

    model.optimize()

    if model.status == GRB.OPTIMAL:
        objVal = model.objVal
        results.append((T, model.objVal))
        print(f"Capacity {T}: Optimal objective = {model.objVal}")

        if objVal > best_objVal:
            best_objVal = objVal
            best_capacity = T
            best_solution_values = {var.varName: var.x for var in model.getVars()}
    else:
        results.append((T, None))
        print(f"Capacity {T}: No optimal solution found.")

print()
print("-----------------------------")
print("Best Capacity:", best_capacity)
print("Best Profit (Total Profit):", best_objVal)


if best_solution_values is not None:
    print("Best solution (allocations by (Category, Destination)):")
    for i in categories:
        for j in destinations:
            allocated = sum(best_solution_values.get(f"y_{i}_{j}_{k}", 0) for k in range(1, s[i] + 1))
            print(f"{i} -> {j}: {allocated} bicycle")

print()
print(f"Best solution raw fitness (profit minus penalty): {best_objVal}")


plot_optimal_profit(results)

plot_interative_optimal_profit(results)
