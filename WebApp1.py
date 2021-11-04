import streamlit as st
import streamlit.components.v1 as components
import pandas as pd 

import matplotlib.pyplot as plt

Header = st.container()
Viewer = st.container()
Volume = st.container()
Carbon = st.container()

materialKgm3 = {"Concrete":2400, "Steel":7850, "Timber":305, "Insulation":100, "Reinforcement":7850}
materialCo2 = {"Concrete":0.13, "Steel":2.45, "Timber":0.27, "Insulation":1.0, "Reinforcement":1.99}

#@st.cache
def get_data(filename):
    data = pd.read_csv(filename)
    return data

with Header:
    st.header("Revit sample structural model")
    #st.text("Volumes in m3 and materials from Revit with Dynamo")
    data = get_data("https://raw.githubusercontent.com/davewilsonxyz/data/main/volumesMaterials.csv")
    data["kg"] = data["Material"].map(materialKgm3)
    data["kgCO2kg"] = data["Material"].map(materialCo2)
    data["CO2"] = data["Volumes"] * data["kg"] * data["kgCO2kg"]
    st.write(data[["Mark", "Volumes", "Material", "CO2"]])

    
    st.text("")
 
    tots = pd.DataFrame(data.groupby(["Material"]).sum())

    
    carbon = round(data["CO2"].sum(),3)
    flights = int(carbon / 234)
    burgers = int(carbon / 4.85)
    burgerYears = int(burgers/365)
    meters = (70/1000)*burgers
    st.text("The total carbon cost " + str(carbon)+" kg")
    st.text("The equivalent of taking "+str(flights)+" flights from London to Rome" )
    st.text("The equivalent of eating "+str(burgers)+" burgers. Thats a burger a day for "+ str(burgerYears)+ " years.")
    
with Viewer:
    st.header("Speckle viewer")
    st.text("Revit sample model hosted in Speckle")
    components.iframe("https://speckle.xyz/embed?stream=21598ecfdf&branch=structural", height=400)
    
with Volume:
    st.header("Structural Volumes")
    st.text("Structural volumes by material")
    
    import matplotlib.pyplot as plt

    labels = ['Concrete', 'Insul', 'Rebar', 'Steel', 'Timber']
    sizes = list(tots["Volumes"]/sum(tots["Volumes"]))
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99', '#ffcc99']
    plt.rcParams.update({'font.size': 7})

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=20)
    centre_circle = plt.Circle((0,0),0.750,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    ax1.axis('equal')  
    plt.tight_layout()
    st.pyplot(fig1)

with Carbon:
    st.header("Embodied Carbon")
    st.text("Embodied carbon by material")
    totsCO2 = pd.DataFrame(data.groupby(["Material"]).sum())
    sizes = list(totsCO2["CO2"]/sum(data["CO2"]))
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=10)
    centre_circle = plt.Circle((0,0),0.750,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    ax1.axis('equal')  
    plt.tight_layout()
    st.pyplot(fig1)
