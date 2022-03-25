from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import pymssql
import pandas as pd
import numpy as np
def MEWS(request):
    au = request.session.get('au')
    return render(request, 'MEWS/MEWS.html',{'au':au})

def connect():
    conn = pymssql.connect(
        server='172.31.6.157',
        user='TEST',
        password='81218',
        database='MEWS',
        #charset='UTF8'
    )
    cursor = conn.cursor()

    def SQL(sql, colname):
        cursor.execute(sql)
        row = cursor.fetchall()
        df = pd.DataFrame(row, columns = colname)
        return df

    sql = '''
            SELECT DISTINCT ChartNo, VisitNo, OccurDate, Ward, DivName
            FROM RRTFinish
            ORDER BY ChartNo, VisitNo, OccurDate
        '''

    # 欄位定義
    colname = ['ChartNo', 'VisitNo', 'OccurDate', 'Ward', 'DivName']
    chdf = SQL(sql, colname)
    chdf.set_index('OccurDate', inplace=True)

    sql = '''
            SELECT DISTINCT ChartNo, VisitNo, OccurDate,
                    BP_V1, Score1, PULSE_V1, Score2, RESPIRATORY_V1, Score3,
                    BT_V1, Score4, SPO2_V1, Score5,
                    GCS_V, Score6, Score, RRT
            FROM RRTFinish
            ORDER BY ChartNo, VisitNo, OccurDate
        '''


    # 欄位定義
    colname = ['ChartNo', 'VisitNo', 'OccurDate',
            'BP_V1', 'Score1', 'PULSE_V1', 'Score2', 'RESPIRATORY_V1', 'Score3',
            'BT_V1', 'Score4', 'SPO2_V1', 'Score5','GCS_V', 'Score6', 'Score', 'RRT']
    mews = SQL(sql, colname)
    mews.set_index('OccurDate', inplace=True)
    return chdf ,mews