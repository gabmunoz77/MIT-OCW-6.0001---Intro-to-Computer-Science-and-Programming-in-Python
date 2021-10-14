# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Gabriel Munoz
# Collaborators: None
# Time: Wednesday, March 10, 2021 - Tuesday, March 30, 2021

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        """
        Initializes a NewsStory object

        :param guid: (string) a globally unique identifier for this news story
        :param title: (string) the news story's headline
        :param description: (string) a paragraph or so summarizing the news story
        :param link: (string) a link to a website with the entire story
        :param pubdate: (datetime) date the news story was published

        A NewsStory object has five attributes:
            self.guid (string, a globally unique identifier for this news story)
            self.title (string, the news story's headline)
            self.description (string, a paragraph or so summarizing the news story)
            self.link (string, a link to a website with the entire story)
            self.pubdate (datetime, date the news story was published)
        """
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        """
        Used to safely access self.guid outside of the class

        :return: self.guid
        """
        return self.guid

    def get_title(self):
        """
        Used to safely access self.title outiside of the class

        :return: self.title
        """
        return self.title

    def get_description(self):
        """
        Used to safely access self.description outside of the class

        :return: self.description
        """
        return self.description

    def get_link(self):
        """
        Used to safely access self.link outside of the class

        :return: self.link
        """
        return self.link

    def get_pubdate(self):
        """
        Used to safely access self.pubdate outside of the class

        :return: self.pubdate
        """
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        """
        PhraseTrigger is an abstract class for a phrase trigger

        :param phrase: (string) one or more words, NOT case-sensitive, separated by a single space, without punctuation

        PhraseTrigger inherits from parent class Trigger and has one attribute:
            self.phrase (string, one or more words, NOT case-sensitive, separated by a single space, no punctuation)
        """
        self.phrase = phrase

    def is_phrase_in(self, text):
        """
        Checks whether the phrase is in the given text.

        :param text: (string) a snippet or long body of text in which to look for the phrase

        :return: (boolean) True if the whole phrase is present in text, False otherwise - NOT case-sensitive
        """

        # Algorithm
        # assumption(s): phrase is a valid phrase
        # 1. lower case both the text and the phrase
        # 2. iterate through text, replace characters in string.punctuation with spaces
        # 3. Create word lists of text and phrase by splitting it over the spaces
        # 4. Need to check 2 things: that all words from phrase are in text; that they appear consecutively -- ie. that
        #       the words in phrase all have consecutive indices in the word list for text (consecutive indices have
        #       indices that when subtracted == 1)

        # working with text and phrase NOT case-sensitive
        phrase = self.phrase.lower()
        text = text.lower()
        # lets replace all the special characters with spaces
        for char in string.punctuation:
            text = text.replace(char, " ")
        # lets list all the words in the text by splitting over whitespace (space(s))
        text_word_list = text.split()
        # could we get any empty strings? If so, remove them...the words in our phrase as well
        phrase_word_list = phrase.split()
        # initialize boolean to return for phrase trigger if phrase found in text
        found = True
        # create empty list to append INDICES of words from phrase that appear in the text
        test_word_indices = []
        # iterate over phrase word list
        for i in range(len(phrase_word_list)):
            # compare every word in text to each word in phrase
            for j in range(len(text_word_list)):
                if phrase_word_list[i] == text_word_list[j]:
                    test_word_indices.append(j)
        # if did not at least find all the words in the phrase, we know the phrase is NOT in the text
        if len(test_word_indices) < len(phrase_word_list):
            return not found
        # now we check that every consecutive pair of words in the LIST is consecutive in the TEXT (are 1 index apart)
        for i in range(len(test_word_indices) - 1):
            # if any consecutive pair of words in the LIST is NOT consecutive in the LIST, we know phrase is not in text
            if test_word_indices[i+1] - test_word_indices[i] != 1:
                return not found
        # if we finish the loop, we know every word in the phrase was found at consecutive locations in the text and
        # i.e. the phrase was found in the text
        return found

# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        """
        TitleTrigger is an abstract class for a title phrase trigger

        :param phrase: (string) one or more words, NOT case-sensitive, separated by a single space, without punctuation

        TitleTrigger inherits from parent PhraseTrigger, which inherits from parent Trigger, and has one attribute:
            self.phrase (string, one or more words, NOT case-sensitive, separated by a single space, no punctuation)
        """
        # just call PhraseTrigger constructor
        PhraseTrigger.__init__(self, phrase)

    # now just need to write TitleTrigger evaluate method--don't want to use empty parent class Trigger evaluate method
    def evaluate(self, story):
        """
        Checks whether the given phrase appears in the NewsStory's title

        :param story: (NewsStory object) the RSS news story whose title we will search for the given phrase

        :return: True if the given phrase is in the title, False otherwise
        """
        return self.is_phrase_in(story.get_title())

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        """
        DescriptionTrigger is an abstract class for a description phrase trigger

        :param phrase: (string) one or more words, NOT case-sensitive, separated by a single space, without punctuation

        DescriptionTrigger inherits from parent PhraseTrigger, which inherits from super Trigger, and has one attribute:
            self.phrase (string, one ore more words, NOT case-sensitive, separated by a single space, no punctuation)
        """
        # call parent class constructor
        PhraseTrigger.__init__(self, phrase)

    # now just need to write DescriptionTrigger evaluate method
    def evaluate(self, story):
        """
        Checks whether the given phrase appears in the NewsStory's description

        :param story: (NewsStory object) the RSS news story whose description we will search for the given phrase

        :return: True if the given phrase is in the description, False otherwise
        """
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
class TimeTrigger(Trigger):
    # Constructor:
    #        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
    #        Convert time from string to a datetime before saving it as an attribute.
    def __init__(self, time):
        # user should give time string in format e.g. "3 Oct 2016 17:00:10" with valid datetime class values, in EST
        # d - day, b - month, Y - year, H - hour, M - minute, S - second
        try:
            # method returns a datetime object by parsing string "time" in specified format
            dt = datetime.strptime(time, "%d %b %Y %H:%M:%S")
            # method changes the timezone to Eastern Standard Time
            # tzinfo an optional argument of datetime objects - tzinfo is an abstract base class, need to pass an
            # instance of a subclass--here provided by pytz.timezone (from RSS feed, time in GMT - Greenwich Mean Time)
            dt = dt.replace(tzinfo=pytz.timezone("EST"))
        # if invalid values given, try it again
        except ValueError:
            dt = datetime.strptime(time, "%d %b %Y %H:%M:%S")
            dt = dt.replace(tzinfo=pytz.timezone("EST"))
        # now assign datetime to time attribute
        self.time = dt

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self, time):
        """
        BeforeTrigger is a abstract class of TimeTrigger for a time trigger

        :param time: (string) the NewsStory's time in EST and formatted as "%d %b %Y %H:%M:S"

        BeforeTrigger inherits from TimeTrigger and has one attribute:
            self.time (string, ...)
        """
        # simply call TimeTrigger's constructor
        TimeTrigger.__init__(self, time)

    def evaluate(self, story):
        """
        Checks whether the given story was published BEFORE the time trigger

        :param pubdate: (NewsStory object) the RSS news story whose pubdate we will compare with time attribute

        :return: (boolean) True if the story was published strictly before the trigger's time, False otherwise
        """
        # can use the >, ==, < operators to compare datetime-s!
        # our time triggers are in EST, need to convert the story's GMT times to EST
        return story.get_pubdate().replace(tzinfo=pytz.timezone("EST")) < self.time

class AfterTrigger(TimeTrigger):
    def __init__(self, time):
        """
        AfterTrigger is a abstract class of TimeTrigger for a time trigger

        :param time: (string) the NewsStory's time in EST and formatted as "%d %b %Y %H:%M:S"

        AfterTrigger inherits from TimeTrigger and has one attribute:
            self.time (string, ...)
        """
        # simply call TimeTrigger's constructor
        TimeTrigger.__init__(self, time)

    def evaluate(self, story):
        """
        Checks whether the given story was published AFTER the time trigger

        :param pubdate: (NewsStory object) the RSS news story whose pubdate we will compare with time attribute

        :return: (boolean) True if the story was published strictly after the trigger's time, False otherwise
        """
        # can use the >, ==, < operators to compare datetime-s!
        return story.get_pubdate().replace(tzinfo=pytz.timezone("EST")) > self.time

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trig):
        """
        NotTrigger is an abstract class for a composite trigger to check whether a trigger failed to trigger

        :param trig: (Trigger object) the trigger to invert, can be any Trigger subclass

        NotTrigger inherits from Trigger and has one attribute:
            self.trigger (Trigger object, the trigger to invert, can be any Trigger subclass)
        """
        self.trigger = trig

    def evaluate(self, story):
        """
        Takes in a NewsStory object and inverts a given Trigger subclass's evaluate output;
        i.e. checks whether a given trigger did NOT fire for the NewsStory story

        :param story: (NewsStory object) the RSS news story to search and fire/not fire composite NotTrigger for

        :return: (boolean) True if trigger.evaluate(story) == False, False otherwise
        """
        return not self.trigger.evaluate(story)

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trig1, trig2):
        """
        AndTrigger is an abstract class for a composite trigger to check whether two given triggers fired

        :param trig1: (Trigger object) one of the triggers to check, can be any Trigger subclass
        :param trig2: (Trigger object) the other trigger to check, can be any Trigger subclass

        AndTrigger inherits from Trigger and has two attributes:
            self.trigger1 (Trigger object, a trigger to check in conjunction with another, can be any Trigger subclass)
            self.trigger2 (Trigger object, the trigger to check with trigger1, can be any Trigger subclass)
        """
        self.trigger1 = trig1
        self.trigger2 = trig2

    def evaluate(self, story):
        """
        Takes in a NewsStory object story and checks whether any two given triggers fire for story

        :param story: (NewsStory object) the RSS news story to search and fire/not fire composite AndTrigger for

        :return: (boolean) True if BOTH given triggers would fire on given news story, False otherwise
        """
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trig1, trig2):
        """
        OrTrigger is an abstract class for a composite trigger to check whether either one/both of two triggers fired

        :param trig1: (Trigger object) one of the triggers to check, can be any Trigger subclass
        :param trig2: (Trigger object) the other trigger to check, can be any Trigger subclass

        OrTrigger inherits from Trigger and has two attributes:
            self.trigger1 (Trigger object, a trigger to check in conjunction with another, can be any Trigger subclass)
            self.trigger2 (Trigger object, the trigger to check with trigger1, can be any Trigger subclass)
        """
        self.trigger1 = trig1
        self.trigger2 = trig2

    def evaluate(self, story):
        """
        Takes in a NewsStory object story and checks whether either of/both of two triggers fire for story

        :param story: (NewsStory object) the RSS news story to search and fire/not fire composite OrTrigger for

        :return: (boolean) True if EITHER trigger1 or trigger2 fire OR both trigger1 and trigger2 fire, False otherwise
        """
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    """
    # initialize empty list to append stories for which a trigger fired
    filtered = []
    # check every story for each trigger
    for story in stories:
        for trigger in triggerlist:
            # if (at least?) a trigger fires, append story - DON'T want to append story multiple times
            # (multiple triggers could fire for same story, but only want to display the story once)
            if trigger.evaluate(story):
                filtered.append(story)
                break
    return filtered
    """
    # This is the equivalent list comprehension
    return [story for story in stories if any(trigger.evaluate(story) for trigger in triggerlist)]

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """

    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    print(lines) # for now, print it so you see what it contains!

    # Initialize empty dictionary for Triggers, empty list for ADD statements, and empty list for Triggers to return
    triggerdict = {}
    triggerlist = []

    # close the file to avoid corrupted output/files
    trigger_file.close()

    # Helper function
    def constructTrigger(typeandargs):
        """
        Constructs a Trigger object given a string of the format: "TRIGGERTYPE,arg1[,arg2]"

        :param typeandargs: (string) specifies the type of trigger to be constructed and its arguments
        :return: (Trigger object) the trigger specified by the input string
        """

        # Split the string into the type and its arguments
        typeandargs = typeandargs.split(',')
        type = typeandargs[0]
        args = typeandargs[1:]

        # Check what type of trigger we need to create--7 types
        if type == "TITLE":
            trig = TitleTrigger(args[0])
        elif type == "DESCRIPTION":
            trig = DescriptionTrigger(args[0])
        elif type == "AFTER":
            trig = AfterTrigger(args[0])
        elif type == "BEFORE":
            trig = BeforeTrigger(args[0])
        elif type == "NOT":
            trig = NotTrigger(args[0])
        elif type == "AND":
            # PROBLEM?: CAN'T ACCESS ALREADY CREATED TRIGGER OBJECTS INSIDE HELPER FUNCTION...
            # yes we can...CLOSURES in python? accessing variables in an outer scope/namespace...
            #trig = AndTrigger(args[0], args[1])
            trig = AndTrigger(triggerdict[args[0]], triggerdict[args[1]])

            # ALSO, as mentioned below when adding Triggers to the triggerlist, we should be accounting for cases
            # in which Trigger arguments to composite Triggers don't yet exist!

        elif type == "OR":
            #trig = OrTrigger(args[0], args[1])
            trig = OrTrigger(triggerdict[args[0]], triggerdict[args[1]])
        return trig

    # Iterate through lines in list of lines to parse
    for line in lines:
        # if line is NOT an ADD statement
        if not line.startswith("ADD"):
            # split the line once-> line now a list of two elements: the trigger name and the trigger type,arguments
            line = line.split(',', 1)
            # call function to create Trigger objects as specified in file
            trig = constructTrigger(line[1])
            # create key:value pair of the trigger with key trigger name and value Trigger object
            triggerdict[line[0]] = triggerdict.get(line[0], trig)
        # else line IS an ADD statement
        else:
            # Here lets add the triggers to the triggerlist
            # -> the one problem that could arise is adding triggers that don't exist yet
            # -> an exception in the main body (bottom of file) appears to handle it by printing the triggers not yet
            #       created, but doesn't "handle" the error--the search isn't carried out...

            # split ADD statement line to access the trigger names
            line = line.split(',')
            # iterate through trigger names and use them as keys to access the trigger dictionary and add the Triggers
            for trigname in line[1:]:
                triggerlist.append(triggerdict[trigname])

    return triggerlist

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        """
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]
        """

        """
        t1 = TitleTrigger("Atlanta")
        t2 = DescriptionTrigger("spas")
        t3 = DescriptionTrigger("shootings")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]
        """

        """
        t1 = TitleTrigger("Colorado")
        t2 = DescriptionTrigger("store")
        t3 = DescriptionTrigger("shooting")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]
        """

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line
        triggerlist = read_trigger_config('triggerstest1.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # 03/17/2021 - COMMENTED THE BELOW LINE IN ORDER FOR PROGRAM TO WORK
            #               YAHOO RSS FEED NO LONGER USES DESCRIPTIONS
            #stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        #print("Specified Trigger does not exist.")
        # Why/How does this exception work?
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

