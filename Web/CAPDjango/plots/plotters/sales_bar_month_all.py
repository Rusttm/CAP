from django.db.models import Sum, Avg, Count, Max
import plotly.express as px
import plotly.graph_objects as go
import datetime
from ..models import InvoicesOut


class SalesBarMonthsAll():
    """ takes data for model from pgsql sever 'cap_db'
    and uses aggregate functions for data"""

    def __int__(self):
        self.get_chart()

    def get_chart(self, request):
        start = request.GET.get('start')
        end = request.GET.get('end')
        # start_time = datetime.datetime.strptime(start, '%Y-%m-%d')
        # filter_dict = {
        #     'moment__year': start_time.year,
        #     # 'moment__month': start_time.month,
        # }
        inv_out = InvoicesOut.objects.using('cap_db').all().order_by('moment__year', 'moment__month')
        # inv_out = InvoicesOut.objects.using('cap_db').all().order_by('moment').filter(**filter_dict)#.aggregate(avg=Sum('sum'))

        if start:
            inv_out = inv_out.filter(moment__gte=start)
        if end:
            inv_out = inv_out.filter(moment__lte=end)
        if not (start and end):
            start = datetime.datetime.strptime('2018-10-01', '%Y-%m-%d').strftime('%Y-%m-%d')
            end = datetime.datetime.now().strftime('%Y-%m-%d')

        inv_out_year = inv_out.values('moment__year', 'moment__month').annotate(sum=Sum('sum') / 100)
        test_list_dict = [{"date": f"{elem['moment__year']}-{elem['moment__month']}-28", "sum": elem['sum']} for elem in
                          inv_out_year]

        fig = px.bar(
            # x=inv_out_year.values_list('moment__month', flat=True),
            x=[elem['date'] for elem in test_list_dict],
            y=inv_out_year.values_list('sum', flat=True),

            title=f"SUM of Invoices by months from {start} to {end}",
            labels={'x': 'Date', 'y': 'SUM'},
            # text='date',
            text_auto='.2s'
        )

        fig.update_layout(title={'font_size': 24, 'xanchor': 'center', 'x': 0.5}, xaxis_tickangle=30, barmode='group')
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        res_chart = fig.to_html()
        return res_chart
