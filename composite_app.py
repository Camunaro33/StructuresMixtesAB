# composite_app.py  — GCI-2011 Poutre Composite Interactive
# Université Laval · Luca Sorelli · CSA S16:24 / A23.3
# pip install streamlit plotly numpy

import math, sys, os, json, io
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG  — must be first Streamlit call
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="GCI-2011 · Poutre Composite",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  EMBEDDED ENGINEERING LIBRARY
# ══════════════════════════════════════════════════════════════════════════════
PHI=0.90; PHI_C=0.65; PHI_SC=0.80; F_SC=415.0; E_S=200_000

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
    "W460x52": dict(dl=0.510,As=6650, d=450,bf=152,tf=10.8,tw=8.0, Ix=212,  Zx=1090),
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
    "WWF1200x380":dict(dl=3.80,As=48400,d=1200,bf=500,tf=30.0,tw=16.0,Ix=12300,Zx=20500),
}

# ── Exercise presets ──────────────────────────────────────────────────────────
PRESETS = {
    "— Aucun —": None,
    "Ex 7.1a — W410x54 f'c=20 p=50% ⊥": dict(
        sec="W410x54", fc=20, Fy=350, be=2500, tc=65, hd=75, p=50, L=9.0,
        gc=22.6, ec_f="Simplifiée (4500√f'c)", Ec_given=None,
        deck="Nervures ⊥ à la poutre", dg=19, hsc=115, wd=180, Fu=415,
        wD=5.0, wL=8.0, aD=1.25, aL=1.50, struct="Plancher"),
    "Ex 7.1c — W410x54 f'c=35 p=50% ⊥": dict(
        sec="W410x54", fc=35, Fy=350, be=2500, tc=65, hd=75, p=50, L=9.0,
        gc=22.6, ec_f="Simplifiée (4500√f'c)", Ec_given=None,
        deck="Nervures ⊥ à la poutre", dg=19, hsc=115, wd=180, Fu=415,
        wD=5.0, wL=8.0, aD=1.25, aL=1.50, struct="Plancher"),
    "Ex 7.2 — W310x39 f'c=20 p=40% dalle": dict(
        sec="W310x39", fc=20, Fy=350, be=2100, tc=130, hd=0, p=40, L=9.0,
        gc=25.0, ec_f="Complète (3300√f'c+6900)·(ρ/2300)^1.5", Ec_given=None,
        deck="Dalle pleine (sans nervures)", dg=19, hsc=115, wd=150, Fu=415,
        wD=9.975, wL=6.3, aD=1.25, aL=1.50, struct="Plancher"),
    "Ex 7.3 — W410x46 f'c=25 p=50% léger ⊥": dict(
        sec="W410x46", fc=25, Fy=350, be=3000, tc=85, hd=75, p=50, L=12.0,
        gc=18.15, ec_f="Complète (3300√f'c+6900)·(ρ/2300)^1.5", Ec_given=None,
        deck="Nervures ⊥ à la poutre", dg=19, hsc=120, wd=180, Fu=415,
        wD=12.6, wL=7.2, aD=1.25, aL=1.50, struct="Plancher"),
    "Ex 7.4 — WWF1200x380 PONT Ec=30000": dict(
        sec="WWF1200x380", fc=35, Fy=350, be=1850, tc=200, hd=0, p=100, L=36.0,
        gc=24.0, ec_f="Donnée directement (pont)", Ec_given=30000,
        deck="Dalle pleine (sans nervures)", dg=20, hsc=150, wd=0, Fu=450,
        wD=28.9, wL=11.0, aD=1.25, aL=1.50, struct="Pont"),
    "Ex 7.5 — W460x52 f'c=25 p=100% ⊥": dict(
        sec="W460x52", fc=25, Fy=350, be=3050, tc=65, hd=75, p=100, L=12.2,
        gc=23.26, ec_f="Simplifiée (4500√f'c)", Ec_given=None,
        deck="Nervures ⊥ à la poutre", dg=19, hsc=115, wd=180, Fu=450,
        wD=14.0, wL=6.71, aD=1.25, aL=1.50, struct="Plancher"),
}

# ── Ec helper ─────────────────────────────────────────────────────────────────
def compute_Ec(fc, rho, formula, Ec_given=None):
    if formula == "Donnée directement (pont)" and Ec_given:
        return float(Ec_given)
    if "Complète" in formula:
        return (3300*math.sqrt(fc)+6900)*(rho/2300)**1.5
    return 4500*math.sqrt(fc)

def compute_Ap(h_stud, wd):
    return 2*math.sqrt(2)*h_stud**2 + (math.sqrt(2)/2)*h_stud*wd

def alpha1(fc): return max(0.85-0.0015*fc, 0.67)

def elu_calc(sec, fc, Fy, be, tc, hd, p, Ec_v):
    a1=alpha1(fc); As=sec['As']; d=sec['d']; bf=sec['bf']; tf=sec['tf']; tw=sec['tw']
    Tr=PHI*As*Fy; Cr=a1*PHI_C*be*tc*fc
    Qr=p*min(Tr,Cr); Crs=(Tr-Qr)/2; Crfmax=PHI*bf*tf*Fy
    ae=Qr/(a1*PHI_C*be*fc)
    steps=[
        ("α₁",          f"{a1:.4f}",      ""),
        ("T_r,max",      f"{Tr/1e3:.2f}",  "kN"),
        ("C'_r,max",     f"{Cr/1e3:.2f}",  "kN"),
        ("Q_r",          f"{Qr/1e3:.3f}",  "kN"),
        ("C_rs",         f"{Crs/1e3:.3f}", "kN"),
        ("C_rf,max",     f"{Crfmax/1e3:.3f}","kN"),
        ("ae",           f"{ae:.2f}",       "mm"),
    ]
    if p==1.0 and Cr>Tr:
        ep=d/2+hd+tc-ae/2; Mrc=Tr*ep; Vh=Tr; dt=d/2; dc=0.0
        steps+=[("→ Cas A","ANP dans la dalle",""),
                ("e'",f"{ep:.2f}","mm"),("M_rc",f"{Mrc/1e6:.3f}","kN·m")]
        return dict(case='a',Mrc=Mrc/1e6,Vh=Vh/1e3,ae=ae,
                    Cr_prime=Qr/1e3,Cr_steel=0,Tr_max=Tr/1e3,
                    Cr_max=Cr/1e3,a1=a1,e=0,e_prime=ep,dt=dt,dc=dc,steps=steps)
    if Crs<=Crfmax:
        tfc=Crs/Crfmax*tf
        dt=(0.5*As*d-0.5*bf*tfc**2)/(As-bf*tfc)
        es=dt-tfc/2; ep=dt+hd+tc-ae/2; Mrc=Crs*es+Qr*ep; dc=0.0
        steps+=[("→ Cas B","ANP dans l'aile",""),("tfc",f"{tfc:.3f}","mm"),
                ("dt",f"{dt:.3f}","mm"),("es",f"{es:.3f}","mm"),
                ("e'",f"{ep:.3f}","mm"),("M_rc",f"{Mrc/1e6:.3f}","kN·m")]
        return dict(case='b',Mrc=Mrc/1e6,Vh=Qr/1e3,ae=ae,
                    Cr_prime=Qr/1e3,Cr_steel=Crs/1e3,Tr_max=Tr/1e3,
                    Cr_max=Cr/1e3,a1=a1,e=es,e_prime=ep,dt=dt,dc=dc,steps=steps)
    else:
        Crw=Crs-Crfmax; hc=Crw/(PHI*tw*Fy)
        Asf=bf*tf; Asc2=Asf+hc*tw
        dc=(0.5*Asf*tf+hc*tw*(tf+0.5*hc))/Asc2
        dt=(As*0.5*d-Asc2*(d-dc))/(As-Asc2)
        es=d-dc-dt; ep=d+hd+tc-dt-ae/2; Mrc=Crs*es+Qr*ep
        steps+=[("→ Cas C","ANP dans l'âme",""),("hc",f"{hc:.3f}","mm"),
                ("dc",f"{dc:.3f}","mm"),("dt",f"{dt:.3f}","mm"),
                ("es",f"{es:.3f}","mm"),("e'",f"{ep:.3f}","mm"),
                ("M_rc",f"{Mrc/1e6:.3f}","kN·m")]
        return dict(case='c',Mrc=Mrc/1e6,Vh=Qr/1e3,ae=ae,
                    Cr_prime=Qr/1e3,Cr_steel=Crs/1e3,Tr_max=Tr/1e3,
                    Cr_max=Cr/1e3,a1=a1,e=es,e_prime=ep,dt=dt,dc=dc,steps=steps)

def els_calc(sec, fc, be, tc, hd, p, Ec_v, phi_cr=2.7, chi=0.73):
    As=sec['As']; d=sec['d']; Is=sec['Ix']*1e6
    n=E_S/Ec_v; ys=d/2+hd+tc
    ybar=n*(As/be)*(math.sqrt(1+2*be*ys/(n*As))-1)
    if ybar<=tc:
        It=be*ybar**3/(3*n)+Is+As*(ys-ybar)**2
        ybar_e=ybar
    else:
        Ac=be*tc/n; ybar_e=(Ac*tc/2+As*ys)/(Ac+As)
        It=be*tc**3/(12*n)+Ac*(ybar_e-tc/2)**2+Is+As*(ys-ybar_e)**2
    Ie=Is+0.85*(p**0.25)*(It-Is)
    Ecp=Ec_v/(1+chi*phi_cr); ns=E_S/Ecp
    ybar_c=ns*(As/be)*(math.sqrt(1+2*be*ys/(ns*As))-1)
    if ybar_c<=tc:
        Its=be*ybar_c**3/(3*ns)+Is+As*(ys-ybar_c)**2
        ybar_s=ybar_c
    else:
        Ac2=be*tc/ns; ybar_s=(Ac2*tc/2+As*ys)/(Ac2+As)
        Its=be*tc**3/(12*ns)+Ac2*(ybar_s-tc/2)**2+Is+As*(ys-ybar_s)**2
    Ies=Is+0.85*(p**0.25)*(Its-Is)
    return dict(Is=Is,It=It,Ie=Ie,Its=Its,Ies=Ies,
                n=n,Ec=Ec_v,ns=ns,Ecp=Ecp,
                ybar=ybar_e,ybar_c=ybar_s,phi_cr=phi_cr,chi=chi)

# ══════════════════════════════════════════════════════════════════════════════
#  PLOT HELPERS (Plotly)
# ══════════════════════════════════════════════════════════════════════════════
BL="#1d4ed8"; LBL="#93c5fd"; GR="#78716c"; LGR="#e2e8f0"
AM="#d97706"; GN="#16a34a"; RD="#dc2626"; PU="#7c3aed"; BG="#f8fafc"; DK="#1e293b"

def _layout(title, h=400):
    return dict(title=dict(text=title,font=dict(size=13,color=DK)),
                height=h,plot_bgcolor=BG,paper_bgcolor="white",
                showlegend=False,margin=dict(l=20,r=20,t=70,b=20))

def fig_moment(Mrc, Mr_steel, Mf):
    gain=(Mrc/Mr_steel-1)*100; util=Mf/Mrc*100
    fig=go.Figure()
    fig.add_trace(go.Bar(x=["Mr acier seul","M_rc composite","M_f factorée"],
        y=[Mr_steel,Mrc,Mf],marker_color=[LBL,BL,RD if Mf>Mrc else GN],
        text=[f"<b>{v:.1f} kN·m</b>" for v in [Mr_steel,Mrc,Mf]],
        textposition='outside'))
    fig.update_layout(**_layout(
        f"<b>Résistance en flexion ELU</b><br><sub>Gain composite: +{gain:.0f}%  ·  Utilisation: {util:.0f}%</sub>",380))
    fig.update_yaxes(title="Moment [kN·m]",gridcolor=LGR)
    return fig

def fig_xsec(sec, tc, hd, be, elu, uid="xsec"):
    d=sec['d']; bf=sec['bf']; be_d=min(be,bf*4); tot=d+hd+tc
    fig=go.Figure()
    fig.add_shape(type="rect",x0=-be_d/2,x1=be_d/2,y0=d+hd,y1=d+hd+tc,
                  fillcolor=LGR,line=dict(color=GR,width=2))
    if hd>0:
        fig.add_shape(type="rect",x0=-be_d/2,x1=be_d/2,y0=d,y1=d+hd,
                      fillcolor="rgba(220,211,202,0.5)",line=dict(color=GR,width=1,dash='dot'))
    for y0,y1 in [(0,sec['tf']),(d-sec['tf'],d)]:
        fig.add_shape(type="rect",x0=-bf/2,x1=bf/2,y0=y0,y1=y1,fillcolor=LBL,line=dict(color=BL,width=1.5))
    fig.add_shape(type="rect",x0=-sec['tw']/2,x1=sec['tw']/2,y0=sec['tf'],y1=d-sec['tf'],fillcolor=LBL,line=dict(color=BL,width=1.5))
    ae=elu['ae']; case=elu['case']
    if case=='a': y_anp=d+hd+tc-ae
    elif case=='b':
        tfc_v=elu['Cr_steel']*1e3/(PHI*bf*sec['tf']*350) if elu.get('Cr_steel',0)>0 else 0
        Fy_e=350; tfc_v=min(elu.get('Cr_steel',0)*1e3/(PHI*bf*Fy_e),sec['tf']) if elu.get('Cr_steel',0)>0 else 0
        y_anp=d-tfc_v
    else:
        Crf=PHI*bf*sec['tf']*350/1e3; hc_v=max((elu.get('Cr_steel',0)-Crf)*1e3/(PHI*sec['tw']*350),0)
        y_anp=d-sec['tf']-hc_v
    fig.add_shape(type="line",x0=-be_d/2*1.1,x1=be_d/2*1.1,y0=y_anp,y1=y_anp,
                  line=dict(color=RD,width=2.5,dash="dash"))
    fig.add_annotation(x=be_d/2*1.15,y=y_anp,text=f"<b>ANP — Cas {case.upper()}</b>",
                       showarrow=False,font=dict(color=RD,size=11),xanchor="left")
    fig.add_shape(type="rect",x0=-be_d/2,x1=be_d/2,y0=d+hd+tc-ae,y1=d+hd+tc,
                  fillcolor="rgba(217,119,6,0.3)",line=dict(color=AM,width=2))
    fig.add_annotation(x=-be_d/2*1.3,y=d+hd+tc-ae/2,text=f"<b>ae={ae:.1f}mm</b>",
                       showarrow=True,arrowhead=2,ax=50,ay=0,font=dict(color=AM,size=10))
    fig.update_layout(**_layout(f"<b>Section composite — {sec.get('name','')} — Cas {case.upper()}</b>",480),
                      uirevision=uid)
    fig.update_xaxes(visible=False,range=[-be_d*0.85,be_d*0.85])
    fig.update_yaxes(visible=False,range=[-tot*0.08,tot*1.12])
    return fig

def fig_ane(sec, tc, hd, be, els_r):
    d=sec['d']; bf=sec['bf']; be_d=min(be,bf*3.5); tot=d+hd+tc
    fig=go.Figure()
    fig.add_shape(type="rect",x0=-be_d/2,x1=be_d/2,y0=d+hd,y1=d+hd+tc,fillcolor=LGR,line=dict(color=GR,width=1.5))
    if hd>0:
        fig.add_shape(type="rect",x0=-be_d/2,x1=be_d/2,y0=d,y1=d+hd,fillcolor="rgba(220,211,202,0.4)",line=dict(color=GR,width=1,dash='dot'))
    for y0,y1 in [(0,sec['tf']),(d-sec['tf'],d)]:
        fig.add_shape(type="rect",x0=-bf/2,x1=bf/2,y0=y0,y1=y1,fillcolor=LBL,line=dict(color=BL,width=1.5))
    fig.add_shape(type="rect",x0=-sec['tw']/2,x1=sec['tw']/2,y0=sec['tf'],y1=d-sec['tf'],fillcolor=LBL,line=dict(color=BL,width=1.5))
    for ybar_top,color,label,dash_ in [
        (els_r['ybar'], AM, f"ANE instantané  ȳ={els_r['ybar']:.1f}mm  (n={els_r['n']:.2f})", "solid"),
        (els_r['ybar_c'],PU,f"ANE fluage  ȳ={els_r['ybar_c']:.1f}mm  (nₛ={els_r['ns']:.2f})","dash"),
    ]:
        y_pl=tot-ybar_top
        fig.add_shape(type="line",x0=-be_d/2*1.05,x1=be_d/2*1.05,y0=y_pl,y1=y_pl,line=dict(color=color,width=2.5,dash=dash_))
        fig.add_annotation(x=be_d/2*1.1,y=y_pl,text=f"<b>{label}</b>",showarrow=False,font=dict(color=color,size=9),xanchor="left")
    fig.update_layout(**_layout(f"<b>ANE — Axe Neutre Élastique</b><br><sub>Ec={els_r['Ec']:.0f} MPa · E'c={els_r['Ecp']:.0f} MPa (fluage)</sub>",440))
    fig.update_xaxes(visible=False,range=[-be_d*0.9,be_d*0.9])
    fig.update_yaxes(visible=False,range=[-tot*0.05,tot*1.1])
    return fig

def fig_inertia(els_r, p):
    Is=els_r['Is']/1e6; It=els_r['It']/1e6; Ie=els_r['Ie']/1e6
    Its=els_r['Its']/1e6; Ies=els_r['Ies']/1e6
    labels=["Is<br>(acier)","It<br>(transform.)","Ie<br>(effective)","Its<br>(fluage)","Ies<br>(eff.fluage)"]
    vals=[Is,It,Ie,Its,Ies]; colors=[LBL,BL,AM,PU,"#64748b"]
    text=[f"{v:.0f}" if i==0 else f"{v:.0f}<br>+{(v/Is-1)*100:.0f}%" for i,v in enumerate(vals)]
    fig=go.Figure(go.Bar(x=labels,y=vals,marker_color=colors,text=text,textposition='outside'))
    fig.update_layout(**_layout(f"<b>Moments d'inertie [×10⁶ mm⁴]</b><br><sub>p={p*100:.0f}%  ·  Ie=Is+0.85·p^0.25·(It-Is)</sub>",380))
    fig.update_yaxes(title="I [×10⁶ mm⁴]",gridcolor=LGR)
    return fig

def fig_studs(L, n_half, qr_N, Vh):
    n_tot=2*n_half; MAX=18; show=min(n_half,MAX); sp=(L/2)/(show+1) if show>0 else L/2
    lw=max(0.8,min(2.0,16/max(show,1)))
    fig=go.Figure()
    fig.add_shape(type="rect",x0=0,x1=L,y0=0,y1=0.4,fillcolor=LBL,line=dict(color=BL,width=2))
    fig.add_shape(type="rect",x0=0,x1=L,y0=0.4,y1=0.9,fillcolor=LGR,line=dict(color=GR,width=1.5))
    for half in range(2):
        x0=half*L/2
        for i in range(1,show+1):
            x=x0+i*sp
            fig.add_shape(type="line",x0=x,x1=x,y0=0.3,y1=0.95,line=dict(color=RD,width=lw))
            fig.add_shape(type="circle",x0=x-0.025*L/12,x1=x+0.025*L/12,y0=0.93,y1=0.97,fillcolor=RD,line=dict(color=RD))
        if n_half>MAX:
            fig.add_annotation(x=x0+L/4,y=1.02,text=f"({n_half} goujons)",showarrow=False,font=dict(color=RD,size=10))
    fig.add_shape(type="line",x0=L/2,x1=L/2,y0=-0.1,y1=1.3,line=dict(color=AM,width=1.5,dash="dash"))
    fig.add_annotation(x=L/2,y=1.35,text="<b>M_max</b>",font=dict(color=AM,size=11),showarrow=False)
    for x0,x1 in [(0,L/2),(L/2,L)]:
        mid=(x0+x1)/2
        fig.add_annotation(x=x0,y=1.18,ax=x1,ay=1.18,axref='x',ayref='y',arrowhead=2,arrowcolor=GR,text="",showarrow=True)
        fig.add_annotation(x=x1,y=1.18,ax=x0,ay=1.18,axref='x',ayref='y',arrowhead=2,arrowcolor=GR,text="",showarrow=True)
        fig.add_annotation(x=mid,y=1.25,text=f"<b>L/2={L/2:.1f}m · {n_half} goujons</b>",showarrow=False,font=dict(color=DK,size=10))
    util=min(Vh/(n_tot*qr_N/1e3)*100,999)
    fig.update_layout(**_layout(f"<b>Distribution des goujons</b><br><sub>n_total={n_tot} · q_r={qr_N/1e3:.2f} kN · V_h={Vh:.0f} kN · util={util:.0f}%</sub>",320))
    fig.update_xaxes(visible=False,range=[-L*0.03,L*1.03])
    fig.update_yaxes(visible=False,range=[-0.2,1.5])
    return fig

def fig_deflection(dL, dD, dCreep, dSh, L):
    limit=L*1000/360; d_lc=dL+dCreep; d_tot=dL+dCreep+dSh
    cats=["Δ_L<br>(vivante)","Δ_D<br>(morte)","Δ_fluage<br>(+15%DL)","Δ_retrait","Δ_L+fluage","Δ_total"]
    vals=[dL,dD,dCreep,dSh,d_lc,d_tot]
    colors=[BL,"#6366f1",AM,PU,GN if d_lc<=limit else RD,GN if d_tot<=limit else RD]
    fig=go.Figure(go.Bar(x=cats,y=vals,marker_color=colors,
        text=[f"{v:.1f}mm" for v in vals],textposition='outside'))
    fig.add_hline(y=limit,line=dict(color=RD,width=2,dash="dash"),
                  annotation_text=f"L/360={limit:.1f}mm",annotation_font=dict(color=RD))
    fig.update_layout(**_layout(f"<b>Déflexions ELS</b><br><sub>L/360={limit:.1f}mm · L={L:.1f}m</sub>",380))
    fig.update_yaxes(title="Δ [mm]",gridcolor=LGR)
    return fig

# ══════════════════════════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.block-container{padding-top:1rem;padding-bottom:2rem;}
.formula-box{background:#f0f9ff;border-left:4px solid #1d4ed8;padding:10px 16px;border-radius:0 8px 8px 0;margin:6px 0;font-size:0.93em;}
.result-card{background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:14px;margin:5px 0;box-shadow:0 2px 8px rgba(0,0,0,0.05);}
.step-row{background:#f8fafc;border-radius:6px;padding:6px 10px;margin:2px 0;font-family:monospace;font-size:0.88em;}
.disclaimer{background:#fef3c7;border:2px solid #d97706;border-radius:12px;padding:20px 24px;font-size:0.93em;color:#78350f;line-height:1.7;}
.section-hdr{font-size:1.05em;font-weight:700;color:#1d4ed8;border-bottom:2px solid #dbeafe;padding-bottom:3px;margin:14px 0 8px;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  DISCLAIMER GATE
# ══════════════════════════════════════════════════════════════════════════════
if 'disclaimer_accepted' not in st.session_state:
    st.session_state.disclaimer_accepted = False

if not st.session_state.disclaimer_accepted:
    st.markdown("<style>section[data-testid='stSidebar']{display:none}</style>",unsafe_allow_html=True)
    st.markdown("## 🏗️ Conception de Poutre Composite — GCI-2011 · Université Laval")
    st.divider()
    st.markdown("## ⚠️ Avertissement — Lire et accepter avant utilisation")
    st.markdown("""<div class="disclaimer">
    <b style="font-size:1.1em">🎓 Outil pédagogique — GCI-2011 Conception des structures I</b><br><br>
    Développé à des fins <b>exclusivement pédagogiques</b> dans le cadre du cours
    <b>GCI-2011</b> de l'<b>Université Laval</b> (Prof. Luca Sorelli).<br><br>
    <b>Limitations importantes :</b>
    <ul style="margin:8px 0 8px 20px">
      <li>Calculs basés sur <b>CSA S16:24 Ch.17</b>, CSA A23.3 et les notes de cours B1/B2.</li>
      <li>Cet outil <b>ne remplace pas</b> le jugement d'un ingénieur professionnel.</li>
      <li>Les résultats doivent être <b>vérifiés indépendamment</b> avant toute application réelle.</li>
      <li>Ni l'auteur ni l'Université Laval n'assument de <b>responsabilité</b> pour l'utilisation.</li>
      <li>Validé sur Ex. 7.1–7.5 du cours uniquement.</li>
    </ul>
    <b>EN CLIQUANT SUR « J'ACCEPTE », VOUS RECONNAISSEZ AVOIR LU ET COMPRIS CES CONDITIONS.</b>
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    agreed = st.checkbox("✅ J'ai lu et j'accepte les conditions d'utilisation", key="disclaimer_cb")
    col_btn,_=st.columns([1,4])
    with col_btn:
        if st.button("▶️ Accéder à l'outil", type="primary", disabled=not agreed, key="disclaimer_btn"):
            st.session_state.disclaimer_accepted=True; st.rerun()
    if not agreed:
        st.info("👆 Cochez la case ci-dessus pour activer le bouton d'accès.")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("## 🏗️ Conception de Poutre Composite")
st.markdown("**GCI-2011 · Université Laval** · CSA S16:24 Ch.17 · Module B1/B2")
st.markdown('<div style="display:inline-block;background:#dcfce7;color:#15803d;padding:3px 10px;border-radius:20px;font-size:0.82em;font-weight:600">✅ Avertissement accepté — outil pédagogique uniquement</div>',unsafe_allow_html=True)
st.divider()

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚙️ Paramètres")

    # ── Presets ──────────────────────────────────────────────────────────────
    st.markdown("### 🎯 Exercices du cours")
    preset_key = st.selectbox("Charger un exercice :", list(PRESETS.keys()), key="preset_sel")
    P = PRESETS[preset_key]  # None or dict

    # ── Import JSON ───────────────────────────────────────────────────────────
    st.markdown("### 📂 Importer des paramètres")
    uploaded = st.file_uploader("Fichier JSON (.json)", type=["json"], key="json_upload")
    if uploaded:
        try:
            raw = json.loads(uploaded.read())
            P = raw.get('gci2011_composite_beam',{}).get('inputs', raw)
            st.success(f"✅ Chargé : {P.get('description','fichier JSON')}")
        except Exception as e:
            st.error(f"Erreur: {e}")

    st.divider()

    def _v(key, default):
        return P.get(key, default) if P else default

    # ── Section ───────────────────────────────────────────────────────────────
    st.markdown("### 🔩 Section d'acier")
    all_secs = sorted(T1.keys())
    default_sec = _v('sec','W410x54')
    sec_idx = all_secs.index(default_sec) if default_sec in all_secs else all_secs.index('W410x54')
    sec_name = st.selectbox("Section T1 (HSC)", all_secs, index=sec_idx, key="sec_sel")
    sec = dict(T1[sec_name]); sec['name']=sec_name

    with st.expander("📐 Propriétés"):
        c1,c2=st.columns(2)
        c1.metric("As [mm²]",f"{sec['As']:,}"); c2.metric("d [mm]",sec['d'])
        c1.metric("bf [mm]",sec['bf']); c2.metric("tf [mm]",sec['tf'])
        c1.metric("tw [mm]",sec['tw']); c2.metric("Ix [×10⁶]",sec['Ix'])
        c1.metric("Zx [×10³]",sec['Zx']); c2.metric("Poids [kN/m]",sec['dl'])

    # ── Béton & acier ─────────────────────────────────────────────────────────
    st.markdown("### 🧱 Béton")
    fc_val  = st.slider("f'c [MPa]",   15, 60, _v('fc',20),   5, key="fc")
    Fy_val  = st.select_slider("Fy [MPa]",[300,350,400,450], _v('Fy',350), key="fy")
    be_val  = st.slider("be [mm]",    500,5000, _v('be',2500), 50, key="be")
    tc_val  = st.slider("tc [mm]",     50, 300, _v('tc',65),   5, key="tc")

    # ── Coffrage ──────────────────────────────────────────────────────────────
    st.markdown("### 🏗️ Coffrage")
    deck_opts=["Dalle pleine (sans nervures)","Nervures ⊥ à la poutre","Nervures ∥ à la poutre"]
    default_deck = _v('deck',"Dalle pleine (sans nervures)")
    deck_idx = deck_opts.index(default_deck) if default_deck in deck_opts else 0
    deck_type = st.selectbox("Type de coffrage", deck_opts, index=deck_idx, key="deck")
    hd_val=0
    if deck_type != "Dalle pleine (sans nervures)":
        hd_val = st.select_slider("hd [mm]",[38,75], _v('hd',75), key="hd")
        wd_val = st.slider("wd [mm]", 50,300, _v('wd',180), 10, key="wd")
    else:
        wd_val=180

    # ── Structure type & Ec ───────────────────────────────────────────────────
    st.markdown("### ⚙️ Formule Ec")
    ec_opts=["Simplifiée (4500√f'c)","Complète (3300√f'c+6900)·(ρ/2300)^1.5","Donnée directement (pont)"]
    default_ec = _v('ec_f',"Simplifiée (4500√f'c)")
    ec_idx = ec_opts.index(default_ec) if default_ec in ec_opts else 0
    ec_formula = st.selectbox("", ec_opts, index=ec_idx, key="ec_form")
    gc_val = st.slider("γc [kN/m³]", 18.0,26.0, float(_v('gc',25.0)), 0.5, key="gc")
    Ec_given_val = None
    if ec_formula == "Donnée directement (pont)":
        Ec_given_val = st.number_input("Ec [MPa]", 10000,50000, int(_v('Ec_given',30000) or 30000), 500, key="ec_given")

    rho  = gc_val*1000/9.81
    Ec_v = compute_Ec(fc_val, rho, ec_formula, Ec_given_val)
    st.caption(f"Ec = {Ec_v:.0f} MPa  →  n = {200000/Ec_v:.2f}")

    # ── Composite & span ──────────────────────────────────────────────────────
    st.markdown("### ⚡ Composite & Portée")
    p_val = st.slider("p [%]",25,100, _v('p',50), 5, key="p_pct")
    L_val = st.slider("L [m]", 3.0,40.0, float(_v('L',9.0)), 0.5, key="span")

    # ── Charges ───────────────────────────────────────────────────────────────
    st.markdown("### 📦 Charges")
    wD_val = st.number_input("wD [kN/m]",0.0,200.0, float(_v('wD',5.0)), 0.5, key="wD")
    wL_val = st.number_input("wL [kN/m]",0.0,200.0, float(_v('wL',8.0)), 0.5, key="wL")

    # ── Goujons ───────────────────────────────────────────────────────────────
    st.markdown("### 🔧 Goujons")
    dg_val  = st.select_slider("d_goujon [mm]",[16,19,20,22,25], _v('dg',19), key="dg")
    Fu_val  = st.select_slider("Fu [MPa]",[415,450], _v('Fu',415), key="fu")
    phi_cr  = st.slider("φ fluage",1.0,3.5,2.7,0.1, key="phi_cr")
    if deck_type=="Nervures ⊥ à la poutre":
        hsc_val=st.select_slider("h_stud [mm]",[75,90,115,120,140], _v('hsc',115), key="hsc")
    else:
        hsc_val=115

    # ── NBCC ──────────────────────────────────────────────────────────────────
    st.markdown("### 🔢 NBCC")
    aD_val=st.number_input("αD",0.5,1.5,1.25,0.05,key="aD")
    aL_val=st.number_input("αL",0.5,2.0,1.50,0.05,key="aL")

# ══════════════════════════════════════════════════════════════════════════════
#  CALCULATIONS
# ══════════════════════════════════════════════════════════════════════════════
p  = p_val/100.0
F_SC_used = Fu_val  # stud ultimate strength (from input)

# Stud resistance
Asc_stud = math.pi*dg_val**2/4
qrs_base = min(0.5*PHI_SC*Asc_stud*math.sqrt(fc_val*Ec_v), PHI_SC*Asc_stud*F_SC_used)
if deck_type=="Dalle pleine (sans nervures)":
    qr_N=qrs_base
elif deck_type=="Nervures ⊥ à la poutre":
    Ap=compute_Ap(hsc_val, wd_val)
    rho_c=1.0 if rho>=2150 else 0.85
    coef=0.35 if abs(hd_val-75)<5 else (0.61 if abs(hd_val-38)<5 else 0.35+(0.61-0.35)*(hd_val-38)/(75-38))
    qr_N=min(coef*PHI_SC*rho_c*Ap*math.sqrt(fc_val), qrs_base)
else:
    if hd_val>0 and wd_val/hd_val>=1.5:
        qr_N=min(qrs_base*(0.75+0.167*(wd_val/hd_val-1.5)),qrs_base)
    else:
        qr_N=0.75*qrs_base

Qr_N = p*min(PHI*sec['As']*Fy_val, alpha1(fc_val)*PHI_C*be_val*tc_val*fc_val)
elu_r = elu_calc(sec, fc_val, Fy_val, be_val, tc_val, hd_val, p, Ec_v)
n_half = math.ceil(elu_r['Vh']*1e3/qr_N) if qr_N>0 else 0
n_tot  = 2*n_half

els_r  = els_calc(sec, fc_val, be_val, tc_val, hd_val, p, Ec_v, phi_cr)
w_dead_tot = wD_val + sec['dl']
Ie=els_r['Ie']; E=200000; L_mm=L_val*1e3
def _delta(w,I): return 5*w*(L_mm**4)/(384*E*I)
dL    = _delta(wL_val, Ie)
dD    = _delta(w_dead_tot, Ie)
dCreep= 0.15*dD
dSh   = 0.0

wu   = max(aD_val*w_dead_tot+aL_val*wL_val, 1.4*w_dead_tot)
Mf   = wu*L_val**2/8
Mr_s = PHI*sec['Zx']*1e3*Fy_val/1e6

# ══════════════════════════════════════════════════════════════════════════════
#  EXPORT JSON (sidebar bottom)
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.divider()
    st.markdown("### 💾 Exporter les paramètres")
    if st.button("📥 Générer fichier JSON", key="export_btn"):
        exp_data = {
            "gci2011_composite_beam": {
                "version":"1.0",
                "inputs": dict(
                    description=f"Design — {sec_name}",
                    sec=sec_name, fc=fc_val, Fy=Fy_val, be=be_val,
                    tc=tc_val, hd=hd_val, p=p_val, L=L_val,
                    gc=gc_val, ec_f=ec_formula, Ec_given=Ec_given_val,
                    deck=deck_type, dg=dg_val, hsc=hsc_val, wd=wd_val,
                    Fu=Fu_val, wD=wD_val, wL=wL_val, aD=aD_val, aL=aL_val,
                    struct="Pont" if "pont" in ec_formula.lower() else "Plancher",
                )
            }
        }
        json_str = json.dumps(exp_data, indent=2, ensure_ascii=False)
        fname = f"beam_{sec_name.replace('/','-')}_p{p_val}.json"
        st.download_button("⬇️ Télécharger JSON", json_str, fname, "application/json", key="dl_json")

# ══════════════════════════════════════════════════════════════════════════════
#  KPI STRIP
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("## 📊 Résultats")
mrc_ok=(elu_r['Mrc']>=Mf); def_ok=(dL+dCreep)<=L_val*1000/360
k1,k2,k3,k4,k5=st.columns(5)
k1.metric("M_rc [kN·m]",f"{elu_r['Mrc']:.1f}",f"+{(elu_r['Mrc']/Mr_s-1)*100:.0f}% vs acier seul")
k2.metric("M_f [kN·m]",f"{Mf:.1f}",f"{'✅ OK' if mrc_ok else '❌ FAIL'}",delta_color="normal" if mrc_ok else "inverse")
k3.metric("n goujons",n_tot,f"q_r={qr_N/1e3:.2f} kN/goujon")
k4.metric("Δ_L+fluage [mm]",f"{dL+dCreep:.1f}",f"L/360={L_val*1000/360:.0f}mm {'✅' if def_ok else '❌'}",delta_color="normal" if def_ok else "inverse")
k5.metric("Cas ANP",elu_r['case'].upper(),f"ae={elu_r['ae']:.1f}mm")
st.divider()

# ══════════════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1,tab2,tab3,tab4,tab5=st.tabs(["🔺 ELU — Flexion","🔧 Goujons","📐 Section & ANP","📏 ELS — Déflexions","📚 Formules"])

# ── Tab 1 ─────────────────────────────────────────────────────────────────────
with tab1:
    cL,cR=st.columns([1.2,1])
    with cL:
        st.plotly_chart(fig_moment(elu_r['Mrc'],Mr_s,Mf), use_container_width=True, key='ch_moment')
        st.plotly_chart(fig_xsec(sec,tc_val,hd_val,be_val,elu_r,uid='tab1'), use_container_width=True, key='ch_xsec_t1')
    with cR:
        st.markdown('<div class="section-hdr">🧮 Étapes de calcul ELU (§17.9.3)</div>',unsafe_allow_html=True)
        case_names={'a':'ANP dans la dalle','b':"ANP dans l'aile",'c':"ANP dans l'âme"}
        ok_c=GN if mrc_ok else RD
        st.markdown(f'<div class="result-card"><b>Cas {elu_r["case"].upper()}</b> — {case_names[elu_r["case"]]}&nbsp;&nbsp;<span style="background:{ok_c};color:white;padding:2px 8px;border-radius:10px;font-size:0.82em">{"✅ M_rc ≥ M_f" if mrc_ok else "❌ M_rc < M_f"}</span></div>',unsafe_allow_html=True)
        for lbl,val,unit in elu_r['steps']:
            if '→ Cas' in lbl:
                st.markdown(f'<div style="background:#dbeafe;border-radius:6px;padding:6px 10px;margin:6px 0;font-weight:700;color:#1d4ed8">{lbl} — {val}</div>',unsafe_allow_html=True)
            else:
                a,b=st.columns([2,1])
                a.markdown(f'<div class="step-row">{lbl}</div>',unsafe_allow_html=True)
                b.markdown(f'<div class="step-row" style="text-align:right"><b>{val}</b> {unit}</div>',unsafe_allow_html=True)
        st.markdown('<div class="section-hdr">📋 Synthèse</div>',unsafe_allow_html=True)
        for lbl,v,u in [("α₁",elu_r['a1'],""),("C'r,max",elu_r['Cr_max'],"kN"),
                         ("Tr,max",elu_r['Tr_max'],"kN"),("Qr",elu_r['Vh'],"kN"),
                         ("ae",elu_r['ae'],"mm"),("e'",elu_r['e_prime'],"mm"),
                         ("M_rc",elu_r['Mrc'],"kN·m"),("Mf",Mf,"kN·m"),("Util.",Mf/elu_r['Mrc']*100,"%")]:
            a,b,c=st.columns([2,1,1]); a.write(lbl); b.write(f"**{v:.4g}**"); c.write(u)

# ── Tab 2 ─────────────────────────────────────────────────────────────────────
with tab2:
    cL,cR=st.columns([1.5,1])
    with cL:
        st.plotly_chart(fig_studs(L_val,n_half,qr_N,elu_r['Vh']), use_container_width=True, key='ch_studs')
    with cR:
        st.markdown('<div class="section-hdr">🔧 Résistance des goujons</div>',unsafe_allow_html=True)
        deck_ref={"Dalle pleine (sans nervures)":"§17.7.2.2","Nervures ⊥ à la poutre":"§17.7.2.4","Nervures ∥ à la poutre":"§17.7.2.3"}
        st.markdown(f'<div class="result-card"><b>Type:</b> {deck_type}<br><b>Réf.:</b> {deck_ref[deck_type]}<br><b>d_goujon:</b> {dg_val} mm · Fu={Fu_val} MPa</div>',unsafe_allow_html=True)
        for lbl,v,u in [("Ec",Ec_v,"MPa"),("n=Es/Ec",200000/Ec_v,""),
                         ("q_rs (dalle pl.)",qrs_base/1e3,"kN"),("q_r utilisé",qr_N/1e3,"kN"),
                         ("V_h = Q_r",elu_r['Vh'],"kN"),("n par demi-portée",n_half,""),
                         ("n total",n_tot,""),("Q_r fourni",n_tot*qr_N/1e3,"kN"),
                         ("Util.",elu_r['Vh']/(n_tot*qr_N/1e3)*100 if n_tot>0 else 0,"%")]:
            a,b,c=st.columns([2,1,1]); a.write(lbl); b.write(f"**{v:.4g}**"); c.write(u)
        ok_conn=(n_tot*qr_N/1e3>=elu_r['Vh'])
        st.markdown(f'<div style="background:{"#dcfce7" if ok_conn else "#fee2e2"};border-radius:8px;padding:10px;margin-top:8px"><b>{"✅ Goujons suffisants" if ok_conn else "❌ Goujons insuffisants"}</b><br>Q_r={n_tot*qr_N/1e3:.1f} kN {"≥" if ok_conn else "<"} V_h={elu_r["Vh"]:.1f} kN</div>',unsafe_allow_html=True)

# ── Tab 3 ─────────────────────────────────────────────────────────────────────
with tab3:
    cL,cR=st.columns(2)
    with cL:
        st.plotly_chart(fig_xsec(sec,tc_val,hd_val,be_val,elu_r,uid='tab3'), use_container_width=True, key='ch_xsec_t3')
    with cR:
        st.plotly_chart(fig_ane(sec,tc_val,hd_val,be_val,els_r), use_container_width=True, key='ch_ane')
    st.plotly_chart(fig_inertia(els_r,p), use_container_width=True, key='ch_inertia')
    st.markdown('<div class="section-hdr">📊 Paramètres ELS</div>',unsafe_allow_html=True)
    cols=st.columns(4)
    for i,(lbl,v,u) in enumerate([("n",els_r['n'],""),("Ec",els_r['Ec'],"MPa"),
                                    ("ȳ instant.",els_r['ybar'],"mm"),("It",els_r['It']/1e6,"×10⁶mm⁴"),
                                    ("Ie",els_r['Ie']/1e6,"×10⁶mm⁴"),("nₛ fluage",els_r['ns'],""),
                                    ("E'c",els_r['Ecp'],"MPa"),("ȳ fluage",els_r['ybar_c'],"mm")]):
        with cols[i%4]: st.metric(f"{lbl} [{u}]" if u else lbl, f"{v:.4g}")

# ── Tab 4 ─────────────────────────────────────────────────────────────────────
with tab4:
    st.plotly_chart(fig_deflection(dL,dD,dCreep,dSh,L_val), use_container_width=True, key='ch_defl')
    st.markdown('<div class="section-hdr">📋 Synthèse déflexions</div>',unsafe_allow_html=True)
    limit=L_val*1000/360
    for lbl,v,s in [("Ie effective",f"{els_r['Ie']/1e6:.0f} ×10⁶ mm⁴",""),
                     ("Δ_L (vive)",f"{dL:.2f} mm","✅" if dL<=limit else "⚠️"),
                     ("Δ_D (morte)",f"{dD:.2f} mm",""),
                     ("Δ_fluage (+15%DL)",f"{dCreep:.2f} mm",""),
                     ("Δ_L + fluage",f"{dL+dCreep:.2f} mm","✅ OK" if dL+dCreep<=limit else "❌ Dépasse"),
                     ("Limite L/360",f"{limit:.1f} mm","")]:
        a,b,c=st.columns([3,2,2]); a.write(lbl); b.write(f"**{v}**"); c.write(s)
    st.markdown('<div class="formula-box">Δ = 5·w·L⁴/(384·E·Ie)  &nbsp;·&nbsp;  Ie=Is+0.85·p^0.25·(It−Is)  &nbsp;·&nbsp;  Δ_fluage≈+15%·Δ_D  &nbsp;·&nbsp;  Limite: L/360</div>',unsafe_allow_html=True)

# ── Tab 5 ─────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown("## 📚 Référentiel des formules — CSA S16:24 / GCI-2011")
    with st.expander("🔷 ELU §17.9.3",expanded=True):
        st.markdown("""<div class="formula-box">
        α₁ = 0.85 − 0.0015·f'c ≥ 0.67<br>
        T_r,max = φ·As·Fy &nbsp;·&nbsp; C'_r,max = α₁·φc·be·tc·f'c<br>
        Q_r = p·min(T_r,C'_r) &nbsp;·&nbsp; C_rs = (T_r−Q_r)/2<br>
        ae = Q_r/(α₁·φc·be·f'c)<br><br>
        <b>Cas A</b> (ANP dalle): e'=d/2+hd+tc−ae/2 &nbsp;→&nbsp; M_rc=T_r·e'<br>
        <b>Cas B</b> (ANP aile): t_fc=C_rs/C_rf,max·tf &nbsp;→&nbsp; M_rc=C_rs·es+Q_r·e'<br>
        <b>Cas C</b> (ANP âme): hc=(C_rs−C_rf,max)/(φ·tw·Fy) &nbsp;→&nbsp; M_rc=C_rs·es+Q_r·e'
        </div>""",unsafe_allow_html=True)
    with st.expander("🔶 ELS §17.3.1"):
        st.markdown("""<div class="formula-box">
        Ec simplifié: 4500·√f'c &nbsp;·&nbsp; Ec complet: (3300√f'c+6900)·(ρ/2300)^1.5 &nbsp;·&nbsp; Ec pont: donné<br>
        ȳ = n·(As/be)·[√(1+2·be·ys/(n·As))−1]  (si ȳ≤tc)<br>
        It = be·ȳ³/(3n) + Is + As·(ys−ȳ)²<br>
        Ie = Is + 0.85·p^0.25·(It−Is)<br>
        E'c = Ec/(1+χ·φ)  χ=0.73 · φ=fluage → nₛ=Es/E'c → Its, Ies
        </div>""",unsafe_allow_html=True)
    with st.expander("🔴 Goujons §17.7.2"):
        st.markdown("""<div class="formula-box">
        Dalle pleine: q_rs = 0.5·φsc·Asc·√(f'c·Ec) ≤ φsc·Asc·Fu<br>
        Nervures ⊥: q_rr = 0.35·φsc·ρc·Ap·√f'c &nbsp;·&nbsp; Ap=2√2·h²+(√2/2)·h·wd<br>
        Nervures ∥: q_rr = q_rs·[0.75+0.167·(wd/hd−1.5)] pour wd/hd≥1.5<br>
        n_total = 2·ceil(V_h/q_rr)
        </div>""",unsafe_allow_html=True)
    with st.expander("🌉 Pont vs Plancher"):
        st.markdown("""<div class="formula-box">
        <b>Pont (Ex 7.4):</b> Ec donné directement (ex: 30000 MPa, pas de formule)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;be = min(L/4, s/2) — demi-espacement entre poutres<br>
        &nbsp;&nbsp;&nbsp;&nbsp;Dalle pleine (hd=0) · Charges: uniforme + concentrée au centre<br><br>
        <b>Plancher (Ex 7.1–7.3, 7.5):</b> Ec calculé par formule (γc ou simplifié)<br>
        &nbsp;&nbsp;&nbsp;&nbsp;be = min(L/4, espacement) — plein espacement<br>
        &nbsp;&nbsp;&nbsp;&nbsp;Coffrage métallique possible (hd>0, nervures ⊥ ou ∥)
        </div>""",unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(f'<div style="text-align:center;color:#94a3b8;font-size:0.80em;padding:8px">GCI-2011 Conception des structures I · Université Laval · Prof. Luca Sorelli · CSA S16:24 Ch.17<br>Outil pédagogique — aucune responsabilité · Validé Ex.7.1–7.5 · Python {sys.version[:6]}</div>',unsafe_allow_html=True)
