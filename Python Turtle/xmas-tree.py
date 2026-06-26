import turtle
from turtle import *

speed(100)
color("blue")
begin_fill()

fd(470)
lt(90)
fd(400)
lt(90)
fd(945)
lt(90)
fd(790)
lt(90)
fd(945)
lt(90)
fd(390)


end_fill()

lt(90)
fd(450)
lt(180)

speed(7)
color("#466f4b")
begin_fill()


fd(100)    
lt(150)
fd(90)
rt(150)
fd(60)
lt(150)
fd(60)
rt(150)
fd(40)
lt(150)
fd(80)


lt(60) 
fd(80)
lt(150)
fd(40)
rt(150)
fd(60)
lt(150)
fd(60)
rt(150)
fd(90)
lt(150)
fd(80)

end_fill()

speed(2)
color("#4c3228")
begin_fill()

rt(90)
fd(40)
lt(90)
fd(40)
lt(90)
fd(40)
lt(90)
fd(40)

end_fill()


#circle
penup()
fd(150)
rt(90)
fd(200)
pendown()


speed(100)
color("white")
begin_fill()
circle(10)
end_fill()

speed(50)
penup()
goto(200,100)
pendown()
color("white")
begin_fill()
circle(8)
end_fill()

speed(100)
penup()
goto(-200,-100)
pendown()
color("white")
begin_fill()
circle(10)
end_fill()

speed(50)
penup()
goto(-50,200)
pendown()
color("white")
begin_fill()
circle(7)
end_fill()

speed(10)
penup()
goto(300,300)
pendown()
color("white")
begin_fill()
circle(5)
end_fill()


#goto(0,0)


done()





