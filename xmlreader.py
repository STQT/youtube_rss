import xml.etree.ElementTree as ET
import json

# Parse the XML file
tree = ET.parse('youtube_subs.xml')
root = tree.getroot()

# Initialize an empty dictionary to store xmlUrl values
xmlUrls = {}

# Iterate through the outline elements and extract xmlUrl attributes
for outline in root.findall('.//outline[@xmlUrl]'):
    xmlUrl = outline.get('xmlUrl')
    channel_id = xmlUrl.split('=')[-1]
    xmlUrls[channel_id] = []

# Save the dictionary to a JSON file
with open('db.json', 'w') as json_file:
    json.dump(xmlUrls, json_file, indent=4)

print("Data saved to db.json")
