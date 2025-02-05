import igraph as ig
import plotly.graph_objects as go
import plotly.express as px

def generate_company_data():
    """
    This returns a dictionary of company-specific data, including hierarchy info,
    statistics, and company descriptions.
    """
    return {
        "Amalfi midco Ltd 14185820": {
            "graph_data": {
                "vertices":  ["Amalfi midco Ltd 14185820", "Amalfi Cleanco Ltd 14185950", "Amalfi Bidco Ltd 14186033", "Caretech holding Plc 04457287", "Cambian Group Plc 08929371", "Cambian Group Holdings Ltd 08929407", "Caretech Comms Services Ltd 02804415"],
                "edges": [
                    ("Amalfi midco Ltd 14185820", "Amalfi Cleanco Ltd 14185950"),
                    ("Amalfi Cleanco Ltd 14185950", "Amalfi Bidco Ltd 14186033"),
                    ("Amalfi Cleanco Ltd 14185950", "Caretech holding Plc 04457287"),  
                    ("Amalfi Cleanco Ltd 14185950", "Cambian Group Plc 08929371"),
                    ("Amalfi Cleanco Ltd 14185950", "Cambian Group Holdings Ltd 08929407"),
                    ("Amalfi Cleanco Ltd 14185950", "Caretech Comms Services Ltd 02804415"),
                ],
                "categories": {
                    "new_company": ["Amalfi Bidco Ltd 14186033", "Cambian Group Plc 08929371", "Cambian Group Holdings Ltd 08929407"],
                    "update": ["Cambian Group Holdings Ltd 08929407", "Caretech Comms Services Ltd 02804415", "Caretech holding Plc 04457287"]
                }
            },
            "stats": {
                "total_companies": 7,
                "categories": 2,
                "hierarchy_depth": 2
            },
            "description": "Amalfi midco Ltd 14185820 specializes care homes located all over the UK."
        },
        "CompanyB1234": {
            "graph_data": {
                "vertices": ["CompanyB1234", "Category1234", "Category5678", "CompanyB2", "CompanyB3", "CompanyB4", "CompanyB5", "CompanyB6", "CompanyB7"],
                "edges":  [
                    ("CompanyB1234", "Category1234"),
                    ("CompanyB1234", "Category5678"),
                    ("Category1234", "CompanyB2"),
                    ("Category1234", "CompanyB3"),  
                    ("Category5678", "CompanyB4"),
                    ("Category5678", "CompanyB5"),
                    ("Category5678", "CompanyB6"),
                    ("Category5678", "CompanyB7"),
                ],
                "categories": {
                    "new_company": ["CompanyB2"],
                    "update": ["CompanyB5"]
                }
            },
            "stats": {
                "total_companies": 3,
                "categories": 1,
                "hierarchy_depth": 2
            },
            "description": "CompanyB1234 is known for its wide range of care services."
        },
        "CompanyC789": {
            "graph_data": {
                "vertices": ["CompanyC789", "Category C123", "Company C1", "Company C2"],
                "edges": [
                    ("CompanyC789", "Category C123"),
                    ("Category C123", "Company C1"),
                    ("Category C123", "Company C2"),
                ],
                "categories": {
                    "new_company": ["Company C1"],
                    "update": ["Company C2"]
                }
            },
            "stats": {
                "total_companies": 4,
                "categories": 6,
                "hierarchy_depth": 3
            },
            "description": "CompanyC789 is a highly professional company"
        },
        "CompanyD012": {
            "graph_data": {
                "vertices": ["CompanyD012", "Category D969", "Category D789", "Company D100", "Company D200", "Company D300", "Company D400", "Company D500"],
                "edges": [
                    ("CompanyD012", "Category D789"),
                    ("CompanyD012", "Category D969"),
                    ("Category D789", "Company D100"),
                    ("Category D789", "Company D300"),
                    ("Category D969", "Company D200"),
                    ("Category D969", "Company D400"),
                    ("Category D969", "Company D500"),
                ],
                "categories": {
                    "new_company": ["Company D300"],
                    "update": ["Company D500"]
                }
            },
            "stats": {
                "total_companies": 9,
                "categories": 6,
                "hierarchy_depth": 9
            },
            "description": "CompanyD012 has additional related companies."
        }
    }

def generate_product_graph(company_name, category='all'):
    all_data = generate_company_data()

    if company_name not in all_data:
        raise ValueError(f"Company '{company_name}' not found.")

    company_info = all_data[company_name]

    full_vertices = company_info["graph_data"]["vertices"]
    full_edges = company_info["graph_data"]["edges"]

    if category != 'all':
        category_products = company_info["graph_data"]["categories"].get(category, [])
        filtered_vertices = [
            v for v in full_vertices if v in category_products or v == company_name or "Category" in v
        ]
        filtered_edges = [
            e for e in full_edges if e[0] in filtered_vertices and e[1] in filtered_vertices
        ]
    else:
        filtered_vertices = full_vertices
        filtered_edges = full_edges

    graph = ig.Graph(directed=True)
    graph.add_vertices(filtered_vertices)
    graph.add_edges(filtered_edges)
    graph.vs["label"] = filtered_vertices

    return {
        "graph": graph,
        "stats": company_info["stats"],
        "description": company_info["description"]
    }


def create_plot(graph):
    layout = graph.layout_reingold_tilford(root=[0])
    x_coords, y_coords = zip(*layout)
    y_coords = [-y for y in y_coords]  # Flip y-coordinates

    edges = graph.get_edgelist()
    edge_x, edge_y = [], []
    for src, dst in edges:
        edge_x.extend([x_coords[src], x_coords[dst], None])
        edge_y.extend([y_coords[src], y_coords[dst], None])

    node_labels = graph.vs["label"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(color='black', width=1),
        hoverinfo='none'
    ))
    fig.add_trace(go.Scatter(
        x=x_coords, y=y_coords,
        mode='markers+text',
        marker=dict(color='blue', size=10),
        text=node_labels,
        textposition='top center',
        hoverinfo='text'
    ))

    fig.update_layout(
        autosize=True,
        width=1200,  # Increase width
        height=600, # Increase height
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        margin=dict(t=40, l=40, r=40, b=40),
        plot_bgcolor='rgba(253,253,253,1)',
        paper_bgcolor='rgba(255,255,255,1)',
    )

    return fig.to_html(full_html=False, config={"displayModeBar": False})


def load_csv_data(company_name):
    """
    Load CSV data dynamically based on the company name.
    """
    file_path = f"dashboard/data/company_reports.csv"  
    return pd.read_csv(file_path)

def prepare_charts(data):
    """
    Prepare Plotly charts based on the data.
    """
    # Vertical Table
    table_figure = go.Figure(data=[go.Table(
        header=dict(values=["Column 1", "Column 2", "Column 3"]),
        cells=dict(values=[data[col] for col in data.columns])
    )])

    # Bar Chart
    bar_chart = go.Figure(data=[
        go.Bar(x=data["Provider type"], y=data["Number of providers(% of chain)"])
    ])

    # Pie Chart
    pie_chart = go.Figure(data=[
        go.Pie(labels=data["Overall effectiveness"], values=data["Number of providers(% of chain)"])
    ])

    return {
        "table": table_figure.to_html(full_html=False, config={"displayModeBar": False}),
        "bar_chart": bar_chart.to_html(full_html=False, config={"displayModeBar": False}),
        "pie_chart": pie_chart.to_html(full_html=False, config={"displayModeBar": False}),
    }

def reports_view(request):
    """
    Reports tab view.
    """
    company_name = request.GET.get('company_name', 'Amalfi midco Ltd 14185820')  # Default company
    data = load_csv_data(company_name)
    charts = prepare_charts(data)

    return render(request, "dashboard/reports.html", {
        "charts": charts,
        "selected_company": company_name
    })

def create_vertical_bar_chart(data, x_column, y_column, title):
    """
    Creates a vertical bar chart using Plotly.
    """
    fig = px.bar(data, x=x_column, y=y_column, title=title)
    fig.update_layout(
        autosize=True,
        margin=dict(t=30, l=10, r=10, b=30),
    )
    return fig.to_html(full_html=False, config={"displayModeBar": False})

def create_pie_chart(data, labels_column, values_column, title):
    """
    Creates a pie chart using Plotly.
    """
    fig = px.pie(data, names=labels_column, values=values_column, title=title)
    fig.update_layout(
        autosize=True,
        margin=dict(t=30, l=10, r=10, b=30),
    )
    return fig.to_html(full_html=False, config={"displayModeBar": False})


