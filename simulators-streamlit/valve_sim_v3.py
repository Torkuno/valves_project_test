import streamlit as st
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import time

# Azure Blob Storage setup
connect_str = "DefaultEndpointsProtocol=https;AccountName=valvestatus;AccountKey=jjwKA+WoOe6BtHufikuu3gXpd8tksXWrMRY7txb9MUTA6nwKTd9VTQK7Mdpo+iZabzZbIz6jsWVh+ASt8vvNZA==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "valve-3"
blob_name = "sensor_data.json"

def get_blob_message():
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_data = blob_client.download_blob().readall()
        message = blob_data.decode('utf-8').strip()
        return message.lower()
    except Exception as e:
        print("Error:", e)
        return "error"

def main():
    st.title("Valve 3 Simulator")

    message = get_blob_message()
    if message == '{"condition": "open"}':
        st.markdown(f"<h1 style='color: green;'>{message.upper()}</h1>", unsafe_allow_html=True)
    elif message == '{"condition": "closed"}':
        st.markdown(f"<h1 style='color: red;'>{message.upper()}</h1>", unsafe_allow_html=True)
    else:
        st.write("Unknown message:", message)

    time.sleep(3)
    st.experimental_rerun()

if __name__ == "__main__":
    main()