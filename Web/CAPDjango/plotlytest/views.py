from django.shortcuts import render
import plotly.express as px

from .forms import DateForm
from .models import CO2, InvoicesOut

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
    return render(request, 'plotlytest/chart.html', context)


def chart2(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    inv_out = InvoicesOut.objects.using('cap_db').all().order_by('moment')
    if start:
        inv_out = inv_out.filter(moment__gte=start)
    if end:
        inv_out = inv_out.filter(moment__lte=end)

    fig = px.line(
        x=[c.moment for c in inv_out],
        y=[c.sum for c in inv_out],
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
    return render(request, 'plotlytest/chart.html', context)

