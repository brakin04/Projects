//
//
//  Bryan Akin brakin
//  Briana Flores briflore
//  Submission date: 5/7/25
//
//  TableViewController.swift
//  ColorGuesser
//
//  Created by Akin, Bryan on 4/18/25.
//

import UIKit

class TableViewController: UITableViewController {
    // will show best score for each difficulty / mode

    var appDelegate: AppDelegate?
    var myModel: Model?
    
    // array of scores
    var items = [[0]]

    override func viewDidLoad() {
        super.viewDidLoad()
        self.title = "Best Scores"
        self.appDelegate = UIApplication.shared.delegate as? AppDelegate
        self.myModel = self.appDelegate!.myModel
        self.items = self.myModel!.bestScore
    }

    override func viewDidAppear(_ animated: Bool) {
//        print("table view items updated " + String(describing: self.items))
        self.items = self.myModel!.bestScore
    }
    // MARK: - Table view data source

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 6
    }

    override func tableView(_ tableView: UITableView,
                            cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cellIdentifier = "cell"
            
        // Try to reuse a cell
        var cell = tableView.dequeueReusableCell(withIdentifier: cellIdentifier)
            
        // If no reusable cell available create one
        if cell == nil {
            cell = UITableViewCell(style: .subtitle, reuseIdentifier: cellIdentifier)
        }

        self.reloadView()
        var item = items[indexPath.row]
        var mode = ["Easy", "Medium", "Hard"][indexPath.row % 3]
        if indexPath.row >= 3 {
            mode += " Memory"
        }
        item[2] == Int.max ? item[2] = 0 : ()
        cell?.textLabel?.text = "\(mode): \(item[1])% in \(item[2])s"
        cell?.selectionStyle = .none

        return cell!
    }
    
    func reloadView() {
        self.myModel = self.appDelegate!.myModel
        self.items = self.myModel!.bestScore
    }
}
