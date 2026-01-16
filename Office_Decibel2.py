import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------
# STAP 1: DATA GENEREREN (Met specifieke patronen)
# ---------------------------------------------------------
print("1. Data genereren...")
np.random.seed(42) # Voor reproduceerbare 'random' getallen

data = []
# We simuleren een werkdag van 08:00 tot 18:00
hours = range(8, 19) 
rooms = ["Open vloer", "Vergaderruimte", "Studeerruimte", "Kantine"]

for hour in hours:
    for room in rooms:
        
        # --- LOGICA PER RUIMTE ---
        
        if room == "Open vloer":
            # Constant druk en rumoerig
            occupancy = np.random.randint(20, 30)
            base_noise = 65 
            
        elif room == "Studeerruimte":
            # Hele dag rustig, weinig mensen
            occupancy = np.random.randint(1, 5)
            base_noise = 35 
            
        elif room == "Vergaderruimte":
            # Ochtend (9-11) en Middag (14-16) sessies
            if (9 <= hour <= 11) or (14 <= hour <= 16):
                occupancy = np.random.randint(6, 12)
                base_noise = 60 # Vergadering bezig
            else:
                occupancy = 0
                base_noise = 30 # Lege ruimte
                
        elif room == "Kantine":
            # Piek tijdens lunch (12-13), anders rustig
            if hour == 12 or hour == 13:
                occupancy = np.random.randint(30, 50)
                base_noise = 70 # Lunchdrukte
            else:
                occupancy = np.random.randint(0, 5)
                base_noise = 35 # Koffiepauze of leeg
        
        # Voeg een klein beetje variatie toe zodat het niet te "nep" lijkt
        noise = base_noise + np.random.normal(0, 2)
        
        # Maak timestamp (datum van vandaag + uur)
        timestamp = pd.Timestamp.now().normalize() + pd.Timedelta(hours=hour)
        
        data.append([timestamp, hour, room, occupancy, round(noise, 1)])

# Maak DataFrame
df = pd.DataFrame(data, columns=['timestamp', 'hour', 'room_type', 'occupancy', 'decibel_level'])

# Sla op als CSV
csv_filename = 'kantoor_geluid_data.csv'
df.to_csv(csv_filename, index=False, sep=';')
print(f"   -> CSV opgeslagen als '{csv_filename}'")


# ---------------------------------------------------------
# STAP 2: HEATMAP MAKEN
# ---------------------------------------------------------
print("2. Heatmap genereren...")

# Tabel 1: Voor de KLEUR (Decibel)
pivot_decibel = df.pivot_table(index='room_type', columns='hour', values='decibel_level', aggfunc='mean')

# Tabel 2: Voor de TEKST (Occupancy / Aantal mensen)
pivot_occupancy = df.pivot_table(index='room_type', columns='hour', values='occupancy', aggfunc='mean')

# Zorg voor een logische volgorde van de kamers op de Y-as
custom_order = ["Open vloer", "Kantine", "Vergaderruimte", "Studeerruimte"]
pivot_decibel = pivot_decibel.reindex(custom_order)
pivot_occupancy = pivot_occupancy.reindex(custom_order)

# Plotten
plt.figure(figsize=(14, 7))

sns.heatmap(data=pivot_decibel, 
            annot=pivot_occupancy, # Dit zet de getallen (mensen) in de vakjes
            fmt=".0f",             # Geen decimalen bij aantal mensen
            cmap="RdBu_r",         # Blauw = Stil, Rood = Luid
            linewidths=.5,         # Witte lijntjes tussen de blokken
            cbar_kws={'label': 'Geluidsniveau (dB)'})

plt.title('Geluidsniveau per Ruimte (Kleur = dB, Getal = Aantal Mensen)')
plt.xlabel('Uur van de dag')
plt.ylabel('Type Ruimte')

# Sla op als PNG
output_filename = 'kantoor_heatmap.png'
plt.savefig(output_filename)
print(f"   -> Plaatje opgeslagen als '{output_filename}'")

plt.show()
print("Klaar!")