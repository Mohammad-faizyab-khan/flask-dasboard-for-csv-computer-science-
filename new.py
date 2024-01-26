from flask import Flask, render_template, request, redirect
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import csv

app = Flask(__name__)

# Read initial data from CSV
df = pd.read_csv('Sample.csv')

@app.route('/')
def dashboard():
    # Create the dashboard layout
    plots = []

    profit_by_ship_mode = df.groupby('Mode')['CPU usage'].sum().reset_index()
    ship_mode_bar = px.bar(profit_by_ship_mode, x='Mode', y='CPU usage', title='CPU usage by classes')
    ship_mode_bar.update_layout(height=400)  # Customize the plot height
    plots.append(ship_mode_bar.to_html(full_html=False))


    profit_by_segment = df.groupby('Segment')['CPU usage'].sum().reset_index()
    segment_pie = px.pie(profit_by_segment, values='CPU usage', names='Segment', title='CPU usage by Segment')
    segment_pie.update_layout(height=400)  # Customize the plot height
    plots.append(segment_pie.to_html(full_html=False))

    profit_by_country_city = df.groupby(['Country', 'City'])['CPU usage'].sum().reset_index()
    top_10_country_city = profit_by_country_city.nlargest(10, 'CPU usage')
    country_city_bar = px.bar(top_10_country_city, x='Country', y='CPU usage', color='City', title='Top 10 Cities by CPU usage')
    country_city_bar.update_layout(height=400)  # Customize the plot height
    plots.append(country_city_bar.to_html(full_html=False))

    scatter_plot = px.scatter(df, x='Quantity', y='CPU usage', color='Temp Rise', title='CPU usage vs. Disk Usage')
    scatter_plot.update_layout(height=400)  # Customize the plot height
    plots.append(scatter_plot.to_html(full_html=False))

    profit_by_region = df.groupby('Region')['CPU usage'].sum().reset_index()
    region_bar = px.bar(profit_by_region, x='Region', y='CPU usage', title='CPU usage by Region')
    region_bar.update_layout(height=400)  # Customize the plot height
    plots.append(region_bar.to_html(full_html=False))


    profit_by_category = df.groupby('Category')['CPU usage'].sum().reset_index()
    sunburst_chart = px.sunburst(profit_by_category, path=['Category'], values='CPU usage', title='Usage by Category')
    sunburst_chart.update_layout(height=400)  # Customize the plot height
    plots.append(sunburst_chart.to_html(full_html=False))

    profit_by_subcategory = df.groupby('Sub-Category')['CPU usage'].sum().reset_index()
    funnel_chart = px.funnel(profit_by_subcategory, x='CPU usage', y='Sub-Category', title='Profit by Sub-Category')
    funnel_chart.update_layout(height=400)  # Customize the plot height
    plots.append(funnel_chart.to_html(full_html=False))

    sales_by_country = df.groupby('Country')['consumption'].sum().reset_index()
    animated_bubble_map = px.scatter_geo(sales_by_country, locations='Country', locationmode='country names', size='consumption', title=' Country')
    animated_bubble_map.update_layout(height=400)  # Customize the plot height
    plots.append(animated_bubble_map.to_html(full_html=False))

    # Render the template with all plots
    return render_template('dashboard.html', plot_html=plots)

# Function to write data to CSV file
def write_to_csv(data):
    with open('Sample.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Create, Read, Update, Delete (CRUD) operations

# Read operation
@app.route('/data.html')
def get_data():
	return render_template('data.html', data=df)

# Create operation
@app.route('/add_data', methods=['POST'])
def add_data():
    data = [
        request.form['mode'], request.form['segment'], request.form['country'],
        request.form['city'], request.form['state'], request.form['postal_code'],
        request.form['region'], request.form['category'], request.form['sub_category'],
        float(request.form['consumption']), int(request.form['quantity']),
        float(request.form['discount']), float(request.form['cpu_usage']),
        request.form['ip_address']
    ]

    write_to_csv(data)
    # Reload the dataframe after adding data
    global df
    df = pd.read_csv('Sample.csv')
    
    return redirect('/data.html')

# Update operation (Not implemented in this example)

# Delete operation
@app.route('/delete_data', methods=['POST'])
def delete_data():
    index = int(request.form['row_index'])
    # Drop the selected row
    df.drop(index, inplace=True)
    # Save the updated dataframe to CSV
    df.to_csv('Sample.csv', index=False)

    return redirect('/data.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)

