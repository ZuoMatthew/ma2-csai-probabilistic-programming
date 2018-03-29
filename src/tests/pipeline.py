import unittest
import util


class TestPipeline(unittest.TestCase):

    def assertEqualResultsToProblog(self, file):
        results = util.results_with_pipeline(file, print_steps=False)
        problog_results = util.results_with_problog(file, print_steps=False)

        results = [(query, round(result, 3)) for query, result in results]
        problog_results = [(query, round(result, 3)) for query, result in problog_results]

        self.assertListEqual(results, problog_results)

    def test_alarm_ad(self):
        self.assertEqualResultsToProblog("alarm_ad.pl")

    def test_alarm_first_order(self):
        self.assertEqualResultsToProblog("alarm_first_order.pl")

    def test_alarm_multi_valued_ad(self):
        self.assertEqualResultsToProblog("alarm_multi_valued_ad.pl")

    def test_annotated_disjunction_evidence(self):
        self.assertEqualResultsToProblog("annotated_disjunction_evidence.pl")

    # def test_ball_colors_and_types(self):
    #     self.assertEqualResultsToProblog("ball_colors_and_types.pl")

    # def test_ball_colors_unused_variable_in(self):
    #     self.assertEqualResultsToProblog("ball_colors_unused_variable_in.pl")

    # def test_ball_colors_unused_variable_out(self):
    #     self.assertEqualResultsToProblog("ball_colors_unused_variable_out.pl")

    def test_bayesian_networks(self):
        self.assertEqualResultsToProblog("bayesian_networks.pl")

    def test_bloodtype(self):
        self.assertEqualResultsToProblog("bloodtype.pl")

    def test_bloodtype(self):
        self.assertEqualResultsToProblog("bloodtype.pl")

    def test_flexible_probability(self):
        self.assertEqualResultsToProblog("flexible_probability.pl")

    def test_inhibition_1(self):
        self.assertEqualResultsToProblog("inhibition_1.pl")

    def test_inhibition_2(self):
        self.assertEqualResultsToProblog("inhibition_2.pl")

    def test_inhibition_infection(self):
        self.assertEqualResultsToProblog("inhibition_infection.pl")

    def test_inhibition_infection_negated_head(self):
        self.assertEqualResultsToProblog("inhibition_infection_negated_head.pl")

    def test_inhibition_max_entropy(self):
        self.assertEqualResultsToProblog("inhibition_max_entropy.pl")

    def test_inhibition_osteoporosis(self):
        self.assertEqualResultsToProblog("inhibition_osteoporosis.pl")

    def test_intensional_probabilistic_facts(self):
        self.assertEqualResultsToProblog("intensional_probabilistic_facts.pl")

    def test_monty_hall(self):
        self.assertEqualResultsToProblog("monty_hall.pl")

    def test_multiple_declarations(self):
        self.assertEqualResultsToProblog("multiple_declarations.pl")

    def test_probabilistic_graph(self):
        self.assertEqualResultsToProblog("probabilistic_graph.pl")

    def test_rolling_dice(self):
        self.assertEqualResultsToProblog("rolling_dice.pl")

    # def test_rolling_dice_infinite(self):
    #     self.assertEqualResultsToProblog("rolling_dice_infinite.pl")

    def test_rolling_dice_infinite_sequences(self):
        self.assertEqualResultsToProblog("rolling_dice_infinite_sequences.pl")

    # def test_rolling_dice_negation_as_failure(self):
    #     self.assertEqualResultsToProblog("rolling_dice_negation_as_failure.pl")

    # def test_social_network(self):
    #     self.assertEqualResultsToProblog("social_network.pl")

    def test_tossing_coins(self):
        self.assertEqualResultsToProblog("tossing_coins.pl")


if __name__ == '__main__':
    unittest.main()
