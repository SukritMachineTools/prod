import tkinter as tk
from tkinter import ttk
import pandas as pd

def display_dataframe(dataframes):
    root = tk.Tk()
    root.title("DataFrame Display")

    # Create a Frame to hold the Treeview and scrollbar
    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)

    for i,dataframe in enumerate(dataframes):
        # Create a new frame for each dataframe
        frame = tk.Frame(root)
        frame.pack()
        # Create a Treeview widget
        treeview = ttk.Treeview(frame)
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
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=treeview.yview)
        treeview.configure(yscroll=scrollbar.set)

        # Grid layout configuration within the Frame
        treeview.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure grid weights within the Frame to resize properly
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    root.mainloop()

# Example usage
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "London", "Paris"]
}

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

job='S.R. Shaft THD'
breakTime='01:30'
start_date = '2023-06-01'
end_date = '2023-07-07'

# mask = (df['date'] > start_date) & (df['date'] <= end_date)
mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
datedf = df.loc[mask]
newdf = datedf[datedf['Job'] == job]
newdf = newdf.reset_index(drop=True)
total_time = newdf['time_difference1'].sum()
# df=df.drop(['time_difference1'], axis=1)
total_hours = total_time.total_seconds() / 3600
newdf = newdf.astype(
    {'Total_Prod': 'int', 'M/C': 'int', 'CASTING': 'int', 'OTHER': 'int', 'Total_Rej': 'int', 'Final_Prod': 'int'})
newdf['Date'] = newdf['Date'].dt.strftime('%d-%m-%Y')
sumrow = {'Date': 'Total', 'Total_Prod': sum(newdf['Total_Prod']), 'M/C': sum(newdf['M/C']),
          'CASTING': sum(newdf['CASTING']), 'OTHER': sum(newdf['OTHER']), 'Final_Prod': sum(newdf['Final_Prod']),
          'time_difference': total_hours}
sumrow = pd.DataFrame(sumrow, index=['Total'])
newdf = pd.concat([newdf, sumrow], axis=0)

# Get the distinct values in a specific column
distinct_values_Job = df['Job'].unique()
distinct_values_Job = list(distinct_values_Job)
distinct_values_Job.pop()

# multi table
machinej = []
t_prodj = []
mcj = []
castj = []
otherj = []
final = []
column_names = ['Machines', 'PRODUCT', 'Total_Prod', 'M/C', 'CASTING', 'OTHER', 'FINAL']
dflist = []
# Create an empty dataframe with the specified column names
jobs = pd.DataFrame(columns=column_names)

for j in range(len(distinct_values_Job)):
    job1 = df[df['Job'] == distinct_values_Job[j]]
    job1 = job1.loc[mask]
    job1 = job1.reset_index(drop=True)
    job1 = job1.astype(
        {'Total_Prod': 'int', 'M/C': 'int', 'CASTING': 'int', 'OTHER': 'int', 'Total_Rej': 'int', 'Final_Prod': 'int'})
    distinct_values_Mc = job1['Machines'].unique()
    distinct_values_Mc = list(distinct_values_Mc)

    jobs = pd.DataFrame(columns=column_names)

    for m in range(len(distinct_values_Mc)):
        job2 = job1[job1['Machines'] == distinct_values_Mc[m]]
        job2 = job2.astype({'Total_Prod': 'int', 'M/C': 'int', 'CASTING': 'int', 'OTHER': 'int', 'Total_Rej': 'int',
                            'Final_Prod': 'int'})
        job3 = {'Machines': distinct_values_Mc[m], 'PRODUCT': distinct_values_Job[j],
                'Total_Prod': sum(job2['Total_Prod']), 'M/C': sum(job2['M/C']), 'CASTING': sum(job2['CASTING']),
                'OTHER': sum(job2['OTHER']), 'FINAL': sum(job2['Final_Prod'])}
        job3 = pd.DataFrame(job3, index=[m])
        jobs = pd.concat([jobs, job3], ignore_index=True)
    job3 = {'Machines': 'Total', 'Total_Prod': sum(jobs['Total_Prod']), 'M/C': sum(jobs['M/C']),
            'CASTING': sum(jobs['CASTING']), 'OTHER': sum(jobs['OTHER']), 'FINAL': sum(jobs['FINAL'])}
    job3 = pd.DataFrame(job3, index=[0])
    jobs = pd.concat([jobs, job3], ignore_index=True)
    dflist.append(jobs)

# df = pd.DataFrame(dflist)

display_dataframe(dflist)
