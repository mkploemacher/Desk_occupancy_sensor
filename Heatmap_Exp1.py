import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

print("--- Start Script ---")

# 1. Data Inladen
# Pas dit pad eventueel aan als het bestand elders staat
file_path = '/Users/Maartenkiko/Desktop/Heatmap Exp/Heatmap_Experiment.csv'

if os.path.exists(file_path):
    print(f"Stap 1: Bestand gevonden op {file_path}")
    try:
        df = pd.read_csv(file_path, sep=';')
        print(f" - Data succesvol ingeladen! ({len(df)} rijen)")
    except Exception as e:
        print(f" - FOUT bij inladen CSV: {e}")
        exit()
else:
    print(f"FOUT: Bestand niet gevonden op: {file_path}")
    print("Check of de naam en map exact kloppen.")
    exit()

# 2. Data Schoonmaken
print("Stap 2: Data schoonmaken...")
def clean_decibel_value(val):
    val_str = str(val).replace('.', '')
    # Pak de eerste 2 cijfers als de dB waarde
    if len(val_str) >= 2:
        return int(val_str[:2])
    return None

df['decibel_clean'] = df['decibel_level'].apply(clean_decibel_value)
# Print even een voorbeeldje om te zien of het werkt
print(f" - Voorbeeld schoongemaakte data: {df['decibel_clean'].head().tolist()}")

# 3. Data Transformatie
print("Stap 3: Pivot table maken...")
heatmap_data = df.pivot_table(
    index='day_of_week', 
    columns='hour', 
    values='decibel_clean', 
    aggfunc='mean'
)

# 4. Plotten
print("Stap 4: Plot genereren...")
plt.figure(figsize=(14, 8))

sns.heatmap(heatmap_data, cmap='RdBu_r', annot=True, fmt=".0f", 
            cbar_kws={'label': 'Gemiddeld Decibel (dB)'})

plt.title('Geluidsniveau Heatmap: Uur vs Dag (Volledige Dataset)')
plt.xlabel('Uur van de dag (0-23)')
plt.ylabel('Dag van de week')

# Sla het bestand op (veiligste optie)
output_file = 'heatmap_resultaat.png'
plt.savefig(output_file)
print(f"Stap 5: Plot opgeslagen als '{output_file}' in dezelfde map als dit script.")

# Probeer het ook te tonen
print("Probeer plot te tonen...")
plt.show()

print("--- Script Klaar ---")