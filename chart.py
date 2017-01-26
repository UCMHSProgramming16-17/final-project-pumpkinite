import numpy as np
import pandas as pd

from bokeh.plotting import figure, show
from bokeh.models import HoverTool, ColumnDataSource, LogColorMapper
from bokeh.palettes import Viridis6 as palette

# import data
df = pd.read_csv('prescriber-info.csv')

### organize data for axes and values

# clean dataframe
del df["Opioid.Prescriber"]
del df["NPI"]

# create sorted lists containing all fields of medicine and drugs
specialties = sorted(set([name for name in df["Specialty"]]))
drugs = [name for name in df.columns.values]
# clean drugs list
del drugs[0:4]

# create empty matrix to store counts and percentages in
counts = np.zeros((len(specialties), len(drugs)))
drugpercents = np.zeros((len(specialties), len(drugs)))
# iterate through specialties
for specialty in specialties:
    # select only doctors with the specified specialty and isolate drug data
    specdf = df.loc[df["Specialty"] == specialty]
    specdf = specdf.select_dtypes(include=["int"])
    
    # iterate through drugs
    for drug in drugs:
        # assign values for 
        # (1) total prescriptions for specified drug within specified specialty
        # (2) percentage that the specified drug makes up of total prescriptions within specified specialty
        counts[specialties.index(specialty), drugs.index(drug)] = specdf[drug].sum()
        drugpercents[specialties.index(specialty), drugs.index(drug)] = float(specdf[drug].sum()) / float(specdf.values.sum())

### visualization

# set up lists for data points
drugsdata=[]
specialtiesdata=[]
alpha=[] # lower percentage -> more transparent square
count=[] # higher count -> darker color square

# set up color gradient
palette.reverse()
color_mapper = LogColorMapper(palette=palette)

# determine data points and corresponding alpha value
for i in range(0,len(drugs)):
    for j in range(0,len(specialties)):
        drugsdata.append(drugs[i])
        specialtiesdata.append(specialties[j])
        count.append(counts[j, i])
        
        alpha.append(drugpercents[j, i])
        
        
# organize the data
source = ColumnDataSource(data=dict(
    x=drugsdata,
    y=specialtiesdata,
    count=count,
    alphas=alpha
))

# toolbar
TOOLS = "pan,zoom_out,zoom_in,reset,hover,save"

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
       fill_color={'field': 'count', 'transform': color_mapper}, 
       hover_color={'field': 'count', 'transform': color_mapper}, 
       color="black", alpha='alphas',
       line_color=None, hover_line_color='black')

# set up hovering tooltips
p.select_one(HoverTool).tooltips = [
    ('Specialty', '@y'),
    ('Drug', '@x'),
    ('Number of prescriptions', '@count'),
    ('Fraction of prescriptions in this field', '@alphas')
]

# show chart
show(p)