import math


def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


if __name__ == "__main__":
    vector_a = [1, 2, 3]

    vector_b = [1, 2, 3]
    vector_c = [-1, -2, -3]
    vector_d = [10, 20, 30]

    print("A vs B:", cosine_similarity(vector_a, vector_b))
    print("A vs C:", cosine_similarity(vector_a, vector_c))
    print("A vs D:", cosine_similarity(vector_a, vector_d))