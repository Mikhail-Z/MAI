% �����:
% ����: 06.12.2015
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

 ������(����, ������,������):- ������(����, ������, ������,[]).

    ������(����, ������,[������,����|L1],L1):-child(����, ������).
    ������(����, ������, L,L1):- child(����, ��������),
                                                ������(��������, ������,L,[��������,����|L1]).


 �������(����, �������):- male(�������), child(����, ��������),child(��������, �������).

  �������(����, �������):- female(�������), child(����, ��������),child(��������, �������).

����(����, ����):-  male(����), child(����, ����).

����(����, ����):-  female(����), child(����, ����).

����(����, ����):-  male(����), child(����, Parent ),child(����,Parent ) , ����=\=����.


������(����, ������):-  female(������), child(����, Parent ),child(������,Parent ) , ����=\=������.


�����(����, �����):-  male(����), female(����),
                                    child(Child ,����),
                                    child(Child ,���� ),
                                   child(����, Parent ),
                                   child(����� ,Parent ),
                                    male(�����).

  /*�� ������ ��������� ������������� ��������*/
    ����������([],[]).
     ����������([H|T],[H|T1]):- ����������(T,T1), not(member(H,T1)),!.
     ����������([H|T],T1):- ����������(T,T1).

 /* ����� ����� ������� � �������  */
  go(Start, Goal, R):-  go2([[Start]],Goal, R).

  go2([First|Rest], Goal,First):-First = [Goal|_].
  go2([[Last|Trail]|Rest], Goal,Trace):-
                                            findall([Z,W,Last|Trail], nextnode(Last,Trail,Z),List),
                                        append(List,Rest,NewTraces), go2(NewTraces, Goal, Trace).
not_member(X,[]).
not_member(X,[H|T]);-X=\=H,!,fail,not_member(X,T).

  nextnode(X,Trail,Y):- child(X,Y), not_member(Y,Trail),write('�������').
  nextnode(X,Trail,Y):-child(Y,X),/*W="��������",*/ not_member(Y,Trail),write('��������').


      nextnode1(X,Trail,Y,W):- (child(X,Y),W="   �������   ";
                                        ����(Y,X),W="   ����   ";
                                        ����(Y,X), W="  ����  ";
                                        �����(Y,X), W ="  �����  ";
                                        ������(Y,X), W="  ������ ";
                                        ����(Y,X),W="  ����   ";
                                        �������(Y,X), W="  �������  ";
                                        �������(Y,X), W = "  �������  "),
                                not(isMember(Y,Trail)).

/* ����� ������ ������������� */
writeStr([],_).
writeStr([�(Name1,Name2)|T], �������):-write("      �   ",Name1,"  ",�������,"  ",Name2),nl,
                                                writeStr(T, �������).

/* �����  ������������� 2 */

 writeR([]).
 writeR([X,Y,Z|T]):-write(X,Y,Z),nl, writeR([Z|T]).
