# composite_app.py  — GCI-2011 Poutre Composite Interactive
# Université Laval · Luca Sorelli · CSA S16:24 / A23.3
# Requires: streamlit, plotly, numpy  →  pip install streamlit plotly numpy

import math, sys, os
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GCI-2011 · Poutre Composite",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  EMBEDDED ENGINEERING LIBRARY  (no external import needed for GitHub deploy)
# ══════════════════════════════════════════════════════════════════════════════

PHI    = 0.90
PHI_C  = 0.65
PHI_SC = 0.80
F_SC   = 415.0   # MPa  W59 Type B
E_S    = 200_000  # MPa

T1 = {
    "W310x39": dict(dl=0.380,As=4940, d=310,bf=165,tf=9.7, tw=5.8, Ix=85.1, Zx=634),
    "W360x45": dict(dl=0.442,As=5730, d=352,bf=171,tf=9.8, tw=6.9, Ix=122,  Zx=779),
    "W360x51": dict(dl=0.496,As=6450, d=355,bf=171,tf=11.6,tw=7.2, Ix=141,  Zx=894),
    "W360x57": dict(dl=0.556,As=7220, d=358,bf=172,tf=13.1,tw=7.9, Ix=161,  Zx=1010),
    "W360x64": dict(dl=0.627,As=8140, d=347,bf=203,tf=13.5,tw=7.7, Ix=178,  Zx=1140),
    "W360x91": dict(dl=0.891,As=11600,d=353,bf=254,tf=16.4,tw=9.5, Ix=267,  Zx=1660),
    "W360x101":dict(dl=0.993,As=12900,d=357,bf=255,tf=18.3,tw=10.5,Ix=301,  Zx=1880),
    "W360x110":dict(dl=1.08, As=14000,d=360,bf=256,tf=19.9,tw=11.4,Ix=331,  Zx=2080),
    "W360x122":dict(dl=1.19, As=15500,d=363,bf=257,tf=21.7,tw=13.0,Ix=365,  Zx=2270),
    "W410x39": dict(dl=0.385,As=4990, d=399,bf=140,tf=8.8, tw=6.4, Ix=127,  Zx=730),
    "W410x46": dict(dl=0.454,As=5890, d=403,bf=140,tf=11.2,tw=7.0, Ix=156,  Zx=885),
    "W410x54": dict(dl=0.524,As=6810, d=403,bf=177,tf=10.9,tw=7.5, Ix=186,  Zx=1050),
    "W410x60": dict(dl=0.584,As=7560, d=407,bf=178,tf=12.8,tw=7.7, Ix=216,  Zx=1190),
    "W410x67": dict(dl=0.662,As=8600, d=410,bf=179,tf=14.4,tw=8.8, Ix=246,  Zx=1360),
    "W410x74": dict(dl=0.735,As=9550, d=413,bf=180,tf=16.0,tw=9.7, Ix=275,  Zx=1510),
    "W410x85": dict(dl=0.834,As=10800,d=417,bf=181,tf=18.2,tw=10.9,Ix=315,  Zx=1730),
    "W410x100":dict(dl=0.992,As=12900,d=415,bf=260,tf=16.9,tw=10.0,Ix=404,  Zx=2160),
    "W410x114":dict(dl=1.14, As=14800,d=420,bf=261,tf=19.3,tw=11.6,Ix=468,  Zx=2490),
    "W410x132":dict(dl=1.31, As=17000,d=425,bf=263,tf=22.2,tw=13.3,Ix=545,  Zx=2890),
    "W410x149":dict(dl=1.48, As=19200,d=431,bf=265,tf=25.0,tw=14.9,Ix=625,  Zx=3280),
    "W460x61": dict(dl=0.588,As=7640, d=450,bf=189,tf=10.8,tw=8.1, Ix=254,  Zx=1290),
    "W460x74": dict(dl=0.728,As=9450, d=457,bf=190,tf=14.5,tw=9.0, Ix=333,  Zx=1650),
    "W460x82": dict(dl=0.804,As=10400,d=460,bf=191,tf=16.0,tw=9.9, Ix=370,  Zx=1830),
    "W460x89": dict(dl=0.876,As=11400,d=463,bf=192,tf=17.7,tw=10.5,Ix=410,  Zx=2010),
    "W460x97": dict(dl=0.947,As=12300,d=466,bf=193,tf=19.0,tw=11.4,Ix=445,  Zx=2180),
    "W460x106":dict(dl=1.04, As=13500,d=469,bf=194,tf=20.6,tw=12.6,Ix=488,  Zx=2390),
    "W530x72": dict(dl=0.702,As=9120, d=524,bf=207,tf=10.9,tw=8.9, Ix=400,  Zx=1750),
    "W530x82": dict(dl=0.806,As=10500,d=528,bf=209,tf=13.3,tw=9.5, Ix=477,  Zx=2060),
    "W530x92": dict(dl=0.907,As=11800,d=533,bf=209,tf=15.6,tw=10.2,Ix=552,  Zx=2360),
    "W530x101":dict(dl=0.995,As=12900,d=537,bf=210,tf=17.4,tw=10.9,Ix=617,  Zx=2620),
    "W530x109":dict(dl=1.07, As=13900,d=539,bf=211,tf=18.8,tw=11.6,Ix=667,  Zx=2830),
    "W530x123":dict(dl=1.21, As=15700,d=544,bf=212,tf=21.2,tw=13.1,Ix=761,  Zx=3210),
    "W530x138":dict(dl=1.36, As=17600,d=549,bf=214,tf=23.6,tw=14.7,Ix=861,  Zx=3610),
}

def alpha1(fc): return max(0.85 - 0.0015*fc, 0.67)
def Ec(fc):     return 4500*math.sqrt(fc)
def Ec_full(fc, rho): return (3300*math.sqrt(fc)+6900)*(rho/2300)**1.5
def n_ratio(fc, rho=None, formula='simplified'):
    ec = Ec_full(fc, rho) if formula=='full' and rho else Ec(fc)
    return E_S/ec, ec

def compute_qrs(dg, fc, rho=None, formula='simplified'):
    Asc = math.pi*dg**2/4
    _, ec = n_ratio(fc, rho, formula)
    q = 0.5*PHI_SC*Asc*math.sqrt(fc*ec)
    return min(q, PHI_SC*Asc*F_SC)

def compute_Ap(h_stud, wd):
    return 2*math.sqrt(2)*h_stud**2 + (math.sqrt(2)/2)*h_stud*wd

def compute_qrr_perp(dg, fc, hd, h_stud, wd, rho=None, formula='simplified'):
    qrs = compute_qrs(dg, fc, rho, formula)
    Ap  = compute_Ap(h_stud, wd)
    rhoC = 1.0
    coef = 0.35 if abs(hd-75)<5 else (0.61 if abs(hd-38)<5 else
           0.35+(0.61-0.35)*(hd-38)/(75-38))
    return min(coef*PHI_SC*rhoC*Ap*math.sqrt(fc), qrs)

def compute_qrr_parallel(dg, fc, hd, wd, rho=None, formula='simplified'):
    qrs = compute_qrs(dg, fc, rho, formula)
    if wd/hd >= 1.5:
        return min(qrs*(0.75+0.167*(wd/hd-1.5)), qrs)
    return 0.75*qrs

def elu_calc(sec, fc, Fy, be, tc, hd, p, qr_N):
    a1  = alpha1(fc)
    As  = sec['As']; d=sec['d']; bf=sec['bf']; tf=sec['tf']; tw=sec['tw']
    Tr  = PHI*As*Fy
    Cr  = a1*PHI_C*be*tc*fc
    Qr  = p*min(Tr, Cr)
    Crs = (Tr - Qr)/2
    Crfmax = PHI*bf*tf*Fy
    ae  = Qr/(a1*PHI_C*be*fc)

    steps = []  # list of (formula_name, latex, value, unit)

    steps.append(("α₁", r"\alpha_1 = 0.85 - 0.0015 f'_c", a1, ""))
    steps.append(("T_r,max = φ·As·Fy", r"\phi A_s F_y", Tr/1e3, "kN"))
    steps.append(("C'_r,max = α₁·φc·be·tc·f'c", r"\alpha_1 \phi_c b_e t_c f'_c", Cr/1e3, "kN"))
    steps.append(("Q_r = p·min(T_r,C'_r)", r"p \cdot \min(T_r, C'_r)", Qr/1e3, "kN"))
    steps.append(("C_rs = (Tr-Qr)/2", r"\frac{T_r - Q_r}{2}", Crs/1e3, "kN"))
    steps.append(("C_rf,max = φ·bf·tf·Fy", r"\phi b_f t_f F_y", Crfmax/1e3, "kN"))
    steps.append(("ae = Qr/(α₁·φc·be·f'c)", r"\frac{Q_r}{\alpha_1 \phi_c b_e f'_c}", ae, "mm"))

    if p == 1.0 and Cr > Tr:
        case = 'a'
        e_prime = d/2 + hd + tc - ae/2
        Mrc = Tr*e_prime
        Vh  = Tr
        dt  = d/2; dc = 0.0
        steps.append(("→ Cas A: ANP dans la dalle", r"y_{ANP} = d + h_d + t_c - a_e", d+hd+tc-ae, "mm"))
        steps.append(("e' = d/2 + hd + tc - ae/2", r"\frac{d}{2} + h_d + t_c - \frac{a_e}{2}", e_prime, "mm"))
        steps.append(("M_rc = Tr·e'", r"T_r \cdot e'", Mrc/1e6, "kN·m"))
        return dict(case='a', Mrc=Mrc/1e6, Vh=Vh/1e3, ae=ae,
                    Cr_prime=Qr/1e3, Cr_steel=0, Tr_max=Tr/1e3,
                    Cr_max=Cr/1e3, a1=a1, e=0, e_prime=e_prime,
                    dt=dt, dc=dc, steps=steps)

    if Crs <= Crfmax:
        case = 'b'
        tfc = Crs/Crfmax*tf
        dt  = (0.5*As*d - 0.5*bf*tfc**2)/(As - bf*tfc)
        es  = dt - tfc/2
        ec_lev = dt + hd + tc - ae/2
        Mrc = Crs*es + Qr*ec_lev
        Vh  = Qr; dc = 0.0
        steps.append(("→ Cas B: ANP dans l'aile", r"t_{fc} = \frac{C_{rs}}{C_{rf,max}} t_f", tfc, "mm"))
        steps.append(("dt = centroïde acier tendu", r"\frac{0.5 A_s d - 0.5 b_f t_{fc}^2}{A_s - b_f t_{fc}}", dt, "mm"))
        steps.append(("es = dt - tfc/2", r"d_t - t_{fc}/2", es, "mm"))
        steps.append(("e' = dt + hd + tc - ae/2", r"d_t + h_d + t_c - a_e/2", ec_lev, "mm"))
        steps.append(("M_rc = Crs·es + Qr·e'", r"C_{rs} e_s + Q_r e'", Mrc/1e6, "kN·m"))
        return dict(case='b', Mrc=Mrc/1e6, Vh=Qr/1e3, ae=ae,
                    Cr_prime=Qr/1e3, Cr_steel=Crs/1e3, Tr_max=Tr/1e3,
                    Cr_max=Cr/1e3, a1=a1, e=es, e_prime=ec_lev,
                    dt=dt, dc=dc, steps=steps)
    else:
        case = 'c'
        Crw  = Crs - Crfmax
        hc   = Crw/(PHI*tw*Fy)
        Asf  = bf*tf
        Asc2 = Asf + hc*tw
        dc   = (0.5*Asf*tf + hc*tw*(tf+0.5*hc))/Asc2
        dt   = (As*0.5*d - Asc2*(d-dc))/(As-Asc2)
        es   = d - dc - dt
        ec_lev = d + hd + tc - dt - ae/2
        Mrc  = Crs*es + Qr*ec_lev
        Vh   = Qr
        steps.append(("→ Cas C: ANP dans l'âme", r"h_c = \frac{C_{rw}}{\phi t_w F_y}", hc, "mm"))
        steps.append(("dc = centroïde acier comprimé", r"\frac{0.5 A_{sf} t_f + h_c t_w (t_f+0.5h_c)}{A_{sc}}", dc, "mm"))
        steps.append(("dt = centroïde acier tendu", r"\frac{A_s \cdot 0.5d - A_{sc}(d-d_c)}{A_s - A_{sc}}", dt, "mm"))
        steps.append(("es = d - dc - dt", r"d - d_c - d_t", es, "mm"))
        steps.append(("e' = d + hd + tc - dt - ae/2", r"d + h_d + t_c - d_t - a_e/2", ec_lev, "mm"))
        steps.append(("M_rc = Crs·es + Qr·e'", r"C_{rs} e_s + Q_r e'", Mrc/1e6, "kN·m"))
        return dict(case='c', Mrc=Mrc/1e6, Vh=Qr/1e3, ae=ae,
                    Cr_prime=Qr/1e3, Cr_steel=Crs/1e3, Tr_max=Tr/1e3,
                    Cr_max=Cr/1e3, a1=a1, e=es, e_prime=ec_lev,
                    dt=dt, dc=dc, steps=steps)

def els_calc(sec, fc, be, tc, hd, p, rho, formula, phi_cr=2.7, chi=0.73):
    As=sec['As']; d=sec['d']; Is=sec['Ix']*1e6
    n, Ecv = n_ratio(fc, rho, formula)
    ys = d/2 + hd + tc
    ybar = n*(As/be)*(math.sqrt(1+2*be*ys/(n*As))-1)
    if ybar <= tc:
        It = be*ybar**3/(3*n) + Is + As*(ys-ybar)**2
    else:
        Ac = be*tc/n; yc = tc/2
        ybar = (Ac*yc+As*ys)/(Ac+As)
        It = be*tc**3/(12*n)+Ac*(ybar-yc)**2+Is+As*(ys-ybar)**2
    Ie = Is + 0.85*(p**0.25)*(It-Is)
    # Creep
    Ecp  = Ecv/(1+chi*phi_cr)
    ns   = E_S/Ecp
    ybar_c = ns*(As/be)*(math.sqrt(1+2*be*ys/(ns*As))-1)
    if ybar_c <= tc:
        Its = be*ybar_c**3/(3*ns)+Is+As*(ys-ybar_c)**2
    else:
        Ac2=be*tc/ns; yc2=tc/2
        ybar_c=(Ac2*yc2+As*ys)/(Ac2+As)
        Its=be*tc**3/(12*ns)+Ac2*(ybar_c-yc2)**2+Is+As*(ys-ybar_c)**2
    Ies = Is+0.85*(p**0.25)*(Its-Is)
    return dict(Is=Is, It=It, Ie=Ie, Its=Its, Ies=Ies,
                n=n, Ec=Ecv, ns=ns, Ecp=Ecp,
                ybar=ybar, ybar_c=ybar_c,
                phi_cr=phi_cr, chi=chi)

def deflections(sec, els, w_dead, w_live, L, eps_sh=583e-6, c=0.5):
    E = E_S; Ie=els['Ie']; Ies=els['Ies']
    def delta(w,I): return 5*(w*1e3/1e3)*( L*1e3)**4/(384*E*I)
    dL = delta(w_live, Ie)
    dD = delta(w_dead, Ie)
    dCreep = 0.15*dD
    # Shrinkage
    ns=els['ns']; As=sec['As']; d=sec['d']
    ybar_c=els['ybar_c']
    tc_val = None  # will be passed from outside
    return dict(dL=dL, dD=dD, dCreep=dCreep)

# ══════════════════════════════════════════════════════════════════════════════
#  PLOTLY HELPERS
# ══════════════════════════════════════════════════════════════════════════════
BLUE   = "#1d4ed8"; LBLUE  = "#93c5fd"; GREY   = "#78716c"; LGREY  = "#e2e8f0"
AMBER  = "#d97706"; GREEN  = "#16a34a"; RED    = "#dc2626"; PURPLE = "#7c3aed"
BG     = "#f8fafc"; DARK   = "#1e293b"

def cross_section_fig(sec, tc, hd, be, elu):
    d=sec['d']; bf=sec['bf']; tf=sec['tf']; tw=sec['tw']
    tot = d+hd+tc
    # normalise be for display
    be_disp = min(be, bf*4)
    fig = go.Figure()
    # slab
    fig.add_shape(type="rect",x0=-be_disp/2,x1=be_disp/2,y0=d+hd,y1=d+hd+tc,
                  fillcolor=LGREY,line=dict(color=GREY,width=2))
    # deck
    if hd>0:
        fig.add_shape(type="rect",x0=-be_disp/2,x1=be_disp/2,y0=d,y1=d+hd,
                      fillcolor="rgba(220,211,202,0.5)",line=dict(color=GREY,width=1,dash='dot'))
    # top flange
    fig.add_shape(type="rect",x0=-bf/2,x1=bf/2,y0=d-tf,y1=d,
                  fillcolor=LBLUE,line=dict(color=BLUE,width=1.5))
    # web
    fig.add_shape(type="rect",x0=-tw/2,x1=tw/2,y0=tf,y1=d-tf,
                  fillcolor=LBLUE,line=dict(color=BLUE,width=1.5))
    # bottom flange
    fig.add_shape(type="rect",x0=-bf/2,x1=bf/2,y0=0,y1=tf,
                  fillcolor=LBLUE,line=dict(color=BLUE,width=1.5))

    # ANP line
    case=elu['case']; ae=elu['ae']
    dt=elu['dt']; dc=elu.get('dc',0)
    if case=='a':   y_anp = d+hd+tc-ae
    elif case=='b':
        tfc_v = elu['Cr_steel']*1e3/(PHI*bf*sec['tf']*350) if elu['Cr_steel']>0 else 0
        # recompute tfc properly
        Fy_est=350
        tfc_v = min(elu['Cr_steel']*1e3/(PHI*bf*Fy_est), tf)
        y_anp = d-tfc_v
    else:
        Crf=PHI*bf*tf*350/1e3
        hc_v=(elu['Cr_steel']-Crf)*1e3/(PHI*tw*350)
        y_anp = d-tf-max(hc_v,0)

    fig.add_shape(type="line",x0=-be_disp/2*1.1,x1=be_disp/2*1.1,y0=y_anp,y1=y_anp,
                  line=dict(color=RED,width=2.5,dash="dash"))
    fig.add_annotation(x=be_disp/2*1.15,y=y_anp,text=f"<b>ANP</b><br>Cas {case.upper()}",
                       showarrow=False,font=dict(color=RED,size=11),xanchor="left")

    # ae bracket
    fig.add_shape(type="rect",x0=-be_disp/2,x1=be_disp/2,
                  y0=d+hd+tc-ae,y1=d+hd+tc,
                  fillcolor="rgba(217,119,6,0.25)",line=dict(color=AMBER,width=2))
    fig.add_annotation(x=-be_disp/2*1.2,y=d+hd+tc-ae/2,
                       text=f"<b>ae={ae:.1f}mm</b>",
                       showarrow=True,arrowhead=2,ax=40,ay=0,
                       font=dict(color=AMBER,size=10))

    # dimension labels
    for y_mm, lbl in [(0,"0"),(d,f"d={d}mm"),(d+hd,f"+hd={hd}mm" if hd else None),(d+hd+tc,f"+tc={tc}mm")]:
        if lbl is None: continue
        fig.add_annotation(x=-be_disp/2*1.4,y=y_mm,text=lbl,
                           showarrow=False,font=dict(color=GREY,size=9),xanchor="right")

    fig.update_layout(
        title=dict(text=f"<b>Section composite — {sec.get('name','')}</b><br>"
                       f"<sub>Cas {case.upper()} · ANP · be={be}mm</sub>",
                   font=dict(size=14,color=DARK)),
        height=480, plot_bgcolor=BG, paper_bgcolor="white",
        xaxis=dict(visible=False, range=[-be_disp*0.75, be_disp*0.75]),
        yaxis=dict(visible=False, range=[-tot*0.08, tot*1.12]),
        margin=dict(l=80,r=80,t=70,b=20),
        showlegend=False,
    )
    return fig

def ane_fig(sec, tc, hd, be, els_r):
    d=sec['d']; bf=sec['bf']; tf=sec['tf']; tw=sec['tw']
    tot=d+hd+tc
    be_disp=min(be,bf*3.5)
    fig=go.Figure()
    # slab
    fig.add_shape(type="rect",x0=-be_disp/2,x1=be_disp/2,y0=d+hd,y1=d+hd+tc,
                  fillcolor=LGREY,line=dict(color=GREY,width=1.5))
    if hd>0:
        fig.add_shape(type="rect",x0=-be_disp/2,x1=be_disp/2,y0=d,y1=d+hd,
                      fillcolor="rgba(220,211,202,0.4)",line=dict(color=GREY,width=1,dash='dot'))
    for y0,y1 in [(0,tf),(d-tf,d)]:
        fig.add_shape(type="rect",x0=-bf/2,x1=bf/2,y0=y0,y1=y1,
                      fillcolor=LBLUE,line=dict(color=BLUE,width=1.5))
    fig.add_shape(type="rect",x0=-tw/2,x1=tw/2,y0=tf,y1=d-tf,
                  fillcolor=LBLUE,line=dict(color=BLUE,width=1.5))

    ybar_e = els_r['ybar']     # from TOP of slab
    ybar_c = els_r['ybar_c']
    n_v    = els_r['n']
    ns_v   = els_r['ns']

    for ybar_top, color, label, dash in [
        (ybar_e, AMBER,  f"ANE instantané  ȳ={ybar_e:.1f}mm  (n={n_v:.2f})", "solid"),
        (ybar_c, PURPLE, f"ANE fluage/retrait  ȳ={ybar_c:.1f}mm  (nₛ={ns_v:.2f})", "dash"),
    ]:
        y_plot = tot - ybar_top  # from bottom of steel
        fig.add_shape(type="line",x0=-be_disp/2*1.05,x1=be_disp/2*1.05,
                      y0=y_plot,y1=y_plot,
                      line=dict(color=color,width=2.5,dash=dash))
        fig.add_annotation(x=be_disp/2*1.1,y=y_plot,text=f"<b>{label}</b>",
                           showarrow=False,font=dict(color=color,size=10),xanchor="left")

    fig.update_layout(
        title=dict(text="<b>Axes Neutres Élastiques (ANE)</b><br>"
                       f"<sub>Ec={els_r['Ec']:.0f} MPa · E'c={els_r['Ecp']:.0f} MPa (fluage)</sub>",
                   font=dict(size=14,color=DARK)),
        height=440, plot_bgcolor=BG, paper_bgcolor="white",
        xaxis=dict(visible=False,range=[-be_disp*0.9,be_disp*0.9]),
        yaxis=dict(visible=False,range=[-tot*0.05,tot*1.1]),
        margin=dict(l=20,r=200,t=70,b=20), showlegend=False,
    )
    return fig

def inertia_bar_fig(els_r, p):
    Is=els_r['Is']/1e6; It=els_r['It']/1e6
    Ie=els_r['Ie']/1e6; Its=els_r['Its']/1e6; Ies=els_r['Ies']/1e6
    labels=["Is<br>(acier seul)","It<br>(transformée)","Ie<br>(effective)",
            "Its<br>(fluage)","Ies<br>(eff. fluage)"]
    vals=[Is,It,Ie,Its,Ies]
    colors=[LBLUE,BLUE,AMBER,PURPLE,"#64748b"]
    gain=[0]+[(v/Is-1)*100 for v in vals[1:]]
    fig=go.Figure()
    fig.add_trace(go.Bar(x=labels,y=vals,marker_color=colors,
                         text=[f"{v:.0f}<br>+{g:.0f}%" if i>0 else f"{v:.0f}"
                               for i,(v,g) in enumerate(zip(vals,gain))],
                         textposition='outside',
                         hovertemplate="<b>%{x}</b><br>I = %{y:.0f} ×10⁶ mm⁴<extra></extra>"))
    fig.update_layout(
        title=dict(text=f"<b>Moments d'inertie</b>  [×10⁶ mm⁴]<br>"
                       f"<sub>p={p*100:.0f}%  · Ie = Is + 0.85·p^0.25·(It-Is)</sub>",
                   font=dict(size=14,color=DARK)),
        height=380, plot_bgcolor=BG, paper_bgcolor="white",
        xaxis=dict(tickfont=dict(size=11)),
        yaxis=dict(title="I [×10⁶ mm⁴]",gridcolor=LGREY),
        showlegend=False, margin=dict(t=80,b=20),
    )
    return fig

def stud_fig(L, n_half, qr_N, Vh):
    n_tot = 2*n_half
    spacing = (L/2)/(n_half+1) if n_half>0 else L/2
    MAX=18; show=min(n_half,MAX)
    sp2 = (L/2)/(show+1)

    fig = go.Figure()
    # beam body
    fig.add_shape(type="rect",x0=0,x1=L,y0=0,y1=0.4,
                  fillcolor=LBLUE,line=dict(color=BLUE,width=2))
    # slab
    fig.add_shape(type="rect",x0=0,x1=L,y0=0.4,y1=0.9,
                  fillcolor=LGREY,line=dict(color=GREY,width=1.5))
    # studs
    for half in range(2):
        x0=half*L/2
        for i in range(1,show+1):
            x=x0+i*sp2
            fig.add_shape(type="line",x0=x,x1=x,y0=0.3,y1=0.95,
                          line=dict(color=RED,width=max(1.5,14/show)))
            fig.add_shape(type="circle",x0=x-0.03,x1=x+0.03,y0=0.92,y1=0.98,
                          fillcolor=RED,line=dict(color=RED))

    # Mmax line
    fig.add_shape(type="line",x0=L/2,x1=L/2,y0=-0.1,y1=1.3,
                  line=dict(color=AMBER,width=1.5,dash="dash"))
    fig.add_annotation(x=L/2,y=1.32,text="<b>M<sub>max</sub></b>",
                       font=dict(color=AMBER,size=12),showarrow=False)

    # half-span arrows
    for x0,x1 in [(0,L/2),(L/2,L)]:
        mid=(x0+x1)/2
        fig.add_annotation(x=x0,y=1.15,ax=x1,ay=1.15,
                           axref='x',ayref='y',
                           arrowhead=2,arrowcolor=GREY,
                           text="",showarrow=True)
        fig.add_annotation(x=x1,y=1.15,ax=x0,ay=1.15,
                           axref='x',ayref='y',
                           arrowhead=2,arrowcolor=GREY,
                           text="",showarrow=True)
        fig.add_annotation(x=mid,y=1.22,
                           text=f"<b>L/2={L/2:.1f}m · {n_half} goujons</b>",
                           showarrow=False,font=dict(color=DARK,size=11))

    util=min(Vh/(n_tot*qr_N/1e3)*100,999)
    fig.update_layout(
        title=dict(text=f"<b>Distribution des goujons</b><br>"
                       f"<sub>n_total={n_tot} · q_r={qr_N/1e3:.2f}kN/goujon · V_h={Vh:.0f}kN · util={util:.0f}%</sub>",
                   font=dict(size=14,color=DARK)),
        height=320, plot_bgcolor=BG, paper_bgcolor="white",
        xaxis=dict(visible=False,range=[-L*0.03,L*1.03]),
        yaxis=dict(visible=False,range=[-0.2,1.5]),
        margin=dict(t=80,b=10), showlegend=False,
    )
    return fig

def deflection_fig(dL, dD, dCreep, dSh, L):
    limit=L*1000/360
    d_lc=dL+dCreep; d_tot=dL+dCreep+dSh
    cats=["Δ_L<br>(vivante)","Δ_D<br>(morte)","Δ_fluage<br>(+15%DL)","Δ_retrait","Δ_L+fluage","Δ_total"]
    vals=[dL,dD,dCreep,dSh,d_lc,d_tot]
    colors=[BLUE,"#6366f1",AMBER,PURPLE,
            GREEN if d_lc<=limit else RED,
            GREEN if d_tot<=limit else RED]
    fig=go.Figure()
    fig.add_trace(go.Bar(x=cats,y=vals,marker_color=colors,
                         text=[f"{v:.1f}mm" for v in vals],
                         textposition='outside',
                         hovertemplate="<b>%{x}</b><br>Δ = %{y:.2f} mm<extra></extra>"))
    fig.add_hline(y=limit,line=dict(color=RED,width=2,dash="dash"),
                  annotation_text=f"L/360 = {limit:.1f}mm",
                  annotation_font=dict(color=RED,size=11))
    fig.update_layout(
        title=dict(text="<b>Déflexions ELS</b><br>"
                       f"<sub>L/360 = {limit:.1f}mm · L={L:.1f}m</sub>",
                   font=dict(size=14,color=DARK)),
        height=380, plot_bgcolor=BG, paper_bgcolor="white",
        yaxis=dict(title="Δ [mm]",gridcolor=LGREY),
        xaxis=dict(tickfont=dict(size=11)),
        showlegend=False, margin=dict(t=80,b=20),
    )
    return fig

def moment_gauge(Mrc, Mr_steel, Mf):
    gain=(Mrc/Mr_steel-1)*100
    util=Mf/Mrc*100
    fig=go.Figure()
    fig.add_trace(go.Bar(
        x=["Mr acier seul","M_rc composite","M_f factorée"],
        y=[Mr_steel,Mrc,Mf],
        marker_color=[LBLUE,BLUE,RED if Mf>Mrc else GREEN],
        text=[f"<b>{v:.1f} kN·m</b>" for v in [Mr_steel,Mrc,Mf]],
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>%{y:.1f} kN·m<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text=f"<b>Résistance en flexion ELU</b><br>"
                       f"<sub>Gain composite: +{gain:.0f}% · Utilisation: {util:.0f}%</sub>",
                   font=dict(size=14,color=DARK)),
        height=360, plot_bgcolor=BG, paper_bgcolor="white",
        yaxis=dict(title="Moment [kN·m]",gridcolor=LGREY),
        showlegend=False, margin=dict(t=80,b=20),
    )
    return fig

# ══════════════════════════════════════════════════════════════════════════════
#  STREAMLIT UI
# ══════════════════════════════════════════════════════════════════════════════

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
  html,body,[class*="css"]{font-family:'Inter',sans-serif;}
  .block-container{padding-top:1rem;padding-bottom:2rem;}
  .formula-box{background:#f0f9ff;border-left:4px solid #1d4ed8;padding:10px 16px;
               border-radius:0 8px 8px 0;margin:6px 0;font-size:0.95em;}
  .result-card{background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;
               padding:16px;margin:6px 0;box-shadow:0 2px 8px rgba(0,0,0,0.06);}
  .ok-badge{background:#dcfce7;color:#15803d;padding:4px 10px;border-radius:20px;
            font-weight:700;font-size:0.85em;}
  .warn-badge{background:#fef9c3;color:#a16207;padding:4px 10px;border-radius:20px;
              font-weight:700;font-size:0.85em;}
  .fail-badge{background:#fee2e2;color:#b91c1c;padding:4px 10px;border-radius:20px;
              font-weight:700;font-size:0.85em;}
  .step-row{background:#f8fafc;border-radius:8px;padding:8px 12px;margin:3px 0;
            font-family:monospace;font-size:0.9em;}
  .disclaimer{background:#fef3c7;border:1px solid #d97706;border-radius:10px;
              padding:14px 18px;font-size:0.88em;color:#78350f;}
  .section-header{font-size:1.1em;font-weight:700;color:#1d4ed8;
                  border-bottom:2px solid #dbeafe;padding-bottom:4px;margin:16px 0 10px;}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown("## 🏗️")
with col_title:
    st.markdown("# Conception de Poutre Composite")
    st.markdown("**GCI-2011 · Université Laval** · CSA S16:24 Ch.17 · Module B1/B2")

# ── Disclaimer ────────────────────────────────────────────────────────────────
with st.expander("⚠️ Avertissement / Disclaimer — Lire avant utilisation", expanded=False):
    st.markdown("""
    <div class="disclaimer">
    <b>🎓 Outil pédagogique — GCI-2011 Conception des structures I</b><br><br>
    Cet outil interactif a été développé à des fins <b>exclusivement pédagogiques</b> dans le cadre du cours
    <b>GCI-2011 Conception des structures I</b> de l'<b>Université Laval</b> (Prof. Luca Sorelli).<br><br>
    <b>Limitations importantes :</b>
    <ul>
      <li>Les calculs sont basés sur CSA S16:24 Ch.17, CSA A23.3 et les notes de cours B1/B2.</li>
      <li>Cet outil <b>ne remplace pas</b> le jugement d'un ingénieur professionnel.</li>
      <li>Les résultats doivent être <b>vérifiés indépendamment</b> avant toute application réelle.</li>
      <li>Ni l'auteur ni l'Université Laval n'assument de responsabilité pour l'utilisation de ces résultats.</li>
      <li>Validé sur Ex. 7.1 (2026) et Ex. 7.2 du cours uniquement.</li>
    </ul>
    <b>EN UTILISANT CET OUTIL, VOUS ACCEPTEZ CES CONDITIONS.</b>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── SIDEBAR — All inputs ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Paramètres de conception")

    # Quick presets
    st.markdown("### 🎯 Exemples du cours")
    preset = st.radio("Charger un exemple :",
                      ["— Aucun —", "Ex. 7.1 — W410x54 (f'c=20)", "Ex. 7.1 — W410x54 (f'c=35)", "Ex. 7.2 — W310x39"],
                      index=0)

    st.divider()

    # Apply presets
    defaults = {}
    if "7.1" in preset and "20" in preset:
        defaults = dict(sec="W410x54",fc=20,Fy=350,be=2500,tc=65,hd=75,p=50,L=9.0,
                        wD=5.0,wL=8.0,gc=22.6,deck="Nervures ⊥ à la poutre",
                        dg=19,hsc=115,wd_val=180,ec_f="Simplifiée (4500√f'c)")
    elif "7.1" in preset and "35" in preset:
        defaults = dict(sec="W410x54",fc=35,Fy=350,be=2500,tc=65,hd=75,p=50,L=9.0,
                        wD=5.0,wL=8.0,gc=22.6,deck="Nervures ⊥ à la poutre",
                        dg=19,hsc=115,wd_val=180,ec_f="Simplifiée (4500√f'c)")
    elif "7.2" in preset:
        defaults = dict(sec="W310x39",fc=20,Fy=350,be=2100,tc=130,hd=0,p=40,L=9.0,
                        wD=9.975,wL=6.3,gc=25.0,deck="Dalle pleine (sans nervures)",
                        dg=19,hsc=115,wd_val=180,ec_f="Complète (3300√f'c+6900)·(ρ/2300)^1.5")

    st.markdown("### 🔩 Section d'acier")
    all_secs = sorted(T1.keys())
    sec_name = st.selectbox("Section T1 (HSC)", all_secs,
                             index=all_secs.index(defaults.get('sec','W410x54')))
    sec = T1[sec_name]; sec['name']=sec_name

    with st.expander("📐 Propriétés de la section"):
        c1,c2 = st.columns(2)
        c1.metric("As [mm²]", f"{sec['As']:,}")
        c2.metric("d [mm]", sec['d'])
        c1.metric("bf [mm]", sec['bf'])
        c2.metric("tf [mm]", sec['tf'])
        c1.metric("tw [mm]", sec['tw'])
        c2.metric("Ix [×10⁶ mm⁴]", sec['Ix'])
        c1.metric("Zx [×10³ mm³]", sec['Zx'])
        c2.metric("Poids [kN/m]", sec['dl'])

    st.markdown("### 🧱 Dalle de béton")
    fc_val = st.slider("f'c [MPa]", 20, 50, defaults.get('fc',20), 5)
    Fy_val = st.select_slider("Fy [MPa]", [300,350,400,450], defaults.get('Fy',350))
    be_val = st.slider("be — largeur efficace [mm]", 500, 4000, defaults.get('be',2500), 50)
    tc_val = st.slider("tc — épaisseur dalle [mm]", 50, 200, defaults.get('tc',65), 5)

    st.markdown("### 🏗️ Coffrage / Nervures")
    deck_type = st.selectbox("Type de coffrage",
                              ["Dalle pleine (sans nervures)",
                               "Nervures ⊥ à la poutre",
                               "Nervures ∥ à la poutre"],
                              index=["Dalle pleine (sans nervures)",
                                     "Nervures ⊥ à la poutre",
                                     "Nervures ∥ à la poutre"].index(
                                         defaults.get('deck',"Dalle pleine (sans nervures)")))
    hd_val = 0
    if deck_type != "Dalle pleine (sans nervures)":
        hd_val = st.select_slider("hd — hauteur nervures [mm]", [38,75], defaults.get('hd',75))
        wd_val = st.slider("wd — largeur nervures [mm]", 50, 300, defaults.get('wd_val',180), 10)

    st.markdown("### ⚡ Action composite")
    p_val  = st.slider("p — degré composite [%]", 25, 100, defaults.get('p',50), 5)
    L_val  = st.slider("L — portée [m]", 3.0, 15.0, defaults.get('L',9.0), 0.5)

    st.markdown("### 📦 Charges")
    wD_val = st.number_input("wD — charge morte [kN/m]", 0.0, 50.0, defaults.get('wD',5.0), 0.5)
    wL_val = st.number_input("wL — charge vive [kN/m]",  0.0, 80.0, defaults.get('wL',8.0), 0.5)

    st.markdown("### 🔧 Goujons de cisaillement")
    dg_val = st.select_slider("Diamètre goujon [mm]", [16,19,22,25], defaults.get('dg',19))
    if deck_type == "Nervures ⊥ à la poutre":
        hsc_val = st.select_slider("Hauteur goujon hsc [mm]", [75,90,115,140], defaults.get('hsc',115))
    gc_val  = st.slider("γc — densité béton [kN/m³]", 20.0, 26.0, defaults.get('gc',25.0), 0.5)
    ec_formula = st.selectbox("Formule Ec",
                               ["Simplifiée (4500√f'c)",
                                "Complète (3300√f'c+6900)·(ρ/2300)^1.5"],
                               index=0 if defaults.get('ec_f','Simplifiée')[:3]=='Sim' else 1)
    phi_cr = st.slider("φ — coefficient de fluage", 1.0, 3.5, 2.7, 0.1)

    st.markdown("### 🔢 Facteur NBCC")
    alpha_D = st.number_input("αD (charge morte)", 0.5, 1.5, 1.25, 0.05)
    alpha_L = st.number_input("αL (charge vive)",  0.5, 2.0, 1.50, 0.05)

# ══════════════════════════════════════════════════════════════════════════════
#  CALCULATIONS
# ══════════════════════════════════════════════════════════════════════════════
rho = gc_val*1000/9.81
p   = p_val/100.0
ec_f_key = 'simplified' if 'Simpli' in ec_formula else 'full'

# Stud resistance
if deck_type == "Dalle pleine (sans nervures)":
    qr_N = compute_qrs(dg_val, fc_val, rho, ec_f_key)
    hd_val = 0
elif deck_type == "Nervures ⊥ à la poutre":
    qr_N = compute_qrr_perp(dg_val, fc_val, hd_val, hsc_val, wd_val, rho, ec_f_key)
else:
    qr_N = compute_qrr_parallel(dg_val, fc_val, hd_val, wd_val, rho, ec_f_key)

# ELU
Qr_N = p * min(PHI*sec['As']*Fy_val, alpha1(fc_val)*PHI_C*be_val*tc_val*fc_val)
elu_r = elu_calc(sec, fc_val, Fy_val, be_val, tc_val, hd_val, p, Qr_N)

n_half = math.ceil(elu_r['Vh']*1e3 / qr_N)
n_tot  = 2*n_half

# ELS
els_r = els_calc(sec, fc_val, be_val, tc_val, hd_val, p, rho, ec_f_key, phi_cr)
Ie=els_r['Ie']; E=200_000
w_dead_tot = wD_val + sec['dl']
dL     = 5*(wL_val*1e3/1e3)*(L_val*1e3)**4/(384*E*Ie)
dD     = 5*(w_dead_tot*1e3/1e3)*(L_val*1e3)**4/(384*E*Ie)
dCreep = 0.15*dD
dSh    = 0.0  # simplified (shrinkage full calc needs eps_sh)

# Demands
wu   = max(alpha_D*w_dead_tot + alpha_L*wL_val, 1.4*w_dead_tot)
Mf   = wu * L_val**2 / 8
Mr_steel = PHI * sec['Zx'] * 1e3 * Fy_val / 1e6

# ══════════════════════════════════════════════════════════════════════════════
#  RESULTS DISPLAY
# ══════════════════════════════════════════════════════════════════════════════

# ── Top KPI strip ─────────────────────────────────────────────────────────────
st.markdown("## 📊 Résultats")
k1,k2,k3,k4,k5 = st.columns(5)
mrc_ok = elu_r['Mrc'] >= Mf
def_ok = (dL+dCreep) <= L_val*1000/360

k1.metric("M_rc [kN·m]", f"{elu_r['Mrc']:.1f}",
          delta=f"+{(elu_r['Mrc']/Mr_steel-1)*100:.0f}% vs acier seul")
k2.metric("M_f [kN·m]", f"{Mf:.1f}",
          delta=f"{'✅ OK' if mrc_ok else '❌ FAIL'}",
          delta_color="normal" if mrc_ok else "inverse")
k3.metric("n goujons total", n_tot,
          delta=f"q_r={qr_N/1e3:.2f} kN/goujon")
k4.metric("Δ_L+fluage [mm]", f"{dL+dCreep:.1f}",
          delta=f"L/360={L_val*1000/360:.0f}mm {'✅' if def_ok else '❌'}",
          delta_color="normal" if def_ok else "inverse")
k5.metric("Cas ANP", elu_r['case'].upper(),
          delta=f"ae={elu_r['ae']:.1f}mm")

st.divider()

# ── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔺 ELU — Flexion", "🔧 Goujons", "📐 Section & ANP",
    "📏 ELS — Déflexions", "📚 Formules"
])

# ════════ TAB 1 — ELU ═══════════════════════════════════════════════════════
with tab1:
    col_fig, col_steps = st.columns([1.2, 1])
    with col_fig:
        st.plotly_chart(moment_gauge(elu_r['Mrc'], Mr_steel, Mf),
                        use_container_width=True)
        st.plotly_chart(cross_section_fig(sec, tc_val, hd_val, be_val, elu_r),
                        use_container_width=True)

    with col_steps:
        st.markdown('<div class="section-header">🧮 Étapes de calcul ELU (§17.9.3)</div>',
                    unsafe_allow_html=True)
        case_names = {'a':'ANP dans la dalle','b':"ANP dans l'aile",'c':"ANP dans l'âme"}
        badge_col = GREEN if mrc_ok else RED
        st.markdown(f"""
        <div class="result-card">
          <b>Cas {elu_r['case'].upper()}</b> — {case_names[elu_r['case']]}
          &nbsp;&nbsp;
          <span style="background:{badge_col};color:white;padding:3px 10px;
            border-radius:12px;font-size:0.85em">
            {'✅ M_rc ≥ M_f' if mrc_ok else '❌ M_rc < M_f'}
          </span>
        </div>
        """, unsafe_allow_html=True)

        for lbl, formula_latex, val, unit in elu_r['steps']:
            if '→ Cas' in lbl:
                st.markdown(f"""<div style="background:#dbeafe;border-radius:8px;
                    padding:8px 12px;margin:8px 0;font-weight:700;color:#1d4ed8">
                    {lbl}</div>""", unsafe_allow_html=True)
            else:
                col_a, col_b = st.columns([2,1])
                col_a.markdown(f'<div class="step-row">{lbl}</div>',
                               unsafe_allow_html=True)
                col_b.markdown(f'<div class="step-row" style="text-align:right;">'
                               f'<b>{val:.3g}</b> {unit}</div>',
                               unsafe_allow_html=True)

        # Key results summary
        st.markdown('<div class="section-header">📋 Synthèse ELU</div>',
                    unsafe_allow_html=True)
        for lbl, val, unit in [
            ("α₁",          elu_r['a1'],            ""),
            ("C'r,max",      elu_r['Cr_max'],         "kN"),
            ("Tr,max",       elu_r['Tr_max'],         "kN"),
            ("Qr (goujons)", elu_r['Vh'],             "kN"),
            ("ae",           elu_r['ae'],             "mm"),
            ("e' (levier)",  elu_r['e_prime'],        "mm"),
            ("M_rc",         elu_r['Mrc'],            "kN·m"),
            ("Mf factorée",  Mf,                      "kN·m"),
            ("Utilisation",  Mf/elu_r['Mrc']*100,    "%"),
        ]:
            c_a,c_b,c_c = st.columns([2,1,1])
            c_a.write(lbl)
            c_b.write(f"**{val:.4g}**")
            c_c.write(unit)

# ════════ TAB 2 — GOUJONS ═══════════════════════════════════════════════════
with tab2:
    col_diag, col_info = st.columns([1.5, 1])
    with col_diag:
        st.plotly_chart(stud_fig(L_val, n_half, qr_N, elu_r['Vh']),
                        use_container_width=True)

    with col_info:
        st.markdown('<div class="section-header">🔧 Résistance des goujons</div>',
                    unsafe_allow_html=True)
        deck_ref = {
            "Dalle pleine (sans nervures)": "§17.7.2.2",
            "Nervures ⊥ à la poutre":       "§17.7.2.4",
            "Nervures ∥ à la poutre":        "§17.7.2.3",
        }
        st.markdown(f"""
        <div class="result-card">
          <b>Type:</b> {deck_type}<br>
          <b>Référence:</b> {deck_ref[deck_type]}<br>
          <b>Diamètre:</b> dg = {dg_val} mm<br>
          <b>Asc:</b> π·dg²/4 = {math.pi*dg_val**2/4:.0f} mm²
        </div>
        """, unsafe_allow_html=True)

        _, Ecv = n_ratio(fc_val, rho, ec_f_key)
        qrs_base = compute_qrs(dg_val, fc_val, rho, ec_f_key)

        for lbl, val, unit in [
            ("Ec",     Ecv,          "MPa"),
            ("q_rs (dalle pleine)", qrs_base/1e3, "kN"),
            ("q_r utilisé",         qr_N/1e3,    "kN"),
            ("V_h = Q_r",           elu_r['Vh'],  "kN"),
            ("n par demi-portée",   n_half,        "goujons"),
            ("n total",             n_tot,         "goujons"),
            ("Q_r fourni",          n_tot*qr_N/1e3,"kN"),
            ("V_h / Q_r fourni",    elu_r['Vh']/(n_tot*qr_N/1e3)*100, "%"),
        ]:
            c_a,c_b,c_c = st.columns([2,1,1])
            c_a.write(lbl)
            c_b.write(f"**{val:.4g}**")
            c_c.write(unit)

        ok_conn = n_tot*qr_N/1e3 >= elu_r['Vh']
        st.markdown(f"""<div class="{'result-card' if ok_conn else 'result-card'}"
            style="margin-top:10px;background:{'#dcfce7' if ok_conn else '#fee2e2'}">
            <b>{'✅ Goujons suffisants' if ok_conn else '❌ Goujons insuffisants'}</b><br>
            Q_r fourni = {n_tot*qr_N/1e3:.1f} kN
            {'≥' if ok_conn else '<'} V_h = {elu_r['Vh']:.1f} kN
        </div>""", unsafe_allow_html=True)

        # Formula display
        st.markdown('<div class="section-header">📐 Formule</div>', unsafe_allow_html=True)
        if deck_type == "Dalle pleine (sans nervures)":
            st.markdown("""<div class="formula-box">
            q_rs = 0.5 · φsc · Asc · √(f'c · Ec) ≤ φsc · Asc · Fu<br>
            φsc = 0.80 · Fu = 415 MPa
            </div>""", unsafe_allow_html=True)
        elif deck_type == "Nervures ⊥ à la poutre":
            st.markdown("""<div class="formula-box">
            q_rr = 0.35 · φsc · ρc · Ap · √f'c ≤ q_rs<br>
            Ap = 2√2·h² + (√2/2)·h·wd  [pyramide]
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="formula-box">
            q_rr = q_rs · [0.75 + 0.167·(wd/hd − 1.5)]  si wd/hd ≥ 1.5<br>
            wd/hd = """ + (f"{wd_val/hd_val:.2f}" if hd_val else "—") + """
            </div>""", unsafe_allow_html=True)

# ════════ TAB 3 — SECTION & ANP/ANE ════════════════════════════════════════
with tab3:
    col_l, col_r = st.columns(2)
    with col_l:
        st.plotly_chart(cross_section_fig(sec, tc_val, hd_val, be_val, elu_r),
                        use_container_width=True)
    with col_r:
        st.plotly_chart(ane_fig(sec, tc_val, hd_val, be_val, els_r),
                        use_container_width=True)

    st.plotly_chart(inertia_bar_fig(els_r, p), use_container_width=True)

    st.markdown('<div class="section-header">📊 Paramètres ELS</div>',
                unsafe_allow_html=True)
    cols = st.columns(4)
    for i,(lbl,val,unit) in enumerate([
        ("n = Es/Ec",    els_r['n'],    ""),
        ("Ec",           els_r['Ec'],   "MPa"),
        ("ȳ (instantané)", els_r['ybar'], "mm"),
        ("It",           els_r['It']/1e6,"×10⁶mm⁴"),
        ("Ie",           els_r['Ie']/1e6,"×10⁶mm⁴"),
        ("nₛ (fluage)",  els_r['ns'],   ""),
        ("E'c (fluage)", els_r['Ecp'],  "MPa"),
        ("ȳ (fluage)",   els_r['ybar_c'],"mm"),
    ]):
        with cols[i%4]:
            st.metric(f"{lbl} [{unit}]" if unit else lbl, f"{val:.4g}")

# ════════ TAB 4 — ELS ════════════════════════════════════════════════════════
with tab4:
    st.plotly_chart(deflection_fig(dL, dD, dCreep, dSh, L_val),
                    use_container_width=True)

    st.markdown('<div class="section-header">📋 Synthèse des déflexions</div>',
                unsafe_allow_html=True)
    limit = L_val*1000/360
    rows = [
        ("Ie effective", f"{els_r['Ie']/1e6:.0f} ×10⁶ mm⁴", ""),
        ("Δ_L (vive)",       f"{dL:.2f} mm",    "✅" if dL<=limit else "⚠️"),
        ("Δ_D (morte)",      f"{dD:.2f} mm",    ""),
        ("Δ_fluage (+15%DL)",f"{dCreep:.2f} mm",""),
        ("Δ_L + fluage",     f"{dL+dCreep:.2f} mm",
         "✅ OK" if dL+dCreep<=limit else "❌ Dépasse L/360"),
        ("Limite L/360",     f"{limit:.1f} mm", ""),
    ]
    for lbl, val, status in rows:
        c1,c2,c3 = st.columns([3,2,2])
        c1.write(lbl); c2.write(f"**{val}**"); c3.write(status)

    st.markdown("""<div class="formula-box">
    Δ = 5·w·L⁴ / (384·E·Ie) · · · Ie = Is + 0.85·p^0.25·(It−Is)<br>
    Δ_fluage ≈ +15%·Δ_D  (§17.3.1b)  · · ·  Limite : L/360
    </div>""", unsafe_allow_html=True)

# ════════ TAB 5 — FORMULAS ════════════════════════════════════════════════════
with tab5:
    st.markdown("## 📚 Référentiel des formules — CSA S16:24 / GCI-2011")

    with st.expander("🔷 ELU — Résistance en flexion §17.9.3", expanded=True):
        st.markdown("""
        <div class="formula-box">
        <b>Résistances maximales :</b><br>
        T_r,max = φ · As · Fy<br>
        C'_r,max = α₁ · φc · be · tc · f'c<br>
        α₁ = 0.85 − 0.0015·f'c ≥ 0.67<br>
        <br>
        <b>Composite partiel (p < 100%) :</b><br>
        Q_r = p · min(T_r,max , C'_r,max)<br>
        C_rs = (T_r,max − Q_r) / 2<br>
        <br>
        <b>Cas A — ANP dans la dalle :</b><br>
        ae = Q_r / (α₁·φc·be·f'c) = T_r·tc / C'_r,max (proportion)<br>
        e' = d/2 + hd + tc − ae/2<br>
        M_rc = T_r · e'<br>
        <br>
        <b>Cas B — ANP dans l'aile (C_rs ≤ C_rf,max) :</b><br>
        t_fc = C_rs / C_rf,max · tf<br>
        dt = (0.5·As·d − 0.5·bf·t_fc²) / (As − bf·t_fc)<br>
        es = dt − t_fc/2 &nbsp;·&nbsp; e' = dt + hd + tc − ae/2<br>
        M_rc = C_rs·es + Q_r·e'<br>
        <br>
        <b>Cas C — ANP dans l'âme (C_rs > C_rf,max) :</b><br>
        hc = (C_rs − C_rf,max) / (φ·tw·Fy)<br>
        dc = (0.5·Asf·tf + hc·tw·(tf+0.5hc)) / Asc<br>
        es = d − dc − dt &nbsp;·&nbsp; e' = d + hd + tc − dt − ae/2<br>
        M_rc = C_rs·es + Q_r·e'
        </div>
        """, unsafe_allow_html=True)

    with st.expander("🔶 ELS — Moments d'inertie §17.3.1"):
        st.markdown("""
        <div class="formula-box">
        <b>Rapport modulaire :</b><br>
        n = Es / Ec &nbsp;·&nbsp; Ec = 4500·√f'c  (simplifiée, Ex.7.1 2026)<br>
        ou Ec = (3300·√f'c + 6900)·(ρ/2300)^1.5  (complète)<br>
        <br>
        <b>ANE instantané (position ȳ depuis le dessus de la dalle) :</b><br>
        ȳ = n·(As/be)·[√(1 + 2·be·ys/(n·As)) − 1]<br>
        ys = d/2 + hd + tc<br>
        It = be·ȳ³/(3n) + Is + As·(ys−ȳ)²  (si ȳ ≤ tc)<br>
        Ie = Is + 0.85·p^0.25·(It − Is)<br>
        <br>
        <b>ANE fluage (module âgé-ajusté) :</b><br>
        E'c = Ec / (1 + χ·φ) &nbsp;·&nbsp; χ=0.73, φ=2.7 (Annexe H)<br>
        nₛ = Es / E'c<br>
        Its, Ies calculés avec nₛ à la place de n
        </div>
        """, unsafe_allow_html=True)

    with st.expander("🔴 Goujons de cisaillement §17.7.2"):
        st.markdown("""
        <div class="formula-box">
        <b>Dalle pleine :</b><br>
        q_rs = 0.5·φsc·Asc·√(f'c·Ec) ≤ φsc·Asc·Fu<br>
        φsc = 0.80, Fu = 415 MPa (W59 Type B)<br>
        <br>
        <b>Nervures ⊥ à la poutre (hd=75mm) :</b><br>
        q_rr = 0.35·φsc·ρc·Ap·√f'c<br>
        Ap = 2√2·h² + (√2/2)·h·wd  [pyramide de décollement]<br>
        <br>
        <b>Nervures ∥ à la poutre :</b><br>
        q_rr = q_rs · [0.75 + 0.167·(wd/hd − 1.5)]  pour wd/hd ≥ 1.5<br>
        <br>
        <b>Nombre de goujons :</b><br>
        n ≥ V_h / q_rr &nbsp;·&nbsp; n_total = 2·ceil(V_h / q_rr)
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📊 Déflexions §17.3.1"):
        st.markdown("""
        <div class="formula-box">
        Δ = 5·w·L⁴ / (384·E·Ie)  [charge uniformément répartie]<br>
        Δ_fluage = Δ_D · 15%  (§17.3.1b, charge soutenue)<br>
        Δ_retrait = c·εsh·Ac·ȳ·L² / (8·nₛ·Ies)  [β₁=0.5, εsh=583×10⁻⁶]<br>
        Critère : Δ_vive + Δ_fluage ≤ L/360
        </div>
        """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────
st.divider()
st.markdown(f"""
<div style="text-align:center;color:#94a3b8;font-size:0.82em;padding:10px">
  GCI-2011 Conception des structures I · Université Laval · Prof. Luca Sorelli<br>
  CSA S16:24 Ch.17 · CSA A23.3 · Outil pédagogique — aucune responsabilité<br>
  Validé sur Ex.7.1 (2026) et Ex.7.2 · Python {sys.version[:6]} · Streamlit
</div>
""", unsafe_allow_html=True)
