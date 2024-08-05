import streamlit as st

def feet_to_meters(feet):
    return feet * 0.3048

def mph_to_kmh(mph):
    return mph * 1.60934

def hectares_to_acres(hectares):
    return hectares / 0.404686

def calculate_coverage(machine_width, machine_speed, field_length, turn_around_time, operational_hours_per_day, operational_days_per_week):
    # Calculate coverage in metric units
    machine_width_metric = feet_to_meters(machine_width)
    machine_speed_metric = mph_to_kmh(machine_speed)
    field_length_metric = feet_to_meters(field_length)
    
    coverage_per_pass = (machine_width_metric * field_length_metric) / 10000
    time_per_pass = field_length_metric / (machine_speed_metric * 1000 / 60)
    total_turnarounds_per_hour = 60 / (time_per_pass + turn_around_time)
    time_spent_turning_around_per_hour = total_turnarounds_per_hour * turn_around_time
    coverage_per_hour = (60 / (time_per_pass + turn_around_time)) * coverage_per_pass
    coverage_per_day = coverage_per_hour * operational_hours_per_day
    total_turnarounds_per_day = total_turnarounds_per_hour * operational_hours_per_day
    time_spent_turning_around_per_day = time_spent_turning_around_per_hour * operational_hours_per_day / 60
    coverage_per_week = coverage_per_day * operational_days_per_week
    total_turnarounds_per_week = total_turnarounds_per_day * operational_days_per_week
    time_spent_turning_around_per_week = time_spent_turning_around_per_day * operational_days_per_week

    return {
        'coverage_per_hour': round(hectares_to_acres(coverage_per_hour), 1),
        'total_turnarounds_per_hour': round(total_turnarounds_per_hour, 1),
        'time_spent_turning_around_per_hour': round(time_spent_turning_around_per_hour, 1),
        'coverage_per_day': round(hectares_to_acres(coverage_per_day), 1),
        'total_turnarounds_per_day': round(total_turnarounds_per_day, 1),
        'time_spent_turning_around_per_day': round(time_spent_turning_around_per_day, 1),
        'coverage_per_week': round(hectares_to_acres(coverage_per_week), 1),
        'total_turnarounds_per_week': round(total_turnarounds_per_week, 1),
        'time_spent_turning_around_per_week': round(time_spent_turning_around_per_week, 1),
    }

st.title('Farm Implement Coverage Calculator')

# Create two columns
col1, col2 = st.columns(2)

# Define a function to update results
def update_results():
    results = calculate_coverage(
        st.session_state.machine_width, 
        st.session_state.machine_speed, 
        st.session_state.field_length, 
        st.session_state.turn_around_time, 
        st.session_state.operational_hours_per_day, 
        st.session_state.operational_days_per_week
    )
    with col2:
        st.header('Outputs (Imperial)')
        st.write(f"Machine Coverage per Hour: {results['coverage_per_hour']} acres")
        st.write(f"Total Turnarounds per Hour: {results['total_turnarounds_per_hour']}")
        st.write(f"Total Time per Hour Spent Turning Around: {results['time_spent_turning_around_per_hour']} minutes")
        st.write(f"Machine Coverage per Day: {results['coverage_per_day']} acres")
        st.write(f"Total Turnarounds per Day: {results['total_turnarounds_per_day']}")
        st.write(f"Total Time per Day Spent Turning Around: {results['time_spent_turning_around_per_day']} hours")
        st.write(f"Machine Coverage per Week: {results['coverage_per_week']} acres")
        st.write(f"Total Turnarounds per Week: {results['total_turnarounds_per_week']}")
        st.write(f"Total Time per Week Spent Turning Around: {results['time_spent_turning_around_per_week']} hours")

# Placeholders for inputs and outputs
with col1:
    st.header('Inputs (Imperial)')
    st.number_input('Machine Width (feet)', value=20.0, step=1.0, min_value=0.0, key='machine_width', on_change=update_results)
    st.number_input('Machine Speed (mph)', value=0.75, step=0.05, min_value=0.0, key='machine_speed', on_change=update_results)
    st.number_input('Field Length (feet)', value=2000.0, step=250.0, min_value=0.0, key='field_length', on_change=update_results)
    st.number_input('Turn Around Time (minutes)', value=3.0, step=0.5, min_value=0.0, key='turn_around_time', on_change=update_results)
    st.number_input('Operational Hours per Day (hours)', value=8.0, step=0.5, min_value=0.0, max_value=24.0, key='operational_hours_per_day', on_change=update_results)
    st.number_input('Operational Days per Week (days)', value=5, step=1, min_value=0, max_value=7, key='operational_days_per_week', on_change=update_results)

# Initial calculation to display default values
update_results()
