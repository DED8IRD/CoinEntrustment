"""
Game.py

This is a command-line Coin Entrustment game (a Prisoner's dilemma analogue) used as a measure of trust in the Trust in Agent Appearance-Voice Consistency study.
Note: Requires Windows to have sound integrated.

Created by Eunika Wu on 28 Feb, 2017.
"""
from __future__ import division
from Player import Player
from math import ceil
import argparse, os, winsound

parser = argparse.ArgumentParser(description="This is a command-line Coin Entrustment game (a Prisoner's dilemma analogue) with audio. To skip audio, run in silent mode --silent or -s")
parser.add_argument('-s', '--silent', help='Runs CEGame without audio', action='store_true')
args = parser.parse_args()

SILENT = args.silent
FORM_CONDITION = None
VOICE_CONDITION = None
PARTICIPANT = None
TRUST_SCORE = 0
COOPERATION_SCORE = 0
OPPONENT_SCORE = 0
AGENT_SCORE = 0
NUM_ROUNDS = 7


def get_condition(cond):
    while True:
        cond = raw_input("\n\t\tEnter " +cond+ " condition (H/R): ")
        cond = cond.strip().lower()
        if cond == 'h' or cond == 'human' or cond == 'humanoid':
            return 'HUMAN'
        elif cond == 'r' or cond == 'robot' or cond == 'machine' or cond == 'mechanoid':
            return 'ROBOT'
        else:
            print("\t\tInvalid. Answer (h/r)")


if SILENT:
    def play_audio(dir, file, caption=None):
        pass
else:
    def play_audio(dir, file, caption=None):
        if caption:
            print("\t\t" + caption + '\n')
        winsound.PlaySound(os.path.join(dir, file), winsound.SND_FILENAME)

def get_subject_entrustment():
    while True:
        coins = raw_input("\n\t\tEnter number of coins the subject entrusts: ")
        try:
            coins = int(coins)
            if (0 <= coins <= 10):
                print('\n')
                return coins
            print("\t\tInvalid. Number must be between 0 and 10.")
            play_audio(audio_dir, 'NUMERROR.wav')
        except ValueError:
            print("\t\tInvalid. Number must be between 0 and 10.")
            play_audio(audio_dir, 'NUMERROR.wav')


def get_subject_cooperation():
    while True:
        response = raw_input("\n\t\tDid the subject return your coins? (y/n): ")
        response = response.strip().lower()
        if response == 'y' or response == 'yes':
            print('\n')            
            return True
        elif response == 'n' or response == 'no':
            print('\n')            
            return False
        else:
            print("\t\tInvalid. Answer (y/n)")
            play_audio(audio_dir, 'YNERROR.wav')

def print_entrustment_prompt(round):
    wav = -1
    if ROUND == 1:
        wav = 1
    elif 1 < ROUND < 7: 
        wav = 3
    elif ROUND == 7:
        wav = 4
    caption = '****Play the round introduction audio \'' +str(wav)+ '.wav\'****'
    play_audio(audio_dir, str(wav) + '.wav', caption)


def print_scores():
    if OPPONENT_SCORE > AGENT_SCORE:
        winner = 'SUBJECT'
    elif OPPONENT_SCORE == AGENT_SCORE:
        winner = 'BOTH OF YOU: IT\'S A TIE'
    else:
        winner = 'AGENT'

    participant_info = ('-'*80
                     + '\nPARTICIPANT: ' + PARTICIPANT
                     + '\nFORM CONDITION: ' + FORM_CONDITION
                     + '\nVOICE CONDITION: ' + VOICE_CONDITION
                     + '\n' + '-'*80 + '\n')

    out = ('\n' + '-'*80
        + '\n\tTHE WINNER IS ' + winner
        + '\n' + '-'*80 + '\n'
        + '\n\t\tSUBJECT SCORE: ' + str(OPPONENT_SCORE)
        + '\n\t\tAGENT SCORE: ' + str(AGENT_SCORE)
        + '\n\n\t\tSUBJECT TRUST SCORE: ' + str(TRUST_SCORE)
        + '\n\t\tSUBJECT COOPERATION SCORE: ' + str(COOPERATION_SCORE) +'\n')

    scoredest = os.path.join(os.getcwd(), 'Scores', PARTICIPANT + '.score')
    with open(scoredest, 'w') as outfile:
        outfile.write(participant_info)
        outfile.write(out)
        outfile.write('\n')
        outfile.write('Agent\n')
        outfile.write(str(agent))
        outfile.write('\n\n')     
        outfile.write('Subject\n')
        outfile.write(str(subject)) 

    print(out + '\n\n')
    return winner


if __name__ == '__main__':
    ROUND = 1
    agent = Player()
    subject = Player()
    defected = False
    prev_payoff = 0

    print('-'*80)
    print('\tThis is the Coin Entrustment Game.')
    print('\n\tYou are the operator of this game. As operator, you will embody a 3d' \
        + '\n\tavatar agent named Rovy. You will \"play\" a game with the participant' \
        + '\n\tas the avatar through a video call. To \"play\" the command-line game,' \
        + '\n\tsimply follow the prompts and record the participant\'s inputs.')
    print('-'*80)

    FORM_CONDITION = get_condition('form')
    VOICE_CONDITION = get_condition('voice')
    PARTICIPANT = raw_input("\n\t\tEnter participant: ")

    if VOICE_CONDITION == 'HUMAN':
        audio_dir = os.path.join(os.getcwd(), 'Human audio')
        coins_dir = os.path.join(os.getcwd(), 'Human audio', 'coins')
    elif VOICE_CONDITION == 'ROBOT':
        audio_dir = os.path.join(os.getcwd(), 'Robot audio')
        coins_dir = os.path.join(os.getcwd(), 'Robot audio', 'coins')

    raw_input("\n\t\tPress ENTER to start\n")
    caption = '****Play introduction audio \'0.wav\'****'
    play_audio(audio_dir, '0.wav', caption)
    raw_input("\t\tPress ENTER to continue")

    while ROUND <= NUM_ROUNDS:
        print('\n' + '-'*80)
        print('\tROUND ' + str(ROUND))
        print('-'*80 + '\n')

        agent.coins.append(10)
        subject.coins.append(10)

        # Entrustment phase
        print_entrustment_prompt(ROUND)
        if ROUND == 1:
            agent.entrust(subject, 3)
        else:
            if defected:
                agent.entrust(subject, 1)
            elif prev_payoff > 0:
                agent.entrustment = (ceil(10 + (prev_payoff - 10) / 1.5))  
                agent.entrust(subject, min(agent.entrustment, 10))
            else:
                agent.entrust(subject, max(1, 10 + prev_payoff))

        subject_entrust_coins = get_subject_entrustment()
        subject.entrust(agent, subject_entrust_coins)
        
        caption = '****Play entrustment audio \'9.1.wav\'****'
        play_audio(audio_dir, '9.1.wav', caption)
        caption = '****Play coins \'' +str(agent.trust[-1])+ '.wav\'****'
        play_audio(coins_dir, str(agent.trust[-1]) + '.wav', caption)
        print('\t\t'+'-'*45+'\n')

        # Cooperation phase
        caption = '****Play cooperation prompt audio \'2\'****'
        play_audio(audio_dir, '2.wav', caption)
        subject_cooperates = get_subject_cooperation()

        if subject_cooperates:
            subject.cooperate(agent)
        else:
            subject.defect(agent)

        if sum(subject.coop[-2:]) < 2 and len(subject.coop) > 1:
            defected = True
        else:
            defected = False

        if not defected:
            agent.cooperate(subject)
            caption = '****Play cooperate audio \'9.2.wav\'****'
            play_audio(audio_dir, '9.2.wav', caption)

        else:
            agent.defect(subject)
            caption = '****Play defect audio \'9.3.wav\'****'
            play_audio(audio_dir, '9.3.wav', caption)

        prev_payoff = sum(agent.coins[ROUND*5-4:ROUND*5])
        print('\n\t\tROUND ' +str(ROUND)+ ' RESULTS: ' \
            + '\tSUBJECT: ' +str(subject.get_score()) \
            + '\tAGENT: ' +str(agent.get_score())+ '\n')
        ROUND += 1

    OPPONENT_SCORE = subject.get_score()
    AGENT_SCORE = agent.get_score()
    TRUST_SCORE = subject.get_trust_score(NUM_ROUNDS)
    COOPERATION_SCORE = subject.get_coop_score(NUM_ROUNDS)

    winner = print_scores()
    caption = '****Play end of game audio****'
    play_audio(audio_dir, '5.wav', caption)

    # play_audio(audio_dir, '6.1.wav')
    # raw_input("\n\t\tEnter participant score into TTS. Participant score: " + str(OPPONENT_SCORE) \
    #         + "\n\t\t Press any key to continue." )
    # play_audio(audio_dir, '6.2.wav')
    # raw_input("\n\t\tEnter the agent score into TTS. Your score: " + str(AGENT_SCORE) \
    #         + "\n\t\t Press any key to continue." )

    caption = '****If AGENT wins, play wav \'7.wav\' else play \'8.wav\'****'
    if winner == 'AGENT':
        play_audio(audio_dir, '7.wav', caption)
    elif winner == 'SUBJECT':
        play_audio(audio_dir, '8.wav', caption)
