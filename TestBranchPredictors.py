from dynamic_branch_predictors.read_data import read_data
from dynamic_branch_predictors.correlating_predictor import CorrelatingPredictor
from dynamic_branch_predictors.tournament_predictor import TournamentPredictor

addresses, decisions = read_data()

CP = CorrelatingPredictor(addresses, decisions)
TP = TournamentPredictor(addresses, decisions)

CP.predict()
TP.predict()

CP_accuracy = CP.get_prediction_accuracy()
TP_accuracy = TP.get_prediction_accuracy()

print("Prediction accuracy(Correlating Predictor) = " + f'{CP_accuracy:.2f}' + "%")
print("Prediction accuracy(Tournament Predictor)  = " + f'{TP_accuracy:.2f}' + "%")
