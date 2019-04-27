import math

max_score = 5
min_score = 1


def calculate_metrics(query_scores, metrics_f):
    """
    Вычисляет заданную метрику от всех запросов
    :param queries_scores: список оценок за все запросы
    :param metrics_f: функция, задающая метрику от оценок за результаты одного поискового запроса
    :return: значения метрик за уровни 1,3,5
    """
    return round(metrics_f(query_scores, 1), 3), round(metrics_f(query_scores, 3), 3), round(metrics_f(query_scores, 5), 3)