import math

import numpy as np


class CageTemplate:
    """Class for methods shared between the sea cages and reservoir."""

    def __init__(self, cfg):
        self.cfg = cfg
        self.logger = cfg.logger

    def update_background_lice_mortality(self, lice_population, days):
        """
        Background death in a stage (remove entry) -> rate = number of
        individuals in stage*stage rate (nauplii 0.17/d, copepods 0.22/d,
        pre-adult female 0.05, pre-adult male ... Stien et al 2005)
        """
        lice_mortality_rates = self.cfg.background_fish_mortality_rates

        dead_lice_dist = {}
        for stage in lice_population:
            mortality_rate = lice_population[stage] * lice_mortality_rates[stage] * days
            mortality = min(np.random.poisson(mortality_rate), lice_population[stage])
            dead_lice_dist[stage] = mortality

        self.logger.debug('    background mortality distribn of dead lice = {}'.format(dead_lice_dist))
        return dead_lice_dist

    def fish_growth_rate(self, days):
        """
        Fish growth rate -> 10000/(1+exp(-0.01*(t-475))) fitted logistic curve to data from
        http://www.fao.org/fishery/affris/species-profiles/atlantic-salmon/growth/en/
        """
        return 10000/(1 + math.exp(-0.01*(days-475)))

    @classmethod
    def logit_normalize(self, x):
        expd = math.exp(x)
        return expd / (1 + expd)