import pandas as pd
from bokeh.io import show
from bokeh.models import ColumnDataSource, HoverTool, LogColorMapper
from bokeh.palettes import Inferno10 as palette
from bokeh.plotting import figure

# import data
from bokeh.sampledata.us_states import data as states
df = pd.read_csv('prescriber-info.csv')

### data analysis

# create dictionary to relate states (postal codes) and avg prescriptions per doctor
prescriptions = {}

# add column showing total drug prescriptions for each doctor
df["Total"] = df.sum(axis=1) - df["NPI"] - df["Opioid.Prescriber"]

# find average number of prescriptions per doctor for each state
for code in states:
    # select doctors in the specified state and create new dataframe with only the total column
    statedf = df.loc[df["State"] == code]["Total"]
    # find average prescriptions per doctor in the specified state
    prescriptions[code] = float(statedf.sum()) / float(statedf.count())

### visualization

# set up color gradient
palette.reverse()
color_mapper = LogColorMapper(palette=palette)

# ignore non-contiguous states
del states["HI"]
del states["AK"]

# set up coordinates
state_xs = [states[code]["lons"] for code in states]
state_ys = [states[code]["lats"] for code in states]

# set up state info (name, avg prescription rate)
state_names = [state['name'] for state in states.values()]
state_rates = [int(prescriptions[code]) for code in states]

# organize the data
source = ColumnDataSource(data=dict(
    x=state_xs,
    y=state_ys,
    name=state_names,
    rate=state_rates
))

# toolbar
TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"

# set up plotting area
p = figure(
    title="2014 Medicare Drug Prescription Rates", tools=TOOLS,
    x_axis_location=None, y_axis_location=None,
    plot_width=1100, plot_height=700
)
p.grid.grid_line_color = None

# plot the states
p.patches('x', 'y', source=source,
          fill_color={'field': 'rate', 'transform': color_mapper},
          line_color="white", line_width=0.5)

# set up hovering tooltips
hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Name", "@name"),
    ("Avg. prescriptions per doctor", "@rate"),
    ("(Long, Lat)", "($x, $y)"),
]

# show figure
show(p)