import numpy as np
import pandas as pd
import stats
from functools import reduce
import streamlit as st
import altair as alt


class mvt_bayesian_calculator_manual:
    
    def __init__(self,sample_size_dict,conversions_dict,expected_loss_threshold,expected_loss_type,
                      mcs_simulations=10000):


            self.sample_size_dict = sample_size_dict
            self.conversions_dict = conversions_dict
            self.expected_loss_threshold = expected_loss_threshold
            self.expected_loss_type = expected_loss_type
            self.mcs_simulations = mcs_simulations
            self.alpha_dict = {}
            self.beta_dict = {}
            self.values_dict = {}
            self.categories_wins = {}
            self.prob_wins_dict={}
            for variant in self.sample_size_dict.keys():
                self.alpha_dict [variant] = 1 + self.conversions_dict[variant]
                self.beta_dict [variant] = 1 + self.sample_size_dict[variant] - self.conversions_dict[variant]
                self.values_dict[variant] = np.random.beta(self.alpha_dict[variant],self.beta_dict[variant],mcs_simulations)
                self.categories_wins[variant] = 0
    
    def get_probablities(self):
        for sample in range(self.mcs_simulations):
            values_samples = {}
            for variant in self.sample_size_dict.keys():
                values_samples[variant] = self.values_dict[variant][sample]
            
            winner = max(values_samples,key=values_samples.get)
            print(sample,winner)
            self.categories_wins[winner]+=1

        for variant in self.sample_size_dict.keys():
            self.prob_wins_dict[variant] = round((self.categories_wins[variant]/self.mcs_simulations)*100,3)

        return self.prob_wins_dict

    def get_expected_loss(self):
        # this logic is coming from the following VWO paper, page 14: https://vwo.com/downloads/VWO_SmartStats_technical_whitepaper.pdf
        for variant in self.list_of_variants:

            list_of_values = [self.values_dict[variant]]

            all_other_variants_list = [x for x in self.list_of_variants if x != variant]

            for other_variant in all_other_variants_list:
                list_of_values.append(self.values_dict[other_variant])


            
            samples =list(zip(*list_of_values))


            # for other_variant in all_other_variants_list:

            # print(other_variant,variant)
                # samples =list(zip(values_dict[other_variant],values_dict[variant]))
                # print(samples)
            # for idx in enumerate():
            # print(samples)
            # difference = map(lambda sample: np.max([sample[0]-sample[1], 0]), samples)

            # differences = list(map(lambda sample: np.max([sample[0] - sample[i] for i in range(1, len(sample)),0]), samples))

            # differences = list(map(lambda sample: np.max([sample[0] - sample[i], 0 for i in range(1, len(sample))]), samples))
            differences_for_variant = map(lambda sample: np.max([(sample[0] - sample[i],0) for i in range(1, len(sample))]), samples)
            # print(list(differences_for_variant))
            sum_diff_variant = reduce(lambda x,y:x+y, differences_for_variant)

            # print(sum_diff_variant.mean())

            absolute_expected_loss_variant = (sum_diff_variant/self.mcs_simulations) * 100

            relative_expected_loss_variant = absolute_expected_loss_variant/self.conversions_dict[variant]

            print("absolute_expected_loss_variant",variant,"is ",absolute_expected_loss_variant)
            # print(sum_diff_variant.mean())
                
            print("relative_expected_loss_variant",variant,"is ",relative_expected_loss_variant)
            # break
    def plotting_graph(self):

        # st.write(prob_wins_dict)
        
        prob_wins_dict_fig = {"Variation":list(self.prob_wins_dict.keys()),"Probability":list(self.prob_wins_dict.values())}
        # st.write(prob_wins_dict_fig)
        # # print(prob_wins_dict_fig)
        # fig = px.bar(prob_wins_dict_fig, x='Probability', y='Variation',orientation='h',title='Probability to be Best',opacity=1,text = "Probability",width= 1000,height = 500)
        # fig.update_yaxes(showgrid=True)
        # st.plotly_chart(fig,use_container_width=True)
        source = pd.DataFrame(prob_wins_dict_fig)
        bars = alt.Chart(source).mark_bar().encode(
            x='Probability:Q',
            y="Variation:O"
        ).properties(title = "Probability to be Best ")
        text = bars.mark_text(
                # align='center',
                # baseline='middle',
                xOffset = -50,
                dx=-25 # Nudges text to right so it doesn't appear on top of the bar
            ).encode(
                text='Probability:Q'
            )
        chart = (bars + text).properties(width= 1000,height = 500)
        chart = chart.configure_axis(grid=False)
        st.altair_chart(chart, theme="streamlit", use_container_width=True)