% Автор:
% Дата: 06.12.2015
male("Konstantin /Zabelin/").
male("Mikhail /Zabelin/").
male("Alexander /Pister/").
male("Jacob /Pister/").
male("Vasiliy /Zabelin/").
male("Radiy /Kadyshev/").
male("George /Kadyshev/").
male("Denis /Blishenkov/").
male("Vyacheslav /Blishenkov/").
male("Andrey/Zabelin").

female("Elena /Kadysheva/Zabelina").
female("Nina /Zabelina/").
female("Amalia /Pister/").
female("Anna /Svetkova/Zabelina").
female("Galina /Kadysheva/Blishenkova").
female("Sofya /Ershova/Kadysheva").
female("Valentina /Saprika/Blishenkova").

child("Mikhail /Zabelin/","Konstantin /Zabelin/").
child("Mikhail /Zabelin/","Elena /Kadysheva/Zabelina").
child("Konstantin /Zabelin/","Alexander /Pister/").
child("Konstantin /Zabelin/","Nina /Zabelina/").
child("Alexander /Pister/","Jacob /Pister/").
child("Alexander /Pister/","Amalia /Pister/").
child("Nina /Zabelina/","Vasiliy /Zabelin/").
child("Nina /Zabelina/","Anna /Svetkova/Zabelina").
%child("Andrey/Zabelin","Vasiliy /Zabelin/").
%child("Andrey/Zabelin","Anna /Svetkova/Zabelina").
child("Elena /Kadysheva/Zabelina","Radiy /Kadyshev/").
child("Elena /Kadysheva/Zabelina","Galina /Kadysheva/Blishenkova").
child("Radiy /Kadyshev/","George /Kadyshev/").
child("Radiy /Kadyshev/","Sofya /Ershova/Kadysheva").
child("Galina /Kadysheva/Blishenkova","Denis /Blishenkov/").
child("Galina /Kadysheva/Blishenkova","Valentina /Saprika/Blishenkova").
child("Vyacheslav /Blishenkov/","Denis /Blishenkov/").
child("Vyacheslav /Blishenkov/","Valentina /Saprika/Blishenkova").

 предок(Кому, Предок,Список):- предок(Кому, Предок, Список,[]).

    предок(Кому, Предок,[Предок,Кому|L1],L1):-child(Кому, Предок).
    предок(Кому, Предок, L,L1):- child(Кому, Родитель),
                                                предок(Родитель, Предок,L,[Родитель,Кому|L1]).


 дедушка(Кому, Дедушка):- male(Дедушка), child(Кому, Родитель),child(Родитель, Дедушка).

  бабушка(Кому, Бабушка):- female(Бабушка), child(Кому, Родитель),child(Родитель, Бабушка).

папа(Кому, Папа):-  male(Папа), child(Кому, Папа).

мама(Кому, Мама):-  female(Мама), child(Кому, Мама).

брат(Кому, Брат):-  male(Брат), child(Кому, Parent ),child(Брат,Parent ) , Кому=\=Брат.


сестра(Кому, Сестра):-  female(Сестра), child(Кому, Parent ),child(Сестра,Parent ) , Кому=\=Сестра.


шурин(Кому, Шурин):-  male(Кому), female(Жена),
                                    child(Child ,Кому),
                                    child(Child ,Жена ),
                                   child(Жена, Parent ),
                                   child(Шурин ,Parent ),
                                    male(Шурин).

  /*Из списка удаляются повторяющиеся элементы*/
    уникальные([],[]).
     уникальные([H|T],[H|T1]):- уникальные(T,T1), not(member(H,T1)),!.
     уникальные([H|T],T1):- уникальные(T,T1).

 /* Обход графа поиском в глубину  */
  go(Start, Goal, R):-  go2([[Start]],Goal, R).

  go2([First|Rest], Goal,First):-First = [Goal|_].
  go2([[Last|Trail]|Rest], Goal,Trace):-
                                            findall([Z,W,Last|Trail], nextnode(Last,Trail,Z),List),
                                        append(List,Rest,NewTraces), go2(NewTraces, Goal, Trace).
not_member(X,[]).
not_member(X,[H|T]);-X=\=H,!,fail,not_member(X,T).

  nextnode(X,Trail,Y):- child(X,Y), not_member(Y,Trail),write('ребенок').
  nextnode(X,Trail,Y):-child(Y,X),/*W="родитель",*/ not_member(Y,Trail),write('родитель').


      nextnode1(X,Trail,Y,W):- (child(X,Y),W="   ребенок   ";
                                        папа(Y,X),W="   папа   ";
                                        мама(Y,X), W="  мама  ";
                                        шурин(Y,X), W ="  шурин  ";
                                        сестра(Y,X), W="  сестра ";
                                        брат(Y,X),W="  брат   ";
                                        дедушка(Y,X), W="  дедушка  ";
                                        бабушка(Y,X), W = "  бабушка  "),
                                not(isMember(Y,Trail)).

/* Вывод списка родственников */
writeStr([],_).
writeStr([ш(Name1,Name2)|T], Родство):-write("      У   ",Name1,"  ",Родство,"  ",Name2),nl,
                                                writeStr(T, Родство).

/* Вывод  родственников 2 */

 writeR([]).
 writeR([X,Y,Z|T]):-write(X,Y,Z),nl, writeR([Z|T]).
