import re
from collections import Counter
import numpy as np
from itertools import groupby


text1 = ('To the Magnificent Lorenzo Di Piero De Medici'
         'Those who strive to obtain the good graces of a prince are accustomed '
         'to come before him with such things '
         'as they hold most precious, or in which they see him take most delight'
         'whence one often sees horses, arms, cloth of gold, precious stones, '
         'and similar ornaments presented to princes, worthy of their greatness.'
         'Desiring therefore to present myself to your Magnificence '
         'with some testimony of my devotion towards you, '
         'I have not found among my possessions anything which I hold more dear than, '
         'or value so much as, the knowledge of the actions of great men, '
         'acquired by long experience in contemporary affairs, and a continual study of antiquity'
         'which, having reflected upon it with great and prolonged diligence, '
         'I now send, digested into a little volume, to your Magnificence.'
         'And although I may consider this work unworthy of your countenance, '
         'nevertheless I trust much to your benignity that it may be acceptable, '
         'seeing that it is not possible for me to make a better '
         'gift than to offer you the opportunity of understanding '
         'in the shortest time all that I have learnt in so many years, and with so many troubles '
         'and dangers which work I have not embellished with swelling or magnificent words,'
         'nor stuffed with rounded periods, nor with any extrinsic allurements or '
         'adornments whatever, '
         'with which so many are accustomed to embellish their works'
         'for I have wished either that no honour should be given it, '
         'or else that the truth of the matter and the weightiness of '
         'the theme shall make it acceptable.'
         'Nor do I hold with those who regard it '
         'as a presumption if a man of low and humble condition '
         'dare to discuss and settle the concerns of princes'
         'because, just as those who draw landscapes place'
         'themselves below in the plain to contemplate '
         'the nature of the mountains and of lofty places, and'
         'in order to contemplate the plains place themselves upon high mountains,'
         'even so to understand the nature of the people it needs to be '
         'a prince, and to understand that if princes it needs to be of the people.'
         'Take then, your Magnificence, this little gift in the spirit in which I send it'
         'wherein, if it be diligently read and considered by you, '
         'you will learn my extreme desire that you should attain that'
         'greatness which fortune and your other attributes promise. '
         'And if your Magnificence from the summit of your greatness '
         'will sometimes turn your eyes to these lower regions,'
         'you will see how unmeritedly I suffer a great and continued malignity of fortune.')


text2 = ('There was once a young Shepherd Boy who tended his sheep'
         ' at the foot of a mountain near a dark forest.'
         ' It was rather lonely for him all day, so he thought'
         ' upon a plan by which he could get a little company and some excitement.'
         'He rushed down towards the village calling out “Wolf, Wolf, ”'
         ' and the villagers came out to meet him, and some of them stopped'
         ' with him for a considerable time. This pleased the boy so much '
         'that a few days afterwards he tried the same trick,'
         ' and again the villagers came to his help. But shortly '
         'after this a Wolf actually did come out from the forest,'
         ' and began to worry the sheep, and the boy of course cried out'
         ' “Wolf, Wolf, ” still louder than before. But this time the villagers,'
         ' who had been fooled twice before, thought the boy was again deceiving them,'
         ' and nobody stirred to come to his help. So the Wolf'
         ' made a good meal off the boy’s flock, and when the boy complained,'
         ' the wise man of the village said:'
         '“A liar will not be believed, even when he speaks the truth.”')

text3 = ("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
         "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
         "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM9OOOUOOMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMHMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNOtllltlllltdHMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMEV6lllltllltVVHMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMltttllllltlltlld9MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMtltltlltttltttllttMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         "# SllttllttllttlllltlttHMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNtttllllltllttllltOTMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         "# tttltllltlllllltttltWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#llttllttllttllttltttttldMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         "# OttttllllllllltlttltlttlldMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN6ttlllttltllllltllltttMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         "# OllttttttttlltttltlttttlldMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMtllltltttllllllltlttttwHMMMMMMMMMMMMMMMMMMMMBUWHWWHBMMMMUUWHMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMbOtlltttlllllttttltltllvMMMMMMMMMHHWXSZuuZZZuuuuuuuuZZZZZZZZZZZZZZZuXVT6XVBMHWMMMMlllllttttttttttttllttttttdMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         "# ltllttttlltlllllltlltltOS9llttXZZZZuuuZZuuZZZZuuZZZZuZZuZuuuuZUVOtttttttttlllOOlllllllltlltlttllltllllllqMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMKttttlllltllllttltttltlltlttltOXuZuZZZuZZZZZZZZZZuZuZuuZZ0XZOttttllttttttttltllltllllllllltttlllllllllzgMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNsttttttlllllttttlttttttttlttttwZuZZZuZuZZZuuuZZZZZZuXXZOlttttttlttttttttttttllllllllllllllllllllttllqMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNtttttttttttttltttttlttllltttwuZZZuuZuuuuZZZZZXUU0OttlllltttlltttttttllllttlllllltllttlltlllltlllOdMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMttlltlllttttltttttttttlllttlOXZuuuZZuZXVZZVtOttttttttttltttlttlttllttttllltllltlllltlttlllltttQMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM9ltltttlllttllttttltltttttlltttlltlOOttttlllltttltttttttttttlttlttlltlttlltttllllltlltlttlttttlOMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM8ttlttttttlttltlttttttltlllltllllltttlttttllttttltttttlttttttttttttttttlltlttttttltlllltllllllllttttdMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM@ltttltttttttlttltttttllttttlltlllttltltttttlltltlttlllltllltttllltlttlltttltttltlllltlllllltlltltllltlddMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM@tltltttlttttltttttttltttlttttttttttttllttttttltllltllltlllllltltttttltllttllltllllltttttttllllltltlltltttlZMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM@OlllltttttttltttttttlttttllllltlttttltllllllllllltlltlltltttlltttltllttllttttlllltltttlltlllttllllllltttttllllMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM8tlllttttltlltllltttttttttllllltllttttllltllllllltltttlltltlltlltttlttllttttttltlttttltltlltllllltllllllllltlllllvVHMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMEttttttttlttlttttlttttttlttllllllllllllllllttlllltllltllttttlllttttlllllttlttlltttlttltttltttllttttlttltlllllllllllllzTMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM0tttlltttttltllllttttttttttllltllttlllllllllllllllltttlltllltlltllttlttlttttttttlttttttttttttlttlltlllttlltllllllllltttttZWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMIllttttttrttttttlllttltllllOwOlltlllttttttttttlttttttttttttttllllOuQHdHgmOltltlltllllttttlttlllltllllllltlllllllllltlllltltllMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM6ttttttttttttttttttttllttOAdHHHHMmytltlttttttlttttttllttttlltlltttdMHHHHHHHMkOllttttllttltttlllttlttllllltlltllltlttlttllllllllOHMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         "# HH#HH#MHOtltttttttttrttttltttttttttttwMHH###H#HH#RyttttlttltttlltttllttttlllltlttlllttltllttltllllttZMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMM@ttttttlllltltlttttttttttttwMH'
         "# H##H#HHMZlttllttltlttrttttttttttlttlldMHHH#HHHHH#M6ltltttttttttttttttttttttttttlltttltlltlllltttttttttdMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMXttttttlttttltttttltltttttttdM'
         "# H#HH##HH#IlttlllltttttrttttttttttttttlZHMH##HH#H#MMOtlllllttltttttrtrtttrtrttttttttttttttttttltttttttttttMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
         'MMMMMMMMMMMMMMMMMMMMMMMMM@rrrrrrttlttttttllllltllttttllwM'
         "# HHM8ttllllttttttttttttttlltltttlttllZBMH##MMM8tttttttttltttltttrrrrrrrrrvrrrtttOrttttttlttttttttttttltdMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
         'MMMMMMMMMMMMMMMMMMMMMMMMBrrrrrrrrOtttltlltlltllllltlttltTMHHH'
         'MMMMMMMMMMMMMMMMMMMMMMMBvrrrrrrrrttOttttltltttlllttttlltltZVHH8OllttttttltttlttttllttltllttltlttlltltOZUZOttlltttltltttlttrrrvrvvvvzzzzvzvrrrrrrttttttttttttttttttltZMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMvvrvvrrrrrrrrrrrttttttlttlttttltllttttttttltllllllllllltt > ~_1ltlltttltttlttlllltttttlttlllltttttttrrrrvvvzzzuzvvzzzzzzvzvrrtttrtrrtttllttttlttttqMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMSvrrzzvrrrvvrrrrttrtttllltttllllltttltlttttlttttlllllttl << _..._?ztltttltttltttttttllllltttttttttttrtrrrrvvvzzzzvvzzzzzzzzzvvrrrtttttttllllttlttttZMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMBvrvvzvvvvzvvvvrrrtrttttlttllttltlttttttttlttttttttlltlv1~........_1zltttllltlllllltttlttlltlltttttttrrrrvvvvvvzzzzzuzzzvzzzvzvrrrttttttlttltttttttrwMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMEvvzzzzzvvzzvzzvvvrrrttttltlltlltttlltltlllllllltttOz << ~.............._1ltttlltltlltltttttttttttttltttrrrrrrrvvvzzzvvvzzzzvzzzvrrrrttttlltlttttttlttttZMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMM@vvzzzvvzzzzvrrrvvvrrttttltttllttllllllllttttlllttv < ~...................-_ <?1ltttlltllllttltltttttttttttttrrrrvvrvzzvvvzzzzzzzvvvrrttrtrttttttltttttltlttMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         "# rrrvvvvrvzzzvvrrrvrrrrttttttttttlttlttttttttltv1>_...._-------((_--..........(<1ttttttllltttlltttttttttttrrtrrrtrrwzvrrrrvvvvrrrvrrtrtttlltrtttttttltltlt?MMMMMMMMMMMMMMMMMMMMMMMMMMMMM"
         'MMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMM6tttrrrrrrvvvvrrrrrrtttttttlttttlttlllttttlOvv < _.....(WHWmgmqmqHqmgka, ............_?z1zOttttttttlllltlltttttrrrrrrtrrrOwOrrtrrtrrrrrrttttttttttttttttltltttdMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMF!_ <?I1Ottrtrrrrtrrtttrttttttlttltttltlzzvz <!__......-JmmmmmmmmqqmggmggH > ..............._ <<??1OtttttllltttltlttttttttttttrttttttttttlttrtttttttttllttlttttlttdMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMM  # _....._._<?1zOttttttttttttttltllzzz<<<!__............_OmmqqmqqmmmmmmmmH3......................__<?<+1lztlltttttttttttttttttlttlttlttttttttllllllltttttlttOzv<<<WMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMM@~.............__ <<?<< << <?<?<!<!~.-_....................-7YUHmmmmmmmgmq9!.......`......................__~~_ < ~ < ~ << +v?< 1I?1v1zzlttlttllvOtltlllttttlzlzz <??<~_....7MMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMM ^ ............................................................_!?7T7=?!!......`.....................`.............................__...._!_~~_ < ___ < _..............-MMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMM5............................................................................`...................................................................................._XMMMMMMMMMMMMMMMMMMMMMMMMM'
         "MMMMMMMMMMB'...............`..`.`.........................................................`.`......................................................................`..........-dMMMMMMMMMMMMMMMMMMMMMMMM"
         'MMMMMMMMMM, ....`.........`..`......`.........`.......................`...............`.........................................................................................(MMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMF ......`..`..`.........................`................`.............................................`...............................................`.........`....(MMMMMMMMMMMMMMMMMMMMMMMM'
         "MMMMMMMMMM'.......`...`..................`.................-_...........................`.`........(+-.-.........`................`.........`..`..`..`.....`......`.`..`......._MMMMMMMMMMMMMMMMMMMMMMMM"
         'MMMMMMMMM$..`..`..........`..`..`......`................-JXwwz_...`....`.`.`...`.`...`...........-JuuuZs_...........`...`.......`.........`.....`.......`...`.`..`...`..`....`.-dMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMN-.`.....`......................................jZZZZX-.....`......-_uwo(-....`......`....(wuuZ0_.............................`.............`....`.....`................(MMMMMMMMMMMMMMMMMMMMMMM'
         # -..........`..`......`.........................(XZuuu:..........--dwuuuuuA-.....`........(XZuyk~...............`..`..................`....`...`...`.....................MMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMM'
         'MMMMMMMMM/...`.`..........`.............................(wuuuuo-..`..`.-(zuuuuuuuuuX & --_........--(ZZZZZ!....................`..`.`..`.....`......`.....`...`...............`....JMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMM: ......`.`.................................`....juuZZZX & J-(z+wwuuuZZ0VOuuuuZZXuwu+w & &uwXZZZyZUl............`..`..............`..`..`...`.................`..............(MMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMM: ....`......`...`..............................._?XZZuZZZuuZuuuZZuVC~.._jZZZuuZZZZZZZuZZZZZ0V!.................`.........`................`..........`...................WMMMMMMMMMMMMMMMMMMMMM'
         " # !...........`....................................._?7XZZZuuuuZXUC_......._7?U0XXZZZuZZuXXT7!................`....`....`....`..`.......`......`...`.....`........`.......(MMMMMMMMMMMMMMMMMMMMMM"
         'MMMMMMMM'
         'MMMMMMMMN}.............`......................................__ <<?<< < _~...............___?!~__!< _...........................`...............`......................---_.......`..JMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMM!......................`............................................................................`...`...............`........`......................._(?>> < ......`...(MMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMm..............................................................`...............................................`...............`...........`.........`..-+???< ~..........JMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMR-..............`...`.........................................................`...........................`.................`..........................(+???< ~...........(MMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMm, ........................................`.`..`...................`..-.((J--_.......`.`.......`.............`...`.`..`...........................`--(?>??<_.........`..-vMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMN, .................`...........................`.`.................(ggHkkkqHa, ...........`..`..................................`..`.....`........((?>> > <~......`........dMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMNx..`...........................`...........`......`............(WgggqkkqkkqHx-....`.................`...................................`..`--+>>?> <!.................-MMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMM, ...`.............................`....`......`...`........._dgg@@qqqkqkqHHo..................................`.....`..`................- < +>> >?<~....................JMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMNa., .................`...`..........`........`..........`.`(dg@@@@qkkqkkkg@h._............`..........`..........................`..`..((>> >?<<~_.........`.....`.....(MMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMN, -............`..........`..`.......`.`..............-jH@@gg@mqqkkkkH@@H+...............`...........`.......................--(>> >???<<_...........`........`...(MMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMNR-_....`.`.....`..`......................`..`......JWgg@gg@qkqqkkkH@@@K_.......................`......................-(+ <<?>??>?<!_..................`....`...JMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMN+(`......`.......`.......`.`..............`...._JkHg@@ggkkkkkkkH@@gH{.................`..............`...`.....(( > (+?????<< <~..............................-MMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMNN--.....`.................`.............`..(Wqqgg@g@HkkkkkbHgg@gH < .............`.....`....`..............._+?>???> << _.....................`..`.........-MMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNaJJ.........`..........`......`.`.....(Wqkgg@@@Hkkqkbkqgg@@H2.....`....`..........`.................._ << <<~_......................`...........`.`.-MMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN -`..................`............(XkqH@@@gmkkqkkkH@g@gHkc......................`..`......`..............................`..............`.....(MMMMMMMMMMMMMMMMMMM'
         "# ~.`........`..`...`.....---_--((+v61ZUHH@HkkqkkkHg@H993++++-(-----.....`..........`.`......`........................................`........dMMMMMMMMMMMMMMMMMM"
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM]................------++???>?>> >??>>???+ZHHqkkkbHH81?>> >> >?>>>>>>>> > + < ( < __........................................`.......`..................(MMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMb.........._.-((>>>>>>?==??>??<< << << <<???1XkqkbbbW$>> > << << << << < + <<?>?>?>>?> <; +----......................................`......`...`..........-MMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMF....`..-+++>>>>?>> << << <<!............_ < >>+WkbbkkHI???< ........._.___ << + <?>>?>>?>?<<_...........................`..............................(MMMMMMMMMMMMMMMMM'
         "# ........_<???<><<!~...................(<>?zWkkkkqRz??<_...................__<<<????<~.............`..............................`...`.........?MMMMMMMMMMMMMMMMM"
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN.......`._ < __........................_(>?>zWkkqkkHy???+ _........................._~__..........`....`.............`....`.....`..............`..dMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN_....`............................`..- << >>jXHkkkkkHH3???< ..................................................................................`....JMMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM@...................................._(?>?jX@HkkkkbbHk <>?> < _..................................`.......................`.....`....`..`............ MMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM@...`..`............................( < >> > j@@ggHkkkkHggRz >?>> < .`..`..`...`........................``.`..`...........................`........`....(MMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN ....................`........`..`_ <>?>1uH@@ggqkkkbHg@gHk+>>?< _...........`..`..................................................`.................JMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM3...................`............(>>??1dH@@@@@qkkqkqgg@gHkI?>?> < _.`...`........`.............`..`........`.`............`...............`..`......JMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN ........`.....`.`............_(+?>??zWqmg@@@gHkkkqqg@g@gHl(+?>> < -_....................................`..........................................WMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN ...`.....`..`....`....`...._((>>??< _.?HqH@g@@Hqkkqqg@gggH > ._ <>???<-_.............`..............................`...`.....`......................dMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM!......`............`.....-(+???<< ~..._7HH@@@@HqkkkH@g@gHt ..._ >????>_....`....`.......................................`..........................MMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN .`............`........(+ >??> << _......_(Hg@@@@HkkkHgg@@8: ......_ <????> < _-..`...................................`........`......`....`............dMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN...`.`.....`.........(>> >??> << _..........vHggg@HkkkH@g@H!........._ < >>?>> > +_........`......`......................`.......`..`....................(MMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM].........`...`......_ << >> < ~_............._?THHkqqqH@H=!............._ << > <> _....`.`............`....`...`............`.............`..`...........?MMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM].....................____...................__?777YT!.........................`........`.........`...........`.`........`................`.......(MMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMb.......`......`.............................................`.......................`...............`..........................`..........`......(MMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMb -`.........`...............`..`..`................................`.........`....`.......`..`..`.........................`.........`...`......`..-MMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMP...........................................................................................`..`..`...`..`........`....`.....`....................(TMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMF.................`.....`.......................................`.....................`.........................................`.................(MMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMF...........................`..........`.......................................`.................`..`.......`...............`......................(MMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMF.........................................................................................`.....`....`.........`.`.................`..`.`........._(MMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM @ ....................................................................`.....`..`....`......................`.............`..`..`..........`.........dMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN..........................`.................`...........................`................`....`....`...........`.................`..`.............?MMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM@...............................`.....................................................`..`..............`............`.......`..`...........`....`.(MMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMb.....................................................................................................................`..`...............`.........JMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN .....................................`................`............`..`.........`....`.....................`.`..`................`.`.`....`......JMMMMMMMMMMMMMMMM'
         'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM!...................................................`....`....................`.................`...`.....................`............`......`...JMMMMMMMMMMMMMMMM')


def calc_entropy(text):
    c = Counter(text)
    # print(text)
    # print(c)
    L = len(text)
    p = np.array([n/float(L) for n in c.values()])
    entropy = np.sum(-p*np.log2(p))
    print('')
    print(f"text_entropy = {entropy:.4f}", f"word_count ={L}")
    print('')


if __name__ == '__main__':

    text1_str = re.sub(r'[.,"“”’\'-?:!;]', '', text1)
    text2_str = re.sub(r'[.,"“”’\'-?:!;]', '', text2)
    text3_str = text3
    # print(text1_str, '++++++++++++++++++++++++++++++++++')
    text1_word = text1_str.split(' ')  # 1word list
    text2_word = text2_str.split(' ')
    text1_char = list(text1_str)  # 1character list
    text2_char = list(text2_str)
    text3_char = list(text3_str)
    # print(text1_word, '----------', len(text1_word))
    # print(text2_word, '---------', len(text2_word))
    calc_entropy(text1_char)
    print()
    calc_entropy(text2_char)
    print()
    calc_entropy(text3_char)


class Huffman:
    def __init__(self):
        self.tree = None
        self.pattern = None
        self.encode_dict = {}
        self.decode_dict = {}

    def encode(self, data):
        unique_data = set(data)
        nodes = []

        for v in unique_data:
            node_obj = Node(value=v, count=data.count(v))  # アルファベット一文字の数
            nodes.append(node_obj)
        temp = []
        while len(nodes) >= 2:
            for v in range(2):
                elem = min(nodes, key=lambda x: x.count)
                temp.append(elem)
                nodes.remove(elem)
            n = Node(value=None, count=temp[0].count+temp[1].count, left=temp[0], right=temp[1])
            temp = []
            nodes.append(n)  # nodeの更新 左が小さい値で右が大きな値
        self.tree = nodes[0]
        self.recursive_code(self.tree, "")
        s = ""
        for v in data:
            # print(v, end='')  #英文
            s += self.encode_dict[v]
        return s

    def recursive_code(self, node, s):  # 圧縮結果を取得する
        if not isinstance(node, Node):
            return
        if node.value:
            self.encode_dict[node.value] = s
            self.decode_dict[s] = node.value
            return
        self.recursive_code(node.right, s+"1")
        self.recursive_code(node.left, s+"0")

    def decode(self, data):
        assert (self.decode_dict)
        result = ""
        s = ""
        for bit in data:
            s += bit
            if s in self.decode_dict:
                result += self.decode_dict[s]
                s = ""
        return result


class Node:  # 葉を表すクラス
    def __init__(self, value=None, count=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.count = count


h = Huffman()
x_1 = h.encode(text1_str)
x_2 = h.encode(text2_str)
x_3 = h.encode(text3_str)
print()
print(f'\ntext1ハフマン符号{len(x_1)}')
# print(x_1, f'\ntext1ハフマン符号{len(x_1)}')
print()
print(f'\ntex2ハフマン符号{len(x_2)}')
# print(x_2, f'\ntex2ハフマン符号{len(x_2)}')
print()
print(f'\ntex3ハフマン符号{len(x_3)}')
# print(x_3, f'\ntex2ハフマン符号{len(x_3)}')
d_1 = h.decode(x_1)
d_2 = h.decode(x_2)
d_3 = h.decode(x_3)

# print("decoded:", d)

ans_1 = [(k, len(list(g))) for k, g in groupby(text1_str)]
ans_2 = [(k, len(list(g))) for k, g in groupby(text2_str)]
ans_3 = [[k, len(list(g))] for k, g in groupby(text3_str)]

# print(ans_1)  # ランレングス
print()
print()
print()
# print(ans_2)
print()  # ランレングス
print()  # ランレングス
print()  # ランレングス
# print(ans_3)  # ランレングス
y_1 = ''
j_1 = 0
y_2 = ''
j_2 = 0
y_3 = ''
j_3 = 0
for i in ans_1:
    j_1 += 1
    y_1 += str(i[1])
print(len(y_1)+j_1)
for i in ans_2:
    j_2 += 1
    y_2 += str(i[1])
print(len(y_2)+j_2)
for i in ans_3:
    j_3 += 1
    y_3 += str(i[1])
print(len(y_3)+j_3)
