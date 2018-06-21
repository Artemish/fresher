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

### Commands

* 'dv' - Downvote

   Demotes the current song, indicating you'd like to hear it less

* 'uv' - Upvote

   Promotes the current song, indicating you'd like to hear it more

* 're' - Repopulate

   Looks into your music directory for any new music files, and assigns new
   files a freshness of 100.

* 'n' - next

   Randomly samples the songs in your library according to their freshness,
   decreases its freshness a bit, then returns the song title

### Design goals

I'm not sure whether keeping freshness constant is a worthy design goal, but
I'll try it and see how it goes. Every operation affecting the freshness of a
song will either distribute freshness to (in the case of lost freshness) or
take freshness from (in the case of gained freshness) all other songs. 
