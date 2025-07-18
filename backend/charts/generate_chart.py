import matplotlib.pyplot as plt

def generate_chart(chart_data: dict) -> str:
    """
    Generate a chart from RBI compliance data.
    chart_data should contain:
        - 'type': 'line', 'bar', or 'pie'
        - 'title': chart title
        - 'xlabel', 'ylabel': axis labels (for line/bar)
        - 'x': list of x values (for line/bar)
        - 'y': list of y values (for line/bar)
        - 'labels', 'sizes': for pie chart
    Returns path to saved chart image.
    """
    chart_type = chart_data.get('type', 'line')
    title = chart_data.get('title', 'RBI Compliance Chart')
    chart_path = '/tmp/chart.png'
    plt.figure()
    if chart_type == 'line':
        plt.plot(chart_data['x'], chart_data['y'], marker='o')
        plt.xlabel(chart_data.get('xlabel', 'X'))
        plt.ylabel(chart_data.get('ylabel', 'Y'))
    elif chart_type == 'bar':
        plt.bar(chart_data['x'], chart_data['y'])
        plt.xlabel(chart_data.get('xlabel', 'X'))
        plt.ylabel(chart_data.get('ylabel', 'Y'))
    elif chart_type == 'pie':
        plt.pie(chart_data['sizes'], labels=chart_data['labels'], autopct='%1.1f%%')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()
    return chart_path
