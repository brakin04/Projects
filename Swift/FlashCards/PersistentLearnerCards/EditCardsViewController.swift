//
//  EditCardsViewController.swift
//  PersistentLearnerCards
//

import UIKit
import Foundation

class EditCardsViewController: UIViewController {

    @IBOutlet weak var questionTextField: UITextField!
    @IBOutlet weak var answerTextField: UITextField!
    @IBOutlet var label: UILabel!
    
    var appDelegate: AppDelegate?
    var myLearnerCardModel: LearnerCardModel?
    var tooBig = false
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.appDelegate = UIApplication.shared.delegate as? AppDelegate
        self.myLearnerCardModel = self.appDelegate?.myLearnerCardModel
        var cQuestion = ""
        var cAnswer = ""
        tooBig = self.myLearnerCardModel!.tooBig()
            
        if (!tooBig) {
            cAnswer = self.myLearnerCardModel!.getAnswer()
            cQuestion = self.myLearnerCardModel!.getCurrentQuestion()
        } else {
            cQuestion = "Cannot edit this"
            cAnswer = "Cannot edit this"
        }
            
        // Do any additional setup after loading the view.
        self.questionTextField.text = cQuestion
        self.answerTextField.text = cAnswer
        // Add an observer for when a new question is shown
        NotificationCenter.default.addObserver(self, selector: #selector(Update), name: Notification.Name("UpdateEdit"), object: nil)
    }
    
    @objc func Update() {
        self.viewDidLoad()
        self.label.text = ""
    }
    
    @IBAction func buttonOKAction(sender: AnyObject) {
        // changes the q/a to what was put unless blank
        if (tooBig) {
            self.viewDidLoad()
            return
        }
        let QT = self.questionTextField.text!
        let AT = self.answerTextField.text!
        if (QT.isEmpty || AT.isEmpty) {
            self.label.text = "These are both required"
            return
//            print ("self.questionTextField.text = \(self.questionTextField.text)")
//            print ("self.answerTextField.text = \(self.answerTextField.text)")
        }
        if (self.myLearnerCardModel!.currentQuestionIdx != 0 && !self.myLearnerCardModel!.tooBig()) {
            self.appDelegate = UIApplication.shared.delegate as? AppDelegate
            self.myLearnerCardModel = self.appDelegate?.myLearnerCardModel
            // setting the new data
            self.myLearnerCardModel!.setCurrentQuestion(question: QT)
            self.myLearnerCardModel!.setCurentAnswer(answer: AT)
            self.myLearnerCardModel!.currentQuestionIdx -= 1
            // say the model has been updated
            NotificationCenter.default.post(name: Notification.Name("ModelUpdated"), object: nil)
            // saves instance every time OK is pressed
            self.myLearnerCardModel?.saveInstance()
            return
        }
        // if the idx is 0 or too big, do nothing
        return
    }
    
    @IBAction func buttonNewQuestion(sender: AnyObject) {
        let QT = self.questionTextField.text!
        let AT = self.answerTextField.text!
        if (QT.isEmpty || AT.isEmpty) {
            self.label.text = "These are both required"
            return
        }
        self.appDelegate = UIApplication.shared.delegate as? AppDelegate
        self.myLearnerCardModel = self.appDelegate?.myLearnerCardModel
        // setting the new data
        self.myLearnerCardModel!.addQuestion(question: QT)
        self.myLearnerCardModel!.addAnswer(answer: AT)
        self.myLearnerCardModel!.currentQuestionIdx -= 1
        // say the model has been updated
        NotificationCenter.default.post(name: Notification.Name("ModelUpdated"), object: nil)
        // saves instance every time New Question is pressed
        self.myLearnerCardModel?.saveInstance()
        return
    }

}
