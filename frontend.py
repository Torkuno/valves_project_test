import streamlit as st
import time

st.set_page_config(
    page_title="Valve Dashboard",
    page_icon="👋",
)

# Function to send command to the backend
def send_valve_command(valveId, command):
    # Add logic to send commands to backend and Azure IoT Hub
    pass

def generate_temporary_success(message, seconds):
    successContainer = st.success(message)  # generate the success
    time.sleep(seconds)  # wait
    successContainer.empty()  # eliminate success

st.title('Valve Control Dashboard')

valveUpdate = ''

# Valve states dictionary
valves = {
    'Valve 1': 'closed',
    'Valve 2': 'closed',
    'Valve 3': 'closed',
    'Valve 4': 'closed',
}

# Make columns
col1, col2 = st.columns((1, 1))

# LEFT COLUMN: The selectbox and Open / Close buttons
with col1:
    valveId = st.selectbox('Select Valve', ['Valve 1', 'Valve 2', 'Valve 3', 'Valve 4'])
    btnOpenValve = st.button('Open Valve')
    btnCloseValve = st.button('Close Valve')

    if btnOpenValve:  # the open button is pressed
        send_valve_command(valveId, 'open')
        valves[valveId] = 'open'  # set the corresponding valve to open

    if btnCloseValve:  # the close button is pressed
        send_valve_command(valveId, 'closed')
        valves[valveId] = 'closed'  # set the corresponding valve to closed

# RIGHT COLUMN: Valve status and success message
with col2:
    st.markdown(f'**Status: {valves[valveId]}**')  # print the status of the corresponding valve
    valveUpdate = f'The valve is {valves[valveId]}'
    generate_temporary_success(valveUpdate, 1)  # print success message after either button
