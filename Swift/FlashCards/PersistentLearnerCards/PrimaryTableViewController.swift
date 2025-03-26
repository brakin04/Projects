//
//  PrimaryTableViewController.swift
//  PersistentLearnerCards
//

import UIKit

class PrimaryTableViewController: UITableViewController {
    
    var appDelegate: AppDelegate?
    var myLearnerCardModel: LearnerCardModel?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.appDelegate = UIApplication.shared.delegate as? AppDelegate
        self.myLearnerCardModel = self.appDelegate?.myLearnerCardModel
        // reigster basic cell
        self.tableView.register(UITableViewCell.self, forCellReuseIdentifier: "QuestionCell")
        // Add an observer for when the model is updated
        NotificationCenter.default.addObserver(self, selector: #selector(update), name: Notification.Name("ModelUpdated"), object: nil)
    }
    
    // initiaizes the amount of rows
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return myLearnerCardModel?.questions.count ?? 0
    }

    // returns cells at specific index
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "QuestionCell", for: indexPath)
            
        // gets and adds question from model
        if let question = myLearnerCardModel?.questions[indexPath.row] {
            cell.textLabel?.text = question
            cell.backgroundColor = .lightGray
        }
            
        return cell
    }
        
    // question selection via table view
        override func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
            // When a cell is clicked, it takes you to that question
            tableView.deselectRow(at: indexPath, animated: true)
            self.myLearnerCardModel?.currentQuestionIdx = indexPath.row
            // tell learner card that a cell has been selected
            NotificationCenter.default.post(name: Notification.Name("CellClicked"), object: nil)
        }
    
    @objc func update() {
        self.tableView.reloadData()
    }
    
}
