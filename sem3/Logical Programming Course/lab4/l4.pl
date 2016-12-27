c([Y|T],Y,T).

 isMember(X,[X|T]).
isMember(X,[_|T]):-isMember(X,T).



 isMember1(A,X,[Y|T]):-isMember(X,Y),Y=[A|_].
isMember1(A,X,[_|T]):-isMember1(A,X,T).


noun(A,f1(s),L0,L1):-c(L0,S,L1),
                                isMember1(A,S,[['Саша','Сашей'],['Лена','Леной'],['шоколад'],['Я','мною'],/*["шоколадки"],*/
                                ['Sasha'],['Lena'],['Vika'],['Dima'],['chocolate'],['john'],
                                ['mary'],['student'],['sport'],['programming'],['prolog']]).
noun(A,f1(pl),L0,L1):-c(L0,S,L1),
                                isMember1(A,S,[['students'],['sports'], ['шоколадки']]).
adjective(S,L0,L1):- c(L0,S,L1),
                    isMember(S,['умные','smart','stupid','young','old']).

article(["nondet"],f1(s),L0,L1):-c(L0,'a',L1).

verb(A,s,L0,L1):- c(L0,S,L1),
                isMember1(A,S,[['любить','люблю','любит'],['like','likes'],['dislike', 'hates'],['like','prefers']]).
verb(A,pl,L0,L1):-c(L0,S,L1),
                isMember1(A,S,[['любить','любят'],['like','like'],['dislike', 'hate'],['like','prefer']]).
verb(A,pass,L0,L1):-c(L0,S,L1),
                  isMember1(A,S,[['любить','любим','любимы'],['like','liked'],['dislike', 'hated'],['like','prefered']]).

article(['det'],f1(pl),L0,L1):-c(L0,'the',L1).



verb_clause(action(A),f(N,act),L0,L1):- verb(A,N,L0,L1) .
verb_clause(action(A),f(s,pass),L0,L2):- verb(A,pass,L0,L2).
verb_clause(action(A),f(pl,pass),L0,L2):- verb(A,pass,L0,L2).
verb_clause(action(A),f(N,act),L0,L2):-negation(N,L0,L1), verb(B,N,L1,L2), neg(B,A).
verb_clause(action(A),f(N,pass),L0,L3):-tobe3f(N,L0,L1), verb(A,pass,L1,L2),c(L2,'by',L3).
verb_clause(action(A),f(N,pass),L0,L4):-tobe3f(N,L0,L1), c(L1,'not',L2),verb(B,pass,L2,L3),
                                                       c(L3,'by',L4),neg(B,A).


tobe3f(s,L0,L1):-c(L0,'is',L1).
tobe3f(pl,L0,L1):-c(L0,'are',L1).

negation(pl,L0,L2):-c(L0,'do',L1),c(L1,'not',L2).
negation(s,L0,L2):-c(L0,'does',L1),c(L1,'not',L2).

neg('любит', 'нелюбит').
neg('like', 'dislike').
neg('dislike', 'like').

subject_clause(and1(A,B),f1(pl),L0,L3):-subject(A,_,L0,L1),c(L1,'и',L2),subject(B,_,L2,L3).
subject_clause(and1(A,B),f1(pl),L0,L3):-subject(A,_,L0,L1),c(L1,'and',L2),subject(B,_,L2,L3).
subject_clause(X,F,L0,L1):-subject(X,F,L0,L1).


object_clause(X,F,L0,L1):-subject_clause(X,F,L0,L1).

subject(noun(X,[]),F,L0,L1):- noun(X,F,L0,L1).
subject(noun(X,[A]),F,L0,L2):- adjective(A,L0,L1), noun(X,F,L1,L2).
subject(noun(X,A),F,L0,L2):- article(A,F,L0,L1), noun(X,F,L1,L2).

sentence(frame(subject1(S),A,object(O)),L0,L3):-
                            subject_clause(S,f1(F1),L0,L1),/*write(S,"  ",f1(F1)),nl,*/
                             verb_clause(A,F,L1,L2),F=f(F1,act),/*write(A,"  ",F),nl,*/
                             object_clause(O,_,L2,L3).
sentence(frame(subject1(S),A,object(O)),L0,L3):-
                                        subject_clause(O,f1(F1),L0,L1),/*write(O,"  ",f1(F1)),nl,*/
                                         verb_clause(A,F,L1,L2),F=f(F1,pass),/*write(A,"  ",F),nl,*/
                                         object_clause(S,_,L2,L3).

synonym(A,B):-sentence(S1,A,[]),write(S1),sentence(S2,B,[]), write(S2),S1=S2, write('yes!').