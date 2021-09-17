import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_bio as db
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

PORT = 8051
ADDRESS = "10.84.146.29"

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#FDF7EB',
    'text': '#381010'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

#loading data

df = "/home/xiavan/collab/amer/amer_sle_betas_imputed_combat_TSS1500_median_DE.csv"
df = pd.read_csv(df,index_col=0)
df.index = df.index.rename("gene")
df = df.reset_index()
hits = df[df.sig==True].gene.unique()

corr = pd.read_hdf("/home/xiavan/collab/amer/amr_de_corr.h5",key="data")
de_corr = corr.loc[hits][hits]
pos_corr = df[(df.sig==True) & (df.coef>0)].gene.unique()
pos_corr = corr.loc[pos_corr][pos_corr]
anti_corr = df[(df.sig==True) & (df.coef<0)].gene.unique()
anti_corr = corr.loc[anti_corr][anti_corr]

meta = "/data/ncbi.bak/geo/GPL13534/meta/meth_tools/mana/mana_GEO.full_labels"
meta = pd.read_csv(meta,sep=",",header=0,index_col=0)

#test = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

#prepping app and figs

app = dash.Dash(__name__)

#fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
#fig = px.scatter(data_frame=df,y="-log(adjusted p)",x="coef",color="sig")

#fig = px.density_heatmap(data_frame=corr)
#fig = px.imshow(corr)

#fig.update_layout(
#    plot_bgcolor=colors['background'],
#    paper_bgcolor=colors['background'],
#    font_color=colors['text']
#)


#non-interactive plots

#de_clustergram = db.Clustergram(data=de_corr)

#card helpers 

card_content = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
        ]
    ),
]


pos_de_clustergram = db.Clustergram(
    #data=de_corr,
    data = pos_corr,
    height=800,
    width=700,
    row_labels = list(de_corr.index),
    column_labels = list(de_corr.columns),
    hidden_labels="column",
    tick_font={"size":12},
    display_ratio=[0.1, 0.1],
    color_map= [
        [0.0, '#636EFA'],
        [0.5, '#FFFFFF'],
        [1.0, '#EF553B']
    ]
)

anti_de_clustergram = db.Clustergram(
    #data=de_corr,
    data = anti_corr,
    height=800,
    width=700,
    row_labels = list(de_corr.index),
    column_labels = list(de_corr.columns),
    hidden_labels="column",
    tick_font={"size":12},
    display_ratio=[0.1, 0.1],
    color_map= [
        [0.0, '#636EFA'],
        [0.5, '#FFFFFF'],
        [1.0, '#EF553B']
    ]
)

volcano_card = [
    dbc.CardHeader("DMG Volcano plot"),
    dbc.CardBody(
        [
            dcc.Graph(id='volcano',style={'width': '50vh', 'height': '40vh'}),
            dcc.Slider(
                id='volcano-slider',
                min=0.001,
                max=0.2,
                value=0.05,
                marks={str(year): str(year) for year in (0.001,0.01,0.02,0.05,0.1,0.2)},
                step=None
            )
        ]
    )
]


volcano_card = [
            dcc.Graph(id='volcano',style={'width': '85vh', 'height': '40vh'}),
            dcc.Slider(
                id='volcano-slider',
                min=0.001,
                max=0.2,
                value=0.05,
                marks={str(year): str(year) for year in (0.001,0.01,0.02,0.05,0.1,0.2)},
                step=None
            )
        ]

'''
cluster_card = [
    dbc.CardHeader("DMG Clustergram"),
    dbc.CardBody(
        [
            dcc.Graph(figure=de_clustergram)
        ]
    )
]
'''

hist = [
    dbc.CardHeader("Platform Stats"),
    dbc.CardBody(
        [
            dcc.Dropdown(
                id='platform-dropdown',
                options=[{'label': i, 'value': i} for i in meta.columns],
                value='TissueName'
            ),
            dcc.RadioItems(
                id="platform-radio",
                options=[{'label': i, 'value': i} for i in ["Linear","Log"]],
                value="Linear",
                labelStyle={"display":"inline-block"}
            ),
            dcc.Graph(id='platform')
        ]
    )
]

hist = [
            dcc.Dropdown(
                id='platform-dropdown',
                options=[{'label': i, 'value': i} for i in meta.columns],
                value='TissueName'
            ),
            dcc.RadioItems(
                id="platform-radio",
                options=[{'label': i, 'value': i} for i in ["Linear","Log"]],
                value="Linear",
                labelStyle={"display":"inline-block"}
            ),
            dcc.Graph(id='platform')
        ]

pos_cluster_card = [
    dbc.CardHeader("Pos DMG Clustergram"),
    dbc.CardBody(
        [
            dcc.Graph(figure=pos_de_clustergram)
        ]
    )
]

anti_cluster_card = [
    dbc.CardHeader("Anti DMG Clustergram"),
    dbc.CardBody(
        [
            dcc.Graph(figure=anti_de_clustergram)
        ]
    )
]

#card layout

cards = html.Div(
    [
        html.H1(
            children='Trend Deviation',
            style={
                'textAlign': 'left',
                'color': colors['text']
            }),
        dbc.Row(
            [
                dbc.Col(volcano_card),
                dbc.Col(hist)
                #dbc.Col(dbc.Card(cluster_card))
                #dcc.Graph(de_clustergram)
            ],
            className="mb-4",
        ),
        dbc.Row([
                dbc.Col(dbc.Card(pos_cluster_card)),
                dbc.Col(dbc.Card(anti_cluster_card))
        ]),
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content, color="success", inverse=True)),
                dbc.Col(dbc.Card(card_content, color="warning", inverse=True)),
            ],
            className="mb-4",
        )
    ]
)

#app = dash.Dash(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = cards

#callbacks

@app.callback(
    Output('volcano', 'figure'),
    Input('volcano-slider', 'value'))
def update_volcano(value):
    filtered_df = df
    filtered_df["sig"] = filtered_df["adjusted p"]<value

    fig = px.scatter(data_frame=filtered_df,y="-log(adjusted p)",x="coef",color="sig",hover_data={"gene":True,"sig":False})

    fig.update_layout(transition_duration=500)

    return(fig)

@app.callback(
    Output('platform', 'figure'),
    Input('platform-dropdown', 'value'),
    Input("platform-radio","value"))
def update_hist(annotation,scale):
    toplot = pd.DataFrame(meta[annotation].value_counts().reset_index())
    toplot["index"] = toplot["index"].astype(str)
    toplot.columns = [annotation,"count"]
    fig = px.histogram(toplot,y=annotation,x="count",orientation="h")
    #filtered_df["sig"] = filtered_df["adjusted p"]<value

    #fig = px.scatter(data_frame=filtered_df,y="-log(adjusted p)",x="coef",color="sig",hover_data={"gene":True,"sig":False})

    fig.update_layout(transition_duration=500)
    fig.update_xaxes(title="sum of count",
                    type="linear" if scale=="Linear" else "log")
    
    return(fig)

#run app

if __name__ == '__main__':
    app.run_server(debug=True,port=PORT,host=ADDRESS)