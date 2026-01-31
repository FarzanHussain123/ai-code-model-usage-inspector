STANDARDS_MAPPING = {
    "Instruction bypass attempt": {
        "nist": [
            "NIST AI RMF - Govern 1.2 (Risk Management Processes)",
            "NIST AI RMF - Protect 2.1 (System Integrity)"
        ],
        "eu_ai_act": [
            "Article 9 - Risk Management System",
            "Article 15 - Accuracy, Robustness and Cybersecurity"
        ],
        "cert": [
            "Secure Design Principle - Input Validation",
            "Secure AI - Prompt Injection Mitigation"
        ]
    },

    "Hardcoded API key detected": {
        "nist": [
            "NIST AI RMF - Protect 1.1 (Secure Development Practices)",
            "NIST AI RMF - Govern 2.3 (Data Protection)"
        ],
        "eu_ai_act": [
            "Article 10 - Data Governance",
            "Article 15 - Cybersecurity"
        ],
        "cert": [
            "Secure Coding - Secrets Management",
            "Credential Handling Best Practices"
        ]
    }
}
