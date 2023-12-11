import streamlit as st
from azure.iot.device import IoTHubDeviceClient, Message
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import json

# HEAD
st.set_page_config(
    page_title="Pipe Valve Dashboard",
    page_icon="👋",
)

pipeCS = {
    "valve-1": "HostName=cloud-final-project.azure-devices.net;DeviceId=valve-1;SharedAccessKey=d8LOzgbhgU31Z7k09ILmTXADBp1XHDYy/AIoTKtXyA4=",
    "valve-2": "HostName=cloud-final-project.azure-devices.net;DeviceId=valve-2;SharedAccessKey=t6ZwKzDn8K/iGgyJvktZPCA/AB2R4KBOLAIoTONAnvQ=",
    "valve-3": "HostName=cloud-final-project.azure-devices.net;DeviceId=valve-3;SharedAccessKey=a9Erx9/+KhWOm/mAWRzeE0fiSVFyrNG6GAIoTNPCCo4=",
    "valve-4": "HostName=cloud-final-project.azure-devices.net;DeviceId=valve-4;SharedAccessKey=y2PSh29338hh8gtrK8PTEqfp5dvaGH4mjAIoTKZ/CWY="
    }

pipeStates = {
    'valve-1': 'closed',
    'valve-2': 'closed',
    'valve-3': 'closed',
    'valve-4': 'closed'
}

storage_connection_string = "DefaultEndpointsProtocol=https;AccountName=valvestatus;AccountKey=jjwKA+WoOe6BtHufikuu3gXpd8tksXWrMRY7txb9MUTA6nwKTd9VTQK7Mdpo+iZabzZbIz6jsWVh+ASt8vvNZA==;EndpointSuffix=core.windows.net"
container_names = ["valve-1", "valve-2", "valve-3", "valve-4"]
blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)

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

    st.success(f"Condition: {condition} sent to {whichPipe}")

    client.disconnect()

    json_string = json.dumps(message_body)
    blob_name = "sensor_data.json"
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    blob_client = blob_service_client.get_blob_client(container=whichPipe, blob=blob_name)
    blob_client.upload_blob(json_string, overwrite=True)



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
    # Buttons for opening and closing the pipe
    btnOpenPipe = st.button('Open pipe')
    btnClosePipe = st.button('Close pipe')

    # Check if a button was pressed
    if btnOpenPipe or btnClosePipe:
        newState = 'open' if btnOpenPipe else 'closed'
        message_to_hub(pipeId, newState)
        pipeStates[pipeId] = newState

    # Display success message if available
    if 'pipeUpdate' in st.session_state:
        st.success(st.session_state['pipeUpdate'])
        del st.session_state['pipeUpdate']  # Clear the success message after displaying

    for container_name in container_names:
        container_client = blob_service_client.get_container_client(container_name)
        blobs = container_client.list_blobs()
        latest_blob = max(blobs, key=lambda blob: blob.last_modified)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=latest_blob.name)
        blob_content = blob_client.download_blob().readall()
        json_data = json.loads(blob_content)
        st.text(f"{container_name}: {json_data}")
