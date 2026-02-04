//
//  Bryan Akin brakin
//  Briana Flores briflore
//  Submission date: 5/7/25
//
//  AppDelegate.swift
//  ColorGuesser
//
//  Created by Akin, Bryan on 4/18/25.
//

import UIKit
import UserNotifications
import SwiftData

@main
class AppDelegate: UIResponder, UIApplicationDelegate, UNUserNotificationCenterDelegate {
    
    // container for model
    var container: ModelContainer!
    
    // reference to model instance
    var myModel: Model!
    
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        // initialize the SwiftData container for model class
        do {
            // create SwiftData container
            container = try ModelContainer(for: Model.self)
            let context = container.mainContext
            
            // correct usage of FetchDescriptor
            let descriptor = FetchDescriptor<Model>()
            let savedModels = try context.fetch(descriptor)
            
            if let saved = savedModels.first {
                myModel = saved
                
            } else {
                // if no saved model create a new one with default values
                myModel = Model()
                context.insert(myModel)
            }
            
            // save context to ensure persistence
            try context.save()
            
        } catch {
            print("Failed to load model container: \(error)")
        }
        // override point for customization after application launch.
        let center = UNUserNotificationCenter.current()
        center.delegate = self
        center.requestAuthorization(options: [.alert, .sound, .badge]) { granted, error in
            print("Notification permission granted? \(granted)")
            if let error { print(error) }
        }
        
        return true
    }
    
    func schedulePing(after seconds: TimeInterval = 25) {
        UNUserNotificationCenter.current().getNotificationSettings { settings in
            guard settings.authorizationStatus == .authorized else {
                print("Skipping ping – user hasn’t allowed notifications")
                return
            }
            
            let content = UNMutableNotificationContent()
            content.title = "Stuck?"
            content.body  = "Shake to reset the grid"
            content.sound = .default
            
            let trigger = UNTimeIntervalNotificationTrigger(timeInterval: seconds, repeats: false)
            let request = UNNotificationRequest(identifier: "fifteenSecondPing",
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
        
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                    willPresent notification: UNNotification,
                                    withCompletionHandler completion: @escaping (UNNotificationPresentationOptions) -> Void) {
        completion([.banner, .sound])
    }
        
        
    func application(_ application: UIApplication,
                    configurationForConnecting connectingSceneSession: UISceneSession,
                    options: UIScene.ConnectionOptions) -> UISceneConfiguration {
        UISceneConfiguration(name: "Default Configuration",
                            sessionRole: connectingSceneSession.role)
    }
}
