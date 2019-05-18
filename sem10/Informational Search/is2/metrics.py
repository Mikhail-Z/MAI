import math
import numpy as np
from functools import reduce


def mult(elements):
    return reduce(lambda x, y: x * y, elements)


def err(query_scores, n):
    """
    Вычисляет метрику Err@n
    :param query_scores: оценки выдачи на запрос
    :param n: кол-во рассматриваемых результатов поиска
    :return: значение метрики
    """
    max_score = max(query_scores[:n])
    scores = (np.power(2, np.array(query_scores[:n])) - 1) / np.power(2, max_score)
    error = 0
    r = 1
    p = 1
    for score in scores:
        error += p * score / r
        p = p * (1-score)
        r += 1
    return error


def dcg(query_scores, n):
    """
    Вычисляет метрику DCG@n
    :param query_scores: список оценок за результаты поисковой выдачи
    :param n: кол-во рассматриваемых результатов поиска
    :return: значение метрики
    """
    return sum(map(lambda elem: (math.pow(2, elem[1]) - 1) / math.log(elem[0] + 2, 2), list(enumerate(query_scores[:n]))))


def ndcg(query_scores, n):
    """
    Вычисляет нормализованную метрику DCG@n
    :param query_scores: список оценок за результаты поисковой выдачи
    :param n: кол-во рассматриваемых результатов поиска
    :return: значение метрики
    """
    idcg = dcg(sorted(query_scores, reverse=True), n)
    return dcg(query_scores, n) / idcg


def p(query_scores, n):
    """
     Вычисляет значение метрики P@n
    :param query_scores:
    :param n:
    :return:
    """
    return sum(query_scores[:n]) / n