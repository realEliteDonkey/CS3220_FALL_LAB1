# Import dependencies
import streamlit as st
import streamlit.components.v1 as components #to display the HTML code
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx #Networkx for creating graph data
from pyvis.network import Network #to create the graph as an interactive html object
import json
import io
import os


class Dynasty:
    def __init__(self,name):
        self._name=name # House name, for.ex."Martell"
        self.characters=[] # Family members ("Doran Martell","Ellaria Sand","Nymeria Sand",...)


    @property
    def name(self): # getter for the private instance attribute _name
        # your code here
        return self._name
       

    @name.setter
    def name(self, value):
        # your code here - should include Validation: Ensure value is not an empty string
        if len(value) == 0:
            return ValueError("Name length must be greater than zero!")
        self.name = value

    def append(self, ch): # to append character to the House (during reading data from JSON-file)
        # your code here 
        #this code will check if character is an instance
        #of the String class. If not, an exception will be raised
        if not isinstance(ch, str):
            return TypeError("Character is not an instance of the String class!")
        self.characters.append(ch)

    def __iter__(self): # to loop through the list of characters via IN operator (for ex. for person in house: ....)
         # your code here 
        for character in sorted(self.characters):
            yield character

    def __contains__(self, ch): # to check if the character belongs to the house (for ex., if person in house ...)
        # your code here 
        # return True or False
        if ch in self.characters:
            return True
        else:
            return False

    def __str__(self): # to print like print(house) - > displat the house's name
        # your code here 
        return self.name
    
    def getStrength(self): # return N of family members in this house (int)
        # your code here
        return int(len(self.characters))
    
    
class GameOfThronesGraph:
    def __init__(self, corpus):
        #initialisation of dictionary that will store all houses. They keys are Houses' (Dynasty) names, the values are Dynasty objects.
        self.houses = {}
        #Load the house corpus
        for data_item in corpus:
            # your code here 
            house=Dynasty(data_item['name'])
            for character in data_item['characters']:
                house.append(character)
            self.houses[data_item['name']] = house


    def __iter__(self): # for the case like the following: for house in GameOfThronesHouses:
        # your code here 
        for house in self.houses.values():
            yield house
            
    def __contains__(self, h): #Check if h (house's name) is a key in dict houses
        if h in self.houses:
            return True
        else:
            return False


def main():
    file_name = "data/game-of-thrones-characters-groups.json"
    path="data"
    
    json_files = [os.path.join(root, name) 
              for root, dirs, files in os.walk(path) 
              for name in files 
              if name.endswith((".json"))] #If we needed to read several files extensions: if name.endswith((".ext1", ".ext2"))

    print('Number of JSON files ready to be loaded: ' + str(len(json_files)))
    print('Path to the first file: '+json_files[0])
    
    #Open the file using the name of the json file witn open() function
    #Read the json file using load() and put the json data into a variable.
    with open(json_files[0]) as f:
        json_data = json.load(f)
        
    json_data.keys() #the top-level variable 
    
    for data in json_data['groups']:
        house=Dynasty(data['name'])
        for character in data['characters']:
            house.append(character)
        print(house)
        print("Our members:")
        for person in house:
            print(person)
        print(f"We have {house.getStrength()} family members!!!")
    
    corpusData=json_data['groups']
    GameOfThronesHouses=GameOfThronesGraph(corpusData)
    for house in GameOfThronesHouses:
        print(house)
        
    visualisationData={}
    legendData=[]
    for house in GameOfThronesHouses:
        print(house)
        print(f"Strength: {house.getStrength()}")
        visualisationData[house.name]=house.getStrength()
        legendData.append(house.name)
        
    #Configure your x and y values from the dictionary:
    x= list(visualisationData.keys())
    y=list(visualisationData.values())

    #Create the graph = create seaborn barplot
    ax=sns.barplot(x=x,y=y)

    #specfiy axis labels
    ax.legend(legendData)
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1.05, 1))
    ax.set(xlabel='Houses',
        ylabel='Strength (N family members)',
        title='Strength of GameOfThronesHouses')

    plt.xticks(rotation=45)
    #display barplot
    plt.show()
    
    g = nx.Graph() # graph initialization
    
    N_houses=0
    colorKeys=[]
    for house in GameOfThronesHouses:
        if house.name!="Include":
            N_houses+=1
            colorKeys.append(house.name)
    sns.color_palette("husl", N_houses) # N_houses colors
    
    list(sns.color_palette("husl", N_houses))
    
    nodeColors=dict(zip(colorKeys, [tuple(int(c*255) for c in cs) for cs in sns.color_palette("husl", N_houses)]))
    
    g.clear()
    
    for house in GameOfThronesHouses:
        if house.name!="Include":
            # add the house's name as a node to the graph g (houses's strength values is used as a node's size)
            #your code here
            g.add_node(house.name, strength=house.getStrength(), color=nodeColors[house.name])
    
    for node, attributes in g.nodes(data=True): # run this code to check your code above
        print(f"Node: {node}, Attributes: {attributes}")
    
    for house in GameOfThronesHouses:
        if house.name!="Include":
            # add each character as a node to the graph g 
            #your code here
            for character in house.characters:
                g.add_node(character, color=nodeColors[house.name])
                
    for node, attributes in g.nodes(data=True): # run this code to check your code above
        print(f"Node: {node}, Attributes: {attributes}")
        
    myEdges=[]
    
    for house in GameOfThronesHouses:
        if house.name != "Include":
            for person in house.characters:
                #your code here
                myEdges.append((house.name, person))
        
    print("Connections between a House and its family members:") # run this code to check your code above

    g.add_edges_from(myEdges)
    
    list(g.edges)
    
    len(list(g.edges))
    
    GameOfThronesNet = Network(
                bgcolor ="#101010",
                font_color = "white",
                height = "1000px",
                width = "100%",
                notebook=True,
                cdn_resources = "remote")
    
    GameOfThronesNet.from_nx(g)  
    
    for node in GameOfThronesNet.nodes:
        # specify colors for houses
        if node["id"] in GameOfThronesHouses.houses:
            # Convert RGB to hexadecimal string
            node["color"] = '#%02x%02x%02x' % nodeColors[node["id"]]
        # specify colors for members
        else:
            house_name = None
            for pair in myEdges:
                if pair[1] == node["id"]:
                    house_name = pair[0]
            if house_name in nodeColors:
                node["color"] = '#%02x%02x%02x' % nodeColors[house_name]
        
    GameOfThronesNet.show("GameOfThronesNet.html",notebook=False)
    
    
    
# STREAMLIT FUNCTIONALITY ---------------------------------------------------------------------------------

    st.header("Task 2: Infographic of Relationships between characters in GoT")

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Game of Thrones Houses", "Members of Houses", "Graph of GOT Houses"])

    # ---- Tab 1: Houses ----
    with tab1:
        st.header("Game of Thrones Houses")

        st.write("Game of Thrones Houses:")
        
        for house in GameOfThronesHouses:
            st.write("This is a house of ", house, "!", " Strength: ", len(house.characters))
        
        st.pyplot(plt)

    # ---- Tab 2: Members ----
    with tab2:
        st.header("Members of Houses")

        for houses in GameOfThronesHouses:
            st.write("This is a House of ", houses, "! Our Members:")
            for character in houses.characters:
                st.write(character)

    # ---- Tab 3: Graph + HTML ----
    with tab3:
        st.header("Graph of GOT Houses")

        with open('GameOfThronesNet.html', 'r') as f:
            html = f.read()
        st.components.v1.html(html, height=1000)


        
        



if __name__ == '__main__':
    main()