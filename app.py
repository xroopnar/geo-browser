#from jupyter_dash import JupyterDash  # pip install dash
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import pandas as pd  # pip install pandas
import plotly.express as px
import math
from dash import no_update

from sklearn.decomposition import PCA 

####### LOADING DATA

data = pd.read_csv("https://raw.githubusercontent.com/xroopnar/SPUG2019/master/SPUG_tiny_data.csv",header=0,index_col=0)
labels = pd.read_csv("https://raw.githubusercontent.com/xroopnar/SPUG2019/master/SPUG_labels.csv",header=0,index_col=0).astype(str)
data,labels = data.align(labels,axis=0,join="inner")

#prepare PCA
pca = PCA(n_components=20)
pc = pca.fit_transform(data)
pc = pd.DataFrame(pc)
pc.index = data.index

####### APP LAYOUT

colors = {
    'background': '#eb3434',
    'bodyColor':'#F2DFCE',
    'text': '#ffffff'
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

app.layout = html.Div(dbc.Container([
                       dbc.Row([
                                dbc.Col([html.H1("GEO 450k data browser",id="header",style={"color":colors["text"],"margin-left":"5px"})])
                       ],align="center",style={"backgroundColor":colors["background"],"margin-bottom":"10px"}),
                       dbc.Row([
                           dbc.Col([
                       html.H3("PCA Results"),
                       dcc.Dropdown(id="pca-color",
                                    value="ExperimentID",
                                    options=[
                                            {"label": x,"value": x}
                                            for x in labels.columns
                                             ]
                                    ),

                       dcc.Graph(id="pca-plot"),
                           ]),
                           dbc.Col([
                       html.H3("TSS1500 Methylation"),
                       dcc.Dropdown(id="tissue-dropdown",
                                    value="brain",
                                    options=[
                                            {"label": x,"value": x}
                                            for x in labels.TissueName.unique()
                                            ]
                                    ),
                       dcc.Graph(id="tissue-dist")
                           ])
                       ])
]))

###### CALLBACKS

@app.callback(
              Output('pca-plot', 'figure'),
              Input('pca-color', 'value'))
def update_pca(value):
  fig = px.scatter(pc,x=0,y=1,color=labels[value])
  return(fig)

@app.callback(
              Output('tissue-dist', 'figure'),
              Input('tissue-dropdown', 'value'))
def update_tissue(value):
  hits = labels[labels.TissueName==value].index
  hits = data.loc[hits]
  fig = px.histogram(data.sample(100).sample(100,axis=1).unstack())
  return(fig)

###### RUN APP
ADDRESS = "10.84.146.29"
PORT = 8030
app.run_server(debug=True, host=ADDRESS,port=PORT)