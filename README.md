# Conceptual model for optimization problems

Challenges:

- Clear and total separation between optimization problems (OP) and optimization methods (OM).
- An optimization problem encompasses:
  1. A space composed of components,
    * A component is a problem specific concept, e.g. in a knapsack problem it can be an item, in a minimum spanning tree problem it can be an edge,
    * Components are the unities of information used to compose and modify solutions in the lower-level of the framework.
  2. The components induce a neighborhood structure on the solution space:
    * Solutions are considered neighbors if they differ by only one component,
    * Complex components lead to larger neighborhoods.
  3. A partial solution structure, which provides methods to add and remove components:
    * An empty solution has neighbors which are composed of more components,
    * Partial solutions are usually infeasible solutions.
  4. Everything is local-search:
    * Constructive methods work on neighborhoods containing partial solutions,

- An optimization method must choose which solution representation and respective neighborhood to use:
  1. From a incumbent solution and neighborhood exploration methods, they must implement which 



