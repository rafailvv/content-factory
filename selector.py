class Selector:
    def __init__(self, fetcher, limit):
        self.limit = limit
        self.fetcher = fetcher

    async def channel_baseline(self, channel):
        recent = await self.fetcher.fetch_latest(channel, self.limit)
        view_list = []
        reaction_list = []

        for p in recent:
            view = p.get("views") or 0
            view_list.append(view)

            reaction = p.get("reactions") or 0
            if reaction > 0 and view > 0:
                reaction_list.append(reaction / view)

        avg_view = (sum(view_list) / len(view_list)) if view_list else 0
        avg_reaction = (sum(reaction_list) / len(reaction_list)) if reaction_list else 0

        return avg_reaction, avg_view

    async def channel_top(self, post):
        scored = []
        baseline = {}

        for p in post:
            ch = p["channel"]
            if ch not in baseline:
                baseline[ch] = await self.channel_baseline(ch)

            avg_reaction, avg_view = baseline[ch]
            view = p.get("views") or 0
            reaction = p.get("reactions") or 0

            if avg_reaction > 0:
                score = (reaction / view) / avg_reaction if view > 0 else 0
            else:
                score = view / avg_view if avg_view > 0 else 0

            scored.append((score, p))

        # scored = sorted(scored)
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1] if scored else {}



