import pandas as pd
import plotly.express as px
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
    ui.output_ui("gpi_map")
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

# Create the app
app = App(app_ui, server)

if __name__ == '__main__':
    app.run()
