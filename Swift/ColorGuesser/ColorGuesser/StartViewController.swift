//
//
//  Bryan Akin brakin
//  Briana Flores briflore
//  Submission date: 5/7/25
//
//  ViewController.swift
//  ColorGuesser
//
//  Created by Akin, Bryan on 4/18/25.
//

import UIKit

class StartViewController: UIViewController {
    
    var appDelegate: AppDelegate?
    var myModel: Model?
    let nm: NotificationManager = NotificationManager()
    
    @IBOutlet var startButton: UIButton!
    @IBOutlet var imageView: UIImageView!
    

    override func viewDidAppear(_ animated: Bool) {
            super.viewDidAppear(animated)
            AudioManager.shared.startBackgroundMusic()
        }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.appDelegate = UIApplication.shared.delegate as? AppDelegate
        self.myModel = self.appDelegate?.myModel
        nm.requestAuthorizationIfNeeded()
        // Load the image
        imageView.image = UIImage(named: "gridImage")
    }
    
    @IBAction func playGame(_ sender: UIButton) {
        // Schedule ping 15 seconds from now
        performSegue(withIdentifier: "goToGame", sender: self)
    }
//    override func viewDidAppear(_ animated: Bool) {
//        super.viewDidAppear(animated)
//        scheduleFifteenSecondPing()
//     }
    
    // func newGameButtonTapped(_ sender: Any) {
        // Reschedule whenever the user starts a brand‑new game
//        nm.shared.schedulePing(after: 15)
    // }
}

