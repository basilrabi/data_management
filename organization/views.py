from django.shortcuts import render

from .models import ServiceProvider
def index(request):
    ad = 0
    ct = 0
    dt = 0
    ft = 0
    rg = 0
    st = 0
    sv = 0
    tl = 0
    tx = 0
    vr = 0
    wl = 0
    wt = 0
    total = 0
    data_set = []
    for contractor in ServiceProvider.objects.filter(active=True, service='Contractor'):
        fleet = contractor.equipment_registry_count()
        ad += fleet['AD']
        ct += fleet['CT']
        dt += fleet['DT']
        ft += fleet['FT']
        rg += fleet['RG']
        st += fleet['ST']
        sv += fleet['SV']
        tl += fleet['TL']
        tx += fleet['TX']
        vr += fleet['VR']
        wl += fleet['WL']
        wt += fleet['WT']
        total += fleet['Total']
        data_set.append(fleet)
    data_set.append({
        'contractor': 'TOTAL',
        'AD': ad,
        'CT': ct,
        'DT': dt,
        'FT': ft,
        'RG': rg,
        'ST': st,
        'SV': sv,
        'TL': tl,
        'TX': tx,
        'VR': vr,
        'WL': wl,
        'WT': wt,
        'Total': total
    })
    return render(request, 'organization/index.html', {'contractors': data_set})

