import unittest
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import util


def get_results(file):
    results = util.results_with_pipeline(file, counter="minic2d", print_steps=False)
    problog_results = util.results_with_problog(file, print_steps=False)

    results = [(query.replace(" ", ""), round(result, 3)) for query, result in results]
    problog_results = [(query.replace(" ", ""), round(result, 3)) for query, result in problog_results]
    return results, problog_results


class TestPipeline(unittest.TestCase):

    def test_alarm_ad(self):
        results, problog_results = get_results("alarm_ad.pl")
        self.assertListEqual(results, problog_results)

    def test_alarm_first_order(self):
        results, problog_results = get_results("alarm_first_order.pl")
        self.assertListEqual(results, problog_results)

    def test_alarm_multi_valued_ad(self):
        results, problog_results = get_results("alarm_multi_valued_ad.pl")
        self.assertListEqual(results, problog_results)

    def test_annotated_disjunction_evidence(self):
        results, problog_results = get_results("annotated_disjunction_evidence.pl")
        self.assertListEqual(results, problog_results)

    def test_ball_colors_and_types(self):
        results, problog_results = get_results("ball_colors_and_types.pl")
        self.assertListEqual(results, problog_results)

    def test_ball_colors_unused_variable_in(self):
        results, problog_results = get_results("ball_colors_unused_variable_in.pl")
        self.assertListEqual(results, problog_results)

    def test_ball_colors_unused_variable_out(self):
        results, problog_results = get_results("ball_colors_unused_variable_out.pl")
        self.assertListEqual(results, problog_results)

    def test_bayesian_networks(self):
        results, problog_results = get_results("bayesian_networks.pl")
        self.assertListEqual(results, problog_results)

    def test_bloodtype(self):
        results, problog_results = get_results("bloodtype.pl")
        self.assertListEqual(results, problog_results)

    # CONTAINS LISTS, OUT OF SCOPE OF PROJECT
    # def test_flexible_probability(self):
    #     results, problog_results = get_results("flexible_probability.pl")
    #     self.assertListEqual(results, problog_results)

    def test_inhibition_1(self):
        results, problog_results = get_results("inhibition_1.pl")
        self.assertListEqual(results, problog_results)

    def test_inhibition_2(self):
        results, problog_results = get_results("inhibition_2.pl")
        self.assertListEqual(results, problog_results)

    # CONTAINS CIRCULAR RULES, OUT OF SCOPE OF PROJECT
    # def test_inhibition_infection(self):
    #     results, problog_results = get_results("inhibition_infection.pl")
    #     self.assertListEqual(results, problog_results)

    def test_inhibition_infection_negated_head(self):
        results, problog_results = get_results("inhibition_infection_no_circular.pl")
        self.assertListEqual(results, problog_results)

    # CONTAINS CIRCULAR RULES, OUT OF SCOPE OF PROJECT
    # def test_inhibition_infection_negated_head(self):
    #     results, problog_results = get_results("inhibition_infection_negated_head.pl")
    #     self.assertListEqual(results, problog_results)

    def test_inhibition_max_entropy(self):
        results, problog_results = get_results("inhibition_max_entropy.pl")
        self.assertListEqual(results, problog_results)

    def test_inhibition_osteoporosis(self):
        results, problog_results = get_results("inhibition_osteoporosis.pl")
        self.assertListEqual(results, problog_results)

    def test_intensional_probabilistic_facts(self):
        results, problog_results = get_results("intensional_probabilistic_facts.pl")
        self.assertListEqual(results, problog_results)

    def test_monty_hall(self):
        results, problog_results = get_results("monty_hall.pl")
        self.assertListEqual(results, problog_results)

    def test_multiple_declarations(self):
        results, problog_results = get_results("multiple_declarations.pl")
        self.assertListEqual(results, problog_results)

    def test_probabilistic_graph(self):
        results, problog_results = get_results("probabilistic_graph.pl")
        self.assertListEqual(results, problog_results)

    def test_rolling_dice(self):
        results, problog_results = get_results("rolling_dice.pl")
        self.assertListEqual(results, problog_results)

    # CONTAINS CIRCULAR RULES, OUT OF SCOPE OF PROJECT
        # def test_rolling_dice_infinite(self):
    #     results, problog_results = get_results("rolling_dice_infinite.pl")
    #     self.assertListEqual(results, problog_results)

    # CONTAINS LISTS, OUT OF SCOPE OF PROJECT
    # def test_rolling_dice_infinite_sequences(self):
    #     results, problog_results = get_results("rolling_dice_infinite_sequences.pl")
    #     self.assertListEqual(results, problog_results)

    # CONTAINS CIRCULAR RULES, OUT OF SCOPE OF PROJECT
    # def test_rolling_dice_negation_as_failure(self):
    #     results, problog_results =   get_results("rolling_dice_negation_as_failure.pl")
    #     self.assertListEqual(results, problog_results)

    def test_social_network(self):
        results, problog_results = get_results("social_network.pl")
        self.assertListEqual(results, problog_results)

    def test_tossing_coins(self):
        results, problog_results = get_results("tossing_coins.pl")
        self.assertListEqual(results, problog_results)


if __name__ == '__main__':
    unittest.main()
