import dash_table
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
import dash_ui as dui
from dash.dependencies import Input, Output, State
import datetime
from dateutil.relativedelta import relativedelta
import yfinance as yf
import plotly.graph_objects as go
from logic import *


############################################################################################

app = Dash()
external_stylesheets = ['https://codepen.io/rmarren1/pen/mLqGRg.css']
app = Dash(__name__, external_stylesheets=external_stylesheets, )
server = app.server
my_css_urls = ["https://codepen.io/rmarren1/pen/mLqGRg.css"]

colors = {
    'background': '#050505',
    'text': '#7FDBFF'
}

############################################################################################

grid = dui.Grid(_id="grid", num_rows=12, num_cols=12, grid_padding=0)

# Top border (title)
page_title = html.Div([html.H1('LIGHTHAVEN INVESTMENT PROCESS')],
                           style={'textAlign': 'center', 'fontSize':20})
grid.add_element(col=1, row=1, width=12, height=1, element=page_title)

grid.add_element(col=1, row=1, width=12, height=1, element=html.Div(
    style={"background-color": "#1B91CF", "height": "100%", "width": "100%"}
))

# Bottom border
grid.add_element(col=1, row=12, width=12, height=1, element=html.Div(
    style={"background-color": "#1B91CF", "height": "100%", "width": "100%"}
))

# Left border
grid.add_element(col=1, row=2, width=1, height=10, element=html.Div(
    style={"background-color": "#1B91CF", "height": "100%", "width": "100%"}
))

# Right border
grid.add_element(col=12, row=2, width=1, height=10, element=html.Div(
    style={"background-color": "#1B91CF", "height": "100%", "width": "100%"}
))

############################################################################################

# Get API sheets data
ticker = 'AMZN'
ticker_data = get_ticker_data(ticker)

# Get stock price data
start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()

#try:
price_data = yf.download(ticker, start, end)
price_data = price_data.reset_index()
#except:
#    return "Could not get data"

############################################################################################

# Create main chart
fig = go.Figure()

fig.add_trace(go.Scatter(x=list(price_data['Date']), y=list(price_data['Close']), name="close",
                         line=dict(color="#03b1fc", width=3)))

def create_annotation_list(data):
    annotation_list = []

    for row in range(0, data.shape[0]):
        counter = 1
        comment = '<b>' + data.iloc[row]['Event'] + '</b><br>' + add_new_line(data.iloc[row]['Comment'])
        date = last_trading_day(data.iloc[row]['Date']) # fix helper function to get last trading day
        price_stock = price_data[price_data['Date'] == date].iloc[0]['Close']
        max_price = price_data['Close'].max()
        new_entry = dict(
                        x=date,
                        y=price_stock,
                        text=comment,
                        showarrow=True,
                        font=dict(
                            size=12,
                            color="#414b4d"
                        ),
                        align="center",
                        arrowhead=3,
                        arrowsize=1,
                        arrowwidth=1,
                        arrowcolor="#414b4d",
                        bordercolor="#414b4d",
                        borderwidth=2,
                        borderpad=3,
                        bgcolor="#D0E4F7",
                        opacity=0.8
                        )
        annotation_list.append(new_entry)

    return annotation_list

fig.update_layout(
    title='<b>' + ticker + ' Investment Process</b>',
    title_x=0.5,
    xaxis_title="<b>Date</b>",
    font=dict(
            size=16,
            color="black"
        ),
    yaxis_title="<b>Stock Price</b>",
    margin={'l': 50, 'r': 50, 't': 40, 'b': 40},
    annotations=create_annotation_list(ticker_data),
    height=775,
    paper_bgcolor='lightgrey'
    )

stock_chart = dcc.Graph(id="Stock Graph", figure=fig)

grid.add_element(col=2, row=2, width=10, height=10, element=(stock_chart))

############################################################################################

app.layout = html.Div(
    dui.Layout(
        grid=grid,
    ),
    style={
        'height': '100vh',
        'width': '100vw'
    }
)

if __name__ == "__main__":
    app.run_server(debug=True)

############################################################################################
