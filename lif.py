from PIL import Image
import matplotlib.pyplot as plt
import random

images = []
for i in range(10):
    images.append(Image.open("img"+str(i)+".png"))

vecs = []
for image in images:
    vecs.append(image.convert('1').getdata())


class LIF:

    def __init__(self):
        self.dt = .0001
        self.T = .16
        self.steps = int(self.T/self.dt)
        self.tau = .02
        self.r = 3e7
        self.e = -.07
        self.theta = -.03
        self.psc = []
        self.ipsc = []
        self.psc.append(.05)
        self.psc.append(.09)
        self.ipsc.append(.04)
        self.tau_s = .003
        self.q = 40e-12
        self.i_0 = q / tau_s
        self.voltages = [0 for i in range(self.steps)]
        self.currents = [0 for i in range(self.steps)]

        self.voltages[0] = -.07
        self.currents[0] = 0
        self.noise = [3e-9 * random.normalvariate(0, 1.5) for i in range(steps)]#random.gauss(.75, .01) for i in range(steps)]
        self.t_spike = 0
        self.arp = .01
        self.spikes = 0
        self.times = [dt*i for i in range(self.steps)]



    def simulate(self):
        for i in range(self.steps-1):
            for k in range(len(self.psc)):
                if i == int(self.psc[k] / self.dt):
                    self.currents[i] = self.currents[i] + self.i_0
            for k in range(len(self.ipsc)):
                if i == int(self.ipsc[k] / self.dt):
                    self.currents[i] = self.currents[i] - self.i_0 
           
            self.currents[i+1] = (self.currents[i] - self.dt/self.tau_s * self.currents[i])
            self.dV = (self.dt/self.tau) * (self.e-self.voltages[i]+self.currents[i]*self.r + self.noise[i]*self.r)
            #dV = (dt/tau) * (e-voltages[i] + currents[i]*r)

            
            self.voltages[i+1] = (self.voltages[i] + self.dV)

            if(self.voltages[i+1] > self.theta):
                if self.spikes > 0:
                    if(self.times[i] >= self.t_spike+self.arp):
                        self.voltages[i+1] = self.e
                        self.voltages[i] = 0
                        self.t_spike = self.times[i]
                        self.spikes += 1
                else:
                    self.voltages[i+1] = self.e
                    self.voltages[i] = 0
                    self.t_spike = self.times[i]
                    self.spikes += 1

    def plot(self):
        print len(self.times), len(self.voltages)
        plt.plot(self.times, self.voltages)
        plt.show()
        

steps = len(vecs[0]) #int(T / dt)
dt = .0001
T = steps * dt

tau = .02
r = 3e7
e = -.07
theta = -.03
psc = []
ipsc = []
pscs = []
for i in range(len(vecs)):
    pscs.append([])
    for px in vecs[i]:
        pscs[i].append(px / 255)

tau_s = .003
q = 40e-12
i_0 = q / tau_s

voltages = [0 for i in range(steps)]
currents = [0 for i in range(steps)]

voltages[0] = -.07
currents[0] = 0

noise = [3e-9 * random.normalvariate(0, 1.5) for i in range(steps)]#random.gauss(.75, .01) for i in range(steps)]
t_spike = 0
arp = .01
spikes = 0
times = [dt*i for i in range(steps)]


lif = LIF()
lif.simulate()
lif.plot()

for j in range(0):#len(vecs)):
    for i in range(steps-1):
        #for k in range(len(psc)):
         #   if i == int(psc[k] / dt):
          #      currents[i] = currents[i] + i_0
        #for k in range(len(ipsc)):
         #   if i == int(ipsc[k] / dt):
          #      currents[i] = currents[i] - i_0 
       
         
        if pscs[j][i] == 0:
            currents[i] = currents[i] + i_0
        if pscs[j][i] == 1:
            currents[i] = currents[i] - i_0

        currents[i+1] = (currents[i] - dt/tau_s * currents[i])
        dV = (dt/tau) * (e-voltages[i]+currents[i]*r + noise[i]*r)
        #dV = (dt/tau) * (e-voltages[i] + currents[i]*r)

        voltages[i+1] = (voltages[i] + dV)

        if(voltages[i+1] > theta):
            if spikes > 0:
                if(times[i] >= t_spike+arp):
                    voltages[i+1] = e
                    voltages[i] = 0
                    t_spike = times[i]
                    spikes += 1
            else:
                voltages[i+1] = e
                voltages[i] = 0
                t_spike = times[i]
                spikes += 1

    plt.plot(times, voltages)
    plt.show()

