import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

data1 = pd.read_csv('athlete_events.csv')
data2 = pd.read_csv('noc_regions.csv')

data1 = preprocessor.process(data1, data2)

st.sidebar.title("Olympics Analysis")

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Analysis', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)


st.dataframe(data1)

if user_menu == 'Medal Analysis':
    st.sidebar.header('Medal Analysis')
    years, nation = helper.nation_year_list(data1)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_nation = st.sidebar.selectbox("Select Country", nation)

    medal_count1 = helper.fetch_medal_tally(data1,selected_year,selected_nation)
    st.dataframe(medal_count1)

if user_menu == 'Overall Analysis':
    editions = data1['Year'].unique().shape[0]-1
    cities = data1['City'].unique().shape[0]
    sports = data1['Sport'].unique().shape[0]
    events = data1['Event'].unique().shape[0]
    athlete = data1['Name'].unique().shape[0]
    country = data1['region'].unique().shape[0]

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Host")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)


    col1, col2, col3 = st.columns(3)
    with col1:
         st.header("Events")
         st.title(events)

    with col2:
        st.header("Nations")
        st.title(country)

    with col3:
        st.header("Athletes")
        st.title(athlete)


    st.title("No. of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = data1.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = data1['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(data1,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(data1,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)



if user_menu == 'Athlete wise Analysis':
    athlete_df = data1.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = data1['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(data1, selected_sport)

    # Scatter plot
    fig, ax = plt.subplots()
    sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=60, ax=ax)
    st.pyplot(fig)

    # Pie chart
    medal_counts = temp_df['Medal'].value_counts().reset_index()
    medal_counts.columns = ['Medal', 'count']
    pie_fig = px.pie(medal_counts, values='count', names='Medal', title='Medal Distribution')

    st.plotly_chart(pie_fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(data1)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
