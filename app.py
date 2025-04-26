
import pandas as pd
import plotly.express as px
import streamlit as st

# Page configuration
st.set_page_config(layout='wide', page_title='📊 Supermarket Sales EDA', page_icon='🛒')

# Load the dataset
@st.cache_data

def load_data():
    df = pd.read_csv('supermarket_sales - Sheet1.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Time'] = pd.to_datetime(df['Time']).dt.time
    return df

supermarket = load_data()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio('Select Page:', ['Dataset Overview', 'Univariate Analysis', 'Bivariate Analysis', 'Multivariate Analysis', 'Statistical Questions', 'Filter by Date & City'])

# ======================= Dataset Overview =======================
if page == 'Dataset Overview':
    st.title('🧾 Supermarket Dataset Overview')
    st.subheader('Raw Data Preview')
    st.dataframe(supermarket)

    st.subheader("Basic Information")
    st.write("Number of Rows:", supermarket.shape[0])
    st.write("Number of Columns:", supermarket.shape[1])
    st.write("Column Types:")
    st.write(supermarket.dtypes)

    st.subheader("Missing Values")
    st.write(supermarket.isnull().sum())

# ======================= Univariate Analysis =======================
elif page == 'Univariate Analysis':
    st.title('📌 Univariate Analysis')
    question = st.selectbox('Choose a Question:', [
        'Distribution of Unit Prices',
        'Frequency of Payment Methods',
        'Distribution of Customer Ratings',
        'Most Frequently Purchased Product Line',
        'Average Quantity per Product Line'])

    if question == 'Distribution of Unit Prices':
        st.plotly_chart(px.box(supermarket, x='Unit price', title='Unit Price Distribution'))

    elif question == 'Frequency of Payment Methods':
        st.plotly_chart(px.histogram(supermarket, x='Payment', title='Payment Method Frequency'))

    elif question == 'Distribution of Customer Ratings':
        st.plotly_chart(px.box(supermarket, x='Rating', title='Customer Ratings Distribution'))

    elif question == 'Most Frequently Purchased Product Line':
        product_count = supermarket['Product line'].value_counts().reset_index()
        product_count.columns = ['Product line', 'Count']
        st.plotly_chart(px.bar(product_count, x='Product line', y='Count', title='Most Frequently Purchased Product Line'))

    elif question == 'Average Quantity per Product Line':
        avg_quantity = supermarket.groupby('Product line')['Quantity'].mean().reset_index()
        st.plotly_chart(px.bar(avg_quantity, x='Product line', y='Quantity', title='Average Quantity by Product Line'))

# ======================= Bivariate Analysis =======================
elif page == 'Bivariate Analysis':
    st.title('🔁 Bivariate Analysis')
    question = st.selectbox('Choose a Question:', [
        'Total Sales Across Product Lines',
        'Correlation Between Unit Price and Quantity',
        'Average Gross Income by Gender',
        'Relationship Between Rating and Total'])

    if question == 'Total Sales Across Product Lines':
        df = supermarket.groupby('Product line')['Total'].sum().reset_index()
        st.plotly_chart(px.bar(df, x='Product line', y='Total', title='Total Sales by Product Line'))

    elif question == 'Correlation Between Unit Price and Quantity':
        correlation = supermarket[['Unit price', 'Quantity']].corr().iloc[0,1]
        st.write(f"Correlation: {correlation:.2f}")
        st.plotly_chart(px.scatter(supermarket, x='Unit price', y='Quantity', title='Unit Price vs Quantity'))

    elif question == 'Average Gross Income by Gender':
        df = supermarket.groupby('Gender')['gross income'].mean().reset_index()
        st.plotly_chart(px.bar(df, x='Gender', y='gross income', title='Average Gross Income by Gender'))

    elif question == 'Relationship Between Rating and Total':
        st.plotly_chart(px.scatter(supermarket, x='Rating', y='Total', trendline='ols', title='Rating vs Total'))

# ======================= Multivariate Analysis =======================
elif page == 'Multivariate Analysis':
    st.title('📊 Multivariate Analysis')
    question = st.selectbox('Choose a Question:', [
        'Gross Income by City and Customer Type',
        'Unit Price, Quantity, and Total Relationship',
        'Gender Preference by Product Line and Gross Income',
        'Average Rating by Branch and Product Line',
        'Sales by Time, Payment, and Branch'])

    if question == 'Gross Income by City and Customer Type':
        st.plotly_chart(px.box(supermarket, x='City', y='gross income', color='Customer type', title='Gross Income by City and Customer Type'))

    elif question == 'Unit Price, Quantity, and Total Relationship':
        st.plotly_chart(px.scatter(supermarket, x='Unit price', y='Quantity', size='Total', color='Product line', title='Unit Price vs Quantity vs Total'))

    elif question == 'Gender Preference by Product Line and Gross Income':
        df = supermarket.groupby(['Gender', 'Product line'])['gross income'].mean().reset_index()
        st.plotly_chart(px.bar(df, x='Product line', y='gross income', color='Gender', barmode='group', title='Gross Income by Product Line & Gender'))

    elif question == 'Average Rating by Branch and Product Line':
        df = supermarket.groupby(['Branch', 'Product line'])['Rating'].mean().reset_index()
        st.plotly_chart(px.bar(df, x='Branch', y='Rating', color='Product line', barmode='group', title='Rating by Branch & Product Line'))

    elif question == 'Sales by Time, Payment, and Branch':
        df = supermarket.groupby(['Branch', 'Date', 'Payment'])['Total'].sum().reset_index()
        st.plotly_chart(px.scatter(df, x='Date', y='Total', color='Payment', facet_col='Branch', title='Sales by Date, Payment, and Branch'))

# ======================= Statistical Questions =======================
elif page == 'Statistical Questions':
    st.title('📉 Statistical Questions')
    question = st.selectbox('Select a Statistical Question:', [
        'Average Gross Income per Product Line',
        'Highest Average Total Sales by City',
        'Rating Distribution & Outliers',
        'Sales Differences by Gender',
        'Popular Payment Methods and Spending'])

    if question == 'Average Gross Income per Product Line':
        avg_income = supermarket.groupby('Product line')['gross income'].mean().reset_index()
        st.plotly_chart(px.bar(avg_income, x='Product line', y='gross income', title='Average Gross Income per Product Line'))

    elif question == 'Highest Average Total Sales by City':
        city_sales = supermarket.groupby('City')['Total'].mean().reset_index().sort_values(by='Total', ascending=False)
        st.write(city_sales)

    elif question == 'Rating Distribution & Outliers':
        st.write(supermarket['Rating'].describe())
        st.plotly_chart(px.box(supermarket, y='Rating', title='Rating Distribution'))

    elif question == 'Sales Differences by Gender':
        gender_sales = supermarket.groupby('Gender')['Total'].sum().reset_index()
        st.plotly_chart(px.bar(gender_sales, x='Gender', y='Total', title='Total Sales by Gender'))

    elif question == 'Popular Payment Methods and Spending':
        payment_stats = supermarket.groupby('Payment').agg({'Invoice ID':'count','Total':'mean'}).reset_index()
        st.write(payment_stats.sort_values(by='Invoice ID', ascending=False))

# ======================= Filter by Date & City =======================
elif page == 'Filter by Date & City':
    st.title('📆 Filter by Date & City')

    min_date = supermarket['Date'].min().date()
    max_date = supermarket['Date'].max().date()

    start_date = st.date_input('Start Date', value=min_date, min_value=min_date, max_value=max_date)
    end_date = st.date_input('End Date', value=max_date, min_value=min_date, max_value=max_date)

    cities = st.multiselect('Select Cities:', options=supermarket['City'].unique(), default=supermarket['City'].unique())

    filtered_data = supermarket[(supermarket['Date'] >= pd.to_datetime(start_date)) & 
                                (supermarket['Date'] <= pd.to_datetime(end_date)) & 
                                (supermarket['City'].isin(cities))]

    st.subheader("Filtered Data")
    st.dataframe(filtered_data)

    st.subheader("Product Line Counts in Filtered Data")
    count_df = filtered_data['Product line'].value_counts().reset_index()
    count_df.columns = ['Product line', 'Count']
    st.plotly_chart(px.bar(count_df, x='Product line', y='Count', title='Product Line Count'))

