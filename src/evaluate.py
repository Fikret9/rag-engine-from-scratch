import os


def evaluate(test_cases, provider,retriever):
    passed = 0
    failed = 0
    failures = []
    document = None
    text = None
    for test in test_cases:
        print("=" * 80)
        print(test["question"])

        """    Create Vector for the query """
        response = provider.embed([test["question"]])
        question_vector = response.embeddings[0]

        results = retriever.find_relevant_context(question_vector)
        print("Retriever results ")
        print(results)

        passed_test = False

        for score, text, document in results:
            print("*" * 60)

            print(repr(test["expected_document"]))
            print(repr(document))

            print(f"Expected: {repr(test['expected_contains'])}")
            print(f"Text contains? {text[:200], "..."}")
            print(repr(test["expected_contains"]))
            print(text.find(test["expected_contains"]))
            print(len(text))
            print(len(text.split()))

            if (
                os.path.normpath(document) == os.path.normpath(test["expected_document"])
                and test["expected_contains"] in text
            ):
                passed_test = True
                break

        if passed_test:
           passed +=1
           print(
                 f"PASS\n"
                 f"Question: {test['question']}\n"
                 f"Retrieved: {document}\n"
                )
        else:
          failed +=1
          print(
                f"FAIL\n"
                f"Expected: {test['expected_document']}\n"
                f"Retrieved: {document}\n\n"
            )

    total = passed + failed
    accuracy = (passed / total * 100) if total else 0

    print("=" * 21)
    print("Evaluation Summary")
    print("=" * 21)
    print()
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Accuracy: {accuracy:.1f}%")
    print()
    print("Failures:")
    print()

    for item in failures:
        print(f"- {item}")