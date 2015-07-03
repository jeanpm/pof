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


Implementation: 
- Se a estrutura de vizinhaça tiver que providenciar mecanismos para aplicar os movimentos, ela também terá que conhecer a estrutura da solução.

- Se, por outro lado, a aplicação de um movimento for responsabilidade da solução, a vizinhança se torna independente da representação da solução.

- O espaço S é definido implicitamente como o power set do conjunto de possíveis componentes C. Assim, as solucoes x E S, podem ser incompletas


Application:
- Low-level:
  * Definir o espaço baseado em componentes específicos de um determinado problema.
  * Implementar dentro das soluções os controle dos componentes disponíveis. Cada solução mantém em seu estado os componentes utilizados e os disponíveis.

Utilizando os componentes disponíveis, possivelmente implementar novas vizinhanças.

- High-level:
Escolhe a solução a ser utilizada. Não conhece como a solução mantém seu estado de componentes. Apenas sabe a representação utilizada: binária, lista, etc.

- Escolhe a vizinhança a ser utilizada. Bitflip, Swap, etc.

- A vizinhança conhece os componentes usados e os disponíveis de cada solução. Porém não conhece a composição dos componentes.
