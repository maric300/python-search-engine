class Graph:
  """ Reprezentacija jednostavnog grafa"""

  #------------------------- Ugnjeydena klasa Vertex -------------------------
  class Vertex:
    """ Struktura koja predstavlja cvor grafa."""
    __slots__ = '_element'

    def __init__(self, x):
      self._element = x
  
    def element(self):
      """Vraca element vezan za cvor grafa."""
      return self._element
  
    def __hash__(self):
      return hash(id(self))

    def __str__(self):
      return str(self._element)
    
  #------------------------- Ugnjeydena klasa Edge -------------------------
  class Edge:
    """ Struktura koja predstavlja ivicu grafa """
    __slots__ = '_origin', '_destination', '_element'
  
    def __init__(self, origin, destination, element):
      self._origin = origin
      self._destination = destination
      self._element = element
  
    def opposite(self, v):
      """ Vraca cvor koji se nalazi sa druge strane cvora v ove ivice."""
      if not isinstance(v, Graph.Vertex):
        raise TypeError('v mora biti instanca klase Vertex')
      if self._destination == v:
        return self._origin
      elif self._origin == v:
        return self._destination
      raise ValueError('v nije cvor ivice')
  
    def element(self):
      """ Vraca element vezan za ivicu"""
      return self._element
  
    def __hash__(self):         # omogucava da Edge bude kljuc mape
      return hash( (self._origin, self._destination) )

    def __str__(self):
      return '({0},{1},{2})'.format(self._origin,self._destination,self._element)
    
  #------------------------- Metode klase Graph -------------------------
  def __init__(self):
    """ Kreira prazan usmereni graf

    """
    self._outgoing = {}
    self._incoming = {}

  def _validate_vertex(self, v):
    """ Proverava da li je v cvor(Vertex) ovog grafa."""
    if not isinstance(v, self.Vertex):
      raise TypeError('Ocekivan je objekat klase Vertex')
    if v not in self._outgoing:
      raise ValueError('Vertex ne pripada ovom grafu.')

  def vertex_count(self):
    """ Vraca broj cvorova u grafu."""
    return len(self._outgoing)

  def edge_count(self):
    """ Vraca broj ivica u grafu."""
    total = sum(len(self._outgoing[v]) for v in self._outgoing)
    return total

  def get_edge(self, u, v):
    """ Vraca ivicu izmedju cvorova u i v ili None ako nisu susedni."""
    self._validate_vertex(u)
    self._validate_vertex(v)
    return self._outgoing[u].get(v)

  def incident_edges(self, v, outgoing=True):   
    """ Vraca sve (odlazne) ivice iz cvora v u grafu.

    Ako je graf usmeren, opcioni parametar outgoing se koristi za brojanje dolaznih ivica.
    """
    self._validate_vertex(v)
    adj = self._outgoing if outgoing else self._incoming
    for edge in adj[v].values():
      yield edge

  def insert_vertex(self, x=None):
    """ Ubacuje i vraca novi cvor (Vertex) sa elementom x"""
    v = self.Vertex(x)
    self._outgoing[v] = {}
    self._incoming[v] = {}       
    return v
      
  def insert_edge(self, u, v, x=None):
    """ Ubacuje i vraca novu ivicu (Edge) od u do v sa pomocnim elementom x.

    Baca ValueError ako u i v nisu cvorovi grafa.
    Baca ValueError ako su u i v vec povezani.
    """
    if self.get_edge(u, v) is not None:      
      raise ValueError('u and v are already adjacent')
    e = self.Edge(u, v, x)
    self._outgoing[u][v] = e
    self._incoming[v][u] = e

def graph_from_edgelist(E):
  """Kreira graf od ivica.

  Dozvoljeno je dva nacina navodjenje ivica:
  (origin,destination, destionation, ...)
  Podrazumeva se da se labele cvorova mogu hesovati.
  """
  g = Graph()
  V = set()
  for e in E:
    for small_e in e:
      V.add(small_e)

  vertices = {} #izbegavamo ponavljanje labela izmedju cvorova
  for v in V:
    vertices[v] = g.insert_vertex(v)

  for e in E:
    src = e[0]
    for small_e in range(1, len(e)):
      dest = e[small_e]
      g.insert_edge(vertices[src],vertices[dest],None)

  return vertices, g
