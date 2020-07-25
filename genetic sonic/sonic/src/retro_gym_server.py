#!/usr/bin/env python
# license removed for brevity
import rospy
import retro
import cv2
import numpy as np
import imutils
import Genetic as ga
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist
from Genetic import Gene
from Genetic import Chromosome

#check world debug

env = retro.make(game='SonicTheHedgehog-Genesis', state='GreenHillZone.Act1')
image_pub = rospy.Publisher('world_observation/image_raw', CompressedImage, queue_size=10)
counter = 0
counter_mov = 0 #Contador de movimiento
count_indi = 0 #Contador del numero de individuos
count_generation = 1
xpos_max = 0
fitness = 0

n_poblacion = ga.poblacion

first_generation = True
len_gene = Gene().len_gene
first_individuo = True

first_poblacion = ga.generate_population()
individuo = first_poblacion.pop(0)
mov_individuo = individuo.Genes
# mov = mov.generate_parent()

poblacion = [None] * ga.poblacion
temp_poblacion = [None] * ga.poblacion
limit = 0

#avanzen el codigo
def moverse(vel_msg):
    global mov_individuo, counter_mov
    # 0 0 0 1
    for i in mov_individuo:
        if mov_individuo[0][0] == 1:
            vel_msg.linear.x = -1
        if mov_individuo[0][2] == 1:
            vel_msg.linear.y = 1
        if mov_individuo[0][0] == 1:
            vel_msg.linear.x = 1
        if mov_individuo[0][1] == 1:
            vel_msg.linear.y = -1
        mov_individuo = np.delete(mov_individuo, 0, 0)
        counter_mov += 1
        return vel_msg
    

def key_action(vel_msg):
    #["B", "A", "MODE", "START", "UP"genes, "DOWN", "LEFT", "RIGHT", "C", "Y", "X", "Z"]
    keys = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    vel_msg = moverse(vel_msg)
    if vel_msg.linear.x is not None:
        if vel_msg.linear.x == -1:
            keys[6] = 1
        if vel_msg.linear.y == 1:
            keys[0] = 1
        if vel_msg.linear.x == 1:
            keys[7] = 1
        if vel_msg.linear.y == -1:
            keys[5] = 1
        return keys

def pub_image(env):
    #GYM RENDER AS IMAGE
    img = env.render(mode='rgb_array')
    # ROTATE THE IMAGE THE MATRIX IS 90 grates and mirror
    img = np.flipud(np.rot90(img))
    image_np = imutils.resize(img, width=500)
    # Publish new image
    msg = CompressedImage()
    msg.header.stamp = rospy.Time.now()
    msg.format = "jpeg"
    compressed_images = cv2.imencode('.jpg', image_np)
    msg.data = np.array(compressed_images[1]).tostring()
    image_pub.publish(msg)

def open_world(vel_msg):
    global counter, xpos_max, fitness, limit, first_generation, first_poblacion
    global counter_mov, mov_individuo, count_indi, poblacion, individuo
    global first_individuo, count_generation, temp_poblacion
    pub_image(env)
    if first_generation:
        if count_indi < n_poblacion:
            if counter_mov == len_gene:
                if len(first_poblacion) > 0:
                    print("Fitness Agregado")
                    poblacion[count_indi] = Chromosome(individuo.Genes, fitness, xpos_max)
                    # if len(first_poblacion) > 0:
                    individuo = first_poblacion.pop(0)
                    mov_individuo = individuo.Genes
                    counter_mov = 0
                    xpos_max = 0
                    fitness = 0
                    done = True
                    env.reset()

                count_indi += 1
            else:
                action = key_action(vel_msg)
                obs, rew, done, info = env.step(action)
                xpos = info['x']
                if xpos > xpos_max:
                    xpos_max = xpos
                    fitness += 15

                if individuo.pos_max == 9546:
                    print("Objetivo alcanzado")
            ga.display(count_generation, count_indi, individuo, fitness, counter_mov)
        else:
            first_generation = False
            count_indi = 0
            count_generation += 1
            done = True
            env.reset()
    else:
        if first_individuo:
            print("Fase de Mutación y Crossover")
            parent = ga.selection_parent(poblacion)
            nuevos_poblacion = ga.crossover(parent)
            mutados = ga.mutation(nuevos_poblacion)
            poblacion = mutados
            individuo = poblacion.pop(0)
            mov_individuo = individuo.Genes
            first_individuo = False

        if count_indi < n_poblacion:
            if counter_mov == len_gene:
                if len(poblacion) > 0:
                    print("Fitness Agregado")
                    temp_poblacion[count_indi] = Chromosome(individuo.Genes, fitness, xpos_max)
                    individuo = poblacion.pop(0)
                    mov_individuo = individuo.Genes
                    counter_mov = 0
                    xpos_max = 0
                    fitness = 0
                    done = True
                    env.reset()
                count_indi += 1
            else:
                action = key_action(vel_msg)
                obs, rew, done, info = env.step(action)

                xpos = info['x']
                if xpos > xpos_max:
                    xpos_max = xpos
                    fitness += 15

                if individuo.pos_max == 9546:
                    print("Objetivo alcanzado")

            ga.display(count_generation, count_indi, individuo, fitness, counter_mov)

        else:
            first_individuo = True
            count_indi = 0
            count_generation += 1
            done = True
            env.reset()
            poblacion = temp_poblacion

if __name__ == '__main__':
    rospy.init_node('world_observation_server', anonymous=True)
    try:
        rospy.Subscriber("world_observation/cmd_vel", Twist, open_world)
        env.reset()
        pub_image(env)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
