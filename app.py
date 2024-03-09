import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt


data_frame = pd.read_csv("startup_cleaned.csv")
st.set_page_config(layout='wide', page_title='Startup Analysis')
st.title("Isha Mathkar-FS23AI016")
# to convert 'date' column to datetime format and extract month and year
data_frame['date']=pd.to_datetime(data_frame['date'],errors='coerce')
data_frame['month']=data_frame['date'].dt.month
data_frame['year']=data_frame['date'].dt.year

#INVESTOR
# defining a function to display details of a selected investor
def dis_invest_details(inv):
    st.title(inv)
    st.subheader('Most Recent Investments')
#to show the last five investments
    last_five = data_frame[data_frame['investors'].str.contains(inv, na=False)].head(5)[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.dataframe(last_five)
# to find the startup where the investor made the maximum investment
    st.subheader('Maximum Investment')
    max_inv = data_frame[data_frame['investors'].str.contains(inv, na=False)].groupby('startup')['amount'].sum().sort_values(
        ascending=False).head(1)
    st.dataframe(max_inv)
#columns
    col1, col2, col3 = st.columns(3)
    with col1:
        big_series = data_frame[data_frame['investors'].str.contains(inv, na=False)].groupby('startup')[
            'amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_ser = data_frame[data_frame['investors'].str.contains(inv, na=False)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_ser, labels=vertical_ser.index, autopct="0.01f%%")

        st.pyplot(fig1)

    with col3:
        # Corrected the line below, changed square brackets to parentheses
        new_city = data_frame[data_frame['investors'].str.contains(inv, na=False)].groupby('city')['amount'].sum()
        st.subheader('City-Wise')
        fig2, ax2 = plt.subplots()
        ax2.pie(new_city, labels=new_city.index)

        st.pyplot(fig2)
#to show sub-vertical data
    sub1 = data_frame[data_frame['investors'].str.contains(inv, na=False)].groupby('subvertical')['amount'].sum()
    col1.subheader('Subvertical Data')
    fig3, ax3 = plt.subplots()
    ax3.bar(sub1.index, sub1.values)
    col1.pyplot(fig3)
#to display the yearly investment of the investor
    data_frame['date'] = pd.to_datetime(data_frame['date'])
    data_frame['year'] = data_frame['date'].dt.year
    sub2 = data_frame[data_frame['investors'].str.contains(inv, na=False)].groupby('year')['amount'].sum()
    col2.subheader('Yearly Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(sub2.index, sub2.values)
    col2.pyplot(fig2)

#to display the investments by the round
    rounds = data_frame[data_frame['investors'].str.contains('3one4 Capital', na=False)].groupby('round')['amount'].sum()
    col3.subheader('Round-Wise')
    fig3, ax3 = plt.subplots()
    ax3.bar(rounds.index, rounds.values)
    col3.pyplot(fig3)

#OVERALL ANALYSIS
#defining a function to display the overall analysis
def overall():
    st.title('Overall-Analysis')
#to find the maximum amount
    total = round(data_frame['amount'].sum())

    max_funding = data_frame.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    avg_funding = data_frame.groupby('startup')['amount'].sum().mean()
    num_startups = data_frame['startup'].nunique()
#columns
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total',str(total) + 'Cr')
    with col2:
        st.metric('Max',str(max_funding)+'Cr')
    with col3:
        st.metric('Avg',str(round(avg_funding))+'Cr')

    with col4:
        st.metric('Founded Startups',num_startups)

#to dispplay the MOM Chart
    st.header('M.O.M Chart')
    selected_opt = st.selectbox('select type',[' Total','Count'])
    if selected_opt== 'Total':
        temp_df = data_frame.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = data_frame.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig3,ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'],temp_df['amount'])

    st.pyplot(fig3)

#to find the top 3 industries
    st.header('Sector Analysis')
    st.subheader("Top 3 Industries")
    top_verticals = data_frame['vertical'].value_counts().head(3)
    fig, ax = plt.subplots()
    top_verticals.plot(kind='pie', ax=ax)
    st.pyplot(fig)


    st.header('City Wise funding')
# groupby city , total investment amounts & filling missing values with 0
    tot_inv_city = data_frame.groupby('city')['amount'].sum().fillna(0)
# sort the result by total investment amount
    tot_inv_city = tot_inv_city.sort_values(ascending=False)
# reset index to make city a column a
    tot_inv_city = tot_inv_city.reset_index()


#to display the total investment made by the city
    st.subheader('Total Investment by City')
# plot pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie( tot_inv_city['amount'], labels=tot_inv_city['city'], autopct='%1.1f%%')
    ax.set_title('Total Investment by City')
    ax.axis('equal')  # equal aspect ratio  to ensure that the pie is a circle.
# display the plot
    st.pyplot(fig)

#to find the max investment amount for each investor

    data_frame['date'] = pd.to_datetime(data_frame['date'])

 # extract year from the date col
    data_frame['year'] = data_frame['date'].dt.year

    top_startups_yearly = data_frame.groupby(['year'])['startup'].agg(lambda x: x.value_counts().idxmax()).reset_index()


#bar graph
    st.title('Top Startup Year-Wise Overall')
#plot
    fig, ax = plt.subplots()
    ax.bar(top_startups_yearly['year'], top_startups_yearly['startup'], color='skyblue')
    ax.set_xlabel('Year')
    ax.set_ylabel('Top Startup')
    ax.set_title('Top Startup Each Year Overall')
# rotating labels for better readability
    plt.xticks(rotation=45)
#display
    st.pyplot(fig)

#to find teh top investors
    st.title("Top Investors")
# investment amounts for each investor
    investor_totals = data_frame.groupby('investors')['amount'].sum().reset_index()
# rank investors based on total investment amount
    investor_totals = investor_totals.sort_values(by='amount', ascending=False)

    top_investors = investor_totals.head(10)
# plot the chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(top_investors['amount'], labels=top_investors['investors'], autopct='%1.1f%%')
    ax.set_title('Top Investors')
    ax.axis('equal')
    st.pyplot(fig)
#to display the funding heatmap
    st.subheader('Funding Heatmap')
    heatmap_data = data_frame.pivot_table(values='amount', index='year', columns='month', aggfunc='sum')
    fig10, ax10 = plt.subplots()
    cax = ax10.matshow(heatmap_data, cmap='viridis')
    fig10.colorbar(cax)
    ax10.set_xticks(range(len(heatmap_data.columns)))
    ax10.set_xticklabels(heatmap_data.columns, rotation=45)
    ax10.set_yticks(range(len(heatmap_data.index)))
    ax10.set_yticklabels(heatmap_data.index)
    st.pyplot(fig10)

#STARTUP DETAILS
def startup_details(startup_name):
    st.header('Founders:')
#display the founders
    old_data_frame = data_frame[data_frame['startup'] == startup_name]
    int1 = old_data_frame['investors']
    investors_data_frame = pd.DataFrame(int1, columns=['investors']).reset_index()
#Display
    st.write(investors_data_frame)
#columns
    col1, col2 = st.columns(2)

    with col1:
        st.title('Industry')
        industry_data = data_frame[data_frame['startup'].str.contains(startup_name, na=False)]['vertical'].str.lower().value_counts().head()

        # Create a pie chart for 'Industry'
        fig_industry, ax_industry = plt.subplots()
        ax_industry.pie(industry_data, labels=industry_data.index, autopct='%1.1f%%', startangle=90)
        ax_industry.set_title('Industry Distribution')

        # Display the pie chart using Streamlit
        st.pyplot(fig_industry)

    with col2:
        st.title('Sub-Industry')
        sub_industry_data = data_frame[data_frame['startup'].str.contains(startup_name, na=False)]['subvertical'].str.lower().value_counts().head()

        # Create a pie chart for 'Sub-Industry'
        fig_subindustry, ax_subindustry = plt.subplots()
        ax_subindustry.pie(sub_industry_data, labels=sub_industry_data.index, autopct='%1.1f%%', startangle=90)
        ax_subindustry.set_title('Sub-Industry Distribution')

        # Display the pie chart using Streamlit
        st.pyplot(fig_subindustry)

#to display city pie chart
    st.title('City')
    city_data = data_frame[data_frame['startup'].str.contains(startup_name, na=False)].groupby('startup')['city'].value_counts().head()

# create a chart
    fig_city, ax_city = plt.subplots()
    ax_city.pie(city_data, labels=city_data.index, autopct='%1.1f%%', startangle=90)
    ax_city.set_title('City Distribution')

# display
    st.pyplot(fig_city)

    st.header('Funding Rounds')
    fund_rnds_info = data_frame[['round', 'investors', 'date']].sort_values('date', ascending=False)
    st.dataframe(fund_rnds_info)




#to run the code as per the selection of the the user
# st.dataframe(df)
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    overall()


elif option == 'Startup':
    st.title("Startup Analysis")
    select_start=selected_investor = st.sidebar.selectbox('Select One',
                                             sorted(set(data_frame['startup'].astype(str).str.split(',').sum())))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        st.title(select_start)
        startup_details(select_start)

else:
    st.title('Investor')
    selected_investor = st.sidebar.selectbox('Select One',
                                             sorted(set(data_frame['investors'].astype(str).str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investors Details')
    if btn2:
       dis_invest_details(selected_investor)



