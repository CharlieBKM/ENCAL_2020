# Dash components, html, and dash tables
import dash_html_components as html
# Import Bootstrap components
import dash_bootstrap_components as dbc
# Import custom data.py
import data
import pandas as pd
import dash_table
import plotly.express as px


# Import data from data.py file
df=data.eni_complete
              

# Para tablas con enlaces a bases de datos

bancoLayout =html.Div([
    dbc.Row(dbc.Col(html.H3(children='\n'))),
    dbc.Row(dbc.Col(html.H3(children='\n'))),
    dbc.Row(dbc.Col(html.H3(children='Material para consulta y análisis'))),
    html.Iframe(src='assets/appBD.html', width='100%', height='200', 
                style={'border':'none'},
                )

],className = 'app-page')




# Para "Sistemita de Percepción Social"

spsLayout=html.Div([
#    dbc.Row(dbc.Col(html.H3(children='Antecedentes'))),
#    dbc.Row(dbc.Col(html.H4(children='\n'))),
    
    html.Iframe(src='assets/A1.html', width='100%', height='850', 
                style={'background': '13322B', 'border':'none'},
                )
],className = 'app-page')





#Para resultados 1


titulo=html.Div('Estudio Nacional de Calidad de la Atención del Servicio\
                de Salud 2020', 
                style={'fontSize':27,"textAlign": "center", 'font-weight':'bold'},)


reslayout = html.Div([
    titulo,
    html.Div(children=[html.Hr(style={'border':'none'},),
        html.Button('Añadir gráfico', id='add-chart', n_clicks=0),
        html.Button(html.A("Ir a nuevo gráfico",
                           style={'color':'#D4C19C', 'font-family': 'Montserrat'},
                           href='#the-end'), id="go-end"),
        html.H2(children='\n'),
        html.Label("Sección", style={'fontSize':19,'color':'#13322B', 'textAlign':'left',}),
        
    ]),
    html.Div(id='container', children=[]),
    html.Div(html.Button(html.A("Ir Arriba",
                                style={'color':'#D4C19C', 'font-family': 'Montserrat'},
                                href='#add-chart'),id='the-end'), style={'float': 'right'}),
    

], className = 'app-page'),

