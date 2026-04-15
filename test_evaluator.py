import requests

url = "http://127.0.0.1:8000/evaluate"

payload = {
    "question": "Explain binary search and its time complexity.",
    "answer": "Binary search divides the array into halves and checks middle element. Time complexity is O(log n).",
    "topic": "Data Structures and Algorithms",
    "max_marks": 5
}

response = requests.post(url, json=payload)

print("Status:", response.status_code)
print("Response:")
print(response.json())