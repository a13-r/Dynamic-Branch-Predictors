class TournamentPredictor:
    addresses = []
    decisions = []
    local_history_table = []
    local_prediction_table = []
    global_prediction_table = []
    choice_prediction_table = []
    global_history_register = '0000'
    correct_predictions = 0

    def __init__(self, file_addresses, file_decisions):
        self.addresses = file_addresses
        self.decisions = file_decisions
        self.reset_lht()
        self.reset_lpt()
        self.reset_gpt()
        self.reset_cpt()

    def reset_lht(self):
        for i in range(16):
            self.local_history_table.append('0000')

    def reset_lpt(self):
        for i in range(16):
            self.local_prediction_table.append(0)

    def reset_gpt(self):
        for i in range(16):
            self.global_prediction_table.append(0)

    def reset_cpt(self):
        for i in range(16):
            self.choice_prediction_table.append(0)

    @staticmethod
    def extract_4_lsb(address):
        lsb = bin(address)
        return lsb[len(lsb) - 4:]

    @staticmethod
    def index(lsb):
        return int(lsb, 2)

    def update_tables(self, decision, lht_index, lpt_index, ghr_index, local_prediction, global_prediction):
        if decision == 0:
            if self.local_prediction_table[lpt_index] > 0:
                self.local_prediction_table[lpt_index] -= 1
            if self.global_prediction_table[ghr_index] > 0:
                self.global_prediction_table[ghr_index] -= 1
            self.local_history_table[lht_index] = '0' + self.local_history_table[lht_index][0:3]
            self.global_history_register = '0' + self.global_history_register[0:3]
        else:
            if self.local_prediction_table[lpt_index] < 3:
                self.local_prediction_table[lpt_index] += 1
            if self.global_prediction_table[ghr_index] < 3:
                self.global_prediction_table[ghr_index] += 1
            self.local_history_table[lht_index] = '1' + self.local_history_table[lht_index][0:3]
            self.global_history_register = '1' + self.global_history_register[0:3]

        if (local_prediction >= 2) != (global_prediction >= 2):
            if local_prediction >= 2 and decision == 1:
                if self.choice_prediction_table[ghr_index] > 0:
                    self.choice_prediction_table[ghr_index] -= 1
            elif local_prediction < 2 and decision == 0:
                if self.choice_prediction_table[ghr_index] > 0:
                    self.choice_prediction_table[ghr_index] -= 1
            else:
                if self.choice_prediction_table[ghr_index] < 3:
                    self.choice_prediction_table[ghr_index] += 1

    def update_correct_predictions(self, decision, prediction):
        if prediction >= 2 and decision == 1:
            self.correct_predictions += 1
        elif prediction < 2 and decision == 0:
            self.correct_predictions += 1

    def tournament_prediction(self, local_prediction, global_prediction, ghr_index):
        if (local_prediction >= 2) != (global_prediction >= 2):
            cpt_choice = self.choice_prediction_table[ghr_index]
            if cpt_choice >= 2:
                return global_prediction
        return local_prediction

    def predict(self):
        for i in range(len(self.addresses)):
            address = self.addresses[i]
            lsb = self.extract_4_lsb(address)
            lht_index = self.index(lsb)
            local_prediction_history = self.local_history_table[lht_index]
            lpt_index = self.index(local_prediction_history)
            local_prediction = self.local_prediction_table[lpt_index]
            ghr_index = self.index(self.global_history_register)
            global_prediction = self.global_prediction_table[ghr_index]
            prediction = self.tournament_prediction(local_prediction, global_prediction, ghr_index)
            decision = self.decisions[i]
            self.update_tables(decision, lht_index, lpt_index, ghr_index, local_prediction, global_prediction)
            self.update_correct_predictions(decision, prediction)

    def get_prediction_accuracy(self):
        return self.correct_predictions / len(self.decisions) * 100
