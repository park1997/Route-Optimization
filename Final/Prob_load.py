import pandas as pd
import TSP_settings as tsp
import random

attributes_task = ['ID', 'Pos1', 'Pos2']
attributes_day = ['ID', 'Pos1', 'Pos2']


def generate_prob_xslx(path, num_task=12, num_day=3, depot_loc=list):
    df_task = pd.DataFrame(columns=attributes_task)
    df_day = pd.DataFrame(columns=attributes_day)

    for vhc in range(num_day):
        row_attributes_vhc = {i: 0 for i in attributes_day}
        row_attributes_vhc['ID'] = vhc + 1
        row_attributes_vhc['Pos1'] = depot_loc[0]
        row_attributes_vhc['Pos2'] = depot_loc[1]
        df_day = df_day.append(row_attributes_vhc, ignore_index=True)

    for task in range(num_task):
        row_attributes_task = {i: 0 for i in attributes_task}
        row_attributes_task['ID'] = task + 1
        row_attributes_task['Pos1'] = random.randint(0, 1000)
        row_attributes_task['Pos2'] = random.randint(0, 1000)
        df_task = df_task.append(row_attributes_task, ignore_index=True)

    # Write DataFrame to Excel File
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df_task.to_excel(writer, sheet_name='Tasks')
    df_day.to_excel(writer, sheet_name='Days')
    writer.save()


def load_prob_xlsx(xlsx):
    # Load Excel file as a class
    df_task = pd.read_excel(xlsx, sheet_name='Tasks')
    df_day = pd.read_excel(xlsx, sheet_name='Days')

    day_list, tasklist = [], []
    for _day in df_day['ID']:
        _day = tsp.Day()
        day_list.append(_day)

    for _task in df_task['ID']:
        _task = tsp.Task()
        tasklist.append(_task)

    for i in range(len(day_list)):
        day_list[i].id = df_day['ID'][i]
        day_list[i].loc = [df_day['Pos1'][i], df_day['Pos2'][i]]
        day_list[i].origin = [df_day['Pos1'][i], df_day['Pos2'][i]]
        day_list[i].end = [df_day['Pos1'][i], df_day['Pos2'][i]]

    for i in range(len(tasklist)):
        tasklist[i].id = df_task['ID'][i]
        tasklist[i].loc = [df_task['Pos1'][i], df_task['Pos2'][i]]

    origin = tsp.Task()
    end = tsp.Task()
    origin.loc = [500,500]
    end.loc = [500,500]

    tasklist.insert(0,origin)
    tasklist.append(end)

    dist = []
    for i in range(len(tasklist)):
        i_to_j = []
        for j in range(len(tasklist)):
            i_to_j.append(tsp.distance(tasklist[i], tasklist[j]))
        dist.append(i_to_j)

    for i in range(len(dist)):
        for j in range(len(dist)):
            dist[i][j] = dist[j][i]
        dist[i][-1] = dist[i][0]
    del tasklist[0]
    del tasklist[-1]

    return day_list, tasklist, dist


