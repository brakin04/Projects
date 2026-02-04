Created by: Bryan Akin and Briana Flores

Brief instructions:


	Start page:
	When the app is started you are loaded into the start screen where the start button
	starts the game. In the tab bar controller at the bottom, the first tab is the start 
	screen, second is the settings page, and third is the info page. 
	
	
	Settings page:
	On the button to the left of each difficulty the game will show your best scores for 
	both the memorize order portion of the game as well as the regular mode. To select a
	difficulty, click this button. For the other settings at the bottom, either click on 
	the black or white circle to turn it on/off (shown at the bottom). 
	
	
	Info page:
	This details why the game was created and contains a general description of it
	
	
	Game page:
	The time at the top counts down from 10 seconds if you're playing the normal mode or 
	5, 10, or 17 seconds for easy, normal, hard remember order modes. After this time is 
	up, the board clears and you can attempt to recreate it. To choose which color you 
	want to place on the grid, select a color from below "choose a color" and click on 
	the position in the grid where you would like to place it. When you are satisfied with
	your grid, click the submit button and you will see your best score for each mode for
	each difficulty displayed in a table view controller. To close this, drag down from the 
	top of the view. Use this same method if you would like to leave the game view as well.
	For the order memory portion of the game, you need to select the squares in the same 
	order that they were shown with the same color that they were shown as. At any point 
	during either mode, you can clear your board and start from scratch by shaking your 
	phone (this is more useful for the order memory because it resets the buttons you've
	clicked already).
	
	
Environment used:
	
	
		iOS 18.4; Swift 5; InfoDictionary version 6.0; XCode 16.2; 
		Hardware: iPhone 12, iOS 18.4, CoreMotion
	
	
What was used:


	GUI:
	Each view contains text (labels), and all but one contain buttons. We used UIKit, so 
	our project has 3 regular view controllers and a table view controller. 
	GameViewController.swift controls the game screen
	SettingsViewController.swift controls the setting screen
	StartViewController.swift controls the start screen
	TableViewController.swift controls the hi-scores table view
	
	
	Persistent local data storage:
	This was incorporated into the app using SwiftData. Parts of this can be found in: 
	AppDelegate.swift and Model.swift where it is used to save your best scores and your 
	desired difficulty.  
	
	
	iOS frameworks:
	Core Motion is used to determine if the phone is shaken in order to reset the board 
	and the input order array. Can be seen in GameViewController.swift.
	User Notifications are used to congratulate you on your score when you submit and 
	are posted 15s after the game starts to let you know that you can shake the phone to 
	reset the board. Can be seen in AppDelegate.swift, SettingsViewController.swift, 
	GameViewController.swift, and NotificationManager.swift.
	Swift data is used to store the best scores and your desired difficulty. It can be 
	seen implemented in both Model.swift and AppDelegate.swift