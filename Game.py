"""
Game.py

This is a command-line Coin Entrustment game (a Prisoner's dilemma analogue) used as a measure of trust in the Trust in Agent Appearance-Voice Consistency study.

Created by Eunika Wu on 28 Feb, 2017.
"""
from __future__ import division
from Player import Player
from math import ceil

PARTICIPANT = None
TRUST_SCORE = 0
COOPERATION_SCORE = 0
OPPONENT_SCORE = 0
AGENT_SCORE = 0
NUM_ROUNDS = 5

def get_subject_entrustment():
    while True:
        coins = raw_input("\n\t\tEnter number of coins the subject entrusts: ")
        try:
            coins = int(coins)
            if (0 <= coins <= 10):
                return coins
            print("\t\tInvalid. Number must be between 0 and 10.")                
        except ValueError:
            print("\t\tInvalid. Number must be between 0 and 10.")

def get_subject_cooperation():
    while True:
        response = raw_input("\t\tDid the subject return your coins? (y/n): ")
        response = response.strip().lower()
        if response == 'y' or response == 'yes':
            return True
        elif response == 'n' or response == 'no':
            return False
        else:
            print("Invalid. Answer (y/n)")

def print_scores():
    out = ('-'*80
          + '\n\tTHE WINNER IS THE ' 
          + ('SUBJECT ' + PARTICIPANT if OPPONENT_SCORE > AGENT_SCORE else 'AGENT') 
          + '\n' + '-'*80 + '\n'
          + '\n\t\tSUBJECT SCORE: ' + str(OPPONENT_SCORE)
          + '\n\t\tAGENT SCORE: ' + str(AGENT_SCORE)
          + '\n\n\t\tSUBJECT TRUST SCORE: ' + str(TRUST_SCORE)
          + '\n\t\tSUBJECT COOPERATION SCORE: ' + str(COOPERATION_SCORE) +'\n'
          )

    with open(PARTICIPANT +'.score', 'w') as outfile:
        outfile.write(out)
        outfile.write('\n')
        outfile.write('Agent\n')
        outfile.write(str(agent))
        outfile.write('\n\n')     
        outfile.write('Subject\n')
        outfile.write(str(subject)) 

    print(out)


if __name__ == '__main__':
    ROUND = 1
    agent = Player()
    subject = Player()
    defected = False
    prev_payoff = 0

    print('-'*80)
    print('\tThis is the Coin Entrustment Game.')
    print('-'*80)

    PARTICIPANT = raw_input("\tEnter participant: ")

    while ROUND <= NUM_ROUNDS:
        print('-'*80)
        print('\tROUND ' + str(ROUND))
        print('-'*80)

        agent.coins.append(10)
        subject.coins.append(10)
        if sum(subject.coop[-2:]) < -1:
            defected = True

        # Entrustment phase
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

        # Cooperation phase
        if not defected:
            agent.cooperate(subject)
        else:
            agent.defect(subject)

        subject_cooperates = get_subject_cooperation()
        if subject_cooperates:
            subject.cooperate(agent)
        else:
            subject.defect(agent)
        prev_payoff = sum(agent.coins[ROUND*5-4:ROUND*5])
        ROUND += 1
        print('\n')

    OPPONENT_SCORE = subject.get_score()
    AGENT_SCORE = agent.get_score()
    TRUST_SCORE = subject.get_trust_score(NUM_ROUNDS)
    COOPERATION_SCORE = subject.get_coop_score(NUM_ROUNDS)

    print_scores()




