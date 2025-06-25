import pandas as pd
import requests
from functions import get_data

class generator:
    # generate data excel
    @staticmethod
    def data_process_1(date=str, branch=str, data=None):
        data = get_data.get_data_excel(date=date, branch=branch, data=data)

        # database karyawan
        db_emp = get_data.get_data_gsheet(
            url="https://docs.google.com/spreadsheets/d/18zheER6i6d72o9tJqFe93ljsETmiFUYYYr_N8-OKgNw/export?format.xlsx",
            path='Database',
            filename='database_karyawan',
            sheetname='Database Karyawan'
        )

        # cleaning data 
        db_emp.columns = [''.join('_'.join(i.lower().split()).split('.')) for i in db_emp.columns.tolist()]
        db_emp = db_emp.dropna(subset=['no_urut'])

        # feature engineering
        db_emp['id_2'].replace('37#RIO Office Equipment','37#RIO Utama', inplace=True)

        #  filter branch
        if branch == 'RIO Digital Printing':
            branch_target = ['RIO Digital Printing']
        else:
            branch_target = ['RIO Office Equipment', 'RIO Utama']

        # filter database karyawan
        db_emp = db_emp[db_emp.branch.isin(branch_target)]
        
        # merge data 
        data = db_emp[db_emp.status_bekerja == 'Aktif'][['id_2','nama_karyawan_(sesuai_ktp)']].merge(data, on='id_2', how='left')
        data['id'] = data['id_2'].apply(lambda x: str(x).split('#')[0])

        data = data.drop(columns=['id_2','branch'])
        data.columns = ['emp_name','id','cek_in','cek_rest_out','cek_rest_in','cek_out']
        data = data[['id','emp_name','cek_in','cek_rest_out','cek_rest_in','cek_out']]
        data = data.dropna(subset=['emp_name'])

        # return processed data
        return data