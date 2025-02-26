# 🚲 RentalBike Optimization with Gurobi  

## 📖 Project Overview  
**RentalBike** is a bike-sharing company specializing in short-term bicycle rentals across different city areas. Customers can rent bicycles for any duration and return them to a different location, as long as it is within an operational zone.  

Since bicycles can be returned to locations different from their origin, **RentalBike** must frequently redistribute bikes to balance supply and meet expected demand. This project aims to **optimize the redistribution process** using **Gurobi**, ensuring maximum profitability while efficiently relocating bikes.  

---

## 🎯 **Optimization Problem**  
The objective is to **determine the optimal number of bicycles** to be moved between areas while maximizing **total profit**. The redistribution decision is based on:  
- Expected demand in each area.  
- Surplus or shortage of bikes.  
- Profitability of moving bikes from one area to another.  

The optimization model will help RentalBike make **cost-effective** and **data-driven** decisions for bicycle relocation.  

---

## ⚙️ **Technology Stack**  
This project is implemented using:  
- 🐍 **Python**  
- 📊 **Gurobi Optimizer**  
- 🛠 **Pandas & NumPy** (Data handling)  
- 📈 **Plotly/Matplotlib** (Visualization)  

---

## 🚀 **How to Run the Optimization Model**  
1. **Install Dependencies**  
   ```bash
   pip install gurobipy numpy pandas matplotlib plotly
