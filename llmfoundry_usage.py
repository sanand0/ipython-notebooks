# /// script
# requires-python = ">=3"
# dependencies = [
#     "pandas",
#     "pyarrow",
#     "marimo",
#     "requests",
#     "openpyxl",
# ]
# ///

import marimo

__generated_with = "0.9.1"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md(
        r"""
        # LLM Foundry Usage

        This app calculates the [LLM Foundry](https://llmfoundry.straive.com/) usage over the last 30 days.

        Get `darwinbox.parquet` via:

        ```
        rsync -avzP ubuntu@gramener.com:/mnt/gramener/apps/learn.gramener.com.v1/people/darwinbox.parquet
        ```

        Then run this notebook. It will create an `llmfoundry-metrics.xlsx` that lists the
        """
    )
    return


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import requests

    stats = requests.get("https://llmfoundry.straive.com/log/stats").json()
    users = {row["email"] for row in stats["users-by-date"]}
    return mo, pd, requests, stats, users


@app.cell
def __(pd):
    from typing import Dict, Set

    def get_all_reports(manager: str, hierarchy: Dict[str, Set[str]]) -> Set[str]:
        """Recursively get all direct and indirect reports for a manager."""
        reports = hierarchy.get(manager, set())
        for report in list(reports):
            reports |= get_all_reports(report, hierarchy)
        return reports


    def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate metrics for each manager."""
        hierarchy = df.groupby("direct_manager_email")["company_email_id"].apply(set).to_dict()

        results = []
        for manager in df["direct_manager_email"].unique():
            reports = get_all_reports(manager, hierarchy)
            results.append(
                {
                    "direct_manager_email": manager,
                    "report_count": len(reports),
                    "llmfoundry_sum": df[df["company_email_id"].isin(reports)][
                        "llmfoundry_used"
                    ].sum(),
                }
            )

        return pd.DataFrame(results)
    return Dict, Set, calculate_metrics, get_all_reports


@app.cell
def __(calculate_metrics, pd, users):
    df = pd.read_parquet("darwinbox.parquet")
    df["direct_manager_email"] = df["direct_manager_email"].str.lower()
    df["company_email_id"] = df["company_email_id"].str.lower()
    df["llmfoundry_used"] = df["company_email_id"].isin(users).astype(int)
    calculate_metrics(df).to_excel("llmfoundry-metrics.xlsx", index=False)
    return (df,)


if __name__ == "__main__":
    app.run()
