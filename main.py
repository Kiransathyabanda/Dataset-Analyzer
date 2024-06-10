import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go

st.set_page_config(page_title="Dataset Visualization", layout="wide")

st.markdown(
    """
    <style>
    .title {
        font-size:60px;
        font-weight: bold;
        color: #ff5733;
        text-align: center;
        padding: 20px;
        }
    </style>
    """
    , unsafe_allow_html=True)

st.markdown("<p class='title'>Dataset Visualization</p>", unsafe_allow_html=True)

@st.cache_data
def load_data(file):
    if file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        dataset = pd.read_excel(file)
    elif file.type == "text/csv":
        dataset = pd.read_csv(file)
    else:
        st.write("Unsupported file type. Please upload a .csv or .xlsx file.")
        return None, None, None

    column_data_types = dataset.dtypes
    index_name = dataset.index.name

    return dataset, column_data_types, index_name

def preprocess_data(dataset, selected_columns):
    for col in selected_columns:
        if dataset[col].dtype == "object":
            dataset[col] = pd.Categorical(dataset[col]).codes

    return dataset

def render_chart(dataset, chart_type, x_axis, y_axis):
    if chart_type == "line_chart":
        fig = px.line(dataset, x=x_axis, y=y_axis)
    elif chart_type == "area_chart":
        fig = px.area(dataset, x=x_axis, y=y_axis)
    elif chart_type == "bar_chart":
        fig = px.bar(dataset, x=x_axis, y=y_axis)
    elif chart_type == "scatter_plot":
        fig = px.scatter(dataset, x=x_axis, y=y_axis)
    elif chart_type == "histogram":
        fig = px.histogram(dataset, x=x_axis)
    elif chart_type == "box_plot":
        fig = px.box(dataset, x=x_axis, y=y_axis)
    elif chart_type == "violin_plot":
        fig = px.violin(dataset, x=x_axis, y=y_axis)
    else:
        st.write("Unsupported chart type.")
        return

    fig.update_layout(
        title=f"{chart_type.replace('_', ' ')} of {y_axis} vs {x_axis}" if y_axis else f"{chart_type.replace('_', ' ')} of {x_axis}",
        xaxis_title=x_axis,
        yaxis_title=y_axis if y_axis else None
    )

    st.plotly_chart(fig)

def display_summary_stats(dataset, selected_columns):
    st.subheader("Summary Statistics")
    stats = dataset[selected_columns].describe().transpose()
    st.write(stats)

    fig = make_subplots(rows=len(selected_columns), cols=2, subplot_titles=[f"Histogram - {col}" for col in selected_columns] + [f"Box Plot - {col}" for col in selected_columns])

    for i, col in enumerate(selected_columns):
        fig.add_trace(go.Histogram(x=dataset[col], nbinsx=30), row=i+1, col=1)
        fig.add_trace(go.Box(y=dataset[col], name=col), row=i+1, col=2)

    fig.update_layout(height=800, showlegend=False)
    st.plotly_chart(fig)

uploaded_files = st.file_uploader("Upload datasets", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files is not None:
    datasets = []
    column_data_types = {}
    index_names = []
    column_values = {}

    for file in uploaded_files:
        dataset, column_data_types_file, index_name = load_data(file)
        if dataset is not None:
            datasets.append(dataset)
            column_data_types.update(column_data_types_file)
            index_names.append(index_name)

            column_values_file = {}
            for col in dataset.columns:
                column_values_file[col] = set(dataset[col].unique())
            column_values.update(column_values_file)

    if len(datasets) > 0:
        combined_dataset = pd.concat(datasets, ignore_index=True)
        st.write("### Combined Dataset")
        st.write(combined_dataset)

        selected_columns = st.multiselect("Select columns for the chart", list(column_data_types.keys()), key='selected_columns')
        chart_type = st.selectbox("Select chart type", ["line_chart", "area_chart", "bar_chart", "scatter_plot", "histogram", "box_plot", "violin_plot"], key='chart_type')

        if st.button("Preprocess data", key='preprocess_button'):
            combined_dataset = preprocess_data(combined_dataset, selected_columns)

        if len(selected_columns) >= 1:
            if chart_type in ["histogram"]:
                x_axis = st.selectbox("Select a column", selected_columns, key='x_axis')
                if x_axis:
                    render_chart(combined_dataset, chart_type, x_axis, None)
            else:
                x_axis = st.selectbox("Select x-axis column", selected_columns, key='x_axis')
                y_axis = st.selectbox("Select y-axis column", selected_columns, key='y_axis')

                if x_axis and y_axis:
                    render_chart(combined_dataset, chart_type, x_axis, y_axis)
                else:
                    st.write("Please select both x and y axes for the chart.")
        else:
            st.write("Please select at least one column for the chart.")

        if st.checkbox("Show Summary Statistics", key='show_stats'):
            display_summary_stats(combined_dataset, selected_columns)

    else:
        st.write("Please upload at least one dataset.")
else:
    st.write("Please upload at least one dataset.")
