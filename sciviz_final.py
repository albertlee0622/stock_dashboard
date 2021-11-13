#!/usr/bin/env python
# coding: utf-8

# Author: Albert Lee  
# Illinois Netid: albertl8  
# Title: Stock Price Dashboard  

# In[1]:


import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

df_aapl = pd.read_csv('AAPL.csv')
df_goog = pd.read_csv('GOOG.csv')


# In[2]:


df_aapl['Close1'] = df_aapl['Close'].shift(1)
df_goog['Close1'] = df_goog['Close'].shift(1)
df_aapl['Return'] = df_aapl['Close1'] / df_aapl['Close'][0]
df_goog['Return'] = df_goog['Close1'] / df_goog['Close'][0]
df_aapl['dReturn'] = df_aapl['Close'].pct_change()
df_goog['dReturn'] = df_goog['Close'].pct_change()
df_aapl.dropna(inplace=True)
df_goog.dropna(inplace=True)


# In[3]:


# df_aapl.head()


# In[4]:


# df_goog.head()


# In[5]:


window = 20
returns = pd.DataFrame({
    'AAPL_Norm': df_aapl['Return'],
    'GOOG_Norm': df_goog['Return']
    })
returns.index = df_aapl.Date
returns[f'AAPL_MA{window}'] = returns.AAPL_Norm.rolling(window).mean()
returns[f'GOOG_MA{window}'] = returns.GOOG_Norm.rolling(window).mean()


# In[6]:


return_fig = go.Figure()

for column in returns.columns.to_list():
    return_fig.add_trace(
        go.Scatter(
            x = returns.index,
            y = returns[column],
            name = column
        )
    )
    
return_fig.update_layout(
    updatemenus=[go.layout.Updatemenu(
        active=0,
        buttons=list(
            [dict(label = 'All',
                  method = 'update',
                  args = [{'visible': [True, True, True, True]},
                          {'title': 'All',
                           'showlegend':True}]),
             dict(label = 'AAPL',
                  method = 'update',
                  args = [{'visible': [True, False, True, False]}, # the index of True aligns with the indices of plot traces
                          {'title': 'AAPL',
                           'showlegend':True}]),
             dict(label = 'GOOG',
                  method = 'update',
                  args = [{'visible': [False, True, False, True]},
                          {'title': 'GOOG',
                           'showlegend':True}]),
             dict(label = 'Cum.Rtn.Only',
                  method = 'update',
                  args = [{'visible': [True, True, False, False]},
                          {'title': 'Cum.Return',
                           'showlegend':True}]),
             dict(label = f'MA{window} Only',
                  method = 'update',
                  args = [{'visible': [False, False, True, True]},
                          {'title': f'MA{window}',
                           'showlegend':True}]),
            ])
        )
    ])

# return_fig.show()


# In[7]:


corr_fig = px.scatter(x=df_aapl['dReturn'], y=df_goog['dReturn'], trendline="ols", trendline_color_override="red")
corr_fig
corr_fig.update_layout(xaxis_title='AAPL', yaxis_title='GOOG')
# corr_fig.show()


# In[8]:


fig = make_subplots(rows=2, cols=1, 
#                     specs=[[{}, {}],
#                            [{"colspan": 2}, None],
#                            [{"colspan": 2}, None]],
                           subplot_titles=("Apple", "Google"),
                           shared_xaxes=False,)

fig.append_trace(go.Candlestick(x=df_aapl['Date'],
                                    open=df_aapl['Open'],
                                    high=df_aapl['High'],
                                    low=df_aapl['Low'],
                                    close=df_aapl['Close'],
                                    showlegend=False),
                row=1, col=1)

fig.append_trace(go.Candlestick(x=df_goog['Date'],
                                    open=df_goog['Open'],
                                    high=df_goog['High'],
                                    low=df_goog['Low'],
                                    close=df_goog['Close'],
                                    showlegend=False),
                row=2, col=1)

fig.update_layout(xaxis1_rangeslider_visible=True,
                  xaxis2_rangeslider_visible=True, 
)
fig.update_xaxes(rangeslider_thickness = 0.05)
fig.layout.annotations[0].update(x=0.025)
fig.layout.annotations[1].update(x=0.025)
fig.update_layout(
    autosize=True,
#     width=1000,
    height=600,
    margin=dict(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=1
    ),
    yaxis1_title='USD',
    yaxis2_title='USD',
)



# fig.show()


# In[9]:


import plotly.graph_objects as go # or plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([ html.H1('Stock Price Dashboard', style={'textAlign': 'center'}),
                        html.Div([
                                html.Div([html.H2('Summary', style={'textAlign': 'center'}),
                                    dcc.Graph(figure=return_fig)
                                ], style={'width': '60%', 'display': 'inline-block'}),
                                html.Div([html.H2('Return Correlation', style={'textAlign': 'center'}),
                                    dcc.Graph(figure=corr_fig)
                                ], style={'width': '40%', 'display': 'inline-block'}),
                        html.Div([html.H2('Daily OHLC Charts', style={'textAlign': 'center'}),
                        dcc.Graph(figure=fig)
                        ], style={'width': '100%', 'display': 'block'}),
                        ],)
])

app.run_server(debug=False, use_reloader=False)


# In[ ]:




