test_cases = [

    {
        "question": "What is the vacation policy?",
        "expected_document": "data/Employee-Handbook.pdf",
        "expected_contains": "all leaves of absence are subject to the approval of the department head"
    },

    {
        "question": "How many vacation hours do full-time salaried employees receive?",
        "expected_document": "data/Employee-Handbook.pdf",
        "expected_contains": "90 hours per year"
    },
    {
        "question": "What's the vacation limit?",
        "expected_document": "data/Employee-Handbook.pdf",
        "expected_contains": "twice the yearly"
    }

]