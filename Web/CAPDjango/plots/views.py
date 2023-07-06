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


def charts_group(request):
    charts_context = []
    from .plotters.sales_bar_month_all import SalesBarMonthsAll
    res_chart = SalesBarMonthsAll().get_chart(request=request)
    charts_context.append(res_chart)

    from .plotters.sales_bar_years import SalesBarYearsAll
    res_chart = SalesBarYearsAll().get_chart(request=request)
    charts_context.append(res_chart)

    from .plotters.sales_bar_months_by_years import SalesBarMonthsByYears
    res_chart = SalesBarMonthsByYears().get_chart(request=request)
    charts_context.append(res_chart)

    start = request.GET.get('start')
    end = request.GET.get('end')
    if not(start and end):
        start = datetime.datetime.strptime('2018-10-01', '%Y-%m-%d').strftime('%Y-%m-%d')
        end = datetime.datetime.now().strftime('%Y-%m-%d')
    initial_form_values = {'start': start, 'end': end}


    context = {'charts': charts_context, 'form': DateForm(initial=initial_form_values)}
    return render(request, 'plots/charts.html', context)
