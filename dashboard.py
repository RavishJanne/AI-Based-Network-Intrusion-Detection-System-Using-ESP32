import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from micromlgen import port
import os

# --- 1. Dataset Generation ---
# This automatically creates the CSV if you haven't saved it manually
csv_filename = 'esp32_network_traffic.csv'
if not os.path.exists(csv_filename):
    print(f"Creating dataset: {csv_filename}...")
    csv_data = """time_interval_ms,packet_rate_per_sec,payload_size_bytes,failed_auth_attempts,label
2500,2,128,0,Normal
1800,5,256,0,Normal
3200,1,64,0,Normal
2000,4,128,0,Normal
1500,8,512,0,Normal
2800,2,128,0,Normal
1200,10,256,1,Normal
3500,1,64,0,Normal
2200,3,128,0,Normal
1900,6,256,0,Normal
10,180,32,0,Attack_DoS
5,220,32,0,Attack_DoS
12,150,64,0,Attack_DoS
8,200,32,0,Attack_DoS
20,120,64,0,Attack_DoS
15,160,32,0,Attack_DoS
2100,3,2048,0,Attack_Payload
2400,2,4096,0,Attack_Payload
1800,4,1024,0,Attack_Payload
500,25,64,5,Attack_BruteForce
400,30,64,8,Attack_BruteForce
450,28,128,6,Attack_BruteForce
100,60,64,12,Attack_BruteForce
2600,2,128,0,Normal
1700,7,256,0,Normal
9,190,32,0,Attack_DoS
2300,3,2048,0,Attack_Payload
420,29,64,7,Attack_BruteForce
1600,9,512,0,Normal
3000,1,64,0,Normal"""
    
    with open(csv_filename, 'w') as f:
        f.write(csv_data)

# --- 2. Load the Dataset ---
print("Loading data...")
data = pd.read_csv(csv_filename)

# Separate features (Inputs) and labels (Outputs)
# Order is critical here: it must match the array in your ESP32 code!
X = data[['time_interval_ms', 'packet_rate_per_sec', 'payload_size_bytes', 'failed_auth_attempts']].values
y = data['label'].values

# --- 3. Train the Model ---
print("Training Decision Tree Classifier...")
# We use max_depth=4 to keep the resulting C++ code very small and fast on the ESP32
classifier = DecisionTreeClassifier(max_depth=4, random_state=42)
classifier.fit(X, y)

# --- 4. Export to C++ via micromlgen ---
print("Converting Python model to C++...")
# The port function generates the C++ header file string
cpp_code = port(classifier, classname="NetworkClassifier")

# Save the generated code to a .h file
header_filename = "NetworkClassifier.h"
with open(header_filename, "w") as f:
    f.write(cpp_code)

print(f"\n✅ Success! Model trained and saved as '{header_filename}'.")
print("Next step: Drag this file into your Arduino sketch folder.")