from django.db.models import Sum, Avg, Count, Max
import plotly.express as px
import plotly.graph_objects as go

from ..models import InvoicesOut


class SalesBarYearsAll():
    """ takes data for model from pgsql sever 'cap_db'
    and uses aggregate functions for data"""

    def __int__(self):
        self.get_chart()

    def get_chart(self, request):
        # start = request.GET.get('start')
        # end = request.GET.get('end')
        inv_out = InvoicesOut.objects.using('cap_db').all()#.order_by('moment__year', 'moment__month')

        # if start:
        #     inv_out = inv_out.filter(moment__gte=start)
        # if end:
        #     inv_out = inv_out.filter(moment__lte=end)
        inv_out_year = inv_out.values('moment__year').annotate(sum=Sum('sum') / 100)

        fig = px.bar(
            x=inv_out_year.values_list('moment__year', flat=True),
            y=inv_out_year.values_list('sum', flat=True),

            title=f"SUM of Invoices by year",
            labels={'x': 'Date', 'y': 'SUM'},
            text_auto='.2s'
        )

        fig.update_layout(title={'font_size': 24, 'xanchor': 'center', 'x': 0.5}, xaxis_tickangle=-45, barmode='group')
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        res_chart = fig.to_html()
        return res_chart
