## Fresher

Fresher is a tool that is meant to attach a 'freshness' score to the music you
listen to. If I really like a song I tend to listen to it incessantly until
it's not good anymore. So, in an attempt to enjoy music longer, and give older
tracks that have slipped your mind another chance, Fresher will automatically
demote songs you listen to a lot, promote songs you don't hear often, and allow
you to manipulate scores manually to control when you hear a given song again.

Fresher will populate a data store with all of the song titles contained in a
given directory, and assign each song a score of 100. As you listen to a song, it
decreases the freshness, and distributes the freshness among other songs.

### Usage

 > user@shell$ ./fresher.py --help
 > usage: fresher.py [-h] {show,repopulate,next,upvote,downvote} ...
 > 
 > positional arguments:
 >   {show,repopulate,next,upvote,downvote}
 >                         commands
 >     show                Dump the score dictionary
 >     repopulate          Repopulate and reset the score dictionary
 >     next                Samples the list of songs and suggests a new one
 >     upvote              Upvote the currently playing song
 >     downvote            Downvote the currently playing song
 > 
 > optional arguments:
 >   -h, --help            show this help message and exit

### Design goals

I'm not sure whether keeping freshness constant is a worthy design goal, but
I'll try it and see how it goes. Every operation affecting the freshness of a
song will either distribute freshness to (in the case of lost freshness) or
take freshness from (in the case of gained freshness) all other songs. 
