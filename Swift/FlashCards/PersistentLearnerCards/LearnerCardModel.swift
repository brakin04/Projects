//
//  LearnerCardModel.swift
//  PersistentLearnerCards
//

import UIKit

class LearnerCardModel: NSObject, Codable {
    
    var currentQuestionIdx = 0;
    var questions = ["How much is 7+7 ?", "In what country is Timbuktu?", "What rotates when you ride a bike?", "Who is the current president?", "What programming language is this app coded in?", "Where did Sally sell sea shells?", "What beer is Ireland popular for?", "How many neck vertabre do giraffes have?"]
    var answers = ["14", "Mali", "Wheels", "Donald Trump", "Swift", "By the sea shore", "Guiness", "Seven"]
    
    func getNextQuestion() -> String {
        // if its not the last idx increase it, if it is then say it was
        self.currentQuestionIdx += 1
        if (!tooBig()) {
            return self.questions[self.currentQuestionIdx-1]
        }
        return "That's all the questions! "
    }
    func getCurrentQuestion() -> String {
        if (currentQuestionIdx == 0) {
            return "look at a question to edit it"
        }
        if (!tooBig()) {
            return self.questions[self.currentQuestionIdx-1]
        }
        return "Can't edit this"
    }
    
    func getAnswer() -> String {
        if (currentQuestionIdx == 0) {
            return "look at a question to edit it"
        }
        if (!tooBig()) {
            return self.answers[self.currentQuestionIdx-1]
        }
        return "That's all the answers!"
    }
    func setCurrentQuestion(question : String) {
        self.questions[currentQuestionIdx-1] = question
    }
    func setCurentAnswer(answer : String) {
        self.answers[currentQuestionIdx-1] = answer
    }
    
    func tooBig() -> Bool {
        return currentQuestionIdx > questions.count
    }
    
    func addQuestion(question : String) {
        self.questions.append(question)
    }
    
    func addAnswer(answer : String) {
        self.answers.append(answer)
    }
    
    func saveInstance() {
        let encoder = JSONEncoder()
        do {
            // encodes itself to data
            let data = try encoder.encode(self)
            // saves data to UserDefaults under "LearnerCardModel" key
            UserDefaults.standard.set(data, forKey: "LearnerCardModel")
        } catch {
            print("Failed to encode LearnerCardModel: \(error)")
        }
    }
    
    func loadInstance() {
        if let savedData = UserDefaults.standard.data(forKey: "LearnerCardModel") {
            let decoder = JSONDecoder()
            do {
                // decodes saved data back into LearnerCardModel instance
                let decodedModel = try decoder.decode(LearnerCardModel.self, from: savedData)
                // copies decoded data into current instance
                self.currentQuestionIdx = decodedModel.currentQuestionIdx
                self.questions = decodedModel.questions
                self.answers = decodedModel.answers
            } catch {
                print("Failed to decode LearnerCardModel: \(error)")
            }
        }
    }
}
