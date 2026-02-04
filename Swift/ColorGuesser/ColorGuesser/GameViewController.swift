//
//
//  Bryan Akin brakin
//  Briana Flores briflore
//  Submission date: 5/7/25
//
//  GameViewController.swift
//  ColorGuesser
//
//  Created by Akin, Bryan on 4/18/25.
//

import UIKit
import CoreMotion
import UserNotifications

class GameViewController: UIViewController {
    
    let nm: NotificationManager = NotificationManager()
    var appDelegate: AppDelegate?
    var myModel: Model?
    var canPlay = false
    
    // easy buttons
    @IBOutlet var eb1: UIButton!; @IBOutlet var eb2: UIButton!; @IBOutlet var eb3: UIButton!; @IBOutlet var eb4: UIButton! //@IBOutlet var eb5: UIButton!; @IBOutlet var eb6: UIButton!; @IBOutlet var eb7: UIButton!; @IBOutlet var eb8: UIButton!; @IBOutlet var eb9: UIButton!
    
    // medium buttons
    @IBOutlet var mb1: UIButton!; @IBOutlet var mb2: UIButton!; @IBOutlet var mb3: UIButton!; @IBOutlet var mb4: UIButton!; @IBOutlet var mb5: UIButton!; @IBOutlet var mb6: UIButton!; @IBOutlet var mb7: UIButton!; @IBOutlet var mb8: UIButton!; @IBOutlet var mb9: UIButton!; //@IBOutlet var mb10: UIButton!; @IBOutlet var mb11: UIButton!; @IBOutlet var mb12: UIButton!; @IBOutlet var mb13: UIButton!; @IBOutlet var mb14: UIButton!; @IBOutlet var mb15: UIButton!; @IBOutlet var mb16: UIButton!
    
    // hard buttons
    @IBOutlet var hb1: UIButton!; @IBOutlet var hb2: UIButton!; @IBOutlet var hb3: UIButton!; @IBOutlet var hb4: UIButton!; @IBOutlet var hb5: UIButton!; @IBOutlet var hb6: UIButton!; @IBOutlet var hb7: UIButton!; @IBOutlet var hb8: UIButton!; @IBOutlet var hb9: UIButton!; @IBOutlet var hb10: UIButton!; @IBOutlet var hb11: UIButton!; @IBOutlet var hb12: UIButton!; @IBOutlet var hb13: UIButton!; @IBOutlet var hb14: UIButton!; @IBOutlet var hb15: UIButton!; @IBOutlet var hb16: UIButton!; //@IBOutlet var hb17: UIButton!; @IBOutlet var hb18: UIButton!; @IBOutlet var hb19: UIButton!; @IBOutlet var hb20: UIButton!; @IBOutlet var hb21: UIButton!; @IBOutlet var hb22: UIButton!; @IBOutlet var hb23: UIButton!; @IBOutlet var hb24: UIButton!; @IBOutlet var hb25: UIButton!
    
    // color select buttons
    @IBOutlet var cb1: UIButton!; @IBOutlet var cb2: UIButton!; @IBOutlet var cb3: UIButton!; @IBOutlet var cb4: UIButton!; @IBOutlet var cb5: UIButton!; @IBOutlet var cb6: UIButton!; @IBOutlet var cb7: UIButton!; @IBOutlet var cb8: UIButton!; @IBOutlet var cb9: UIButton!; @IBOutlet var cb10: UIButton!
    
    
    
    // time
    @IBOutlet var timeLabel: UILabel!
    var timer: Timer?
    var time = 0
    
    // coloring
    var selectedColor = UIColor.systemGray5
    
    // score Label
    @IBOutlet var scoreLabel: UILabel!
    
    // sumbit / play again buttons
    @IBOutlet var submitButton: UIButton!
    @IBOutlet var againButton: UIButton!
    
    var selectedOrder: [Int] = []
    
    // this difficulty's buttons
    var buttons: [UIButton]!
    
    // core motion variables
    let motionManager = CMMotionManager()
    let shakeThreshold: Double = 2.5
    
    override func viewDidLoad() {
        super.viewDidLoad()
        nm.schedulePing(after: 25)
        // Do any additional setup after loading the view.
        self.appDelegate = UIApplication.shared.delegate as? AppDelegate
        self.myModel = self.appDelegate?.myModel
        // initialize the board
        self.myModel!.initBoard()
        self.timer = Timer.scheduledTimer(timeInterval: 1.0,
                                          target: self,
                                          selector: #selector(updateTimer),
                                          userInfo: nil,
                                          repeats: true)
        self.timeLabel.textColor = UIColor.red
        // initialize the buttons
        let difficulty = self.myModel!.difficulty
        if difficulty == 1 {
            self.buttons = [eb1,eb2,eb3,eb4]
        } else if difficulty == 2 {
            self.buttons = [mb1,mb2,mb3,mb4,mb5,mb6,mb7,mb8,mb9]
        } else {
            self.buttons = [hb1,hb2,hb3,hb4,hb5,hb6,hb7,hb8,hb9,hb10,hb11,hb12,hb13,hb14,hb15,hb16]
        }
        for button in self.buttons {
            button.isHidden = false
        }
        
        self.setColorButtons()
        
        // core motion setup
        if motionManager.isAccelerometerAvailable {
            motionManager.accelerometerUpdateInterval = 0.2
            motionManager.startAccelerometerUpdates(to: .main) { data, error in
                guard let data = data else { return }
                
                let acceleration = data.acceleration
                let magnitude = sqrt(acceleration.x * acceleration.x +
                                     acceleration.y * acceleration.y +
                                     acceleration.z * acceleration.z)
                
                if magnitude > self.shakeThreshold {
                    self.handleShake()
                }
            }
        }
    }
    
    override func viewDidAppear(_ animated: Bool) {
        
        // colors board depending on game mode after view has been loaded
        if self.myModel!.rememberOrder {
            //            self.colorInOrder()
            self.colorinOrder()
        } else {
            self.colorBoard()
        }
    }
    
    override func viewDidDisappear(_ animated: Bool) {
        motionManager.stopAccelerometerUpdates()
    }
    
    func colorinOrder() {
        // this is used for the memory portion of the game
        let colors = self.myModel!.board
        var count = 1
        for i in self.myModel!.order {
            DispatchQueue.main.asyncAfter(deadline: .now() + Double(count)) {
                UIView.animate(withDuration: 0.3) {
                    self.buttons[i].tintColor = colors[i]
                }
            }
            count += 1
        }
    }
    
    // populates board
    func colorBoard() {
        let colors = self.myModel!.board
        let step = [3,8,15][self.myModel!.difficulty - 1]
        for i in 0...step {
            self.buttons[i].tintColor = colors[i]
            self.buttons[i].tag = i
            self.buttons[i].titleLabel!.textColor = colors[i]
        }
    }
    
    // depopulates board colors
    func clearBoard() {
        let color = UIColor.darkGray
        let step = [3,8,15][self.myModel!.difficulty - 1]
        for i in 0...step {
            self.buttons[i].tintColor = color
            self.buttons[i].titleLabel!.textColor = color
        }
    }
    
    // clears the board when the phone is shaken using core motion
    func handleShake() {
        if canPlay {
            self.selectedOrder = []
            self.clearBoard()
        }
    }
        
    func setColorButtons() {
        let colors = self.myModel!.colors
        let cbuttons = [cb1,cb2,cb3,cb4,cb5,cb6,cb7,cb8,cb9,cb10]
        for i in 0...9 {
            cbuttons[i]!.tintColor = colors[i]
        }
    }
        
    @IBAction func chooseColor(_ sender: UIButton) {
        // this will set the selected color to what the user chooses
        if canPlay {
            self.selectedColor = sender.tintColor
        }
    }
        
    @IBAction func putColor(_ sender: UIButton) {
        // this will make the selected buttons color the selectedColor
        if canPlay && selectedColor != UIColor.systemGray5 {
            // checks if it needs to record order
            if self.myModel!.rememberOrder {
                //                print("\(sender.tag) was clicked")
                selectedOrder.append(sender.tag)
            }
            sender.tintColor = self.selectedColor
        }
    }
        
    @IBAction func playAgain(_ sender: UIButton) {
        self.submitButton.isHidden = false
        self.againButton.isHidden = true
        self.refreshView()
    }
        
        
    @IBAction func submit(_ sender: UIButton) {
        let incTime = self.myModel!.rememberOrder ? buttons.count + 2 : 10
        if (time >= incTime) {
            // this will submit the players board
            self.canPlay = false
            var answer = [self.buttons[0].tintColor!]
            let step = [3,8,15][self.myModel!.difficulty-1]
            for i in 1...step {
                answer.append(self.buttons[i].tintColor!)
            }
            let values = self.myModel!.submit(answer: answer, inOrder: selectedOrder, time: self.time - incTime)
            self.scoreLabel!.text = "You got \(values[0])/\(values[1]) or \(values[2])%!"
            self.submitButton.isHidden = true
            self.againButton.isHidden = false
            self.saveData()
        }
    }
        
    @objc func updateTimer() {
        let incValue = self.myModel!.rememberOrder ? buttons.count + 2 : 10
        if (self.time < incValue || canPlay) {
            self.time += 1
            let tempTime = self.time - incValue
            if tempTime > 0 {
                if self.time >= 60 {
                    self.timeLabel.text = "Time: \(tempTime/60):\(tempTime%60)s"
                } else {
                    self.timeLabel.text = "Time: \(tempTime)s"
                }
            } else {
                self.timeLabel.textColor = UIColor.red
                self.timeLabel.text = "Time: \(-tempTime)s"
            }
            // allows to play the game
            if self.time == incValue {
                self.canPlay = true
                self.clearBoard()
                self.timeLabel.textColor = UIColor.black
            }
        } else if (self.time >= incValue && !canPlay) {
            timer!.invalidate()
        }
    }
        
    // for when playing again
    private func refreshView() {
        // reset all values
        self.canPlay = false
        self.time = 0
        self.selectedOrder = []
        // initialize the board
        self.myModel!.initBoard()
        self.clearBoard()
        self.selectedColor = UIColor.systemGray5
        self.timer = Timer.scheduledTimer(timeInterval: 1.0,
                                            target: self,
                                            selector: #selector(updateTimer),
                                            userInfo: nil,
                                            repeats: true)
        if self.myModel!.rememberOrder {
            self.colorinOrder()
        } else {
            self.colorBoard()
        }
        self.scoreLabel!.text = ""
        self.timeLabel.textColor = UIColor.red
        self.timeLabel.text = "Time: --s"
    }
        
    func saveData() {
        let context = appDelegate?.container.mainContext
        do {
            try context?.save()  // Persist the updated model
        } catch {
            print("Failed to save updated difficulty: \(error)")
        }
    }
        
    func scheduleFifteenSecondPing() {
        let content = UNMutableNotificationContent()
        content.title = "Time's Up!"
        content.body = "15 seconds have passed."
        content.sound = UNNotificationSound.default
            
        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 15, repeats: false)
            
        let request = UNNotificationRequest(identifier: UUID().uuidString, content: content, trigger: trigger)
            
        UNUserNotificationCenter.current().add(request) { error in
            if let error = error{
                print("Notification scheduling failed: \(error.localizedDescription)")
            } else {
                print("Notification Scheduled.")
            }
        }
    }
}
