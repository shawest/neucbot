import functools
from . import neucbot
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import io
import base64
from colour import Color
import numpy as np
import pandas as pd

from flask import ( # type: ignore
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from UI.db import get_db # type: ignore

bp = Blueprint('calc', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
def calc():
    if request.method == 'POST':
        alphas = request.form.get('alpha_chain')
        mat = request.form.get('material')
        slow_calc = request.form.get('a_energy_calculation')

        if not alphas:
            flash('Input text is required')
            return redirect(url_for('calc.calc'))
        
        #Process the 
        #neucbot.constants.run_talys = True
        neucbot.constants.download_data = True
        alpha_list = neucbot.loadChainAlphaList(alphas)
        #alpha_list = neucbot.loadAlphaList(alphas)
        mat_comp = neucbot.readTargetMaterial(mat)

        neucbot.download_talys_data(mat_comp)

        if(slow_calc == "True"):
            xsects, nspec, pspec, aspec, max_alpha, a_n_list, aspec_norm = neucbot.run_alpha_energy_loss(alpha_list, mat_comp, .01)

            blue = Color("blue")
            colors = list(blue.range_to(Color("Yellow"),100))
            
            #nspec graph
            fig, ax = plt.subplots()
            ax.plot(sorted(pspec.keys()),[pspec[k] for k in sorted(pspec.keys())], linestyle="-", color='g')
            ax.set_title("Neutron Emission Probability Spectrum")
            ax.set_xlabel("Neutron Energy")
            ax.set_ylabel("Probability")
            ax.grid()

            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            ngraph = base64.b64encode(buf.getvalue()).decode()

            graph_list = {}
            tuf = {}
            for e in a_n_list:

                fig, nx = plt.subplots()
                nx.plot(sorted(a_n_list[e].keys()),[a_n_list[e][k] for k in sorted(a_n_list[e].keys())], linestyle="-", color='b')
                title = "(a,n) Spectrum for " + str(e) + " keV En"
                nx.set_title(title)
                nx.set_xlabel("ΔEα")
                nx.set_ylabel("Probability/keV")
                #plt.figure(figsize=(8,6))

                tuf[e] = io.BytesIO()
                plt.savefig(tuf[e], format="png")
                tuf[e].seek(0)
                graph_list[e] = base64.b64encode(tuf[e].getvalue()).decode()

            fig, tx = plt.subplots()

            max_prob = max(aspec_norm.values())
            viridis_colors = [cm.viridis(i / (10000-1)) for i in range(10000)]

            xbins = np.unique(sorted({key[0] for key in aspec_norm.keys()}))
            ybins = np.unique(sorted({key[1] for key in aspec_norm.keys()}))

            histogram_data = np.zeros((len(ybins), len(xbins)))

            for i, x in enumerate(xbins):
                for j, y in enumerate(ybins):
                    histogram_data[j, i] = aspec_norm.get((x, y), 0)

            # Plot using `pcolormesh`
            plt.figure(figsize=(8,6))
            hx = plt.pcolormesh(xbins, ybins, histogram_data, shading='nearest', cmap='rainbow')
            
            cbar = plt.colorbar(hx)

            plt.title("2d histogram")
            plt.xlabel("Neutron Energy(keV)")
            plt.ylabel("ΔEα(MeV)")

            suf = io.BytesIO()
            plt.savefig(suf,format="png")
            suf.seek(0)
            hist = base64.b64encode(suf.getvalue()).decode()


            return render_template('calc/calc.html', xsect = xsects,nspec = nspec, probspec = pspec, aspec = aspec, max_alpha = max_alpha, ngraph=ngraph, graph_list = graph_list, hist = hist)

        else:
            xsects, nspec = neucbot.run_alpha(alpha_list, mat_comp, .01)
            return render_template('calc/calc.html', xsect = xsects,nspec = nspec)
            
        print(f"User input: {alpha_list}")
        
    else:
        return render_template('calc/calc.html')
