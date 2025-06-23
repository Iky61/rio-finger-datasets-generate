import pandas as pd
import requests

class support_functions:
    # split time string to list
    @staticmethod
    def split_time_string(time_string=list):
        return [time_string[i:i+5] for i in range(0, len(time_string), 5)]
    
    # time category based on date and condition
    @staticmethod
    def time_category(data=str, date=str):
        data = pd.to_datetime(f"{date} {data}")
        day = data.day_name()

        if day != 'Friday':
            if pd.to_datetime(data) < pd.to_datetime(f'{date} 12:00'):
                msg = 'Cek In'
            elif pd.to_datetime(data) >= pd.to_datetime(f'{date} 12:00') and pd.to_datetime(data) < pd.to_datetime(f'{date} 16:30'):
                msg = 'Cek Rest'
            else:
                msg = 'Cek Out'
        else:
            if pd.to_datetime(data) < pd.to_datetime(f'{date} 11:00'):
                msg = 'Cek In'
            elif pd.to_datetime(data) >= pd.to_datetime(f'{date} 11:00') and pd.to_datetime(data) < pd.to_datetime(f'{date} 16:30'):
                msg = 'Cek Rest'
            else:
                msg = 'Cek Out'
        return msg
    
    # split time category
    @staticmethod
    def split_time_category(data=list, date=str, condition=str):
        _ = []
        for i in data:
            n_time = i
            category_time = support_functions.time_category(i, date)
            _.append(pd.DataFrame({'time':[n_time], 'category':[category_time]}))
        msg = pd.concat(_).reset_index(drop=True)
        
        try:
            if condition == 'Cek In':
                msg = msg[msg.category == condition]['time'].min()
            elif condition == 'Cek Rest Out':
                msg = msg[msg.category == 'Cek Rest']['time'].min()
            elif condition == 'Cek Rest In':
                msg = msg[msg.category == 'Cek Rest']['time'].max()
            else:
                msg = msg[msg.category == 'Cek Out']['time'].max()
        except:
            msg = 'Unknown'
        return msg

class get_data:
    # get data google sheet and save to Database
    @staticmethod
    def get_data_gsheet(url=str, path=str, filename=str, sheetname=str):
        path = f'./{path}/{filename}.xlsx'
        
        try:
            os.remove(path)
        except:
            None
            
        output_filename = path
        
        # get the data from spreadsheet
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_filename, "wb") as f:
                f.write(response.content)

        # read data
        data = pd.read_excel(path, sheet_name=sheetname)
        return data
    
    # get and transform data presensi format excel
    def get_data_excel(self=None, date=str, branch=str, data=None):
        # data = pd.read_excel('./Datasets/datasets_presensi.xls', sheet_name='Lap. Log Absen')
        
        data = data[data.index >= 3].reset_index(drop=True)[['Lap. Detail Absensi','Unnamed: 1','Unnamed: 2']]
        data.columns = ['log_absen','unknown','id']
        data = data[['id','log_absen']]
        data['id'] = data['id'].ffill()
        data = data[data.log_absen != 'ID:']
        data['log_absen'].fillna('-', inplace=True)
        data = data[data.log_absen != '-'].reset_index(drop=True)
        data['log_absen'] = data.log_absen.apply(lambda x: support_functions.split_time_string(str(x)))

        data['cek_in'] = data.log_absen.apply(lambda x: support_functions.split_time_category(x, date=date, condition='Cek In'))
        data['cek_rest_out'] = data.log_absen.apply(lambda x: support_functions.split_time_category(x, date=date, condition='Cek Rest Out'))
        data['cek_rest_in'] = data.log_absen.apply(lambda x: support_functions.split_time_category(x, date=date, condition='Cek Rest In'))
        data['cek_out'] = data.log_absen.apply(lambda x: support_functions.split_time_category(x, date=date, condition='Cek Out'))
        data.drop(columns=['log_absen'], inplace=True)
        data['branch'] = branch
        data['id_2'] = data['id'] + '#' + data['branch']
        return data
    
class load_data:
    @staticmethod
    def load_data_excel_to_export(data=None, filename=str):
        if data is not None:
            # Save the DataFrame to an Excel file
            output_filename = f'./Exports/{filename}.xlsx'
            data.to_excel(output_filename, index=False)
            msg = 'Data has been successfully saved to ' + output_filename
        else:
            msg = ("Data is None. Please provide a valid DataFrame")
        return msg