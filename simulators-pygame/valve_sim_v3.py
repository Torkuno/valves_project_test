from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import pygame
import time

# Pygame setup
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

def set_screen_color(color):
    if color == 'red':
        screen.fill((255, 0, 0))  # RGB for red
    elif color == 'green':
        screen.fill((0, 255, 0))  # RGB for green

    pygame.display.flip()

# Azure Blob Storage setup
connect_str = "DefaultEndpointsProtocol=https;AccountName=valvestatus;AccountKey=jjwKA+WoOe6BtHufikuu3gXpd8tksXWrMRY7txb9MUTA6nwKTd9VTQK7Mdpo+iZabzZbIz6jsWVh+ASt8vvNZA==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "valve-3"
blob_name = "sensor_data.json"

try:
    while True:
        # Get the latest message from Azure Blob Storage
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_data = blob_client.download_blob().readall()
        message = blob_data.decode('utf-8').strip()

        # Set screen color based on the message
        if message.lower() == '{"condition": "open"}':
            set_screen_color('green')
        elif message.lower() == '{"condition": "closed"}':
            set_screen_color('red')
        else:
            print("Unknown message:", message)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        time.sleep(5)  # Check for new messages every 5 seconds

except Exception as e:
    print("Error:", e)
    pygame.quit()