import streamlit as st
from azure.iot.device import IoTHubDeviceClient, Message
import json
# time is not typically recommended for use in Streamlit for delaying operations
# Streamlit's rerun feature should be used instead

# HEAD
st.set_page_config(
    page_title="pipe Dashboard",
    page_icon="👋",
)

pipeCS = {
    "pipe1": "HostName=cloud-final-project.azure-devices.net;DeviceId=valve-1;SharedAccessKey=d8LOzgbhgU31Z7k09ILmTXADBp1XHDYy/AIoTKtXyA4=",
    "pipe2": "HostName=cloud-final-project.azure-devices.net;DeviceId=valve-2;SharedAccessKey=t6ZwKzDn8K/iGgyJvktZPCA/AB2R4KBOLAIoTONAnvQ=",
    "pipe3": "HostName=cloud-final-project.azure-devices.net;DeviceId=valve-3;SharedAccessKey=a9Erx9/+KhWOm/mAWRzeE0fiSVFyrNG6GAIoTNPCCo4=",
    "pipe4": "HostName=cloud-final-project.azure-devices.net;DeviceId=valve-4;SharedAccessKey=y2PSh29338hh8gtrK8PTEqfp5dvaGH4mjAIoTKZ/CWY="
    }

# declare the variables for pipe status
pipeStates = {
    'pipe1': 'closed',
    'pipe2': 'closed',
    'pipe3': 'closed',
    'pipe4': 'closed'
}

def message_to_hub(whichPipe: str, condition: str):
    # connecting to IoT hub directly from Streamlit
    client = IoTHubDeviceClient.create_from_connection_string(pipeCS[whichPipe])
    client.connect()

    # constructing the message
    message_body = {
        "condition": condition
    }

    # sending message
    client.send_message(Message(str(message_body)))

    st.success(f"Message {message_body} sent to {whichPipe}")

    client.disconnect()

    # # connecting to iot hub directly from streamlit
    # client = IoTHubDeviceClient.create_from_connection_string(pipeCS[whichPipe])
    # client.connect()
    # # sending message
    # client.send_message(Message(message))
    # st.success(f"\nMessage {message} sent to {whichPipe}\n")
    # client.disconnect()


# BODY
# tab title
st.title('Pipe Control Dashboard')
# Make columns for UX design
col1, col2 = st.columns((1, 1))

# LEFT COL. The selectbox and Open / Close buttons
with col1:
    pipeId = st.selectbox('Select Pipe', list(pipeStates.keys()))
    # st.markdown(f'**State of {pipeId}: {pipeStates[pipeId]}**')

# RIGHT COL. pipe status and success message
with col2:
    btnOpenPipe = st.button('Open pipe')
    btnClosePipe = st.button('Close pipe')

    # Check if a button was pressed
    if btnOpenPipe or btnClosePipe:
        newState = 'open' if btnOpenPipe else 'closed'
        message_to_hub(pipeId, newState)
        pipeStates[pipeId] = newState
        # st.session_state['pipeUpdate'] = f'The {pipeId} is now {new_status}'

    # Display success message if available
    if 'pipeUpdate' in st.session_state:
        st.success(st.session_state['pipeUpdate'])