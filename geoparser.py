import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_bio as db
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

import GEOparse as geo

PORT = 8050
ADDRESS = "10.84.146.29"

#default_gse = "GSE145614"
default_gse = "GSE61160"

#display mehthylation sample counts 

meta = "/data/ncbi.bak/geo/GPL13534/meta/meth_tools/mana/mana_GEO.full_labels"
meta = pd.read_csv(meta,sep=",",header=0,index_col=0)

#helper functions - put in utils later

def gse_df(gse,path="./"):
    try:
        gse = geo.get_GEO(filepath="./"+gse+"_family.soft.gz")
    except:
        gse = geo.get_GEO(geo=gse,destdir=path)
    out = [x.table.set_index("ID_REF").VALUE for key,x in gse.gsms.items()]
    out = pd.DataFrame(out)
    out.index = list(gse.gsms.keys())
    return(out)

#app = dash.Dash(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)

layout = html.Div(
    [
        dcc.Input(
            id="input",
            type="text",
            placeholder="input type",
            value=default_gse,
            debounce=True
        ),
        html.Div(id="text-out"),
        dcc.Graph(id="geo-violin"),
        dcc.Graph(id="meta-bar")
        
    ]
)

app.layout = layout

@app.callback(
    Output("text-out", "children"),
    Output("geo-violin","figure"),
    Output("meta-bar","figure"),
    Input("input", "value")
)
def update_value(value):
    info = str(value)
    data = gse_df(value)
    data = data.sample(250,axis=1)
    fig = px.violin(data.T,points="all",box=True)
    #fig = px.scatter([1,1,1])
    fig.update_layout(transition_duration=500)
    mf = meta[meta.ExperimentID==int(value[3:])]
    mf = mf.TissueName.value_counts().reset_index()
    mf.columns = ["TissueName","count"]
    meta_fig = px.histogram(mf,x="TissueName",y="count")
    meta_fig.update_layout(transition_duration=500)
    
    return(info,fig,meta_fig)
#def cb_render(*vals):
#    return " | ".join((str(val) for val in vals if val))


if __name__ == '__main__':
    app.run_server(debug=True,port=PORT,host=ADDRESS)

#load in a particular gse and view the table head (whole row)
#load in labels from ale if possible 