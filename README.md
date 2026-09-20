# 📍 GridPoint

### Warehouse Location Optimization Platform

GridPoint is a warehouse location optimization platform that uses **geographic location and neighborhood order demand** to identify warehouse locations that minimize order-weighted delivery distance.

## 🚀 Problem Statement

E-commerce companies serve multiple neighborhoods with different order volumes and geographic locations. Choosing warehouse locations manually can result in inefficient delivery routes and increased delivery distance.

GridPoint addresses this problem by analyzing neighborhood locations and daily order demand to determine suitable warehouse locations and assign neighborhoods to the nearest optimized warehouse.

## 💡 Solution

GridPoint:

1. Accepts neighborhood names, geographic coordinates, and daily order demand.
2. Accepts the number and locations of existing warehouses.
3. Calculates distances using the **Haversine formula**.
4. Assigns each neighborhood to its nearest warehouse.
5. Calculates the current order-weighted delivery distance.
6. Evaluates possible warehouse combinations based on neighborhood locations.
7. Selects the warehouse combination with the minimum order-weighted delivery distance.
8. Reassigns neighborhoods to the optimized warehouses.
9. Compares the current and optimized delivery distances.
10. Displays the optimized locations and assignments on a map.

## ✨ Features

* 📍 Neighborhood location input
* 📦 Daily order demand input
* 🏭 Multiple warehouse support
* 📏 Geographic distance calculation
* 🎯 Demand-weighted warehouse optimization
* 🔗 Neighborhood-to-warehouse assignment
* 📊 Current vs optimized delivery distance comparison
* 🗺️ Interactive map visualization
* 📈 Percentage reduction in weighted delivery distance

## 🧠 Optimization Approach

GridPoint uses a **discrete warehouse location optimization approach**.

Neighborhood locations are treated as candidate warehouse locations. For a selected number of warehouses, GridPoint evaluates possible combinations of candidate locations.

For each combination, the algorithm:

* Calculates the distance from every neighborhood to each selected warehouse.
* Assigns each neighborhood to its nearest warehouse.
* Multiplies the nearest distance by that neighborhood's daily order demand.
* Sums these values to obtain the total order-weighted delivery distance.

The combination with the lowest total value is selected as the optimized warehouse configuration.

### Objective

The optimization m
