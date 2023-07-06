from django.db.models import Sum, Avg, Count, Max
import plotly.express as px
import plotly.graph_objects as go

from ..models import InvoicesOut


class SalesBarMonthsByYears():
    """ takes data for model from pgsql sever 'cap_db'
    and uses aggregate functions for data"""

    def __int__(self):
        self.get_chart()

    def get_chart(self, request):
        # start = request.GET.get('start')
        # end = request.GET.get('end')
        inv_out = InvoicesOut.objects.using('cap_db').all().order_by('moment__year', 'moment__month')

        # if start:
        #     inv_out = inv_out.filter(moment__gte=start)
        # if end:
        #     inv_out = inv_out.filter(moment__lte=end)
        inv_out_year = inv_out.values('moment__year', 'moment__month').annotate(sum=Sum('sum') / 100)
        test_list_dict = [{"date": f"{elem['moment__year']}-{elem['moment__month']}-28", "sum": elem['sum']} for elem in
                          inv_out_year]

        fig = go.Figure()
        ten_colors = px.colors.qualitative.Plotly
        position = 0
        months_dict = {1: "Jan", 2: "Feb", 3: "March", 4: "Apr", 5: "May", 6: "June",
                       7: "July", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
        start_year = inv_out_year[0].get('moment__year')
        years_in_list = len(test_list_dict) // 12 + 1

        for year_count in range(years_in_list):
            x = []
            y = []
            for month in range(12):
                position = year_count * 12 + month
                x.append(months_dict.get(month + 1, None))
                try:
                    pos_dict = inv_out_year[position]
                    if pos_dict.get('moment__month', None) == month + 1:
                        y.append(round(pos_dict.get('sum', 0), 2))
                    else:
                        y.append(0)
                except IndexError as e:
                    print(f"Year {start_year + year_count} month {month + 1} is not passed, error: {e}")
                    y.append(0)
            fig.add_trace(go.Bar(
                x=x,
                y=y,
                name=f'Year {start_year + year_count}',
                marker_color=ten_colors[year_count % 10],
            ))
            if position >= len(test_list_dict):
                break
        fig.update_annotations(selector={"text": "Top"}, text="TOP_TEST")
        fig.update_layout(title={'font_size': 24, 'xanchor': 'center', 'x': 0.5}, xaxis_tickangle=-45, barmode='group')
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        res_chart = fig.to_html()
        return res_chart
