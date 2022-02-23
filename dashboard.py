from distutils.log import debug
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go 

import numpy as np
import pandas as pd
import json

CENTER_LAT, CENTER_LON = -14.2725, -51.2556

# df = pd.read_csv("./data/HIST_PAINEL_COVIDBR_13mai2021.csv", sep=";")
# df_states = df[(~df["estado"].isna()) & (df["codmun"].isna())]
# df_brasil = df[df["regiao"]=="Brasil"]
# df_states.to_csv("./data/df_states.csv")
# df_brasil.to_csv("./data/df_brasil.csv")

df_states = pd.read_csv("./data/df_states.csv")
df_brasil = pd.read_csv("./data/df_brasil.csv")

df_states_ = df_states[df_states["data"] == "2020-05-13"]
brazil_states = json.load(open("./geojson/brazil_geo.json", "r"))
# brazil_states = json.load(open("./geojson/geojs-100-mun.json", "r"))
df_data = df_states[df_states["estado"]=="PA"]

select_columns = {
  "casosAcumulado": "Casos Acumulados",
  "casosNovos": "Novos Casos",
  "obitosAcumulado": "Óbitos Totais",
  "obitosNovos": "Óbitos por dia"
}
# =========================================
# Instanciação Dash

# Temas https://bootswatch.com/
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

fig = px.choropleth_mapbox(
  df_states_, locations="estado", color="casosNovos",
  center={"lat": -16.95, "lon": -47.78}, zoom=3,
  geojson=brazil_states, color_continuous_scale="Redor",
  opacity=0.4, hover_data={"casosAcumulado": True, 
  "casosNovos": True, "obitosNovos": True, "estado": True}
)

fig.update_layout(
  paper_bgcolor="#212121",
  autosize=True,
  margin=go.layout.Margin(l=0, r=0, t=0, b=0),
  showlegend=False,
  mapbox_style="carto-positron")

fig2 = go.Figure(layout={"template": "plotly_dark"})
fig2.add_trace(go.Scatter(x=df_data["data"], y=df_data["casosAcumulado"]))
fig2.update_layout(
  paper_bgcolor="#212121",
  plot_bgcolor="#212121",
  autosize=True,
  margin=dict(l=10, r=10, t=10, b=10)
)

# =========================================
# Layout
app.layout = dbc.Container(
  dbc.Row(
    [
      dbc.Col(
        [
          html.Div([
            html.Img(id="logo", src=app.get_asset_url("logo_dark2.png"), height=50),
            html.H5("Evolução COVID-19"),
            dbc.Button("BRASIL", color="primary", id="location-button", size="lg")
            ],
            style={}
          ),
          html.P(
            "Informe a data para obter informações:",
            style={"marginTop": "20px"}
          ),
          html.Div(
            id="div-test",
            children=[
              dcc.DatePickerSingle(
                id="date-picker",
                min_date_allowed=df_brasil["data"].min(),
                max_date_allowed=df_brasil["data"].max(),
                initial_visible_month=df_brasil["data"].min(),
                date=df_brasil["data"].max(),
                display_format="MMMM D, YYYY",
                style={"border": "0px solid black"}
              )
            ]
          ),  
          dbc.Row(
            [
              dbc.Col(
                [
                  dbc.Card(
                    [
                      dbc.CardBody(
                        [
                          html.Span("Casos recuperados"),
                          html.H4(
                            style={ "color": "#adfc92"},
                            id="casos-recuperados-text"
                          ),
                          html.Span("Em acompanhamento"),
                          html.H5(id="em-acompanhamento-text"),
                        ],
                        style={"height": "100%"}
                      )
                    ],
                    color="light",
                    outline=True,
                    style={
                      "border": "1px solid lime",
                      "height": "100%",
                      "marginTop": "10px",
                      "boxShadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                      "color": "#FFFFFF"
                    }
                  )
                ],
                md=4
              ),
              dbc.Col(
                [
                  dbc.Card(
                    [
                      dbc.CardBody(
                        [
                          html.Span("Casos confirmados totais"),
                          html.H4(
                            style={"color": "#389fd6"},
                            id="casos-confirmados-text"
                          ),
                          html.Span("Novos casos na data"),
                          html.H5(id="novos-casos-text"),
                        ],
                        style={"height": "100%"}
                      )
                    ],
                    color="light",
                    outline=True,
                    style={
                      "height": "100%",
                      "marginTop": "10px",
                      "boxShadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                      "color": "#FFFFFF"
                    }
                  )
                ],
                md=4
              ),
              dbc.Col(
                [
                  dbc.Card(
                    [
                      dbc.CardBody(
                        [
                          html.Span("Óbitos confirmados"),
                          html.H4(
                            style={"color": "#df2935"},
                            id="obitos-text"
                          ),
                          html.Span("Óbitos na data"),
                          html.H5(id="obitos-na-data-text"),
                        ],
                        style={"height": "100%"}
                      )
                    ],
                    color="light",
                    outline=True,
                    style={
                      "height": "100%",
                      "marginTop": "10px",
                      "boxShadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                      "color": "#FFFFFF"
                    }
                  )
                ],
                md=4
              ),
            ]
          ),
          html.Div(
            [
              html.P(
                "Selecione o tipo de dado que deseja visualizar:",
                style={"marginTop": "15px"}
              ),
              dcc.Dropdown(
                id="location-dropdown",
                options=[{"label": j, "value": i} for i, j in select_columns.items()],
                value="casosNovos",
                style={"marginTop": "10px"}
              ),
              dcc.Graph(
                id="line-graph",
                figure=fig2,
                style={
                  "boxShadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                  "height": "400px"
                }
                )
            ]
          ),
        ],
        md=6,
        style={
          "height": "100vh",
          "padding": "10px",
          "backgroundColor": "#242424",
        }
      ),
      dbc.Col(
        [
          # : 'graph', 'cube', 'circle', 'dot' or 'default'
          dcc.Loading(
            id="loading",
            type="circle",
            children=[
              dcc.Graph(
                id="choropleth-map",
                figure=fig,
                style={
                  "height": "100vh",
                  "marginRight": "10px"
                }
              )
            ]
          ),
        ],
        md=6
      )
    ]
  ),
  fluid=True
)

# =========================================
# Interatividade

@app.callback(
  [
    Output("casos-recuperados-text", "children"),
    Output("em-acompanhamento-text", "children"),
    Output("casos-confirmados-text", "children"),
    Output("novos-casos-text", "children"),
    Output("obitos-text", "children"),
    Output("obitos-na-data-text", "children"),
  ],
  [
    Input("date-picker", "date"),
    Input("location-button", "children")
  ]
)
def display_status(date, location):
  if location=="BRASIL":
    df_data_on_date = df_brasil[df_brasil["data"]==date]
  else:
    df_data_on_date = df_states[(df_states["estado"]==location) &
                                (df_states["data"]==date)]
  
  recuperados_novos     = "-" if df_data_on_date["Recuperadosnovos"].isna().values[0] else f'{int(df_data_on_date["Recuperadosnovos"].values[0]):,}'.replace(",", ".")
  acompanhamentos_novos = "-" if df_data_on_date["emAcompanhamentoNovos"].isna().values[0] else f'{int(df_data_on_date["casosAcumulado"].values[0]):,}'.replace(",", ".")
  casos_acumulados      = "-" if df_data_on_date["casosAcumulado"].isna().values[0] else f'{int(df_data_on_date["casosAcumulado"].values[0]):,}'.replace(",", ".")
  casos_novos           = "-" if df_data_on_date["casosNovos"].isna().values[0] else f'{int(df_data_on_date["casosNovos"].values[0]):,}'.replace(",", ".")
  obitos_acumulado      = "-" if df_data_on_date["obitosAcumulado"].isna().values[0] else f'{int(df_data_on_date["obitosAcumulado"].values[0]):,}'.replace(",", ".")
  obitos_novos          = "-" if df_data_on_date["obitosNovos"].isna().values[0] else f'{int(df_data_on_date["obitosNovos"].values[0]):,}'.replace(",", ".")
  
  return (
    recuperados_novos,
    acompanhamentos_novos,
    casos_acumulados,
    casos_novos,
    obitos_acumulado,
    obitos_novos
  )
  
@app.callback(
  Output("line-graph", "figure"),
  [
    Input("location-dropdown", "value"),
    Input("location-button", "children")
  ]          
)
def plot_line_graph(plot_type, location):
  if location == "BRASIL":
    df_data_on_location = df_brasil.copy()
  else:
    df_data_on_location = df_states[df_states["estado"]==location]
    
  bar_plots = ["casosNovos", "obitosNovos"]
  fig2 = go.Figure(layout={"template": "plotly_dark"})
  
  if plot_type in bar_plots:
    fig2.add_trace(go.Bar(x=df_data_on_location["data"],
                          y=df_data_on_location[plot_type]))
  else:
    fig2.add_trace(
      go.Scatter(
        x=df_data_on_location["data"],
        y=df_data_on_location[plot_type]
      )
    )
  
  fig2.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, t=10, b=10)
  )
  
  return fig2

@app.callback(
  Output("choropleth-map", "figure"),
  [Input("date-picker", "date")]
)
def update_map(date):
  df_data_on_states = df_states[df_states["data"]==date]
  
  fig = px.choropleth_mapbox(
    df_data_on_states,
    locations="estado",
    geojson=brazil_states,
    center={
      "lat": CENTER_LAT,
      "lon": CENTER_LON
    },
    zoom=4,
    color="casosAcumulado",
    color_continuous_scale="Viridis",
    opacity=0.55,
    hover_data={"casosAcumulado": True, 
    "casosNovos": True,
    "obitosNovos": True,
    "estado": False}
  )

  fig.update_layout(
    paper_bgcolor="#242424",
    mapbox_style="carto-positron",
    autosize=True,
    margin=go.layout.Margin(l=0, r=0, t=0, b=0),
    showlegend=False,
  )
  
  return fig

@app.callback(
  Output("location-button", "children"),
  [
    Input("choropleth-map", "clickData"),
    Input("location-button", "n_clicks")
  ]
)
def update_location(click_data, n_clicks):
  changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
  if click_data is not None and changed_id != "location-button.n_clicks":
    state = click_data["points"][0]["location"]
    return "{}".format(state)
  else:
    return "BRASIL"

if __name__ == "__main__":
  app.run_server(debug=True)