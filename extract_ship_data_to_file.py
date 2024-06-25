import json
from cosmoteer_save_tools import Ship, decode_ship_data

data_str = decode_ship_data("ship.png")
f = open("data.json", "w")
f.write(data_str)
f.close()