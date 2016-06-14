# coding: utf-8
#import sys  # to get OS
import pdb  # for debugging
from random import choice

# TODO

    
def input_number(prompt, min_value, max_value):
    value = None
    while value is None:
        try:
            value = int(raw_input(prompt))
        except ValueError:
            print 'Please enter a number!'
        if value < min_value or value > max_value:
            print ('Please enter a number between %i and %i!' % 
                (min_value, max_value))
            value = None
    return value


def mode(list):
    # Take a list of values and return the mode; the value that exists most often
    # credit to http://thelivingpearl.com/2013/10/24/compute-the-average-min-max-and-mode-of-a-list-in-python/
    d = {}
    for elm in list:
        try:
            d[elm] += 1
        except(KeyError):
            d[elm] = 1

    keys = d.keys()
    max = d[keys[0]]

    for key in keys[1:]:
        if d[key] > max:
            max = d[key]

    max_k = []
    for key in keys:
        if d[key] == max:
            max_k.append(key),
    return str(max_k).strip('[]\'')


def by_stats():
    import urllib2, csv, re, os
    from shutil import move

    url = "http://www.powerball.com/powerball/winnums-text.txt"
    file_name = url.split('/')[-1]			# basically gets the file name
    u = urllib2.urlopen(url)
    f = open(file_name,'w+b')

    block_sz = 8192
    f.truncate()
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        f.write(buffer)
    
    # Convert space dilimeted to csv and use cvs functions
    old_f = f.name
    new_f = file_name[0:-3] + 'csv'
    tmp_f = file_name[0:-3] + 'tmp'
    f.close()
    move(old_f,new_f)
    f = open(new_f,'r+b')
    tf = open(tmp_f,'w+b')
    for line in f:
        tf.write(line.replace(" ", ","))
    tf.close()
    f.close()

    tf = open(tmp_f,'r+b')
    f = open(new_f,'w+b')
    f.truncate()
    for line in tf:
        # The double ,, is for when/if there are dual spaces in the file
        f.write(line.replace(",,", ","))
    tf.close()
    f.close()
    f = open(new_f,'r+b')
    
    csv_f = csv.reader(f)
    w1 = []
    w2 = []
    w3 = []
    w4 = []
    w5 = []
    pb = []
    for row in csv_f:
        w1.append(row[1])
        w2.append(row[2])
        w3.append(row[3])
        w4.append(row[4])
        w5.append(row[5])
        pb.append(row[6])
    # the reverse pop is to remove the header row
    w1.reverse()
    w1.pop()
    w2.reverse()
    w2.pop()
    w3.reverse()
    w3.pop()
    w4.reverse()
    w4.pop()
    w5.reverse()
    w5.pop()
    pb.reverse()
    pb.pop()

    output = None
    output = str("\nWhite ball 1 choose ")
    if len(mode(w1)) > 2:
        output += str("between these: " + str(mode(w1)))
    else:
        #output += str(mode(w1)).strip('[]\'')
        output += str(mode(w1))

    output += str("\nWhile ball 2 choose ")
    if len(mode(w2)) > 2:
        output += str("between these: " + str(mode(w2)))
    else:
        output += str(mode(w2))

    output += "\nWhile ball 3 choose "
    if len(mode(w3)) > 2:
        output += str("between these: " + str(mode(w3)))
    else:
        output += str(mode(w3))

    output += "\nWhile ball 4 choose "
    if len(mode(w4)) > 2:
        output += str("between these: " + str(mode(w4)))
    else:
        output += str(mode(w4))

    output += "\nWhile ball 5 choose "
    if len(mode(w5)) > 2:
        output += str("between these: " + str(mode(w5)))
    else:
        output += str(mode(w5))

    output += "\nAnd for Big Red Power Ball choose "
    if len(mode(pb)) > 2:
        output += str("between these: " + str(mode(pb)))
    else:
        output += str(mode(pb))
    f.close()

    # cleanup
    os.remove(f.name)
    os.remove(tf.name)
    #os.remove(csv_f) # This doesn't work on iOS
    print str(output)


def main():
    import re
    try:
        print "\n" * 200                        # clear the screen
        title = 'Powerball Generator'   
        print title
        print '=' * 40                          # print a seperator line
        found = False
        resp = raw_input("Would you prefer randomly generated numbers, " \
                         "or that I get the most winning numbers from all " \
                         "the winning numbers over the years? \n\n>")
        while found is False:
            m = re.search("(random.*)", resp, re.IGNORECASE)
            if m:
                found = True
                wmin = 1
                wmax = 69
                rmin = 1
                rmax = 26
                # get white balls
                all_numbers = range(wmin,wmax)
                wselection = []
                for i in xrange(5):
                    r = choice(all_numbers)
                    wselection.append(r)
                    all_numbers.remove(r)
            
                # get Powerball
                all_numbers = range(rmin,rmax)
                rselection = []
                r = choice(all_numbers)
                rselection.append(r)
                print 'The white balls of ' + str(wselection) \
                + ' and the Power Ball of ' + str(rselection).strip('[]') \
                + ' just might be a winner! \n Maybe.'
            else:
                m = re.search("(stat.*)", resp, re.IGNORECASE)
                if m:
                    found = True
                    by_stats()
                else:
                    resp = raw_input("Sorry, you need to choose either randomly generated or from stats.\n")
        
    except:
        raise
        print 'Fate has declared that you do not get numbers today'
        return
    # Only do the quit() to end a program compeltely
    #quit()

if __name__ == "__main__":
    main()
