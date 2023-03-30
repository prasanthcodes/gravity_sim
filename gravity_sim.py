import pygame
import random
import math
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#---input params---
fps_rate=30
slow_rate=1.0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
max_time=1e3

g_acceleration = -9.8


class ball:
    def __init__(self,radius,initial_pos):
        self.radius=radius
        self.initial_pos=list(initial_pos)#its a list of x and y value. e.g [x,y]
        self.current_pos = list(initial_pos)
        self.g_acceleration=-9.8
        self.slow_rate=1.0
        self.top_limit=0
        self.bottom_limit=0
        self.left_limit=0
        self.right_limit=0
        self.coefficient_of_restitution=1
        self.motion_flag=1
        self.time_count=0
        self.ground_hit_velocity=0
        self.v_velocity=0
        self.v_distance = 0
        self.h_velocity=0
        self.h_distance = 0
        self.initial_v_velocity=0
        self.initial_h_velocity=0
        self.last_hit_velocity=0
        self.angle=0
        self.bounce_count=0
        self.mass=1
        self.color=(255,0,0)
    def set_initial_pos(self,initial_pos):
        self.initial_pos=list(initial_pos)#its a list of x and y value. e.g [x,y]
        self.current_pos = list(initial_pos)
        self.last_hit_velocity = 0
    def set_environment_params(self,g_acceleration=-9.8,slow_rate=1.0,coefficient_of_restitution=1.0):
        self.g_acceleration=g_acceleration
        self.slow_rate=slow_rate
        self.coefficient_of_restitution=coefficient_of_restitution
        self.last_hit_velocity = 0
    def set_velocity_params1(self,v_velocity,h_velocity):
        self.initial_v_velocity=v_velocity
        self.initial_h_velocity=h_velocity
        self.h_velocity=self.initial_h_velocity
        self.last_hit_velocity = 0
    def set_velocity_params2(self,velocity,angle):
        self.initial_v_velocity=velocity*math.sin(angle*math.pi/180)
        self.initial_h_velocity=velocity*math.cos(angle*math.pi/180)
        self.h_velocity=self.initial_h_velocity
        self.last_hit_velocity = 0
    def set_bounding_limits(self,top,bottom,left,right):
        # self.top_limit=top
        # self.bottom_limit=bottom
        # self.left_limit=left
        # self.right_limit=right
        # ---set limits considering circle radius (ball)---
        self.top_limit=top+self.radius
        self.bottom_limit=bottom-self.radius
        self.left_limit=left+self.radius
        self.right_limit=right-self.radius
    def stop_the_motion(self):
        self.motion_flag=0
    def stop_it_at_min_velocity(self,velocity_limit):
        if abs(self.v_velocity)<velocity_limit: self.motion_flag=0
    def update(self):
        if self.motion_flag==1:
            self.v_velocity = self.initial_v_velocity+self.g_acceleration * self.time_count
            self.v_distance = self.initial_v_velocity*self.time_count+0.5 * self.g_acceleration * self.time_count * self.time_count
            self.current_pos[1] = self.initial_pos[1] - self.v_distance
            self.current_pos[0]=self.current_pos[0]+self.h_velocity/self.slow_rate
            # print(self.v_distance)
            self.time_count += (1/self.slow_rate)

            #---if ball hit the bounding limits (bottom,top,left,right) ---
            if (self.current_pos[1]  > self.bottom_limit):
                # to find time of hit
                sol1=(-self.initial_v_velocity+math.sqrt(self.initial_v_velocity**2+2*-self.g_acceleration*(self.bottom_limit-self.initial_pos[1])))/(self.g_acceleration)
                sol2=(-self.initial_v_velocity-math.sqrt(self.initial_v_velocity**2+2*-self.g_acceleration*(self.bottom_limit-self.initial_pos[1])))/(self.g_acceleration)
                self.v_velocity = self.initial_v_velocity + self.g_acceleration * sol2
                # stop the ball motion if min velocity reaches
                self.stop_it_at_min_velocity( velocity_limit=1)
                self.current_pos[1]=self.bottom_limit
                self.initial_v_velocity=-1*self.v_velocity
                self.initial_v_velocity=self.initial_v_velocity*self.coefficient_of_restitution
                self.h_velocity = self.h_velocity * self.coefficient_of_restitution
                # print(self.h_velocity)
                self.initial_pos[1]=self.bottom_limit
                self.time_count=0
                self.bounce_count+=1
            if (self.current_pos[1]  < self.top_limit):
                self.current_pos[1]=self.top_limit
                self.initial_v_velocity=-1*self.v_velocity
                self.initial_v_velocity = self.initial_v_velocity * self.coefficient_of_restitution
                self.h_velocity = self.h_velocity * self.coefficient_of_restitution
                self.initial_pos[1]=self.top_limit
                self.time_count=0
            if (self.current_pos[0]  >= self.right_limit):
                self.current_pos[0]=self.right_limit
                self.h_velocity=-1*self.h_velocity
                self.h_velocity = self.h_velocity * self.coefficient_of_restitution
                self.initial_pos[0]=self.right_limit
            if (self.current_pos[0]  <= self.left_limit):
                self.current_pos[0]=self.left_limit
                self.h_velocity=-1*self.h_velocity
                self.h_velocity = self.h_velocity * self.coefficient_of_restitution
                self.initial_pos[0]=self.left_limit

# N_balls=1
# all_balls=[]
# for i in range(N_balls):
#     ball_object=ball(radius=5,initial_pos=[300,300])
#     ball_object.color=(0,0,255)
#     ball_object.set_environment_params(g_acceleration=g_acceleration,slow_rate=slow_rate,coefficient_of_restitution=0.8)
#     ball_object.set_velocity_params2(velocity=50, angle=0)
#     ball_object.set_bounding_limits(top=0,bottom=SCREEN_HEIGHT,left=0,right=SCREEN_WIDTH)
#     all_balls.append(ball_object)

N_balls=10
all_balls=[]
for i in range(N_balls):
    ball_object=ball(radius=5,initial_pos=[300,300])
    ball_object.color=(100+100*random.random(),100+100*random.random(),100+100*random.random())
    ball_object.set_environment_params(g_acceleration=g_acceleration,slow_rate=slow_rate,coefficient_of_restitution=0.8+0.17*random.random())
    ball_object.set_velocity_params2(velocity=10+50+random.random(), angle=0+360*random.random())
    ball_object.set_bounding_limits(top=0,bottom=SCREEN_HEIGHT,left=0,right=SCREEN_WIDTH)
    all_balls.append(ball_object)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

time_count=1
running = True
clock = pygame.time.Clock()
# Run until the user asks to quit
while running:

    #----window closing conditions-------
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
        # if maximum time reaches, stop the loop
        if time_count > max_time:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))
    # Draw all balls
    for i in range(N_balls):
        c1=pygame.draw.circle(screen, all_balls[i].color, (all_balls[i].current_pos[0], all_balls[i].current_pos[1]), all_balls[i].radius)
    c1 = pygame.draw.circle(screen, (255, 0, 0), [300,300],3)
    # update ball positions
    for i in range(len(all_balls)):
        all_balls[i].update()
    # Flip the display
    pygame.display.flip()
    time_count+=1
    # This limits the while loop to a max of 'fps_rate' times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(fps_rate)
    fps=clock.get_fps()
    # print('time_count=%d,fps=%d'%(time_count,fps))
# Done! Time to quit.
pygame.quit()


