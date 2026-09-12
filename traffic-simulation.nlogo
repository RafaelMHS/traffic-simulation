globals [
  traffic-light-open-to
  red-throughput
  blue-throughput
  red-delay
  blue-delay
  basis-follow-up 
  increment-follow-up 
  basis-critical-gap 
  increment-critical-gap 
  basis-delay-traffic-light 
  increment-delay-traffic-light 
]

turtles-own[ 
  was-leader?
  travel-time
  crossed?
  reaction-time
  reaction-score
  stopped?
  slowness
  initial-queue-position
]

to setup
  clear-all
  resize-world -16 16 -16 16 
  set-patch-size 16
  
  ; general lane parameters
  set basis-follow-up 2
  set increment-follow-up 2
  set basis-critical-gap 4
  set increment-critical-gap 3
  set basis-delay-traffic-light 1
  set increment-delay-traffic-light 1
  
  if has-seed[
    random-seed seed
  ]
  
  ; initial state of crossing and counters
  set traffic-light-open-to "horizontal"
  set red-throughput 0
  set blue-throughput 0
  set red-delay 0
  set blue-delay 0
  
  ; pavement design
  ask patches with [pycor = 0 or pxcor = 0] [
    set pcolor gray
  ]
    
  reset-ticks
end

to go
  if method = "red light" [
    traffic-light-control
  ]
  
  spawn-red
  spawn-blue
  
  ask turtles [
    if not crossed? [
      set travel-time travel-time + 1
    ]
    
    ; verifies center crossing
    if (color = red and xcor > 0) or (color = blue and ycor < 0) [
      set crossed? true
    ]
    
    ifelse method = "stop sign"[
      stop-sign
    ] [
      traffic-light
    ]
     
    ; ends vehicle cycle and delay metrics
    if xcor >= max-pxcor or ycor <= min-pycor [
      let prob-move (1 - (slowness / 100)) 
      let ideal-time ((17 / prob-move) + 1)
      let delay (travel-time - ideal-time)
      
      if delay < 0 [ set delay 0 ] 
      
      if color = red [
        set red-throughput red-throughput + 1
        set red-delay red-delay + delay 
      ]
      
      if color = blue [
        set blue-throughput blue-throughput + 1
        set blue-delay blue-delay + delay 
      ]
    
      die
    ]
  ]
  tick
end

to spawn-red
  if random-float 100 < red-spawn and not any? turtles-on patch min-pxcor 0 [
    create-turtles 1[
      set reaction-time 0
      set shape "car"
      set color red
      set heading 90
      setxy min-pxcor 0
      set travel-time 0
      set crossed? false
      set stopped? false
      set reaction-score random-float 1
      set slowness reaction-score * 30
      set initial-queue-position 0 
    ]
  ]
end

to spawn-blue
  if random-float 100 < blue-spawn and not any? turtles-on patch 0 max-pycor[
    create-turtles 1[
      set reaction-time 0
      set shape "car"
      set color blue
      set heading 180
      setxy 0 max-pycor
      set travel-time 0
      set crossed? false
      set stopped? false
      set reaction-score random-float 1
      set slowness reaction-score * 30
      set initial-queue-position 0
    ]
  ]
end

to stop-sign
  let car-ahead? any? turtles-on patch-ahead 1
  let main-occupied? false
  let on-boundary-line? false
  
  ; check if blue vehicle is at stop line and if main road is occupied
  if color = blue and ycor = 1 [
    set on-boundary-line? true
    
    if any? turtles-on (patch-set patch 0 0 patch -1 0 patch -2 0) [
      set main-occupied? true
    ]
  ]
  
  ifelse car-ahead? or main-occupied? [
    ; stop state
    if on-boundary-line? [
      set stopped? true
      
      ifelse not car-ahead? [
        set was-leader? true
      ] [
        set was-leader? false
      ]
    ]
  ] [
    ;  main road is clear, proceed with reaction time
    if on-boundary-line? and stopped? [
      ifelse was-leader? [
        set reaction-time round (basis-critical-gap + (reaction-score * increment-critical-gap))
      ] [
        set reaction-time round (basis-follow-up + (reaction-score * increment-follow-up))
      ]
      
      set stopped? false 
    ]
    
    ifelse reaction-time > 0 [
      set reaction-time reaction-time - 1
    ] [
      if random 100 > slowness [
        forward 1
      ]
    ]
  ]
end

to traffic-light-control
  ; invert the traffic lights for each period
  if ticks mod 50 = 0 [
    ifelse traffic-light-open-to = "horizontal" [
      ask patch 0 1 [ set pcolor green ]
      ask patch -1 0 [ set pcolor red ]
      set traffic-light-open-to "vertical"
    ] [
      ask patch 0 1 [ set pcolor red ]
      ask patch -1 0 [ set pcolor green ]
      set traffic-light-open-to "horizontal"
    ]
  ]
end

to traffic-light
  let car-ahead? any? turtles-on patch-ahead 1
  let traffic-light-closed? false
  let on-boundary-line? false
  
  ; determine if vehicle is at stop line and if traffic light is red  
  if color = red and xcor = -1 [
    set on-boundary-line? true
    if traffic-light-open-to = "vertical" [
      set traffic-light-closed? true
    ]
  ]
  
  if color = blue and ycor = 1 [
    set on-boundary-line? true
    if traffic-light-open-to = "horizontal" [
      set traffic-light-closed? true
    ]
  ]
  
  ifelse car-ahead? or traffic-light-closed? [
    ; data of first stop on queue
    if initial-queue-position = 0 [
      ifelse color = red [
        set initial-queue-position abs xcor
      ] [
        set initial-queue-position abs ycor
      ]
    ]
    
    if on-boundary-line? [
      set stopped? true
    ]
  ] [
    ; reaction on traffic light opening depending on initial position
    if on-boundary-line? and stopped? [
      ifelse initial-queue-position <= 4 [
        set reaction-time round (basis-delay-traffic-light + (reaction-score * increment-delay-traffic-light))
      ] [
        set reaction-time 0 
      ]
      
      set stopped? false 
      set initial-queue-position 0 
    ]
    
    ifelse reaction-time > 0 [
      set reaction-time reaction-time - 1
    ] [
      if random 100 > slowness [
        forward 1
      ]
    ]
  ]
end