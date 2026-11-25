# composite_app.py  — GCI-2011 Poutre Composite Interactive
# Université Laval · Luca Sorelli · CSA S16:24 / A23.3
# pip install streamlit plotly numpy

import math, sys, json
import streamlit as st
import plotly.graph_objects as go
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
#  ENGINEERING LIBRARY
# ══════════════════════════════════════════════════════════════════════════════
PHI=0.90; PHI_C=0.65; PHI_SC=0.80; E_S=200_000

T1={
    "W310x39":dict(dl=0.380,As=4940,d=310,bf=165,tf=9.7,tw=5.8,Ix=85.1,Zx=634),
    "W360x45":dict(dl=0.442,As=5730,d=352,bf=171,tf=9.8,tw=6.9,Ix=122,Zx=779),
    "W360x51":dict(dl=0.496,As=6450,d=355,bf=171,tf=11.6,tw=7.2,Ix=141,Zx=894),
    "W360x57":dict(dl=0.556,As=7220,d=358,bf=172,tf=13.1,tw=7.9,Ix=161,Zx=1010),
    "W360x64":dict(dl=0.627,As=8140,d=347,bf=203,tf=13.5,tw=7.7,Ix=178,Zx=1140),
    "W360x91":dict(dl=0.891,As=11600,d=353,bf=254,tf=16.4,tw=9.5,Ix=267,Zx=1660),
    "W360x101":dict(dl=0.993,As=12900,d=357,bf=255,tf=18.3,tw=10.5,Ix=301,Zx=1880),
    "W360x110":dict(dl=1.08,As=14000,d=360,bf=256,tf=19.9,tw=11.4,Ix=331,Zx=2080),
    "W360x122":dict(dl=1.19,As=15500,d=363,bf=257,tf=21.7,tw=13.0,Ix=365,Zx=2270),
    "W410x39":dict(dl=0.385,As=4990,d=399,bf=140,tf=8.8,tw=6.4,Ix=127,Zx=730),
    "W410x46":dict(dl=0.454,As=5890,d=403,bf=140,tf=11.2,tw=7.0,Ix=156,Zx=885),
    "W410x54":dict(dl=0.524,As=6810,d=403,bf=177,tf=10.9,tw=7.5,Ix=186,Zx=1050),
    "W410x60":dict(dl=0.584,As=7560,d=407,bf=178,tf=12.8,tw=7.7,Ix=216,Zx=1190),
    "W410x67":dict(dl=0.662,As=8600,d=410,bf=179,tf=14.4,tw=8.8,Ix=246,Zx=1360),
    "W410x74":dict(dl=0.735,As=9550,d=413,bf=180,tf=16.0,tw=9.7,Ix=275,Zx=1510),
    "W410x85":dict(dl=0.834,As=10800,d=417,bf=181,tf=18.2,tw=10.9,Ix=315,Zx=1730),
    "W410x100":dict(dl=0.992,As=12900,d=415,bf=260,tf=16.9,tw=10.0,Ix=404,Zx=2160),
    "W410x114":dict(dl=1.14,As=14800,d=420,bf=261,tf=19.3,tw=11.6,Ix=468,Zx=2490),
    "W410x132":dict(dl=1.31,As=17000,d=425,bf=263,tf=22.2,tw=13.3,Ix=545,Zx=2890),
    "W410x149":dict(dl=1.48,As=19200,d=431,bf=265,tf=25.0,tw=14.9,Ix=625,Zx=3280),
    "W460x52":dict(dl=0.510,As=6650,d=450,bf=152,tf=10.8,tw=8.0,Ix=212,Zx=1090),
    "W460x61":dict(dl=0.588,As=7640,d=450,bf=189,tf=10.8,tw=8.1,Ix=254,Zx=1290),
    "W460x74":dict(dl=0.728,As=9450,d=457,bf=190,tf=14.5,tw=9.0,Ix=333,Zx=1650),
    "W460x82":dict(dl=0.804,As=10400,d=460,bf=191,tf=16.0,tw=9.9,Ix=370,Zx=1830),
    "W460x89":dict(dl=0.876,As=11400,d=463,bf=192,tf=17.7,tw=10.5,Ix=410,Zx=2010),
    "W460x97":dict(dl=0.947,As=12300,d=466,bf=193,tf=19.0,tw=11.4,Ix=445,Zx=2180),
    "W460x106":dict(dl=1.04,As=13500,d=469,bf=194,tf=20.6,tw=12.6,Ix=488,Zx=2390),
    "W530x72":dict(dl=0.702,As=9120,d=524,bf=207,tf=10.9,tw=8.9,Ix=400,Zx=1750),
    "W530x82":dict(dl=0.806,As=10500,d=528,bf=209,tf=13.3,tw=9.5,Ix=477,Zx=2060),
    "W530x92":dict(dl=0.907,As=11800,d=533,bf=209,tf=15.6,tw=10.2,Ix=552,Zx=2360),
    "W530x101":dict(dl=0.995,As=12900,d=537,bf=210,tf=17.4,tw=10.9,Ix=617,Zx=2620),
    "W530x109":dict(dl=1.07,As=13900,d=539,bf=211,tf=18.8,tw=11.6,Ix=667,Zx=2830),
    "W530x123":dict(dl=1.21,As=15700,d=544,bf=212,tf=21.2,tw=13.1,Ix=761,Zx=3210),
    "W530x138":dict(dl=1.36,As=17600,d=549,bf=214,tf=23.6,tw=14.7,Ix=861,Zx=3610),
    "WWF1200x380":dict(dl=3.80,As=48400,d=1200,bf=500,tf=30.0,tw=16.0,Ix=12300,Zx=20500),
}

PRESETS={
    "— Aucun —":None,
    "Ex 7.1a — W410x54 · f'c=20 · p=50% · ⊥":dict(sec="W410x54",fc=20,Fy=350,be=2500,tc=65,hd=75,p=50,L=9.0,gc=22.6,ec_f="Simplifiée (4500√f'c)",Ec_given=None,deck="Nervures ⊥ à la poutre",dg=19,hsc=115,wd=180,Fu=415,wD=5.0,wL=8.0,aD=1.25,aL=1.50),
    "Ex 7.1c — W410x54 · f'c=35 · p=50% · ⊥":dict(sec="W410x54",fc=35,Fy=350,be=2500,tc=65,hd=75,p=50,L=9.0,gc=22.6,ec_f="Simplifiée (4500√f'c)",Ec_given=None,deck="Nervures ⊥ à la poutre",dg=19,hsc=115,wd=180,Fu=415,wD=5.0,wL=8.0,aD=1.25,aL=1.50),
    "Ex 7.2 — W310x39 · f'c=20 · p=40% · dalle":dict(sec="W310x39",fc=20,Fy=350,be=2100,tc=130,hd=0,p=40,L=9.0,gc=25.0,ec_f="Complète (3300√f'c+6900)·(ρ/2300)^1.5",Ec_given=None,deck="Dalle pleine (sans nervures)",dg=19,hsc=115,wd=150,Fu=415,wD=9.975,wL=6.3,aD=1.25,aL=1.50),
    "Ex 7.3 — W410x46 · f'c=25 · p=50% · léger":dict(sec="W410x46",fc=25,Fy=350,be=3000,tc=85,hd=75,p=50,L=12.0,gc=18.15,ec_f="Complète (3300√f'c+6900)·(ρ/2300)^1.5",Ec_given=None,deck="Nervures ⊥ à la poutre",dg=19,hsc=120,wd=180,Fu=415,wD=12.6,wL=7.2,aD=1.25,aL=1.50),
    "Ex 7.4 — WWF1200x380 · PONT · Ec=30000":dict(sec="WWF1200x380",fc=35,Fy=350,be=1850,tc=200,hd=0,p=100,L=36.0,gc=24.0,ec_f="Donnée directement (pont)",Ec_given=30000,deck="Dalle pleine (sans nervures)",dg=20,hsc=150,wd=0,Fu=450,wD=28.9,wL=11.0,aD=1.25,aL=1.50),
    "Ex 7.5 — W460x52 · f'c=25 · p=100% · ⊥":dict(sec="W460x52",fc=25,Fy=350,be=3050,tc=65,hd=75,p=100,L=12.2,gc=23.26,ec_f="Simplifiée (4500√f'c)",Ec_given=None,deck="Nervures ⊥ à la poutre",dg=19,hsc=115,wd=180,Fu=450,wD=14.0,wL=6.71,aD=1.25,aL=1.50),
}

def compute_Ec(fc,rho,formula,Ec_given=None):
    if formula=="Donnée directement (pont)" and Ec_given: return float(Ec_given)
    if "Complète" in formula: return (3300*math.sqrt(fc)+6900)*(rho/2300)**1.5
    return 4500*math.sqrt(fc)
def compute_Ap(h,wd): return 2*math.sqrt(2)*h**2+(math.sqrt(2)/2)*h*wd
def alpha1(fc): return max(0.85-0.0015*fc,0.67)

def elu_calc(sec,fc,Fy,be,tc,hd,p,Ec_v):
    a1=alpha1(fc); As=sec['As']; d=sec['d']; bf=sec['bf']; tf=sec['tf']; tw=sec['tw']
    Tr=PHI*As*Fy; Cr=a1*PHI_C*be*tc*fc
    Qr=p*min(Tr,Cr); Crs=(Tr-Qr)/2; Crfmax=PHI*bf*tf*Fy
    ae=Qr/(a1*PHI_C*be*fc)
    steps=[("α₁",f"{a1:.4f}",""),("T_r,max",f"{Tr/1e3:.2f}","kN"),("C'_r,max",f"{Cr/1e3:.2f}","kN"),
           ("Q_r",f"{Qr/1e3:.3f}","kN"),("C_rs",f"{Crs/1e3:.3f}","kN"),
           ("C_rf,max",f"{Crfmax/1e3:.3f}","kN"),("ae",f"{ae:.2f}","mm")]
    if p==1.0 and Cr>Tr:
        ep=d/2+hd+tc-ae/2; Mrc=Tr*ep; dt=d/2; dc=0.0
        steps+=[("→ Cas A","ANP dans la dalle",""),("e'",f"{ep:.2f}","mm"),("M_rc",f"{Mrc/1e6:.3f}","kN·m")]
        return dict(case='a',Mrc=Mrc/1e6,Vh=Tr/1e3,ae=ae,Cr_prime=Qr/1e3,Cr_steel=0,Tr_max=Tr/1e3,Cr_max=Cr/1e3,a1=a1,e=0,e_prime=ep,dt=dt,dc=dc,steps=steps)
    if Crs<=Crfmax:
        tfc=Crs/Crfmax*tf; dt=(0.5*As*d-0.5*bf*tfc**2)/(As-bf*tfc)
        es=dt-tfc/2; ep=dt+hd+tc-ae/2; Mrc=Crs*es+Qr*ep; dc=0.0
        steps+=[("→ Cas B","ANP dans l'aile",""),("tfc",f"{tfc:.3f}","mm"),("dt",f"{dt:.3f}","mm"),("es",f"{es:.3f}","mm"),("e'",f"{ep:.3f}","mm"),("M_rc",f"{Mrc/1e6:.3f}","kN·m")]
        return dict(case='b',Mrc=Mrc/1e6,Vh=Qr/1e3,ae=ae,Cr_prime=Qr/1e3,Cr_steel=Crs/1e3,Tr_max=Tr/1e3,Cr_max=Cr/1e3,a1=a1,e=es,e_prime=ep,dt=dt,dc=dc,steps=steps)
    else:
        Crw=Crs-Crfmax; hc=Crw/(PHI*tw*Fy); Asf=bf*tf; Asc2=Asf+hc*tw
        dc=(0.5*Asf*tf+hc*tw*(tf+0.5*hc))/Asc2; dt=(As*0.5*d-Asc2*(d-dc))/(As-Asc2)
        es=d-dc-dt; ep=d+hd+tc-dt-ae/2; Mrc=Crs*es+Qr*ep
        steps+=[("→ Cas C","ANP dans l'âme",""),("hc",f"{hc:.3f}","mm"),("dc",f"{dc:.3f}","mm"),("dt",f"{dt:.3f}","mm"),("es",f"{es:.3f}","mm"),("e'",f"{ep:.3f}","mm"),("M_rc",f"{Mrc/1e6:.3f}","kN·m")]
        return dict(case='c',Mrc=Mrc/1e6,Vh=Qr/1e3,ae=ae,Cr_prime=Qr/1e3,Cr_steel=Crs/1e3,Tr_max=Tr/1e3,Cr_max=Cr/1e3,a1=a1,e=es,e_prime=ep,dt=dt,dc=dc,steps=steps)

def els_calc(sec,fc,be,tc,hd,p,Ec_v,phi_cr=2.7,chi=0.73):
    As=sec['As']; d=sec['d']; Is=sec['Ix']*1e6; n=E_S/Ec_v; ys=d/2+hd+tc
    yb=n*(As/be)*(math.sqrt(1+2*be*ys/(n*As))-1)
    if yb<=tc: It=be*yb**3/(3*n)+Is+As*(ys-yb)**2; ye=yb
    else:
        Ac=be*tc/n; ye=(Ac*tc/2+As*ys)/(Ac+As)
        It=be*tc**3/(12*n)+Ac*(ye-tc/2)**2+Is+As*(ys-ye)**2
    Ie=Is+0.85*(p**0.25)*(It-Is)
    Ecp=Ec_v/(1+chi*phi_cr); ns=E_S/Ecp
    ybs=ns*(As/be)*(math.sqrt(1+2*be*ys/(ns*As))-1)
    if ybs<=tc: Its=be*ybs**3/(3*ns)+Is+As*(ys-ybs)**2; ys2=ybs
    else:
        Ac2=be*tc/ns; ys2=(Ac2*tc/2+As*ys)/(Ac2+As)
        Its=be*tc**3/(12*ns)+Ac2*(ys2-tc/2)**2+Is+As*(ys-ys2)**2
    Ies=Is+0.85*(p**0.25)*(Its-Is)
    # ── Shrinkage deflection (Annex H — HSC §17.3.1) ──────────────────────
    # Δ_s = (L²/8) · c · ε_f · Ac · y / (ns · Ies)
    # ε_f = 583×10⁻⁶ (Annex H.4), c = 0.5 (Fig H.2, simply supported)
    # y   = ȳ_s (from top of slab with ns) − 0.5·tc  = eccentricity ANE→slab centroid
    # Ac  = be · tc   (slab area, full width)
    return dict(Is=Is,It=It,Ie=Ie,Its=Its,Ies=Ies,n=n,Ec=Ec_v,ns=ns,Ecp=Ecp,
                ybar=ye,ybar_c=ys2,phi_cr=phi_cr,
                _shrink_params=dict(Ies=Ies,ns=ns,ybar_c_top=ys2,tc=tc,be=be))

# ══════════════════════════════════════════════════════════════════════════════
#  DARK THEME PALETTE
# ══════════════════════════════════════════════════════════════════════════════
# Background: #0f172a (deep navy) | Card: #1e293b | Border: #334155
# Accent blue: #3b82f6 | Cyan: #06b6d4 | Amber: #f59e0b
# Green: #10b981 | Red: #ef4444 | Purple: #a855f7 | Muted: #94a3b8

BG_PLOT   = "#0f172a"
CARD_BG   = "#1e293b"
BORDER    = "#334155"
BLUE      = "#3b82f6"
BLUE_LT   = "#60a5fa"
CYAN      = "#06b6d4"
AMBER     = "#f59e0b"
GREEN     = "#10b981"
RED       = "#ef4444"
PURPLE    = "#a855f7"
MUTED     = "#94a3b8"
TEXT      = "#f1f5f9"
TEXT_DIM  = "#64748b"

def _base_layout(title, h=400):
    return dict(
        title=dict(text=title, font=dict(size=13, color=TEXT, family="Inter, sans-serif"), x=0.01),
        height=h,
        plot_bgcolor=CARD_BG,
        paper_bgcolor=CARD_BG,
        font=dict(color=TEXT, family="Inter, sans-serif", size=11),
        showlegend=False,
        margin=dict(l=16, r=16, t=56, b=16),
        xaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER, tickfont=dict(color=MUTED)),
        yaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER, tickfont=dict(color=MUTED)),
    )

def fig_moment(Mrc, Mr_steel, Mf):
    gain=(Mrc/Mr_steel-1)*100; util=Mf/Mrc*100
    vals=[Mr_steel, Mrc, Mf]
    colors=[BLUE_LT, BLUE, GREEN if Mf<=Mrc else RED]
    text=[f"<b>{v:.1f}</b>" for v in vals]
    fig=go.Figure()
    fig.add_trace(go.Bar(
        x=["Mr acier seul", "M_rc composite", "M_f factorée"],
        y=vals, marker_color=colors,
        marker_line=dict(width=0),
        text=text, textposition='outside',
        textfont=dict(color=TEXT, size=12, family="Inter"),
        hovertemplate="<b>%{x}</b><br>%{y:.1f} kN·m<extra></extra>",
    ))
    # Annotation: gain composite
    fig.add_annotation(x=1, y=Mrc*1.08,
        text=f"<b>+{gain:.0f}% vs acier seul</b>",
        showarrow=False, font=dict(color=CYAN, size=11))
    fig.add_annotation(x=2, y=Mf*1.08,
        text=f"<b>Util. {util:.0f}%</b>",
        showarrow=False, font=dict(color=GREEN if util<=100 else RED, size=11))
    lo=_base_layout(f"<b>Résistance en flexion ELU</b>  <span style='color:{MUTED}'>Gain composite: +{gain:.0f}%  ·  Utilisation: {util:.0f}%</span>", 380)
    lo['yaxis']['title']="Moment [kN·m]"
    lo['yaxis']['tickfont']['color']=MUTED
    fig.update_layout(**lo)
    return fig

def fig_xsec(sec, tc, hd, be, elu, uid="xsec"):
    d=sec['d']; bf=sec['bf']; be_d=min(be,bf*4.5); tot=d+hd+tc
    fig=go.Figure()
    # Slab (concrete)
    fig.add_shape(type="rect", x0=-be_d/2, x1=be_d/2, y0=d+hd, y1=d+hd+tc,
                  fillcolor="#1e3a5f", line=dict(color=CYAN, width=1.5))
    # Slab label
    fig.add_annotation(x=0, y=d+hd+tc/2, text=f"<b>Dalle béton</b><br>tc={tc}mm",
                       showarrow=False, font=dict(color=CYAN, size=9))
    # Deck fill
    if hd>0:
        fig.add_shape(type="rect", x0=-be_d/2, x1=be_d/2, y0=d, y1=d+hd,
                      fillcolor="#162032", line=dict(color=BORDER, width=1, dash='dot'))
        fig.add_annotation(x=0, y=d+hd/2, text=f"hd={hd}mm",
                           showarrow=False, font=dict(color=MUTED, size=8))
    # I-beam — gradient effect using two rectangles
    for y0,y1 in [(0, sec['tf']), (d-sec['tf'], d)]:
        fig.add_shape(type="rect", x0=-bf/2, x1=bf/2, y0=y0, y1=y1,
                      fillcolor=BLUE, line=dict(color=BLUE_LT, width=1))
    fig.add_shape(type="rect", x0=-sec['tw']/2, x1=sec['tw']/2,
                  y0=sec['tf'], y1=d-sec['tf'],
                  fillcolor="#2563eb", line=dict(color=BLUE_LT, width=0.5))
    # ANP line
    ae=elu['ae']; case=elu['case']
    if case=='a': y_anp=d+hd+tc-ae
    elif case=='b':
        tfc=min(elu.get('Cr_steel',0)*1e3/(PHI*bf*350),sec['tf'])
        y_anp=d-tfc
    else:
        Crf=PHI*bf*sec['tf']*350/1e3
        hc=max((elu.get('Cr_steel',0)-Crf)*1e3/(PHI*sec['tw']*350),0)
        y_anp=d-sec['tf']-hc
    # Compression zone highlight
    fig.add_shape(type="rect", x0=-be_d/2, x1=be_d/2,
                  y0=d+hd+tc-ae, y1=d+hd+tc,
                  fillcolor="rgba(245,158,11,0.25)", line=dict(color=AMBER, width=2))
    # ANP dashed line
    fig.add_shape(type="line", x0=-be_d/2*1.1, x1=be_d/2*1.1,
                  y0=y_anp, y1=y_anp,
                  line=dict(color=RED, width=2.5, dash="dash"))
    fig.add_annotation(x=be_d/2*1.15, y=y_anp,
                       text=f"<b>ANP — Cas {case.upper()}</b>",
                       showarrow=False, font=dict(color=RED, size=11, family="Inter"),
                       xanchor="left")
    # ae bracket + label
    fig.add_shape(type="line", x0=-be_d/2*1.3, x1=-be_d/2*1.3,
                  y0=d+hd+tc-ae, y1=d+hd+tc,
                  line=dict(color=AMBER, width=1.5))
    for y_tick in [d+hd+tc-ae, d+hd+tc]:
        fig.add_shape(type="line", x0=-be_d/2*1.35, x1=-be_d/2*1.25,
                      y0=y_tick, y1=y_tick, line=dict(color=AMBER, width=1.5))
    fig.add_annotation(x=-be_d/2*1.5, y=d+hd+tc-ae/2,
                       text=f"<b>ae={ae:.1f}mm</b>",
                       showarrow=False, font=dict(color=AMBER, size=10))
    # Dimension lines
    for y_mm, lbl in [(0,"0"), (d,f"d={d}"), (d+hd+tc,f"+{tc}mm")]:
        fig.add_annotation(x=-be_d/2*1.65, y=y_mm, text=lbl,
                           showarrow=False, font=dict(color=TEXT_DIM, size=8), xanchor="right")
    lo=_base_layout(f"<b>Section composite — {sec.get('name','')} — Cas {case.upper()}</b>", 500)
    lo['xaxis']['visible']=False; lo['yaxis']['visible']=False
    lo['xaxis']['range']=[-be_d*0.9, be_d*0.9]
    lo['yaxis']['range']=[-tot*0.1, tot*1.18]
    lo['uirevision']=uid
    fig.update_layout(**lo)
    return fig

def fig_ane(sec, tc, hd, be, els_r):
    d=sec['d']; bf=sec['bf']; be_d=min(be,bf*4); tot=d+hd+tc
    fig=go.Figure()
    fig.add_shape(type="rect",x0=-be_d/2,x1=be_d/2,y0=d+hd,y1=d+hd+tc,
                  fillcolor="#1e3a5f",line=dict(color=CYAN,width=1.5))
    if hd>0:
        fig.add_shape(type="rect",x0=-be_d/2,x1=be_d/2,y0=d,y1=d+hd,
                      fillcolor="#162032",line=dict(color=BORDER,width=1,dash='dot'))
    for y0,y1 in [(0,sec['tf']),(d-sec['tf'],d)]:
        fig.add_shape(type="rect",x0=-bf/2,x1=bf/2,y0=y0,y1=y1,fillcolor=BLUE,line=dict(color=BLUE_LT,width=1))
    fig.add_shape(type="rect",x0=-sec['tw']/2,x1=sec['tw']/2,y0=sec['tf'],y1=d-sec['tf'],fillcolor="#2563eb",line=dict(color=BLUE_LT,width=0.5))
    for ybar_top,color,dash_,lbl in [
        (els_r['ybar'], AMBER, "solid", f"ANE instantané  ȳ={els_r['ybar']:.1f}mm  (n={els_r['n']:.2f})"),
        (els_r['ybar_c'], PURPLE, "dash", f"ANE fluage  ȳ={els_r['ybar_c']:.1f}mm  (nₛ={els_r['ns']:.2f})"),
    ]:
        y_pl=tot-ybar_top
        fig.add_shape(type="line",x0=-be_d/2*1.1,x1=be_d/2*1.1,y0=y_pl,y1=y_pl,
                      line=dict(color=color,width=2.5,dash=dash_))
        fig.add_annotation(x=be_d/2*1.15,y=y_pl,text=f"<b>{lbl}</b>",
                           showarrow=False,font=dict(color=color,size=9),xanchor="left")
    lo=_base_layout(f"<b>ANE — Axe Neutre Élastique</b><br><span style='color:{MUTED};font-size:11px'>Ec={els_r['Ec']:.0f} MPa  ·  E'c={els_r['Ecp']:.0f} MPa (fluage)</span>",480)
    lo['xaxis']['visible']=False; lo['yaxis']['visible']=False
    lo['xaxis']['range']=[-be_d*0.9,be_d*0.9]; lo['yaxis']['range']=[-tot*0.08,tot*1.12]
    fig.update_layout(**lo)
    return fig

def fig_inertia(els_r, p):
    Is=els_r['Is']/1e6; It=els_r['It']/1e6; Ie=els_r['Ie']/1e6
    Its=els_r['Its']/1e6; Ies=els_r['Ies']/1e6
    labels=["Is<br>(acier)","It<br>(transform.)","Ie<br>(effective)","Its<br>(fluage)","Ies<br>(eff.fluage)"]
    vals=[Is,It,Ie,Its,Ies]
    colors=[BLUE_LT,BLUE,AMBER,PURPLE,"#64748b"]
    text=[f"<b>{v:.0f}</b>" if i==0 else f"<b>{v:.0f}</b><br><span style='color:{MUTED}'>+{(v/Is-1)*100:.0f}%</span>" for i,v in enumerate(vals)]
    fig=go.Figure(go.Bar(x=labels,y=vals,marker_color=colors,marker_line=dict(width=0),
        text=text,textposition='outside',hovertemplate="<b>%{x}</b><br>%{y:.0f} ×10⁶ mm⁴<extra></extra>"))
    lo=_base_layout(f"<b>Moments d'inertie  [×10⁶ mm⁴]</b><br><span style='color:{MUTED}'>p={p*100:.0f}%  ·  Ie = Is + 0.85·p^0.25·(It−Is)</span>",380)
    lo['yaxis']['title']="I [×10⁶ mm⁴]"
    fig.update_layout(**lo)
    return fig

def fig_studs(L, n_half, qr_N, Vh):
    n_tot=2*n_half; MAX=20; show=min(n_half,MAX)
    sp=(L/2)/(show+1) if show>0 else L/2
    lw=max(0.8,min(2.2,18/max(show,1)))
    fig=go.Figure()
    # Beam body (gradient look)
    fig.add_shape(type="rect",x0=0,x1=L,y0=0,y1=0.35,fillcolor=BLUE,line=dict(color=BLUE_LT,width=1.5))
    # Slab
    fig.add_shape(type="rect",x0=0,x1=L,y0=0.35,y1=0.78,fillcolor="#1e3a5f",line=dict(color=CYAN,width=1.2))
    # Studs
    for half in range(2):
        x0=half*L/2
        for i in range(1,show+1):
            x=x0+i*sp
            fig.add_shape(type="line",x0=x,x1=x,y0=0.26,y1=0.82,line=dict(color=AMBER,width=lw))
            fig.add_shape(type="circle",x0=x-0.018*L/12,x1=x+0.018*L/12,y0=0.80,y1=0.84,
                          fillcolor=AMBER,line=dict(color=AMBER))
        if n_half>MAX:
            fig.add_annotation(x=x0+L/4,y=0.90,text=f"<b>({n_half} goujons)</b>",
                               showarrow=False,font=dict(color=AMBER,size=10))
    # Mmax line
    fig.add_shape(type="line",x0=L/2,x1=L/2,y0=-0.08,y1=1.22,line=dict(color=RED,width=1.5,dash="dash"))
    fig.add_annotation(x=L/2,y=1.27,text="<b>M<sub>max</sub></b>",font=dict(color=RED,size=11),showarrow=False)
    # Half-span arrows
    for x0f,x1f in [(0,L/2),(L/2,L)]:
        mid=(x0f+x1f)/2
        for xa,xb in [(x0f,x1f),(x1f,x0f)]:
            fig.add_annotation(x=xa,y=1.10,ax=xb,ay=1.10,axref='x',ayref='y',
                               arrowhead=2,arrowcolor=MUTED,text="",showarrow=True,arrowwidth=1.5)
        fig.add_annotation(x=mid,y=1.17,text=f"<b>L/2={L/2:.1f}m · {n_half} goujons</b>",
                           showarrow=False,font=dict(color=TEXT,size=10))
    util=min(Vh/(n_tot*qr_N/1e3)*100,999) if n_tot>0 else 0
    lo=_base_layout(f"<b>Distribution des goujons</b>  <span style='color:{MUTED}'>n_total={n_tot} · q_r={qr_N/1e3:.2f} kN · V_h={Vh:.0f} kN · util={util:.0f}%</span>",320)
    lo['xaxis']['visible']=False; lo['yaxis']['visible']=False
    lo['xaxis']['range']=[-L*0.03,L*1.05]; lo['yaxis']['range']=[-0.15,1.4]
    fig.update_layout(**lo)
    return fig

def fig_deflection(dL, dD, dCreep, dSh, L):
    limit=L*1000/360; d_lc=dL+dCreep; d_tot=dL+dCreep+dSh
    cats=["Δ_L<br>vivante","Δ_D<br>morte","Δ_fluage<br>+15%DL","Δ_retrait","Δ_L<br>+fluage","Δ_total"]
    vals=[dL,dD,dCreep,dSh,d_lc,d_tot]
    colors=[BLUE,CYAN,AMBER,PURPLE,GREEN if d_lc<=limit else RED,GREEN if d_tot<=limit else RED]
    fig=go.Figure()
    fig.add_trace(go.Bar(x=cats,y=vals,marker_color=colors,marker_line=dict(width=0),
        text=[f"<b>{v:.1f}</b>" for v in vals],textposition='outside',
        hovertemplate="<b>%{x}</b><br>Δ=%{y:.2f} mm<extra></extra>"))
    # L/360 reference line
    fig.add_shape(type="line",x0=-0.5,x1=5.5,y0=limit,y1=limit,
                  line=dict(color=RED,width=2,dash="dot"))
    fig.add_annotation(x=5.5,y=limit,text=f" L/360={limit:.1f}mm",
                       showarrow=False,font=dict(color=RED,size=10),xanchor="left")
    lo=_base_layout(f"<b>Déflexions ELS</b>  <span style='color:{MUTED}'>Limite L/360 = {limit:.1f} mm  ·  L={L:.1f} m</span>",400)
    lo['yaxis']['title']="Δ [mm]"
    fig.update_layout(**lo)
    return fig

# ══════════════════════════════════════════════════════════════════════════════
#  DARK THEME CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Global background ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0f172a !important;
    color: #f1f5f9 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stMain"] { background-color: #0f172a !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #111827 100%) !important;
    border-right: 1px solid #1e293b !important;
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #f1f5f9 !important; }
[data-testid="stSidebarNav"] { display: none; }

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: #1e293b;
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
    border-bottom: none !important;
}
[data-testid="stTabs"] [role="tab"] {
    color: #94a3b8 !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    font-weight: 500 !important;
    border: none !important;
    background: transparent !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: #3b82f6 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 14px 18px !important;
    transition: border-color 0.2s;
}
[data-testid="stMetric"]:hover { border-color: #3b82f6; }
[data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 0.78em !important; letter-spacing: 0.05em; text-transform: uppercase; }
[data-testid="stMetricValue"] { color: #f1f5f9 !important; font-size: 1.9em !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"] { font-size: 0.82em !important; }

/* ── Selectbox / slider ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] input {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
}
[data-testid="stSlider"] [data-testid="stThumbValue"] { color: #3b82f6 !important; }
[data-testid="stFileUploader"] {
    background: #1e293b !important;
    border: 1px dashed #334155 !important;
    border-radius: 10px !important;
}

/* ── Buttons ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    font-weight: 600 !important;
    transition: opacity 0.2s !important;
}
[data-testid="stButton"] > button:hover { opacity: 0.85 !important; }
[data-testid="stButton"] > button:disabled {
    background: #334155 !important;
    color: #64748b !important;
}
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: white !important; border: none !important; border-radius: 8px !important;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary { color: #93c5fd !important; font-weight: 600 !important; }

/* ── Divider ── */
hr { border-color: #1e293b !important; }

/* ── Custom classes ── */
.glass-card {
    background: rgba(30,41,59,0.8);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 18px 20px;
    margin: 6px 0;
    backdrop-filter: blur(8px);
}
.kpi-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px; }
.section-hdr {
    font-size: 0.75em;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 6px;
    margin: 18px 0 10px;
}
.step-row {
    display: flex;
    justify-content: space-between;
    background: #0f172a;
    border-radius: 6px;
    padding: 6px 12px;
    margin: 2px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85em;
    border-left: 3px solid #1e293b;
}
.step-row.case-header {
    background: rgba(59,130,246,0.15);
    border-left: 3px solid #3b82f6;
    font-weight: 700;
    color: #60a5fa;
}
.step-val { color: #06b6d4; font-weight: 600; }
.formula-box {
    background: rgba(59,130,246,0.08);
    border-left: 3px solid #3b82f6;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 8px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85em;
    color: #cbd5e1;
    line-height: 1.8;
}
.badge-ok   { background: rgba(16,185,129,0.2); color: #10b981; border: 1px solid rgba(16,185,129,0.4); padding: 2px 10px; border-radius: 20px; font-size: 0.82em; font-weight: 700; }
.badge-fail { background: rgba(239,68,68,0.2);  color: #ef4444; border: 1px solid rgba(239,68,68,0.4);  padding: 2px 10px; border-radius: 20px; font-size: 0.82em; font-weight: 700; }
.badge-info { background: rgba(59,130,246,0.2); color: #60a5fa; border: 1px solid rgba(59,130,246,0.4); padding: 2px 10px; border-radius: 20px; font-size: 0.82em; font-weight: 700; }
.hero-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f2744 100%);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #3b82f6, #06b6d4, #a855f7);
}
.sidebar-section {
    font-size: 0.7em; font-weight: 700; color: #3b82f6;
    text-transform: uppercase; letter-spacing: 0.12em;
    margin: 20px 0 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid #1e293b;
}
.disclaimer-dark {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.3);
    border-radius: 14px;
    padding: 24px 28px;
    color: #fcd34d;
    line-height: 1.8;
    font-size: 0.95em;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  DISCLAIMER GATE
# ══════════════════════════════════════════════════════════════════════════════
if 'disclaimer_accepted' not in st.session_state:
    st.session_state.disclaimer_accepted = False

if not st.session_state.disclaimer_accepted:
    st.markdown("<style>section[data-testid='stSidebar']{display:none}</style>", unsafe_allow_html=True)
    st.markdown("""
    <div class="hero-banner" style="text-align:center; padding:40px;">
        <div style="font-size:3em; margin-bottom:8px">🏗️</div>
        <h1 style="color:#f1f5f9; margin:0 0 6px; font-size:2em; font-weight:800">Poutre Composite</h1>
        <p style="color:#94a3b8; font-size:1.1em; margin:0">GCI-2011 · Université Laval · CSA S16:24 Ch.17</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="disclaimer-dark">
    <div style="font-size:1.1em; font-weight:700; margin-bottom:12px">⚠️  Avertissement — Outil pédagogique GCI-2011</div>
    Développé à des fins <b>exclusivement pédagogiques</b> dans le cadre du cours
    <b>GCI-2011 Conception des structures I</b> de l'<b>Université Laval</b> (Prof. Luca Sorelli).<br><br>
    <ul style="margin:8px 0 0 20px; color:#fde68a">
      <li>Calculs basés sur <b>CSA S16:24 Ch.17</b>, CSA A23.3 et les notes de cours B1/B2</li>
      <li>Cet outil <b>ne remplace pas</b> le jugement d'un ingénieur professionnel</li>
      <li>Les résultats doivent être <b>vérifiés indépendamment</b> avant toute application réelle</li>
      <li>Ni l'auteur ni l'Université Laval n'assument de <b>responsabilité</b> pour l'utilisation</li>
      <li>Validé sur Ex. 7.1 (2026), Ex. 7.2, Ex. 7.3, Ex. 7.4 et Ex. 7.5</li>
    </ul>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    agreed = st.checkbox("✅  J'ai lu et j'accepte les conditions d'utilisation ci-dessus", key="disc_cb")
    c1,_=st.columns([1,3])
    with c1:
        if st.button("▶  Accéder à l'outil", type="primary", disabled=not agreed, key="disc_btn"):
            st.session_state.disclaimer_accepted = True
            st.rerun()
    if not agreed:
        st.markdown('<p style="color:#64748b; font-size:0.88em; margin-top:6px">👆 Cochez la case ci-dessus pour activer l\'accès.</p>', unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
#  HEADER BANNER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-banner">
  <div style="display:flex; align-items:center; gap:20px; flex-wrap:wrap">
    <div style="font-size:2.8em">🏗️</div>
    <div>
      <h1 style="color:#f1f5f9; margin:0; font-size:1.75em; font-weight:800; letter-spacing:-0.02em">
        Conception de Poutre Composite
      </h1>
      <p style="color:#94a3b8; margin:4px 0 0; font-size:0.95em">
        GCI-2011 · Université Laval · Prof. Luca Sorelli
        &nbsp;·&nbsp; CSA S16:24 Ch.17 · Modules B1 &amp; B2
      </p>
    </div>
    <div style="margin-left:auto">
      <span class="badge-ok">✅ Avertissement accepté</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div style="text-align:center; padding:12px 0 16px"><span style="font-size:1.6em">⚙️</span><br><span style="font-size:1.1em; font-weight:700; color:#f1f5f9">Paramètres</span></div>', unsafe_allow_html=True)

    # Presets
    st.markdown('<div class="sidebar-section">🎯  Exercices du cours</div>', unsafe_allow_html=True)
    preset_key = st.selectbox("", list(PRESETS.keys()), key="preset_sel", label_visibility="collapsed")
    P = PRESETS[preset_key]

    # Import
    st.markdown('<div class="sidebar-section">📂  Importer JSON</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("", type=["json"], key="json_up", label_visibility="collapsed")
    if uploaded:
        try:
            raw=json.loads(uploaded.read())
            P=raw.get('gci2011_composite_beam',{}).get('inputs',raw)
            st.success(f"✅  {P.get('description','chargé')}")
        except Exception as e:
            st.error(f"Erreur: {e}")

    def _v(k,d): return P.get(k,d) if P else d

    # Section
    st.markdown('<div class="sidebar-section">🔩  Section d\'acier</div>', unsafe_allow_html=True)
    all_secs=sorted(T1.keys())
    defsec=_v('sec','W410x54')
    sec_idx=all_secs.index(defsec) if defsec in all_secs else all_secs.index('W410x54')
    sec_name=st.selectbox("Section T1 (HSC)",all_secs,index=sec_idx,key="sec_sel")
    sec=dict(T1[sec_name]); sec['name']=sec_name
    with st.expander("📐 Propriétés"):
        c1,c2=st.columns(2)
        for (l,v),(l2,v2) in zip([("As",f"{sec['As']:,} mm²"),("bf",f"{sec['bf']} mm"),("tw",f"{sec['tw']} mm"),("Zx",f"{sec['Zx']} ×10³")],[("d",f"{sec['d']} mm"),("tf",f"{sec['tf']} mm"),("Ix",f"{sec['Ix']} ×10⁶"),("Poids",f"{sec['dl']} kN/m")]):
            c1.metric(l,v); c2.metric(l2,v2)

    # Béton
    st.markdown('<div class="sidebar-section">🧱  Dalle de béton</div>', unsafe_allow_html=True)
    fc_val  =st.slider("f'c [MPa]",15,60,_v('fc',20),5,key="fc")
    Fy_val  =st.select_slider("Fy [MPa]",[300,350,400,450],_v('Fy',350),key="fy")
    be_val  =st.slider("be [mm]",500,5000,_v('be',2500),50,key="be")
    tc_val  =st.slider("tc [mm]",50,300,_v('tc',65),5,key="tc")

    # Coffrage
    st.markdown('<div class="sidebar-section">🏗️  Coffrage</div>', unsafe_allow_html=True)
    deck_opts=["Dalle pleine (sans nervures)","Nervures ⊥ à la poutre","Nervures ∥ à la poutre"]
    defdeck=_v('deck',"Dalle pleine (sans nervures)")
    deck_idx=deck_opts.index(defdeck) if defdeck in deck_opts else 0
    deck_type=st.selectbox("Type",deck_opts,index=deck_idx,key="deck")
    hd_val=0; wd_val=180
    if deck_type!="Dalle pleine (sans nervures)":
        hd_val=st.select_slider("hd [mm]",[38,75],_v('hd',75),key="hd")
        wd_val=st.slider("wd [mm]",50,300,_v('wd',180),10,key="wd")

    # Ec
    st.markdown('<div class="sidebar-section">⚙️  Formule Ec</div>', unsafe_allow_html=True)
    ec_opts=["Simplifiée (4500√f'c)","Complète (3300√f'c+6900)·(ρ/2300)^1.5","Donnée directement (pont)"]
    defec=_v('ec_f',"Simplifiée (4500√f'c)")
    ec_idx=ec_opts.index(defec) if defec in ec_opts else 0
    ec_formula=st.selectbox("",ec_opts,index=ec_idx,key="ec_form",label_visibility="collapsed")
    gc_val=st.slider("γc [kN/m³]",18.0,26.0,float(_v('gc',25.0)),0.5,key="gc")
    Ec_given_val=None
    if ec_formula=="Donnée directement (pont)":
        Ec_given_val=st.number_input("Ec [MPa]",10000,50000,int(_v('Ec_given',30000) or 30000),500,key="ec_given")
    rho=gc_val*1000/9.81
    Ec_v=compute_Ec(fc_val,rho,ec_formula,Ec_given_val)
    n_v=200000/Ec_v
    st.markdown(f'<div style="background:#0f172a;border:1px solid #1e293b;border-radius:8px;padding:8px 12px;font-family:JetBrains Mono,monospace;font-size:0.85em;color:#06b6d4">Ec = {Ec_v:.0f} MPa  →  n = {n_v:.2f}</div>', unsafe_allow_html=True)

    # Composite & portée
    st.markdown('<div class="sidebar-section">⚡  Composite & Portée</div>', unsafe_allow_html=True)
    p_val=st.slider("p [%]",25,100,_v('p',50),5,key="p_pct")
    L_val=st.slider("L [m]",3.0,40.0,float(_v('L',9.0)),0.5,key="span")

    # Charges
    st.markdown('<div class="sidebar-section">📦  Charges</div>', unsafe_allow_html=True)
    wD_val=st.number_input("wD [kN/m]",0.0,200.0,float(_v('wD',5.0)),0.5,key="wD")
    wL_val=st.number_input("wL [kN/m]",0.0,200.0,float(_v('wL',8.0)),0.5,key="wL")

    # Goujons
    st.markdown('<div class="sidebar-section">🔧  Goujons</div>', unsafe_allow_html=True)
    dg_val=st.select_slider("d_goujon [mm]",[16,19,20,22,25],_v('dg',19),key="dg")
    Fu_val=st.select_slider("Fu [MPa]",[415,450],_v('Fu',415),key="fu")
    phi_cr=st.slider("φ fluage",1.0,3.5,2.7,0.1,key="phi_cr")
    hsc_val=115
    if deck_type=="Nervures ⊥ à la poutre":
        hsc_val=st.select_slider("h_stud [mm]",[75,90,115,120,140],_v('hsc',115),key="hsc")

    # NBCC
    st.markdown('<div class="sidebar-section">🔢  Facteurs NBCC</div>', unsafe_allow_html=True)
    aD_val=st.number_input("αD",0.5,1.5,1.25,0.05,key="aD")
    aL_val=st.number_input("αL",0.5,2.0,1.50,0.05,key="aL")

    # Export
    st.markdown('<div class="sidebar-section">💾  Exporter</div>', unsafe_allow_html=True)
    if st.button("📥  Générer JSON",key="exp_btn"):
        d=dict(description=f"Design — {sec_name}",sec=sec_name,fc=fc_val,Fy=Fy_val,
               be=be_val,tc=tc_val,hd=hd_val,p=p_val,L=L_val,gc=gc_val,
               ec_f=ec_formula,Ec_given=Ec_given_val,deck=deck_type,
               dg=dg_val,hsc=hsc_val,wd=wd_val,Fu=Fu_val,wD=wD_val,wL=wL_val,aD=aD_val,aL=aL_val)
        js=json.dumps({"gci2011_composite_beam":{"version":"1.0","inputs":d}},indent=2,ensure_ascii=False)
        st.download_button("⬇️  Télécharger",js,f"beam_{sec_name}_{p_val}p.json","application/json",key="dl_js")

# ══════════════════════════════════════════════════════════════════════════════
#  CALCULATIONS
# ══════════════════════════════════════════════════════════════════════════════
p=p_val/100.0
Asc_s=math.pi*dg_val**2/4
qrs_base=min(0.5*PHI_SC*Asc_s*math.sqrt(fc_val*Ec_v), PHI_SC*Asc_s*Fu_val)
if deck_type=="Dalle pleine (sans nervures)":
    qr_N=qrs_base
elif deck_type=="Nervures ⊥ à la poutre":
    Ap=compute_Ap(hsc_val,wd_val); rho_c=1.0 if rho>=2150 else 0.85
    coef=0.35 if abs(hd_val-75)<5 else (0.61 if abs(hd_val-38)<5 else 0.35+(0.61-0.35)*(hd_val-38)/(75-38))
    qr_N=min(coef*PHI_SC*rho_c*Ap*math.sqrt(fc_val),qrs_base)
else:
    qr_N=min(qrs_base*(0.75+0.167*(wd_val/hd_val-1.5)),qrs_base) if hd_val>0 and wd_val/hd_val>=1.5 else 0.75*qrs_base

elu_r=elu_calc(sec,fc_val,Fy_val,be_val,tc_val,hd_val,p,Ec_v)
n_half=math.ceil(elu_r['Vh']*1e3/qr_N) if qr_N>0 else 0
n_tot=2*n_half
els_r=els_calc(sec,fc_val,be_val,tc_val,hd_val,p,Ec_v,phi_cr)
w_dt=wD_val+sec['dl']; Ie=els_r['Ie']; L_mm=L_val*1e3; E=200000
def _dlt(w,I): return 5*w*(L_mm**4)/(384*E*I)
dL=_dlt(wL_val,Ie); dD=_dlt(w_dt,Ie); dCreep=0.15*dD
# ── Shrinkage deflection — Annex H / HSC §17.3.1 ──────────────────────────
# Δ_s = (L²/8) · c · ε_f · Ac · y / (ns · Ies)
# ε_f=583×10⁻⁶, c=0.5 (appui simple), y = ȳ_s − 0.5·tc
_sp    = els_r['_shrink_params']
_ns    = _sp['ns'];   _Ies = _sp['Ies']
_ybar_c= _sp['ybar_c_top'];  _tc_sh = _sp['tc'];  _be_sh = _sp['be']
_Ac    = _be_sh * _tc_sh
_y     = _ybar_c - 0.5*_tc_sh   # eccentricity: ANE → centroid of slab
_eps_f = 583e-6;  _c = 0.5
dSh    = (L_mm**2/8) * _c * (_eps_f * _Ac * _y) / (_ns * _Ies) if _y > 0 else 0.0
wu=max(aD_val*w_dt+aL_val*wL_val,1.4*w_dt); Mf=wu*L_val**2/8
Mr_s=PHI*sec['Zx']*1e3*Fy_val/1e6
mrc_ok=elu_r['Mrc']>=Mf; def_ok=(dL+dCreep)<=L_val*1000/360

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION PROPERTIES BANNER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style="background:#1e293b; border:1px solid #334155; border-radius:14px;
            padding:16px 22px; margin-bottom:18px;">
  <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px; flex-wrap:wrap;">
    <span style="font-size:1.3em">🔩</span>
    <span style="font-size:1.1em; font-weight:700; color:#f1f5f9">Section choisie : {sec_name}</span>
    <span style="background:rgba(59,130,246,0.2);color:#60a5fa;border:1px solid rgba(59,130,246,0.3);
                 padding:2px 10px;border-radius:20px;font-size:0.82em;font-weight:600">T1 — HSC</span>
    <span style="color:#64748b;font-size:0.88em;margin-left:4px">Fy = {Fy_val} MPa  ·  f'c = {fc_val} MPa  ·  p = {p_val}%  ·  L = {L_val} m</span>
  </div>
  <div style="display:grid; grid-template-columns:repeat(8,1fr); gap:8px;">
    {''.join(f'<div style="background:#0f172a;border:1px solid #334155;border-radius:8px;padding:8px 10px;text-align:center"><div style="color:#64748b;font-size:0.70em;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:3px">{lbl}</div><div style="color:#06b6d4;font-weight:700;font-family:JetBrains Mono,monospace;font-size:0.95em">{val}</div></div>'
    for lbl,val in [
        ("As [mm²]",  f"{sec['As']:,}"),
        ("d [mm]",    f"{sec['d']}"),
        ("bf [mm]",   f"{sec['bf']}"),
        ("tf [mm]",   f"{sec['tf']}"),
        ("tw [mm]",   f"{sec['tw']}"),
        ("Ix [×10⁶]", f"{sec['Ix']}"),
        ("Zx [×10³]", f"{sec['Zx']}"),
        ("SW [kN/m]", f"{sec['dl']}"),
    ])}
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  KPI STRIP
# ══════════════════════════════════════════════════════════════════════════════
k1,k2,k3,k4,k5=st.columns(5)
k1.metric("M_rc [kN·m]",f"{elu_r['Mrc']:.1f}",f"+{(elu_r['Mrc']/Mr_s-1)*100:.0f}% vs acier seul")
k2.metric("M_f [kN·m]",f"{Mf:.1f}",f"{'✅ OK' if mrc_ok else '❌ FAIL'}",delta_color="normal" if mrc_ok else "inverse")
k3.metric("n goujons",n_tot,f"q_r = {qr_N/1e3:.2f} kN/goujon")
k4.metric("Δ_L+fluage [mm]",f"{dL+dCreep:.1f}",f"L/360 = {L_val*1000/360:.0f} mm {'✅' if def_ok else '❌'}",delta_color="normal" if def_ok else "inverse")
k5.metric("Cas ANP",elu_r['case'].upper(),f"ae = {elu_r['ae']:.1f} mm")

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1,tab2,tab3,tab4,tab5=st.tabs(["🔺  ELU — Flexion","🔧  Goujons","📐  Section & ANP / ANE","📏  ELS — Déflexions","📚  Formules"])

# ── Tab 1 ─────────────────────────────────────────────────────────────────────
with tab1:
    cL,cR=st.columns([1.3,1])
    with cL:
        st.plotly_chart(fig_moment(elu_r['Mrc'],Mr_s,Mf),use_container_width=True,key='ch_mom')
        st.plotly_chart(fig_xsec(sec,tc_val,hd_val,be_val,elu_r,uid='t1'),use_container_width=True,key='ch_xs1')
    with cR:
        case_lbl={'a':'ANP dans la dalle','b':"ANP dans l'aile",'c':"ANP dans l'âme"}
        st.markdown(f'<div class="glass-card"><div style="display:flex;align-items:center;justify-content:space-between"><span style="font-size:1.1em;font-weight:700;color:#f1f5f9">Cas {elu_r["case"].upper()} — {case_lbl[elu_r["case"]]}</span><span class="{"badge-ok" if mrc_ok else "badge-fail"}">{"✅ M_rc ≥ M_f" if mrc_ok else "❌ M_rc < M_f"}</span></div></div>',unsafe_allow_html=True)
        st.markdown('<p class="section-hdr">Étapes de calcul ELU §17.9.3</p>',unsafe_allow_html=True)
        for lbl,val,unit in elu_r['steps']:
            if '→ Cas' in lbl:
                st.markdown(f'<div class="step-row case-header"><span>{lbl}</span><span style="color:#94a3b8">{val}</span></div>',unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="step-row"><span style="color:#cbd5e1">{lbl}</span><span class="step-val">{val} <span style="color:#475569">{unit}</span></span></div>',unsafe_allow_html=True)
        st.markdown('<p class="section-hdr">Synthèse</p>',unsafe_allow_html=True)
        for lbl,v,u in [("α₁",elu_r['a1'],""),("C'r,max",elu_r['Cr_max'],"kN"),("Tr,max",elu_r['Tr_max'],"kN"),
                         ("Qr",elu_r['Vh'],"kN"),("ae",elu_r['ae'],"mm"),("e'",elu_r['e_prime'],"mm"),
                         ("M_rc",elu_r['Mrc'],"kN·m"),("Mf",Mf,"kN·m"),("Utilisation",Mf/elu_r['Mrc']*100,"%")]:
            a,b,c=st.columns([2,1,1])
            a.markdown(f'<span style="color:#94a3b8;font-size:0.9em">{lbl}</span>',unsafe_allow_html=True)
            b.markdown(f'<span style="color:#06b6d4;font-weight:600;font-family:JetBrains Mono,monospace">{v:.4g}</span>',unsafe_allow_html=True)
            c.markdown(f'<span style="color:#475569;font-size:0.85em">{u}</span>',unsafe_allow_html=True)

# ── Tab 2 ─────────────────────────────────────────────────────────────────────
with tab2:
    cL,cR=st.columns([1.6,1])
    with cL:
        st.plotly_chart(fig_studs(L_val,n_half,qr_N,elu_r['Vh']),use_container_width=True,key='ch_stds')
    with cR:
        deck_ref={"Dalle pleine (sans nervures)":"§17.7.2.2","Nervures ⊥ à la poutre":"§17.7.2.4","Nervures ∥ à la poutre":"§17.7.2.3"}
        ok_conn=n_tot*qr_N/1e3>=elu_r['Vh'] if n_tot>0 else False
        st.markdown(f'<div class="glass-card"><div style="display:flex;align-items:center;justify-content:space-between"><span style="font-weight:700">{deck_type}</span><span class="badge-info">{deck_ref[deck_type]}</span></div><div style="color:#64748b;font-size:0.85em;margin-top:6px">d_goujon={dg_val}mm · Fu={Fu_val} MPa · Ec={Ec_v:.0f} MPa</div></div>',unsafe_allow_html=True)
        st.markdown('<p class="section-hdr">Résultats goujons</p>',unsafe_allow_html=True)
        for lbl,v,u in [("qrs (dalle pleine)",qrs_base/1e3,"kN"),("q_r utilisé",qr_N/1e3,"kN"),("V_h = Q_r",elu_r['Vh'],"kN"),
                         ("n par demi-portée",n_half,""),("n total",n_tot,""),
                         ("Q_r fourni",n_tot*qr_N/1e3,"kN"),("Utilisation",elu_r['Vh']/(n_tot*qr_N/1e3)*100 if n_tot>0 else 0,"%")]:
            a,b,c=st.columns([2,1,1])
            a.markdown(f'<span style="color:#94a3b8;font-size:0.9em">{lbl}</span>',unsafe_allow_html=True)
            b.markdown(f'<span style="color:#06b6d4;font-weight:600;font-family:JetBrains Mono,monospace">{v:.4g}</span>',unsafe_allow_html=True)
            c.markdown(f'<span style="color:#475569;font-size:0.85em">{u}</span>',unsafe_allow_html=True)
        st.markdown(f'<div style="background:{"rgba(16,185,129,0.1)" if ok_conn else "rgba(239,68,68,0.1)"};border:1px solid {"rgba(16,185,129,0.3)" if ok_conn else "rgba(239,68,68,0.3)"};border-radius:10px;padding:12px 16px;margin-top:12px"><b style="color:{"#10b981" if ok_conn else "#ef4444"}">{"✅ Goujons suffisants" if ok_conn else "❌ Goujons insuffisants"}</b><br><span style="color:#94a3b8;font-size:0.88em">Q_r={n_tot*qr_N/1e3:.1f} kN {"≥" if ok_conn else "<"} V_h={elu_r["Vh"]:.1f} kN</span></div>',unsafe_allow_html=True)

# ── Tab 3 ─────────────────────────────────────────────────────────────────────
with tab3:
    cL,cR=st.columns(2)
    with cL:
        st.plotly_chart(fig_xsec(sec,tc_val,hd_val,be_val,elu_r,uid='t3'),use_container_width=True,key='ch_xs3')
    with cR:
        st.plotly_chart(fig_ane(sec,tc_val,hd_val,be_val,els_r),use_container_width=True,key='ch_ane')
    st.plotly_chart(fig_inertia(els_r,p),use_container_width=True,key='ch_in')
    st.markdown('<p class="section-hdr">Paramètres ELS</p>',unsafe_allow_html=True)
    cols=st.columns(4)
    for i,(l,v,u) in enumerate([("n",els_r['n'],""),("Ec",els_r['Ec'],"MPa"),("ȳ instant.",els_r['ybar'],"mm"),("It",els_r['It']/1e6,"×10⁶mm⁴"),
                                  ("Ie",els_r['Ie']/1e6,"×10⁶mm⁴"),("nₛ fluage",els_r['ns'],""),("E'c",els_r['Ecp'],"MPa"),("ȳ fluage",els_r['ybar_c'],"mm")]):
        with cols[i%4]: st.metric(f"{l} [{u}]" if u else l,f"{v:.4g}")

# ── Tab 4 ─────────────────────────────────────────────────────────────────────
with tab4:
    st.plotly_chart(fig_deflection(dL,dD,dCreep,dSh,L_val),use_container_width=True,key='ch_def')
    st.markdown('<p class="section-hdr">Synthèse déflexions</p>',unsafe_allow_html=True)
    limit=L_val*1000/360
    _sp2   = els_r['_shrink_params']
    _y_sh  = _sp2['ybar_c_top'] - 0.5*_sp2['tc']
    for lbl,v,s in [
        ("Ie effective",          f"{els_r['Ie']/1e6:.0f} ×10⁶ mm⁴",""),
        ("Δ_L (vive)",            f"{dL:.2f} mm",       "✅" if dL<=limit else "⚠️"),
        ("Δ_D (morte)",           f"{dD:.2f} mm",       ""),
        ("Δ_fluage (+15% Δ_D)",   f"{dCreep:.2f} mm",   "§17.3.1b"),
        ("Δ_retrait",             f"{dSh:.2f} mm",      "Annexe H"),
        ("Δ_L + Δ_fluage",        f"{dL+dCreep:.2f} mm","✅ OK" if dL+dCreep<=limit else "❌ Dépasse"),
        ("Δ_total (L+fluage+ret.)",f"{dL+dCreep+dSh:.2f} mm","✅" if dL+dCreep+dSh<=limit else "⚠️"),
        ("Limite L/360",          f"{limit:.1f} mm",    ""),
    ]:
        a,b,c=st.columns([3,2,2])
        a.markdown(f'<span style="color:#94a3b8;font-size:0.9em">{lbl}</span>',unsafe_allow_html=True)
        b.markdown(f'<span style="color:#f1f5f9;font-weight:500">{v}</span>',unsafe_allow_html=True)
        c.markdown(f'<span style="color:#64748b;font-size:0.85em">{s}</span>',unsafe_allow_html=True)

    # Shrinkage parameters detail
    with st.expander("🔍 Paramètres Δ_retrait (Annexe H)"):
        st.markdown(f"""<div class="formula-box">
        Δ_s = (L²/8) · c · ε_f · Ac · y / (nₛ · Ies)<br><br>
        ε_f = 583×10⁻⁶  (Annexe H.4)  &nbsp;·&nbsp;  c = 0.5  (Fig. H.2, appui simple)<br>
        Ac = be·tc = {_sp2['be']:.0f}×{_sp2['tc']:.0f} = {_sp2['be']*_sp2['tc']:.0f} mm²<br>
        y = ȳₛ − 0.5·tc = {_sp2['ybar_c_top']:.1f} − {0.5*_sp2['tc']:.1f} = {_y_sh:.2f} mm<br>
        nₛ = {_sp2['ns']:.2f}  &nbsp;·&nbsp;  Ies = {_sp2['Ies']/1e6:.1f} ×10⁶ mm⁴<br>
        → <b style="color:#06b6d4">Δ_s = {dSh:.2f} mm</b>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="formula-box">Δ_élastique = 5·w·L⁴/(384·E·Ie)  &nbsp;·&nbsp;  Ie=Is+0.85·p^0.25·(It−Is)  &nbsp;·&nbsp;  Δ_fluage=+15%·Δ_D  &nbsp;·&nbsp;  Limite: L/360</div>',unsafe_allow_html=True)

# ── Tab 5 ─────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown('<h3 style="color:#f1f5f9">📚 Référentiel des formules — CSA S16:24 / GCI-2011</h3>',unsafe_allow_html=True)
    for title,content in [
        ("🔷  ELU §17.9.3 — Résistance en flexion",
         "α₁ = 0.85 − 0.0015·f'c  ≥  0.67\nT_r,max = φ·As·Fy  ·  C'_r,max = α₁·φc·be·tc·f'c\nQ_r = p·min(T_r,C'_r)  ·  C_rs = (T_r − Q_r)/2  ·  ae = Q_r/(α₁·φc·be·f'c)\n\nCas A — ANP dans la dalle:  e' = d/2 + hd + tc − ae/2  →  M_rc = T_r·e'\nCas B — ANP dans l'aile:  tfc = C_rs/C_rf,max·tf  →  M_rc = C_rs·es + Q_r·e'\nCas C — ANP dans l'âme:  hc = (C_rs−C_rf,max)/(φ·tw·Fy)  →  M_rc = C_rs·es + Q_r·e'"),
        ("🔶  ELS §17.3.1 — Moments d'inertie & ANE",
         "Ec simplifié : 4500·√f'c  |  Ec complet : (3300√f'c+6900)·(ρ/2300)^1.5  |  Ec pont : donné\nȳ = n·(As/be)·[√(1 + 2·be·ys/(n·As)) − 1]  (si ȳ ≤ tc)\nIt = be·ȳ³/(3n) + Is + As·(ys−ȳ)²  |  Ie = Is + 0.85·p^0.25·(It−Is)\nFluage : E'c = Ec/(1+χ·φ)  χ=0.73  →  nₛ = Es/E'c  →  Its, Ies"),
        ("🔴  Goujons §17.7.2",
         "Dalle pleine : q_rs = 0.5·φsc·Asc·√(f'c·Ec)  ≤  φsc·Asc·Fu\nNervures ⊥  : q_rr = 0.35·φsc·ρc·Ap·√f'c  |  Ap = 2√2·h² + (√2/2)·h·wd\nNervures ∥  : q_rr = q_rs·[0.75 + 0.167·(wd/hd − 1.5)]  si wd/hd ≥ 1.5\nn_total = 2·ceil(V_h / q_rr)"),
        ("🌉  Pont vs Plancher",
         "PONT (Ex 7.4) : Ec donné directement (ex: 30 000 MPa)  |  be = min(L/4, s/2)\n  Dalle pleine (hd=0)  |  Charges: uniforme + concentrée  |  Fu=450 MPa\n\nPLANCHER (Ex 7.1–7.3, 7.5) : Ec calculé par formule  |  be = min(L/4, s)\n  Coffrage métallique possible (hd>0)  |  Nervures ⊥ ou ∥  |  Fu=415 or 450 MPa"),
    ]:
        with st.expander(title, expanded=("ELU" in title)):
            st.markdown(f'<div class="formula-box">{content.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f'<div style="text-align:center;color:#334155;font-size:0.78em;padding:20px 0;border-top:1px solid #1e293b;margin-top:24px">GCI-2011 Conception des structures I  ·  Université Laval  ·  Prof. Luca Sorelli  ·  CSA S16:24 Ch.17<br>Outil pédagogique — aucune responsabilité assumée  ·  Validé Ex.7.1–7.5  ·  Python {sys.version[:6]}</div>',unsafe_allow_html=True)
