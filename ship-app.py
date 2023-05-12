import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
import plotly.express as px #New Package
import pydeck as pdk
import numpy as np
import math

st.set_page_config(page_title="NJ Shipwreck Database")

ad_unit_code_ = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8357676857910564"
     crossorigin="anonymous"></script>
<!-- Ship1 -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-8357676857910564"
     data-ad-slot="6944243680"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
"""
st.markdown(ad_unit_code_, unsafe_allow_html=True)

adsense_code = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8357676857910564"
     crossorigin="anonymous"></script>
"""
st.markdown(adsense_code, unsafe_allow_html=True)

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
    header1 = '<p style="font-family:Verdana; color:#00CED1; font-size: 25px;">Below is a list of all the names of the ships in the map above with the given coordinates:'
    st.markdown(header1, unsafe_allow_html=True)
    df_page_1 = df.loc[:, ["SHIP'S NAME", "LOCATION LOST", "LATITUDE", "LONGITUDE"]]
    def search_column(col, text, df = (path + "Working Shipwreck Database.csv")):
        return df[df[col].str.contains(text, case=False)]
    input_text = st.text_input("Enter ship name:")
    result = search_column("SHIP'S NAME", input_text, df_page_1)
    st.write(result)
    header2 = '<p style="font-family:Verdana; color:#00CED1; font-size: 25px;">Below is a map of all the coordinates to sunken ships:'
    st.markdown(header2, unsafe_allow_html=True)
    df2 = df_page_1.drop(columns=["LOCATION LOST"])
    df2.rename(columns={"LATITUDE": "lat", "LONGITUDE": "lon"}, inplace=True)
    ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/2/23/Map_marker_icon_%E2%80%93_Nicolas_Mollet_%E2%80%93_Shipwreck_%E2%80%93_Industry_%E2%80%93_Light.png"
    icon_data = {"url": ICON_URL,"width": 100,"height": 100,"anchorY": 1}
    df2["icon_data"] = None
    for i in df2.index:
        df2["icon_data"][i] = icon_data
    icon_layer = pdk.Layer(type="IconLayer",data=df2,get_icon="icon_data",get_position='[lon,lat]',get_size=2,size_scale=10,pickable=True)
    view_state = pdk.ViewState(latitude=df2["lat"].mean(),longitude=df2["lon"].mean(),zoom=6,pitch=0)
    tool_tip = {"html": "Ship Name:<br/> <b>{SHIP'S NAME}</br> <b>{lat}, {lon}</b>", "style": {"backgroundColor": "blue", "color": "white"}}
    icon_map = pdk.Deck(map_style='mapbox://styles/mapbox/satellite-v9',layers=[icon_layer],initial_view_state=view_state,tooltip=tool_tip)
    st.pydeck_chart(icon_map) # Map with custom icon, tooltips, and a satellite style
    header3 = '<p style="font-family:Verdana; color:#00CED1; font-size: 25px;">More details regarding the minimum and maximum coordinates:'
    st.markdown(header3, unsafe_allow_html=True)

def page2():
    st.title("Ship Analytics")
    # Discussion Point 1
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
    most_frequent_range = df2["year_range"].value_counts().idxmax()
    st.header(f"As we can see from the graph above, the year range with the highest amount of shipwrecks was between {most_frequent_range}.")
    df3 = df.loc[:, ["CONSTRUCTION"]].sort_values("CONSTRUCTION", ascending=True) # Sort by ascending order
    construction_counts = df3["CONSTRUCTION"].value_counts()
    fig = px.pie(values=construction_counts.values, names=construction_counts.index, title= "Materials Used for Ship Construction")#New Package
    fig.update_layout(legend_title="Materials") #New Package/Pie Chart
    st.plotly_chart(fig, use_container_width=True) #New Package/Pie Chart
    most_frequent_range2 = df3["CONSTRUCTION"].value_counts().idxmax()
    st.header(f"As we can see from the graph above, {most_frequent_range2.lower()} was by far the most frequent material used in constructing the sunken ships.")
    df4 = df.loc[:, ["VESSEL TYPE"]].sort_values("VESSEL TYPE", ascending=True)
    vessel_counts = df4["VESSEL TYPE"].value_counts()
    OTHER_LIMIT = 5
    other_values = vessel_counts[vessel_counts < OTHER_LIMIT].index.tolist()
    df4["VESSEL TYPE"] = df4["VESSEL TYPE"].apply(lambda x: 'Other' if x in other_values else x)
    vessel_counts = df4["VESSEL TYPE"].value_counts()
    fig2 = px.pie(values=vessel_counts.values, names=vessel_counts.index,
                 title="Types of Vessels", hole=.3)  # New Package
    fig2.update_layout(legend_title="Vessel Types")  # New Package/Donut Chart
    st.plotly_chart(fig2, use_container_width=True)  # New Package/Donut Chart
    st.write(f"Note: All ship types with less than {OTHER_LIMIT} data points are grouped into the other category.")
    most_frequent_range3 = df4["VESSEL TYPE"].value_counts().idxmax()
    st.header(f"As we can see from the graph above, {most_frequent_range3}s were by far the most frequent material of the sunken ships.")

def page3():
    st.title("Value of Treasure")
    MIN_VALUE = 0
    INCREMENT = 1000
    MAX_VALUE = int(max(df["SHIP VALUE"]))
    MAX_VALUE2 = int(max(df["CARGO VALUE"]))
    DEFAULT_VALUES = [MIN_VALUE, MAX_VALUE]
    DEFAULT_VALUES2 = [MIN_VALUE,MAX_VALUE2]
    min_values, max_values = st.slider(f"Select a ship value range: {MIN_VALUE} to {MAX_VALUE}", MIN_VALUE, MAX_VALUE, DEFAULT_VALUES, INCREMENT)
    st.write(f"Selected ship value range: {min_values} to {max_values}")
    min_values2, max_values2 = st.slider(f"Select a cargo value range: {MIN_VALUE} to {MAX_VALUE2}", MIN_VALUE, MAX_VALUE2, DEFAULT_VALUES2, INCREMENT)
    st.write(f"Selected cargo value range: {min_values2} to {max_values2}")
    df["SHIP VALUE"] = pd.to_numeric(df["SHIP VALUE"])
    df["CARGO VALUE"] = pd.to_numeric(df["CARGO VALUE"])
    df_page_3 = df.loc[:,["SHIP'S NAME", "SHIP VALUE", "CARGO VALUE"]]
    df_page_3 = df_page_3[(df_page_3["SHIP VALUE"] >= min_values) & (df_page_3["SHIP VALUE"] <= max_values) #Filter by two or more conditions
    & (df_page_3["CARGO VALUE"] >= min_values2) & (df_page_3["CARGO VALUE"] <= max_values2)][["SHIP'S NAME", "SHIP VALUE", "CARGO VALUE"]]
    #Problem to talk about:
    df_page_3 = df_page_3.astype(str)
    df_page_3 = df_page_3.apply(lambda x: x.fillna("No Data") if x.dtype == "object" else x.fillna(0))
    df_page_3 = df_page_3.replace("0.0", "No Data")
    st.write(df_page_3)
    def min_nonzero(x):
        nonzero_vals = x[x != 0]
        if len(nonzero_vals) > 0:
            return np.min(nonzero_vals)
        else:
            return 0
    top_3_columns = df["CONSTRUCTION"].value_counts().nlargest(3).index.tolist()
    pivot_table = pd.pivot_table(df[df["CONSTRUCTION"].isin(top_3_columns)], values="SHIP VALUE", index="CONSTRUCTION", aggfunc=[min_nonzero,max]) # Pivot Tables
    pivot_table2 = pd.pivot_table(df[df["CONSTRUCTION"].isin(top_3_columns)].iloc[:], values="CARGO VALUE", index="CONSTRUCTION",
                                 aggfunc=[min_nonzero, max])
    header1 = '<p style="font-family:Verdana; color:#00CED1; font-size: 30px;">The minimum and maximum ship values from the three most common construction materials:'
    st.markdown(header1, unsafe_allow_html=True)
    st.write(pivot_table) # Pivot Table
    header2 = '<p style="font-family:Verdana; color:#00CED1; font-size: 30px;">The minimum and maximum cargo values from the three most common construction materials:'
    st.markdown(header2, unsafe_allow_html=True)
    st.write(pivot_table2) # Pivot Table 2
    st.write(f"All values are dollar denominated.")

def page4():
    st.title("Ship Dimension Specifications")
    MIN_VALUE = 0
    INCREMENT = 5
    MAX_VALUE_LENGTH = math.ceil(df["LENGTH"].max() / INCREMENT) * INCREMENT #These values are chosen as numbers that are a multiple of 5 above the maximum value in each column
    MAX_VALUE_BEAM = math.ceil(df["BEAM"].max() / INCREMENT) * INCREMENT
    MAX_VALUE_DRAFT = math.ceil(df["DRAFT"].max() / INCREMENT) * INCREMENT
    MAX_VALUE_GROSS = math.ceil(df["GROSS TONNAGE"].max() / INCREMENT) * INCREMENT
    DEFAULT_VALUE_LENGTH = [MIN_VALUE, MAX_VALUE_LENGTH]
    DEFAULT_VALUE_BEAM = [MIN_VALUE, MAX_VALUE_BEAM]
    DEFAULT_VALUE_DRAFT = [MIN_VALUE, MAX_VALUE_DRAFT]
    DEFAULT_VALUE_GROSS = [MIN_VALUE, MAX_VALUE_GROSS]
    #Discussion Point 2
    min_values, max_values= st.slider("Select a ship length range:", MIN_VALUE, MAX_VALUE_LENGTH, DEFAULT_VALUE_LENGTH, INCREMENT)
    st.write(f"Selected ship length range: {min_values} to {max_values}")
    min_values2, max_values2 = st.slider("Select a ship beam range:", MIN_VALUE, MAX_VALUE_BEAM, DEFAULT_VALUE_BEAM, INCREMENT)
    st.write(f"Selected ship beam range: {min_values2} to {max_values2}")
    min_values3, max_values3 = st.slider("Select a ship draft range:", MIN_VALUE, MAX_VALUE_DRAFT, DEFAULT_VALUE_DRAFT, INCREMENT)
    st.write(f"Selected ship draft range: {min_values3} to {max_values3}")
    min_values4, max_values4 = st.slider("Select a ship gross tonnage range:", MIN_VALUE, MAX_VALUE_GROSS, DEFAULT_VALUE_GROSS, INCREMENT)
    st.write(f"Selected ship gross tonnage range: {min_values4} to {max_values4}")
    df["LENGTH"] = pd.to_numeric(df["LENGTH"])
    df["BEAM"] = pd.to_numeric(df["BEAM"])
    df["DRAFT"] = pd.to_numeric(df["DRAFT"])
    df["GROSS TONNAGE"] = pd.to_numeric(df["GROSS TONNAGE"])
    df_page_4 = df.loc[:, ["SHIP'S NAME", "LENGTH", "BEAM", "DRAFT", "GROSS TONNAGE"]]
    df_page_4 = df_page_4[(df_page_4["LENGTH"] >= min_values) & (df_page_4["LENGTH"] <= max_values) #Filter by two or more conditions
                              & (df_page_4["BEAM"] >= min_values2) & (df_page_4["BEAM"] <= max_values2) &
                              (df_page_4["DRAFT"] >= min_values3) & (df_page_4["DRAFT"] <= max_values3)
                              & (df_page_4["GROSS TONNAGE"] >= min_values4) & (df_page_4["GROSS TONNAGE"] <= max_values4)][
            ["SHIP'S NAME", "LENGTH", "BEAM", "DRAFT", "GROSS TONNAGE"]]
    df_page_4 = df_page_4.astype(str)
    df_page_4 = df_page_4.apply(lambda x: x.fillna("No Data") if x.dtype == "object" else x.fillna(0))
    df_page_4 = df_page_4.replace("0.0", "No Data")
    st.write(df_page_4)
    st.write("Note: Length, Beam, and Draft Measurements are in Feet. Gross Tonnage is in Tons.")

def main():
    menu = ["Map", "Ship Analytics", "Value of Treasure", "Ship Dimension Specifications"]
    choice = st.sidebar.selectbox("Select an Option:", menu)
    def minmax(column_name, df = (path + "Working Shipwreck Database.csv")):
        non_zero = df[df[column_name] != 0][column_name]  # Exclude zero values
        min_val = non_zero.min()
        max_val = df[column_name].max()
        return min_val, max_val
    if choice == "Map":
        page1()
        columns = ["LATITUDE", "LONGITUDE"]
        column_name = st.multiselect("Please select a coordinate: ", columns)
        for col in column_name:
            st.write(f"Minimum value of {col}: {minmax(column_name, df)[0][col]}")
            st.write(f"Maximum value of {col}: {minmax(column_name, df)[-1][col]}")
    elif choice == "Ship Analytics":
        page2()
    elif choice == "Value of Treasure":
        page3()
    elif choice == "Ship Dimension Specifications":
        page4()
        columns = ["LENGTH", "BEAM", "DRAFT", "GROSS TONNAGE"]
        column_name = st.selectbox("Please select a column: ", columns)
        st.write("You have selected", column_name)
        string_min, string_max = str(minmax(column_name, df)[0]), str(minmax(column_name, df)[-1])
        st.write("The minimum measurement is", string_min, "and the maximum measurement is",
                 string_max + ".")
if __name__ == '__main__':
    main()
