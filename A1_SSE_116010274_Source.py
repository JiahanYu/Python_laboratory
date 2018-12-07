import sys
import random

g_target = '0000'
g_fix_num = ''

def is_valid_number(number):
    return number.isdigit() and len(number) == 4 and len(set(number)) == 4

def target_number():
    target = ''.join(random.sample('0123456789',4))
    return target
    
def check_correct(p_target,p_number):
    guess_correct,guess_position = 0,0
    for i in range(0,4):
        if p_target[i] == p_number[i]:
            guess_correct += 1
        if p_target.find(p_number[i]) != -1:
            guess_position += 1
    return guess_correct, guess_position - guess_correct

def game(target):
    count = 1
    result = ''
    while count <= 8:
        number = input('Your Guess %d/8 : '%count)
        if is_valid_number(number):
            result += '{} : Correct : {} Position : {}'.format(number, *check_correct(g_target,number)) + '\n'
            if number == target:
                result += 'Congratulations !! Number : {}'.format(target)
                print(result)
                break
            if count == 8:
                result += 'Game is over !! Number : {}'.format(target)
            print(result)
            count += 1
        else:
            print('Please enter a 4-digit number with no repeated digits\n')

def startup(show): 
    global g_target
    while True:
        g_target = target_number()
        if show:
            if sys.argv[1] == 'fix':
                g_target = g_fix_num
            print(g_target)
        command = input('Game? (y/n) >')
        if command.lower() == 'y':
            game(g_target)
        if command.lower() == 'n':
            break

if __name__ == '__main__':
    show = False
    if len(sys.argv) == 2 and sys.argv[1] == 'show':
        show = True
    if len(sys.argv) == 3 and sys.argv[1] == 'fix':
        if is_valid_number(sys.argv[2]) == False:
            print('Number {} is not valid'.format(sys.argv[2]))
            g_fix_num = target_number()
        else:
            show = True 
            g_fix_num = sys.argv[2] 
    startup(show)
    