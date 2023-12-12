import streamlit as st
from azure.storage.blob import BlobServiceClient
import time

# Azure Blob Storage setup
connect_str = "DefaultEndpointsProtocol=https;AccountName=valvestatus;AccountKey=jjwKA+WoOe6BtHufikuu3gXpd8tksXWrMRY7txb9MUTA6nwKTd9VTQK7Mdpo+iZabzZbIz6jsWVh+ASt8vvNZA==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# Define your container and blob names for each valve
valve_info = {
    "valve1": {"container_name": "valve-1", "blob_name": "sensor_data.json"},
    "valve2": {"container_name": "valve-2", "blob_name": "sensor_data.json"},
    "valve3": {"container_name": "valve-3", "blob_name": "sensor_data.json"},
    "valve4": {"container_name": "valve-4", "blob_name": "sensor_data.json"}
}

def get_blob_message(container_name, blob_name):
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_data = blob_client.download_blob().readall()
        message = blob_data.decode('utf-8').strip()
        return message.lower()
    except Exception as e:
        st.error(f"Error in {blob_name}: " + str(e))
        return "error"

def display_valve_status(valve_name, container_name, blob_name):
    message = get_blob_message(container_name, blob_name)
    if message == '{"condition": "open"}':
        st.markdown(f"<h2 style='color: green;'>{valve_name.upper()} - {message.upper()}</h2>", unsafe_allow_html=True)
    elif message == '{"condition": "closed"}':
        st.markdown(f"<h2 style='color: red;'>{valve_name.upper()} - {message.upper()}</h2>", unsafe_allow_html=True)
    else:
        st.write(f"{valve_name.upper()} - Unknown message:", message)

def main():
    st.title("Azure Blob Valve Status Display")

    for valve, info in valve_info.items():
        display_valve_status(valve, info["container_name"], info["blob_name"])

    # Set a timer to rerun the app every few seconds
    time.sleep(3)
    st.experimental_rerun()

if __name__ == "__main__":
    main()