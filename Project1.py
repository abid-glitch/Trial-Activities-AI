# DO add this command in terminal - python -m pip install textblob


from textblob import TextBlob 

print("Welcome to AI Mood Detector ")
name = input("What's your name ? ")
print(f"Nice to meet you, {name}!. Now Let's find out your mood by your sentence sentiments ?")
print("Type 'exit' to quit")

while True:
    sentence = input("Enter your sentence? ")
    if(sentence.lower() == 'exit'):
        break

    blob = TextBlob(sentence)
    sentiment = blob.sentiment.polarity

    if sentiment > 0:
        print("Positive Sentiment Detected :)) \n")

    elif sentiment < 0:
        print("Negative Sentiment Detected :((\n")
    
    else:
        print("Nuetral Sentiment Detected :|| \n")
    

