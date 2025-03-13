import json
import random

def generate_drill_examples(num_examples=30):
    """Generate properly structured football drill examples for fine-tuning"""
    
    examples = []
    
    # Define common drill types with proper player distributions
    drill_types = [
        {"name": "3x3 rondo", "focus": "RONDO", "possession": 3, "defense": 3, "neutrals": 0},
        {"name": "4x2 rondo", "focus": "RONDO", "possession": 4, "defense": 2, "neutrals": 0},
        {"name": "5x2 rondo", "focus": "RONDO", "possession": 5, "defense": 2, "neutrals": 0},
        {"name": "6x3 rondo", "focus": "RONDO", "possession": 6, "defense": 3, "neutrals": 0},
        {"name": "4x4 possession", "focus": "BALL-POSSESSION", "possession": 4, "defense": 4, "neutrals": 0},
        {"name": "5x5+2 possession", "focus": "BALL-POSSESSION", "possession": 5, "defense": 5, "neutrals": 2},
        {"name": "3x3+1 transition", "focus": "TRANSITION-GAMES", "possession": 3, "defense": 3, "neutrals": 1},
        {"name": "4x3 finishing", "focus": "FINISHINGS", "possession": 4, "defense": 3, "neutrals": 0},
        {"name": "2x2+GK crossing", "focus": "FINISHINGS", "possession": 2, "defense": 2, "neutrals": 1}, # GK is neutral
        {"name": "3x2 counter-attack", "focus": "TRANSITION-GAMES", "possession": 3, "defense": 2, "neutrals": 0},
    ]
    
    fields = [
        "assets/fields/CUADRADO_CENTRAL.png",
        "assets/fields/MEDIO_CAMPO.png",
        "assets/fields/CAMPO_VACIO.png",
        "assets/fields/ZONA_ENTRENAMIENTO2.png"
    ]
    
    # Generate player positions on a grid
    def generate_positions(num_players, area="outer", center_bias=0.5):
        positions = []
        if area == "outer":
            # Generate positions around the perimeter
            for i in range(num_players):
                angle = (i / num_players) * 2 * 3.14159
                radius = random.uniform(0.35, 0.45)
                x = 0.5 + radius * (0.9 + 0.2 * random.random()) * (1 if random.random() > center_bias else -1) * random.uniform(0.8, 1.0)
                y = 0.5 + radius * (0.9 + 0.2 * random.random()) * (1 if random.random() > center_bias else -1) * random.uniform(0.8, 1.0)
                # Keep within bounds
                x = max(0.1, min(0.9, x))
                y = max(0.1, min(0.9, y))
                positions.append((x, y))
        else:
            # Generate positions in the center
            for i in range(num_players):
                x = 0.5 + (random.random() - 0.5) * 0.5
                y = 0.5 + (random.random() - 0.5) * 0.5
                positions.append((x, y))
        return positions
    
    # Player positions for different formations
    player_positions = {
        "GOALKEEPER": ["GOALKEEPER"],
        "DEFENSE": ["RIGHT_BACK", "LEFT_BACK", "CENTRAL_BACK", "RIGHT_CENTRAL_BACK", "LEFT_CENTRAL_BACK"],
        "MIDFIELD": ["DEFENSIVE_MIDFIELDER", "OFFENSIVE_MIDFIELDER", "RIGHT_MIDFIELDER", "LEFT_MIDFIELDER"],
        "ATTACK": ["RIGHT_WINGER", "LEFT_WINGER", "FORDWARD", "STRIKER"]
    }
    
    # Colors for different team roles
    colors = {
        "possession": ["4294926946", "4293889850"],  # Yellow/Gold colors
        "defense": ["4294169411", "4288570111"],     # Red colors
        "neutral": ["4278190080", "4284665855"]      # Blue/Green colors
    }
    
    # Descriptions templates for different drill types
    descriptions = {
        "RONDO": [
            "Este ejercicio es un rondo {0}x{1}, donde {0} jugadores (color amarillo) se posicionan en el exterior formando un {2}, mientras {1} defensores (color rojo) se colocan en el interior. Los jugadores exteriores intentan mantener la posesión con un máximo de 2 toques, mientras los defensores intentan interceptar el balón. Si un defensor recupera el balón, intercambia posición con el atacante que lo perdió.",
            "Rondo {0}x{1} donde los {0} jugadores exteriores (amarillos) deben mantener la posesión del balón frente a {1} defensores (rojos) en el centro. Los jugadores exteriores se colocan en forma de {2} y deben realizar pases precisos, preferiblemente a un toque. Si un defensor intercepta el balón, cambia su posición con el jugador que lo perdió.",
            "Un rondo clásico {0}x{1} donde {0} jugadores de posesión (amarillos) forman un {2} en el exterior y {1} defensores (rojos) trabajan en el interior para recuperar el balón. El objetivo para el equipo en posesión es completar el mayor número de pases posible, mientras que los defensores buscan interceptar y forzar errores."
        ],
        "BALL-POSSESSION": [
            "Ejercicio de posesión {0}x{1}{3} en espacio reducido. {0} jugadores (color amarillo) intentan mantener la posesión frente a {1} defensores (color rojo){4}. El objetivo es completar un mínimo de 5 pases consecutivos para obtener un punto. Los jugadores están limitados a 2 toques máximo.",
            "Juego de posesión {0}x{1}{3} donde el equipo amarillo ({0} jugadores) busca mantener el balón frente al equipo rojo ({1} jugadores){4}. Se trabaja en un espacio delimitado con énfasis en la circulación rápida y los desmarques. Se puntúa al completar 8 pases consecutivos.",
            "Ejercicio de conservación {0}x{1}{3} donde los {0} jugadores de amarillo deben mantener la posesión ante la presión de {1} defensores de rojo{4}. El espacio de juego está limitado para aumentar la intensidad y forzar decisiones rápidas."
        ],
        "TRANSITION-GAMES": [
            "Ejercicio de transición {0}x{1}{3} donde el equipo en posesión ({0} jugadores amarillos) ataca hacia la portería, mientras que los defensores ({1} jugadores rojos) intentan recuperar el balón{4}. Una vez que recuperan, deben realizar una transición rápida hacia la portería contraria.",
            "Juego de transición {0}x{1}{3} con énfasis en el paso de defensa a ataque. Los {0} jugadores amarillos comienzan con el balón, mientras los {1} defensores rojos presionan para recuperarlo{4}. Al recuperar, deben atacar rápidamente hacia la portería contraria.",
            "Transición {0}x{1}{3} donde el equipo amarillo ({0} jugadores) inicia con posesión y el equipo rojo ({1} jugadores) debe recuperar el balón{4}. Al producirse la recuperación, el equipo rojo debe atacar rápidamente mientras el amarillo realiza una transición defensiva."
        ],
        "FINISHINGS": [
            "Ejercicio de finalización {0}x{1}{3} donde los atacantes ({0} jugadores amarillos) buscan crear y concretar ocasiones de gol ante la oposición de {1} defensores (rojos){4}. El énfasis está en la precisión de los centros y la definición en el área.",
            "Drill de finalización {0}x{1}{3} centrado en la creación de situaciones de gol. El equipo atacante ({0} jugadores amarillos) debe trabajar en conjunto para superar a los {1} defensores (rojos){4} y finalizar con éxito en portería.",
            "Entrenamiento de finalización {0}x{1}{3} donde los {0} jugadores ofensivos (amarillos) crean situaciones de gol contra {1} defensores (rojos){4}. Se trabaja la precisión en el último pase y la eficacia en el remate."
        ]
    }
    
    shapes = {
        3: "triángulo",
        4: "cuadrado",
        5: "pentágono",
        6: "hexágono"
    }
    
    for i in range(num_examples):
        # Choose a random drill type
        drill = random.choice(drill_types)
        field = random.choice(fields)
        
        # Generate positions
        possession_positions = generate_positions(drill["possession"], "outer")
        defense_positions = generate_positions(drill["defense"], "inner")
        neutral_positions = generate_positions(drill["neutrals"], "inner", 0.2) if drill["neutrals"] > 0 else []
        
        # Format description placeholders
        neutral_text = f"+{drill['neutrals']}" if drill["neutrals"] > 0 else ""
        neutral_desc = f", con {drill['neutrals']} jugador{'es' if drill['neutrals'] > 1 else ''} neutral{'es' if drill['neutrals'] > 1 else ''} (color azul) que apoyan al equipo en posesión" if drill["neutrals"] > 0 else ""
        
        shape = shapes.get(drill["possession"], "círculo")
        
        # Choose a random description template and format it
        description_template = random.choice(descriptions[drill["focus"]])
        description = description_template.format(
            drill["possession"], 
            drill["defense"], 
            shape, 
            neutral_text, 
            neutral_desc
        )
        
        # Build the players array
        players = []
        
        # Possession players
        possession_color = colors["possession"][0]
        for idx, (x, y) in enumerate(possession_positions):
            position_type = random.choice(["MIDFIELD", "ATTACK"] if idx % 2 == 0 else ["DEFENSE", "MIDFIELD"])
            position = random.choice(player_positions[position_type])
            players.append({
                "player": {"position": position},
                "color": possession_color,
                "x": x,
                "y": y
            })
        
        # Defense players
        defense_color = colors["defense"][0]
        for idx, (x, y) in enumerate(defense_positions):
            position_type = random.choice(["DEFENSE", "MIDFIELD"])
            position = random.choice(player_positions[position_type])
            players.append({
                "player": {"position": position},
                "color": defense_color,
                "x": x,
                "y": y
            })
        
        # Neutral players
        if drill["neutrals"] > 0:
            neutral_color = colors["neutral"][0]
            for idx, (x, y) in enumerate(neutral_positions):
                position_type = "GOALKEEPER" if drill["focus"] == "FINISHINGS" and idx == 0 else random.choice(["MIDFIELD", "DEFENSE"])
                position = random.choice(player_positions[position_type if position_type != "GOALKEEPER" else "GOALKEEPER"])
                players.append({
                    "player": {"position": position},
                    "color": neutral_color,
                    "x": x,
                    "y": y
                })
        
        # Add equipment items (ball, cones)
        items = []
        # Add a ball
        items.append({
            "id": 1,
            "icon": "assets/football_items/ball/ball_1.png",
            "x": 0.5 + (random.random() - 0.5) * 0.3,
            "y": 0.5 + (random.random() - 0.5) * 0.3
        })
        
        # Add some cones
        for i in range(2, 5):
            items.append({
                "id": i,
                "icon": "assets/football_items/cone/cone-y.png",
                "x": 0.2 + random.random() * 0.6,
                "y": 0.2 + random.random() * 0.6
            })
        
        # Create the full drill specification
        drill_spec = {
            "rest": random.choice([0, 1]),
            "name": drill["name"].title(),
            "description": description,
            "field": field,
            "duration": random.randint(1, 5),
            "repetitions": random.randint(3, 10),
            "players": players,
            "items": items
        }
        
        # Create the chat format for fine-tuning
        example = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert football/soccer coach who creates detailed training drills. Always output in JSON format exactly as requested. For NxM drills, always use exactly N players of one color for the possession team and M players of another color for the defense team. For rondos, the first number represents players on the outside (possession) and the second number represents defenders in the middle."
                },
                {
                    "role": "user",
                    "content": f"Create a football drill specification for '{drill['name']}' with focus on {drill['focus']}"
                },
                {
                    "role": "assistant",
                    "content": json.dumps(drill_spec, ensure_ascii=False)
                }
            ]
        }
        
        examples.append(example)
    
    return examples

def save_examples_to_jsonl(examples, filename='structured_football_drills.jsonl'):
    """Save the examples to a JSONL file for fine-tuning"""
    with open(filename, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    print(f"Successfully saved {len(examples)} examples to {filename}")

# Generate and save the examples
examples = generate_drill_examples(40)  # Generate 40 examples
save_examples_to_jsonl(examples)