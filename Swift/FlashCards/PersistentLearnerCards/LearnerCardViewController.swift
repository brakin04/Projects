//
//  LearnerCardViewController.swift
//  PersistentLearnerCards
//

import UIKit

class LearnerCardViewController: UIViewController {
    
    @IBOutlet var answerLabel: UILabel!
    @IBOutlet var questionLabel: UILabel!
    var appDelegate: AppDelegate?
    var myLearnerCardModel: LearnerCardModel?
    var questionShown = false;
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        self.appDelegate = UIApplication.shared.delegate as? AppDelegate
        self.myLearnerCardModel = self.appDelegate?.myLearnerCardModel
        
        if (self.myLearnerCardModel?.currentQuestionIdx != 0) {
            self.myLearnerCardModel?.currentQuestionIdx -= 1
            self.showQuestion(self)
        }
        
        // add an observer for when the model is updated
        NotificationCenter.default.addObserver(self, selector: #selector(modelUpdated), name: Notification.Name("ModelUpdated"), object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(modelUpdated), name: Notification.Name("CellClicked"), object: nil)
    }
    
    // these handle button events
    @IBAction func showQuestion(_ sender: Any) {
        // say a question has been looked at
        questionShown = true
        self.appDelegate = UIApplication.shared.delegate as? AppDelegate
        self.myLearnerCardModel = self.appDelegate?.myLearnerCardModel
        let lQuestion : String = self.myLearnerCardModel!.getNextQuestion()
        self.questionLabel.text = lQuestion
        if (self.questionLabel.text == "That's all the questions! ") {
            self.showAnswer(self)
        }
        else {
            self.answerLabel.text = "(...try guessing...)"
        }
        // tell the edit cards a new question was shown
        NotificationCenter.default.post(name: Notification.Name("UpdateEdit"), object: nil)
    }
    
    // update when ModelUpdated notif
    @objc func modelUpdated() {
        self.showQuestion(self)
    }
    
    @IBAction func showAnswer(_ sender: Any) {
        self.appDelegate = UIApplication.shared.delegate as? AppDelegate
        self.myLearnerCardModel = self.appDelegate?.myLearnerCardModel
        // if the question was looked at already, then it wil show the answer but if not it'll tell you to look at it
        if questionShown {
            let lQuestion : String = self.myLearnerCardModel!.getAnswer()
            self.answerLabel.text = lQuestion
        } else {
            self.answerLabel.text = "Look at the question first."
        }
    }

}

