import hangman_helper as hh


def update_word_pattern(word, pattern, letter):
    """
    :param word: the current word
    :param pattern: the current pattern
    :param letter: letter picked by user
    :return: updated pattern
    """
    pattern = list(pattern)
    for i in range(len(word)):
        if letter == word[i]:
            pattern[i] = word[i]
    return "".join(pattern)


# word = "apple"
# ette = "p"
# a= "_____"
#
# pattern = update_word_pattern(word, a, ette)
# print(pattern)
# print(update_word_pattern(word,pattern,"e"))

def filter_words_list(words_list, pattern, wrong_guess_lst):
    """
    filter words from text file that match pattern
    :param words_list: words.txt file
    :param pattern: current pattern
    :param wrong_guess_lst: list of wrong guesses
    :return: list with words matching the pattern
    """
    filter1 = []
    filter2 = []
    hints = []
    # match pattern length to words
    for i in words_list:
        if len(pattern) == len(i):
            filter1.append(i)
    
    # remove words with wrong letters
    for i in range(len(filter1)):
        q = any(j in filter1[i] for j in wrong_guess_lst)
        if q == False:
            filter2.append(filter1[i])
    
    # match exposed letters to filter2 words
    for i in range(len(filter2)):
        booles = [False] * len(filter2[i])
        for j in range(len(filter2[i])):
            if pattern[j] == "_":
                booles[j] = True
            elif pattern[j] == filter2[i][j]:
                booles[j] = True
            else:
                booles[j] = False
        if False not in booles:
            hints.append(filter2[i])
    return hints


def run_single_game(list_words, score):
    """
    
    :param list_words: list of words from txt file
    :param score: current score, initially 10
    :return: score at end of game
    """
    # initialize game
    picked_word = hh.get_random_word(list_words)
    pattern = "_" * len(picked_word)
    # score += hh.POINTS_INITIAL  # ???
    wrong_guess_lst = []
    msg = "hi! welcome to Hangman Game!"
    hh.display_state(pattern, wrong_guess_lst, score, msg)
    input = hh.get_input()
    while score > 1 or picked_word != pattern:
        
        match input[0]:
            
            
            case 1:
                if len(input[1]) == 0 or len(input[1]) > 1 or input[1].isupper():
                    msg = "invalid input! pick something else or use lowercase"
                    hh.display_state(pattern, wrong_guess_lst, score, msg)
                
                elif input[1] in pattern or input[1] in wrong_guess_lst:
                    msg = "already picked letter"
                    hh.display_state(pattern, wrong_guess_lst, score, msg)
                
                
                else:  # valid letter
                    
                    score -= 1
                    if score == 0:
                        # hh.display_state((pattern, wrong_guess_lst, score, "you lose!"))
                        return score
                    count_letters = 0
                    for i in picked_word:
                        if input[1] == i:  # check if user input letter is same in picked_word
                            count_letters += 1
                    if count_letters > 0:  # update pattern if the letter exists
                        score = score + count_letters * (count_letters + 1) // 2
                        pattern = update_word_pattern(picked_word, pattern, input[1])
                        hh.display_state(pattern, wrong_guess_lst, score, "")
                    else:
                        wrong_guess_lst.append(input[1])
                        hh.display_state(pattern, wrong_guess_lst, score, "")
                    if pattern == picked_word:
                        # hh.display_state(pattern, wrong_guess_lst, score, "you won!")
                        return score
            
            case 2:
                score -= 1
                if input[1] == picked_word:
                    
                    count_blanks = 0
                    for i in range(len(picked_word)):
                        if picked_word[i] != pattern[i]:
                            count_blanks += 1
                    score = count_blanks * (count_blanks + 1) // 2
                    return score
                else:
                    
                    msg = "wrong!"
                    if score != 0:
                        hh.display_state(pattern, wrong_guess_lst, score, msg)
                    else:
                        return score
            
            case 3:
                score -= 1
                hints = []
                full_hints = filter_words_list(list_words, pattern, wrong_guess_lst)
                if len(full_hints) > hh.HINT_LENGTH:
                    for i in range(1, hh.HINT_LENGTH + 1):
                        hint_index = ((i - 1) * len(full_hints) // hh.HINT_LENGTH)
                        hints.append(full_hints[hint_index])
                    hh.show_suggestions(hints)
                else:
                    hh.show_suggestions(full_hints)
                
                # hh.play_again(msg="you lose! ")
        input = hh.get_input()
        if score == 0:
            
            return score


def main():
    words_list = hh.load_words()
    score = 0
    score = score + hh.POINTS_INITIAL
    num_of_games = 0
    play = True
    score = run_single_game(words_list, score)
    while play:
        num_of_games += 1
        if num_of_games > 1:
            s = "s"
        else:
            s = ""
        if score > 0:
            play = hh.play_again(
                f'You played {num_of_games} game{s} so far and you have {score} points. Do you want to keep playing?')
            if play == True:
                score = run_single_game(words_list, score)
            else:
                return
        elif hh.play_again(f'You managed to play {num_of_games} game{s}. Well Done! Do you want to play again?'):
            num_of_games = 0
            score = run_single_game(words_list, hh.POINTS_INITIAL)
        else:
            continue


if __name__ == "__main__":
    main()
