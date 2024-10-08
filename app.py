import streamlit as st

def feet_to_meters(feet):
    return feet * 0.3048

def meters_to_feet(meters):
    return meters / 0.3048

def mph_to_kmh(mph):
    return mph * 1.60934

def kmh_to_mph(kmh):
    return kmh / 1.60934

def hectares_to_acres(hectares):
    return hectares * 2.47105

def acres_to_hectares(acres):
    return acres / 2.47105

def calculate_coverage(machine_width, machine_speed, field_length, turn_around_time, operational_hours_per_day, operational_days_per_week, is_metric):
    if not is_metric:
        # Convert imperial to metric for calculations
        machine_width = feet_to_meters(machine_width)
        machine_speed = mph_to_kmh(machine_speed)
        field_length = feet_to_meters(field_length)

    # Calculations in metric units
    coverage_per_pass = (machine_width * field_length) / 10000  # hectares
    time_per_pass = field_length / (machine_speed * 1000 / 60)  # minutes
    total_turnarounds_per_hour = 60 / (time_per_pass + turn_around_time)
    time_spent_turning_around_per_hour = total_turnarounds_per_hour * turn_around_time
    coverage_per_hour = (60 / (time_per_pass + turn_around_time)) * coverage_per_pass
    coverage_per_day = coverage_per_hour * operational_hours_per_day
    total_turnarounds_per_day = total_turnarounds_per_hour * operational_hours_per_day
    time_spent_turning_around_per_day = time_spent_turning_around_per_hour * operational_hours_per_day / 60
    coverage_per_week = coverage_per_day * operational_days_per_week
    total_turnarounds_per_week = total_turnarounds_per_day * operational_days_per_week
    time_spent_turning_around_per_week = time_spent_turning_around_per_day * operational_days_per_week

    total_hours_per_day = operational_hours_per_day
    total_hours_per_week = operational_hours_per_day * operational_days_per_week

    if not is_metric:
        # Convert results back to imperial if necessary
        coverage_per_hour = hectares_to_acres(coverage_per_hour)
        coverage_per_day = hectares_to_acres(coverage_per_day)
        coverage_per_week = hectares_to_acres(coverage_per_week)

    return {
        'coverage_per_hour': round(coverage_per_hour, 2),
        'total_turnarounds_per_hour': round(total_turnarounds_per_hour, 1),
        'time_spent_turning_around_per_hour': round(time_spent_turning_around_per_hour, 1),
        'coverage_per_day': round(coverage_per_day, 2),
        'total_turnarounds_per_day': round(total_turnarounds_per_day, 1),
        'time_spent_turning_around_per_day': round(time_spent_turning_around_per_day, 2),
        'coverage_per_week': round(coverage_per_week, 2),
        'total_turnarounds_per_week': round(total_turnarounds_per_week, 1),
        'time_spent_turning_around_per_week': round(time_spent_turning_around_per_week, 2),
        'total_hours_per_day': round(total_hours_per_day, 2),
        'total_hours_per_week': round(total_hours_per_week, 2),
    }

st.title('Carbon Implement Coverage Calculator')

# Initialize session state with default values
if 'machine_width' not in st.session_state:
    st.session_state.machine_width = 20.0  # Default in feet
if 'machine_speed' not in st.session_state:
    st.session_state.machine_speed = 0.75  # Default in mph
if 'field_length' not in st.session_state:
    st.session_state.field_length = 2000.0  # Default in feet
if 'turn_around_time' not in st.session_state:
    st.session_state.turn_around_time = 2.0
if 'operational_hours_per_day' not in st.session_state:
    st.session_state.operational_hours_per_day = 8.0
if 'operational_days_per_week' not in st.session_state:
    st.session_state.operational_days_per_week = 5

# Add toggle for metric/imperial
is_metric = st.checkbox('Use Metric Units')

# Force initial calculation of results
if 'results' not in st.session_state:
    st.session_state.results = calculate_coverage(
        st.session_state.machine_width,
        st.session_state.machine_speed,
        st.session_state.field_length,
        st.session_state.turn_around_time,
        st.session_state.operational_hours_per_day,
        st.session_state.operational_days_per_week,
        is_metric
    )

# Function to update results
def update_results():
    st.session_state.results = calculate_coverage(
        st.session_state.machine_width,
        st.session_state.machine_speed,
        st.session_state.field_length,
        st.session_state.turn_around_time,
        st.session_state.operational_hours_per_day,
        st.session_state.operational_days_per_week,
        is_metric
    )

# Function to display results
def display_results():
    if st.session_state.results:
        st.header(f"Outputs ({'Metric' if is_metric else 'Imperial'})")
        st.write(f"- Machine Coverage per Hour: {st.session_state.results['coverage_per_hour']} {'hectares' if is_metric else 'acres'}")
        st.write(f"- Machine Coverage per Day: {st.session_state.results['coverage_per_day']} {'hectares' if is_metric else 'acres'}")
        st.write(f"- Machine Coverage per Week: {st.session_state.results['coverage_per_week']} {'hectares' if is_metric else 'acres'}")
        st.write(f"- Total Hours Ran per Day: {st.session_state.results['total_hours_per_day']} hours")
        st.write(f"- Total Hours Ran per Week: {st.session_state.results['total_hours_per_week']} hours")
        
        with st.expander("Show Turnaround Details"):
            st.write(f"- Total Turnarounds per Hour: {st.session_state.results['total_turnarounds_per_hour']}")
            st.write(f"- Total Time per Hour Spent Turning Around: {st.session_state.results['time_spent_turning_around_per_hour']} minutes")
            st.write(f"- Total Turnarounds per Day: {st.session_state.results['total_turnarounds_per_day']}")
            st.write(f"- Total Time per Day Spent Turning Around: {st.session_state.results['time_spent_turning_around_per_day']} hours")
            st.write(f"- Total Turnarounds per Week: {st.session_state.results['total_turnarounds_per_week']}")
            st.write(f"- Total Time per Week Spent Turning Around: {st.session_state.results['time_spent_turning_around_per_week']} hours")

# Create two columns
col1, col2 = st.columns(2)

# Inputs in the first column
with col1:
    st.header(f'Inputs ({"Metric" if is_metric else "Imperial"})')
    st.number_input('Machine Width (meters)' if is_metric else 'Machine Width (feet)',
                    value=20.0 if not is_metric else 6.1,
                    step=20.0,
                    min_value=20.0,
                    key='machine_width',
                    on_change=update_results)
    st.number_input('Machine Speed (km/h)' if is_metric else 'Machine Speed (mph)',
                    value=0.75 if not is_metric else 1.2,
                    step=0.05,
                    min_value=0.0,
                    key='machine_speed',
                    on_change=update_results)
    st.number_input('Field Length (meters)' if is_metric else 'Field Length (feet)',
                    value=2000.0 if not is_metric else 609.6,
                    step=10.0,
                    min_value=0.0,
                    key='field_length',
                    on_change=update_results)
    st.number_input('Operational Hours per Day',
                    value=8.0,
                    step=0.5,
                    min_value=0.0,
                    max_value=24.0,
                    key='operational_hours_per_day',
                    on_change=update_results)
    st.number_input('Operational Days per Week',
                    value=5,
                    step=1,
                    min_value=0,
                    max_value=7,
                    key='operational_days_per_week',
                    on_change=update_results)

# Outputs in the second column
with col2:
    display_results()
    st.number_input('Turn Around Time (minutes)',
                    value=0.0,
                    step=0.5,
                    min_value=0.0,
                    key='turn_around_time',
                    on_change=update_results)

# Initial calculation to display default values
update_results()