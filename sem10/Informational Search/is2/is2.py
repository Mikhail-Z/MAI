from core import *
from metrics import *
import csv
import sys


def parse_csv_file(filename):
    scores = []
    with open(filename, "r") as f:
        for line in f:
            scores.append(list(map(int, line.split(",")[1:])))
    return scores


def write_to_csv_file(metrics, filename):
    with open(filename, "w") as f:
        writer = csv.DictWriter(f, ["p@1", "p@3", "p@5", "dcg@1", "dcg@3", "dcg@5", "ndcg@1", "ndcg@3", "ndcg@5", "err@1", "err@3", "err@5"])
        writer.writeheader()
        for i in range(len(queries_scores)):
            writer.writerow({
                "p@1": metrics[i]["p"][0],
                "p@3": metrics[i]["p"][1],
                "p@5": metrics[i]["p"][2],
                "dcg@1": metrics[i]["dcg"][0],
                "dcg@3": metrics[i]["dcg"][1],
                "dcg@5": metrics[i]["dcg"][2],
                "ndcg@1": metrics[i]["ndcg"][0],
                "ndcg@3": metrics[i]["ndcg"][1],
                "ndcg@5": metrics[i]["ndcg"][2],
                "err@1": metrics[i]["err"][0],
                "err@3": metrics[i]["err"][1],
                "err@5": metrics[i]["err"][2],
            })


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Enter filename after script name")
        sys.exit()
    filename = sys.argv[1]
    queries_scores = parse_csv_file(filename)
    out_filename = "out_" + filename
    metrics_results = []
    for query_scores in queries_scores:
        metrics_results.append({
            "p": calculate_metrics(query_scores, p),
            "dcg": calculate_metrics(query_scores, dcg),
            "ndcg": calculate_metrics(query_scores, ndcg),
            "err": calculate_metrics(query_scores, err)
        })

    write_to_csv_file(metrics_results, out_filename)
