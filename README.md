# halte

A refereeing system using ML-driven computer vision to score fencing videos. Videos should include the equipment lights but no referee signs after the combat starts, and no sound.
High level goals per iteration:
1. Classify fencing images according to the weapon displayed (or into "non-fencing")
1. Decide which fencer(s) get a point in single light touches, in any weapon.
1. Recognize double touches in epee
1. Recognize invalid touches in any weapon
1. Assign points based on right-of-way in foil and saber
1. Properly referee "simultaneous" actions at start of combat in saber
More goals may be added later.

## Motivation

Refereeing any sport is like planning a wedding. No matter how brilliantly you do it, 50% of the people will complain.

That said, this project is *not an attempt at replacing human referees* in any sport, specially at fencing where refereeing is a vital part of learning the game and its culture.

This project is intended as a learning tool for the fencing community (and also as a Machine Learning exercise initiated by a passionate fencer). There can be no guarantee at this point as to how accurate or how fast the refereeing system will be. As any human referee, Machine Learning algorithms are rarely 100% perfect (though other use cases have proved that they can frequently be more accurate than humans).


## Many thanks to...

For providing huge amounts of data (images and videos):
- Fernando Scavasin

_more to come..._
