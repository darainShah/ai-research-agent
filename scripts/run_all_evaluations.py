import subprocess
import sys


EVALUATIONS = [
    ("Retrieval Evaluation", "scripts.evaluate_retrieval"),
    ("Reranker Evaluation", "scripts.evaluate_reranker"),
    ("RAG Evaluation", "scripts.evaluate_rag"),
    ("Unanswerable Evaluation", "scripts.evaluate_unanswerable"),
]


def main():
    print("\n" + "=" * 70)
    print("AI RESEARCH AGENT - COMPLETE EVALUATION")
    print("=" * 70)

    for name, module in EVALUATIONS:
        print("\n" + "#" * 70)
        print(f"# {name}")
        print("#" * 70)

        result = subprocess.run(
            [sys.executable, "-m", module],
            check=False
        )

        if result.returncode != 0:
            print(f"\n❌ {name} FAILED")
            print(f"Exit code: {result.returncode}")
            sys.exit(result.returncode)

        print(f"\n✅ {name} COMPLETED")

    print("\n" + "=" * 70)
    print("ALL EVALUATIONS COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()
