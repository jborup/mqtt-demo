FROM python:3.9-slim

# Install MQTT client library
RUN pip install paho-mqtt requests

# Add script
ADD mqtt_script.py /mqtt_script.py

# Run script
CMD ["python", "/mqtt_script.py"]
