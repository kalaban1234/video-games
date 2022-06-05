import dash
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import dcc
from dash import html
from plotly.offline import iplot

# Dataset 'Processing'
df = pd.read_csv('https://raw.githubusercontent.com/kalaban1234/video-games/main/video_games_sales.csv')
df = df.dropna()
df['User_Score'] = df.User_Score.astype('float64', copy=False)
df['Year_of_Release'] = df.Year_of_Release.astype('int64', copy=False)
df['User_Count'] = df.User_Count.astype('int64', copy=False)
df['Critic_Count'] = df.Critic_Count.astype('int64', copy=False)

# Building Graphs
# Let's build a sales chart for video games in different countries depending on the year.
publ_sls = df.groupby(['Year_of_Release', 'Publisher']).Global_Sales.sum().reset_index()
publ_yr_sls = publ_sls.groupby('Year_of_Release').Global_Sales.max().reset_index()
Yr_Sls = df.iloc[:, [2, 0, 9]].groupby(['Year_of_Release']).Global_Sales.max().reset_index()
Gm_yr_Sls = df[['Name', 'Global_Sales', 'Year_of_Release']]
Gm_of_Yr = pd.merge(Yr_Sls, Gm_yr_Sls, on=['Year_of_Release', 'Global_Sales'], how='left')
Pub_of_Yr = pd.merge(publ_yr_sls, publ_sls, on=['Year_of_Release', 'Global_Sales'], how='left')
trace0 = go.Scatter(
    x=df.groupby(df['Year_of_Release'].sort_values()).sum().drop(['Year_of_Release'], axis=1).reset_index()[
        'Year_of_Release'],
    y=df.groupby(df['Year_of_Release'].sort_values()).sum().drop(['Year_of_Release'], axis=1).reset_index()['NA_Sales'],
    mode='lines+markers',
    name='North America Sales',
    marker=dict(size=8),
    line=dict(color='#FA8072', width=2.5),
    text=Pub_of_Yr['Publisher'],
    hovertemplate='<i>Year: %{x}</i>'
                  '<br><i>Sales: %{y} </i>')
trace1 = go.Scatter(
    x=df.groupby(df['Year_of_Release'].sort_values()).sum().drop(['Year_of_Release'], axis=1).reset_index()[
        'Year_of_Release'],
    y=df.groupby(df['Year_of_Release'].sort_values()).sum().drop(['Year_of_Release'], axis=1).reset_index()['EU_Sales'],
    mode='lines+markers',
    name='Europe Sales',
    marker=dict(size=8),
    line=dict(color='#6495ED', width=2.5),
    text=Pub_of_Yr['Publisher'],
    hovertemplate='Year: %{x}'
                  '<br><i>Sales: %{y} </i>')
trace2 = go.Scatter(
    x=df.groupby(df['Year_of_Release'].sort_values()).sum().drop(['Year_of_Release'], axis=1).reset_index()[
        'Year_of_Release'],
    y=df.groupby(df['Year_of_Release'].sort_values()).sum().drop(['Year_of_Release'], axis=1).reset_index()['JP_Sales'],
    mode='lines+markers',
    name='Japan Sales',
    marker=dict(size=8),
    line=dict(color='yellowgreen', width=2.5),
    text=Pub_of_Yr['Publisher'],
    hovertemplate='<i>Year: %{x}</i>'
                  '<br><i>Sales: %{y} </i>')
trace3 = go.Scatter(
    x=df.groupby(df['Year_of_Release'].sort_values()).sum().drop(['Year_of_Release'], axis=1).reset_index()[
        'Year_of_Release'],
    y=df.groupby(df['Year_of_Release'].sort_values()).sum().drop(['Year_of_Release'], axis=1).reset_index()[
        'Other_Sales'],
    mode='lines+markers',
    name='Other Country Sales',
    marker=dict(size=8),
    line=dict(color='#DAA520', width=2.5),
    text=Pub_of_Yr['Publisher'],
    hovertemplate='<i>Year: %{x}</i>'
                  '<br><i>Sales: %{y} </i>')

data = [trace0, trace1, trace2, trace3]
layout = dict(legend=dict(x=-0.04, y=1.09, font=dict(size=10)), legend_orientation="h",
              title="Sales of Games in different regions over the Years",
              xaxis=dict(tickmode='linear', tickangle=-90, tickfont=dict(size=10), title="Year of Release", tickwidth=5,
                         ticklen=8, zeroline=False, gridcolor="white"),
              yaxis=dict(title="Gross Sales in Different Countries", gridcolor="#DCDCDC")
              )

sales_by_regions = go.Figure(data=data, layout=layout)
iplot(sales_by_regions)

# Let's build a line plot with the dynamics of the number of released games and their sales by year.
global_sales_years_df = df.groupby('Year_of_Release')[['Global_Sales']].sum()
released_years_df = df.groupby('Year_of_Release')[['Name']].count()
years_df = global_sales_years_df.join(released_years_df)
years_df.columns = ['Global_Sales', 'Number_of_Games']
trace0 = go.Scatter(
    x=years_df.index,
    y=years_df.Global_Sales,
    mode='lines+markers',
    name='Global Sales',
    marker=dict(size=8),
    line=dict(color='#FA8072', width=2.5),
    text=years_df.Global_Sales,
    hovertemplate='<i>Year</i>: %{x}'
                  '<br><i>Global_Sales</i>: %{text}<br>'
)

trace1 = go.Scatter(
    x=years_df.index,
    y=years_df.Number_of_Games,
    mode='lines+markers',
    name='Number of games released',
    marker=dict(size=8),
    line=dict(color='#6495ED', width=2.5),
    text=years_df.Number_of_Games,
    hovertemplate='<i>Year</i>: %{x}'
                  '<br><i>Number of Games</i>: %{text}<br>'
)

data = [trace0, trace1]
layout = {'title': 'Statistics of video games'}

released_games = go.Figure(data=data, layout=layout)

# Let's build a bar chart that depict the market share of gaming platforms,
# calculated by the number of games released and by total revenue.
global_sales_platforms_df = df.groupby('Platform')[['Global_Sales']].sum()
released_platforms_df = df.groupby('Platform')[['Name']].count()
platforms_df = global_sales_platforms_df.join(released_platforms_df)

platforms_df.columns = ['Global_Sales', 'Number_of_Games']
platforms_df.sort_values('Global_Sales', inplace=True)
platforms_df = platforms_df.apply(lambda x: 100 * x / platforms_df.sum(), axis=1)

trace0 = go.Bar(
    x=platforms_df.index,
    y=platforms_df.Global_Sales,
    name='Global Sales',
    orientation='v'
)

trace1 = go.Bar(
    x=platforms_df.index,
    y=platforms_df.Number_of_Games,
    name='Number of games released',
    orientation='v'
)

data = [trace0, trace1]
layout = {'title': 'Platforms share'}

fig2 = go.Figure(data=data, layout=layout)

# Let's look at the differences in critics' ratings depending on the genre of the game.
# data = []
#
# for genre in df.Genre.unique():
#     data.append(
#         go.Box(y=df[df.Genre == genre].Critic_Score,
#                name=genre)
#     )
# fig3 = iplot(data, show_link = False)

# Let's plot the dependence of the average user rating and critics' rating by genre
scores_genres_df = df.groupby('Genre')[['Critic_Score', 'User_Score']].mean()
sales_genres_df = df.groupby('Genre')[['Global_Sales']].sum()

genres_df = scores_genres_df.join(sales_genres_df)

trace0 = go.Scatter(
    x=genres_df.Critic_Score,
    y=genres_df.User_Score,
    mode='markers+text',
    text=genres_df.index,
    textposition='bottom center',
    marker=dict(
        size=1 / 10 * genres_df.Global_Sales,
        color=[
            'aqua', 'azure', 'beige', 'lightgreen',
            'lavender', 'lightblue', 'pink', 'salmon',
            'wheat', 'ivory', 'silver'
        ]
    )
)

data = [trace0]
layout = {
    'title': 'Statistics of video games genres',
    'xaxis': {'title': 'Critic Score'},
    'yaxis': {'title': 'User Score'}
}

fig4 = go.Figure(data=data, layout=layout)

# Let's build histograms of the distributions of user ratings by genre.
traces = []
for genre in ['Racing', 'Shooter', 'Sports', 'Action']:
    traces.append(
        go.Histogram(
            x=df[df.Genre == genre].User_Score,
            histnorm='probability',
            name=genre,
            visible=(genre == 'Racing'))
    )

layout = go.Layout(
    title='User Score Distribution',
    updatemenus=list([
        dict(
            x=-0.05,
            y=1,
            yanchor='top',
            buttons=list([
                dict(
                    args=['visible', [True] + [False] * 3],
                    label='Racing',
                    method='restyle'
                ),
                dict(
                    args=['visible', [False] + [True] + [False] * 2],
                    label='Shooter',
                    method='restyle'
                ),
                dict(
                    args=['visible', [False] * 2 + [True] + [False]],
                    label='Sports',
                    method='restyle'
                ),
                dict(
                    args=['visible', [False] * 3 + [True]],
                    label='Action',
                    method='restyle'
                )
            ]),
        )
    ]),
)

fig5 = {'data': traces, 'layout': layout}

# The App itself

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1(children='Video Game Sales with Ratings',
            style={'color': '#EDEFEB'}),
            html.Label(
                'This dashboard presents a comparative analysis of video game sales by market and by year, '
                'as well as a graph of the dependence of the average user rating and critics ratings by genre.',
                style={'color': 'rgb(33 36 35)'}),
            html.Img(src=app.get_asset_url('supply_chain.png'),
                     style={'position': 'relative', 'width': '180%', 'left': '-83px', 'top': '-20px'}),
        ], className='side_bar'),

        html.Div([
            html.Div([
                html.Label("1. Global sales by regions",
                            style={'font-size': 'medium'}),
                html.Br(),
                html.Br(),
                dcc.Graph(figure=sales_by_regions)
            ], className='box', style={'width': '40%'}),
            html.Div([
                html.Label("2. Number of released games and their sales", style={'font-size': 'medium'}),
                html.Br(),
                html.Br(),
                dcc.Graph(figure=released_games)
            ], className='box', style={'width': '63%'}),
        ], className='row'),
    ], className='main'),
    html.Div([
        html.Div([
            dcc.Graph(
                id='sales_by_regions',
                figure=sales_by_regions
            ),
                 ], className = 'box', style={'width': '40%'}),
        ]),
    dcc.Graph(
        id='released_games',
        figure=released_games
    ),
    html.Div(children='''
        Platforms share
    '''

             ),

    dcc.Graph(
        id='example-graph2',
        figure=fig2
    ),
    html.Div(children='''
    differences in critics' ratings depending on the genre of the game
'''

             ),

    # dcc.Graph(
    #     id='example-graph3',
    #     figure=fig3
    # ),
    html.Div(children='''
    Dependence of the average user rating and critics' rating by genre
'''

             ),

    dcc.Graph(
        id='example-graph4',
        figure=fig4
    ),
    html.Div(children='''
    histograms of the distributions of user ratings by genre
'''

             ),

    dcc.Graph(
        id='example-graph5',
        figure=fig5
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)
