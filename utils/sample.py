# utils/sample.py
"""
Sample data generation for the evaluation wizard.
"""

def generate_sample_data():
    """
    Generate ~100 sample conversation rows covering:
    - Exact matches
    - Fair paraphrases
    - Poor similarity cases
    Each entry is a dict with 'reference', 'generated', and 'human_score' fields.
    """
    import random

    # Base reference sentences
    references = [
        'Hello, how can I help you today?',
        'What is your account balance?',
        'Please provide your order number.',
        'I am sorry to hear that.',
        'Your appointment is scheduled for tomorrow at 10 AM.',
        'Can you please clarify your request?',
        'Thank you for contacting customer support.',
        'Your password has been successfully changed.',
        'I will look into this issue right away.',
        'Would you like to receive email notifications?',
        'Your refund has been processed.',
        'Please restart the application and try again.',
        'We appreciate your patience.',
        'Your subscription expires next month.',
        'How may I assist you further?',
        'The item is currently out of stock.',
        'You can track your shipment using this link.',
        'Please hold while I transfer your call.',
        'Let me check that information for you.',
        'Would you like to add insurance to your order?',
        'Your payment was successful.',
        'I did not understand your question.',
        'Please try again later.',
        'Your session has timed out.',
        'Thank you for your feedback.',
        'The temperature is set to 22 degrees.',
        'Your booking is confirmed.',
        'Please enter a valid email address.',
        'Your changes have been saved.',
        'I will send you the details via email.',
        'Can I help you with anything else?',
        'Your request has been escalated.',
        'Please update the app to the latest version.',
        'Your order is on its way.'
    ]

    data = []
    for ref in references:
        tokens = ref.split()
        # Exact match
        data.append({
            'reference': ref,
            'generated': ref,
            'human_score': 1.0
        })
        # Fair paraphrase: swap a word or add polite prefix/suffix
        paraphrase = ref.replace('please', 'kindly') if 'please' in ref.lower() else ' '.join(tokens[:3]) + '...' + ' '.join(tokens[-3:])
        data.append({
            'reference': ref,
            'generated': paraphrase,
            'human_score': 0.75
        })
        # Poor similarity: shuffle words or truncate
        shuffled = tokens.copy()
        random.shuffle(shuffled)
        poor = ' '.join(shuffled[:max(2, len(shuffled)//2)])
        data.append({
            'reference': ref,
            'generated': poor,
            'human_score': 0.3
        })

    # Ensure around 100 entries (references=34 * 3 = 102)
    random.shuffle(data)
    return data