import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='Survey Results')
st.header('Survey Results 2021')
st.subheader('Ketul Here!! Created first web APPLICATION')

###------- Load dataframe from Excel

excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(excel_file,
                    sheet_name=sheet_name,
                    usecols='B:D',
                    header=3)

df_participants = pd.read_excel(excel_file,
                                sheet_name=sheet_name,
                                usecols='F:G',
                                header=3)
df_participants.dropna(inplace=True)


department = df['Department'].unique().tolist()
ages = df['Age'].unique().tolist()

age_selection = st.slider('Age:',
                        min_value=min(ages),
                        max_value=max(ages),
                        value=(min(ages),max(ages)))

department_selection = st.multiselect('department:',
                                        department,
                                        default=department)


###---Filter dataframe based on selection ------##

mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

###---Group dataframe after selection ------##

df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age':'Votes'})
df_grouped = df_grouped.reset_index()

###---- Plot the bas chart ------##

bar_chart = px.bar(df_grouped,
                    x="Rating",
                    y='Votes',
                    text='Votes',
                    color_discrete_sequence=['#F63366']*len(df_grouped),
                    template='plotly_white')

st.plotly_chart(bar_chart)

###------- Display Image and piechart and dataframe ---###

col1,col2 = st.columns(2)

col1.dataframe(df[mask])

image = Image.open('Images/survey.jpg')
col2.image(image,
        caption='Image Downloaded from Freepik',
        use_column_width=True)


###-----Plot Pie chart-----####

pie_chart = px.pie(df_participants,
                    title="<b>Total No. of Participants",
                    values="Participants",
                    names='Departments')
st.plotly_chart(pie_chart)


