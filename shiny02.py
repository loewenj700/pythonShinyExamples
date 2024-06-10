import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from shiny import App, render, ui, reactive

# Load the dataset
file_path = 'global_peace_index.csv'  # Ensure this is the correct path to your CSV file
gpi_data = pd.read_csv(file_path)

# Reshape the data to long format
gpi_data_long = gpi_data.melt(id_vars=["Country", "iso3c"], var_name="Year", value_name="GPI_Score")
gpi_data_long["Year"] = gpi_data_long["Year"].astype(int)

# Define the UI
app_ui = ui.page_fluid(
    ui.h3("Global Peace Index Analysis"),
    ui.input_select(
        "year", "Select a Year:",
        {str(year): str(year) for year in sorted(gpi_data_long['Year'].unique())}
    ),
    ui.output_ui("gpi_map"),
    ui.row(
        ui.column(6, ui.output_ui("safest_countries")),
        ui.column(6, ui.output_ui("least_safe_countries"))
    )
)

# Define the server logic
def server(input, output, session):
    @reactive.Calc
    def filtered_data():
        return gpi_data_long[gpi_data_long['Year'] == int(input.year())]

    @output
    @render.ui
    def gpi_map():
        data = filtered_data()
        fig = px.choropleth(
            data,
            locations='iso3c',  # Use ISO-3 country codes for locations
            locationmode='ISO-3',  # Specify that we're using ISO-3 country codes
            color='GPI_Score',  # Use 'GPI_Score' for the values
            hover_name='Country',  # Use 'Country' for the hover information
            color_continuous_scale=px.colors.sequential.YlOrRd,
            labels={'GPI_Score': 'Global Peace Index Score'},
            title=f'Global Peace Index in {input.year()}'
        )
        fig.update_layout(height=600, margin={"r":0,"t":40,"l":0,"b":0})
        fig_html = fig.to_html(full_html=False)
        return ui.HTML(fig_html)

    @output
    @render.ui
    def safest_countries():
        data = filtered_data().nsmallest(10, 'GPI_Score')
        fig = go.Figure(go.Bar(
            x=data['GPI_Score'],
            y=data['Country'],
            orientation='h',
            marker=dict(color='gold')
        ))
        fig.update_layout(
            title='10 Safest Countries',
            xaxis_title='GPI Score',
            yaxis_title='Country',
            height=400,
            margin={"r":0,"t":40,"l":0,"b":0}
        )
        fig_html = fig.to_html(full_html=False)
        return ui.HTML(fig_html)

    @output
    @render.ui
    def least_safe_countries():
        data = filtered_data().nlargest(10, 'GPI_Score')
        fig = go.Figure(go.Bar(
            x=data['GPI_Score'],
            y=data['Country'],
            orientation='h',
            marker=dict(color='red')
        ))
        fig.update_layout(
            title='10 Least Safe Countries',
            xaxis_title='GPI Score',
            yaxis_title='Country',
            height=400,
            margin={"r":0,"t":40,"l":0,"b":0}
        )
        fig_html = fig.to_html(full_html=False)
        return ui.HTML(fig_html)

# Create the app
app = App(app_ui, server)

if __name__ == '__main__':
    app.run()
