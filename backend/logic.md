the logic for server.js

    ```
        const areaRadius = range * 111000  // 0.05 * 111000 = 5550 meters
    ```
    111000: Approximate meters per degree at Earth's latitude

    the maxDistancePerVehicle function :
    * areaRadius/numberOfVehicles: Each vehicle gets a "sector" of the circle
    * deliveriesPerVehicle: Distance needed to visit all deliveries in that sector
    * 2: Buffer factor (return trips, non-optimal paths)

    Math.cos(angle): X-component (East-West offset)
    Math.sin(angle): Y-component (North-South offset)



route_solver.py
    how the vehicle panelty works:
    Example distance matrix (4 locations):
    [[   0, 1500, 2000, 800 ],   # Row sums: 4300
    [1500,    0, 1200, 900 ],   # Row sums: 3600  
    [2000, 1200,    0, 1800],   # Row sums: 5000
    [ 800,  900, 1800,   0 ]]   # Row sums: 3500
    Total sum: 16400
    Average: 16400 / (4²) = 16400 / 16 = 1025 meters
        
    PARALLEL_CHEAPEST_INSERTION:
        Parallel: Considers multiple vehicles simultaneously
        Cheapest Insertion: Finds best position to insert each delivery

    GUIDED_LOCAL_SEARCH:
        Local Search: Improves solution by making small changes
        Guided: Uses memory to avoid repeating bad moves
        Effect: Continues optimizing even after initial solution

    