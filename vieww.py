import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json

# Your JSON data as a string (adjusted to be valid JSON)
json_str = """{
  "rest": 1,
  "name": "5X2 Rondo",
  "description": "Este ejercicio es un rondo 5x2, donde 5 jugadores (color amarillo) se posicionan en el exterior formando un pentágono, mientras 2 defensores (color rojo) se colocan en el interior. Los jugadores exteriores intentan mantener la posesión con un máximo de 2 toques, mientras los defensores intentan interceptar el balón. Si un defensor recupera el balón, intercambia posición con el atacante que lo perdió.",
  "field": "assets/fields/MEDIO_CAMPO.png",
  "duration": 2,
  "repetitions": 7,
  "players": [
    {"player": {"position": "RIGHT_WINGER"}, "color": "4294926946", "x": 0.22876783488347135, "y": 0.8141863623670055},
    {"player": {"position": "LEFT_MIDFIELDER"}, "color": "4294926946", "x": 0.18950768064474122, "y": 0.11779822220517971},
    {"player": {"position": "RIGHT_WINGER"}, "color": "4294926946", "x": 0.19207650191378906, "y": 0.8202605033322092},
    {"player": {"position": "LEFT_CENTRAL_BACK"}, "color": "4294926946", "x": 0.16668284397979555, "y": 0.17759274391621988},
    {"player": {"position": "LEFT_WINGER"}, "color": "4294926946", "x": 0.17160240507672336, "y": 0.12479484034038174},
    {"player": {"position": "RIGHT_BACK"}, "color": "4294169411", "x": 0.26719667809750264, "y": 0.3160362561329318},
    {"player": {"position": "DEFENSIVE_MIDFIELDER"}, "color": "4294169411", "x": 0.5426249245507866, "y": 0.4810887033550298}
  ],
  "items": [
    {"id": 1, "icon": "assets/football_items/ball/ball_1.png", "x": 0.43211815523856334, "y": 0.4458736606418333},
    {"id": 2, "icon": "assets/football_items/cone/cone-y.png", "x": 0.2085535246344489, "y": 0.782809231842327},
    {"id": 3, "icon": "assets/football_items/cone/cone-y.png", "x": 0.6727490052877056, "y": 0.5124012703119563},
    {"id": 4, "icon": "assets/football_items/cone/cone-y.png", "x": 0.40628737703245704, "y": 0.755711659857244}
  ]
}"""

# Parse the JSON string into a Python dictionary
data = json.loads(json_str)

# Function to convert the integer color string to a hex color code
def int_to_hex_color(color_int_str):
    color_int = int(color_int_str)
    hex_str = hex(color_int)[2:].zfill(8)
    # Use the last 6 digits for RGB (ignore potential alpha)
    return '#' + hex_str[-6:]

# Create the Matplotlib figure and axis
fig, ax = plt.subplots(figsize=(8, 8))

# Draw a simple field as a green rectangle (0,0) to (1,1)
field = patches.Rectangle((0, 0), 1, 1, linewidth=2, edgecolor='white', facecolor='green', alpha=0.5)
ax.add_patch(field)

# Set axis limits, aspect ratio, and title
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')
ax.set_title(data["name"])
ax.set_xlabel("Field Width")
ax.set_ylabel("Field Height")

# Plot each player on the field
for player in data["players"]:
    x = player["x"]
    y = player["y"]
    color = int_to_hex_color(player["color"])
    # Plot the player as a circle
    ax.scatter(x, y, s=300, color=color, edgecolors='black', zorder=5)
    # Label the player with their position
    ax.text(x, y, player["player"]["position"], ha='center', va='center', color='white', fontsize=9, zorder=6)

# Plot each item (e.g., ball or cones) as star markers
for item in data["items"]:
    x = item["x"]
    y = item["y"]
    ax.scatter(x, y, s=200, marker='*', color='yellow', edgecolors='black', zorder=5)
    ax.text(x, y, f"Item {item['id']}", ha='center', va='bottom', color='black', fontsize=9, zorder=6)

# Remove axis tick marks for a cleaner look
ax.set_xticks([])
ax.set_yticks([])

plt.show()
