class CorrelatingPredictor:
    addresses = []
    decisions = []
    local_history_table = []
    local_prediction_table = []
    correct_predictions = 0

    def __init__(self, file_addresses, file_decisions):
        self.addresses = file_addresses
        self.decisions = file_decisions
        self.reset_lht()
        self.reset_lpt()

    def reset_lht(self):
        for i in range(16):
            self.local_history_table.append('0000')

    def reset_lpt(self):
        for i in range(16):
            self.local_prediction_table.append(0)

    @staticmethod
    def extract_4_lsb(address):
        lsb = bin(address)
        return lsb[len(lsb) - 4:]

    @staticmethod
    def index(lsb):
        return int(lsb, 2)

    def update_tables(self, decision, lht_index, lpt_index):
        if decision == 0:
            if self.local_prediction_table[lpt_index] > 0:
                self.local_prediction_table[lpt_index] -= 1
            self.local_history_table[lht_index] = '0' + self.local_history_table[lht_index][0:3]
        else:
            if self.local_prediction_table[lpt_index] < 3:
                self.local_prediction_table[lpt_index] += 1
            self.local_history_table[lht_index] = '1' + self.local_history_table[lht_index][0:3]

    def update_correct_predictions(self, decision, prediction):
        if prediction >= 2 and decision == 1:
            self.correct_predictions += 1
        elif prediction < 2 and decision == 0:
            self.correct_predictions += 1

    def predict(self):
        for i in range(len(self.addresses)):
            address = self.addresses[i]
            lsb = self.extract_4_lsb(address)
            lht_index = self.index(lsb)
            local_prediction_history = self.local_history_table[lht_index]
            lpt_index = self.index(local_prediction_history)
            prediction = self.local_prediction_table[lpt_index]
            decision = self.decisions[i]
            self.update_tables(decision, lht_index, lpt_index)
            self.update_correct_predictions(decision, prediction)

    def get_prediction_accuracy(self):
        return self.correct_predictions / len(self.decisions) * 100
