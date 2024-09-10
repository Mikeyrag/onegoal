import pandas as pd 
import numpy as np
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash import dash_table

# 1. Read in the data   

best_fit = pd.read_csv('onegoal_best_fit_list_milestone.csv')
champion_milesone = pd.read_csv('onegoal_champion_milestone.csv')
data_dictionary = pd.read_csv('onegoal_data_dictionary.csv')
gpa_goal = pd.read_csv('onegoal_gpa_goal_milestone.csv')
student_info = pd.read_csv('onegoal_student_information.csv')


'''print(best_fit.head())
print(champion_milesone.head())
print(data_dictionary.head())
print(gpa_goal.head())
print(student_info.head())
'''
# 2. Merge the data

merged_data = pd.merge(student_info, best_fit,how = 'left', on='student_id')
merged_data = pd.merge(merged_data, champion_milesone,how = 'left', on='student_id')
merged_data = pd.merge(merged_data, gpa_goal,how = 'left', on='student_id') 

# check the merged data

#print(merged_data.head())

# 3. Data cleaning + exploration
##On hover, the data should show the list of students who completed the milestone
# check the null values
#print(merged_data.isnull().sum())

#realized null values are '--' instead of NaN
#replace '--' with NaN
merged_data.replace('--', np.nan, inplace=True)

#check null values again
#print(merged_data.isnull().sum())

milestones = {
    'champion': 'champion_status',
    'gpa_goal': 'gpa_goal_status',
    'best_fit': 'status_best_fit'
}

#Check count of students for each teacher
merged_data.teacher.value_counts(sort = False, normalize = False, dropna=True)

#Check postsecondary plan completion
merged_data.status_best_fit.value_counts(sort = False, normalize = False, dropna=False)

#Check GPA goals
merged_data.gpa_goal_status.value_counts(sort = False, normalize = False, dropna=False)

#Check Champion Milestone Completion
merged_data.champion_status.value_counts(sort = False, normalize = False, dropna=False)

# 4. Data Visualization 
import plotly.express as px
import plotly.graph_objects as go

# Champion Milestone Completion
champion_chart = px.bar(
    merged_data,
    x=milestones["champion"],
    title='Champion Milestone Completion',
    labels={milestones["champion"]: 'Champion Status'}
)
#champion_chart.show()


# Best Fit Completion
best_fit_chart = px.bar(
    merged_data,
    x= milestones["best_fit"],
    title='Best Fit Completion',
    labels={milestones["best_fit"]: 'Best Fit Status'}
)
#best_fit_chart.show()

# GPA Goal Completion
gpa_goal_chart = px.bar(
    merged_data,
    x=milestones["gpa_goal"],
    title='GPA Goal Completion',
    labels={milestones["gpa_goal"]: 'GPA Goal Status'}
)
#gpa_goal_chart.show()  

# Create a DataFrame with milestone completion counts for each teacher
milestone_completion = merged_data.groupby('teacher').agg({
    milestones['champion']: lambda x: (x == 'Complete').sum(),
    milestones['gpa_goal']: lambda x: (x == 'Complete').sum(),
    milestones['best_fit']: lambda x: (x == 'Complete').sum()
}).reset_index()

# Melt the DataFrame to create a long format suitable for plotting
milestone_completion_melted = milestone_completion.melt(
    id_vars=['teacher'],
    value_vars=[milestones['champion'], milestones['gpa_goal'], milestones['best_fit']],
    var_name='Milestone',
    value_name='Completed'
)

# Create a stacked bar chart
milestone_completion_chart = px.bar(
    milestone_completion_melted,
    x='Milestone',
    y='Completed',
    color='teacher',
    title='Milestone Completion by Teacher',
    labels={'Milestone': 'Milestone Type', 'Completed': 'Number of Students'},
    barmode='stack'
)

# Update layout for better readability
milestone_completion_chart.update_layout(
    xaxis_title='Milestone Type',
    yaxis_title='Number of Students',
    legend_title='Teacher'
)

# Show the chart
#milestone_completion_chart.show()

# Create Dashboard Layout

from plotly.subplots import make_subplots

# Create a subplot with 1 row and 3 columns
fig = make_subplots(rows=1, cols=3, subplot_titles=('Champion Milestone', 'GPA Goal Milestone', 'Best Fit List Milestone'))

# Add the charts to the subplot
fig.add_trace(champion_chart['data'][0], row=1, col=1)
fig.add_trace(gpa_goal_chart['data'][0], row=1, col=2)
fig.add_trace(best_fit_chart['data'][0], row=1, col=3)

# Update layout
fig.update_layout(title_text='Student Milestones Dashboard')

# Show the dashboard
#fig.show()

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.PULSE])
app.config.suppress_callback_exceptions = True

# Define color scheme
PRIMARY_COLOR = 'rgb(255, 79, 53)'
PRIMARY_COLOR_HEX = '#ff4f35'
BACKGROUND_COLOR = 'white'

# Define the sidebar with updated styles
sidebar = html.Div(
    [
        html.H2("Dashboard Views", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Classroom View", href="/", active="exact"),
                dbc.NavLink("Student Table", href="/student-table", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    },
)

# Add custom CSS to style the nav pills
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .nav-pills .nav-link.active, .nav-pills .show>.nav-link {
                color: #fff;
                background-color: ''' + PRIMARY_COLOR_HEX + ''';
            }
            .nav-pills .nav-link {
                color: ''' + PRIMARY_COLOR_HEX + ''';
            }
            .nav-pills .nav-link:hover {
                color: #fff;
                background-color: ''' + PRIMARY_COLOR_HEX + ''';
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Define the content area
content = html.Div(id="page-content", style={"margin-left": "18rem", "margin-right": "2rem", "padding": "2rem 1rem"})

# Update the app layout
app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
], style={'backgroundColor': BACKGROUND_COLOR})

# Create the classroom view layout
classroom_layout = html.Div([
    html.H1("OneGoal Classroom Progress Dashboard", 
            style={'color': PRIMARY_COLOR, 'marginBottom': '30px', 'textAlign': 'center'}),
    html.Div([
        dcc.Dropdown(
            id='teacher-dropdown',
            options=[{'label': teacher, 'value': teacher} for teacher in merged_data['teacher'].unique()],
            placeholder="Select a teacher",
            style={'marginBottom': '30px'}
        ),
    ], style={'width': '50%', 'margin': 'auto'}),
    html.Div([
        dcc.Graph(id='milestone-completion-chart')
    ], style={
        'border': f'2px solid {PRIMARY_COLOR}',
        'borderRadius': '10px',
        'padding': '10px',
        'marginBottom': '30px'
    }),
    html.Div(id='classroom-analytics', style={'marginTop': '30px'}),
    html.Div(id='student-details', style={'marginTop': '30px'})
], style={'backgroundColor': BACKGROUND_COLOR, 'padding': '20px'})

# Create the student table layout
student_table_layout = html.Div([
    html.H1("Student Data Table", style={'color': PRIMARY_COLOR}),
    dcc.Dropdown(
        id='teacher-dropdown-table',
        options=[{'label': teacher, 'value': teacher} for teacher in merged_data['teacher'].unique()],
        placeholder="Select a teacher"
    ),
    dash_table.DataTable(
        id='student-table',
        columns=[
            {"name": "Student ID", "id": "student_id"},
            {"name": "First Name", "id": "first_name"},
            {"name": "Last Name", "id": "last_name"},
            {"name": "Grade", "id": "grade"},
            {"name": "Champion Status", "id": "champion_status"},
            {"name": "GPA Goal Status", "id": "gpa_goal_status"},
            {"name": "Best Fit Status", "id": "status_best_fit"},
        ],
        style_table={'overflowX': 'auto'},
        style_cell={
            'minWidth': '100px', 'width': '150px', 'maxWidth': '180px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'backgroundColor': BACKGROUND_COLOR,
            'color': 'black',
        },
        style_header={
            'backgroundColor': PRIMARY_COLOR,
            'color': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        page_size=15,
        sort_action='native',
        filter_action='native',
    )
], style={'backgroundColor': BACKGROUND_COLOR, 'padding': '20px'})

# Update the page content based on the URL
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return classroom_layout
    elif pathname == "/student-table":
        return student_table_layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

# Update the student table based on the selected teacher
@app.callback(
    Output('student-table', 'data'),
    Input('teacher-dropdown-table', 'value')
)
def update_student_table(selected_teacher):
    if not selected_teacher:
        return []
    
    teacher_data = merged_data[merged_data['teacher'] == selected_teacher]
    return teacher_data.to_dict('records')

# Update the milestone completion chart
@app.callback(
    Output('milestone-completion-chart', 'figure'),
    Input('teacher-dropdown', 'value')
)
def update_milestone_chart(selected_teacher):
    overall_percentages = {}
    for milestone, status_col in milestones.items():
        overall_percentages[milestone] = (merged_data[status_col] == 'Complete').mean() * 100

    if not selected_teacher:
        df_percentages = pd.DataFrame(list(overall_percentages.items()), columns=['Milestone', 'Percentage'])
        fig = px.line(df_percentages, x='Milestone', y='Percentage', 
                      title='Overall Milestone Completion Percentages',
                      labels={'Percentage': 'Completion Percentage'},
                      markers=True)
    else:
        teacher_data = merged_data[merged_data['teacher'] == selected_teacher]
        teacher_percentages = {}
        for milestone, status_col in milestones.items():
            teacher_percentages[milestone] = (teacher_data[status_col] == 'Complete').mean() * 100
        
        df_percentages = pd.DataFrame({
            'Milestone': list(teacher_percentages.keys()),
            'Teacher Percentage': list(teacher_percentages.values()),
            'Overall Percentage': [overall_percentages[m] for m in teacher_percentages.keys()]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_percentages['Milestone'], y=df_percentages['Teacher Percentage'],
                                 mode='lines+markers', name=f'{selected_teacher} Class'))
        fig.add_trace(go.Scatter(x=df_percentages['Milestone'], y=df_percentages['Overall Percentage'],
                                 mode='lines+markers', name='Overall Average', line=dict(dash='dash')))
        
        fig.update_layout(title=f'Milestone Completion: {selected_teacher} vs Overall Average')
    
    fig.update_layout(
        xaxis_title='Milestone',
        yaxis_title='Completion Percentage',
        yaxis_range=[0, 100],
        hovermode='x unified',
        plot_bgcolor=BACKGROUND_COLOR,
        paper_bgcolor=BACKGROUND_COLOR,
        font_color='black',
        margin=dict(t=40, b=40, l=40, r=40),  # Add some margin inside the graph
    )
    
    fig.update_traces(
        line=dict(color=PRIMARY_COLOR),
        marker=dict(color=PRIMARY_COLOR)
    )
    
    return fig

# Add classroom analytics
@app.callback(
    Output('classroom-analytics', 'children'),
    Input('teacher-dropdown', 'value')
)
def update_classroom_analytics(selected_teacher):
    if not selected_teacher:
        return ""
    
    teacher_data = merged_data[merged_data['teacher'] == selected_teacher]
    overall_percentages = {}
    teacher_percentages = {}
    
    for milestone, status_col in milestones.items():
        overall_percentages[milestone] = (merged_data[status_col] == 'Complete').mean() * 100
        teacher_percentages[milestone] = (teacher_data[status_col] == 'Complete').mean() * 100
    
    analytics = []
    for milestone in milestones:
        diff = teacher_percentages[milestone] - overall_percentages[milestone]
        color = 'green' if diff >= 0 else 'red'
        analytics.append(html.P([
            f"{milestone} completion: ",
            html.Span(f"{teacher_percentages[milestone]:.1f}% ", style={'fontWeight': 'bold'}),
            html.Span(f"({diff:+.1f}% compared to average)", style={'color': color})
        ]))
    
    return html.Div([
        html.H3("Classroom Analytics", style={'color': PRIMARY_COLOR}),
        *analytics
    ])

# Update the callback for student details
@app.callback(
    Output('student-details', 'children'),
    Input('milestone-completion-chart', 'clickData'),
    State('teacher-dropdown', 'value')
)
def display_student_details(clickData, selected_teacher):
    if not clickData:
        return "Click on a point to see details."
    
    point = clickData['points'][0]
    milestone = point['x']
    percentage = point['y']
    
    if selected_teacher:
        status_col = milestones[milestone]
        teacher_data = merged_data[merged_data['teacher'] == selected_teacher]
        completed_students = teacher_data[teacher_data[status_col] == 'Complete']
        incomplete_students = teacher_data[teacher_data[status_col] != 'Complete']
        
        details = [
            html.H4(f"{milestone} Milestone"),
            html.P(f"Completion Percentage: {percentage:.1f}%"),
            html.P(f"Number of students completed: {len(completed_students)}"),
            html.P(f"Number of students not completed: {len(incomplete_students)}"),
            html.P("Students who completed this milestone:"),
            html.Ul([html.Li(f"{row['first_name']} {row['last_name']} (ID: {row['student_id']})") for _, row in completed_students.iterrows()]),
            html.P("Students who have not completed this milestone:"),
            html.Ul([html.Li(f"{row['first_name']} {row['last_name']} (ID: {row['student_id']})") for _, row in incomplete_students.iterrows()])
        ]
    else:
        completed_students = merged_data[merged_data[milestones[milestone]] == 'Complete']
        
        details = [
            html.H4(f"{milestone} Milestone"),
            html.P(f"Overall Completion Percentage: {percentage:.1f}%"),
            html.P(f"Number of students completed: {len(completed_students)}"),
            html.P("Top 10 students who completed this milestone:"),
            html.Ul([html.Li(f"{row['first_name']} {row['last_name']} (ID: {row['student_id']})") for _, row in completed_students.head(10).iterrows()])
        ]
    
    return details

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)






