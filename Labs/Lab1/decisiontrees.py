# decisiontrees.py
# Import the relevant modules from graphviz. Digraph means a graph with directions.

# Create a type called Node. A class is a complex object with associated attributes and functions.
class Node(object):
    ''' An object corresponding to an individual node in a decision tree. 
    There are three types of nodes: event, decision, or outcome (or value) nodes.
    
        The attributes are:
            - name: a user specified string that denotes the Node.
            - type: a string that specifies the type of the node. Outcome nodes are denoted using the name "value."
            - children: list of the immediate nodes that descend from this node. Empty if is an outcome/value node.
            - probabilities: (exists for event nodes only) a list of the corresponding probabilities for the children.
            - value: (exists for outcome nodes only) the value of the node. 

            
        The functions are:
            evaluate(): Return the value of the node using backward induction.
            graph(showValues): Return a graphviz object that corresponds to the decision tree. 
                Use showValues=True to see the values after solving by backward induction.
                Use showValues=False to see the structure of the tree without solving.
            
    '''
    def __init__(self,name,children=[],probabilities=[],value=0):
        ''' To create a node, use the following syntax:
            x=Node(name,children,probabilities) (For event nodes)
            x=Node(name,children) (For decision nodes)
            x=Node(name,value=value) (For outcome nodes)
        '''
        self.name=name
        # Decide what type of node it is based on existence of function inputs.
        if probabilities:
            self.type='event'
            self.children=children
            self.probabilities=probabilities
            assert len(probabilities)==len(children), 'The length of the lists "children" and "probabilities" must equal!'
        elif children:
            self.type='decision'
            self.children=children
        else:
            self.type='value'
            self.children=[]
            self.value=value

    def evaluate(self):
        ''' Function that evaluates the current node by backward induction '''
        if self.type=='value':
            # For outcome nodes, return value
            return self.value
        elif self.type=='event':
            # For event nodes, return expected value
            return sum([self.probabilities[i]*self.children[i].evaluate() for i in range(len(self.children))])
        else:
            # For decision nodes, return the value of the best decision
            return max([self.children[i].evaluate() for i in range(len(self.children))])
        
    def _drawNodes(self,graph,showValues=True):
        ''' Function to draw all nodes that are descendent of the current node.'''
        if self.type=='value':
            graph.attr('node',shape='plaintext')
        elif self.type=='event':
            graph.attr('node',shape='oval')
        else:
            graph.attr('node',shape='square')
        if showValues:
            myLabel='{:.0f}'.format(self.evaluate())
        else:
            myLabel=self.type
        graph.node(repr(self),myLabel)
        for child in self.children:
            child._drawNodes(graph,showValues)
            
    def _drawEdges(self,graph):
        ''' Function to draw all edges that are descendent of the current node.'''
        for i,child in enumerate(self.children):
            if self.type=='decision':
                myLabel=child.name
            else:
                myLabel='{0} ({1:.0%})'.format(child.name,self.probabilities[i])
            graph.edge(repr(self),repr(child),label=myLabel)
        for child in self.children:
            child._drawEdges(graph)

    def graph(self,showValues=True,treeName='decision tree'):
        ''' Function to return a graphviz object that graphically represent the decision tree from this node
        Inputs:
            - showValues: True if draw the values; False if draw the shape only.
            - treeName: a name for the decision tree that is used by the underlying graphviz package.
        '''
        try:
            from agraphviz import Digraph
            graph=Digraph(treeName)
            self._drawNodes(graph,showValues)
            self._drawEdges(graph)
            return graph
        except:
            return str(self)
    
    def _toText(self):
        ''' Function that outputs the underling graph in text format. Used internally by __str__(self) 
        for print statements.
        Returns: 
            - title: a description of the current node.
            - lines: a list of strings representing the descendants of the current node '''
        title='{0}, {1} node with value {2:.2f}'.format(self.name,self.type.upper(),self.evaluate())
        lines=[]
        if self.type=='decision':
            ownValue=self.evaluate()
            for i, child in enumerate(self.children):
                childTitle,childLines=child._toText()
                if child.evaluate()==ownValue:
                    suffix=' (Optimal decision for node {})'.format(self.name)
                else:
                    suffix=''
                lines.append('--> Option {0}: {1}{2}'.format(i+1,childTitle,suffix))
                lines+=['    '+childLine for childLine in childLines]
        elif self.type=='event':
            for i, child in enumerate(self.children):
                childTitle,childLines=child._toText()
                lines.append('--> w.p. {0:.2f}: {1}'.format(self.probabilities[i],childTitle))
                lines+=['    '+childLine for childLine in childLines]
        return title,lines
    
    def __str__(self):
        title,lines=self._toText()
        return '\n'.join([title]+lines)
        
        
    