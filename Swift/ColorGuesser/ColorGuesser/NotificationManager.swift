//
//
//  Bryan Akin brakin
//  Briana Flores briflore
//  Submission date: 5/7/25
//
//  UserNotifications.swift
//  ColorGuesser
//
//  Created by Briana Flores on 4/28/2025.
//

import UIKit
import UserNotifications

class UserNotificationsViewController: UIViewController{
    let popupButton: UIButton = {
        let button = UIButton(type: .system)
        button.setTitle("Popup", for: .normal)
        button.titleLabel?.font = UIFont.boldSystemFont(ofSize: 17)
        button.backgroundColor = .systemBlue
        button.tintColor = .white
        button.layer.cornerRadius = 8
        button.isHidden = true
        return button
    }()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .white
        
        view.addSubview(popupButton)
        
        popupButton.frame = CGRect(x:50, y:200, width: view.frame.width - 100, height: 50)
        
        popupButton.addTarget(self, action: #selector(buttonTapped), for: .touchUpInside)
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            self.showPopupButton()
        }
    }
    
    @objc func showPopupButton() {
        popupButton.isHidden = false
        
        popupButton.alpha = 0
        UIView.animate (withDuration: 15) {
            self.popupButton.alpha = 1
        }
    }
    
    @objc func buttonTapped() {
        print("Button was Tapped!")
    }
    
    func scheduleFifteenSecondPing() {
        let content = UNMutableNotificationContent()
        content.title = "SHAKE to reset grid"
        content.body = "OK"
        content.sound = .default
        
        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 25, repeats: false)
        let request = UNNotificationRequest(
            identifier: "fifteenSecondPing",
            content: content,
            trigger: trigger)
        if let imageURL = Bundle.main.url(forResource: "gridImage", withExtension: "png") {
            do {
                let attachment = try UNNotificationAttachment(identifier: "image", url: imageURL, options: nil)
                content.attachments = [attachment]
            } catch {
                print("Failed to attach image: \(error)")
            }
        }
        UNUserNotificationCenter.current().add(request)
    }
}
        
final class NotificationManager {
    static let shared = NotificationManager()  
    public init() { }
            
    // ask once per launch; does nothing if already authorised
    func requestAuthorizationIfNeeded() {
        let center = UNUserNotificationCenter.current()
        center.getNotificationSettings { settings in
            guard settings.authorizationStatus == .notDetermined else { return }
            center.requestAuthorization(options: [.alert, .sound, .badge]) { _, _ in }
        }
    }
            
    // schedule a one‑off ping after *seconds*.
    func schedulePing(after seconds: TimeInterval = 15) {
        let content = UNMutableNotificationContent()
        content.title = "Stuck?"
        content.body  = "Shake to reset the grid"
        content.sound = .default
                    
        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: seconds,
                                                                repeats: false)
        let request = UNNotificationRequest(identifier: "fifteenSecondPing",
                                            content: content,
                                            trigger: trigger)
        UNUserNotificationCenter.current().add(request)
    }
}
