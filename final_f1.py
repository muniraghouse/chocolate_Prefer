import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image
import datetime
from streamlit_option_menu import option_menu
import graphviz as graphviz
st.set_page_config(
    page_title ="Chocolate Data Analysis",
    page_icon ="chart_with_upwards_trend",
    layout = "wide"
)
# Loading data
df=pd.read_csv(r"C:\Users\Administrator\Desktop\INTERN\python\ChocolateEaters.csv")
df.rename(columns = {'Rating ':'Rating'}, inplace=True)
df.rename(columns = {' Brand ':'Brand'}, inplace=True)

##menu=====================
with st.sidebar:
    selected = option_menu(
    menu_title ="Main menu",
    options = ['Home', 'Overview','Demographic','Brand','Types','Preference','Feedback'],
    icons = ['house','house','book','envelope','book','envelope','house'],
    menu_icon = 'cast',
)
if selected =='Home':
   st.markdown("<h1 style='text-align: center;'>Presentation Of Chocolate Eaters</h1>", unsafe_allow_html=True)
   image = Image.open('choco.jpg')
   st.image(image, caption='Chocolate',width=1000)
if selected =='Overview':
   st.header("")
   st.markdown("<h1 style='text-align: center; color: Brown;'>Chocolate Preferences</h1>", unsafe_allow_html=True)
   st.write("")
   st.graphviz_chart('''
    digraph {
      Demographic -> Rating  
      Brand -> Rating  
      Types -> Rating  
      Preference -> Rating
      Feedback -> Rating
      }
''')


if selected =='Demographic':
    st.header("")
    tab1, tab2, tab3 = st.tabs(["DataFrame","QOI", "Demographic"])
    
    with tab1:
       st.header("Dataset") 
       st.write(df.head())
    with tab2:
     st.markdown("""## Distribution of Rating""")
     fig = px.bar(df['Rating'].value_counts(), text='value')
     st.plotly_chart(fig,use_container_width=True)
     st.header("Summary for Rating")
     r=df['Rating']
     st.table(r.value_counts())
     def convert_df(df):
        return df.to_csv().encode('utf-8')
     st.download_button(
     label="Download",
     data=convert_df(r),
     file_name='Rating.csv',
     mime='text/csv',
     )
    with tab3:
     st.header("Please Filter Here:")
     age_selection = st.slider('Rating:',
                        min_value= min(df['Rating']),
                        max_value= max(df['Rating']),
                        value=(min(df['Rating']),max(df['Rating'])))
     mask = (df['Rating'].between(*age_selection))
     st.header("Distribution of Rating based on Age & Gender")
     fig = px.bar(df[mask], x="Gender", y="Rating", color="Gender", barmode="group",facet_col="Age" )
     st.plotly_chart(fig,use_container_width=True)
     st.header("Summary")
     br= df.groupby(['Gender', 'Age'])['Rating'].aggregate(['count','mean','median','min', 'max'])
     st.table(br)
     def convert_df(df):
        return df.to_csv().encode('utf-8')
     st.download_button(
     label="Download",
     data=convert_df(br),
     file_name='behavior.csv',
     mime='text/csv',
     )
if selected =='Brand':
    st.header("")
    tab1, tab2  = st.tabs(["Brands", "Product"])
    with tab1:
         options=st.selectbox('**Select the variables**', ["None",'Age','Gender'], key="options")
         if options == 'None':
          st.header("Distribution of Rating based on Brand")
          fig = px.pie(df, values='Rating', names='Brand')
          st.plotly_chart(fig,use_container_width=True)
          st.header("Summary")
          brd= df.groupby("Brand")["Rating"].agg({'count','mean','median','min', 'max'})
          st.table(brd)
          def convert_df(df):
            return df.to_csv().encode('utf-8')
          csv = convert_df(brd)
          st.download_button(
          label="Download",
          data=csv,
          file_name='brand.csv',
          mime='text/csv',
        )
         elif options == 'Age':
          st.header("Distribution of Rating based on Brand & Age")
          fig = px.box(df, x='Brand', y='Rating', color='Brand', facet_col='Age')
          st.plotly_chart(fig,use_container_width=True)
          st.header("Summary")
          a=df.groupby(['Brand', 'Age'])['Rating'].aggregate(['count','mean','median','min', 'max'])
          st.table(a)
          
         elif options == 'Gender':
          st.header("Distribution of Rating based on Brand & Gender")
          st.sidebar.header("Please Filter Here:")
          df_selection = st.sidebar.multiselect("Select the Age:",
                   options=df["Age"].unique(),
                   default=df["Age"].unique())
          mask = df['Age'].isin(df_selection) 
          fig = px.box(df[mask], x='Brand', y='Rating', color='Gender')
          st.plotly_chart(fig,use_container_width=True)
          st.header("Summary")
          ag=df.groupby(['Brand', 'Gender'])['Rating'].aggregate(['count','mean','median','min', 'max'])
          st.table(ag)
    with tab2:
       
         options1=st.selectbox('**Select the Brand**', ["Cadbury",'Nestle','Snickers','Galaxy'], key="options1")
         if options1 == 'Cadbury':
          st.header("Distribution of Rating based on Cadbury Product")
          cad_percent = (df[['b_Cadbury', 'Rating', 'Gender']].groupby('b_Cadbury')['Rating'].count() / len(df['b_Cadbury']) * 100).round(2)
          fig = px.bar(cad_percent)
          st.plotly_chart(fig,use_container_width=True)
          st.header("Summary")
          ac=df.groupby(['b_Cadbury', 'Gender'])['Rating'].aggregate(['count','mean','median','min', 'max'])
          st.table(ac)
         elif options1 == 'Nestle':
          st.header("Distribution of Rating based on Nestle Product")
          nes_percent = (df[['b_Nestle ', 'Rating', 'Gender']].groupby('b_Nestle ')['Rating'].count() / len(df['b_Nestle ']) * 100).round(2)
          fig = px.bar(nes_percent)
          st.plotly_chart(fig,use_container_width=True)
          st.header("Summary")
          ac=df.groupby(['b_Nestle ', 'Gender'])['Rating'].aggregate(['count','mean','median','min', 'max'])
          st.table(ac)
         elif options1 == 'Snickers':
          st.header("Distribution of Rating based on Snickers Product")
          snk_percent = (df[['b_Snickers', 'Rating', 'Gender']].groupby('b_Snickers')['Rating'].count() / len(df['b_Snickers']) * 100).round(2)
          fig = px.bar(snk_percent)
          st.plotly_chart(fig,use_container_width=True)
          st.header("Summary")
          ac=df.groupby(['b_Snickers', 'Gender'])['Rating'].aggregate(['count','mean','median','min', 'max'])
          st.table(ac)
         elif options1 == 'Galaxy':
          st.header("Distribution of Rating based on Galaxy Product")
          gal_percent = (df[['b_Galaxy ', 'Rating', 'Gender']].groupby('b_Galaxy ')['Rating'].count() / len(df['b_Galaxy ']) * 100).round(2)
          fig = px.bar(gal_percent)
          st.plotly_chart(fig,use_container_width=True)
          st.header("Summary")
          gb=df.groupby(['b_Galaxy ', 'Gender'])['Rating'].aggregate(['count','mean','median','min', 'max'])
          st.table(gb)
if selected =='Types':
    st.header("")
    tab1, tab2, tab3  = st.tabs(['ChocolateType','Variety','Flavour'])
    with tab1:
     st.header("Distribution of Rating based on Chocolate Type")
     fig = px.bar(df, x="Gender", y="Rating", color=' Type ', barmode="group",facet_col="Age")
     st.plotly_chart(fig,use_container_width=True)
     st.header("Summary")
     ac=df.groupby([' Type ', 'Gender','Age'])['Rating'].aggregate(['count','mean','median','min', 'max'])
     st.table(ac)
    with tab2:
     st.header("Distribution of Rating based on Chocolate Variety")
     fig = px.bar(df, x="Gender", y="Rating", color='Variety', barmode="group",facet_col="Age" )
     st.plotly_chart(fig,use_container_width=True)
     st.header("Summary")
     ac=df.groupby(['Variety', 'Gender','Age'])['Rating'].aggregate(['count','mean','median','min', 'max'])
     st.table(ac)
    with tab3:
     st.header("Distribution of Rating based on Chocolate Flavour")
     fig = px.bar(df, x="Gender", y="Rating", color='Flavour', barmode="group",facet_col="Age" )
     st.plotly_chart(fig,use_container_width=True)
     st.header("Summary")
     ac=df.groupby(['Flavour', 'Gender','Age'])['Rating'].aggregate(['count','mean','median','min', 'max'])
     st.table(ac)

if selected =='Preference':
    st.header("")
    options=st.selectbox('**Select the variable**', ["Size","Purchase","P_day","Buying","S_Week","C_Stock"])
    if options == 'Size':
     st.header("Distribution of Rating by preference in size")
     st.sidebar.header("Please Filter Here:")
     df_selection = st.sidebar.multiselect("Select the Age:",
                   options=df["Age"].unique(),
                   default=df["Age"].unique())
     mask = df['Age'].isin(df_selection)
     fig = px.box(df[mask], x=' Size', y='Rating',color='Gender')
     st.plotly_chart(fig,use_container_width=True)
     st.header("Summary")
     ac=df.groupby(['Gender',' Size'])['Rating'].aggregate(['count','mean','median','min', 'max'])
     st.table(ac)
    elif options == 'Purchase':
     st.header("Distribution of Rating by preference in Purchase")
     st.sidebar.header("Please Filter Here:")
     df_selection = st.sidebar.multiselect("Select the Age:",
                   options=df["Age"].unique(),
                   default=df["Age"].unique())
     mask = df['Age'].isin(df_selection)
     fig = px.box(df[mask], x='Purchase ', y='Rating',color='Gender')
     st.plotly_chart(fig,use_container_width=True)
     st.header("Summary")
     ac=df.groupby(['Gender','Purchase '])['Rating'].aggregate(['count','mean','median','min', 'max'])
     st.table(ac)
    elif options == 'P_day':
     st.header("Distribution of Rating by preference Per day")
     st.sidebar.header("Please Filter Here:")
     df_selection = st.sidebar.multiselect("Select the Age:",
                   options=df["Age"].unique(),
                   default=df["Age"].unique())
     mask = df['Age'].isin(df_selection)
     fig = px.box(df[mask], x='P_day ', y='Rating',color='Gender')
     st.plotly_chart(fig,use_container_width=True)
     st.header("Summary")
     ac=df.groupby(['Gender','P_day '])['Rating'].aggregate(['count','mean','median','min', 'max'])
     st.table(ac)
    elif options == 'Buying':
     st.header("Distribution of Rating by preference in buying")
     st.sidebar.header("Please Filter Here:")
     df_selection = st.sidebar.multiselect("Select the Age:",
                   options=df["Age"].unique(),
                   default=df["Age"].unique())
     mask = df['Age'].isin(df_selection)
     fig = px.box(df[mask], x='Buying ', y='Rating',color='Gender')
     st.plotly_chart(fig,use_container_width=True)
     st.header("Summary")
     ac=df.groupby(['Gender','Buying '])['Rating'].aggregate(['count','mean','median','min', 'max'])
     st.table(ac)
    elif options == 'S_Week':
     st.header("Distribution of Rating by Money Spent in a Week")
     st.sidebar.header("Please Filter Here:")
     df_selection = st.sidebar.multiselect("Select the Age:",
                   options=df["Age"].unique(),
                   default=df["Age"].unique())
     mask = df['Age'].isin(df_selection)
     fig = px.box(df[mask], x='S_Week', y='Rating',color='Gender')
     st.plotly_chart(fig,use_container_width=True)
     st.header("Summary")
     ac=df.groupby(['Gender','S_Week'])['Rating'].aggregate(['count','mean','median','min', 'max'])
     st.table(ac)
    
    elif options == 'C_Stock':
     st.header("Distribution of Rating by stock of chocolates")
     st.sidebar.header("Please Filter Here:")
     df_selection = st.sidebar.multiselect("Select the Age:",
                   options=df["Age"].unique(),
                   default=df["Age"].unique())
     mask = df['Age'].isin(df_selection)
     fig = px.box(df[mask], x='C_Stock', y='Rating',color='Gender')
     st.plotly_chart(fig,use_container_width=True)
     st.header("Summary")
     ac=df.groupby(['Gender','C_Stock'])['Rating'].aggregate(['count','mean','median','min', 'max'])
     st.table(pd.DataFrame(ac))
     st.write(ac.index.names[0], ac.index.names[1])
if selected =='Feedback':
    st.header("")
    options2=st.selectbox('Select the Brand Rating Variable', ["Cadbury",'Nestle','Snickers','Galaxy'], key="options2")
    if options2 == 'Cadbury':
      st.header("Rating vs Cadbury Product & Cadbury Rating")
      st.sidebar.header("Please Filter Here:")
      df_selection = st.sidebar.multiselect("Select the Age:",
                   options=df["Age"].unique(),
                   default=df["Age"].unique())
      mask = df['Age'].isin(df_selection)
      fig = px.bar(df[mask], x='cbr_Cadbury', y='Rating',color='b_Cadbury',facet_col='Gender')
      st.plotly_chart(fig,use_container_width=True)
      st.header("Summary")
      c=df.groupby(['b_Cadbury','cbr_Cadbury','Age'])['Rating'].aggregate(['mean','min', 'max','median','count'])
      st.table(c)
      
    elif options2 == 'Nestle':
      st.header("Rating vs Nestle Product & Nestle Rating")
      st.sidebar.header("Please Filter Here:")
      df_selection = st.sidebar.multiselect("Select the Age:",
                   options=df["Age"].unique(),
                   default=df["Age"].unique())
      mask = df['Age'].isin(df_selection)
      fig = px.bar(df[mask], x='cbr_Nestle ', y='Rating', color='b_Nestle ', facet_col='Gender')
      st.plotly_chart(fig,use_container_width=True)
      st.header("Summary")
      n=df.groupby(['b_Nestle ','cbr_Nestle ','Age',])['Rating'].aggregate(['mean','min', 'max','median','count'])
      st.table(n) 
    elif options2 == 'Snickers':
      st.header("Rating vs Snickers Product & Snickers Rating")
      st.sidebar.header("Please Filter Here:")
      df_selection = st.sidebar.multiselect("Select the Age:",
                   options=df["Age"].unique(),
                   default=df["Age"].unique())
      mask = df['Age'].isin(df_selection)
      fig = px.bar(df[mask], x='cbr_Snickers ', y='Rating', color='b_Snickers', facet_col='Gender')
      st.plotly_chart(fig,use_container_width=True)
      st.header("Summary")
      s=df.groupby(['b_Snickers','cbr_Snickers ','Age',])['Rating'].aggregate(['mean','min', 'max','median','count'])
      st.table(s)
    elif options2 == 'Galaxy':
      st.header("Rating vs Galaxy Product & Galaxy Rating")
      st.sidebar.header("Please Filter Here:")
      df_selection = st.sidebar.multiselect("Select the Age:",
                   options=df["Age"].unique(),
                   default=df["Age"].unique())
      mask = df['Age'].isin(df_selection)
      fig = px.bar(df[mask], x='cbr_Galaxy ', y='Rating',color='b_Galaxy ',facet_col='Gender')
      st.plotly_chart(fig,use_container_width=True)
      st.header("Summary")
      g=df.groupby(['b_Galaxy ','cbr_Galaxy ','Age'])['Rating'].aggregate(['mean','min', 'max','median','count'])
      st.table(g)
        

