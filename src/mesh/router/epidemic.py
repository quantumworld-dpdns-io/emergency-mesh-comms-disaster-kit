from __future__ import annotations


class EpidemicRouter:
    @staticmethod
    def missing_bundles(local_summary: set[str], remote_summary: set[str]) -> set[str]:
        return local_summary - remote_summary
