//
//  Bryan Akin brakin
//  Briana Flores briflore
//  Submission date: 5/7/25
//
//  AudioManager.swift
//  ColorGuesser
//
//  Created by Briana Flores on 5/6/2025.
//


import AVFoundation

final class AudioManager {

    static let shared = AudioManager()
    private var player: AVAudioPlayer?

    private init() {

        try? AVAudioSession.sharedInstance().setCategory(.ambient, mode: .default, options: [.mixWithOthers])
        try? AVAudioSession.sharedInstance().setActive(true)
    }

    func startBackgroundMusic(looped: Bool = true, volume: Float = 0.6) {
        guard player == nil else { return }                   
        guard let url = Bundle.main.url(forResource: "backgroundMusic", withExtension: "mp3") else {
            print("‼️ backgroundMusic.mp3 not found"); return
        }
        do {
            player = try AVAudioPlayer(contentsOf: url)
            player?.numberOfLoops = looped ? -1 : 0            // -1 == infinite loop
            player?.volume = volume
            player?.prepareToPlay()
            player?.play()
        } catch {
            print("Audio error: \(error)")
        }
    }

    // when you want to silence music 
    func stopBackgroundMusic() {
        player?.stop()
        player = nil
    }
}
