######### Import your libraries #######
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly as py
import plotly.graph_objs as go


###### Define your variables #####
tabtitle = 'Titanic!'
color1='#92A5E8'
color2='#8E44AD'
color3='#FFC300'
sourceurl = 'https://www.kaggle.com/c/titanic'
githublink = 'https://github.com/cryswong26/304-titanic-dropdown'


###### Import a dataframe #######
df = pd.read_csv("https://raw.githubusercontent.com/austinlasseter/plotly_dash_tutorial/master/00%20resources/titanic.csv")
#df['Female']=df['Sex'].map({'male':0, 'female':1})
#df['Cabin Class'] = df['Pclass'].map({1:'first', 2: 'second', 3:'third'})
#variables_list=['Survived', 'Female', 'Fare', 'Age']
variables_list=['Sex', 'Pclass', 'Embarked'] #just the ones that don't need grouping for now
#, 'Age (group)', 'Fare (group)'] #added one variable 

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

####### Layout of the app ########
app.layout = html.Div([
    html.H3('What % of each group survived the Titanic? Choose a variable'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in variables_list],
        value=variables_list[0] #starting value is the first value in the list - "Survived"
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
])


######### Interactive callbacks go here #########
@app.callback(Output('display-value', 'figure'), #these are both defined above and below
              [Input('dropdown', 'value')]) #defined above
def display_value(continuous_var): #the dropdown variable
    #grouped_mean=df.groupby(['Cabin Class', 'Embarked'])[continuous_var].mean()
    grouped_mean=df.groupby(continuous_var,as_index=False).Survived.mean()
    results=pd.DataFrame(grouped_mean)
    
    # Create a bar chart
    mydata1 = go.Bar(
        #results,
        #results,
        #x=results.loc['first'].index, 
        x=continuous_var,
        #y=results.loc['first'][continuous_var], 
        #y=results
        y=results.loc[grouped_mean][continuous_var],
        #name='First Class',
        marker=dict(color=color1) #these colors are set above; change them to whatever i want
    )
    mydata2 = go.Bar(
        #results,
        #results,
        #x=results.loc['second'].index,
        #y=results.loc['second'][continuous_var],
        x=continuous_var,
        y=results.loc[grouped_mean][continuous_var],
        #name='Second Class',
        marker=dict(color=color2)
    )
    mydata3 = go.Bar(
        #results,
        #x=results.loc['third'].index,
        #y=results.loc['third'][continuous_var],
        x=continuous_var,
        y=results.loc[grouped_mean][continuous_var],
        #name='Third Class',
        marker=dict(color=color3)
    )

    mylayout = go.Layout(
        title='Bar Chart',
        #xaxis = dict(title = 'Port of Embarkation'), # x-axis label
        #yaxis = dict(title = str(continuous_var)), # y-axis label
        xaxis = dict(title = str(continuous_var)), # x-axis label
        yaxis = dict(title = '% Survived'), # y-axis label

    )
    fig = go.Figure(data=[mydata1, mydata2, mydata3], layout=mylayout)
    return fig


######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
