from ast import main
import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pyttsx3
import webbrowser
import speech_recognition as sr
import datetime
import os
import wikipedia
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
#print (voices)
engine.setProperty('voice',voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour=int(datetime.datetime.now().hour)    
    if hour>=0 and hour <12:
         speak("Good Morning")
    elif hour>=12 and hour<18:
         speak("Good afternoon")
    else :
         speak("Good evening")

    speak("i am Robin . How can i help you" )

def takecommand():
#it is converting voice to string
     r=sr.Recognizer()
     try:

          with sr.Microphone() as source :

               print("Listening ......") 
               speak("listening")
               r.energy_threshold = 100 
               r.pause_threshold  =  1 
               audio=r.listen(source)

     
               print("Recognizing")     
               query = r.recognize_google(audio)
               print(f"user said: {query}\n")

     except Exception as e:
          print("say that again please....")   
          speak("say that again please") 
          return "none"
     return query

query=takecommand().lower()
sentence=[str(query)]    
analyser=SentimentIntensityAnalyzer()
for i in sentence:
    a=analyser.polarity_scores(i)
    print(a)
movie_data=pd.read_csv(r"C:\Users\sagni\Downloads\b68782efa49a16edaf07dc2cdaa855ea-0c794a9717f18b094eabab2cd6a6b9a226903577\b68782efa49a16edaf07dc2cdaa855ea-0c794a9717f18b094eabab2cd6a6b9a226903577\movies.csv.csv")
#print(movie_data.head())
if a['compound']  <0 :
     b=0
     for k in movie_data['Genre']:
          b=b+1
          if 'Comedy' in k:
               movie_name=movie_data['Series_Title'][b]

if a['compound']  ==0 :
     b=0
     for k in movie_data['Genre']:
          b=b+1
          if 'Drama' in k:
               movie_name=movie_data['Series_Title'][b]  

if a['compound'] >0 :
     b=0
     for k in movie_data['Genre']:
          b=b+1
          if 'Romance' in k:
               movie_name=movie_data['Series_Title'][b]                              

print(movie_name)
#movie_name=input("Enter a movie name of your choice")
#print(movie_data.shape)
selected_features=['Genre','Director']
for feature in selected_features:
    movie_data[feature]=movie_data[feature].fillna('')
combined_features=movie_data['Genre']+' '+movie_data['Director']
#print(combined_features)
vectorizer=TfidfVectorizer()
feature_vectors=vectorizer.fit_transform(combined_features)#this converts words to neumericals

#print(feature_vectors)
similarity=cosine_similarity(feature_vectors)
#print(similarity)
#print(similarity.shape)
#movie_name=input("Enter a movie name of your choice")
list_of_all_titles=movie_data['Series_Title'].tolist()
#print(list_of_all_titles)
find_close_match=difflib.get_close_matches(movie_name,list_of_all_titles)
#print(find_close_match)
close_match=find_close_match[0]
index_of_movie=list_of_all_titles.index(close_match)
#print(index_of_movie)
similarity_score=list(enumerate(similarity[index_of_movie]))
#print(similarity_score)
len(similarity_score)
sorted_similar_movie=sorted(similarity_score, key =lambda x:x[1],reverse=True)
#print(sorted_similar_movie)
print("MOvie suggested for you:")
i=1
for movie in sorted_similar_movie:
    index=movie[0]
    title_from_index=list_of_all_titles[index]
    if i<=5:
        print(i,". ",title_from_index)
        i+=1


    

