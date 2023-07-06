from django.shortcuts import render
from django.db.models import Sum, Avg, Count, Max
import plotly.express as px
import datetime
from .forms import DateForm
from .models import CO2, InvoicesOut
import plotly.graph_objects as go


# Create your views here.
def chart(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    co2 = CO2.objects.all()
    if start:
        co2 = co2.filter(date__gte=start)
    if end:
        co2 = co2.filter(date__lte=end)

    fig = px.line(
        x=[c.date for c in co2],
        y=[c.average for c in co2],
        # x=[i for i in range(5)],
        # y=[i for i in range(5)],
        title="CO2 PPM",
        labels={'x': 'Date', 'y': 'CO2 PPM'}
    )

    fig.update_layout(
        title={
            'font_size': 24,
            'xanchor': 'center',
            'x': 0.5
        })
    chart = fig.to_html()
    context = {'chart': chart, 'form': DateForm()}
    return render(request, 'plots/chart.html', context)


def chart2(request):
    """ takes data for model from pgsql sever 'cap_db' """
    start = request.GET.get('start')
    end = request.GET.get('end')

    inv_out = InvoicesOut.objects.using('cap_db').all().order_by('moment')
    if start:
        inv_out = inv_out.filter(moment__gte=start)
    if end:
        inv_out = inv_out.filter(moment__lte=end)

    fig = px.line(
        x=[c.moment for c in inv_out],
        y=[c.sum / 100 for c in inv_out],
        title="SUM of Invoices",
        labels={'x': 'Date', 'y': 'SUM'}
    )

    fig.update_layout(
        title={
            'font_size': 24,
            'xanchor': 'center',
            'x': 0.5
        })
    res_chart = fig.to_html()
    context = {'chart': res_chart, 'form': DateForm()}
    return render(request, 'plots/chart.html', context)


def chart3(request):
    """ takes data for model from pgsql sever 'cap_db'
    and uses aggregate functions for data"""
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
    inv_out_year = inv_out.values('moment__year', 'moment__month').annotate(sum=Sum('sum') / 100)
    test_list_dict = [{"date": f"{elem['moment__year']}-{elem['moment__month']}-28", "sum": elem['sum']} for elem in
                      inv_out_year]

    fig = px.bar(
        # x=inv_out_year.values_list('moment__month', flat=True),
        x=[elem['date'] for elem in test_list_dict],
        y=inv_out_year.values_list('sum', flat=True),

        title=f"SUM of Invoices by months",
        labels={'x': 'Date', 'y': 'SUM'},
        # text='date',
        text_auto='.2s'
    )

    fig.update_layout(title={'font_size': 24, 'xanchor': 'center', 'x': 0.5}, xaxis_tickangle=-45, barmode='group')
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    res_chart = fig.to_html()
    context = {'chart': res_chart, 'form': DateForm()}
    return render(request, 'plots/chart.html', context)


def chart4(request):
    """ takes data for model from pgsql sever 'cap_db'
    and uses aggregate functions for data"""
    start = request.GET.get('start')
    end = request.GET.get('end')
    # start_time = datetime.datetime.strptime(start, '%Y-%m-%d')
    # filter_dict = {
    #     'moment__year': start_time.year_count,
    #     # 'moment__month': start_time.month,
    # }
    inv_out = InvoicesOut.objects.using('cap_db').all().order_by('moment__year', 'moment__month')
    # inv_out = InvoicesOut.objects.using('cap_db').all().order_by('moment').filter(**filter_dict)#.aggregate(avg=Sum('sum'))

    if start:
        inv_out = inv_out.filter(moment__gte=start)
    if end:
        inv_out = inv_out.filter(moment__lte=end)
    inv_out_year = inv_out.values('moment__year', 'moment__month').annotate(sum=Sum('sum') / 100)
    test_list_dict = [{"date": f"{elem['moment__year']}-{elem['moment__month']}-28", "sum": elem['sum']} for elem in
                      inv_out_year]

    fig = go.Figure()
    ten_colors = px.colors.qualitative.Plotly
    position = 0
    months_dict = {1: "Jan", 2: "Feb", 3: "March", 4: "Apr", 5: "May", 6: "June",
                   7: "July", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
    start_year = inv_out_year[0].get('moment__year')
    years_in_list = len(test_list_dict)//12 + 1

    for year_count in range(years_in_list):
        x = []
        y = []
        for month in range(12):
            position = year_count * 12 + month
            x.append(months_dict.get(month+1, None))
            try:
                pos_dict = inv_out_year[position]
                if pos_dict.get('moment__month', None) == month+1:
                    y.append(round(pos_dict.get('sum', 0), 2))
                else:
                    y.append(0)
            except IndexError as e:
                print(f"Year {start_year+year_count} month {month+1} is not passed, error: {e}")
                y.append(0)
        fig.add_trace(go.Bar(
            x=x,
            y=y,
            name=f'Year {start_year+year_count}',
            marker_color=ten_colors[year_count % 10],
        ))
        if position >= len(test_list_dict):
            break


    fig.update_layout(title={'font_size': 24, 'xanchor': 'center', 'x': 0.5}, xaxis_tickangle=-45, barmode='group')
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    res_chart = fig.to_html()
    context = {'chart': res_chart, 'form': DateForm()}
    return render(request, 'plots/chart.html', context)
