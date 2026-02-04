//
//
//  Bryan Akin brakin
//  Briana Flores briflore
//  Submission date: 5/7/25
//
//  SettingsViewController.swift
//  ColorGuesser
//
//  Created by Akin, Bryan on 4/18/25.
//

import UIKit
import UserNotifications


class SettingsViewController: UIViewController {
    
    var appDelegate: AppDelegate?
    var myModel: Model?
    
    // Init all the buttons for the switches
    @IBOutlet var RandDiffOn: UIButton!; @IBOutlet var RandDiffOff: UIButton!; @IBOutlet var RandDiffBG: UIButton!;
    @IBOutlet var sfxOn: UIButton!; @IBOutlet var sfxOff: UIButton!; @IBOutlet var sfxBG: UIButton!;
    @IBOutlet var OrderOn: UIButton!; @IBOutlet var OrderOff: UIButton!; @IBOutlet var OrderBG: UIButton!;
    @IBOutlet var MusicOn: UIButton!; @IBOutlet var MusicOff: UIButton!; @IBOutlet var MusicBG: UIButton!;
    @IBOutlet var easyButton: UIButton!; @IBOutlet var mediumButton: UIButton!; @IBOutlet var hardButton: UIButton!;
    

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        let buttons = [easyButton, mediumButton, hardButton]
        for i in 0...2 {
            buttons[i]!.titleLabel!.lineBreakMode = .byWordWrapping
            let bestTime = myModel!.bestScore[i][2] == Int.max ? 0 : myModel!.bestScore[i][2]
            let wantedText = "Regular: \(myModel!.bestScore[i][0])/\([4,9,16][i]) in \(bestTime)s\nOrder: \(myModel!.bestScore[i+3][1])%"
            let states: [UIControl.State] = [.normal, .highlighted, .selected, .disabled]
            for state in states {
                buttons[i]!.setTitle(wantedText, for: state)
            }
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        self.appDelegate = UIApplication.shared.delegate as? AppDelegate
        self.myModel = self.appDelegate?.myModel
        randomDiffOn(self)
        soundEffectsOn(self)
        rememberOrderOff(self)
        musicOn(self)
        
    }
    
    @IBAction func easyMode(_ sender: Any) {
        self.myModel!.setDifficulty(Difficulty: 1)
        self.saveData()
    }
    @IBAction func mediumMode(_ sender: Any) {
        self.myModel!.setDifficulty(Difficulty: 2)
        self.saveData()
    }
    @IBAction func hardMode(_ sender: Any) {
        self.myModel!.setDifficulty(Difficulty: 3)
        self.saveData()
    }
    
    // Sets colors and values for on / off switches
    @IBAction func randomDiffOff(_ sender: Any) {
        RandDiffOff.tintColor = UIColor.red
        RandDiffOn.tintColor = UIColor.black
        RandDiffBG.tintColor = UIColor.red
        self.myModel!.setRandomDiff(value: false)
    }
    @IBAction func randomDiffOn(_ sender: Any) {
        RandDiffOff.tintColor = UIColor.white
        RandDiffOn.tintColor = UIColor.green
        RandDiffBG.tintColor = UIColor.green
        self.myModel!.setRandomDiff(value: true)
    }
    @IBAction func soundEffectsOff(_ sender: Any) {
        sfxOff.tintColor = UIColor.red
        sfxOn.tintColor = UIColor.black
        sfxBG.tintColor = UIColor.red
        self.myModel!.setSoundEffects(value: false)
    }
    @IBAction func soundEffectsOn(_ sender: Any) {
        sfxOff.tintColor = UIColor.white
        sfxOn.tintColor = UIColor.green
        sfxBG.tintColor = UIColor.green
        self.myModel!.setSoundEffects(value: true)
    }
    @IBAction func rememberOrderOff(_ sender: Any) {
        OrderOff.tintColor = UIColor.red
        OrderOn.tintColor = UIColor.black
        OrderBG.tintColor = UIColor.red
        self.myModel!.setRememberOrder(value: false)
    }
    @IBAction func rememberOrderOn(_ sender: Any) {
        OrderOff.tintColor = UIColor.white
        OrderOn.tintColor = UIColor.green
        OrderBG.tintColor = UIColor.green
        self.myModel!.setRememberOrder(value: true)
    }
    @IBAction func musicOff(_ sender: Any) {
        MusicOff.tintColor = UIColor.red
        MusicOn.tintColor = UIColor.black
        MusicBG.tintColor = UIColor.red
        self.myModel!.setMusic(value: false)
    }
    @IBAction func musicOn(_ sender: Any) {
        MusicOff.tintColor = UIColor.white
        MusicOn.tintColor = UIColor.green
        MusicBG.tintColor = UIColor.green
        self.myModel!.setMusic(value: true)
    }
    
    func saveData() {
        let context = appDelegate?.container.mainContext
        do {
            try context?.save()  // Persist the updated model
        } catch {
            print("Failed to save updated difficulty: \(error)")
        }
    }

}
