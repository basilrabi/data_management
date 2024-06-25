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
    ad_req = 0
    ad_req = 0
    ct_req = 0
    dt_req = 0
    ft_req = 0
    rg_req = 0
    st_req = 0
    sv_req = 0
    tl_req = 0
    tx_req = 0
    vr_req = 0
    wl_req = 0
    wt_req = 0
    total_req = 0
    ad_bal = 0
    ct_bal = 0
    dt_bal = 0
    ft_bal = 0
    rg_bal = 0
    st_bal = 0
    sv_bal = 0
    tl_bal = 0
    tx_bal = 0
    vr_bal = 0
    wl_bal = 0
    wt_bal = 0
    total_bal = 0
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
        ad_req += fleet['AD_req']
        ct_req += fleet['CT_req']
        dt_req += fleet['DT_req']
        ft_req += fleet['FT_req']
        rg_req += fleet['RG_req']
        st_req += fleet['ST_req']
        sv_req += fleet['SV_req']
        tl_req += fleet['TL_req']
        tx_req += fleet['TX_req']
        vr_req += fleet['VR_req']
        wl_req += fleet['WL_req']
        wt_req += fleet['WT_req']
        total_req += fleet['Total_req']
        ad_bal += fleet['AD_bal']
        ct_bal += fleet['CT_bal']
        dt_bal += fleet['DT_bal']
        ft_bal += fleet['FT_bal']
        rg_bal += fleet['RG_bal']
        st_bal += fleet['ST_bal']
        sv_bal += fleet['SV_bal']
        tl_bal += fleet['TL_bal']
        tx_bal += fleet['TX_bal']
        vr_bal += fleet['VR_bal']
        wl_bal += fleet['WL_bal']
        wt_bal += fleet['WT_bal']
        total_bal += fleet['Total_bal']
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
        'Total': total,
        'AD_req': ad_req,
        'CT_req': ct_req,
        'DT_req': dt_req,
        'FT_req': ft_req,
        'RG_req': rg_req,
        'ST_req': st_req,
        'SV_req': sv_req,
        'TL_req': tl_req,
        'TX_req': tx_req,
        'VR_req': vr_req,
        'WL_req': wl_req,
        'WT_req': wt_req,
        'Total_req': total_req,
        'AD_bal': ad_bal,
        'CT_bal': ct_bal,
        'DT_bal': dt_bal,
        'FT_bal': ft_bal,
        'RG_bal': rg_bal,
        'ST_bal': st_bal,
        'SV_bal': sv_bal,
        'TL_bal': tl_bal,
        'TX_bal': tx_bal,
        'VR_bal': vr_bal,
        'WL_bal': wl_bal,
        'WT_bal': wt_bal,
        'Total_bal': total_bal,
    })
    return render(request, 'organization/index.html', {'contractors': data_set})

