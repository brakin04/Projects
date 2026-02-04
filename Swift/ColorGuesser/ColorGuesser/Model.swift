//
//
//  Bryan Akin brakin
//  Briana Flores briflore
//  Submission date: 5/7/25
//
//  Model.swift
//  ColorGuesser
//
//  Created by Akin, Bryan on 4/18/25.
//

import UIKit
import SwiftData

@Model
class Model {
    
    @Transient private var randomDiff = true
    @Transient private var soundEffects = true
    @Transient private var music = true
    @Transient var rememberOrder = false
    
    // to keep track of if its been played or not
    @Transient var played = false
    
    // first 3 are regular last 3 are memory game first is amount second is percent
    var bestScore: [[Int]] = [[Int]](repeating: [0,0,Int.max], count: 6)
    
    var difficulty: Int = 2
    
    @Transient var colors = [UIColor.red, UIColor.blue, UIColor.green, UIColor.orange, UIColor.systemPink, UIColor.yellow, UIColor.black, UIColor.white, UIColor.purple, UIColor.gray]
    
    @Transient var board = [UIColor.red]
    @Transient var order = [-1]
    
    // init for swiftData
    init(bestScore: [[Int]] = [[Int]](repeating: [0,0,Int.max], count: 6), difficulty: Int = 2) {
        self.bestScore = bestScore
        self.difficulty = difficulty
    }
    
    // set the difficulty
    func setDifficulty(Difficulty: Int) {
        self.difficulty = Difficulty
        self.initBoard()
    }
    
    // Initialize the board
    func initBoard() {
        self.board = []
        
        // determines the size of the board
        if randomDiff && !played {
            self.difficulty = [1,2,3].randomElement()!
        }
        let slots = [3,8,15][self.difficulty-1]
        // adds random colors from the colors array
        for _ in 0...slots {
            self.board.append(colors.randomElement()!)
        }
        // if memory is on, give an array to show the order
        if rememberOrder {
            self.order = Array(0...slots).shuffled()
        }
        self.played = true
    }
    
    // gets players score
    func submit(answer: [UIColor], inOrder: [Int], time: Int) -> [Int] {
//        print("Order was \(self.order)\nSelected was \(inOrder)")
        let size = [3,8,15][self.difficulty-1]
        var score = 0
        if rememberOrder {
            for i in 0...min(self.order.count, inOrder.count)-1 {
                if answer[inOrder[i]] == self.board[inOrder[i]] && inOrder[i] == self.order[i] {
                    score += 1
                } else {
                    break
                }
            }
        } else {
            for i in 0...size {
                if answer[i] == self.board[i] {
                    score += 1
                }
            }
        }
        let percentage = Double(score) / Double(size+1) * 100
        let percent = Int(percentage.rounded())
        self.checkForBestScore(score: score, percent: percent, time: time)
        return [score, size+1, percent]
    }
    
    
    // updates best scores array
    func checkForBestScore(score: Int, percent: Int, time: Int) {
//        print("checked best score with: \(score), \(percent), \(time)")
        var idx = self.difficulty-1
        if rememberOrder {
            idx += 3
        }
        if self.bestScore[idx][0] <= score {
            self.bestScore[idx][0] = score
            self.bestScore[idx][1] = percent
            if (self.bestScore[idx][0] == score) {
                if  self.bestScore[idx][2] > time {
//                    print("Time was added")
                    self.bestScore[idx][2] = time
                }
            } else {
                self.bestScore[idx][2] = time
            }
        }
    }
    
    // setter methods
    func setRandomDiff(value: Bool) {
        self.randomDiff = value
    }
    func setSoundEffects(value: Bool) {
        self.soundEffects = value
    }
    func setRememberOrder(value: Bool) {
        self.rememberOrder = value
    }
    func setMusic(value: Bool) {
        self.music = value
    }
    
}
