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

def calculate_coverage(machine_width, machine_speed, field_length, turn_around_time, operational_hours_per_day, operational_days_per_week, is_metric, transportation_trips_per_day=0, transportation_time_per_trip=0):
    # Input validation
    if machine_width <= 0:
        raise ValueError("Machine width must be greater than 0")
    if machine_speed <= 0:
        raise ValueError("Machine speed must be greater than 0")
    if field_length <= 0:
        raise ValueError("Field length must be greater than 0")
    if turn_around_time < 0:
        raise ValueError("Turn around time cannot be negative")
    if operational_hours_per_day <= 0:
        raise ValueError("Operational hours per day must be greater than 0")
    if operational_days_per_week <= 0:
        raise ValueError("Operational days per week must be greater than 0")
    if transportation_trips_per_day < 0:
        raise ValueError("Transportation trips per day cannot be negative")
    if transportation_time_per_trip < 0:
        raise ValueError("Transportation time per trip cannot be negative")

    if not is_metric:
        # Convert imperial to metric for calculations
        machine_width = feet_to_meters(machine_width)
        machine_speed = mph_to_kmh(machine_speed)
        field_length = feet_to_meters(field_length)

    # Calculate transportation time per day
    transportation_time_per_day = transportation_trips_per_day * transportation_time_per_trip / 60  # hours
    
    # Adjust operational hours by subtracting transportation time
    effective_operational_hours_per_day = max(0, operational_hours_per_day - transportation_time_per_day)
    
    # Calculations in metric units
    coverage_per_pass = (machine_width * field_length) / 10000  # hectares
    time_per_pass = field_length / (machine_speed * 1000 / 60)  # minutes
    total_turnarounds_per_hour = 60 / (time_per_pass + turn_around_time)
    time_spent_turning_around_per_hour = total_turnarounds_per_hour * turn_around_time
    coverage_per_hour = (60 / (time_per_pass + turn_around_time)) * coverage_per_pass
    coverage_per_day = coverage_per_hour * effective_operational_hours_per_day
    total_turnarounds_per_day = total_turnarounds_per_hour * effective_operational_hours_per_day
    time_spent_turning_around_per_day = time_spent_turning_around_per_hour * effective_operational_hours_per_day / 60
    coverage_per_week = coverage_per_day * operational_days_per_week
    total_turnarounds_per_week = total_turnarounds_per_day * operational_days_per_week
    time_spent_turning_around_per_week = time_spent_turning_around_per_day * operational_days_per_week

    total_hours_per_day = operational_hours_per_day
    total_hours_per_week = operational_hours_per_day * operational_days_per_week
    effective_hours_per_day = effective_operational_hours_per_day
    effective_hours_per_week = effective_operational_hours_per_day * operational_days_per_week
    transportation_time_per_week = transportation_time_per_day * operational_days_per_week
    
    # Calculate coverage lost due to transportation
    coverage_lost_per_day = coverage_per_hour * transportation_time_per_day
    coverage_lost_per_week = coverage_lost_per_day * operational_days_per_week

    if not is_metric:
        # Convert results back to imperial if necessary
        coverage_per_hour = hectares_to_acres(coverage_per_hour)
        coverage_per_day = hectares_to_acres(coverage_per_day)
        coverage_per_week = hectares_to_acres(coverage_per_week)
        coverage_lost_per_day = hectares_to_acres(coverage_lost_per_day)
        coverage_lost_per_week = hectares_to_acres(coverage_lost_per_week)

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
        'effective_hours_per_day': round(effective_hours_per_day, 2),
        'effective_hours_per_week': round(effective_hours_per_week, 2),
        'transportation_time_per_day': round(transportation_time_per_day, 2),
        'transportation_time_per_week': round(transportation_time_per_week, 2),
        'coverage_lost_per_day': round(coverage_lost_per_day, 2),
        'coverage_lost_per_week': round(coverage_lost_per_week, 2),
    }

st.title('Carbon Coverage Calculator')

# Add this to the initialization block at the beginning, with the other session state initializations
if 'results' not in st.session_state:
    st.session_state.results = None

# Initialize session state with default values in imperial units
if 'is_metric' not in st.session_state:
    st.session_state.is_metric = False
if 'machine_width_imperial' not in st.session_state:
    st.session_state.machine_width_imperial = 20.0
if 'machine_speed_imperial' not in st.session_state:
    st.session_state.machine_speed_imperial = 0.75
if 'field_length_imperial' not in st.session_state:
    st.session_state.field_length_imperial = 2000.0

# Function to handle metric toggle
def on_metric_toggle():
    st.session_state.is_metric = not st.session_state.is_metric
    update_results()

# Add toggle for metric/imperial
is_metric = st.checkbox('Use Metric Units', value=st.session_state.is_metric, on_change=on_metric_toggle)

# Function to update results
def update_results():
    # Get the current values based on unit system
    if st.session_state.is_metric:
        machine_width = st.session_state.machine_width_imperial * 0.3048
        machine_speed = st.session_state.machine_speed_imperial * 1.60934
        field_length = st.session_state.field_length_imperial * 0.3048
    else:
        machine_width = st.session_state.machine_width_imperial
        machine_speed = st.session_state.machine_speed_imperial
        field_length = st.session_state.field_length_imperial

    st.session_state.results = calculate_coverage(
        machine_width,
        machine_speed,
        field_length,
        st.session_state.get('turn_around_time', 2.0),
        st.session_state.get('operational_hours_per_day', 8.0),
        st.session_state.get('operational_days_per_week', 5),
        st.session_state.is_metric,
        st.session_state.get('transportation_trips_per_day', 0),
        st.session_state.get('transportation_time_per_trip', 60.0)
    )

# Function to handle input changes
def on_input_change():
    # Store values in imperial and update results
    if st.session_state.is_metric:
        st.session_state.machine_width_imperial = meters_to_feet(st.session_state.machine_width)
        st.session_state.machine_speed_imperial = kmh_to_mph(st.session_state.machine_speed)
        st.session_state.field_length_imperial = meters_to_feet(st.session_state.field_length)
    else:
        st.session_state.machine_width_imperial = st.session_state.machine_width
        st.session_state.machine_speed_imperial = st.session_state.machine_speed
        st.session_state.field_length_imperial = st.session_state.field_length
    
    update_results()

# And modify the display_results function to handle None values more gracefully
def display_results():
    if hasattr(st.session_state, 'results') and st.session_state.results is not None:
        st.header(f"Outputs ({'Metric' if is_metric else 'Imperial'})")
        st.write(f"- Machine Coverage per Hour: {st.session_state.results['coverage_per_hour']} {'hectares' if is_metric else 'acres'}")
        st.write(f"- Machine Coverage per Day: {st.session_state.results['coverage_per_day']} {'hectares' if is_metric else 'acres'}")
        st.write(f"- Machine Coverage per Week: {st.session_state.results['coverage_per_week']} {'hectares' if is_metric else 'acres'}")
        st.write(f"- Scheduled Hours per Day: {st.session_state.results['total_hours_per_day']} hours")
        st.write(f"- Effective Operating Hours per Day: {st.session_state.results['effective_hours_per_day']} hours")
        st.write(f"- Scheduled Hours per Week: {st.session_state.results['total_hours_per_week']} hours")
        st.write(f"- Effective Operating Hours per Week: {st.session_state.results['effective_hours_per_week']} hours")
        
        with st.expander("Show Turnaround Details"):
            st.write(f"- Total Turnarounds per Hour: {st.session_state.results['total_turnarounds_per_hour']}")
            st.write(f"- Total Time per Hour Spent Turning Around: {st.session_state.results['time_spent_turning_around_per_hour']} minutes")
            st.write(f"- Total Turnarounds per Day: {st.session_state.results['total_turnarounds_per_day']}")
            st.write(f"- Total Time per Day Spent Turning Around: {st.session_state.results['time_spent_turning_around_per_day']} hours")
            st.write(f"- Total Turnarounds per Week: {st.session_state.results['total_turnarounds_per_week']}")
            st.write(f"- Total Time per Week Spent Turning Around: {st.session_state.results['time_spent_turning_around_per_week']} hours")
        
        if st.session_state.results['transportation_time_per_day'] > 0:
            with st.expander("Show Transportation Details"):
                st.write(f"- Transportation Time per Day: {st.session_state.results['transportation_time_per_day']} hours")
                st.write(f"- Transportation Time per Week: {st.session_state.results['transportation_time_per_week']} hours")
                st.write(f"- Transportation Trips per Day: {st.session_state.get('transportation_trips_per_day', 0)}")
                st.write(f"- Transportation Time per Trip: {st.session_state.get('transportation_time_per_trip', 60.0)} minutes")
                st.write(f"- Coverage Lost per Day: {st.session_state.results['coverage_lost_per_day']} {'hectares' if is_metric else 'acres'}")
                st.write(f"- Coverage Lost per Week: {st.session_state.results['coverage_lost_per_week']} {'hectares' if is_metric else 'acres'}")

# Create two columns
col1, col2 = st.columns(2)

# Calculate displayed values based on current unit system
displayed_machine_width = (
    feet_to_meters(st.session_state.machine_width_imperial) if is_metric 
    else st.session_state.machine_width_imperial
)
displayed_machine_speed = (
    mph_to_kmh(st.session_state.machine_speed_imperial) if is_metric 
    else st.session_state.machine_speed_imperial
)
displayed_field_length = (
    feet_to_meters(st.session_state.field_length_imperial) if is_metric 
    else st.session_state.field_length_imperial
)

# Inputs in the first column
with col1:
    st.header(f'Inputs ({"Metric" if is_metric else "Imperial"})')
    st.number_input('Machine Width (meters)' if is_metric else 'Machine Width (feet)',
                    value=displayed_machine_width,
                    step=0.1,
                    min_value=2.0 if not is_metric else 0.6,
                    key='machine_width',
                    on_change=on_input_change)
    st.number_input('Machine Speed (km/h)' if is_metric else 'Machine Speed (mph)',
                    value=displayed_machine_speed,
                    step=0.05,
                    min_value=0.0,
                    key='machine_speed',
                    on_change=on_input_change)
    st.number_input('Field Length (meters)' if is_metric else 'Field Length (feet)',
                    value=displayed_field_length,
                    step=10.0,
                    min_value=0.0,
                    key='field_length',
                    on_change=on_input_change)
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
if 'results' not in st.session_state:
    update_results()

# Ensure results are calculated before display
update_results()

# Outputs in the second column
with col2:
    display_results()
    st.number_input('Turn Around Time (minutes)',
                    value=2.0,
                    step=0.5,
                    min_value=0.0,
                    key='turn_around_time',
                    on_change=update_results)
    
    st.subheader('Transportation Settings')
    st.number_input('Transportation Trips per Day',
                    value=0,
                    step=1,
                    min_value=0,
                    key='transportation_trips_per_day',
                    on_change=update_results)
    st.number_input('Transportation Time per Trip (minutes)',
                    value=60.0,
                    step=15.0,
                    min_value=0.0,
                    key='transportation_time_per_trip',
                    on_change=update_results)