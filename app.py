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
    }

st.title('Carbon Implement Coverage Calculator')

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None

# Add toggle for metric/imperial
is_metric = st.checkbox('Use Metric Units')

# Create two columns
col1, col2 = st.columns(2)

# Create a single empty element for outputs in col2
output_container = col2.empty()

# Define a function to update results
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
    
    # Update the output container
    display_results()

def display_results():
    if st.session_state.results:
        output_container.write(
            f"""
            ### Outputs ({"Metric" if is_metric else "Imperial"})
            - Machine Coverage per Hour: {st.session_state.results['coverage_per_hour']} {'hectares' if is_metric else 'acres'}
            - Total Turnarounds per Hour: {st.session_state.results['total_turnarounds_per_hour']}
            - Total Time per Hour Spent Turning Around: {st.session_state.results['time_spent_turning_around_per_hour']} minutes
            - Machine Coverage per Day: {st.session_state.results['coverage_per_day']} {'hectares' if is_metric else 'acres'}
            - Total Turnarounds per Day: {st.session_state.results['total_turnarounds_per_day']}
            - Total Time per Day Spent Turning Around: {st.session_state.results['time_spent_turning_around_per_day']} hours
            - Machine Coverage per Week: {st.session_state.results['coverage_per_week']} {'hectares' if is_metric else 'acres'}
            - Total Turnarounds per Week: {st.session_state.results['total_turnarounds_per_week']}
            - Total Time per Week Spent Turning Around: {st.session_state.results['time_spent_turning_around_per_week']} hours
            """
        )

# Placeholders for inputs
with col1:
    st.header(f'Inputs ({"Metric" if is_metric else "Imperial"})')
    st.number_input('Machine Width (meters)' if is_metric else 'Machine Width (feet)', 
                    value=20.0 if not is_metric else 6.1, 
                    step=0.1, 
                    min_value=0.0, 
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
    st.number_input('Turn Around Time (minutes)', 
                    value=0.0, 
                    step=0.5, 
                    min_value=0.0, 
                    key='turn_around_time', 
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

# Initial calculation to display default values
update_results()