import sys

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

split_idx = -1
for i, line in enumerate(lines):
    if 'st.sidebar.markdown("### 🎛️ Analysis Controls")' in line:
        split_idx = i
        break

if split_idx == -1:
    print("Could not find split index")
    sys.exit(1)

head = lines[:split_idx]
tail = lines[split_idx:]

new_app = head + [
    "module_selection = st.sidebar.radio(\n",
    "    \"Environmental Domain\",\n",
    "    [\"💨 Air Quality Intelligence\", \"💧 Water Quality Intelligence\", \"🌍 Integrated Environmental Radar\"],\n",
    "    index=0\n",
    ")\n\n",
    "st.sidebar.markdown(\"---\")\n\n",
    "@st.cache_data\n",
    "def load_water_data():\n",
    "    csv_file = 'Indian_water_data.csv'\n",
    "    if not os.path.exists(csv_file):\n",
    "        return pd.DataFrame()\n",
    "    wdf = pd.read_csv(csv_file)\n",
    "    # Clean string columns\n",
    "    if 'State Name' in wdf.columns:\n",
    "        wdf['State Name'] = wdf['State Name'].astype(str).str.strip()\n",
    "    if 'Monitoring Location' in wdf.columns:\n",
    "        wdf['Monitoring Location'] = wdf['Monitoring Location'].astype(str).str.strip()\n",
    "    return wdf\n\n",
    "water_df = load_water_data()\n\n",
    "def render_air_dashboard():\n"
]

# Indent the tail for render_air_dashboard
for line in tail:
    if line.strip() == "":
        new_app.append("\n")
    else:
        new_app.append("    " + line)

new_app.append("\n\n")

with open('app_new.py', 'w', encoding='utf-8') as f:
    f.writelines(new_app)

print("Refactored app.py base logic successfully.")
