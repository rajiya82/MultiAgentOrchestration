import json

# Your exact intent anchors mapped to 34 distinct structural phrasing variations per category
variations = {
    "APPOINTMENT_BOOKING": [
        "I need to look for an opening to book a cleaning tomorrow morning.",
        "I need to book a slot.", "I want to change my appointment time.",
        "I need to make an appointment for next Monday.", "Appointment booking options please.",
        "Can I reserve a time slot for tomorrow?", "Schedule a meeting for 3 PM.",
        "I want to postpone my booking.", "Are there openings on Friday?",
        "Book a dental checkup for me.", "Can you reschedule my slot?",
        "Cancel my current appointment.", "Is anyone available at 10 AM?",
        "I need a clean up appointment.", "Set up a consultation for tomorrow.",
        "Can I check my booking status?", "Lock a time for a maintenance check.",
        "I need to see a doctor today.", "Book an appointment for my son.",
        "Reschedule the 2 PM session.", "Are there slots open this weekend?",
        "I want to book an interview slot.", "Change my reservation to 4 PM.",
        "I need to schedule a dynamic workflow demo.", "Is the 9 AM slot free?",
        "Book a service appointment.", "Move my booking to next month.",
        "Can I book a session now?", "I need an urgent slot today.",
        "Schedule an induction program.", "Set up a meeting with a tutor.",
        "I want to confirm my booking slot.", "Let's book a consultation.",
        "Is there an open slot for a cleaning?"
    ],
    "GENERAL_INFO": [
        "Who was the second person to walk on the moon?", "Who is the president of America?",
        "What is the meaning of life?", "How many legs does a dog have?",
        "What is the capital of Singapore?", "Explain the Retrieval-Augmented Generation concept.",
        "How far is the moon from the earth?", "What is the speed of light?",
        "Why is the sky blue?", "Tell me a fact about history.",
        "What does CI/CD mean in engineering?", "How do clouds form?",
        "What is the largest ocean on earth?", "Who wrote Romeo and Juliet?",
        "What is the function of an LLM router?", "How many planets are in our solar system?",
        "What is the tallest mountain in the world?", "Explain basic Python dictionary structures.",
        "What is the population of London?", "How does a database transaction function?",
        "What is the boiling point of water?", "Tell me about the history of computers.",
        "What is an open-source library?", "How do birds fly?",
        "What is the currency of Japan?", "Explain AWS CloudWatch log architectures.",
        "What are the benefits of using stream processing?", "Who painted the Mona Lisa?",
        "What is the difference between SQL and NoSQL?", "How many days are in a leap year?",
        "What is a standard stop sequence?", "Explain the purpose of a vector database.",
        "How do trees produce oxygen?", "What is the purpose of regular expressions?"
    ],
    "SENSITIVE_INFO": [
        "Here is my NRIC number.", "My birthday is 27/04/1982.",
        "I am living in 670617 Singapore.", "My private phone number is 91234567.",
        "Here is a copy of my passport ID data.", "My home address is Block 123 Bukit Panjang.",
        "This is my secret access credentials file.", "My financial tax file reference number is this.",
        "Here is my credit card details.", "My date of birth is April 27 1982.",
        "I live near Senja Road in Singapore.", "Here are my personal bank records.",
        "My corporate login ID token is active.", "Exposing my email address details.",
        "This is my personal tracking number.", "Here is my security profile questionnaire data.",
        "My identity card number is attached.", "My mobile number is listed below.",
        "I need to input my private health log details.", "Here is my salary statement voucher.",
        "This is my confidential identification pass.", "My registration file contains my NRIC.",
        "I live at 8A Marina Blvd workspace.", "Exposing my secure database credentials keys.",
        "Here is my driving license information.", "My personal email address is test@domain.com.",
        "This holds my biometric scanning reference data.", "My corporate authentication code is this.",
        "Here is my residential postal code.", "My certificate file lists my full name.",
        "This is my private personal identity details.", "My passport expires next year.",
        "Here is my employee reference number.", "My account number is active."
    ]
}

output_file = "train_file.jsonl"

with open(output_file, "w", encoding="utf-8") as f:
    for intent, prompts in variations.items():
        for prompt in prompts:
            line_data = {
                "schemaVersion": "bedrock-conversation-2024",
                "messages": [
                    {"role": "system", "content": "You are a precise intent classifier."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": f"USER_INTENT: {intent}"}
                ]
            }
            f.write(json.dumps(line_data) + "\n")

print(f"🎉 Success! Generated exactly 102 valid JSONL rows inside '{output_file}'!")