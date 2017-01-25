import numpy as np
import pandas as pd

from bokeh.plotting import figure, show
from bokeh.models import HoverTool, ColumnDataSource

# import data
df = pd.read_csv('prescriber-info.csv')

### organize data for axes and counts

# create sorted lists containing all fields of medicine and drugs
specialties = sorted(set([name for name in df["Specialty"]]))
drugs = [name for name in df.columns.values]
# clean drugs list
del drugs[0:5]
del drugs[-1]

# create empty matrix to store counts in
counts = np.zeros((len(specialties), len(drugs)))
# iterate through specialties
for specialty in specialties:
    # select only doctors with the specified specialty
    specdf = df.loc[df["Specialty"] == specialty]
    # iterate through drugs
    for drug in drugs:
        # sum all prescriptions for specified drug and assign count value
        counts[specialties.index(specialty), drugs.index(drug)] = specdf[drug].sum()
        
### set up coloring scheme


### visualization

# organize the data
source = ColumnDataSource(data=dict(
    x=drugs,
    y=specialties,
    #colors=color,
    #alphas=alpha,
    count=counts.flatten(),
))

# toolbar
TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"

# format chart
p = figure(title="2014 Medicare Drug Prescriptions by Specialty",
           x_axis_location="above", tools=TOOLS,
           x_range=drugs, y_range=specialties)
p.plot_width = 1600
p.plot_height = 800
p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "4pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = np.pi/3

# draw squares
p.rect('x', 'y', 1.5, 1.5, source=source,
       #color='colors', hover_color='colors', alpha='alphas'
       line_color=None, hover_line_color='black')

# set up hovering tooltips
p.select_one(HoverTool).tooltips = [
    ('Specialty', '@y'),
    ('Drug', '@x'),
    ('Number of Prescriptions', '@count'),
]

# show chart
show(p)