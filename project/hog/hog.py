
"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return the
    number of 1's rolled.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    "*** REPLACE THIS LINE ***"
    score, appear_1 = 0, 0             #int var for has 1 and sum of the score
    while num_rolls > 0:               #loop until no more roll
        cur_roll = dice()
        if cur_roll == 1:              #test if current roll is 1
            appear_1 += 1
        score += cur_roll              #add current roll to total score
        num_rolls -= 1
    if appear_1:                       #if 1 appears, return number of times 1 appeared
        return appear_1
    return score                       #return score if there's no 1 in the rolls
    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    "*** REPLACE THIS LINE ***"
    return max(opponent_score%10, (opponent_score//10) % 10) + 1  #free bacon rules, return the max of 2 digits of opponent's score + 1
    # END PROBLEM 2


# Write your prime functions here!
def is_prime(score):
    if score <= 1:              #if the score <= 1, not prime
        return False
    count = 2
    while count*count <= score:     #loops until count equals to score, count starts at 2
        if score % count == 0:      #if score can be divided by count, return not prime (False)
            return False
        count += 1
    return True                 #return True when loop ends, which means score is prime

def next_prime(cur_prime):
    assert type(cur_prime) == int, 'Prime number has to be an integer'
    assert cur_prime > 1, 'Prime number has to be larger than 1'
    next_prime = cur_prime + 1
    while not is_prime(next_prime):       #loops until found the next prime
        next_prime += 1                   #increment of next_prime after the loop
    return next_prime

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime and When Pigs Fly rules.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    "*** REPLACE THIS LINE ***"
    score = 0
    if num_rolls == 0:                      #when player choose 0 roll, free bacon rule apllies
        score = free_bacon(opponent_score)
    else:
        score = roll_dice(num_rolls, dice)  #else, roll the dice normally     
    if is_prime(score):                     #if the score is prime, the score will become the next prime number
        score = next_prime(score)
    return min(score, 25 - num_rolls)       #return the minimum between the score and the limit score for the turn
    # END PROBLEM 2


def reroll(dice):
    """Return dice that return even outcomes and reroll odd outcomes of DICE."""
    def rerolled():
        # BEGIN PROBLEM 3
        "*** REPLACE THIS LINE ***"
        cur_score = dice()          #get the first roll
        if cur_score % 2:           #if the first roll is odd, roll again and get the second roll
            cur_score = dice()
        return cur_score            #return the roll at the end
        # END PROBLEM 3
    return rerolled


def select_dice(score, opponent_score, dice_swapped):
    """Return the dice used for a turn, which may be re-rolled (Hog Wild) and/or
    swapped for four-sided dice (Pork Chop).

    DICE_SWAPPED is True if and only if four-sided dice are being used.
    """
    # BEGIN PROBLEM 4
    "*** REPLACE THIS LINE ***"
    #dice = six_sided  # Replace this statement
    if dice_swapped:                #if DICE_SWAPPED is True, dice is four_sided; else, dice is six_sided
        dice = four_sided
    else:
        dice = six_sided
    # END PROBLEM 4
    if (score + opponent_score) % 7 == 0:
        dice = reroll(dice)
    return dice


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    dice_swapped = False  # Whether 4-sided dice have been swapped for 6-sided
    # BEGIN PROBLEM 5
    "*** REPLACE THIS LINE ***"
    def playing(strategy, score, opponent_score, dice_swapped):         #function to perform the game play
        num_rolls = strategy(score, opponent_score)             #calculate number of rolls
        if num_rolls == -1:                                     #if numrolls == -1, change dice_swapped and add 1 to currrent player's score
            dice_swapped = not dice_swapped
            score += 1
        else:                                                   #else, call take turn and add the score to current player's score
            score += take_turn(num_rolls, opponent_score, select_dice(score, opponent_score, dice_swapped))
        return score, dice_swapped                              #return both new score and DICE_SWAPPED
    while max(score1, score0) < goal:                           #loops until one player reaches the goal score
        if player:                                              #if player is player 1, call PLAYING function for player 1
            score1, dice_swapped = playing(strategy1, score1, score0, dice_swapped)
        else:                                                   #else, player is player 0, call PLAYING for player 0
            score0, dice_swapped = playing(strategy0, score0, score1, dice_swapped)            
        if score0 == 2*score1 or score1 == 2*score0:            #if one player's score is double the other's, SWINE_SWAP rule applies
            temp = score0                                       #switch the 2 players' scores
            score0 = score1
            score1 = temp
        player = other(player)                                  #change player
    # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
    # BEGIN PROBLEM 11
        if score == 0:                                      #change to four_sided dice when it is the first turn
            return -1
        diff = opponent_score - score
        margin, num_rolls = 7, 4   
        score_attained = free_bacon(opponent_score)         #find the score for free bacon
        if is_prime(score_attained):                        #if the score is prime number, get the next prime number
            score_attained = next_prime(score_attained)
        if opponent_score == 2*(score + score_attained):    #if the new score is half opponent's score, force the swap
            return 0
        if (score + score_attained + opponent_score) % 7 == 0 and diff > 0:             #at the end of the turn if opponent can reroll_dice, avoid it 
            return num_rolls                                                                #with rolling default number of roll
        
        if score_attained >= margin and 2*opponent_score != (score + score_attained):   #if our score is twice the opponet's when zero is returned, aviod it. 
            return 0                                                                    #when we are able to get highr score than margin by free_bacon, take advantage
        
        if diff < -20:
            return 3
        if diff > 20:
            return 6
        return num_rolls 
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert -1 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the
    strategy returns a valid input. Use `check_strategy_roll` to raise
    an error with a helpful message if the strategy returns an invalid
    output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6
    "*** REPLACE THIS LINE ***"
    for score0 in range(0, goal):         #iterate score0 from 0 to goal - 1
        for score1 in range(0, goal):     #iterate score1 form 0 to goal - 1
            check_strategy_roll(score0, score1, strategy(score0, score1))
    return None
    # END PROBLEM 6


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    """
    # BEGIN PROBLEM 7
    "*** REPLACE THIS LINE ***"
    def average_assist(*args):
        total = 0
        for num in range(0, num_samples): #loops as many times as the num_samples
            total += fn(*args)            #add the result every time to total
        return total/num_samples          #take average
    return average_assist
    # END PROBLEM 7

def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN PROBLEM 8
    "*** REPLACE THIS LINE ***"
    count, cur_high, should_rolls = 1, 0, 0
    while count < 11:                       #loops until the num_rolls gets higher than 10
        cur_score = make_averaged(roll_dice, num_samples)(count, dice)  #calculate average score for a specific roll
        if cur_score > cur_high:            #check if the score calculated is higher than the previous trials
            should_rolls = count            #if higher, set the rolls to count and the high_score to the current roll score
            cur_high = cur_score
        count += 1
    return should_rolls
    # END PROBLEM 8


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


#def average_win_rate(strategy, baseline=always_roll(4)):
def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        rerolled_max = max_scoring_num_rolls(reroll(six_sided))
        print('Max scoring num rolls for re-rolled dice:', rerolled_max)

    if False:  # Change to False when done finding max_scoring_num_rolls
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)
        rerolled_max = max_scoring_num_rolls(reroll(four_sided))
        print('Max scoring num rolls for re-rolled dice:', rerolled_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(4)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True:  # Change to True to test swap_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 9
    "*** REPLACE THIS LINE ***"
    score_attained = free_bacon(opponent_score)         #find the score for free bacon
    if is_prime(score_attained):                        #if it's prime, it will become the next prime number
        score_attained = next_prime(score_attained)
    if score_attained >= margin:                        #check if that score is at least margin point, return 0 if true
        return 0
    return num_rolls  # Replace this statement
    # END PROBLEM 9
check_strategy(bacon_strategy)

def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 10
    "*** REPLACE THIS LINE ***"
    score_attained = free_bacon(opponent_score)         #find the score for free bacon
    if is_prime(score_attained):                        #if it's prime, it will become the next prime number
        score_attained = next_prime(score_attained)
    if opponent_score == 2*(score + score_attained):    #if opponent's score is double current score, should swap, return 0
        return 0
    if score_attained >= margin and 2*opponent_score != (score + score_attained): #check if new score is at least margin point 
        return 0                                                                  #and our score is not the double of opponent's 
    return num_rolls  # Replace this statement
    # END PROBLEM 10
check_strategy(swap_strategy)


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    Statistically rolling 4 sided dice give higher rate of returning lower scores. 
    Therefore if we use the four sided dice, the game progresses slower than using six sided dice. 
    When the game progresses slowly, it is our advantage because we have more chance to apply the Free Bacon rule through out the game. 
    So we always want to use four sided dice. 
    We want to force the Swap when we are guaranteed for Swap. 
    This only happens when we can predict the next score which is the case when we use the Free Bacon rule. 
    Also we want to prevent our opponent from swapping when we are able to control it. 
    """
    # BEGIN PROBLEM 11
    "*** REPLACE THIS LINE ***"
    # # if score == 0:                                      #change to four_sided dice when it is the first turn
    #     return -1
    diff = opponent_score - score
    margin, num_rolls = 7, 5 
    score_attained = free_bacon(opponent_score)         #find the score for free bacon
    if is_prime(score_attained):                        #if the score is prime number, get the next prime number
        score_attained = next_prime(score_attained)
    if opponent_score == 2*(score + score_attained):    #if the new score is half opponent's score, force the swap
        return 0
    if (score + score_attained + opponent_score) % 7 == 0 and diff > 0:             #at the end of the turn if opponent can reroll_dice, avoid it 
        return num_rolls                                                                #with rolling default number of roll
    
    if score_attained >= margin and 2*opponent_score != (score + score_attained):   #if our score is twice the opponet's when zero is returned, aviod it. 
        return 0                                                                    #when we are able to get highr score than margin by free_bacon, take advantage
    
    if diff < -20:
        return 3
    if diff > 20:
        return 6
    return num_rolls                                                                #return default
    # END PROBLEM 11
check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()




