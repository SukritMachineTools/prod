import tkinter as tk
from tkinter import ttk
import pandas as pd

def display_dataframe(dataframe):
    root = tk.Tk()
    root.title("DataFrame Display")

    # Create a Treeview widget
    treeview = ttk.Treeview(root)
    treeview["columns"] = list(dataframe.columns)
    treeview["show"] = "headings"

    # Add columns to the Treeview
    for column in dataframe.columns:
        treeview.heading(column, text=column)
        treeview.column(column, width=100)

    # Add rows to the Treeview
    for row in dataframe.itertuples(index=False):
        treeview.insert("", "end", values=row)

    # Add a vertical scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=treeview.yview)
    treeview.configure(yscroll=scrollbar.set)

    # Pack the Treeview and scrollbar
    treeview.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    root.mainloop()

# Example usage
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "London", "Paris"]
}

##########
# read google sheets
df = pd.read_csv(
    'https://docs.google.com/spreadsheets/d/e/2PACX-1vT6HrGh7EOzzejrvzkG_TGUM_GoGVDuvlUq7UcYqHlESZX6Vv8Hvwatsp4FLdE4Nmff9z5LSG3KQFq9/pub?gid=1362009325&single=true&output=csv')

# renamed columns
df.rename(columns={'Rejection': 'M/C', 'Unnamed: 6': 'CASTING',
                   'Unnamed: 7': 'OTHER', 'Timming': 'Start_Time', 'Unnamed: 11': 'End_Time',
                   'Total Prod': 'Total_Prod', 'Final Prod': 'Final_Prod', 'Total Rej': 'Total_Rej'}, inplace=True)
df = df.drop(index=0)
df = df.reset_index(drop=True)
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

# Convert the 'time_string' column to time object
df['Start_Time'] = pd.to_datetime(df['Start_Time'], format='%H:%M')
df['End_Time'] = pd.to_datetime(df['End_Time'], format='%H:%M')

# Calculate the time difference

df['time_difference1'] = df['End_Time'] - df['Start_Time']
df['time_difference1'] = df['time_difference1'] - pd.Timedelta(hours=1, minutes=30)
df['time_difference'] = df['time_difference1'].apply(
    lambda x: '{:02d}:{:02d}'.format(int(x.seconds // 3600), int((x.seconds // 60) % 60)))

df['Start_Time'] = pd.to_datetime(df['Start_Time'], format='%H:%M').dt.time
df['End_Time'] = pd.to_datetime(df['End_Time'], format='%H:%M').dt.time
df['time_difference'] = pd.to_datetime(df['time_difference'], format='%H:%M').dt.time

total_time = df['time_difference1'].sum()
# df=df.drop(['time_difference1'], axis=1)
total_hours = total_time.total_seconds() / 3600

job = 'S.R. Shaft THD'
breakTime = '01:30'
start_date = '2023-06-01'
end_date = '2023-07-07'

# mask = (df['date'] > start_date) & (df['date'] <= end_date)
mask = (df['Date'] > start_date) & (df['Date'] <= end_date)
datedf = df.loc[mask]
newdf = datedf[datedf['Job'] == job]
newdf = newdf.reset_index(drop=True)
newdf = newdf.astype(
    {'Total_Prod': 'int', 'M/C': 'int', 'CASTING': 'int', 'OTHER': 'int', 'Total_Rej': 'int', 'Final_Prod': 'int'})
sumrow = {'Total_Prod': sum(newdf['Total_Prod']), 'M/C': sum(newdf['M/C']), 'CASTING': sum(newdf['CASTING']),
          'OTHER': sum(newdf['OTHER']), 'Final_Prod': sum(newdf['Final_Prod']), 'time_difference': total_hours}
sumrow = pd.DataFrame(sumrow, index=['Total'])
newdf = pd.concat([newdf, sumrow], axis=0)
machinedf = newdf.copy()
machinedf = machinedf.drop(['time_difference1'], axis=1)
############

# df = pd.read_csv('production.csv')

display_dataframe(machinedf)
