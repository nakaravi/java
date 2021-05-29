

#clcoding
import turtle 
 
t = turtle.Turtle() 
t.speed(20) 
a = ["violet","indigo","blue","green","yellow","orange","red"] 
 
for i in range(50): 
    k = i%7 
    t.color(a[k]) 
    t.circle(120) 
    t.right(10)
