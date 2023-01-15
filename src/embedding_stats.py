def print_stats(pages):
    stats = EmbeddingStats(pages)
    print(
        'Embedding {} characters, as {} pages, for ~${:0.2f}.'.format(
            stats.num_chars, stats.num_pages, stats.cost
        )
    )


class EmbeddingStats:
    def __init__(self, pages):
        text = ''.join(pages)
        self.num_chars = len(text)
        self.num_pages = len(pages)
        self.cost = self.num_chars / 4 / 1000 * 0.0004
