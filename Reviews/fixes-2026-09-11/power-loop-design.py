"""TPS552882 averaged-loop screening using datasheet SLVSFC5 eq19-26.

Not a switching simulation. Inner-loop dynamics and PCB parasitics are absent. A one-cycle delay is included as engineering sensitivity.
Boost models use D=1-Vin/Vout; buck cases use D=0/RHP zero disabled as limiting proxy.
"""
import json,math,itertools
from pathlib import Path
import numpy as np
base=Path(__file__).resolve().parent
freq=np.logspace(-1,6,7000);s=2j*np.pi*freq
results=[]
for label,rc,cc,cp in [('original',49.9,10e-9,100e-12),('proposed',10000,100e-9,1000e-12)]:
    rows=[]
    for vi,vo,io,co,esr,rt,ct,gt,lt,cpt in itertools.product([7.7,8,12,18],[11.68,12.35],[.1,1,5,7.72],[100e-6,220e-6,500e-6],[0,.01,.1],[.99,1.01],[.765,1.265],[.8,1.2],[.8,1.2],[.95,1.05]):
        # gm tolerance ±20% is engineering sensitivity, not a manufacturer guarantee.
        d=max(0,1-vi/vo);rl=vo/io
        gp=rl*(1-d)/(.11)/(1+s*rl*co/2)
        if d>0:gp*=1-s*(2*math.pi*4.7e-6*lt)/(rl*(1-d)**2)/(2*math.pi)
        gp*=1+s*esr*co
        z=1/(1/(rc*rt+1/(s*cc*ct))+s*cp*cpt)
        loop=gp*190e-6*gt*z*(1.2/vo)*np.exp(-s/400000)
        mag=20*np.log10(np.abs(loop));phase=np.unwrap(np.angle(loop))*180/np.pi
        inds=np.where((mag[:-1]>=0)&(mag[1:]<0))[0]
        if len(inds)!=1: rows.append({'bad_crossings':len(inds)});continue
        n=inds[0];q=mag[n]/(mag[n]-mag[n+1]);fc=10**(np.log10(freq[n])*(1-q)+np.log10(freq[n+1])*q)
        pm=180+phase[n]*(1-q)+phase[n+1]*q
        gi=np.where((phase[:-1]>-180)&(phase[1:]<=-180))[0]
        gm=999 if len(gi)==0 else -float(mag[gi[0]])
        rows.append(dict(vin=vi,vout=vo,iout=io,cout=co,esr=esr,r_tolerance=rt,c_tolerance=ct,cp_tolerance=cpt,gm_sensitivity=gt,L_tolerance=lt,crossover_hz=fc,phase_margin_deg=pm,gain_margin_db=gm))
    good=[r for r in rows if 'phase_margin_deg' in r]
    results.append({'design':label,'R_ohm':rc,'C_F':cc,'Cp_F':cp,'count':len(rows),'bad_crossings':len(rows)-len(good),'worst_phase':min(good,key=lambda r:r['phase_margin_deg']),'worst_gain':min(good,key=lambda r:r['gain_margin_db']),'maximum_crossover':max(good,key=lambda r:r['crossover_hz'])})
(base/'power-loop-design-results.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))


