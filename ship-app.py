import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
import plotly.express as px #New Package
import pydeck as pdk

image1 = "C:/Users/acute/OneDrive - Bentley University/shipwrecks_1.jpg"

path = "C:/Users/acute/OneDrive - Bentley University/"

df = pd.read_csv(path + "Working Shipwreck Database.csv")

def page1():
    st.title("Hidden Treasures: A Collection of New Jersey Coastal Shipwrecks")
    st.markdown('<style>body{background-color: blue;}<\style>', unsafe_allow_html=True)
    image = Image.open(image1)
    st.image(image)
    shipwreck_count = len(df)
    st.header(f"At this time there are currently {shipwreck_count} shipwrecks along the coast of New Jersey with identified coordinates.\n")
    header2 = '<p style="font-family:Serif; color:Blue; font-size: 25px;">Below is a list of all the names of the ships in the map above with the given coordinates:'
    st.markdown(header2, unsafe_allow_html=True)
    df_page_1 = df.loc[:, ["SHIP'S NAME", "LOCATION LOST", "LATITUDE", "LONGITUDE"]]
    st.write(df_page_1)
    header1 = '<p style="font-family:Serif; color:Blue; font-size: 25px;">Below is a map of all the coordinates to sunken ships:'
    st.markdown(header1, unsafe_allow_html=True)
    df2 = df_page_1.drop(columns=["LOCATION LOST"])
    df2.rename(columns={"LATITUDE": "lat", "LONGITUDE": "lon"}, inplace=True)
    ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/2/23/Map_marker_icon_%E2%80%93_Nicolas_Mollet_%E2%80%93_Shipwreck_%E2%80%93_Industry_%E2%80%93_Light.png"
    icon_data = {
        "url": ICON_URL,
        "width": 100,
        "height": 100,
        "anchorY": 1
    }
    df2["icon_data"] = None
    for i in df2.index:
        df2["icon_data"][i] = icon_data
    icon_layer = pdk.Layer(type="IconLayer",
                           data=df2,
                           get_icon="icon_data",
                           get_position='[lon,lat]',
                           get_size=2,
                           size_scale=10,
                           pickable=True)
    view_state = pdk.ViewState(
        latitude=df2["lat"].mean(),
        longitude=df2["lon"].mean(),
        zoom=6,
        pitch=0
    )
    tool_tip = {"html": "Ship Name:<br/> <b>{SHIP'S NAME}</b>",
                "style": {"backgroundColor": "blue",
                          "color": "white"}
                }

    icon_map = pdk.Deck(
        map_style='mapbox://styles/mapbox/satellite-v9',
        layers=[icon_layer],
        initial_view_state=view_state,
        tooltip=tool_tip)
    st.pydeck_chart(icon_map)

def page2():
    st.title("Ship Analytics")
    df1 = df.loc[:, ["YEAR LOST"]]
    df1_sorted = df1.sort_values("YEAR LOST", ascending=True) #Sorting Column in Ascending Order
    year_ranges = range(1750, 2051, 50) #Created New Column to Sort "YEAR LOST" into a range of years for chart summary
    labels = [f"{year}-{year + 50}" for year in year_ranges[:-1]] #List Comprehension/Created New Column to Sort "YEAR LOST" into a range of years for chart summary
    bins = [year_ranges[i] for i in range(len(year_ranges))] #List Comprehension/Created New Column to Sort "YEAR LOST" into a range of years for chart summary
    df1_sorted['year_range'] = pd.cut(df1_sorted["YEAR LOST"], bins=bins, labels=labels, include_lowest=True) #Created New Column to Sort "YEAR LOST" into a range of years for chart summary
    df2 = df1_sorted.drop("YEAR LOST", axis=1) #Created New Column to Sort "YEAR LOST" into a range of years for chart summary
    year_range_counts = df2["year_range"].value_counts()
    year_range_counts = year_range_counts.reindex(["1750-1800", "1800-1850", "1850-1900", "1900-1950", "1950-2000", "2000-2050"])
    year_range_counts.plot(kind = "bar", color= ["black", "red"], rot=0)
    plt.show()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.title("Amount of Shipwrecks in Different Year Ranges")
    plt.xlabel("Year Ranges")
    plt.ylabel("Frequency")
    st.pyplot() #Bar Chart
    st.header("As we can see from the graph above, the year range with the highest amount of shipwrecks was between 1850-1900.") #hardcode?
    df3 = df.loc[:, ["CONSTRUCTION"]].sort_values("CONSTRUCTION", ascending=True)
    construction_counts = df3["CONSTRUCTION"].value_counts()
    fig = px.pie(values=construction_counts.values, names=construction_counts.index, title= "Materials Used for Ship Construction")#New Package
    fig.update_layout(legend_title="Materials") #New Package/Pie Chart
    st.plotly_chart(fig, use_container_width=True) #New Package/Pie Chart
    st.header("As we can see from the graph above, wood was by far the most frequent material used in constructing the sunken ships.") #hardcode?/HELP can use multiple pies?
    df4 = df.loc[:, ["VESSEL TYPE"]].sort_values("VESSEL TYPE", ascending=True)
    vessel_counts = df4["VESSEL TYPE"].value_counts()
    OTHER_LIMIT = 5
    other_values = vessel_counts[vessel_counts < OTHER_LIMIT].index.tolist()
    df4["VESSEL TYPE"] = df4["VESSEL TYPE"].apply(lambda x: 'Other' if x in other_values else x)
    vessel_counts = df4["VESSEL TYPE"].value_counts()
    fig2 = px.pie(values=vessel_counts.values, names=vessel_counts.index,
                 title="Types of Vessels", hole=.3)  # New Package
    fig2.update_layout(legend_title="Vessel Types")  # New Package/Pie Chart
    st.plotly_chart(fig2, use_container_width=True)  # New Package/Pie Chart
    st.write(f"Note: All ship types with less than {OTHER_LIMIT} data points are grouped into the other category.")
    st.header(
        "As we can see from the graph above, Schooners were by far the most frequent material of the sunken ships.")  # hardcode?/HELP can use multiple pies?

def page3():
    st.title("Value of Treasure")
    min_value = 0 #CAPITALIZE
    max_value = 9000000
    max_value2 = 550000
    default_values = [0, 9000000]
    default_values2 = [0,550000]
    min_values, max_values = st.slider(f"Select a ship value range: {min_value} to {max_value}", min_value, max_value, default_values, 1000)
    st.write(f"Selected ship value range: {min_values} to {max_values}")
    min_values2, max_values2 = st.slider(f"Select a cargo value range: {min_value} to {max_value2}", min_value, max_value2, default_values2, 1000)
    st.write(f"Selected cargo value range: {min_values2} to {max_values2}")
    df["SHIP VALUE"] = pd.to_numeric(df["SHIP VALUE"])
    df["CARGO VALUE"] = pd.to_numeric(df["CARGO VALUE"])
    df_page_2 = df.loc[:,["SHIP'S NAME", "SHIP VALUE", "CARGO VALUE"]]
    df_page_2 = df_page_2[(df_page_2["SHIP VALUE"] >= min_values) & (df_page_2["SHIP VALUE"] <= max_values) #Filter by two or more conditions
    & (df_page_2["CARGO VALUE"] >= min_values2) & (df_page_2["CARGO VALUE"] <= max_values2)][["SHIP'S NAME", "SHIP VALUE", "CARGO VALUE"]]
    df_page_2 = df_page_2.replace(0, "No Data")
    st.write(df_page_2)
    return st.write(f"All values are dollar denominated.")


def page4():
    st.title("Ship Dimension Specifications")
    min_value = 0 #CAPITALIZE
    max_value_length = 700
    max_value_beam = 100
    max_value_draft = 105
    max_value_gross = 29100
    default_value_length = [0, 700]
    default_value_beam = [0, 100]
    default_value_draft = [0, 105]
    default_value_gross = [0, 29100]
    min_values, max_values= st.slider("Select a ship length range:", min_value, max_value_length, default_value_length, 5)
    st.write(f"Selected ship length range: {min_values} to {max_values}")
    min_values2, max_values2 = st.slider("Select a ship beam range:", min_value, max_value_beam, default_value_beam, 5)
    st.write(f"Selected ship beam range: {min_values2} to {max_values2}")
    min_values3, max_values3 = st.slider("Select a ship draft range:", min_value, max_value_draft, default_value_draft, 5)
    st.write(f"Selected ship draft range: {min_values3} to {max_values3}")
    min_values4, max_values4 = st.slider("Select a ship gross tonnage range:", min_value, max_value_gross, default_value_gross, 5)
    st.write(f"Selected ship gross tonnage range: {min_values4} to {max_values4}")
    df["LENGTH"] = pd.to_numeric(df["LENGTH"])
    df["BEAM"] = pd.to_numeric(df["BEAM"])
    df["DRAFT"] = pd.to_numeric(df["DRAFT"])
    df["GROSS TONNAGE"] = pd.to_numeric(df["GROSS TONNAGE"])
    df_page_3 = df.loc[:, ["SHIP'S NAME", "LENGTH", "BEAM", "DRAFT", "GROSS TONNAGE"]]
    df_page_3 = df_page_3[(df_page_3["LENGTH"] >= min_values) & (df_page_3["LENGTH"] <= max_values) #Filter by two or more conditions
                          & (df_page_3["BEAM"] >= min_values2) & (df_page_3["BEAM"] <= max_values2) &
                          (df_page_3["DRAFT"] >= min_values3) & (df_page_3["DRAFT"] <= max_values3)
                          & (df_page_3["GROSS TONNAGE"] >= min_values4) & (df_page_3["GROSS TONNAGE"] <= max_values4)][
        ["SHIP'S NAME", "LENGTH", "BEAM", "DRAFT", "GROSS TONNAGE"]]
    df_page_3 = df_page_3.replace(0, "No Data")
    st.write(df_page_3)
    st.write("Length, Beam, and Draft Measurements are in Feet. Gross Tonnage is in Tons.")
    columns = ["LENGTH", "BEAM", "DRAFT", "GROSS TONNAGE"]
    column_name = st.selectbox("Please select a column: ", columns)
    st.write("You have selected", column_name)
    def minmax(column_name, df = "C:/Users/acute/OneDrive - Bentley University/Working Shipwreck Database.csv"):
        non_zero = df[df[column_name] != 0][column_name]  # Exclude zero values
        min_val = non_zero.min()
        max_val = df[column_name].max()
        return min_val, max_val
    st.write("The minimum measurement is", minmax(column_name, df)[0], "and the maximum measurement is", minmax(column_name, df)[-1]) #HELP f-string


def main():
    menu = ["Map", "Ship Analytics", "Value of Treasure", "Ship Dimension Specifications"]
    choice = st.sidebar.selectbox("Select an Option:", menu)
    if choice == "Map":
        page1()
    elif choice == "Ship Analytics":
        page2()
    elif choice == "Value of Treasure":
        page3()
    elif choice == "Ship Dimension Specifications":
        page4()
if __name__ == '__main__':
    main()
