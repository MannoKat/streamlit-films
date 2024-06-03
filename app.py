import pandas as pd
import streamlit as st
import plotly.express as px
import datetime

# Load the dataset
file_path = "/datasets/IMDB Top 250 Movies.csv"
df = pd.read_csv(file_path)

# Select the relevant columns
selected_columns = ['rank', 'name', 'rating', 'genre', 'certificate', 'year', 'budget', 'run_time']
df_selected = df[selected_columns].copy()

# Convert budget values to billions
def convert_to_billions(budget_str):
    if pd.isna(budget_str):
        return None
    budget_str = budget_str.replace('$', '').replace(',', '')
    try:
        budget = float(budget_str)
        return budget / 1e9
    except ValueError:
        return None

df_selected.loc[:, 'budget'] = df_selected['budget'].apply(convert_to_billions)

# Create a new DataFrame with split genres
df_genres_expanded = df_selected.assign(genre=df_selected['genre'].str.split(',')).explode('genre')
df_genres_expanded['genre'] = df_genres_expanded['genre'].str.strip()

# Sidebar
with st.sidebar:
    st.markdown("Author: **Your Name**")  # Change name of author here
    st.write("Date: ", datetime.date.today())
    st.text("Description: This app analyzes the IMDb Top 250 Movies dataset.")

# Main content
st.title("Rating Films")
st.markdown("This application allows you to analyze the IMDb Top 250 Movies dataset.")
st.divider()

# Display dataset information
st.header("Dataset Information")
st.markdown(
"""
- **Description**: This dataset stores information about the IMDb Top 250 Movies including their genres, ratings, and other relevant details.
- **Variables**:
    1. **rank**: The rank of the movie.
    2. **name**: The name of the movie.
    3. **rating**: The IMDb rating of the movie.
    4. **genre**: The genre(s) of the movie.
    5. **certificate**: The certification of the movie.
    6. **year**: The release year of the movie.
    7. **budget**: The budget of the movie (in billions).
    8. **run_time**: The runtime of the movie.
"""
)

# Display the original dataset
st.dataframe(df_selected, width=1000)

st.header("Rating of Films Analysis by Selected Category")
st.text("----")

tab1, tab2 = st.tabs(["General relation", "Trending films in year"])

with tab1:
    col1, col2 = st.columns([1, 3])

    with col1:
        category_mapping = {
            'genre': 'Genre',
            'budget': 'Budget (in billions)',
            'certificate': 'Certificate',
            'run_time': 'Run Time',
        }
        by_what = st.radio(
            "Choose a category:",
            ['genre', 'budget', 'certificate', 'run_time'],
            format_func=lambda x: category_mapping[x],
            key="r1"
        )
        
        chart_type = st.radio(
            "Choose a chart type:",
            ['Bar Chart', 'Line Chart', 'Scatter Plot', 'Box Plot'],
            key="chart_type"
        )
        
    with col2:
        if chart_type == 'Bar Chart':
            fig = px.bar(df_genres_expanded, x=by_what, y="rating", color=by_what,
                         labels={by_what: category_mapping[by_what], "rating": "Rating"},
                         title=f"Film Rating by {category_mapping[by_what]}")
        elif chart_type == 'Line Chart':
            fig = px.line(df_genres_expanded, x=by_what, y="rating", color=by_what,
                          labels={by_what: category_mapping[by_what], "rating": "Rating"},
                          title=f"Film Rating by {category_mapping[by_what]}")
        elif chart_type == 'Scatter Plot':
            fig = px.scatter(df_genres_expanded, x=by_what, y="rating", color=by_what,
                             labels={by_what: category_mapping[by_what], "rating": "Rating"},
                             title=f"Film Rating by {category_mapping[by_what]}")
        elif chart_type == 'Box Plot':
            fig = px.box(df_genres_expanded, x=by_what, y="rating", color=by_what,
                         labels={by_what: category_mapping[by_what], "rating": "Rating"},
                         title=f"Film Rating by {category_mapping[by_what]}")
        
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with tab2:
    year = st.slider("Select a year:", min_value=1920, max_value=2021, value=2020, step=1, key="year")
    df_year1 = df_genres_expanded[df_genres_expanded['year'] == year]
    df_year = df_selected[df_selected['year'] == year]

                
    st.markdown(f"**Top movies in {year}:**")
    st.dataframe(df_year[['rank', 'name', 'rating', 'genre']].head(), width=1000)
    popular_genres_year = df_year1['genre'].value_counts().nlargest(10)  # Get top 10 genres for the selected year
    st.write(f"**Number of Films by Genre in {year}:**")
    col1, col2 = st.columns([7, 8])

    with col1:
        if not df_year1.empty:
            
            fig_year_bar = px.bar(popular_genres_year, x=popular_genres_year.index, y=popular_genres_year.values,
                                labels={'x': 'Genre', 'y': 'Number of Films'})
            st.plotly_chart(fig_year_bar, theme="streamlit", use_container_width=True)
        else:
            st.write(f"No films available for the selected year {year}.")
            
    with col2:
        if not df_year1.empty:
            
            fig_year_pie = px.pie(popular_genres_year, values=popular_genres_year.values, names=popular_genres_year.index)
            st.plotly_chart(fig_year_pie, theme="streamlit", use_container_width=True)

        else:
            st.write(f"No films available for the selected year {year}.")
            
