## Conceptual model for optimization problems

### Challenges:

- Clear and total separation between optimization problems (OP) and optimization methods (OM).
- Optimization methods should be implemented using elementar neighborhood operations.
- Such approach enable a fair comparison of different meta-heuristics.
 
### Concepts:
- The **search space S** of a combinatorial optimization problem is a subset of the power set of its components c in C.
- **Solutions** are elements of S, which define *states* for each component c in C (*present*, *absent*, *unknown*)
  - A solution is complete if all the components in C have their state in: *present* or *absent*.
  - A solution is partial if any component in C has its state defined as *unkown*.
- **Components** are problem-specific, it can be a knapsack item, a graph edge, etc.
- **Neighborhoods** define rules of proximity between solutions according to their components. They also can change the components state of a solution. For a minimum spanning tree problem:
  - Prim's algorithm defines as neighbors of x solutions y such c is *unknown* in x but *present* in y
    - By adding c to x, c becomes *present* in x, at the same time other components might become *absent* (e.g. those which leads to infeasible solutions)
  - Kruskal's algorithm, on the other hand, defines other kind of neighboring solutions.
