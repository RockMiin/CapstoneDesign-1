import matplotlib.pyplot as plt
import matplotlib.animation as animation

class RealtimeSensing:

    def __init__(self):
        self.fire_client = None
        self.moisture_client = None
        self.lightMotion_client = None
        self.BUFSIZE = 1024
        self.packet = bytes([0x00, 0x00])
        self.visualizing = False

    def visualization(self):

        fig = plt.figure(figsize=(15, 12))
        ax_fire = fig.add_subplot(2, 2, 1)
        ax_moisture = fig.add_subplot(2, 2, 2)
        ax_light = fig.add_subplot(2, 2, 3)
        ax_motion = fig.add_subplot(2, 2, 4)

        # plot range
        X = list(range(0, 200))
        X_len = len(X)

        Y_fire = [0] * X_len
        Y_moisture = [0] * X_len
        Y_light = [0] * X_len
        Y_motion = [0] * X_len

        Y_range_fire = [-1000, 1000]
        Y_range_moisture = [-700, 700]
        Y_range_light = [-700, 700]
        Y_range_motion = [-2, 2]

        ax_fire.title.set_text("Fire Alarm")
        ax_moisture.title.set_text("Soil Moisture")
        ax_light.title.set_text("Light Power")
        ax_motion.title.set_text("Motion Detection")

        ax_fire.set_ylim(Y_range_fire)
        ax_moisture.set_ylim(Y_range_moisture)
        ax_light.set_ylim(Y_range_light)
        ax_motion.set_ylim(Y_range_motion)

        ax_fire.set_xlabel("Time")
        ax_moisture.set_xlabel("Time")
        ax_light.set_xlabel("Time")
        ax_motion.set_xlabel("Time")

        ax_fire.set_ylabel("Gas value")
        ax_moisture.set_ylabel("Moisture value")
        ax_light.set_ylabel("Light value")
        ax_motion.set_ylabel("Motion value")

        line_fire, = ax_fire.plot(X, Y_fire, color='dodgerblue')
        line_moisture, = ax_moisture.plot(X, Y_moisture, color='dodgerblue')
        line_light, = ax_light.plot(X, Y_light, color='dodgerblue')
        line_motion, = ax_motion.plot(X, Y_motion, color='dodgerblue')

        ax_fire.grid(b=True, axis='y', color='gray', alpha=0.5, linestyle='--')
        ax_moisture.grid(b=True, axis='y', color='gray', alpha=0.5, linestyle='--')
        ax_light.grid(b=True, axis='y', color='gray', alpha=0.5, linestyle='--')
        ax_motion.grid(b=True, axis='y', color='gray', alpha=0.5, linestyle='--')

        def FireSensor_animate(i, Y_fire):

            if self.fire_client is None:
                SensingVal_f = 0
            else:
                self.fire_client.send(self.packet)
                recv_f = self.fire_client.recv(self.BUFSIZE)
                
                SensingVal_f = int(recv_f.decode('utf-8'))
                print(SensingVal_f)

            Y_fire.append(SensingVal_f)
            Y_fire = Y_fire[-X_len: ]

            line_fire.set_ydata(Y_fire)

            return line_fire,

        def MoistureSensor_animate(i, Y_moisture):

            if self.moisture_client is None:
                SensingVal_m = 0
            else:
                self.moisture_client.send(self.packet)
                recv_m = self.moisture_client.recv(self.BUFSIZE)

                SensingVal_m = int(recv_m.decode('utf-8'))

            Y_moisture.append(SensingVal_m)
            Y_moisture = Y_moisture[-X_len:]

            line_moisture.set_ydata(Y_moisture)

            return line_moisture,

        def LightMotionSensor_animate(i, Y_light, Y_motion):

            if self.lightMotion_client is None:
                SensingVal_light = 0
                SensingVal_motion = 0
            else:
                self.lightMotion_client.send(self.packet)
                SensingVal_light = self.lightMotion_client.recv(self.BUFSIZE)

                self.lightMotion_client.send(self.packet)
                SensingVal_motion = self.lightMotion_client.recv(self.BUFSIZE)

            Y_light.append(SensingVal_light)
            Y_motion.append(SensingVal_motion)

            Y_light = Y_light[-X_len:]
            Y_motion = Y_motion[-X_len:]

            line_light.set_ydata(Y_light)
            line_motion.set_ydata(Y_motion)

            return line_light, line_motion

        animation.FuncAnimation(fig, FireSensor_animate, fargs=(Y_fire, ), frames=200, interval= 0.000001, blit=True)
        animation.FuncAnimation(fig, MoistureSensor_animate, fargs=(Y_moisture, ), frames=200, interval= 0.000001, blit=True)
        animation.FuncAnimation(fig, LightMotionSensor_animate, fargs=(Y_light, Y_motion, ), frames=200, interval= 0.000001, blit=True)

        plt.show()

    def set_fire_client(self, socket):
        self.fire_client = socket
        self.start_visualization()

    def set_moisture_client(self, socket):
        self.moisture_client = socket
        self.start_visualization()

    def set_lightMotion_client(self, socket):
        self.lightMotion_client = socket
        self.start_visualization()

    def start_visualization(self):
        if self.fire_client is not None or self.moisture_client is not None or self.lightMotion_client is not None:
            if self.visualizing == False:
                self.visualizing = True
                self.visualization()
                




