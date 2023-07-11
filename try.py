import tkinter as tk
from tkinter import ttk
import pandas as pd

# Create a sample DataFrame
data = {'Name': ['John', 'Alice', 'Bob', 'Jane'],
        'Age': [25, 30, 20, 35],
        'City': ['New York', 'Paris', 'London', 'Sydney']}

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

job = 'S.R. Shaft THD'
breakTime = '01:30'
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
distinct_values = newdf['Operator'].unique()  # Replace 'column_name' with the actual column name

distinct_values = list(distinct_values)
distinct_values.pop()
days = []
total_hours = []
sum_prod = []
sum_mc = []
sum_cast = []
sum_other = []
sum_finalprod = []
avg_hourly = []
avg_day = []
for i in range(len(distinct_values)):
    op1 = newdf[newdf['Operator'] == distinct_values[i]]
    daysop = op1.shape[0]
    days.append(daysop)
    total_timeop = op1['time_difference1'].sum()
    total_hoursop = round((total_timeop.total_seconds() / 3600), 2)
    total_hours.append(total_hoursop)
    sum_prodop = sum(op1['Total_Prod'])
    sum_prod.append(sum_prodop)
    sum_mcop = sum(op1['M/C'])
    sum_mc.append(sum_mcop)
    sum_castop = sum(op1['CASTING'])
    sum_cast.append(sum_castop)
    sum_otherop = sum(op1['OTHER'])
    sum_other.append(sum_otherop)
    sum_finalprodop = sum(op1['Final_Prod'])
    sum_finalprod.append(sum_finalprodop)
    avg_hourlyop = round((sum_prodop / total_hoursop), 2)
    avg_hourly.append(avg_hourlyop)
    avg_dayop = round((sum_prodop / daysop), 2)
    avg_day.append(avg_dayop)
product = {
    'Operator': distinct_values,
    'DAYS': days,
    'HOURS': total_hours,
    'Total_Prod': sum_prod,
    'M/C': sum_mc,
    'Casting': sum_cast,
    'Other': sum_other,
    'Final_Prod': sum_finalprod,
    'Hourly_Avg': avg_hourly,
    'Day_Avg': avg_day
}
print(product)
prod_df = pd.DataFrame(product)
prod_df['Deduct_Machine_rej'] = prod_df['Total_Prod'] - prod_df['M/C']
prod_df['Deduct_Machine_rej'] = prod_df['Deduct_Machine_rej'].round(2)
targetv = 55
incentivev = 0.70
prod_df['Hours X Target'] = prod_df['HOURS'] * targetv
prod_df['Hours X Target'] = prod_df['Hours X Target'].round(2)
prod_df['Extra Prod'] = prod_df['Deduct_Machine_rej'] - prod_df['Hours X Target']
prod_df['Extra Prod'] = prod_df['Extra Prod'].round(2)
prod_df['Incentive'] = prod_df['Extra Prod'] * incentivev
prod_df['Incentive'] = prod_df['Incentive'].round(2)

sumrow2 = {'Operator': 'Total', 'DAYS': sum(prod_df['DAYS']), 'HOURS': sum(prod_df['HOURS']),
           'Total_Prod': sum(prod_df['Total_Prod']), 'M/C': sum(prod_df['M/C']), 'Casting': sum(prod_df['Casting']),
           'Other': sum(prod_df['Other']), 'Final_Prod': sum(prod_df['Final_Prod']),
           'Hourly_Avg': round(sum(prod_df['Hourly_Avg']), 2), 'Day_Avg': round(sum(prod_df['Day_Avg']), 2),
           'Deduct_Machine_rej': round(sum(prod_df['Deduct_Machine_rej']), 2),
           'Hours X Target': round(sum(prod_df['Hours X Target']), 2),
           'Extra Prod': round(sum(prod_df['Extra Prod']), 2), 'Incentive': round(sum(prod_df['Incentive']), 2)}
sumrow2 = pd.DataFrame(sumrow2, index=['Total'])
operatordf = pd.concat([prod_df, sumrow2], axis=0)
# print(operatordf.columns)
# df = pd.DataFrame(data)
# df=operatordf.copy()

# Create the main window
window = tk.Tk()
window.title('Horizontal Scrollbar Example')

# Create a frame
frame = ttk.Frame(window)
frame.grid(row=0, column=0, sticky='nsew')

# Create a canvas
canvas = tk.Canvas(frame)
canvas.grid(row=0, column=0, sticky='nsew')

# Add a horizontal scrollbar
scrollbar = ttk.Scrollbar(frame, orient='horizontal', command=canvas.xview)
scrollbar.grid(row=1, column=0, sticky='ew')
canvas.configure(xscrollcommand=scrollbar.set)

# Create a frame inside the canvas
df_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=df_frame, anchor='nw')

# Create a Pandas DataFrame table within the frame
table = ttk.Treeview(df_frame, columns=list(operatordf.columns), show='headings')
table.grid(row=0, column=0, sticky='nsew')

# Insert column headers
for column in operatordf.columns:
    table.heading(column, text=column)

# Insert data rows
for _, row in operatordf.iterrows():
    table.insert('', 'end', values=list(row))

# Decrease the width of all columns
for column in operatordf.columns:
    table.column(column, width=80)  # Specify the desired width
# Configure the grid weights
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
df_frame.grid_rowconfigure(0, weight=1)
df_frame.grid_columnconfigure(0, weight=1)

# Update the canvas scrolling region
canvas.update_idletasks()
canvas.configure(scrollregion=canvas.bbox('all'))

# Start the main loop
window.mainloop()
