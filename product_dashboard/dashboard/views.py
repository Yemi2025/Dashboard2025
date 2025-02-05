import os
from urllib.request import urlopen
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .utils import generate_product_graph, create_plot, create_vertical_bar_chart, create_pie_chart 
from urllib.parse import unquote
import pandas as pd 
import plotly.express as px
import plotly.io as pio
from django.conf import settings
#from .geojson_data import geojson_uk



def index(request):
    company_name = request.GET.get('company_name', 'Amalfi midco Ltd 14185820')  # Default to valid company
    category = request.GET.get('category', 'all')

    try:
        data = generate_product_graph(company_name)
        graph = data["graph"]
        plot_html = create_plot(graph)
    except Exception as e:
        plot_html = None
        print(f"Error generating graph for {company_name}: {e}")

    context = {
        "plot": plot_html,
        "selected_company": company_name,
        "companies": ["Amalfi midco Ltd 14185820", "CompanyB1234", "CompanyC789", "CompanyD012"],  # Extend as needed
    }
    return render(request, 'dashboard/index.html', context)




def get_graph_data(request):
    company_name = request.GET.get('company_name', '').strip()
    category = request.GET.get('category', 'all')

    if not company_name:
        return JsonResponse({"error": "No company name provided."}, status=400)

    try:
        data = generate_product_graph(company_name, category)
        plot = create_plot(data["graph"])
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=404)

    response_data = {
        "plot": plot,
        "statistics": {
            "total_companies": data["stats"]["total_companies"],
            "categories": data["stats"]["categories"],
            "hierarchy_depth": data["stats"]["hierarchy_depth"]
        },
        "info": {
            "description": data["description"]
        }
    }
    return JsonResponse(response_data)


def reports_view(request):
    company_name = request.GET.get("company_name", "")
    if not company_name:
        return HttpResponse("<p>Please select a company to view reports.</p>")

    try:
        # Construct the path to the CSV file
        csv_path = f"dashboard/data/{company_name.replace(' ', '_')}.csv"
        
        # Check if the file exists
        if not os.path.exists(csv_path):
            return HttpResponse("<p>Data not available for the selected company.</p>")
        
        # Read the CSV file
        data = pd.read_csv(csv_path)

        # Generate charts
        provider_chart = create_vertical_bar_chart(
            data, "Provider type", "Number of providers(% of chain)", "Provider Types"
        )
        region_chart = create_pie_chart(
            data, "Provider region", "Number of providers(% of chain)", "Providers by Region"
        )
        inspection_chart = create_vertical_bar_chart(
            data, "Overall effectiveness", "Number of providers(% of chain)", "Full Inspection Outcomes"
        )

        # Render the charts in the reports content template
        return render(request, "dashboard/reports_content.html", {
            "provider_chart": provider_chart,
            "region_chart": region_chart,
            "inspection_chart": inspection_chart,
        })

    except FileNotFoundError:
        return HttpResponse("<p>Data not available for the selected company.</p>")
    except Exception as e:
        print(f"Error loading reports: {e}")
        return HttpResponse("<p>An error occurred while generating the report. Please try again later.</p>")




def analytics_view(request):
    try:
        # Load Local Authority GeoJSON
        with urlopen('https://raw.githubusercontent.com/thomasvalentine/Choropleth/main/Local_Authority_Districts_(December_2021)_GB_BFC.json') as response:
            local_authorities = json.load(response)

        # Add 'id' property to GeoJSON for linking with DataFrame
        for feature in local_authorities["features"]:
            feature['id'] = feature['properties']['LAD21NM']

        # Prepare analytics data
        analytics_data = [
            {"city": "London", "region": "City of London", "value": 1200, "category": "High"},
            {"city": "Berkshire", "region": "Reading", "value": 800, "category": "Medium"},
            {"city": "Oxford", "region": "Oxford", "value": 750, "category": "Medium"},
            {"city": "Brighton", "region": "Brighton and Hove", "value": 600, "category": "Low"},
            {"city": "Bristol", "region": "Bristol", "value": 950, "category": "Medium"},
            {"city": "Cambridge", "region": "Cambridge", "value": 700, "category": "Medium"},
            {"city": "Southampton", "region": "Southampton", "value": 650, "category": "Low"},
            {"city": "Portsmouth", "region": "Portsmouth", "value": 600, "category": "Low"},
            {"city": "Manchester", "region": "Manchester", "value": 1100, "category": "High"},
            {"city": "Liverpool", "region": "Liverpool", "value": 1000, "category": "High"},
            {"city": "Leeds", "region": "Leeds", "value": 900, "category": "Medium"},
            {"city": "Nottingham", "region": "Nottingham", "value": 850, "category": "Medium"},
            {"city": "Sheffield", "region": "Sheffield", "value": 800, "category": "Medium"},
            {"city": "Birmingham", "region": "Birmingham", "value": 1150, "category": "High"},
            {"city": "Coventry", "region": "Coventry", "value": 780, "category": "Medium"},
            {"city": "Leicester", "region": "Leicester", "value": 720, "category": "Medium"},
            {"city": "Exeter", "region": "Exeter", "value": 650, "category": "Low"},
            {"city": "Norwich", "region": "Norwich", "value": 600, "category": "Low"},
        ]

        # Create DataFrame
        df = pd.DataFrame(analytics_data)


        # Generate Choropleth map
        fig = px.choropleth_mapbox(
            df,
            geojson=local_authorities,
            locations='region',
            color='category',
            featureidkey="properties.LAD21NM",
            mapbox_style="carto-positron",
            center={"lat": 51.5, "lon": -0.12},
            zoom=5,
            color_discrete_map={"High": "darkred", "Medium": "orange", "Low": "green"},
            labels={"category": "Risk Level"},
        )

        # Apply layout updates
        fig.update_layout(
            title={
                "text": "London & Surrounding Areas Analytics",
                "y": 0.95,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
                "font": {"size": 24, "color": "darkblue"},
            },
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
        )

        # Convert Plotly figure to HTML
        plot_html = pio.to_html(fig, full_html=False)

        # Debug: Rendering completed
        print("Rendering completed successfully.")

        # Return response
        return JsonResponse({"plot": plot_html})

    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        return JsonResponse({"error": error_message}, status=500)







