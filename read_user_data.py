import pandas as pd
from colorama import Fore, Style

# requires openpyxl

def read_user_data():
    print(f"{Fore.YELLOW}Reading your specification sheet...{Style.RESET_ALL}")
    user_data = pd.read_excel('./SystemData/System_Specifications.xlsx', index_col=None)

    print(f"{Fore.GREEN}Done!{Style.RESET_ALL}")
    return float(user_data['Lattitude (°)'][0]), float(user_data['Longitude (°)'][0]), float(user_data['Elevation (m)'][0]), \
           float(user_data['Orientation (°)'][0]), float(user_data['Inclination (°)'][0]), \
           int(user_data['Calib vertex short'][0]), int(user_data['Calib vertex long'][0]), float(user_data['Calib square size (mm)'][0]), \
           int(user_data['Start year'][0]), int(user_data['End year'][0]), \
           float(user_data['Solar panel peak wattage'][0]), float(user_data['Converter efficiency (%)'][0]), \
           float(user_data['Charge efficiency (%)'][0]), float(user_data['Discharge efficiency (%)'][0]), float(user_data['Max SOC (%)'][0]), float(user_data['Min SOC (%)'][0]), \
           float(user_data['Batt nominal capacity (Ah)'][0]), float(user_data['Batt nominal voltage (V)'][0])

